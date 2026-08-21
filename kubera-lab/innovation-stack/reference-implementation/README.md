# KUBERA Innovation Stack — Public Reference Implementation

Executable public reference code for selected KUBERA Innovation Stack foundation modules and cross-cutting contracts.

## Implemented foundation prototypes
- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio
- Evidence Ledger — SQLite append-only hash-chained records
- Deterministic Agent Pipeline — Builder → Critic → Verifier → Evidence Ledger

## Cross-cutting prototype contracts
- Visual Systems / DiagramIntent
- External Intelligence Node — hardened provider-independent audit/critic handoff
- Plugin Intelligence Registry — safe external capability intake

## External Intelligence v0.5 hardening
The External Intelligence contract enforces:
- `PRIVATE` context never leaves KUBERA;
- role-specific context ceilings;
- explicit authorization for `PROJECT` packets;
- request UUID and UTC timestamp;
- contract versioning;
- SHA-256 context identity;
- redaction metadata;
- timeout/token budgets;
- provider/model/version/latency metadata;
- finding confidence;
- separate provider/transport execution status from review verdict.

## v0.6 deterministic pipeline
The first executable Agent Society control loop now runs without any external model dependency. Builder, Critic and Verifier are injected Python callables. Each stage is written into an SQLite Evidence Ledger with input/output hashes and a hash link to the previous record.

This proves orchestration mechanics and evidence recording before adding provider adapters.

## Run
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Security boundary
The public code still does not call Claude or another provider and is not production DLP. A future provider adapter must implement secret scanning, minimum-purpose packet construction, structured provider output, authentication, retries and provider-policy enforcement.

The Evidence Ledger hash chain is tamper-evident reference logic, not a digital signature or immutable external audit service.

## Research direction
See [`../HORIZON-2040.md`](../HORIZON-2040.md) for a clearly labelled comparison between current agent frameworks and long-horizon KUBERA research hypotheses.
