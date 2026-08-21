# External Intelligence Node

**Status:** `PROTOTYPE CONTRACT — HARDENED v2`  
**Purpose:** provider-independent specialist intelligence for KUBERA Agent Society

## Core principle
External AI providers are **stateless specialist workers**. KUBERA owns project memory, evidence, permissions and final decisions.

Claude is the first intended external specialist, but the contract is provider-independent.

## Ten specialist roles

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

## Hard privacy boundary

### PUBLIC
May be sent externally when the role allows it.

### PROJECT
May be sent externally **only** when:
- the role ceiling allows `PROJECT`;
- explicit sharing authorization is present;
- the content has been reduced to the minimum required review packet;
- redaction/secret scanning has completed successfully;
- disclosure metadata is recorded.

### PRIVATE
**PRIVATE context must never leave the KUBERA private boundary.** `share_authorized=true` does not override this rule.

If an external reviewer needs information derived from private code, KUBERA must first create a separate sanitized `PROJECT` review packet containing only the minimum material required for the task. Obfuscation alone is not considered a privacy boundary.

## Role classification ceilings

| Role | Maximum external context |
| --- | --- |
| Open-Source Scout | PUBLIC |
| Documentation Reviewer | PUBLIC |
| Visual Architecture Agent | PROJECT |
| Research Challenger | PROJECT |
| Specification Engineer | PROJECT |
| Test Designer | PROJECT |
| Architecture Critic | PROJECT |
| Independent Auditor | PROJECT |
| Red Team | PROJECT |
| Critic / Verifier | PROJECT |

The request may declare a stricter ceiling, but never a broader one than the role policy.

## Provider adapter: minimum architecture

### 1. Pre-Gate
Before a prompt exists:
- validate request contract/version;
- enforce role classification ceiling;
- reject all `PRIVATE` external context;
- run secret/DLP scan;
- create/verify `context_hash` from the exact text to be sent;
- record `redacted_fields`;
- enforce timeout/token budget;
- verify Human Authority Budget / provider permission.

### 2. Invocation
- map role to a fixed role-specific system instruction;
- pass constraints explicitly;
- request structured output against the response contract/tool schema;
- use a dedicated provider credential;
- do not expose unrelated repository content.

### 3. Post-Gate
- validate response structure;
- distinguish task verdict from provider/transport failure;
- record provider/model/model version/latency;
- bind response to `request_id` and `context_hash`;
- append disclosure/result metadata to Evidence Ledger;
- return only validated structured output to the Orchestrator.

## Review packet strategy

When source material originates from private code, KUBERA should build a sanitized `PROJECT` packet using one or more of these methods:

1. **Symbol-targeted extraction** — selected function/class/module plus signatures of directly relevant dependencies.
2. **PR/diff packet** — changed lines plus bounded surrounding context for Test Designer / Architecture Critic / Auditor roles.
3. **Interface/graph packet** — interfaces, types, call graph or architecture summary when source bodies are unnecessary.
4. **Redacted excerpts** — secrets, credentials, identifiers and irrelevant private data removed before external transmission.

The packet must be hashed after redaction. The hash represents the exact context that was approved for external review.

## Request contract — example

```json
{
  "contract_version": "2.0",
  "request_id": "9bb19e1e-7f5a-4d4e-a450-72f28f28ecce",
  "timestamp": "2026-08-21T15:40:00Z",
  "role": "architecture_critic",
  "target": "human_authority_budget",
  "provider": "claude",
  "max_role_classification": "PROJECT",
  "timeout_seconds": 60,
  "budget_tokens": 6000,
  "context": {
    "classification": "PROJECT",
    "share_authorized": true,
    "summary": "Sanitized review packet",
    "context_hash": "sha256:...",
    "redacted_fields": ["api_key", "email"]
  },
  "constraints": ["do_not_modify_code"]
}
```

## Response contract — example

```json
{
  "contract_version": "2.0",
  "request_id": "9bb19e1e-7f5a-4d4e-a450-72f28f28ecce",
  "execution_status": "completed",
  "verdict": "needs_changes",
  "summary": "Two architecture gaps found.",
  "provider": "anthropic",
  "model": "claude",
  "model_version": "provider-reported-version",
  "latency_ms": 1840,
  "findings": [
    {
      "severity": "high",
      "confidence": 0.91,
      "title": "Capability alias may bypass a deny rule",
      "evidence": "...",
      "suggested_fix": "Normalize capability names before policy evaluation."
    }
  ],
  "unresolved_risks": [],
  "provider_error": null
}
```

## Failure semantics

`verdict` describes the **substance of the review**. `execution_status` describes whether the provider invocation itself completed correctly.

Examples:
- `execution_status=completed`, `verdict=needs_changes` → valid review found problems.
- `execution_status=provider_error`, `verdict=null` → external service failed; no review verdict exists.
- `execution_status=schema_validation_failed`, `verdict=null` → provider returned unusable structured output.
- `execution_status=blocked`, `verdict=null` → KUBERA pre/post gate blocked the operation.

## Current implementation boundary
The public reference code validates contract mechanics and hard privacy rules. It still does **not** call Claude or any external provider and is not a production DLP engine. A future provider adapter must implement real secret scanning, exact payload hashing, API authentication, retry policy, tool/structured output enforcement, logging and Evidence Ledger persistence.
