# Human Authority Budget

**Status:** `PROTOTYPE`  
**Layer:** Governance / Permissions

## Purpose
Extend `READ / CREATE / ACT / ADMIN` with explicit temporary limits so an agent cannot keep acting indefinitely after one approval.

## Prototype implementation
The v0.1 runtime implements control levels, capability allowlists, consumable counts and timezone-aware expiry. Missing capabilities, exhausted limits, expired grants and insufficient levels fail closed.

A `GovernanceGate` combines this budget with Personal AI Constitution rules so a constitutional denial cannot consume or bypass authority.

➡️ [Open the reference implementation](../reference-implementation/)

## Example grant
```yaml
level: ACT
expires_in: 2h
limits:
  file_writes: 10
  file_deletes: 0
  github_pull_requests: 1
  purchases: 0
```

## Safety
`ADMIN` is not interpreted as unlimited authority. A capability still needs to be explicitly granted and high-risk classes can remain approval-gated.

## Next prototype step
Add tamper-evident audit entries for grant creation and every budget consumption event.
