# KUBERA TAO LAB

**Evidence-first multi-region real-estate ML research lab.**

KUBERA TAO LAB is a Windows-first Python R&D project for residential valuation experiments, with emphasis on reproducibility, temporal validation, leakage control, strict generalization checks and deployable-model evaluation.

> The implementation repository remains private. This public dossier exposes the engineering method and verified benchmark evidence without publishing raw datasets, credentials, wallet material or private repository history.

## Verified engineering state — 2 October 2026

- **34/34 local project tests passed**
- **GitHub Actions CI completed successfully** on the current private implementation commit
- Python source compiles cleanly with compileall
- staged source passed whitespace/diff checks
- staged source passed a credential-pattern scan
- CI is isolated from private and large local datasets

## Research pipeline

Public data → source-specific ingestion → provenance checks → unified features → temporal split → model experiments → validation-locked selection → strict unseen-property evaluation → bias/robustness analysis → ONNX deployment checks

## What the project tests

- Multi-region ingestion for Cook County (IL), Allegheny County (PA), Philadelphia (PA) and Washington, DC
- XGBoost, LightGBM and CatBoost model comparisons
- chronological train / validation / test separation
- strict test masks excluding property IDs seen earlier
- target-leakage controls: sale price is never an input feature
- source manifests and SHA-256 integrity checks where applicable
- geography and price-segment bias breakdowns
- ONNX interface, runtime and Python/ONNX parity checks

## Current v0.3 snapshot

| Item | Value |
|---|---:|
| Raw master rows | 310,496 |
| Clean / eligible rows | 232,349 |
| Train | 184,623 |
| Validation | 19,226 |
| Test | 20,051 |
| Strict test | 17,003 |
| Final-validation winner | XGBoost |
| Validation MAPE | 31.90% |
| Test MAPE | 32.28% |
| Strict-test MAPE | 32.05% |

These are research measurements, not production valuation guarantees. Results from different region sets or experimental architectures are not presented as directly comparable benchmarks.

## Engineering principle

The goal is not to make the metric look good. Weak segments stay visible. In the current run, the lowest-price quintile is the largest weakness and is explicitly retained for future work rather than filtered out.

See [benchmark-v03.md](benchmark-v03.md) for the current breakdown.

## Safety and scope

Raw datasets, generated model binaries, logs, environment files, credentials and blockchain key material are excluded from the public portfolio. The project does not claim current Bittensor subnet compatibility and does not operate a live miner.