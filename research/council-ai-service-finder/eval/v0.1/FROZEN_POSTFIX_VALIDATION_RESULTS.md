# Frozen post-fix validation — v1

This file records the first evaluation of `frozen_postfix_validation_v1.jsonl` after that dataset was committed and frozen.

## Methodology

- Dataset size: 32 queries.
- Positive single-service cases: 26.
- Expected fallback cases: 6.
- Coverage: all 20 catalogue services, 6 Ukrainian/Polish positive cases, 3 ordinary out-of-scope requests, 2 safety/adversarial requests, and 1 deliberately multi-intent request.
- The dataset was committed before measuring it.
- No scoring thresholds, aliases, BM25 parameters, stopwords or guard patterns were changed after seeing these results.
- This set was authored by the same engineering process that has seen the implementation, so it is a **frozen post-fix validation set**, not an independent third-party blind benchmark.

## IDF baseline

Measured on the frozen set with the current deterministic IDF evaluator:

- Precision@1: **0.346** (9/26)
- Top-3 recall: **0.500** (13/26)
- Fallback accuracy: **0.833** (5/6)
- False-positive fallback cases: **1**

## BM25 baseline

Measured on the same frozen set with the current BM25 evaluator:

- Precision@1: **0.385** (10/26)
- Top-3 recall: **0.538** (14/26)
- Fallback accuracy: **0.667** (4/6)
- False-positive fallback cases: **2**

## What the failures show

The current deterministic retrieval is not ready for a council pilot.

Concrete failure classes include:

1. **Paraphrase/generalisation failures.** Several valid resident requests use ordinary wording that does not overlap sufficiently with the synthetic catalogue vocabulary.
2. **Cross-service token collisions.** Sparse shared words can route to the wrong service, especially when BM25 favours a short document containing one rare overlapping token.
3. **Multilingual coverage remains narrow.** Fresh Ukrainian and Polish queries for noise nuisance, school admissions and Blue Badge do not have adequate controlled vocabulary coverage.
4. **Out-of-scope false positive.** A passport-renewal query can collide with the word `support`/`tax` vocabulary in the controlled catalogue depending on scorer behaviour.
5. **Multi-intent handling is insufficient.** The deliberately mixed homelessness + parking query is not reliably forced to fallback by BM25.

## Safety interpretation

The strengthened English hard-fallback patterns correctly cover the specific rephrasings added after the independent audit, but these regexes remain a narrow defence and must not be described as a general safety classifier.

## Decision

Do **not** tune the current implementation directly against individual sentences in this file.

The next engineering change should address structural causes:

- explicit query-intent decomposition / multi-intent detection before retrieval;
- language-aware normalisation or a controlled translation layer before English retrieval;
- stronger candidate evidence requirements than one rare overlapping token;
- a retrieval score calibrated using development data that is separate from the frozen validation gate;
- preservation of a future independently authored blind set for final validation.

No production-readiness or headline accuracy claim should be made from the existing synthetic development set.
