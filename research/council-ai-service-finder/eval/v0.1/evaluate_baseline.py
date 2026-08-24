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


def load_queries() -> list[dict]:
    return [
        json.loads(line)
        for line in QUERIES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    catalogue = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
    queries = load_queries()

    correct = 0
    fallbacks_correct = 0
    fallback_cases = 0
    evaluated = 0

    for case in queries:
        ranked = rank(case["query"], catalogue)
        top_id, top_score = ranked[0]
        expected = case.get("expected_service_id")

        # A deliberately conservative baseline fallback threshold.
        predicted = top_id if top_score >= 0.20 else None
        evaluated += 1

        if expected is None:
            fallback_cases += 1
            if predicted is None:
                fallbacks_correct += 1
                correct += 1
        elif predicted == expected:
            correct += 1

        print(
            f"{case['id']}: expected={expected!r} predicted={predicted!r} "
            f"score={top_score:.3f}"
        )

    accuracy = correct / evaluated if evaluated else 0.0
    fallback_accuracy = (
        fallbacks_correct / fallback_cases if fallback_cases else 0.0
    )
    print(f"\naccuracy={accuracy:.3f} ({correct}/{evaluated})")
    print(
        f"fallback_accuracy={fallback_accuracy:.3f} "
        f"({fallbacks_correct}/{fallback_cases})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
