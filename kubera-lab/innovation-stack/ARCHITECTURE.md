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

Turns architecture, data, workflows and timelines into explicit visual artifacts. Visual output remains subject to privacy/publication policy and does not depend on one LLM vendor.

### 4. Agent layer
`KUBERA AGENT OS` · `Agent Reputation Engine` · `Agent Society`

Routes work between models, skills and tools while measuring reliability.

### 5. Governance layer
`Personal AI Constitution` · `Human Authority Budget` · `Public / Private Twin`

Defines what agents may do, for how long, with which data, and what may become public.

### 6. Learning layer
`Evidence Ledger` · `Decision Replay` · `Failure Vaccine`

Preserves why decisions happened and turns important failures into future prevention.

### 7. Delivery layer
`Proof-of-Work Portfolio` · `Living README` · `GitHub Guardian`

Makes engineering progress visible, verifiable and maintainable.

### 8. Application layer
`Geographic Intelligence Agent` · `British English Personal Language Agent`

Demonstrates how the architecture can produce domain-specific agents.

## Reference flow

```text
Human goal
  ↓
Personal AI Constitution
  ↓
Life → System Compiler
  ↓
Reality Graph / Project Memory
  ↓
DiagramIntent (when visual explanation is useful)
  ↓
Orchestrator → Model Router → Skill / Tool
  ↓
Human Authority Budget
  ↓
Execution
  ↓
Self Check
  ↓
Evidence Ledger
  ↓
Reputation update + Failure Vaccine
  ↓
Private/Public Gate
  ↓
Proof of Work / Living README / Visual artifact
```

## Visual contract rule

The Visual Systems Layer defines intent and validation separately from the renderer. This allows a future local renderer, Diagram Design, or another compatible capability to be swapped without changing the upstream project logic.

## Geographic provenance rule

GeoMemory records must distinguish `first_hand`, `external_source` and `model_inference`. Kubera Guide is treated as a source of first-hand public place observations, not as a substitute for current external facts such as opening hours or transport status.

## Interoperability rule

Every module should expose simple, replaceable interfaces: JSON/YAML records, SQLite tables, Markdown specifications or tool APIs. No module should require one specific LLM vendor to remain useful.
