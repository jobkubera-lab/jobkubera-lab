# KUBERA Innovation Stack — Public Reference Implementation

This directory contains executable **public reference code** for selected KUBERA Innovation Stack foundation modules plus model-agnostic visual and external-intelligence contracts.

Implemented foundation prototypes:

- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio

Cross-cutting prototype contracts:

- **Visual Systems / DiagramIntent** — validated visual intent independent from a renderer.
- **External Intelligence Node** — provider-independent request/response contract for specialist roles such as auditor, critic, test designer or verifier, with explicit context classification and sharing authorization.

The implementation intentionally uses the Python standard library for runtime logic. It demonstrates clear interfaces and safety properties without exposing any private KUBERA AGENT OS implementation.

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Validation

The v0.3 reference implementation includes **55 unit tests**: 39 foundation tests, 8 Visual Systems tests and 8 External Intelligence contract tests. GitHub CI validates the package across Python 3.11, 3.12 and 3.13.

## Security boundary

This is a reference implementation, not a production security boundary. It does not execute shell commands, call Claude or another external AI provider, access accounts, store credentials, perform autonomous external actions, or provide production DLP. The External Intelligence contract requires explicit sharing authorization for non-public context, but a future gateway must perform real redaction, secret scanning, logging and provider policy enforcement.

See [Security Boundary](docs/SECURITY_BOUNDARY.md) and [Integration Contract](docs/INTEGRATION.md).
