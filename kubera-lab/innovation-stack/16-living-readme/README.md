# Living README

**Status:** `CONCEPT`  
**Layer:** Delivery / Documentation

## Purpose
Keep selected README sections synchronized with verified project state instead of manually editing metrics and statuses everywhere.

## Dynamic blocks
- latest release / version;
- test status;
- active milestone;
- recent meaningful PRs;
- project metrics from approved sources;
- generated architecture summary;
- public roadmap status.

## Design
Only content between explicit markers should be machine-managed. Human-written narrative remains untouched.

## Safety
Never pull private data into a public README. All generated content must pass Public/Private Twin rules.

## Integrations
GitHub Actions, Proof-of-Work Portfolio, GitHub Guardian, Public/Private Twin.

## MVP
A GitHub Action that updates one bounded status block from a local public `status.json` file and opens a PR instead of writing directly to `main`.
