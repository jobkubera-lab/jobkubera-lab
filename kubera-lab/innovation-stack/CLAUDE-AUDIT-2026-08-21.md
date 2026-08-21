# DZAMBALA — Claude Audit Verification (2026-08-21)

This document records a fact-check of Claude's latest audit against the actual current `main` branch and current upstream documentation. It is not a claim that every suggested feature is already implemented.

## Status legend
- `VERIFIED`: confirmed in current code/docs.
- `ALREADY_FIXED`: Claude identified a past weakness that current main already closes.
- `WRONG/STALE`: contradicted by current repository state or stronger primary sources.
- `NEXT`: useful work not yet implemented.
- `RESEARCH`: long-horizon idea; not production-ready.

## Repository corrections

### agent_pipeline.py
Status: `WRONG/STALE` in Claude report.

The file exists at:
`reference-implementation/src/kubera_innovation/agent_pipeline.py`

It implements an injected deterministic Builder → Critic → Verifier pipeline and records every stage in Evidence Ledger.

### evidence_ledger.py
Status: `WRONG/STALE` in Claude report.

The file exists at:
`reference-implementation/src/kubera_innovation/evidence_ledger.py`

It implements SQLite-backed append-only records, canonical hashing, previous-hash chaining and `verify_chain()`.

### Plugin Intelligence Registry
Status: `VERIFIED PROTOTYPE`.

`plugin_registry.py` exists and enforces candidate/license/security/permission/adoption metadata. It does **not** yet download or sandbox third-party code automatically; it is a safety-oriented metadata gate, not a full plugin scanner.

## Claude findings that remain valid

1. Authorization grant should bind to the exact approved context packet, not only an abstract target. `NEXT`.
2. Authorization grant replay should be bounded/idempotent. `NEXT`.
3. Sharing scope should include the intended role/purpose. `NEXT`.
4. ProviderSeriesBudget needs persistence and concurrency safety. `NEXT`.
5. Runtime checkpoint resume needs stronger authorization/integrity semantics. `NEXT`.
6. Secret/DLP scanning before outbound model calls is still missing. `NEXT`.
7. Real provider adapters are still missing. `NEXT`.
8. Model Router is still missing. `NEXT`.
9. Skill DNA executable schema/runtime is still missing. `NEXT`.
10. Context Firewall packet builder is still missing. `NEXT`.

## Claude suggestions that need correction

### Evidence Ledger is not "from scratch"
It already exists and has tests. The next version should harden it with purpose-specific signatures/checkpoints and provider receipts rather than recreate it.

### Do not reuse the human-approval signing key as a permanent ledger-integrity key
Human consent grants expire; historical evidence signatures should remain verifiable. Production design should use a separate purpose-specific integrity key (or separate hardware-backed/asymmetric key) even if the low-level crypto helper is shared.

### Do not allow raw full-repository export as an "elevated grant" shortcut
`PRIVATE` must remain inside the sovereign boundary. Large-repository review should create a sanitized PROJECT packet, not approve raw PRIVATE export.

### Model Router privacy rule
For `PRIVATE`, external/cloud candidates must be hard-filtered out. Privacy is not a tie-break. It is a hard eligibility constraint.

### Model Router cost scoring
`cost_per_1k_tokens <= max_cost` is not sufficient. Production routing should estimate total request cost from input/output token estimates and provider pricing.

### Skill DNA should not depend directly on ExternalRole
Internal skills exist that are not external audit roles. Skill identity/authority should be provider- and role-independent; an external role may be one optional execution binding.

### Commit-reveal is not verifiable compute
A response commitment can prove the provider did not change a committed answer later. It does not prove the provider executed the requested model, prompt, role or computation correctly. ZK/verifiable inference remains research.

### Differential privacy for arbitrary code/text packets
Differential privacy is mature for statistical queries and model training, but it is not a general replacement for semantic minimization/redaction of arbitrary source code. Treat this as `RESEARCH`, not a near-term privacy control.

## Industry fact-check

### MCP 2026-07-28
`VERIFIED`: the protocol core moved to stateless request/response at the protocol layer. Application state can still be explicit.

### LangGraph durable execution
Primary LangGraph documentation explicitly describes durable execution, persistence and resume-after-failure as first-class capabilities. Therefore a third-party statement that LangGraph has "only checkpointing, not durable execution" is not accepted as a settled fact. DZAMBALA should use a runtime adapter and benchmark actual guarantees instead of making a blanket claim.

### AutoGen
`VERIFIED`: teams, reflection/critic patterns, pause/resume state, and experimental GraphFlow with sequential/parallel/conditional/cyclic execution exist.

### CrewAI
Current official documentation advertises flows with state persistence/resume, guardrails, memory, observability and human-in-the-loop triggers. Claims that human-in-the-loop exists only at the end of a task are outdated/unsupported as a general statement.

### OpenAI Agents SDK
`VERIFIED`: handoffs, guardrails, sessions, structured outputs, tracing and provider-neutral test utilities exist. "Low production readiness" is an opinion from secondary reviews, not a fact DZAMBALA should encode.

### Temporal
`VERIFIED`: durable execution and resume-after-failure are core platform claims. DZAMBALA should consider Temporal or comparable engines as optional RuntimeAdapter implementations instead of reimplementing a full durable workflow engine.

## Approved near-term engineering direction

1. Harden authorization grant binding/replay/role scope.
2. Harden ProviderSeriesBudget persistence/concurrency.
3. Harden RuntimeCheckpoint integrity and resume authorization.
4. Add SecretScanner.
5. Add ContextFirewall.
6. Add provider-neutral ExternalProvider protocol and Claude adapter with injected transport/fake tests.
7. Add privacy-first ModelRouter.
8. Add provider-independent Skill DNA schema/runtime.
9. Extend existing EvidenceLedger with provider receipts, artifact hashes and separate integrity signing/checkpoints.
10. Integrate these into the existing deterministic AgentPipeline.

Every item stays `NEXT` until code + tests + CI pass.
