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
Runtime Adapter Layer
    ├─ local runtime
    ├─ OpenAI-style agent runtime
    ├─ graph runtime
    └─ future provider/runtime
    ↓
Capability Supply Chain / MCP-style tool adapters
    ↓
Authority + cumulative cost/risk budgets
    ↓
Execution / checkpoint / resume
    ↓
Evidence Ledger + hash chain
    ↓
Independent Critic / Verifier
    ↓
Outcome Reputation + Failure Vaccine
    ↓
Human decision and control
```

## Engineering principles adopted now

1. **Models are replaceable.** KUBERA memory, permissions, evidence and policy cannot belong to a model vendor.
2. **PRIVATE never leaves the sovereign boundary.** External providers only receive PUBLIC or explicitly granted sanitized PROJECT packets.
3. **Human approval must be attestable.** A boolean set by calling code is not proof of consent; external sharing uses signed, scoped, expiring grants.
4. **Context identity must be cryptographically tied to content.** A declared hash must equal the exact context packet being sent.
5. **Policy tables are immutable at runtime.** Role ceilings cannot be silently widened by another imported module.
6. **Constraints are machine vocabulary, not arbitrary prose.** Unknown safety directives fail closed.
7. **Budgets are cumulative.** Per-call token/time limits are necessary but insufficient; the Orchestrator also limits call count, total tokens, total cost/risk and expiry across a run.
8. **Execution is resumable.** Runtime adapters expose checkpoint identity and explicit resume semantics rather than hiding state inside a provider chat.
9. **Evidence precedes reputation.** Agent/model reputation changes only from verified outcomes with evidence references.
10. **Capabilities enter through a supply chain.** Discover → license → security → permission scope → sandbox → tests → adoption.
11. **Interoperability beats lock-in.** MCP/tool protocols and runtime adapters are preferred over hard-wiring business logic to one provider.
12. **Every futuristic claim must become a deterministic tested component before it is called implemented.**

## 2040 research hypotheses

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

`Signed Grant → Context Gate → Runtime Adapter → Builder/Critic/Verifier → Checkpoint → Evidence Ledger → Verified Result`

The next production step is a real provider adapter, but only after secret scanning, structured-output validation, authority verification and cumulative budgets are enforced.

## Current references

- LangGraph documentation: https://docs.langchain.com/oss/python/langgraph/durable-execution
- AutoGen documentation: https://microsoft.github.io/autogen/stable/
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- Model Context Protocol: https://modelcontextprotocol.io/
- Temporal durable execution concepts: https://docs.temporal.io/

These projects remain independent upstream systems; DZAMBALA is KUBERA's integration/governance direction, not a fork or ownership claim.
