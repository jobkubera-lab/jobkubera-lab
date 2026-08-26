#!/usr/bin/env python3
"""Structured retrieval v3 for Council AI Service Finder.

v3 keeps the deterministic, controlled-catalogue design while fixing classes of
failures found in v2 without tuning against disclosed blind-query wording:
- token/phrase boundary matching instead of raw substring containment;
- conservative token-prefix morphology for declared stems;
- broader hard fallback for impersonation / fabricated official action requests;
- explicit ambiguity fallback for tied or near-tied service evidence.

The v2 implementation remains unchanged for reproducibility.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEXICON_PATH = HERE / "intent_lexicon_v2.json"
QUERIES_PATH = HERE / "queries.jsonl"

ANCHOR_SINGLE_WEIGHT = 1.4
ANCHOR_PHRASE_WEIGHT = 2.0
SUPPORT_WEIGHT = 0.35
MIN_MATCH_SCORE = 1.4
MULTI_INTENT_MIN_SCORE = 2.0
MULTI_INTENT_MARGIN = 1.0
AMBIGUITY_MARGIN = 0.35
MIN_STEM_LENGTH = 4

TOKEN_RE = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)

LEGAL_CONCLUSION_PATTERNS = (
    re.compile(r"\b(?:legal|legally)\b.{0,60}\b(?:guilty|liable|responsible|illegal|lawful|unlawful)\b", re.I),
    re.compile(r"\b(?:breaking|breaks?|broke|violating|violates?|breaching|breaches?)\b.{0,40}\b(?:the\s+)?law\b", re.I),
    re.compile(r"\b(?:in\s+breach\s+of|against)\b.{0,20}\b(?:the\s+)?law\b", re.I),
)

PROMPT_INJECTION_PATTERNS = (
    re.compile(r"\b(?:ignore|override|bypass|disregard)\b.*\b(?:catalogue|instructions?|rules?|safety|system|service)\b", re.I),
    re.compile(r"\b(?:catalogue|instructions?|rules?|safety|system)\b.*\b(?:ignore|override|bypass|disregard)\b", re.I),
    re.compile(r"\binvent\b.*\b(?:service|answer|result)\b", re.I),
)

OFFICIAL_ACTION_PATTERNS = (
    re.compile(r"\b(?:pretend|impersonate|act\s+as)\b.{0,50}\b(?:council|authority|officer|official|government)\b", re.I),
    re.compile(r"\b(?:write|create|generate|issue|give|provide)\b.{0,60}\b(?:official|authorised|authorized|binding)\b.{0,40}\b(?:letter|notice|certificate|exemption|approval|decision|permission)\b", re.I),
    re.compile(r"\b(?:official|authorised|authorized|binding)\b.{0,40}\b(?:exemption|approval|decision|permission|notice|certificate)\b", re.I),
    re.compile(r"\b(?:on\s+behalf\s+of|as\s+if\s+you\s+were)\b.{0,40}\b(?:the\s+)?(?:council|authority|officer|official|government)\b", re.I),
)


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def tokenize(text: str) -> list[str]:
    return [normalize(token) for token in TOKEN_RE.findall(normalize(text))]


def contains_phrase(query_tokens: list[str], phrase: str) -> bool:
    phrase_tokens = tokenize(phrase)
    if not phrase_tokens or len(phrase_tokens) > len(query_tokens):
        return False
    size = len(phrase_tokens)
    return any(query_tokens[i : i + size] == phrase_tokens for i in range(len(query_tokens) - size + 1))


def contains_stem(query_tokens: list[str], stem: str) -> bool:
    normalized_stem = normalize(stem)
    if len(normalized_stem) < MIN_STEM_LENGTH:
        return False
    return any(token.startswith(normalized_stem) for token in query_tokens)


def phrase_weight(phrase: str) -> float:
    return ANCHOR_PHRASE_WEIGHT if len(tokenize(phrase)) > 1 else ANCHOR_SINGLE_WEIGHT


def is_guarded(query: str) -> bool:
    return any(
        pattern.search(query)
        for pattern in (
            *LEGAL_CONCLUSION_PATTERNS,
            *PROMPT_INJECTION_PATTERNS,
            *OFFICIAL_ACTION_PATTERNS,
        )
    )


def score_service(query: str, spec: dict) -> tuple[float, list[str], list[str]]:
    query_tokens = tokenize(query)
    anchors: list[str] = []
    supports: list[str] = []

    for phrase in spec.get("anchors", []):
        if contains_phrase(query_tokens, phrase):
            anchors.append(phrase)

    for stem in spec.get("stems", []):
        if contains_stem(query_tokens, stem):
            anchors.append(stem)

    if not anchors:
        return 0.0, [], []

    score = sum(phrase_weight(anchor) for anchor in anchors)
    for phrase in spec.get("supports", []):
        if contains_phrase(query_tokens, phrase):
            supports.append(phrase)
            score += SUPPORT_WEIGHT

    return score, anchors, supports


def rank(query: str, lexicon: dict) -> list[dict]:
    ranked = []
    for service_id, spec in lexicon.items():
        score, anchors, supports = score_service(query, spec)
        if score > 0:
            ranked.append(
                {
                    "service_id": service_id,
                    "score": score,
                    "anchors": anchors,
                    "supports": supports,
                }
            )
    return sorted(ranked, key=lambda item: (-item["score"], item["service_id"]))


def predict(query: str, lexicon: dict) -> dict:
    if is_guarded(query):
        return {"service_id": None, "reason": "safety_guard", "ranked": []}

    ranked = rank(query, lexicon)
    if not ranked:
        return {"service_id": None, "reason": "no_anchor_evidence", "ranked": []}

    top = ranked[0]
    if top["score"] < MIN_MATCH_SCORE:
        return {"service_id": None, "reason": "below_threshold", "ranked": ranked[:3]}

    if len(ranked) > 1:
        second = ranked[1]

        # Near-equal evidence is not resolved alphabetically. If both services
        # clear the normal match floor, v3 returns an explicit ambiguity fallback.
        if second["score"] >= MIN_MATCH_SCORE and top["score"] - second["score"] <= AMBIGUITY_MARGIN:
            return {"service_id": None, "reason": "ambiguous_tie", "ranked": ranked[:3]}

        if (
            second["score"] >= MULTI_INTENT_MIN_SCORE
            and top["score"] - second["score"] <= MULTI_INTENT_MARGIN
        ):
            return {"service_id": None, "reason": "multi_intent", "ranked": ranked[:3]}

    return {"service_id": top["service_id"], "reason": "matched", "ranked": ranked[:3]}


def load_queries(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def evaluate(lexicon: dict, queries: list[dict]) -> dict:
    positive = fallback = top1_correct = fallback_correct = 0
    false_positive_fallbacks = 0
    ambiguity_fallbacks = 0
    multi_intent_fallbacks = 0

    for case in queries:
        result = predict(case["query"], lexicon)
        expected = case.get("expected_service_id")
        predicted = result["service_id"]

        if expected is None:
            fallback += 1
            if predicted is None:
                fallback_correct += 1
            else:
                false_positive_fallbacks += 1
        else:
            positive += 1
            if predicted == expected:
                top1_correct += 1

        if result["reason"] == "ambiguous_tie":
            ambiguity_fallbacks += 1
        if result["reason"] == "multi_intent":
            multi_intent_fallbacks += 1

        print(
            f"{case['id']}: expected={expected!r} predicted={predicted!r} "
            f"reason={result['reason']} ranked={[x['service_id'] for x in result['ranked']]}"
        )

    return {
        "positive_cases": positive,
        "fallback_cases": fallback,
        "precision_at_1": top1_correct / positive if positive else 0.0,
        "fallback_accuracy": fallback_correct / fallback if fallback else 0.0,
        "false_positive_fallbacks": false_positive_fallbacks,
        "ambiguity_fallbacks": ambiguity_fallbacks,
        "multi_intent_fallbacks": multi_intent_fallbacks,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queries", type=Path, default=QUERIES_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lexicon = json.loads(LEXICON_PATH.read_text(encoding="utf-8"))
    metrics = evaluate(lexicon, load_queries(args.queries))
    print("\nRetrieval v3 metrics")
    for key, value in metrics.items():
        print(f"{key}={value:.3f}" if isinstance(value, float) else f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
