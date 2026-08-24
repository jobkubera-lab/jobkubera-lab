# Baseline results — v0.1

Measured with `evaluate_baseline.py` at `FALLBACK_THRESHOLD = 0.20` against the synthetic v0.1 dataset.

## Overall

- Positive service queries: 38
- Fallback/adversarial queries: 4
- Precision@1: 0.658 (25/38)
- Top-3 recall: 0.921 (35/38)
- Fallback accuracy: 0.500 (2/4)
- False-positive fallback cases: 2

## By language

- English: Precision@1 25/33; Top-3 recall 33/33
- Ukrainian: Precision@1 0/3; Top-3 recall 2/3
- Polish: Precision@1 0/2; Top-3 recall 0/2

## Interpretation

The lexical baseline is useful as a control, but it is not sufficient for a pilot. It performs well as a candidate generator for English (all 33 English positive queries place the correct service in the top 3), while multilingual retrieval is predictably weak because the catalogue currently contains English-only aliases.

The next engineering step should not be to add an LLM blindly. First add controlled multilingual aliases/normalisation and compare the same metrics. An embedding or LLM reranker should only be introduced if it produces a measurable improvement without reducing fallback safety.

These numbers are engineering diagnostics on a synthetic dataset, not a production SLA and not evidence of council deployment.
