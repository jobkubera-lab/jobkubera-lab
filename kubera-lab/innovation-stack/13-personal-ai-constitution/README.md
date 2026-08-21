# Personal AI Constitution

**Status:** `CONCEPT`  
**Layer:** Governance

## Purpose
Keep the owner's permanent rules separate from any replaceable model, system prompt or vendor.

## Rule classes
- privacy and disclosure;
- human approval requirements;
- evidence standards;
- financial/account restrictions;
- allowed automation scope;
- destructive-action rules;
- project-specific exceptions;
- conflict resolution.

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

## Integrations
Human Authority Budget, Private/Public Gate, Orchestrator, Agent Society, Tool Executor.

## MVP
A versioned `constitution.yaml` with a validator that can answer `ALLOW`, `DENY` or `REQUIRE_APPROVAL` for a proposed action.
