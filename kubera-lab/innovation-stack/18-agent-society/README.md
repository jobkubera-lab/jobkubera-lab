# KUBERA Agent Society

**Status:** `CONCEPT`  
**Layer:** Multi-Agent Reasoning

## Purpose
Use multiple narrowly defined agents that challenge, build, audit and verify one another instead of making one model responsible for every role.

## Core roles
- **Researcher** — gathers evidence.
- **Builder** — creates the artifact or code.
- **Critic** — searches for weaknesses and contradictions.
- **Privacy Officer** — checks disclosure and data boundaries.
- **Verifier** — validates tests, links and final state.

## External Intelligence Node — prototype contract

KUBERA now defines an executable provider-independent contract for using an external model such as Claude as a specialist node rather than a second general-purpose builder.

The contract supports 10 specialist roles:

1. `independent_auditor`
2. `red_team`
3. `architecture_critic`
4. `test_designer`
5. `specification_engineer`
6. `visual_architecture_agent`
7. `research_challenger`
8. `open_source_scout`
9. `documentation_reviewer`
10. `critic_verifier`

See [External Intelligence Node](EXTERNAL_INTELLIGENCE_NODE.md), the [JSON contract](external-intelligence-contract.schema.json), and the executable Python reference implementation.

## Coordination

```text
KUBERA Orchestrator
        ↓
Context / Privacy Gate
        ↓
┌──────────────┬───────────────┬──────────────┐
│ ChatGPT      │ External Node │ Local AI     │
│ Builder      │ Critic/Audit  │ Private Work │
└──────────────┴───────────────┴──────────────┘
        ↓ structured results
Evidence Ledger
        ↓
Self-Check
        ↓
Human decision
```

The Orchestrator owns the memory and sends only the context required for the current task. External providers do not become the system of record.

## Anti-pattern
Multiple agents repeating the same answer is not a society. Roles need different objectives, tools, context or evaluation criteria.

## Integrations
Orchestrator, Agent Reputation Engine, Personal AI Constitution, Self-Check Agent, Evidence Ledger, Human Authority Budget, Public / Private Twin, Visual Systems.

## Next implementation step
Build the first deterministic pipeline:

`Builder → External Critic → Verifier → Evidence Ledger`

A real provider adapter will be added separately so Claude, another cloud model, or a future local model can implement the same contract without changing the Orchestrator interface.
