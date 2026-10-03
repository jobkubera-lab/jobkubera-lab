# Deprecated GitHub profile cleanup checklist

> **Historical maintenance record — do not use as a current task list.**

This checklist described an earlier cleanup state. The manual actions it listed for repository About text, Topics and the `kubera-learning.` rename have already been completed, so those instructions are intentionally retired.

## Current maintenance sources

Use the maintained portfolio documents instead:

- [`../README.md`](../README.md) — public profile and entry points;
- [`../STATUS.md`](../STATUS.md) — current priorities and project state;
- [`../REPO_MAP.md`](../REPO_MAP.md) — repository navigation;
- [`../PORTFOLIO_MAP.md`](../PORTFOLIO_MAP.md) — portfolio hierarchy and maturity labels;
- [`../EVIDENCE_MATRIX.md`](../EVIDENCE_MATRIX.md) — verified evidence and boundaries;
- [`../tools/portfolio_audit.py`](../tools/portfolio_audit.py) — automated evidence guardrail.

## Cleanup rules that still apply

- Do not delete or archive repositories/files as part of the current cleanup.
- Do not modify `kubera-lab/kubera-guide-global-mapping/`.
- Do not add secrets, tokens or credentials.
- Use repository-specific pull requests for file changes.
- Preserve upstream authorship and licensing.
- Do not weaken CI or merge changes with failing checks.

Repository settings and current pull-request state should be verified from GitHub directly rather than from this historical checklist.