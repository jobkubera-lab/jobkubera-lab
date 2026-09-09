# KUBERA MCP LAB

**Status:** public engineering and learning track. Starter servers are read-only or prepare-only by default. No autonomous external actions.

KUBERA MCP LAB is the MCP engineering layer of KUBERA Agent OS: reusable, narrowly scoped servers that expose verified tools, resources and prompts to AI hosts while preserving human authority, provenance and least privilege.

## Product position

We do not build MCP servers for their own sake. We build reusable capabilities that can power multiple surfaces:

```text
Chat / Web / WhatsApp / CLI / future voice
                  |
             KUBERA Agent OS
                  |
            KUBERA MCP Gateway
       ___________|____________________________
      |       |       |      |       |     |   |
 Evidence   ONS    Tender   Local  Collector Document Business
   MCP      MCP      MCP     MCP      MCP      MCP     MCP
```

The same server can be reused by more than one host or channel.

## Current MCP baseline

This lab targets **MCP specification 2026-07-28** and the stable v2 SDK lines. Design assumptions:

- stateless protocol core for remote deployments;
- tools/resources/prompts as explicit capability surfaces;
- Streamable HTTP for remote servers and stdio for local learning/dev;
- deterministic tool names and bounded schemas;
- authorization and routing at gateway/tool boundaries;
- human approval before consequential writes;
- provenance for externally sourced facts.

## Implemented starter servers

1. **Hello MCP** — lifecycle/smoke-test server.
2. **Evidence MCP** — privacy-minimal provenance hashing and ledger-ready evidence records.
3. **ONS MCP** — read-only official UK statistics API access restricted to `/v1/` on `api.beta.ons.gov.uk`.
4. **Tender MCP** — typed interface to existing KUBERA Tender Intelligence and DRAFT_ONLY bid packs.
5. **Local MCP** — validates official `gov.uk` service URLs and produces local-service evidence envelopes.
6. **Collector MCP** — compares caller-supplied collectible listings without hidden marketplace scraping.
7. **Document MCP** — fingerprints, exact-term searches and bounded chunking for explicitly supplied text; no arbitrary filesystem access.
8. **Business MCP** — PREPARE_ONLY receptionist/booking and customer-reply artifacts; no message sending or calendar/CRM write.

The **TypeScript gateway reference** holds the deny-by-default route/tool registry for all eight servers.

## Directory map

```text
mcp-lab/
├── README.md
├── ARCHITECTURE.md
├── SECURITY.md
├── ROADMAP.md
├── pyproject.toml
├── shared/
│   ├── __init__.py
│   └── policy.py
├── servers/
│   ├── hello_mcp.py
│   ├── evidence_mcp.py
│   ├── ons_mcp.py
│   ├── tender_mcp.py
│   ├── local_mcp.py
│   ├── collector_mcp.py
│   ├── document_mcp.py
│   └── business_mcp.py
├── gateway/
│   ├── README.md
│   ├── package.json
│   ├── tsconfig.json
│   └── server.ts
├── learning/
│   └── TRACK.md
└── tests/
    └── test_policy_and_tools.py
```

## Operating rules

1. **Read-only first.** A new server starts without external write tools.
2. **One narrow responsibility.** Do not create a giant MCP with unrelated capabilities.
3. **Official/allow-listed sources first.** Procurement, statistics and local-service adapters prefer official APIs/sites.
4. **No credential passthrough.** Tools never ask a model to supply passwords, tokens or private account credentials.
5. **Human authority.** Sending, booking, purchasing, submitting or changing external state requires an explicit approval layer outside starter servers.
6. **Evidence before confidence.** A model-generated statement does not become evidence merely because it sounds plausible.
7. **Stable contracts.** Tool schemas are versioned and changed deliberately.
8. **Deny by default.** Unknown server/tool pairs are rejected by the gateway registry.

## Server catalogue

| Server | State | Side effect | Primary role |
|---|---|---|---|
| `hello_mcp` | runnable starter | READ_ONLY | learning / smoke test |
| `evidence_mcp` | runnable starter | PREPARE_ONLY | provenance hashes / evidence records |
| `ons_mcp` | runnable starter | READ_ONLY | official UK statistics |
| `tender_mcp` | runnable starter | PREPARE_ONLY | procurement qualification / draft bid pack |
| `local_mcp` | runnable starter | READ_ONLY | official local-service evidence |
| `collector_mcp` | runnable starter | READ_ONLY | supplied market-comparison evidence |
| `document_mcp` | runnable starter | READ_ONLY | scoped document utilities |
| `business_mcp` | runnable starter | PREPARE_ONLY | receptionist/booking drafts |

## Run locally

From `kubera-lab/mcp-lab`:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e .
python servers/hello_mcp.py
```

Starter servers use stdio by default. Remote deployment comes only after auth, rate-limit, observability and policy checks are in place.

## Gateway reference

```bash
cd gateway
npm install
npm run typecheck
npm start
```

The current gateway **authorizes logical routes only**. It deliberately does not proxy arbitrary upstream requests. Remote proxying is a later security-gated phase.

## CI gates

Pull requests touching MCP LAB must pass:

- Python package installation on Python 3.12;
- `py_compile` across shared policy and every starter server;
- pytest regression tests for hashing, URL allow-lists, identifiers, input budgets and approval policy;
- TypeScript installation and `tsc --noEmit` for the gateway reference.

A feature is not merged as "working" merely because documentation exists; the executable baseline must remain green.

## Relationship to existing KUBERA components

- **Tender MCP** exposes the existing Tender Intelligence engine rather than duplicating it.
- **Evidence MCP** is the MCP surface for Evidence Ledger concepts.
- **ONS MCP** is the standard read-only MCP direction for official statistics.
- **Local MCP** is designed to converge with Civic Evidence OS/Local Desk official-source logic.
- **Collector MCP** is the safe base for future Collector Intelligence once permitted marketplace/API sources are selected.
- **Document MCP** is the safe base for document workflows without arbitrary disk access.
- **Business MCP** models AI Receptionist preparation while reserving real booking/message writes for an approval architecture.
- **Gateway** is a control plane, not a business-logic monolith.

## Definition of done for a production MCP server

A server is not production-ready merely because it starts. It needs:

- documented scope and non-goals;
- typed tool schemas;
- allow-listed external dependencies;
- input validation and size budgets;
- deterministic error behavior;
- tests and CI;
- explicit remote authorization model;
- rate limits;
- audit/provenance design;
- no secret leakage;
- tenant isolation where applicable;
- human approval for consequential actions;
- idempotency/replay protection for writes;
- deployment and rollback instructions.

## Product rule

**KUBERA MCP servers expose bounded capabilities. KUBERA Agent OS decides when to use them. The human remains the authority for consequential actions.**
