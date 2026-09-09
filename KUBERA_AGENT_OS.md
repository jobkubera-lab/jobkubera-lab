# KUBERA Agent OS

What we show a customer. What we build next. What already exists in this GitHub.

## One sentence

KUBERA takes a real work task, checks sources, prepares the result, and waits for the human before any consequential external action.

## Why a customer pays

Teams already have ChatGPT, search and ten tabs. They still lose time on:

- unchecked answers
- agents that post or send too early
- no trace of why a result appeared
- disconnected tools that cannot be safely reused
- opportunities discovered too late or pursued without checking delivery fit

KUBERA sells the missing layer: **verified groundwork + reusable capabilities + human authority**.

## Product shape

```text
User / business channel
  -> Agent OS plans
  -> MCP capability selected
  -> bounded tool executes
  -> evidence / result returned
  -> verifier / policy check
  -> draft action
  -> human approve / reject
  -> receipt in ledger
```

## Operational noses / capabilities

- work & documents (CV, employer letter, structured applications)
- local verified lookup (council / events)
- research brief for a business question
- UK Tender Intelligence
- ONS / official-statistics retrieval
- Evidence Ledger/provenance operations
- later: controlled business/booking tools and channel adapters

## KUBERA MCP LAB integration

`kubera-lab/mcp-lab/` is the reusable capability-server layer for Agent OS. It targets MCP 2026-07-28 and stable SDK v2 lines.

The first public servers are:

- `kubera-hello-mcp` — smoke test / learning;
- `kubera-evidence-mcp` — evidence hashes and provenance envelopes;
- `kubera-ons-mcp` — allow-listed read-only ONS API retrieval;
- `kubera-tender-mcp` — deterministic procurement scoring and DRAFT_ONLY bid packs.

The TypeScript gateway reference implements a deny-by-default route/tool registry. It is deliberately not an arbitrary proxy.

MCP does not replace KUBERA Agent OS. Agent OS decides **when** a capability should be used; the MCP server defines **what bounded capability exists**; Control/Evidence layers decide **whether the result/action is trusted**.

## MCP security model

New tools start `READ_ONLY` or `PREPARE_ONLY`.

Consequential write tools require, before implementation:

- explicit tool scope;
- authenticated subject/workspace;
- allow-listed destination;
- rate limit and input/result budgets;
- machine-verifiable human approval receipt;
- idempotency/replay protection;
- audit receipt;
- rollback/compensation strategy where possible.

Free-form model text is never sufficient approval for an external write.

## Tender Intelligence integration

`kubera-lab/tender-intelligence/` is a procurement opportunity nose for Agent OS. It now includes official read-only UK procurement intake plus v1.1 intelligence: checkpoint/pagination, deadline, CPV, requirement verification, buyer-history enrichment, win-gap analysis and draft bid packs.

Tender MCP exposes this existing engine rather than copying its business logic.

Core rules:

- provenance is required;
- scoring is explainable and bounded;
- hard blockers override enthusiasm;
- evidence readiness matters as much as keyword match;
- submission, declarations and legal acceptance remain human actions.

## What is already built

- Civic Evidence OS: tested lookup, fallbacks, no form submit
- Assisted plain-text channel
- Optional profile with consent and erasure
- Community Compass: manual event seeds + validation
- Agent Fabric reference: worker budget, approval gate, hash ledger
- Tender Intelligence v1.1 + official read-only procurement adapters
- MCP LAB foundation + four starter capability servers
- MCP deny-by-default gateway reference
- MCP security baseline, learning track and CI
- Public site + technical libraries

Status line: **tested/reference prototypes; not a live council system, not a procurement authority, not an autonomous submission system, and remote MCP services are not production-labelled until auth/operations gates pass.**

## Demo path

A useful demo should show:

1. user enters a real task;
2. Agent OS chooses one bounded MCP capability;
3. tool returns result + provenance where relevant;
4. KUBERA prepares a draft action;
5. nothing consequential is sent/submitted without approval;
6. audit/evidence record explains what happened.

## Do not build for appearance

Do not create hundreds of copied MCP servers, new Agent OS clones, modules 19–30, uncontrolled scraping, unofficial WhatsApp automation, live posting without approval, arbitrary URL/filesystem tools, or claims of official partnership.

## Commercial direction

Products should be configurations over the same core:

- KUBERA AI Receptionist
- KUBERA Tender Desk
- KUBERA Local Desk
- KUBERA Collector Intelligence
- KUBERA Document Desk

A customer buys the useful workflow, not the words "MCP server".

## Rule

**KUBERA prepares and verifies. MCP exposes bounded capabilities. The human remains the authority.**
