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
`SourceEvidenceActionGate` fails closed before consequential work. Missing source or evidence blocks execution. Irreversible operations require signed approval even when a broad policy says `ALLOW`.

### Idempotent execution
`IdempotencyStore` reserves side-effecting work before execution. Same key + same request becomes a replay; same key + different request becomes a conflict.

### Action log
`ActionLogger` writes operational status and references into the existing hash-chained Evidence Ledger rather than creating a competing audit store.

## v0.9.1 Tool Executor hardening

`SovereignToolExecutor` remains the single reference boundary for injected external tool adapters:

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

Hardening in v0.9.1:

- approval is bound to the **final sanitized and validated payload**, not a pre-redaction payload;
- the approval fingerprint includes actor and idempotency key in addition to operation, target and request hash, preventing grant reuse by another actor or under a fresh retry key;
- `IdempotencyStore` exposes `PENDING` versus `COMPLETE` state and serializes reservations;
- a replay of a pending reservation becomes `UNKNOWN_EXTERNAL_STATE` and is never executed blindly;
- an adapter exception is treated as unknown external state because the reference runtime cannot prove whether a remote side effect happened;
- Evidence Ledger appends are serialized so concurrent action logging preserves one valid hash chain;
- malformed authorization grants fail closed;
- the adapter receives only finalized sanitized tool fields and arguments, never signer/grant objects or signing secrets.

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

The runtime cannot stop arbitrary Python code that already owns provider credentials from bypassing an executor. A real deployment must keep provider clients and credentials outside agent/plugin reach and expose only the controlled executor capability.

The runtime does not claim a live council service, banking service, autonomous posting, automatic provider execution, automatic source re-verification, durable distributed workflow recovery or a complete browser/action sandbox.

## Architecture direction

See [`../DZAMBALA.md`](../DZAMBALA.md) for the sovereign architecture and the distinction between implemented mechanics and future research.
