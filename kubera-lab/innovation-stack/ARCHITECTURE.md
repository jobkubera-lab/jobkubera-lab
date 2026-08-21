# KUBERA Innovation Stack — Architecture

## System layers

### 1. Reality layer
`Reality Graph` · `GeoMemory` · `City DNA` · `Creative Object DNA`

### 2. Translation layer
`Life → System Compiler` · `Prompt Evolution Engine`

### 3. Visual Systems layer — cross-cutting
`DiagramIntent` · external renderer adapters · brand tokens · accessibility checks

### 4. Agent layer
`KUBERA AGENT OS` · `Agent Reputation Engine` · `Agent Society` · `External Intelligence Node`

External models are specialist workers behind a common contract, not owners of project memory.

### 5. Governance layer
`Personal AI Constitution` · `Human Authority Budget` · `Public / Private Twin` · `Context / Privacy Gate`

### 6. Learning layer
`Evidence Ledger` · `Decision Replay` · `Failure Vaccine`

### 7. Delivery layer
`Proof-of-Work Portfolio` · `Living README` · `GitHub Guardian`

### 8. Capability intake layer — cross-cutting
`Plugin Intelligence Registry` · `Plugin Gate` · sandbox review · license/security checks

### 9. Application layer
`Geographic Intelligence Agent` · `British English Personal Language Agent`

## Hardened multi-model flow

```text
Human goal
  ↓
Personal AI Constitution
  ↓
KUBERA Orchestrator
  ↓
Context / Privacy Gate
  ├─ PRIVATE → LOCAL ONLY (never external)
  └─ PUBLIC / sanitized PROJECT packet
             ↓
     role ceiling + DLP + hash + budget
             ↓
┌──────────────────┬───────────────────────┬──────────────────┐
│ Builder model    │ External Intelligence │ Local/private AI │
│ create           │ critique / audit      │ private work     │
└──────────────────┴───────────────────────┴──────────────────┘
             ↓ structured response
     Post-Gate / schema validation
             ↓
Evidence Ledger
             ↓
Self-Check
             ↓
Human decision
```

## External intelligence invariant
`PRIVATE` information never crosses the external-provider boundary. If an external specialist needs insight derived from private code, KUBERA creates a minimum sanitized `PROJECT` review packet first. The packet is hashed after redaction and its disclosure is recorded.

## Provider failure invariant
A failed external invocation never becomes a fake task verdict. Transport/provider/schema failures have an independent execution status.

## Interoperability rule
Modules expose replaceable JSON/YAML, SQLite, Markdown or API contracts. No module should require one specific LLM vendor to remain useful.
