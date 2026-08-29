# Frozen post-fix validation — remediation record

This file records the validation sequence for `frozen_postfix_validation_v1.jsonl`.

## Dataset

- 32 queries total
- 26 positive single-service cases
- 6 expected fallback cases
- all 20 catalogue services represented
- Ukrainian and Polish cases included
- ordinary out-of-scope, safety/adversarial and deliberately multi-intent cases included

The dataset was committed before its first measurement. It is a frozen regression gate, not an independent third-party benchmark.

## Baseline measurements

The first frozen-set run exposed structural limitations in token-overlap retrieval.

### IDF baseline

- Precision@1: **0.346** (9/26)
- Top-3 recall: **0.500** (13/26)
- Fallback accuracy: **0.833** (5/6)

### BM25 baseline

- Precision@1: **0.385** (10/26)
- Top-3 recall: **0.538** (14/26)
- Fallback accuracy: **0.667** (4/6)

These measurements are retained as the pre-remediation control.

## Structural remediation: retrieval v2

`retrieval_v2.py` replaces single-token evidence with a controlled intent model:

- service-defining **anchor evidence** is separated from contextual/support words;
- support words cannot produce a service match without an anchor;
- phrase anchors receive stronger evidence weight than isolated terms;
- service-specific Ukrainian/Polish morphological stems handle common inflection without a remote translation dependency;
- two independently supported service intents trigger `multi_intent` fallback rather than an arbitrary winner;
- out-of-scope text with no service anchor returns `no_anchor_evidence`;
- rephrased legal-conclusion and prompt-injection classes retain hard fallback.

The frozen dataset itself was not edited for this remediation.

### Retrieval v2 regression result on the same 32 frozen cases

- Precision@1: **1.000** (26/26)
- Fallback accuracy: **1.000** (6/6)
- False-positive fallback cases: **0**
- Deliberately multi-intent case: **correctly returned fallback**

## Interpretation

The v2 result demonstrates that the identified structural failure classes have regression coverage and are resolved on this frozen gate. Because retrieval v2 was developed after the frozen-set failures were known, this 1.000 result is deliberately described as a **regression result**, not an unbiased real-world accuracy estimate.

The next external-quality gate should be authored independently after v2 is frozen. No aliases, intent anchors, thresholds or safety patterns should be changed after that blind set is revealed until its first result is recorded.
