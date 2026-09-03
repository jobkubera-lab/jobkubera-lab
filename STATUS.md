# KUBERA workspace status

Updated 2026-09-03.

## Flagship (work here)

1. Civic Evidence OS — `kubera-improved-website/civic-evidence-os`
2. Agent Fabric / Trust Mesh + DZAMBALA operational trust v0.9.1 — `jobkubera-lab/kubera-lab/innovation-stack/reference-implementation`
3. Community Compass v0.2 — `jobkubera-lab/kubera-lab/dzambala-community-compass`

PR #38 merged: `HandoffArtifact`, Source/Evidence/Action gates, `IdempotencyStore`, and `ActionLogger` into the existing Evidence Ledger; focused tests 12/12; GitHub Actions green.

PR #39 merged: `SovereignToolExecutor` composes Handoff → Privacy/Validation → Source/Evidence/Action gates → signed approval → idempotency → injected tool adapter → ActionLogger/Evidence Ledger.

PR #40 merged: Tool Executor hardened to v0.9.1 — approval bound to finalized sanitized payload + actor + idempotency key; PENDING/COMPLETE idempotency state; UNKNOWN_EXTERNAL_STATE on uncertain retries; serialized Evidence Ledger writes; malformed grants fail closed. Full Innovation Stack CI: **134/134 tests green on Python 3.11, 3.12 and 3.13**.

## Craft — separate from runtime

KUBERA STONES — `jobkubera-lab/kubera-lab/kubera-stones`

## Frozen

Innovation-stack modules 01–18 are not separate products and should not be expanded as parallel product lines. Do not create modules 19+.

`DZAMBALA.md` plus `reference-implementation/` are the active Control layer. The rest of innovation-stack remains frozen unless directly required by the active reference runtime.

Migration/visa templates remain library material rather than the primary account product narrative.

## Next step

Connect one narrowly scoped real tool adapter only behind `SovereignToolExecutor`; keep provider credentials outside agent/plugin reach and require reconciliation for unknown external state.

## Rule

**KUBERA prepares. The human remains the authority.**
