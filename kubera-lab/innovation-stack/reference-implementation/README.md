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

The reference runtime now adds four mechanics for persistent multi-agent work:

### 1. Handoff artifacts
`HandoffArtifact` transfers a task between specialist agents without relying on chat history. It records the previous owner, next owner, task objective, status, output summary, sources, evidence references and exact next action. Every artifact has a deterministic SHA-256 identity and can be rendered as `HANDOFF.md`.

### 2. Source → Evidence → Action gates
`SourceEvidenceActionGate` fails closed before consequential work:

1. the source must be verified;
2. the evidence must be verified;
3. policy and reversibility determine whether execution is allowed.

An irreversible action requires signed human approval even when a general policy would otherwise allow the operation. The signed grant is bound to the action fingerprint (`operation + target + request hash`).

### 3. Idempotent execution reservations
`IdempotencyStore` prevents a retry from silently repeating an external side effect. The same idempotency key with the same request is treated as a replay; reuse with a different request is a conflict.

### 4. Structured action log
`ActionLogger` does not create a second competing audit database. It records action status, actor, target, reversibility, source/evidence references, idempotency key and approval grant ID into the existing hash-chained Evidence Ledger.

## Operational rule

Reversible work can be automated more freely. Irreversible work — publish, send, buy, delete, sign, accept terms, or equivalent external side effects — must cross the action gate and carry exact approval when required.

The implementation deliberately keeps **approval stricter than convenience**: a broad allow rule does not cancel an irreversible-action approval requirement.

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Security boundary

This remains a reference runtime, not a production security product. The Evidence Ledger is tamper-evident hash-chain logic, not immutable external storage or a digital signature service. The signed-grant reference uses a local HMAC signer; production deployments should use protected key material and stronger identity/attestation where required.

The runtime does not claim automatic provider execution, automatic source re-verification, durable distributed workflow recovery, or a complete browser/action sandbox.

## Architecture direction

See [`../DZAMBALA.md`](../DZAMBALA.md) for the sovereign architecture and the distinction between implemented mechanics and future research.
