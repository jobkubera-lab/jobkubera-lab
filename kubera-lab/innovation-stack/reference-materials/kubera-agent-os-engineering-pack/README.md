# KUBERA Agent OS Engineering Pack — reference import

This directory preserves the supplied engineering pack as reference material. It is not treated as authoritative production code.

## Supplied files

- `KUBERA_AI_ENGINEERING_GUIDE.md`
- `KUBERA_INTEGRATION_CHECKLIST.md`
- `kubera_production_components.py`
- `test_kubera_evals.py`

## Verification result before integration

The supplied evaluation suite was executed locally with `pytest -q` on 2026-08-23. Result: **18 passed, 2 failed**.

The two failing checks were:

1. `test_no_secrets_in_output` — the test scans an intentionally unredacted sample string and therefore correctly finds the secret it was told to reject.
2. `test_cache_effectiveness` — the mock agent has no cache, and the test compares sub-microsecond timings, so the assertion is nondeterministic and does not prove cache behavior.

These failures are kept visible rather than silently changed in the reference material.

## What was integrated into the live reference runtime

The useful non-duplicating mechanisms were reimplemented in `src/kubera_innovation/tool_safety.py`:

- recursive credential redaction (`PrivacyGate`)
- strict tool-input schema subset validation (`ToolValidator`)
- deterministic iteration/time limits (`ToolLoopGuard`)

The existing KUBERA components remain the source of truth for governance, authority, evidence and failure prevention. The imported pack does **not** replace `AuthorityBudget`, `GovernanceGate`, `EvidenceLedger`, `FailureVaccineRegistry` or `RealityGraph`.

The integrated tool-safety module has its own deterministic unit tests in `tests/test_tool_safety.py`.
