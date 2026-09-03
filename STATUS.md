# KUBERA workspace status

Updated 2026-09-03.

## Flagship (work here)

1. Civic Evidence OS — `kubera-improved-website/civic-evidence-os`
2. Agent Fabric / Trust Mesh + DZAMBALA operational trust v0.9 — `jobkubera-lab/kubera-lab/innovation-stack/reference-implementation`
3. Community Compass v0.2 — `jobkubera-lab/kubera-lab/dzambala-community-compass`

PR #38 merged: `HandoffArtifact`, Source/Evidence/Action gates, `IdempotencyStore`, and `ActionLogger` into the existing Evidence Ledger; focused tests 12/12; GitHub Actions green.

PR #39 merged: `SovereignToolExecutor` now composes Handoff → Privacy/Validation → Source/Evidence/Action gates → signed approval → idempotency → injected tool adapter → ActionLogger/Evidence Ledger. The full Innovation Stack suite is green: 120 tests on Python 3.11, 3.12 and 3.13.

## Frozen

Innovation-stack modules 01–18 are not separate products and should not be expanded as parallel product lines. The active Control layer is `DZAMBALA.md` plus `reference-implementation/`.

## Next step

Red-team the `SovereignToolExecutor` and only then connect one narrowly scoped real adapter through this boundary.

## Rule

**KUBERA prepares. The human remains the authority.**
