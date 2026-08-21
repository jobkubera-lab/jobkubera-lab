# Public / Private Twin

**Status:** `CONCEPT`  
**Layer:** Governance / Publishing

## Purpose
Let one project have two deliberate representations:

- **Private Core** — implementation, prompts, private data, internal failures and credentials.
- **Public Twin** — safe architecture, screenshots, metrics, demo, changelog and documentation.

## Pipeline
```text
Private project → classify files/fields → redact → generate public artifact → verify → publish
```

## Safety rules
Never treat `.gitignore` as a privacy system. Public export must scan for credentials, personal identifiers, private paths, private URLs and forbidden fields before publishing.

## Output
A reproducible manifest describing what was exposed, omitted or transformed.

## Integrations
Private/Public Gate, Personal AI Constitution, GitHub Guardian, Proof-of-Work Portfolio, Living README.

## MVP
A manifest-driven exporter that builds `/public-twin/` from an allowlist rather than copying the whole project.
