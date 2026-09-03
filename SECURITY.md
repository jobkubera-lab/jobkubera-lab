# SECURITY POLICY

## Scope

This repository contains public reference implementations, research prototypes, documentation, and demos for KUBERA / DZAMBALA.

The active reference runtime is **not** presented as a production identity, banking, council, autonomous publishing, payment, or credential-management system.

The current control-path security focus includes:

- human authority for consequential actions;
- Source → Evidence → Action gates;
- exact-action approval binding;
- idempotency and unknown-state handling;
- privacy/sanitization before tool execution;
- Evidence Ledger logging;
- a single reference execution boundary through `SovereignToolExecutor`.

## Supported code

Security fixes should prioritize the active files under:

```text
kubera-lab/innovation-stack/reference-implementation/
kubera-lab/innovation-stack/DZAMBALA.md
kubera-lab/innovation-stack/KUBERA_OPERATOR.md
```

Frozen Innovation Stack modules are not production products and should not be expanded merely to address speculative scenarios.

## Reporting a vulnerability

Do **not** place secrets, credentials, personal data, exploit payloads containing sensitive material, or private customer information in a public GitHub issue.

For a suspected security vulnerability, contact:

**jobkubera@gmail.com**

Include, where safe:

- affected file/component;
- concise impact description;
- reproducible steps using non-sensitive test data;
- expected vs. actual security behavior;
- suggested mitigation if known.

If a public issue is appropriate because no sensitive exploit detail is required, keep the report minimal and do not include credentials or private data.

## Security invariants

Changes to the active executor/control layer should preserve these invariants:

1. Missing or unresolved source/evidence fails closed for consequential execution.
2. Irreversible operations require explicit scoped approval even if broader policy is permissive.
3. Approval is bound to the finalized action identity/payload used by the executor.
4. Same completed idempotency key + same request does not repeat the side effect.
5. Pending/unknown external state is reconciled before retry.
6. Same idempotency key + different request conflicts.
7. Raw credentials and secrets are not intentionally stored in Handoff artifacts or Evidence Ledger entries.
8. Application/example code must not bypass `SovereignToolExecutor` to invoke side-effecting adapters directly.
9. Reference/demo signers and local adapters must not be described as production-grade credential infrastructure.
10. The human owner remains the final authority for consequential action.

## Known reference limitations

The public reference runtime intentionally documents limitations instead of hiding them. Examples include reference signing/key handling, local persistence choices, regex/data-minimization limits, and the absence of hardened production credential infrastructure.

A passing test suite demonstrates tested behavior in the reference implementation; it is not a certification of production security.

## Dependency and supply-chain changes

New runtime dependencies, external adapters, model-provider integrations, or protocol connectors require review of:

- license and provenance;
- permission scope;
- secret handling;
- network/data exposure;
- retry/idempotency behavior;
- failure-state reconciliation;
- tests covering blocked and adversarial paths.

Do not add a real send/publish/pay/delete/sign adapter as a documentation-only change.

**KUBERA prepares. The human remains the authority.**
