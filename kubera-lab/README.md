# KUBERA LAB

**AI systems · assurance · bounded agents · ML evaluation · real-estate intelligence · MCP capabilities · civic technology.**

KUBERA LAB is the public engineering record behind the KUBERA portfolio. The rule is simple: a concept, prototype, tested reference and production system are not the same thing, and the repository should say which one it is.

## Current priorities

| Priority | Project | Public evidence | Status |
|---|---|---|---|
| P0 | **KUBERA AGENT OS** | [engineering dossier](agent-os/) · [reference implementation](innovation-stack/reference-implementation/) | verified reference runtime — 173 tests, 89% coverage |
| P1 | **KUBERA TAO LAB** | [ML evidence dossier](kubera-tao-lab/) | active private implementation + public evidence |
| P1 | **KUBERA Real Estate OS** | [product dossier](real-estate-os/) | early verified private core — 3/3 tests; wider product bootstrap |
| P2 | **Tender Intelligence** | [source + tests](tender-intelligence/) | tested applied capability — 16 tests across Python 3.11–3.13 |
| P2 | **MCP LAB** | [architecture + servers + gateway](mcp-lab/) | tested capability layer |
| P2 | **Civic / Local Intelligence** | [Community Compass](dzambala-community-compass/) · [Council AI eval](../research/council-ai-service-finder/eval/v0.1/) | tested prototypes/evaluation |

## Engineering model

```text
real task
  -> bounded capability
  -> source / data
  -> validation + evidence
  -> policy / approval boundary
  -> reversible draft or controlled action
  -> audit record
  -> human authority
```

## P0 — KUBERA AGENT OS

The portfolio's primary systems-engineering track.

The public reference implementation contains executable control mechanics rather than only architecture diagrams:

- Evidence Ledger;
- Builder -> Critic -> Verifier pipeline;
- privacy and tool validation;
- source/evidence/action gates;
- signed approval reference mechanics;
- idempotency and replay control;
- unknown-external-state handling;
- bounded tool adapter interface;
- safe demo;
- automated tests and coverage gate.

[Open Agent OS dossier](agent-os/)

## P1 — KUBERA TAO LAB

Multi-region real-estate ML research focused on temporal validation, leakage control, strict unseen-property testing, model comparison, bias analysis and deployable-model checks.

The implementation remains private; the public dossier publishes verified methodology and benchmark evidence without raw private data or unsafe repository history.

[Open TAO LAB dossier](kubera-tao-lab/)

## P1 — KUBERA Real Estate OS

A London-first product architecture for property intelligence, CRM/workflow automation, governance, analytics and multi-tenant SaaS.

Current status is intentionally labelled **repository bootstrap / architecture**. Production integrations are not claimed until authenticated and tested.

[Open Real Estate OS dossier](real-estate-os/)

## Applied capabilities

### Tender Intelligence
Read-only UK procurement intake, provenance, deterministic qualification, deadline/CPV/requirements/buyer analysis and DRAFT_ONLY bid support.

[Open Tender Intelligence](tender-intelligence/)

### MCP LAB
Reusable bounded capability servers and deny-by-default gateway policy. Agent OS decides when a capability is used; MCP defines the bounded interface.

[Open MCP LAB](mcp-lab/)

### Civic / local intelligence
Deterministic public-service retrieval evaluation and provenance-oriented local/event discovery.

- [Council AI Service Finder](../research/council-ai-service-finder/eval/v0.1/)
- [Community Compass](dzambala-community-compass/)

## Engineering principles

- evidence before claims;
- explicit public/private boundaries;
- no production label without operational proof;
- tests and CI for meaningful implementations;
- no target leakage in ML evaluation;
- provenance for official/public-data workflows;
- deny-by-default capability exposure;
- human approval for consequential external actions;
- credentials and private datasets stay out of public Git;
- failures remain visible and become future controls.

## Portfolio navigation

For a short technical review, use [PORTFOLIO_REVIEW.md](../PORTFOLIO_REVIEW.md).

For current status and ownership boundaries:
- [STATUS.md](../STATUS.md)
- [REPO_MAP.md](../REPO_MAP.md)
- [KUBERA_AGENT_OS.md](../KUBERA_AGENT_OS.md)

**Build small. Verify honestly. Preserve the engineering record.**
