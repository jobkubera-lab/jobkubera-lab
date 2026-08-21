# DZAMBALA — Claude Engineering Task

This file is not a conversation log. It contains only the current engineering task for Claude as an external auditor/critic.

## Current task
Harden the existing `authorization_grant.py` mechanism. Do not redesign unrelated DZAMBALA modules.

## Files to read first
- `reference-implementation/src/kubera_innovation/authorization_grant.py`
- `reference-implementation/src/kubera_innovation/external_intelligence.py`
- `reference-implementation/tests/test_authorization_grant.py`
- `reference-implementation/tests/test_external_intelligence.py`

## What to verify
1. A grant must approve the exact outbound context packet, not only a free-text target.
2. A grant must be bound to the intended external role/purpose.
3. A grant must not be replayable indefinitely; propose the smallest safe single-use or idempotent-consumption mechanism.
4. Existing rule remains: `PRIVATE` never leaves the sovereign boundary.
5. Keep the design minimal: no new external dependencies unless absolutely necessary.

## Required response from Claude
Return only:
- concrete weaknesses still present in these files;
- exact field/API changes you recommend;
- minimal pseudocode for `issue`, `verify`, and `consume`;
- exactly 5 mandatory tests;
- breaking changes, if any.

Do not review Model Router, Skill DNA, Plugin Registry, Evidence Ledger, Runtime Adapter, or future roadmap in this task.

## Done condition
ChatGPT will implement only after the owner approves the proposed change. The change is considered done only after code, tests, and CI pass.
