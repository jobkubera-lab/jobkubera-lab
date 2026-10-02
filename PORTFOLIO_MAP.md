# KUBERA Portfolio Map

This page separates the portfolio into **flagship engineering**, **supporting KUBERA projects**, **legacy/archive work**, and **external/reference repositories**.

The purpose is simple: a reviewer should immediately know what represents current KUBERA engineering and what does not.

## 1. Flagship

### KUBERA AGENT OS — current public flagship

**Role:** AI control, assurance and bounded agent execution.

Start here:
- [Public engineering dossier](kubera-lab/agent-os/)
- [Reference implementation](kubera-lab/innovation-stack/reference-implementation/)
- [MCP capability layer](kubera-lab/mcp-lab/)

Verified public evidence includes:
- executable Python reference code;
- automated tests and CI;
- Evidence Ledger mechanics;
- permission and approval boundaries;
- privacy/tool validation;
- idempotency/replay controls;
- safe demo paths;
- explicit failure states.

This is the primary project for technical review.

## 2. Supporting KUBERA engineering

| Project | Role | Status |
|---|---|---|
| KUBERA TAO LAB | ML evaluation and validation discipline | Active research / evidence dossier |
| KUBERA Real Estate OS | Product architecture and applied AI vertical | Private implementation / public dossier |
| KUBERA MCP LAB | Reusable bounded capability servers | Active public engineering track |
| Tender Intelligence | Procurement qualification and evidence workflows | Applied capability |
| Council AI Service Finder | Deterministic resident-language retrieval evaluation | Applied civic-AI evaluation |
| Kubera Guide / Local Intelligence | Field evidence and geographic knowledge | Active applied research |

## 3. Supporting libraries and content

These are useful assets, but they are **not flagship products**:

- `kubera-ai-prompts` — reusable prompt/rule library;
- `kubera-visa-playbooks` — supporting reference material;
- `kubera-migration-templates` — document templates;
- `kubera-learning.` — learning laboratory;
- visual/creative repositories — experimentation and storytelling.

## 4. Legacy / archive

These repositories are retained for history or reference and should not be interpreted as current product direction:

- `kuberajob`;
- `kubera-local-ai2`;
- `kubera-migration-checklist`.

Each should remain clearly labelled **legacy**, **inactive**, or **historical**.

## 5. External / reference repositories

Some public repositories in the account are retained as **reference code, upstream study material, or domain exposure**. They must not be interpreted as original KUBERA products unless a README explicitly says otherwise.

Examples include repositories derived from or associated with:
- GOV.UK infrastructure;
- NHS design systems / LLM evaluation work;
- LocalGov multilingual tooling;
- HSDS mock API;
- humanitarian / mapping open-source projects.

**Rule:** upstream authorship and origin must remain visible. KUBERA-specific work should be documented separately.

## 6. Portfolio maturity rule

A capability is described using one of these states:

- **Implemented** — code exists and runs.
- **Tested** — automated or documented verification exists.
- **Private** — implementation exists but is intentionally not public.
- **Prototype** — exploratory or incomplete.
- **Planned** — design direction only.
- **Legacy** — retained for history; not current.
- **Reference** — external/upstream material; not claimed as original KUBERA work.

## 7. What the portfolio is becoming

The portfolio is being consolidated around one coherent engineering story:

```text
Real-world task
   ↓
KUBERA AGENT OS
   ↓
Model / Tool / API
   ↓
Controlled execution
   ↓
Observability + Evidence
   ↓
Human approval where needed
   ↓
Verified result
```

Applied verticals such as real estate, civic AI, local intelligence and relocation tools demonstrate the same control-and-evidence architecture in different domains.
