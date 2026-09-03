# CHANGELOG

This file records **verified changes** to the active KUBERA / DZAMBALA public workspace. It is not a roadmap and does not reconstruct older history from memory.

Current priorities and future work belong in [`STATUS.md`](./STATUS.md).

## 2026-09-03 — reference runtime v0.9.1 and operator boundary

### PR #38 — DZAMBALA operational trust layer

Merged: [`#38`](https://github.com/jobkubera-lab/jobkubera-lab/pull/38)

Added the reference operational controls that are now used by the active runtime:

- `HandoffArtifact`;
- Source / Evidence / Action gates;
- signed approval bound to exact action fingerprints;
- `IdempotencyStore`;
- `ActionLogger` writing into the existing Evidence Ledger;
- focused operational-control tests.

### PR #39 — SovereignToolExecutor

Merged: [`#39`](https://github.com/jobkubera-lab/jobkubera-lab/pull/39)

Added `SovereignToolExecutor` as the reference execution boundary over:

`Handoff → Privacy/Validation → Source/Evidence/Action gates → approval → idempotency → injected adapter → ActionLogger/Evidence Ledger`.

No live Slack, email, payment, browser-posting, or Kickstarter adapter was connected.

### PR #40 — runtime hardening to v0.9.1

Merged: [`#40`](https://github.com/jobkubera-lab/jobkubera-lab/pull/40)

Hardened the existing executor and control state:

- approval binding includes the finalized sanitized payload, actor, and idempotency domain;
- idempotency distinguishes `PENDING` from `COMPLETE`;
- uncertain adapter state returns an unknown/reconciliation state instead of blindly retrying;
- Evidence Ledger writes are serialized;
- malformed authorization grants fail closed;
- adversarial hardening tests were added;
- reference package version set to `0.9.1`.

### PR #41 — operator pack

Merged: [`#41`](https://github.com/jobkubera-lab/jobkubera-lab/pull/41)

Added and integrated:

- `KUBERA_OPERATOR.md`;
- five-field `WorkContract` (`Job / Sources / Judgment / Output / Forbidden`);
- ledger-backed Source/Evidence resolution;
- explicit in-flight/unknown handling for pending idempotency reservations;
- `SovereignToolExecutor` documented as the single reference tool choke point.

At merge, the reference CI reported **143/143 tests green** on Python 3.11, 3.12, and 3.13.

### PR #42 — first narrow real adapter and demo

Merged: [`#42`](https://github.com/jobkubera-lab/jobkubera-lab/pull/42)

Added one reversible real adapter behind the executor:

- `LocalDraftAdapter` writes a local UTF-8 draft only;
- example path: `task → brief → approval → SovereignToolExecutor → local draft`;
- replay does not write the completed draft twice;
- no send/publish/payment/network action was added.

After this merge, the reference CI reported **145/145 tests green** on Python 3.11, 3.12, and 3.13.

### PR #43 — restore and lock profile README

Merged: [`#43`](https://github.com/jobkubera-lab/jobkubera-lab/pull/43)

Restored the owner-approved root profile `README.md` and added repository guard ownership/CI controls so ordinary PR work must not silently rewrite the profile page.

### PR #44 — self-healing profile guard

Merged: [`#44`](https://github.com/jobkubera-lab/jobkubera-lab/pull/44)

Strengthened the root profile README protection. Pull requests are checked against the approved canonical README hash, and direct changes to `main` are subject to the self-healing workflow.

## 2026-08-30 — Community Compass v0.2

### PR #36 — verified London + Merton event layer

Merged: [`#36`](https://github.com/jobkubera-lab/jobkubera-lab/pull/36)

Added the manually verified Community Compass v0.2 event layer with provenance/freshness handling and dedicated validation/CI. Automatic scraping, autonomous re-verification, and AI ranking were explicitly not claimed.

## Scope and frozen work

Per [`STATUS.md`](./STATUS.md):

- `DZAMBALA.md` + `reference-implementation/` are the active Control layer;
- Innovation Stack modules 01–18 are not separate product lines;
- do not create modules 19+;
- migration/visa material remains supporting library content rather than the primary account runtime.

## Historical accuracy rule

Older releases and dates are intentionally omitted here unless they are verified from repository history. Do not add invented release dates, reconstructed milestones, or speculative future features to this changelog.

**KUBERA prepares. The human remains the authority.**
