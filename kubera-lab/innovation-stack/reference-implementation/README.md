# KUBERA Innovation Stack — Public Reference Implementation

Executable public reference code for selected KUBERA Innovation Stack foundation modules and cross-cutting contracts.

## Implemented foundation prototypes
- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio

## Cross-cutting prototype contracts
- Visual Systems / DiagramIntent
- External Intelligence Node — hardened provider-independent audit/critic handoff
- Plugin Intelligence Registry — safe external capability intake

## External Intelligence v0.5 hardening
The External Intelligence contract now enforces:
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

The public code still does not call Claude or another provider and is not production DLP. A future adapter must implement secret scanning, exact packet construction, API/tool structured output, Evidence Ledger persistence and provider authentication.

## Run
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Validation
The v0.5 reference implementation contains the existing test suite plus expanded External Intelligence hardening tests. GitHub CI validates Python 3.11, 3.12 and 3.13.
