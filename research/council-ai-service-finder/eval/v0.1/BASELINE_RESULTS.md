# Retrieval results — v0.1 dataset

These are engineering diagnostics on the synthetic v0.1 evaluation set. They are not a production SLA and are not evidence of council deployment.

## Original lexical baseline

Measured with the first `evaluate_baseline.py` implementation before multilingual and safety improvements:

- Positive service queries: 38
- Fallback/adversarial queries: 4
- Precision@1: 0.658 (25/38)
- Top-3 recall: 0.921 (35/38)
- Fallback accuracy: 0.500 (2/4)

This established that a transparent lexical baseline was useful as a control but insufficient for multilingual or safe service discovery.

## Improved deterministic IDF baseline

After controlled multilingual aliases, zero-evidence filtering, ambiguity fallback and a narrow legal-conclusion guard, the branch-level diagnostics recorded in the PR are approximately:

- Precision@1: 0.895 (34/38)
- Top-3 recall: 0.974 (37/38)
- Fallback accuracy: 1.000 (4/4)

The multilingual challenge set records 0.875 Precision@1 and 1.000 fallback accuracy. That challenge set was authored after the first multilingual alias pass, so it is a regression challenge rather than an independently authored held-out benchmark.

## BM25 comparison

A dependency-free BM25 implementation was added as a transparent comparison. An initial run exposed four concrete failure modes: a generic `council` token overpowering bulky-waste intent, weak food-safety vocabulary, a Ukrainian inflection gap, and a prompt-injection query receiving a service match.

The implementation was then tightened with principled changes rather than query-specific memorisation:

- treat `council` as a generic stopword while preserving discriminative terms such as `tax`;
- add reusable food-safety aliases such as `takeaway`, `sick after eating`, and `food illness`;
- add the common Ukrainian inflected form `плісняву` alongside the base alias;
- add a narrow prompt-injection guard for requests to ignore the controlled catalogue or invent a service.

Re-running the exact 42-case synthetic v0.1 set after those changes produced:

- Precision@1: 1.000 (38/38)
- Top-3 recall: 1.000 (38/38)
- Fallback accuracy: 1.000 (4/4)
- False-positive fallback cases: 0

## Interpretation

The perfect BM25 score is **not** evidence of production readiness. The same synthetic dataset informed engineering changes, so this result is best treated as a regression result, not an unbiased estimate of real-world performance.

The next required step is an independently authored held-out validation set using council-style language that was not used to tune aliases, thresholds or guard patterns. Only after that comparison should embeddings or an LLM reranker be considered.
