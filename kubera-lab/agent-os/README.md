# KUBERA AGENT OS — public engineering dossier

**Priority #1 in the KUBERA portfolio.**

KUBERA AGENT OS is the orchestration and control layer for bounded AI workflows. The public reference implementation focuses on human authority, evidence, permissions, failure handling and deterministic execution boundaries rather than autonomous side effects.

## Public implementation evidence

The working reference code lives in:

- [Innovation Stack reference implementation](../innovation-stack/reference-implementation/)
- [Agent OS architecture](../../KUBERA_AGENT_OS.md)
- [MCP capability layer](../mcp-lab/)
- [Tender Intelligence capability](../tender-intelligence/)

The repository includes executable Python reference code, tests, a safe demo, an Evidence Ledger, approval gates, idempotency controls, privacy/tool validation, provider budgets and a controlled tool-execution boundary.

## Control path

```text
Task
  -> context / policy
  -> bounded capability
  -> privacy + validation
  -> source / evidence / action gates
  -> human approval when consequential
  -> idempotent tool execution
  -> action log
  -> Evidence Ledger
```

## What is implemented

- provider-neutral orchestration contracts;
- Evidence Ledger with append-only hash-chain mechanics;
- Builder -> Critic -> Verifier pipeline;
- privacy and tool validation;
- source/evidence/action gates;
- signed approval reference mechanics;
- idempotency and replay protection;
- unknown-external-state handling;
- bounded MCP capability layer;
- safe local-draft tool path;
- automated tests and source-coverage gate.

## What is deliberately not claimed

This is a public reference runtime, not a production security product. It does not claim autonomous email/posting/payment, live council authority, banking authority, arbitrary browser control or production-grade remote identity/attestation.

## Verification

The reference implementation is exercised by [GitHub Actions](../../../.github/workflows/test-innovation-stack-reference.yml) across Python 3.11, 3.12 and 3.13. The workflow also runs the safe demo and enforces an 85% source branch-coverage floor.

**Design rule:** KUBERA prepares and verifies. The human remains the authority.
