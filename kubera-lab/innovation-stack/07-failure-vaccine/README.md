# Failure Vaccine

**Status:** `CONCEPT`  
**Layer:** Learning / Reliability

## Purpose
Turn an important failure into a reusable preventive mechanism.

## Flow
```text
Failure → root cause → severity → prevention rule → automated check/test → future gate
```

## Vaccine record
`failure_id`, `trigger`, `root_cause`, `severity`, `affected_scope`, `prevention`, `test`, `override_level`, `evidence`.

## Example
A deployment fails because the wrong branch was used. The vaccine becomes a pre-deploy assertion that verifies the branch before future releases.

## Critical rule
A vaccine should block only the failure it can identify with reasonable confidence. Broad vague rules can create new failures.

## Integrations
Failure Memory, Human Control Levels, GitHub Guardian, CI, Agent Reputation Engine.

## MVP
Automatically generate a regression test template from selected Failure Memory entries.
