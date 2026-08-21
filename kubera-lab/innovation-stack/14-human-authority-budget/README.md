# Human Authority Budget

**Status:** `CONCEPT`  
**Layer:** Governance / Permissions

## Purpose
Extend `READ / CREATE / ACT / ADMIN` with explicit temporary limits so an agent cannot keep acting indefinitely after one approval.

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

## Enforcement
Every side-effecting tool call spends from the relevant budget. Expiry or exhaustion returns control to the human.

## Safety
ADMIN should still not mean unlimited authority. High-risk classes can remain permanently approval-gated.

## Integrations
Human Control Levels, Personal AI Constitution, Tool Executor, Evidence Ledger, Failure Vaccine.

## MVP
A local permission object checked before every mutating tool call, with immutable audit entries for grants and consumption.
