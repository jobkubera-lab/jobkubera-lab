# KUBERA Improvement Loop

**Repeated friction becomes evidence. Evidence may become a proposal. A proposal never becomes a rule without human approval.**

This is KUBERA's own provider-neutral implementation of a recurring agent-maintenance problem: the same correction should not have to be re-explained forever.

## Pipeline

```text
CorrectionSignal
  ↓
minimal local record
  ↓
cluster by explicit fingerprint
  ↓
PromotionThreshold
  ↓
ImprovementProposal
  ↓
exact diff preview
  ↓
human APPROVE / DISMISS
  ↓
approved payload only
  ↓
normal Git / PR / CI workflow
```

## Privacy boundary

The reference registry does not require raw chat transcripts. A signal contains only:

- `signal_id`;
- `conversation_id`;
- `fingerprint`;
- short `summary`;
- intended artifact type;
- `pain` score from 1 to 5.

Projects can retain richer evidence elsewhere when necessary, but the improvement registry itself should not become a conversation archive.

## Promotion rule

The default `PromotionThreshold` requires:

- at least 3 signals;
- at least 2 distinct conversations;
- aggregate pain of at least 3.

A single angry correction is therefore not silently converted into permanent configuration. Repeated evidence across work contexts is required.

## Supported proposal types

- `rule` — concise agent guidance;
- `skill` — reusable workflow knowledge loaded when needed;
- `gate` — deterministic enforcement when prose is not enough;
- `doc` — repository documentation that closes a recurring context gap.

## Human review

`maybe_propose()` only creates a proposal. It does not write files.

`preview_diff()` shows the exact proposed change against current content.

`approved_change()` raises `PermissionError` until the exact proposal has been approved by a named human reviewer.

Approval still does not bypass repository governance: the returned payload is intended for the normal branch / PR / CI path.

## Agent overview

The same local registry includes a small provider-neutral session model:

- `running`;
- `waiting_approval`;
- `finished`;
- `failed`;
- `idle`;
- `unknown`.

Sessions requiring approval are surfaced first. This is a data model only; there is no claim of live Codex, Claude or Cursor integration.

## Relationship to existing KUBERA controls

This feature does not create a new Innovation Stack module and does not replace:

- `FailureVaccineRegistry` — deterministic prevention rules after validated failures;
- `EvidenceLedger` — canonical evidence/audit records;
- `WorkContract` — task authority boundary;
- `SovereignToolExecutor` — controlled execution choke point;
- GitHub CI / profile guards — deterministic repository enforcement.

A useful pattern is:

`repeated correction → ImprovementProposal → approved gate/rule → regression test / FailureVaccine / CI enforcement`.

## Reference code

`kubera-lab/innovation-stack/reference-implementation/src/kubera_innovation/improvement_loop.py`
