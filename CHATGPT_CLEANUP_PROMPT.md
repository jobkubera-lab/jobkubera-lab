# Deprecated GitHub cleanup prompt

> **Historical maintenance artifact — do not execute.**

This file is retained because the repository cleanup policy currently prohibits deleting files. Its original instructions described an earlier cleanup state and are now obsolete.

## Why it is deprecated

The old prompt referenced superseded pull requests, stale repository names and public-reach claims that are intentionally excluded from the current evidence policy. It also contained instructions that conflict with the current repository-maintenance constraints.

Do **not** use this file as an operational task list and do **not** restore historical metrics or bypass portfolio evidence checks from its old instructions.

## Current sources of truth

Use these maintained files instead:

- [`README.md`](README.md) — public profile and project entry points;
- [`STATUS.md`](STATUS.md) — current project status and priorities;
- [`REPO_MAP.md`](REPO_MAP.md) — repository navigation;
- [`PORTFOLIO_MAP.md`](PORTFOLIO_MAP.md) — portfolio hierarchy and maturity labels;
- [`EVIDENCE_MATRIX.md`](EVIDENCE_MATRIX.md) — verified evidence and public/private boundaries;
- [`tools/portfolio_audit.py`](tools/portfolio_audit.py) — automated evidence guardrail.

## Standing maintenance constraints

- Do not delete or archive repositories/files as part of the current cleanup.
- Do not modify `kubera-lab/kubera-guide-global-mapping/`.
- Do not add secrets, tokens or credentials.
- File changes should go through repository-specific pull requests.
- Do not weaken or disable CI to obtain a green result.
- Do not merge changes with failing checks.
- Preserve upstream authorship, licensing and reference attribution.

This notice supersedes all operational instructions that previously existed in this file.