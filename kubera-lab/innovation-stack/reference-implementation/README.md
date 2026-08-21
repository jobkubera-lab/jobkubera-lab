# KUBERA Innovation Stack — Public Reference Implementation

This directory contains executable public reference code for selected KUBERA Innovation Stack foundation modules plus model-agnostic visual, external-intelligence and plugin-intake contracts.

Implemented foundation prototypes:

- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio

Cross-cutting prototype contracts:

- **Visual Systems / DiagramIntent** — validated visual intent independent from a renderer.
- **External Intelligence Node** — provider-independent request/response contract for specialist external AI roles.
- **Plugin Intelligence Registry** — safety-oriented metadata and adoption gates for third-party capabilities.

## Validation
The v0.4 reference implementation includes **63 unit tests**: 39 foundation tests, 8 Visual Systems tests, 8 External Intelligence tests and 8 Plugin Registry tests. GitHub CI validates the package across Python 3.11, 3.12 and 3.13.

## Security boundary
This project does not automatically install third-party plugins. Discovery is not trust. A candidate must pass license review, security review, explicit permission profiling, human approval and sandbox testing before adoption.
