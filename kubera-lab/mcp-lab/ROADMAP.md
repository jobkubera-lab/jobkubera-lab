# KUBERA MCP LAB Roadmap

## Phase 0 — foundation (this change)

- [x] define architecture and security baseline
- [x] target MCP 2026-07-28 / SDK v2
- [x] local stdio starter server
- [x] evidence, ONS and tender capability starters
- [x] TypeScript gateway reference
- [x] learning track
- [x] regression tests for shared policy logic

## Phase 1 — local capability maturity

- [ ] connect ONS MCP to the existing verified ONS adapter/runtime
- [ ] expose Tender Intelligence v1.1 through typed MCP tools without duplicating scoring logic
- [ ] connect Evidence MCP to the shared append-only Evidence Ledger contract
- [ ] add Local MCP backed by Civic Evidence OS/Local Desk allow-listed official sources
- [ ] add document MCP with explicit file scopes and no arbitrary filesystem traversal
- [ ] add contract tests for every tool schema

Exit criterion: four useful local servers can be called by an MCP host and return verified structured outputs with tests.

## Phase 2 — gateway and remote hardening

- [ ] implement real gateway transport proxy with SDK v2
- [ ] add authenticated subject/client context
- [ ] per-server/tool allow-list
- [ ] per-tool quotas and result-size budgets
- [ ] request IDs + minimal structured audit log
- [ ] health/readiness endpoints
- [ ] container build and non-root runtime
- [ ] CI dependency/security checks
- [ ] documented rollback

Exit criterion: one read-only server can run remotely behind HTTPS without exposing unrestricted tools or secrets.

## Phase 3 — MCP Apps / operator UI

- [ ] compact Tender Intelligence decision card
- [ ] evidence/source inspector
- [ ] ONS statistic/result table
- [ ] tool approval preview for future writes
- [ ] sandbox/network policy review for MCP Apps

Exit criterion: UI visualizes verified capability outputs but does not bypass tool policy.

## Phase 4 — business channels

- [ ] WhatsApp gateway (official Business Platform only)
- [ ] website chat surface
- [ ] email intake where appropriate
- [ ] tenant/workspace isolation
- [ ] customer-specific tool configuration

Exit criterion: channels remain replaceable; MCP capabilities stay reusable underneath.

## Phase 5 — controlled write tools

Potential tools:

- prepare booking -> human approves -> create booking
- prepare customer reply -> human approves -> send
- prepare CRM update -> human approves -> write

Requirements before implementation:

- approval receipt contract;
- idempotency key;
- replay protection;
- audit receipt;
- rollback/compensation strategy where possible;
- explicit customer authorization.

## Phase 6 — commercial packs

Reusable vertical configurations, not forks of the core:

- KUBERA AI Receptionist
- KUBERA Tender Desk
- KUBERA Local Desk
- KUBERA Collector Intelligence
- KUBERA Document Desk

Each product is a surface + policy + selected MCP capabilities, not a new incompatible platform.

## Non-goals

- hundreds of low-value copied MCP servers;
- autonomous procurement submission;
- unofficial WhatsApp automation;
- arbitrary browser/filesystem tools exposed to models;
- storing customer secrets in GitHub;
- claiming production readiness before security/operations gates pass.
