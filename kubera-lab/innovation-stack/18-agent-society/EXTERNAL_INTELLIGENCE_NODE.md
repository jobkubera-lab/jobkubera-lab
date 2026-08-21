# External Intelligence Node

**Status:** `PROTOTYPE CONTRACT v3`  

KUBERA treats external AI providers as stateless specialist workers. Project memory, authority and evidence remain KUBERA-owned.

## v3 hardening

- `PRIVATE` context is structurally forbidden from external requests.
- `PROJECT` sharing requires a **signed, scoped, expiring AuthorizationGrant**, not a self-declared boolean.
- `context_hash` must equal SHA-256 of the exact context packet.
- role classification ceilings are exposed through an immutable mapping.
- safety constraints use a controlled enum; unknown directives fail closed.
- response `summary/provider/model/model_version` are mandatory non-empty metadata.
- request UUID/date-time remain validated in Python; non-Python adapters MUST enable JSON Schema format validation explicitly (for example, the equivalent of a UUID/date-time format checker).
- per-call token/time limits are complemented by an Orchestrator-level cumulative ProviderSeriesBudget.

## External sharing path

```text
Human approval
  ↓
Trusted local AuthoritySigner
  ↓ signed scoped grant
Context packet builder
  ↓ hash + redaction metadata
Role ceiling + constraint validation
  ↓
Provider Series Budget
  ↓
Provider Adapter
  ↓ structured response
Evidence Ledger
```

The HMAC signer in the public reference code is a demonstration of attestable authorization. Production should protect the signing key outside source code and can replace HMAC with asymmetric/hardware-backed signing.

## Provider adapter requirements

Before a real Claude/OpenAI/other adapter is considered production-ready it must implement: secret/DLP scanning, exact packet construction, signed grant verification, cumulative budget consumption, structured-output validation, retry/timeout policy, provider/model metadata, Evidence Ledger recording, and dedicated provider credentials.

## Runtime independence

KUBERA now also defines a small `RuntimeAdapter` protocol with `execute`, `checkpoint` and `resume`. The intention is to allow durable graph runtimes, local runtimes or provider-specific agent SDKs to sit below KUBERA governance without becoming the source of truth.

## JSON Schema note

`format: uuid` and `format: date-time` are annotations unless the chosen validator enables format assertions. Every non-Python adapter must explicitly enable equivalent format validation; schema validation without format checking is not accepted as a security boundary.
