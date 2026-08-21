# Decision Replay

**Status:** `CONCEPT`  
**Layer:** Learning / Audit

## Purpose
Answer a future question such as: **Why did this project choose this design?**

## Replay packet
- original goal;
- alternatives considered;
- evidence available at the time;
- constraints;
- selected option;
- commit / PR references;
- later outcome;
- failures or corrections that changed the decision.

## Important property
Replay is historical, not revisionist. New knowledge must be shown as a later event rather than rewriting what was known at the original decision time.

## Output
A chronological human-readable decision timeline plus machine-readable records.

## Integrations
Evidence Ledger, Git history, Reality Graph, Failure Vaccine, Proof-of-Work Portfolio.

## MVP
Generate a `decision-replay.md` from structured Evidence Ledger records and Git references.
