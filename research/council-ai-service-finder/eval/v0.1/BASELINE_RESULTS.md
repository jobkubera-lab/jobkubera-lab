# Retrieval results — v0.1 dataset

These are engineering diagnostics on synthetic data. They are not a production SLA and are not evidence of council deployment.

## Original lexical baseline

Measured with the first `evaluate_baseline.py` implementation:

- Positive service queries: 38
- Fallback/adversarial queries: 4
- Precision@1: 0.658 (25/38)
- Top-3 recall: 0.921 (35/38)
- Fallback accuracy: 0.500 (2/4)

## Deterministic IDF baseline

The branch later added IDF weighting, multilingual aliases, zero-evidence filtering, ambiguity fallback and a narrow legal-conclusion guard. Those numbers are regression diagnostics only and must not be presented as independent validation.

## BM25 comparison

`evaluate_bm25.py` is a dependency-free Okapi BM25 implementation with a minimum-score floor, ambiguity fallback and narrow hard-fallback patterns for specific legal-conclusion and prompt-injection classes.

During development, the regression set exposed concrete failures including generic-token collisions, catalogue-length effects, incomplete multilingual coverage and guard bypasses. The implementation and catalogue were changed after seeing those failures, which means the original 42-case set is now a regression suite rather than a held-out benchmark.

A previous version of this document recorded a 1.000/1.000/1.000 BM25 run. That result is intentionally **not treated as current evidence** here because an independent audit reported that it could not reproduce the published numbers from the branch state it tested. Until metrics are regenerated automatically from the exact PR head in CI or an equivalent clean environment, do not quote a current BM25 accuracy figure from this file.

## Independent audit findings

An independent second-model review identified the following risks that must be treated as real engineering issues rather than hidden by threshold tuning:

- trivial rephrasings can bypass narrow legal/prompt-injection regex guards;
- BM25 document-length normalisation can over-reward short service documents on a single rare shared token;
- multilingual coverage is shallow and uneven across the 20-service synthetic catalogue;
- safety for non-English queries cannot rely on the absence of lexical overlap;
- the original dataset informed implementation changes and therefore cannot measure unbiased generalisation.

The branch now includes additional regression coverage for rephrased legal-conclusion and prompt-injection requests. These tests are regression guards, not proof of general safety.

## Validation policy

The next meaningful accuracy claim requires all of the following:

1. an independently authored held-out set that was not used to tune aliases, thresholds or guard patterns;
2. metrics produced from the exact commit being evaluated;
3. a third blind validation set after any fixes informed by the first held-out set;
4. a real council-approved service catalogue before any production-readiness claim.

Do not add an LLM or embeddings merely to improve a headline metric. First establish reproducible deterministic baselines and document their failure modes honestly.
