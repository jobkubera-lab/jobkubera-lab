# Nikola Kubera

## AI Systems Builder · Infrastructure & Assurance · Evidence-Driven Automation

I build practical AI systems with an emphasis on bounded agent execution, evidence, reproducible evaluation, human authority and clear public/private boundaries.

My public engineering record is organised around a small number of priorities rather than a long list of unrelated experiments.

## Priority portfolio

### P0 — KUBERA AGENT OS

KUBERA AGENT OS is the control and assurance layer for bounded AI workflows.

Verified public reference evidence on 2 October 2026:

- **173 tests passed** on Python 3.11, 3.12 and 3.13;
- **89% source branch coverage**, with an enforced 85% floor;
- Evidence Ledger, policy/approval gates, privacy/tool validation, idempotency and replay handling;
- safe demo and GitHub Actions verification.

[Open Agent OS dossier](kubera-lab/agent-os/)  
[Open reference implementation](kubera-lab/innovation-stack/reference-implementation/)

### P1 — KUBERA TAO LAB

A private multi-region real-estate ML research implementation with a public evidence dossier.

Verified on 2 October 2026:

- **34/34 local project tests passed**;
- private GitHub Actions CI succeeded on the hardened pipeline commit;
- temporal train/validation/test separation;
- strict unseen-property evaluation;
- leakage controls and explicit weak-segment reporting.

[Open TAO LAB evidence dossier](kubera-lab/kubera-tao-lab/)

### P1 — KUBERA Real Estate OS

A private London-first real-estate product repository with a public architecture/status dossier.

The current private core includes an evidence-first Montenegro land due-diligence module that fails closed when official registry evidence is missing.

Verified on 2 October 2026:

- **3/3 tests passed**;
- GitHub Actions succeeded on Python 3.11 and 3.12;
- broader SaaS/integration work remains product bootstrap, not production-labelled.

[Open Real Estate OS dossier](kubera-lab/real-estate-os/)

### P2 — Applied capabilities

- [Tender Intelligence](kubera-lab/tender-intelligence/) — deterministic UK procurement qualification, provenance, hard blockers and DRAFT_ONLY output. Current CI: **16 tests passed** on Python 3.11, 3.12 and 3.13.
- [MCP LAB](kubera-lab/mcp-lab/) — bounded capability servers and a deny-by-default gateway policy.
- [Council AI Service Finder](research/council-ai-service-finder/eval/v0.1/) — deterministic resident-language retrieval evaluation.
- [Community Compass](kubera-lab/dzambala-community-compass/) — provenance-oriented local/event intelligence.

## Engineering method

```text
problem
  -> scope and evidence
  -> architecture
  -> implementation
  -> tests / CI
  -> explicit failure modes
  -> human review
  -> documented evidence
```

I do not treat an AI answer, architecture diagram or README statement as proof by itself. Important claims should be supported by code, tests, CI, source records or clearly labelled limitations.

## KUBERA design principles

- evidence before claims;
- models and providers are replaceable;
- permissions and private context stay under owner control;
- external capabilities are bounded and deny-by-default;
- consequential actions require human authority;
- test failures and weak metrics remain visible;
- private datasets, credentials and unsafe repository history stay private;
- prototypes are not described as production systems.

## Mapping and local intelligence

Kubera Guide is a field-built mapping and place-documentation project using original observations, photographs and structured location information. It informs KUBERA local-intelligence work, but unsupported historical reach metrics are not used as engineering credentials.

[Open Kubera Guide project](kubera-lab/kubera-guide-global-mapping/)

## Reviewer route

For a short technical review, start with [PORTFOLIO_REVIEW.md](PORTFOLIO_REVIEW.md) and [EVIDENCE_MATRIX.md](EVIDENCE_MATRIX.md).

**Build small. Verify honestly. Keep humans in control.**
