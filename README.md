# NIKOLA KUBERA

## KUBERA Local Desk · DZAMBALA Agent Layer · Civic Evidence

I build practical AI systems that prepare evidence-backed work while keeping consequential authority with the human owner.

> **KUBERA prepares. The human remains the authority.**

Working from **London — Mitcham pilot**.

## Flagship system

| Layer | Project | Role |
| --- | --- | --- |
| **Lookup** | [Civic Evidence OS](https://github.com/jobkubera-lab/kubera-improved-website/tree/main/civic-evidence-os) | Controlled service lookup with official-source evidence and safety fallbacks |
| **Place** | [Community Compass v0.2](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/dzambala-community-compass) | Verified London + Merton community/event discovery with provenance |
| **Control** | [DZAMBALA reference runtime](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/innovation-stack/reference-implementation) | Handoffs, gates, approval, idempotency, tool safety and Evidence Ledger |
| **Craft** | [KUBERA STONES](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/kubera-stones) | One-of-a-kind handmade decorative stones; separate from the AI runtime |

## KUBERA / DZAMBALA control model

```text
Human Owner
    ↓
Project / Handoff Artifact
    ↓
Privacy + Tool Validation
    ↓
Source Gate → Evidence Gate → Action Gate
    ↓
Signed Approval when required
    ↓
Idempotent Tool Execution
    ↓
Action Log → Evidence Ledger
    ↓
Verified Result
```

The public reference runtime is currently **v0.9**. PR #38 added the operational trust layer: `HandoffArtifact`, Source/Evidence/Action gates, exact-action approval binding, `IdempotencyStore`, and `ActionLogger` using the existing hash-chained Evidence Ledger.

PR #39 adds `SovereignToolExecutor`, which composes Handoff → Privacy/Validation → Source/Evidence/Action gates → signed approval → idempotency → injected tool adapter → ActionLogger/Evidence Ledger. The full reference suite is green with **120 tests on Python 3.11, 3.12 and 3.13**.

The next runtime step is red-team review of the executor before connecting one narrowly scoped real adapter through this boundary.

## Engineering principles

- **Human authority:** irreversible external actions require stricter authorization than reversible preparation.
- **Evidence before claims:** official/source evidence is separated from assumptions.
- **Fail closed:** missing source, evidence, authorization or valid tool input blocks execution.
- **Idempotent side effects:** retries must not blindly repeat a completed external action.
- **Provider-neutral architecture:** models and runtimes are replaceable; policy, memory and evidence remain owner-controlled.
- **Privacy by default:** external models and tools receive only the context required for the task.
- **No false production claims:** reference prototypes are not described as live council, banking or autonomous posting services.

## Selected engineering work

### Civic Evidence OS

A working prototype for controlled local-service retrieval. It is designed to return source-backed information and explicit fallbacks rather than inventing official decisions.

[Open Civic Evidence OS](https://github.com/jobkubera-lab/kubera-improved-website/tree/main/civic-evidence-os)

### DZAMBALA Community Compass — London + Merton v0.2

A verified community and event layer with source provenance, freshness checks, filters and validation tests.

[Open Community Compass](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/dzambala-community-compass)

### KUBERA / DZAMBALA reference runtime

Provider-neutral Python reference components for controlled agent execution, including:

- Builder → Critic → Verifier orchestration;
- privacy and secret redaction;
- strict tool-schema validation;
- handoff artifacts;
- source/evidence/action gates;
- signed approval concepts;
- idempotency controls;
- sovereign tool execution boundary;
- action logging and Evidence Ledger;
- failure-prevention and reputation foundations.

[Open Innovation Stack / DZAMBALA](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/innovation-stack)

## Open-source participation

Public civic-tech work includes LocalGov Drupal contribution/proposal activity and technical proposals for public-service interfaces. Experimental work is kept separate from claims of official service ownership or production deployment.

- [LocalGov Drupal issue #927](https://github.com/localgovdrupal/localgov/issues/927)
- [Public-service proposals](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/research/public-service-proposals)

## Libraries and supporting work

Migration/visa templates and older experiments remain libraries or historical material; they are **not** the primary account narrative. The active product direction is Local Desk / agents / evidence / human-controlled execution.

Learning material remains in [kubera-learning.](https://github.com/jobkubera-lab/kubera-learning.) while the canonical repository name is being cleaned up to `kubera-learning`.

## Field evidence

Kubera Guide remains a separate field-mapping and place-documentation project. Its project files are not part of the DZAMBALA runtime.

[View Kubera Guide project](https://github.com/jobkubera-lab/jobkubera-lab/tree/main/kubera-lab/kubera-guide-global-mapping)

## Technical profile

**Python · SQLite · Git · GitHub Actions · AI agents · deterministic validation · JSON / JSON Schema · evidence ledgers · privacy gates · human-in-the-loop controls · interactive maps**

Technical CV: [SHCHEGLOV NIKOLA — AI Engineering Profile](https://github.com/jobkubera-lab/jobkubera-lab/blob/main/career/SHCHEGLOV_NIKOLA_AI_ENGINEERING_PROFILE.md)

## Repository navigation

- [STATUS.md](./STATUS.md) — current work and next step
- [REPO_MAP.md](./REPO_MAP.md) — canonical project map
- [DZAMBALA.md](./kubera-lab/innovation-stack/DZAMBALA.md) — control-layer architecture
- [Reference implementation](./kubera-lab/innovation-stack/reference-implementation/) — executable public runtime
- [KUBERA STONES](./kubera-lab/kubera-stones/) — separate Craft project

## Contact

- GitHub: [jobkubera-lab](https://github.com/jobkubera-lab)
- Email: jobkubera@gmail.com
- Telegram: [@kuberababa](https://t.me/kuberababa)

---

**KUBERA LAB — evidence before claims, privacy by default, human authority.**
