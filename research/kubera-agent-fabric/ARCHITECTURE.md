# KUBERA Agent Fabric

A provider-neutral architecture for persistent, privacy-aware, multi-channel AI agents with verifiable execution.

## Core idea

KUBERA Agent Fabric is not a single chatbot. It is a controlled runtime that can coordinate many specialist agents, preserve task state across channels, attach voice or web interfaces without changing the reasoning core, and require explicit human approval for high-impact actions.

## Design principles

1. **Provider-neutral core** — Grok, Claude, OpenAI-compatible, local models or future providers sit behind one model adapter.
2. **Workflow-first orchestration** — large tasks are decomposed into phases and parallel specialist agents.
3. **Persistent task state** — sessions, checkpoints and evidence survive channel changes and process restarts.
4. **Channel independence** — X, Slack, web, Telegram, voice and future surfaces are adapters, never the source of truth.
5. **Evidence before confidence** — every material result can carry sources, tool traces and verifier decisions.
6. **Privacy by default** — raw personal data is minimized; analytics are aggregated and redacted.
7. **Least privilege** — each agent gets only the tools and scopes required for its current task.
8. **Human control gates** — publishing, payments, account changes and destructive operations require policy checks and, where configured, explicit approval.
9. **Independent verification** — important findings can be challenged by a separate verifier agent before release.
10. **Resumable execution** — workflows checkpoint after phases and can safely resume without repeating completed work.

## Architecture

```text
User / Operator
      |
      v
+---------------------------+
| Channel Adapters          |
| Web | X | Slack | Voice   |
+-------------+-------------+
              |
              v
+---------------------------+
| Identity + Policy Gateway |
| scopes / approvals / TTL  |
+-------------+-------------+
              |
              v
+---------------------------+
| Orchestrator              |
| plan -> fan-out -> verify |
| -> synthesize -> checkpoint|
+------+-----------+--------+
       |           |
       |           +--------------------+
       v                                v
+--------------+                +----------------+
| Worker Pool  |                | Verifier Pool  |
| specialist   |                | adversarial /  |
| agents       |                | evidence checks|
+------+-------+                +--------+-------+
       |                                 |
       +----------------+----------------+
                        v
                +---------------+
                | Tool Gateway  |
                | web/git/files |
                | code/db/etc.  |
                +-------+-------+
                        |
                        v
                +---------------+
                | Evidence Log  |
                | sources       |
                | actions       |
                | decisions     |
                +-------+-------+
                        |
                        v
                +---------------+
                | Memory Store  |
                | task state    |
                | checkpoints   |
                | summaries     |
                +---------------+
```

## Unique KUBERA layer: Trust Mesh

The differentiator is a **Trust Mesh** around every autonomous action. Instead of trusting a single agent response, each consequential action is represented as an `ActionIntent` containing:

- actor / agent identity;
- requested capability;
- exact target;
- evidence used;
- confidence;
- risk class;
- required approval level;
- expiration time;
- verifier decision;
- final execution receipt.

This creates a portable permission and audit object that can follow the same agent across channels and providers.

### Example

```json
{
  "intent_id": "ki_01",
  "agent": "research.news",
  "action": "publish_x_reply",
  "target": "x://post/123",
  "risk": "external_write",
  "evidence": ["source:official-release"],
  "approval": "human_required",
  "expires_in_seconds": 900,
  "verified": true
}
```

## Workflow contract

Each workflow is declared as phases rather than a free-form endless loop.

```yaml
name: technology-intelligence
budget:
  max_agents: 24
  max_minutes: 20
phases:
  - id: collect
    parallel: true
    workers: 8
  - id: verify
    parallel: true
    workers: 4
    requires: collect
  - id: synthesize
    workers: 1
    requires: verify
  - id: approval
    human_gate: true
    when: external_write
```

## Memory model

KUBERA separates four memory classes:

- **Conversation memory** — short-lived dialogue state.
- **Task memory** — durable state for an active workflow.
- **Evidence memory** — immutable references, tool outputs and verification decisions.
- **Learning memory** — distilled patterns that passed quality gates; never raw private conversations by default.

This separation prevents a persistent agent from treating every historical message as permanent authority.

## Privacy model

- credentials remain outside model-visible memory;
- aliases can be used for task-specific identities;
- raw conversation analytics are redacted/aggregated;
- action logs record what was done without storing unnecessary secrets;
- each delegated capability has scope + TTL + revocation;
- future cryptographic payment or signing adapters must remain isolated behind explicit policy gates.

## First KUBERA use case: Technology Intelligence Agent

The first production-minded workflow should monitor selected high-value sources (AI labs, agent platforms, privacy protocols, security research), then:

1. collect fresh releases;
2. discard marketing-only noise;
3. verify claims against primary sources;
4. extract architectural patterns;
5. score relevance to KUBERA;
6. generate a concise Russian brief and optional English X reply;
7. require human approval before any external post;
8. store only verified reusable insights in project memory.

## What not to copy

KUBERA should not clone Grok, Claude, Vercel, ElevenLabs, Monero or Brave. Their implementations, models and proprietary infrastructure remain theirs. We reuse public architectural lessons: fan-out orchestration, persistent sessions, replaceable channel/voice layers, privacy-first identity, evidence-based research, independent security review and controlled autonomy.

## Next implementation gate

A minimal prototype should prove five things before expanding:

- deterministic workflow state machine;
- parallel worker execution with bounded budget;
- independent verifier pass;
- approval gate for external writes;
- append-only evidence/action ledger.

No production-readiness claim should be made until these are exercised with fresh held-out tasks and failure tests.
