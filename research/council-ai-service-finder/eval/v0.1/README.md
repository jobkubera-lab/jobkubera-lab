# Council AI Service Finder — Evaluation Dataset v0.1

This directory is a **pre-production evaluation harness**, not a claim of live council integration.

## Purpose

Measure whether a service-finder can map ordinary resident language to a controlled catalogue of council services without inventing services or advice.

## Files

- `service_catalogue.json` — small canonical test catalogue used only for evaluation.
- `queries.jsonl` — primary synthetic evaluation set.
- `multilingual_challenge.jsonl` — secondary Ukrainian/Polish challenge set written after the first alias pass. It is useful for regression testing but is **not an independently authored held-out set**.
- `evaluate_baseline.py` — deterministic IDF-weighted evaluator with explicit fallback rules.
- `test_evaluate_baseline.py` — unit/regression tests.

## Rules

1. The system may return only service IDs present in `service_catalogue.json`.
2. A query marked `expected_service_id: null` must trigger a fallback rather than a guessed service.
3. Evaluation reports Precision@1, Top-3 recall, fallback accuracy, false-positive fallbacks, and decision reasons.
4. Raw resident queries must not be logged in a production system by default.
5. The datasets are synthetic and must be replaced or supplemented with a real council-approved catalogue and an independently authored validation set before any production-readiness claim.

## Deterministic v0.3 baseline

The baseline remains model-free:

1. tokenize the resident query and controlled service catalogue;
2. derive smoothed IDF weights from the catalogue so common words carry less weight than distinctive terms;
3. rank only official catalogue entries;
4. discard zero-evidence candidates;
5. fall back when the best score is below the engineering threshold;
6. fall back when the top candidates are too close to distinguish safely;
7. apply a narrow safety guard for requests asking the finder to make authoritative legal conclusions.

This is intentionally conservative. A fallback is preferable to confidently routing a resident to the wrong service.

## Measured engineering diagnostics

With `FALLBACK_THRESHOLD = 0.10` and `AMBIGUITY_MARGIN = 0.02`, the current primary synthetic set measures approximately:

- Precision@1: **0.895** (34/38)
- Top-3 recall: **0.974** (37/38)
- fallback accuracy: **1.000** (4/4)

The secondary multilingual challenge set measures:

- Precision@1: **0.875** (7/8)
- Top-3 recall: **0.875** (7/8)
- fallback accuracy: **1.000** (4/4)

These figures are regression diagnostics only. The multilingual challenge set was authored after the first multilingual alias pass, so it cannot demonstrate independent generalisation.

## Known limitations

- The service catalogue is synthetic rather than council-approved production data.
- Multilingual coverage is shallow and limited to a subset of services.
- Tokenisation has no language-specific stemming or lemmatisation.
- The safety guard intentionally covers only narrow legal-conclusion patterns; it is not a general safety classifier.
- Threshold and ambiguity settings are engineering defaults, not an SLA.
- A genuinely held-out evaluation set must be written independently of the catalogue/alias authors.

## Next experiment

Do **not** add an LLM merely to improve headline metrics. First expand independently validated multilingual coverage and compare this deterministic IDF baseline with BM25 or another transparent retrieval baseline. Add embeddings or an LLM reranker only if those simpler systems fail on representative held-out data.
