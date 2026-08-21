# Proof-of-Work Portfolio

**Status:** `PROTOTYPE`  
**Layer:** Delivery / Reputation

## Purpose
Show the engineering path behind a project instead of relying on self-description.

## Prototype implementation
The v0.1 runtime models the project evidence chain as ordered stages from `IDEA` through `RELEASE`, distinguishes verified from unverified evidence, validates stage ordering and renders a Markdown proof-of-work table.

➡️ [Open the reference implementation](../reference-implementation/)

## Evidence chain
```text
Idea → Issue → Branch → Commits → Pull Request → Tests → Merge → Demo → Release
```

## Principle
Do not manufacture activity to look busy. The portfolio should reward coherent development history and verified results.

## Integrations
GitHub Actions, Evidence Ledger, Decision Replay, Living README, Public/Private Twin.
