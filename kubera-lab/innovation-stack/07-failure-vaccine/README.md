# Failure Vaccine

**Status:** `PROTOTYPE`  
**Layer:** Learning / Reliability

## Purpose
Turn an important validated failure into a reusable preventive mechanism.

## Prototype implementation
The v0.1 runtime stores explicit preventive rules in SQLite. Rules support `exact`, `contains` and `regex` triggers with `WARN` or `BLOCK` actions. Blocking rules are never invented automatically; they must be deliberately registered. The module can also generate a regression-test template for a known failure rule.

➡️ [Open the reference implementation](../reference-implementation/)

## Flow
```text
Failure → root cause → severity → prevention rule → automated check/test → future gate
```

## Critical rule
A vaccine should block only a failure it can identify with reasonable confidence. Broad vague rules can create new failures.

## Integrations
Failure Memory, Human Control Levels, GitHub Guardian, CI, Agent Reputation Engine.
