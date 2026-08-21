# Integration Contract

The reference implementation is intentionally model-agnostic.

A private agent runtime can integrate it through six narrow contracts:

1. **Constitution** — evaluate a proposed action before execution.
2. **Authority Budget** — consume temporary permission for side effects.
3. **Reality Graph** — store structured project/reality relations with visibility.
4. **Failure Vaccine** — run preventive checks before known risky operations.
5. **Reputation Engine** — record only verified outcomes and query scores.
6. **Proof of Work** — render a public engineering evidence chain.

Recommended execution order:

```text
Task
 ↓
Constitution
 ↓
Authority Budget
 ↓
Failure Vaccine
 ↓
Tool execution
 ↓
Verification
 ↓
Reputation event
 ↓
Reality / evidence update
 ↓
Proof of Work
```

The public package should never need access to private model prompts or credentials to provide these contracts.
