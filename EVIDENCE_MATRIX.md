# KUBERA Evidence Matrix

Verified snapshot: **2 October 2026**

This document separates implemented evidence from product direction. Counts below come from the stated current CI/test runs; they are not estimates.

| Project | Current status | Verified evidence | Boundary |
|---|---|---|---|
| **KUBERA AGENT OS / Innovation Stack reference** | Implemented public reference runtime | **173 tests passed** on Python 3.11, 3.12, 3.13; **89%** source branch coverage | Public CI success; not a production security product |
| **KUBERA TAO LAB** | Active private ML research implementation | **34/34 local project tests passed**; compile/diff/secret-pattern checks passed; hardened private CI succeeded | Public dossier; not a live miner and no current-subnet compatibility claim |
| **KUBERA Real Estate OS** | Early verified core + wider product bootstrap | Montenegro land due-diligence core; **3/3 tests passed** on Python 3.11 and 3.12 | Private CI success; wider SaaS integrations not production-labelled |
| **Tender Intelligence** | Tested public applied capability | **16 tests passed** on Python 3.11, 3.12 and 3.13 | Public CI success; outputs remain DRAFT_ONLY / human-controlled |
| **Portfolio Evidence Audit** | Public guardrail | Priority paths and headline claims checked automatically | Public CI success |
| **MCP LAB** | Tested capability layer | Python server tests + TypeScript gateway typecheck workflow | Bounded capabilities; no arbitrary proxy or uncontrolled write layer |
| **Council AI Service Finder** | Public evaluation harness | Deterministic retrieval regression suite and multi-version CI workflow | Evaluation/prototype, not council authority |
| **Community Compass** | Public civic/local prototype | Source/event validators and automated tests | Prototype/local intelligence, not official service |

## Public CI evidence

- Agent OS / Innovation Stack reference — workflow run **37061120307**: Python 3.11, 3.12 and 3.13 jobs succeeded; coverage job succeeded; 173 tests and 89% coverage recorded.
- Tender Intelligence — workflow run **37060909375**: Python 3.11, 3.12 and 3.13 jobs succeeded; 16 tests recorded.
- Portfolio Evidence Audit — workflow run **37061120309**: succeeded on the aligned priority/evidence surface.

Private implementation CI is summarised publicly but private run links are intentionally not used as reviewer dependencies.

## Evidence policy

A metric belongs in the public portfolio only when the current repository or a verified run supports it. Historical marketing-style figures that cannot be independently verified are not used as technical credentials.

## Public/private boundary

The public portfolio exposes architecture, evidence, tests and limitations. It does not expose credentials, client data, private raw datasets, wallet/key material or private repository history merely to make the portfolio look larger.