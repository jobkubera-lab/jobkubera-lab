#!/usr/bin/env python3
"""Dependency-free BM25 comparison for the Council AI Service Finder evaluation set."""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOGUE_PATH = HERE / "service_catalogue.json"
QUERIES_PATH = HERE / "queries.jsonl"
TOKEN_RE = re.compile(r"[\w']+", re.UNICODE)
STOPWORDS = {
    "a", "about", "an", "and", "are", "can", "council", "did", "do", "for", "how",
    "i", "is", "it", "me", "my", "of", "on", "please", "should", "tell",
    "that", "the", "these", "this", "those", "to", "want", "was", "what",
    "when", "where", "whether", "who", "why", "will", "with", "would",
    "write",
}
K1 = 1.2
B = 0.75
MIN_SCORE = 0.8
AMBIGUITY_MARGIN = 0.15

# Deliberately narrow hard-fallback patterns. These do not constitute a general
# legal- or prompt-injection classifier; they only protect known classes that
# should never be answered by lexical service retrieval.
LEGAL_CONCLUSION_PATTERNS = (
    re.compile(r"\b(legally|legal)\b.*\b(guilty|liable|illegal|lawful|unlawful)\b", re.I),
    re.compile(r"\b(is|was|are|were)\b.*\b(guilty|liable|illegal|lawful|unlawful)\b", re.I),
    re.compile(r"\b(breaking|breaks?|broke|violating|violates?|breaching|breaches?)\b.{0,40}\b(the\s+)?law\b", re.I),
    re.compile(r"\b(in\s+breach\s+of|against)\b.{0,20}\b(the\s+)?law\b", re.I),
)
PROMPT_INJECTION_PATTERNS = (
    re.compile(r"\b(ignore|override|bypass|disregard)\b.*\b(catalogue|instructions?|rules?|safety|system)\b", re.I),
    re.compile(r"\b(catalogue|instructions?|rules?|safety|system)\b.*\b(ignore|override|bypass|disregard)\b", re.I),
    re.compile(r"\binvent\b.*\b(service|answer|result)\b", re.I),
)


def tokenize(text: str) -> list[str]:
    return [
        token.lower()
        for token in TOKEN_RE.findall(text)
        if len(token) > 1 and token.lower() not in STOPWORDS
    ]


def service_text(service: dict) -> str:
    return " ".join(
        [service["name"], service["description"], *service.get("aliases", [])]
    )


def is_guarded(query: str) -> bool:
    return any(
        pattern.search(query)
        for pattern in (*LEGAL_CONCLUSION_PATTERNS, *PROMPT_INJECTION_PATTERNS)
    )


def build_index(catalogue: list[dict]) -> tuple[list[Counter], dict[str, int], float]:
    docs: list[Counter] = []
    document_frequency: Counter[str] = Counter()

    for service in catalogue:
        counts = Counter(tokenize(service_text(service)))
        docs.append(counts)
        document_frequency.update(counts.keys())

    avg_doc_len = (
        sum(sum(doc.values()) for doc in docs) / len(docs) if docs else 0.0
    )
    return docs, dict(document_frequency), avg_doc_len


def bm25_score(
    query_tokens: list[str],
    doc: Counter,
    document_frequency: dict[str, int],
    document_count: int,
    avg_doc_len: float,
) -> float:
    if not query_tokens or not doc or avg_doc_len <= 0:
        return 0.0

    doc_len = sum(doc.values())
    score = 0.0
    for term in set(query_tokens):
        tf = doc.get(term, 0)
        if tf == 0:
            continue
        df = document_frequency.get(term, 0)
        idf = math.log(1 + (document_count - df + 0.5) / (df + 0.5))
        denominator = tf + K1 * (1 - B + B * doc_len / avg_doc_len)
        score += idf * (tf * (K1 + 1)) / denominator
    return score


def rank(query: str, catalogue: list[dict]) -> list[tuple[str, float]]:
    docs, df, avg_doc_len = build_index(catalogue)
    query_tokens = tokenize(query)
    scored = [
        (
            service["id"],
            bm25_score(query_tokens, doc, df, len(catalogue), avg_doc_len),
        )
        for service, doc in zip(catalogue, docs)
    ]
    return sorted(scored, key=lambda item: (-item[1], item[0]))


def predict(query: str, catalogue: list[dict]):
    if is_guarded(query):
        return None, [], 0.0

    ranked = [item for item in rank(query, catalogue) if item[1] > 0.0]
    if not ranked:
        return None, [], 0.0

    top_id, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    ambiguous = len(ranked) > 1 and (top_score - second_score) < AMBIGUITY_MARGIN
    predicted = top_id if top_score >= MIN_SCORE and not ambiguous else None
    return predicted, ranked[:3], top_score


def load_queries(path: Path = QUERIES_PATH) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def evaluate(catalogue: list[dict], queries: list[dict]) -> dict:
    positive_cases = fallback_cases = 0
    top1_correct = top3_correct = fallback_correct = 0
    false_positive_fallbacks = 0

    for case in queries:
        predicted, top3, top_score = predict(case["query"], catalogue)
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
            f"top3={top3_ids!r} score={top_score:.3f}"
        )

    return {
        "positive_cases": positive_cases,
        "fallback_cases": fallback_cases,
        "precision_at_1": top1_correct / positive_cases if positive_cases else 0.0,
        "top3_recall": top3_correct / positive_cases if positive_cases else 0.0,
        "fallback_accuracy": fallback_correct / fallback_cases if fallback_cases else 0.0,
        "false_positive_fallbacks": false_positive_fallbacks,
    }


def main() -> int:
    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    metrics = evaluate(catalogue, load_queries())
    print("\nBM25 Metrics")
    for key, value in metrics.items():
        print(f"{key}={value:.3f}" if isinstance(value, float) else f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
