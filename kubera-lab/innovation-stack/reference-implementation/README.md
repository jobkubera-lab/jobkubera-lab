# KUBERA Innovation Stack — Public Reference Implementation

This directory contains executable **public reference code** for six foundation modules from the KUBERA Innovation Stack.

Implemented in v0.1:

- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio

The implementation intentionally uses the Python standard library for runtime logic. It is designed to demonstrate clear interfaces and safety properties without exposing any private KUBERA AGENT OS implementation.

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Validation

The v0.1 reference implementation includes **39 unit tests** covering governance decisions, consumable authority, visibility-safe graph export, explicit failure rules, verified-only reputation scoring, proof-of-work ordering and combined governance gates.

## Security boundary

This is a reference implementation, not a production security boundary. It does not execute shell commands, access accounts, store credentials, or perform autonomous external actions.

See [Security Boundary](docs/SECURITY_BOUNDARY.md) and [Integration Contract](docs/INTEGRATION.md).
