# KUBERA repository map

Updated: **2026-10-02**

## Public entry points

1. **Profile / portfolio hub** — `jobkubera-lab/jobkubera-lab`
2. **Reviewer route** — `PORTFOLIO_REVIEW.md`
3. **KUBERA LAB index** — `kubera-lab/README.md`

## Priority architecture

### 1. Control — KUBERA AGENT OS
Paths:
- `KUBERA_AGENT_OS.md`
- `kubera-lab/agent-os/`
- `kubera-lab/innovation-stack/reference-implementation/`

Role:
- orchestration;
- policy and permissions;
- source/evidence/action gates;
- approval boundaries;
- idempotency/replay control;
- Evidence Ledger;
- safe tool execution.

### 2. Capability layer — KUBERA MCP LAB
Path: `kubera-lab/mcp-lab/`

Role:
```text
surface -> Agent OS -> MCP gateway -> bounded capability -> source/tool
                                     -> evidence/result -> human-controlled action
```

MCP is a capability boundary, not a replacement Agent OS.

### 3. ML research — KUBERA TAO LAB
Public path: `kubera-lab/kubera-tao-lab/`

Private implementation: `saturnom999-lab/kubera-tao-lab`.

Role:
- model evaluation discipline;
- temporal validation;
- strict unseen-property testing;
- leakage control;
- bias/error analysis;
- ONNX/deployment checks.

### 4. Product architecture — KUBERA Real Estate OS
Public path: `kubera-lab/real-estate-os/`

Private implementation: `jobkubera-lab/kubera-real-estate-os`.

Role:
- property intelligence;
- workflow/CRM architecture;
- governance and multi-tenant design;
- future authenticated integrations.

Current status remains bootstrap; architecture is not labelled as production.

## Applied systems

### Tender Intelligence
Path: `kubera-lab/tender-intelligence/`

Official read-only procurement intake -> normalize/provenance -> deadline/CPV/requirements/buyer checks -> BID/REVIEW/NO-BID -> DRAFT_ONLY bid pack -> human.

### Council AI Service Finder
Path: `research/council-ai-service-finder/eval/v0.1/`

Deterministic resident-language retrieval evaluation with regression tests and explicit fallbacks.

### Community Compass
Path: `kubera-lab/dzambala-community-compass/`

Local/event intelligence with source validation and provenance-oriented data handling.

## Supporting / library repositories

These remain useful but are not flagship portfolio items:
- migration/visa templates;
- learning repositories;
- prompt libraries;
- small infrastructure experiments;
- legacy web prototypes.

Forks used for upstream/open-source participation remain separate from KUBERA product claims.

## Public/private rule

Private implementation history is not made public merely for appearance. Public dossiers expose architecture, status and verified evidence without publishing credentials, client data, raw private datasets or unsafe history.

## Rule

**KUBERA prepares. Capabilities stay bounded. Evidence is explicit. The human remains the authority.**
