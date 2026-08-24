#!/usr/bin/env python3
"""Deterministic baseline evaluator for the Council AI Service Finder dataset."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable

HERE = Path(__file__).resolve().parent
CATALOGUE_PATH = HERE / "service_catalogue.json"
QUERIES_PATH = HERE / "queries.jsonl"
TOKEN_RE = re.compile(r"[\w']+", re.UNICODE)
STOPWORDS = {
    "a", "an", "and", "are", "can", "do", "for", "how", "i", "is", "it",
    "me", "my", "of", "on", "the", "to", "want", "where", "with",
}
FALLBACK_THRESHOLD = 0.20


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


def score(query_tokens: set[str], candidate_tokens: set[str]) -> float:
    if not query_tokens:
        return 0.0
    overlap = query_tokens & candidate_tokens
    return len(overlap) / len(query_tokens)


def rank(query: str, catalogue: Iterable[dict]) -> list[tuple[str, float]]:
    query_tokens = tokenize(query)
    ranked = [
        (service["id"], score(query_tokens, service_tokens(service)))
        for service in catalogue
    ]
    return sorted(ranked, key=lambda item: (-item[1], item[0]))


def predict(query: str, catalogue: Iterable[dict], threshold: float = FALLBACK_THRESHOLD):
    ranked = rank(query, catalogue)
    if not ranked:
        return None, [], 0.0
    top_id, top_score = ranked[0]
    predicted = top_id if top_score >= threshold else None
    return predicted, ranked[:3], top_score


def load_queries() -> list[dict]:
    return [
        json.loads(line)
        for line in QUERIES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def evaluate(catalogue: list[dict], queries: list[dict]) -> dict:
    top1_correct = 0
    top3_correct = 0
    positive_cases = 0
    fallback_cases = 0
    fallback_correct = 0
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
    queries = load_queries()
    metrics = evaluate(catalogue, queries)

    print("\nMetrics")
    print(f"precision_at_1={metrics['precision_at_1']:.3f}")
    print(f"top3_recall={metrics['top3_recall']:.3f}")
    print(f"fallback_accuracy={metrics['fallback_accuracy']:.3f}")
    print(f"false_positive_fallbacks={metrics['false_positive_fallbacks']}")
    print(
        f"cases: positive={metrics['positive_cases']} "
        f"fallback={metrics['fallback_cases']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
