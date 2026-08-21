# Personal AI Constitution

**Status:** `PROTOTYPE`  
**Layer:** Governance

## Purpose
Keep the owner's permanent rules separate from any replaceable model, system prompt or vendor.

## Prototype implementation
The v0.1 runtime provides deterministic policy rules with priority, action/project patterns and three outcomes: `ALLOW`, `DENY`, `REQUIRE_APPROVAL`. The default is deliberately `REQUIRE_APPROVAL`, and empty actions are denied.

A combined `GovernanceGate` evaluates the Constitution **before** spending a temporary Human Authority Budget.

➡️ [Open the reference implementation](../reference-implementation/)

## Precedence
```text
Hard safety / law
      ↓
Owner constitution
      ↓
Project policy
      ↓
Skill permissions
      ↓
Task instruction
```

## Key property
A new model does not automatically inherit trust. It must operate under the same constitution and permission system.

## Next prototype step
Add a versioned external YAML policy format with schema validation and signed policy snapshots.
