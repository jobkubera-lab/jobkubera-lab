# Council AI Service Finder — Evaluation Dataset v0.1

This directory is a **pre-production evaluation harness**, not a claim of live council integration.

## Purpose

Measure whether a service-finder can map ordinary resident language to a controlled catalogue of council services without inventing services or advice.

## Files

- `service_catalogue.json` — small canonical test catalogue used only for evaluation.
- `queries.jsonl` — resident-style test queries and the expected service ID.

## Rules

1. The system may return only service IDs present in `service_catalogue.json`.
2. A query marked `expected_service_id: null` must trigger a fallback rather than a guessed service.
3. V1 evaluation should report at least Precision@1, Top-3 recall, and fallback accuracy.
4. Raw resident queries must not be logged in a production system by default.
5. This dataset is synthetic and must be replaced or supplemented with a real council-approved catalogue and validation set before any production-readiness claim.

## Suggested baseline

Start with deterministic keyword/BM25 retrieval over `name`, `description`, and `aliases`. Add embeddings or an LLM ranker only if the baseline demonstrably fails on the evaluation set.

## Target threshold for a pilot discussion

A threshold should be agreed with the participating council. Until that happens, results are engineering diagnostics only and must not be represented as a production SLA.
