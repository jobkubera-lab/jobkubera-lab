# Security Boundary

The public reference implementation demonstrates policy and audit mechanics. It is **not** a production security sandbox.

## Deliberately absent

- shell execution;
- browser/account automation;
- cloud credentials;
- secret storage;
- financial actions;
- system administration;
- autonomous GitHub writes.

## Fail-closed principles

- Constitution defaults to `REQUIRE_APPROVAL`.
- Authority capabilities not explicitly granted are denied.
- Expired or exhausted budgets are denied.
- Public Reality Graph export includes only `PUBLIC` nodes and edges between public nodes.
- Failure Vaccine blocking rules must be explicitly registered.
- Reputation ignores unverified events.
- Proof-of-Work distinguishes verified from unverified evidence.

A production integration should add authentication, secure secret storage, tamper-evident audit records, sandboxing, rate limits and tested tool adapters.
