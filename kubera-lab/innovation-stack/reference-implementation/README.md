# KUBERA Innovation Stack — Public Reference Implementation

This directory contains executable **public reference code** for selected KUBERA Innovation Stack foundation modules plus a model-agnostic visual-system contract.

Implemented foundation prototypes:

- Personal AI Constitution
- Human Authority Budget
- KUBERA Reality Graph
- Failure Vaccine
- Agent Reputation Engine
- Proof-of-Work Portfolio

Cross-cutting prototype contract:

- **Visual Systems / DiagramIntent** — validates one of 39 diagram categories, HTML/SVG/PNG output, detail, theme, optional brand source, Mermaid/draw.io source format and static/motion preference. It does not vendor or execute a third-party renderer.

The implementation intentionally uses the Python standard library for runtime logic. It demonstrates clear interfaces and safety properties without exposing any private KUBERA AGENT OS implementation.

## Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

## Validation

The v0.2 reference implementation includes **47 unit tests**: the original 39 foundation tests plus 8 Visual Systems contract tests. GitHub CI validates the package across Python 3.11, 3.12 and 3.13.

## Security boundary

This is a reference implementation, not a production security boundary. It does not execute shell commands, access accounts, store credentials, perform autonomous external actions, or silently publish private diagrams.

See [Security Boundary](docs/SECURITY_BOUNDARY.md) and [Integration Contract](docs/INTEGRATION.md).
