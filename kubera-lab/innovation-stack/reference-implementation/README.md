# KUBERA Innovation Stack — Public Reference Implementation

Executable public reference code for selected KUBERA / DZAMBALA foundation modules and cross-cutting control contracts.

## Implemented reference components

- Personal AI Constitution
- Human Authority Budget
- Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio
- Evidence Ledger — SQLite append-only hash-chained records
- Deterministic Agent Pipeline — Builder → Critic → Verifier → Evidence Ledger
- Privacy Gate, strict tool validation and loop protection
- External Intelligence contracts and provider budgets
- Runtime adapter contracts
- Plugin Intelligence Registry

## v0.9 operational trust layer

### Handoff artifacts
`HandoffArtifact` transfers a task between specialist agents without relying on chat history. It records previous owner, next owner, objective, status, output summary, sources, evidence references and exact next action.

### Source → Evidence → Action gates
`SourceEvidenceActionGate` fails closed before consequential work. Missing source or evidence blocks execution. Irreversible operations require signed approval even when a broad policy says `ALLOW`. Approval is bound to the exact action fingerprint.

### Idempotent execution
`IdempotencyStore` reserves side-effecting work before execution. Same key + same request becomes a replay; same key + different request becomes a conflict.

### Action log
`ActionLogger` writes operational status and references into the existing hash-chained Evidence Ledger rather than creating a competing audit store.

### Sovereign Tool Executor
`SovereignToolExecutor` is the single reference boundary for injected external tool adapters:

```text
HandoffArtifact
  → PrivacyGate
  → ToolValidator
  → Source Gate
  → Evidence Gate
  → Action Gate / signed approval
  → IdempotencyStore reserve
  → injected ToolAdapter
  → ActionLogger
  → Evidence Ledger
```

The adapter receives only finalized sanitized arguments. It does not receive the authorization signer or signing secret. A completed request is replayed without a second side effect; a pending reservation without a confirmed result requires reconciliation instead of blind retry.

No real Slack, email, payment, Kickstarter or browser-posting adapter is connected in this reference implementation.

## Operational rule

**KUBERA prepares. The human remains the authority.**

Reversible preparation can be automated more freely. Irreversible operations such as `send`, `publish`, `pay`, `delete` and `sign` require explicit signed approval in the reference executor.

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Security boundary

This remains a reference runtime, not a production security product. The Evidence Ledger is tamper-evident hash-chain logic, not immutable external storage or a digital-signature service. The signed-grant reference uses a local HMAC signer; production deployments should protect key material and use stronger identity/attestation where required.

The runtime does not claim a live council service, banking service, autonomous posting, automatic provider execution, automatic source re-verification, durable distributed workflow recovery or a complete browser/action sandbox.

## Architecture direction

See [`../DZAMBALA.md`](../DZAMBALA.md) for the sovereign architecture and the distinction between implemented mechanics and future research.
