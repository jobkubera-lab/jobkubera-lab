#!/usr/bin/env python3
"""Deterministic evaluator for the Council AI Service Finder dataset.

The baseline deliberately stays model-free. It uses catalogue-derived IDF weights,
an explicit narrow safety guard, a confidence threshold, and an ambiguity margin.
It never generates council services: every returned ID must exist in the catalogue.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
CATALOGUE_PATH = HERE / "service_catalogue.json"
QUERIES_PATH = HERE / "queries.jsonl"
TOKEN_RE = re.compile(r"[\w']+", re.UNICODE)
STOPWORDS = {
    "a", "about", "an", "and", "are", "can", "did", "do", "for", "how",
    "i", "is", "it", "me", "my", "of", "on", "please", "should", "tell",
    "that", "the", "these", "this", "those", "to", "want", "was", "what",
    "when", "where", "whether", "who", "why", "will", "with", "would",
    "write",
}

# IDF scores have a different scale from the original overlap ratio, so this
# threshold is intentionally calibrated only as an engineering baseline.
FALLBACK_THRESHOLD = 0.10
AMBIGUITY_MARGIN = 0.02

# This guard is deliberately narrow. It blocks requests for authoritative legal
# conclusions; it does not attempt to classify every legal or policy question.
LEGAL_CONCLUSION_PATTERNS = (
    re.compile(r"\b(?:legal|legally)\b.{0,40}\b(?:guilty|liable|responsible)\b", re.I),
    re.compile(r"\b(?:is|are|am|was|were)\b.{0,60}\b(?:illegal|lawful|unlawful|guilty|liable)\b", re.I),
)


def tokenize(text: str) -> set[str]:
    return {
        token.lower()
        for token in TOKEN_RE.findall(text)
        if len(token) > 1 and token.lower() not in STOPWORDS
    }


def service_tokens(service: dict) -> set[str]:
    text = " ".join(
        [service["name"], service["description"], *service.get("aliases", [])]
    )
    return tokenize(text)


def build_idf(catalogue: Iterable[dict]) -> dict[str, float]:
    """Build smoothed inverse-document-frequency weights from the catalogue."""
    services = list(catalogue)
    document_frequency: Counter[str] = Counter()
    for service in services:
        document_frequency.update(service_tokens(service))

    size = len(services)
    return {
        token: math.log((size + 1) / (frequency + 1)) + 1.0
        for token, frequency in document_frequency.items()
    }


def weighted_score(
    query_tokens: set[str],
    candidate_tokens: set[str],
    idf: dict[str, float],
    catalogue_size: int,
) -> float:
    if not query_tokens:
        return 0.0

    # Unseen query terms still count in the denominator so unrelated wording
    # lowers confidence instead of disappearing from the score entirely.
    unseen_weight = math.log((catalogue_size + 1) / 1) + 1.0
    denominator = sum(idf.get(token, unseen_weight) for token in query_tokens)
    overlap = query_tokens & candidate_tokens
    numerator = sum(idf.get(token, 0.0) for token in overlap)
    return numerator / denominator if denominator else 0.0


def rank(query: str, catalogue: Iterable[dict]) -> list[tuple[str, float]]:
    services = list(catalogue)
    query_tokens = tokenize(query)
    idf = build_idf(services)
    ranked = [
        (
            service["id"],
            weighted_score(
                query_tokens,
                service_tokens(service),
                idf,
                len(services),
            ),
        )
        for service in services
    ]
    return sorted(ranked, key=lambda item: (-item[1], item[0]))


def requires_safe_fallback(query: str) -> bool:
    """Return True for narrow classes that must not receive a service guess."""
    return any(pattern.search(query) for pattern in LEGAL_CONCLUSION_PATTERNS)


def predict(
    query: str,
    catalogue: Iterable[dict],
    threshold: float = FALLBACK_THRESHOLD,
    ambiguity_margin: float = AMBIGUITY_MARGIN,
):
    if requires_safe_fallback(query):
        return None, [], 0.0, "safety_guard"

    ranked = [item for item in rank(query, catalogue) if item[1] > 0.0]
    if not ranked:
        return None, [], 0.0, "no_evidence"

    top_id, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0

    if top_score < threshold:
        predicted = None
        reason = "below_threshold"
    elif len(ranked) > 1 and (top_score - second_score) < ambiguity_margin:
        predicted = None
        reason = "ambiguous"
    else:
        predicted = top_id
        reason = "matched"

    return predicted, ranked[:3], top_score, reason


def load_queries(path: Path = QUERIES_PATH) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def evaluate(catalogue: list[dict], queries: list[dict]) -> dict:
    top1_correct = 0
    top3_correct = 0
    positive_cases = 0
    fallback_cases = 0
    fallback_correct = 0
    false_positive_fallbacks = 0
    decision_reasons: Counter[str] = Counter()

    for case in queries:
        predicted, top3, top_score, reason = predict(case["query"], catalogue)
        decision_reasons[reason] += 1
        expected = case.get("expected_service_id")
        top3_ids = [service_id for service_id, _ in top3]

        if expected is None:
            fallback_cases += 1
            if predicted is None:
                fallback_correct += 1
            else:
                false_positive_fallbacks += 1
        else:
            positive_cases += 1
            if predicted == expected:
                top1_correct += 1
            if expected in top3_ids:
                top3_correct += 1

        print(
            f"{case['id']}: expected={expected!r} predicted={predicted!r} "
            f"top3={top3_ids!r} score={top_score:.3f} reason={reason}"
        )

    return {
        "positive_cases": positive_cases,
        "fallback_cases": fallback_cases,
        "precision_at_1": top1_correct / positive_cases if positive_cases else 0.0,
        "top3_recall": top3_correct / positive_cases if positive_cases else 0.0,
        "fallback_accuracy": fallback_correct / fallback_cases if fallback_cases else 0.0,
        "false_positive_fallbacks": false_positive_fallbacks,
        "decision_reasons": dict(sorted(decision_reasons.items())),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queries",
        type=Path,
        default=QUERIES_PATH,
        help="JSONL evaluation file (default: queries.jsonl)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    queries = load_queries(args.queries)
    metrics = evaluate(catalogue, queries)

    print("\nMetrics")
    print(f"precision_at_1={metrics['precision_at_1']:.3f}")
    print(f"top3_recall={metrics['top3_recall']:.3f}")
    print(f"fallback_accuracy={metrics['fallback_accuracy']:.3f}")
    print(f"false_positive_fallbacks={metrics['false_positive_fallbacks']}")
    print(f"decision_reasons={metrics['decision_reasons']}")
    print(
        f"cases: positive={metrics['positive_cases']} "
        f"fallback={metrics['fallback_cases']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
