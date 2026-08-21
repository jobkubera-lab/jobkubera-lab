# KUBERA GitHub Guardian

**Status:** `CONCEPT`  
**Layer:** Delivery / Maintenance

## Purpose
Continuously inspect approved repositories for maintainability and safety problems, then report or propose fixes through normal GitHub workflows.

## Checks
- failed or stale GitHub Actions;
- broken public links;
- accidental credentials / secret patterns;
- missing or outdated README sections;
- abandoned branches;
- duplicate project directories;
- third-party license notices;
- tests missing for executable modules;
- dependency and configuration drift.

## Operating rule
Default mode is **report-only**. Fixes should be proposed in a branch/PR unless explicit authority allows more.

## Output
Health score, findings, severity, evidence and suggested PR plan.

## Integrations
GitHub Actions, Failure Vaccine, Public/Private Twin, Living README, Human Authority Budget.
