# External Intelligence Node

**Status:** `PROTOTYPE CONTRACT`  
**Purpose:** provider-independent specialist intelligence for KUBERA Agent Society

## Why it exists
KUBERA should not depend on one model acting as builder, critic, researcher and verifier at the same time. An External Intelligence Node gives the Orchestrator a second perspective with a deliberately different role.

Claude is the first intended external specialist, but the contract is not Claude-specific. Any compatible provider can receive the same request and return the same response structure.

## Ten specialist roles

### 1. Independent Auditor
Review architecture or code for correctness, maintainability, privacy boundaries, unsafe assumptions, missing tests and documentation gaps.

### 2. Red Team
Attack the logic of KUBERA's own systems: attempt to identify ways governance, privacy, authority budgets or failure controls could be bypassed or could fail. This role is for defensive evaluation of systems the owner is authorized to test, not for operational exploitation of third-party systems.

### 3. Architecture Critic
Challenge complexity, unnecessary components, weak interfaces, hidden coupling, missing states and simpler alternatives before implementation.

### 4. Test Designer
Generate edge cases, negative tests, regression scenarios, security-oriented tests and acceptance criteria from an implementation or specification.

### 5. Specification Engineer
Convert an existing project mechanic into strict inputs, outputs, states, failure modes, API contracts and acceptance criteria.

### 6. Visual Architecture Agent
Translate architecture or workflow context into a `DiagramIntent` or critique an existing diagram plan. Rendering may be delegated to the KUBERA Visual Systems Layer.

### 7. Research Challenger
Given a conclusion and its evidence, search for contradictions, missing alternatives, stale assumptions and cheaper/simpler approaches. It is not independent if the underlying evidence is not provided.

### 8. Open-Source Scout
Find candidate libraries/projects under explicit constraints such as license, language, local-first support, maintenance state and resource requirements.

### 9. Documentation Reviewer
Ask whether an outside developer can understand, install, run, test and safely modify the project from its public documentation.

### 10. Critic / Verifier
Act as the independent challenge or validation stage inside Agent Society and return structured findings rather than silently modifying the artifact.

## Memory principle
External providers are **stateless workers from KUBERA's point of view**. The Orchestrator must send the relevant context every time. Project memory, failures, decisions and evidence stay in KUBERA-owned storage.

## Context / Privacy Gate
Before any external call:

1. classify the context as `PUBLIC`, `PROJECT` or `PRIVATE`;
2. reduce it to the minimum information required;
3. require explicit sharing authorization for `PROJECT` and `PRIVATE` context;
4. remove secrets, credentials and irrelevant personal/private data;
5. record what context was shared and why;
6. store the returned findings in the Evidence Ledger with provider/model metadata.

The public reference implementation enforces the explicit-sharing flag at the contract level. It is **not** a production DLP/security system.

## Request contract

```json
{
  "role": "architecture_critic",
  "target": "human_authority_budget",
  "provider": "claude",
  "context": {
    "classification": "PROJECT",
    "share_authorized": true,
    "summary": "Relevant architecture and code excerpt"
  },
  "constraints": [
    "do_not_modify_code",
    "focus_on_bypass_and_failure_modes"
  ]
}
```

## Response contract

```json
{
  "verdict": "needs_changes",
  "summary": "The permission model has two important gaps.",
  "findings": [
    {
      "severity": "high",
      "title": "Capability alias may bypass a deny rule",
      "evidence": "...",
      "suggested_fix": "Normalize capabilities before policy evaluation."
    }
  ],
  "unresolved_risks": []
}
```

## Provider adapter boundary
The current prototype deliberately **does not call Claude or any external API**. It validates the contract and privacy classification. A future adapter will handle authentication, API invocation, retries, model metadata, cost/latency and response validation.

This keeps the Orchestrator independent from any one external vendor.
