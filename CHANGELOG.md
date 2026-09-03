# CHANGELOG

All notable changes to KUBERA LAB are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.9.1] — 2026-09-03

### Added

- **SovereignToolExecutor** — single choke point for all external side effects
- **IdempotencyStore** — prevents duplicate actions on retries (PENDING/COMPLETE states)
- **SignedApproval** — exact-action fingerprinting for consequential decisions
- **ActionLogger** — writes to Evidence Ledger instead of separate audit database
- **WorkContract** — five-field specialist work boundaries (Job, Sources, Judgment, Output, Forbidden)
- **LocalDraftAdapter** — reversible tool path: task → brief → approval → local draft

### Changed

- Tool Executor hardened: approval now bound to finalized sanitized payload + actor + idempotency key
- UNKNOWN_EXTERNAL_STATE handling improved for uncertain adapter responses
- Evidence gates require actual ledger resolution (no boolean substitutes)
- DZAMBALA operational trust layer now reference-implemented

### Fixed

- Reversibility boundary now enforced: preparation vs. irreversible side effects
- Source Gate → Evidence Gate → Action Gate chain now strict
- Privacy validation prevents PRIVATE context leakage to external providers

### Documentation

- [KUBERA_OPERATOR.md](./kubera-lab/innovation-stack/KUBERA_OPERATOR.md) — operational rules
- [DZAMBALA.md](./kubera-lab/innovation-stack/DZAMBALA.md) — control-layer architecture
- [STATUS.md](./STATUS.md) — current work and next steps

---

## [0.2] — 2026-08-29

### Added

- **Community Compass v0.2** — verified geographic discovery for London + Merton
- **Kubera Guide** — 1.1M+ Google Maps views, structured place documentation
- **KUBERA Visual Systems** — DiagramIntent contract for renderer-independent visual requests
- **Agent Fabric** — trust mesh and approval gates for agent-to-agent work

### Changed

- DZAMBALA reframed as sovereign layer above replaceable runtimes
- Innovation Stack reduced to 18 core modules (no expansion)
- Migration/visa templates moved to library/archive status
- Profile narrowed to three active flagships

### Deprecated

- Innovation-stack modules 19+ (rejected)
- Separate product lines from Innovation Stack modules

---

## [0.1] — 2026-08-15

### Added

- **Civic Evidence OS** — source-backed local-service lookup
  - Privacy-conscious ResidentProfile
  - Evidence ledger (SHA-256 hashed queries)
  - Source/Evidence/Action gates
  - Fallback on ambiguity
  
- **Mitcham Survival Map** — 19 verified park records
  - Official coordinates and source links
  - Mobile-first responsive design
  - PWA shell
  
- **Morden Hall Park Digital Trail** — National Trust prototype proposal
  - Independent interactive experience
  - Requires National Trust approval for production

### Initial releases

- KUBERA LAB public project structure
- Kubera Guide project page (1.1M+ views)
- KUBERA Innovation Stack definition (18 modules)
- Foundation modules with executable reference implementation

---

## Unreleased

### Planned (Next iteration)

- **GeoMemory prototype** — from already-public map records
- **Shared schemas** for remaining Innovation Stack modules
- **Public reference contracts** connected to private KUBERA AGENT OS
- **Reproducible demos** and proof-of-work dashboards
- **Failure Vaccine** — regression tests from verified failures

### In research (2040 horizon)

- Sovereign Agent Kernel — portable governance above several runtimes
- Verifiable Agent History — cryptographically linked evidence records
- Context Firewall — minimum-purpose review packets
- Capability Market with Trust — permission profiles and provenance
- Model Competition — multiple providers reviewed independently
- Permission Economics — authority as consumable resource

---

## Frozen / Not expanding

Per [STATUS.md](./STATUS.md):

- **Innovation Stack modules** — 18 total, no modules 19+
- **Control layer** — DZAMBALA.md + reference-implementation/ are active; rest frozen
- **Migration/visa templates** — library material, not primary product line

---

## See also

- [STATUS.md](./STATUS.md) — current workspace status and next steps
- [KUBERA_OPERATOR.md](./kubera-lab/innovation-stack/KUBERA_OPERATOR.md) — execution flow
- [DZAMBALA.md](./kubera-lab/innovation-stack/DZAMBALA.md) — architecture and principles
- [CONTRIBUTING.md](./CONTRIBUTING.md) — how to contribute

---

**KUBERA prepares. The human remains the authority.**
