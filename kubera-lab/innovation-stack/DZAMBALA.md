# DZAMBALA

**KUBERA sovereign agent architecture — long-horizon engineering direction**

DZAMBALA is the strategic layer for KUBERA. It separates what already exists in modern agent frameworks from the parts KUBERA should own and improve. It is not a claim that future capabilities already exist.

## What the industry already does well

### Durable, stateful execution
LangGraph documents durable execution, persistence, memory and human-in-the-loop interrupts for long-running stateful agents. KUBERA should not reimplement a weaker workflow engine merely to own one.

### Structured multi-agent graphs
AutoGen supports teams and graph-controlled multi-agent workflows, including directed flows and critic/reflection patterns. KUBERA should treat multi-agent routing as replaceable runtime infrastructure.

### Handoffs, guardrails, sessions and traces
OpenAI Agents SDK provides specialized-agent handoffs, guardrails, session context and tracing across model/tool/handoff activity. KUBERA should be able to sit above such runtimes rather than depend on one provider.

### Open tool interoperability
Model Context Protocol (MCP) standardizes how AI applications connect to tools and external context. KUBERA should use protocol adapters where useful instead of inventing a proprietary connector format for every tool.

### Durable workflow principles
Long-running workflow systems such as Temporal demonstrate the value of deterministic workflow state, retries, resumability and separation between orchestration state and side-effecting activities. KUBERA borrows these principles without embedding a heavy workflow dependency in the public reference core.

## DZAMBALA thesis

KUBERA should be the **sovereign layer above replaceable models, providers, tools and runtimes**.

```text
Human Owner
    ↓
Constitution + Identity + Signed Authority Grants
    ↓
Intent / Project Compiler
    ↓
Context Firewall + Provenance + Redaction
    ↓
Persistent Project Workspace + Handoff Artifacts
    ↓
Runtime Adapter Layer
    ├─ local runtime
    ├─ provider agent runtime
    ├─ graph runtime
    └─ future provider/runtime
    ↓
Capability Supply Chain / MCP-style tool adapters
    ↓
Source Gate → Evidence Gate → Action Gate
    ↓
Reversibility + Idempotency Control
    ↓
Execution / checkpoint / resume
    ↓
Action Log + Evidence Ledger + hash chain
    ↓
Independent Critic / Verifier
    ↓
Outcome Reputation + Failure Vaccine
    ↓
Human decision and control
```

## Operational trust layer — implemented in reference v0.9

The following mechanics are now executable reference components rather than architecture-only notes.

### Persistent handoff contract
Agent-to-agent work must not depend on remembered chat context. `HandoffArtifact` carries the task ID, previous owner, next owner, objective, status, output summary, source references, evidence references and exact next action. It can be rendered as a `HANDOFF.md` artifact and has a SHA-256 identity.

Recommended workspace convention for future durable runtimes:

```text
/workspace/tasks/
/workspace/handoffs/
/workspace/evidence/
/workspace/reviews/
/workspace/approved/
/workspace/archive/
```

This directory layout is an architectural convention; the public runtime does not yet claim a distributed persistent workspace manager.

### Three gates before consequential actions

```text
SOURCE GATE → EVIDENCE GATE → ACTION GATE
```

- **Source Gate:** a consequential action must be based on a currently verified authoritative source.
- **Evidence Gate:** the evidence required for the decision must be present and verified.
- **Action Gate:** owner policy, reversibility and signed authorization determine whether execution is allowed.

Any failed source/evidence gate stops the action. Unknown or missing proof fails closed.

### Reversibility boundary

DZAMBALA distinguishes preparation from external side effects.

**Reversible:** research, analyse, draft, summarize, compare, prepare, verify, queue.

**Irreversible / consequential:** publish, send, buy, delete, sign, accept terms, change an external account or execute an equivalent real-world side effect.

An irreversible action requires signed approval even when a broad policy says `ALLOW`. In other words, **approval wins over convenience**.

### Exact-action approval

The action gate binds approval to the action fingerprint:

`operation + target + exact request hash`

A grant for one payload cannot authorize a modified payload. The existing signed-grant mechanism remains a reference HMAC design; production identity and key protection require stronger deployment controls.

### Idempotent retries

Every side-effecting action should carry an idempotency key. `IdempotencyStore` reserves that key before execution:

- same key + same request → replay, do not repeat the side effect;
- same key + different request → conflict, stop;
- new key → eligible for first execution after all other gates pass.

This protects retries after partial failures from double-sending, double-publishing or repeating an equivalent external action.

### Action log uses the Evidence Ledger

DZAMBALA does not create a competing audit database for operations. `ActionLogger` records action ID, actor, operation, target, reversibility, status, source/evidence references, idempotency key and approval-grant reference into the existing hash-chained Evidence Ledger.

## Engineering principles adopted now

1. **Models are replaceable.** KUBERA memory, permissions, evidence and policy cannot belong to a model vendor.
2. **PRIVATE never leaves the sovereign boundary.** External providers only receive PUBLIC or explicitly granted sanitized PROJECT packets.
3. **Human approval must be attestable.** A boolean set by calling code is not proof of consent; external sharing and consequential actions use signed, scoped, expiring grants.
4. **Context identity must be cryptographically tied to content.** A declared hash must equal the exact context packet being sent.
5. **Policy tables are immutable at runtime.** Role ceilings cannot be silently widened by another imported module.
6. **Constraints are machine vocabulary, not arbitrary prose.** Unknown safety directives fail closed.
7. **Budgets are cumulative.** Per-call token/time limits are necessary but insufficient; the Orchestrator also limits call count, total tokens, total cost/risk and expiry across a run.
8. **Execution is resumable and idempotent.** Runtime adapters expose checkpoint identity and explicit resume semantics; retries must not duplicate side effects.
9. **Handoffs are artifacts, not chat memory.** The next worker receives explicit sources, evidence, status and next action.
10. **Source truth is reopened before consequential action.** Cached memory is not sufficient for values or states that may have changed.
11. **Reversibility controls autonomy.** Reversible preparation can be automated more freely; irreversible effects require stricter authority.
12. **Evidence precedes reputation.** Agent/model reputation changes only from verified outcomes with evidence references.
13. **Capabilities enter through a supply chain.** Discover → license → security → permission scope → sandbox → tests → adoption.
14. **Interoperability beats lock-in.** MCP/tool protocols and runtime adapters are preferred over hard-wiring business logic to one provider.
15. **Prefer event-driven triggers to wasteful polling where the upstream system supports events/webhooks.**
16. **Notify by exception.** Routine successful work should not flood the human owner; escalation is for approval, failure, meaningful state change or threshold crossing.
17. **Every futuristic claim must become a deterministic tested component before it is called implemented.**

## 2040 research hypotheses

Learning and reference material selected for the architecture is maintained in [`LEARNING_RESOURCES.md`](./LEARNING_RESOURCES.md).

### Sovereign Agent Kernel
A portable governance/memory/evidence kernel capable of running above several agent runtimes and model providers.

### Verifiable Agent History
Consequential work produces cryptographically linked evidence records and, later, optional signed checkpoints/external timestamping.

### Context Firewall
The system constructs minimum-purpose review packets rather than exporting whole repositories or conversations.

### Capability Market with Trust
Tools, skills and models carry permission profiles, provenance, test history, security status and outcome reputation before being eligible for autonomous use.

### Failure-to-Policy Evolution
Verified failures generate regression tests, prevention rules, routing penalties or stricter authority constraints.

### Model Competition
Several providers can independently review the same evidence packet. Later verified outcomes update routing reputation rather than relying on vendor preference.

### Permission Economics
Authority becomes a consumable resource across time, actions, token/cost budgets and risk classes.

## Near-term target

DZAMBALA is successful only if the public reference runtime can prove these mechanics in small tests:

`Handoff → Source Gate → Evidence Gate → Signed Action Grant → Idempotency Reserve → Execution → Action Log → Evidence Ledger → Verified Result`

The next production slice should connect these controls to one fake/injected tool executor first, then to a real provider/tool adapter only after tests prove that no external side effect can bypass source, evidence, authority and idempotency checks.

## Current references

- LangGraph documentation: https://docs.langchain.com/oss/python/langgraph/durable-execution
- AutoGen documentation: https://microsoft.github.io/autogen/stable/
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- Model Context Protocol: https://modelcontextprotocol.io/
- Temporal durable execution concepts: https://docs.temporal.io/

These projects remain independent upstream systems; DZAMBALA is KUBERA's integration/governance direction, not a fork or ownership claim.

The operational principles added in v0.9 were also informed by user-supplied field notes about multi-agent operations. Their external attribution was not required for implementation and is not presented here as a verified upstream specification.
