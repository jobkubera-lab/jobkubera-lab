# External AI Controls — Adoption Record

Verified: 2026-09-04

**KUBERA prepares. The human remains the authority.**

This record documents how KUBERA should use selected external AI infrastructure ideas without turning the reference runtime into a vendor-locked stack.

## Decision summary

| Project / standard | Decision | KUBERA use |
| --- | --- | --- |
| LiteLLM | ADOPT AS OPTIONAL GATEWAY PATTERN | OpenAI-compatible provider boundary, routing/fallback/budget ideas. Do not vendor the project or depend on enterprise-only code. |
| Presidio | ADOPT OPTIONAL INTEGRATION | PII detection/redaction before model or external-tool egress. Core runtime remains dependency-free. |
| OPA / Casbin | DEFER | Useful when KUBERA needs centrally administered policy across several services. Current WorkContract + GovernanceGate + signed grants already cover the reference runtime. |
| NeMo Guardrails | DEFER | Conversational/model guardrails are separate from KUBERA's deterministic action-authority boundary. Consider only for a concrete dialogue-safety requirement. |
| civic-ai-tools | ADOPT ARCHITECTURAL PATTERN | Portable evidence packages: source/claim metadata + hashes so a result can be inspected without storing raw prompts in the public artifact. |
| GovUK-MCP | REFERENCE ONLY | Useful catalogue of UK-service/API ideas. Do not copy/vendor code because the repository currently exposes no LICENSE file and describes itself as a hobby/demo project. |
| uk-ons-mcp-server | EXPERIMENT CANDIDATE | Useful reference for ONS dataset discovery. Prefer a narrow direct, allowlisted, read-only official ONS adapter behind SovereignToolExecutor. |
| MCP 2026-07-28 | ADOPT COMPATIBILITY REQUIREMENTS | Future MCP transport should assume stateless requests, header-based method/tool routing and the new extension/authorization model. |

## What was verified

### LiteLLM

Repository: https://github.com/BerriAI/litellm

Current repository metadata showed roughly 58k GitHub stars at review time and active development. Its root LICENSE states that content outside `enterprise/` is MIT, while `enterprise/` is governed by its own license.

**KUBERA rule:** use LiteLLM only as an optional provider gateway or compatibility target. The Model Router remains KUBERA-owned. Model choice, authority, privacy, Evidence Ledger and human approval must not be delegated to LiteLLM.

Useful ideas:

- one provider-neutral request surface;
- model groups rather than hard-coded provider names;
- fallback chains;
- provider budgets and rate limits;
- consistent observability around provider calls.

Existing `ProviderSeriesBudget` remains authoritative for the reference runtime until a real gateway adapter is introduced.

### Presidio

Repository: https://github.com/data-privacy-stack/presidio

MIT licensed and actively maintained. Presidio handles deeper PII detection/anonymization than KUBERA's built-in credential scanner.

This change adds a provider-neutral `TextRedactor` seam to `PrivacyGate` and an optional `PresidioTextRedactor` adapter. Presidio is imported lazily only if the adapter is instantiated without injected engines.

Example integration in an environment where Presidio packages are available:

```python
from kubera_innovation import PrivacyGate, PresidioTextRedactor

redactor = PresidioTextRedactor(language="en")
result = PrivacyGate.sanitize(payload, text_redactor=redactor)
```

If the external redactor fails or returns an invalid value, the privacy boundary fails closed.

### Governance engines

Reference list: https://github.com/systempromptio/awesome-ai-agent-governance

OPA: https://github.com/open-policy-agent/opa

OPA is a mature general-purpose policy engine and is Apache-2.0 licensed. Casbin is another strong policy/RBAC option. Neither should be inserted merely because it exists.

KUBERA already has:

- WorkContract scope;
- GovernanceGate;
- AuthorizationGrant;
- Source / Evidence / Action gates;
- SovereignToolExecutor;
- EvidenceLedger;
- idempotency and action logging.

Adding another policy authority now would create two sources of truth. Reconsider OPA/Casbin only when policy must be administered independently across multiple runtimes/services.

### civic-ai-tools

Repository: https://github.com/npstorey/civic-ai-tools

MIT licensed. Its strongest fit for KUBERA is the evidence-package pattern rather than the US/Socrata-specific data stack.

KUBERA now exposes `EvidenceLedger.export_package(run_id)`. The package contains hashes and ledger metadata but deliberately omits raw input/output payloads. `verify_package()` checks the included entry envelopes and package manifest. Full ledger-chain integrity still uses `verify_chain()`.

This keeps the distinction clear:

```text
EvidencePackage = portable evidence manifest
EvidenceLedger  = canonical local audit chain
```

### GovUK-MCP

Repository: https://github.com/Stealth-Labs-LTD/GovUK-MCP

The README is useful as a catalogue of UK APIs and tools, but the repository currently has no detected license and no root `LICENSE` file. It also describes itself as a hobby/demo project.

**Decision:** no copying, vendoring or production dependency. We may independently implement integrations against official upstream APIs after validating each upstream's terms, authentication, freshness and reliability.

### ONS MCP server

Repository: https://github.com/dwain-barnes/uk-ons-mcp-server

MIT licensed. It accesses the ONS beta API and is useful as a compact reference for dataset/dimension discovery.

**Preferred KUBERA design:** direct official ONS read-only adapter rather than chaining through an untrusted third-party server. Any future adapter must be allowlisted, timeout-bound, size-limited, provenance-recorded and called through `SovereignToolExecutor`.

## MCP 2026-07-28 impact

Official release notes: https://blog.modelcontextprotocol.io/posts/2026-07-28/

The new MCP core is stateless. Requests are self-describing; method/tool information can travel in `Mcp-Method` and `Mcp-Name` headers; list responses can be cached; authorization was hardened; and extensions now include Enterprise Managed Authorization (EMA).

KUBERA should therefore keep future MCP support behind a transport boundary:

```text
Agent / workflow
    ↓
KUBERA policy + privacy + evidence
    ↓
SovereignToolExecutor
    ↓
MCP transport adapter
    ↓
allowlisted MCP server / official API
```

MCP authorization does **not** replace KUBERA human approval. EMA can constrain enterprise identity/permissions; KUBERA still decides whether the specific consequential action is authorized by the human for the finalized request.

## What this change does not claim

- no live council integration;
- no autonomous posting or submission;
- no live LiteLLM deployment;
- no Presidio package bundled into the core runtime;
- no OPA/Casbin policy server;
- no GovUK-MCP dependency;
- no production ONS connector;
- no claim that MCP 2026 transport is already implemented.

## Next safe implementation order

1. Keep the new Presidio seam optional and fail-closed.
2. Use EvidencePackage in demos / evidence handoffs where a portable proof manifest helps.
3. If a real multi-model deployment is required, add one LiteLLM-compatible gateway adapter behind the existing KUBERA router contract; never move KUBERA authority into the gateway.
4. Add one narrow read-only official-source adapter first (ONS is a candidate), with strict host allowlisting, HTTPS, timeout, response-size/content-type checks and EvidenceLedger provenance.
5. Only then add an MCP transport adapter conforming to the 2026-07-28 stateless model.
