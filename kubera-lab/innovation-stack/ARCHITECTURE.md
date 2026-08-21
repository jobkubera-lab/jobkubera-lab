# KUBERA Innovation Stack — Architecture

## System layers

### 1. Reality layer
`Reality Graph` · `GeoMemory` · `City DNA` · `Creative Object DNA`

Captures structured facts, relationships, place knowledge and object/project context.

### 2. Translation layer
`Life → System Compiler` · `Prompt Evolution Engine`

Turns human intent and observations into technical specifications, experiments and repeatable instructions.

### 3. Visual Systems layer — cross-cutting
`DiagramIntent` · external renderer adapters · brand tokens · accessibility checks

Turns architecture, data, workflows and timelines into explicit visual artifacts.

### 4. Agent layer
`KUBERA AGENT OS` · `Agent Reputation Engine` · `Agent Society` · `External Intelligence Node`

Routes work between models, skills and tools while measuring reliability. External models are specialist workers behind a common contract, not owners of project memory.

### 5. Governance layer
`Personal AI Constitution` · `Human Authority Budget` · `Public / Private Twin` · `Context / Privacy Gate`

Defines what agents may do, for how long, with which data, and what may leave the private boundary.

### 6. Learning layer
`Evidence Ledger` · `Decision Replay` · `Failure Vaccine`

Preserves why decisions happened and turns important failures into future prevention.

### 7. Delivery layer
`Proof-of-Work Portfolio` · `Living README` · `GitHub Guardian`

Makes engineering progress visible, verifiable and maintainable.

### 8. Application layer
`Geographic Intelligence Agent` · `British English Personal Language Agent`

Demonstrates how the architecture can produce domain-specific agents.

## Reference multi-model flow

```text
Human goal
  ↓
Personal AI Constitution
  ↓
KUBERA Orchestrator
  ↓
Context / Privacy Gate
  ↓
┌──────────────────┬───────────────────────┬──────────────────┐
│ Builder model    │ External Intelligence │ Local/private AI │
│ create           │ critique / audit      │ private work     │
└──────────────────┴───────────────────────┴──────────────────┘
  ↓ structured handoffs
Evidence Ledger
  ↓
Self-Check
  ↓
Human decision
```

## External intelligence rule
Project memory belongs to KUBERA. External providers receive only task-scoped context. `PROJECT` and `PRIVATE` context requires explicit sharing authorization in the public reference contract. A production gateway must additionally redact secrets, enforce provider policies and record disclosure metadata.

## Visual contract rule
The Visual Systems Layer defines intent and validation separately from the renderer, allowing visual capabilities to be replaced without changing upstream project logic.

## Interoperability rule
Every module should expose simple, replaceable interfaces: JSON/YAML records, SQLite tables, Markdown specifications or tool APIs. No module should require one specific LLM vendor to remain useful.
