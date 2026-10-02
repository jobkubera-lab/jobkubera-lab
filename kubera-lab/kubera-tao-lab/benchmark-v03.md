# KUBERA RESI v0.3 — benchmark evidence

Snapshot: 2 October 2026

## Dataset split

| Stage | Rows |
|---|---:|
| Raw master | 310,496 |
| Clean / eligible | 232,349 |
| Train | 184,623 |
| Validation | 19,226 |
| Test | 20,051 |
| Strict test | 17,003 |

## Final model comparison

| Model | Validation MAPE | Test MAPE | Strict-test MAPE |
|---|---:|---:|---:|
| XGBoost | **31.90%** | **32.28%** | **32.05%** |
| CatBoost | 32.05% | 32.68% | 32.43% |
| LightGBM | 32.24% | 32.78% | 32.59% |
| Baseline | 41.82% | 41.44% | 43.10% |

The current report selects XGBoost by final-validation performance. Test metrics are evidence, not manual selection targets.

## Current winner — test breakdown

| Segment | MAPE |
|---|---:|
| Washington, DC | 26.19% |
| Illinois | 27.66% |
| Pennsylvania | 36.76% |
| Q1 — lowest-price quintile | 61.96% |
| Q3 | 24.61% |
| Q4 | 20.33% |
| Q5 — highest-price quintile | 23.04% |

## Method controls

- chronological train / validation / test windows
- strict unseen-property test subset
- no price-derived model inputs
- validation-driven selection
- source-specific completeness rules
- manifest/hash integrity checks where available
- explicit reporting of weak geographies and price segments

The main current research priority is improving low-price and Pennsylvania generalization without tuning against the test set.