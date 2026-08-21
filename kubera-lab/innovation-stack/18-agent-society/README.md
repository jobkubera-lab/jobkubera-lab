# KUBERA Agent Society

**Status:** `CONCEPT`  
**Layer:** Multi-Agent Reasoning

## Purpose
Use multiple narrowly defined agents that can challenge and verify one another instead of making one model responsible for every role.

## Example roles
- **Researcher** — gathers evidence.
- **Builder** — creates the artifact or code.
- **Critic** — searches for weaknesses and contradictions.
- **Privacy Officer** — checks disclosure and data boundaries.
- **Verifier** — validates tests, links and final state.

## Coordination
The Orchestrator assigns roles, Evidence Ledger stores their claims, and a final synthesis must distinguish agreement, disagreement and unresolved uncertainty.

## Anti-pattern
Multiple agents repeating the same model answer is not a society. Roles need different objectives, tools or evaluation criteria.

## Integrations
Orchestrator, Agent Reputation Engine, Personal AI Constitution, Self-Check Agent, Evidence Ledger, Human Authority Budget.

## MVP
A deterministic 3-role pipeline: Builder → Critic → Verifier, with structured JSON handoffs and a final audit report.
