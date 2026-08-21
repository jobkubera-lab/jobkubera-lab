# First Deterministic Agent Pipeline

**Status:** `PROTOTYPE`  
**Implemented:** public reference implementation v0.6

## What now actually runs

KUBERA has a real deterministic control loop:

```text
Request
  ↓
Builder callable
  ↓
Critic callable
  ↓
Verifier callable
  ↓
Evidence Ledger
  ↓
PASS / NEEDS_CHANGES / BLOCKED
```

The stages are ordinary Python callables. This is intentional: the orchestration can be tested before any LLM provider is connected.

## Evidence Ledger

Every stage records:

- `run_id`
- stage name
- UTC timestamp
- SHA-256 hash of stage input
- SHA-256 hash of stage output
- previous ledger-entry hash
- current ledger-entry hash
- structured metadata

Entries are stored in SQLite and linked as a hash chain. This provides tamper-evidence within the reference database but is **not** a digital-signature or production immutability guarantee.

## Deterministic behavior

- Builder always runs first.
- Critic receives the original request plus Builder output.
- Verifier receives the request, Builder output and Critic output.
- A Critic `BLOCKED` verdict stops normal verification and records the blocked state.
- `NEEDS_CHANGES` propagates to the final verdict.
- Every stage is still written to the Evidence Ledger.

## What is deliberately not implemented yet

- Claude/OpenAI/other provider API invocation
- automatic Model Router
- Skill DNA execution engine
- production DLP or secret scanning
- durable distributed execution
- cryptographic signing of ledger checkpoints

Those remain separate engineering steps. The purpose of v0.6 is to prove the workflow mechanics without pretending the model/runtime integrations already exist.

## Next step

Introduce a provider adapter behind the Critic interface while keeping this deterministic orchestration unchanged. The adapter must use the External Intelligence v2 contract and never send `PRIVATE` context externally.
