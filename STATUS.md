# KUBERA workspace status

Updated 2026-09-03.

## Flagship (work here)

1. Civic Evidence OS — `kubera-improved-website/civic-evidence-os`
2. Agent Fabric / Trust Mesh + DZAMBALA operational trust v0.9.1 — `jobkubera-lab/kubera-lab/innovation-stack/reference-implementation`
3. Community Compass v0.2 — `jobkubera-lab/kubera-lab/dzambala-community-compass`

PR #38 merged: `HandoffArtifact`, Source/Evidence/Action gates, `IdempotencyStore`, and `ActionLogger` into the existing Evidence Ledger; focused tests 12/12; GitHub Actions green.

PR #39 merged: `SovereignToolExecutor` composes Handoff → Privacy/Validation → Source/Evidence/Action gates → signed approval → idempotency → injected tool adapter → ActionLogger/Evidence Ledger.

PR #40 merged: Tool Executor hardened to v0.9.1 — approval bound to finalized sanitized payload + actor + idempotency key; PENDING/COMPLETE idempotency state; UNKNOWN_EXTERNAL_STATE on uncertain retries; serialized Evidence Ledger writes; malformed grants fail closed.

PR #41 merged: KUBERA operator pack landed — `KUBERA_OPERATOR.md`, five-field `WorkContract`, ledger-backed Source/Evidence resolution, explicit PENDING/IN_FLIGHT idempotency handling, and `SovereignToolExecutor` as the single reference tool choke point. CI: **143/143 tests green on Python 3.11, 3.12 and 3.13**.

PR #42 merged: `LocalDraftAdapter` adds one reversible real tool path behind `SovereignToolExecutor`: `task → brief → approval → local draft`. Replay does not write the draft twice. Full Innovation Stack CI: **145/145 tests green on Python 3.11, 3.12 and 3.13**.

PR #43 and #44 merged: the owner-approved root profile `README.md` was restored and protected by a hash-check/self-healing workflow. The profile README is owner-controlled and must not be changed by routine project work.

Current reference CI also measures source-only branch coverage. Unit tests + safe demo report **89%**, with an enforced **85% fail-under floor**.

## Frozen

Innovation-stack modules 01–18 are not separate products and should not be expanded as parallel product lines. Do not create modules 19+.

`DZAMBALA.md` plus `reference-implementation/` are the active Control layer. The rest of innovation-stack remains frozen unless directly required by the active reference runtime.

Migration/visa templates remain library material rather than the primary account product narrative.

## Next step

If a real external integration is added, add at most one narrowly scoped read/lookup adapter behind `SovereignToolExecutor`; raw provider credentials remain outside agent/plugin reach and no send/publish/payment action is added without a separate review.

## Rule

**KUBERA prepares. The human remains the authority.**
