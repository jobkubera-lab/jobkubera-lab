# KUBERA Plugin Intelligence Registry

**Status:** `PROTOTYPE CONTRACT`  
**Purpose:** safely discover, evaluate and adopt external agent plugins/capabilities without blindly installing third-party code.

## Why this exists
The public `awesome-dsh-plugin` catalog is useful because it exposes a very large set of DeepSeek Harness plugins across memory, browser/web, voice/audio, docs/rendering, workflow/automation, Git/code review, security/permissions, remote/mobile, usage/billing and many other categories.

The catalog itself explicitly warns that installing a plugin runs third-party code with the user's permissions and may read files, use credentials or access the network. Therefore KUBERA does **not** treat “listed in an awesome list” as a security approval.

## KUBERA adoption pipeline

```text
DISCOVER
  ↓
SOURCE VERIFY
  ↓
LICENSE CHECK
  ↓
SECURITY REVIEW
  ↓
COMPATIBILITY REVIEW
  ↓
HUMAN APPROVAL
  ↓
SANDBOX TEST
  ↓
ADOPT / REJECT / WATCH
```

## Registry fields
Every candidate should record:

- upstream repository;
- source catalog;
- capability category;
- KUBERA module(s) it may strengthen;
- license state;
- code-review state;
- filesystem access expectation;
- credential access expectation;
- network access expectation;
- install/test state;
- risk level;
- adoption verdict;
- evidence / notes.

## Source catalog checked

- Catalog: `awesome-dsh-plugin/awesome-dsh-plugin`
- URL: https://github.com/awesome-dsh-plugin/awesome-dsh-plugin
- Catalog license: **CC0-1.0**
- Catalog purpose: curated list of plugins for DeepSeek Harness
- Important distinction: **individual plugin repositories may use different licenses and must be checked separately before copying or integrating code.**

## Capability map relevant to KUBERA

High-value areas from the source catalog:

1. **Memory** → Project Memory, Reality Graph, Failure Memory
2. **Browser & Web** → Research tools, acceptance tests, live information
3. **Vision & Multimodal** → image/document understanding
4. **Voice & Audio** → voice control, speech interfaces
5. **Docs & Rendering** → documentation and artifact generation
6. **Skills** → reusable agent capabilities
7. **Workflow & Automation** → orchestration and scheduled/controlled actions
8. **Git & Code Review** → GitHub Guardian, Builder/Critic/Verifier workflows
9. **Security & Permissions** → Constitution, Authority Budget, Privacy Gate
10. **Remote & Mobile** → mobile/remote KUBERA control
11. **Usage & Billing** → token/cost observability
12. **Models & Providers** → model routing and provider adapters
13. **Sessions & Messages** → durable agent sessions
14. **Notifications & Integrations** → event delivery and external systems
15. **Development & Runtime** → local execution, sandboxes, tooling
16. **UI Enhancements** → future operator console
17. **Plugin Markets & Managers** → capability discovery/update management
18. **Identity & Communication** → agent/provider identity boundaries
19. **Themes & Appearance** → low priority for core architecture
20. **Just for Fun** → excluded from core unless a real product use appears

## First verified candidates

### `00080000/dsh-project-memory`
**Source category:** memory  
**Why interesting:** indexes project files into searchable summaries as they are read; later retrieves matching information with source citations and BM25 ranking instead of re-reading everything.  
**KUBERA fit:** Project Memory, Reality Graph retrieval, Life → System Compiler context loading.  
**Status:** `CANDIDATE` — upstream plugin license/security review still required.

### `030611/dsh-telemetry-redactor`
**Source category:** security  
**Why interesting:** redacts supported secret patterns from telemetry export copies before data reaches configured telemetry backends.  
**KUBERA fit:** Context / Privacy Gate, External Intelligence Gateway, telemetry hygiene.  
**Status:** `CANDIDATE` — implementation scope and upstream license must be reviewed.

### `030611/dsh-verification-receipt`
**Source category:** security  
**Why interesting:** records local JSONL summaries of tool counts and coarse verification signals without storing prompts, tool arguments or result text.  
**KUBERA fit:** Evidence Ledger, Proof-of-Work, privacy-preserving observability.  
**Status:** `CANDIDATE`.

### `030611/qiushi-dsh-evidence-audit`
**Source category:** security  
**Why interesting:** appends local hash-chained JSONL receipts for tool results and session events without storing prompts, arguments, result text or raw session IDs.  
**KUBERA fit:** tamper-evident Evidence Ledger, Decision Replay, audit trail.  
**Status:** `CANDIDATE`.

## Important rule
KUBERA may learn from architecture and metadata immediately, but **third-party code is never copied merely because the catalog is free**. Code adoption requires a plugin-level license check plus security review.

## Relationship to Open-Source Scout
The `Open-Source Scout` role inside External Intelligence Node can feed this registry. Its job is discovery and comparison; the Plugin Gate remains the authority that decides whether a candidate is safe enough to test.
