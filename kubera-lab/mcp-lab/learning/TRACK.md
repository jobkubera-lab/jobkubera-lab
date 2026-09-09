# KUBERA MCP Learning Track

The learning track is project-based. Every level produces code that remains useful in KUBERA.

## Level 1 — understand the protocol surface

Build/run: `hello_mcp.py`

Learn:

- host vs client vs server;
- tool discovery;
- tool invocation;
- resources;
- stdio transport;
- typed tool arguments.

Exercise: add one harmless deterministic tool, then write a test for its input bounds.

## Level 2 — evidence and trust

Build/run: `evidence_mcp.py`

Learn:

- why model output is not evidence;
- canonical hashing;
- provenance envelopes;
- privacy-minimal records;
- stable identifiers.

Exercise: create two records from identical payloads and prove the evidence hash is stable.

## Level 3 — official API MCP

Build/run: `ons_mcp.py`

Learn:

- API endpoint versus website;
- allow-listed hosts/paths;
- JSON retrieval;
- timeouts;
- source evidence;
- why arbitrary URL tools are dangerous.

Exercise: retrieve a known ONS `/v1/` resource and inspect its evidence envelope.

## Level 4 — reuse existing KUBERA logic

Build/run: `tender_mcp.py`

Learn:

- MCP as an interface, not a replacement for domain code;
- dynamic integration with an existing engine;
- deterministic scoring;
- DRAFT_ONLY artifacts;
- mandatory/desirable requirement classification.

Exercise: pass a normalized sample tender and compare MCP output to direct Tender Intelligence output.

## Level 5 — control plane

Build/run: `gateway/server.ts`

Learn:

- TypeScript MCP v2 SDK;
- deny-by-default route registries;
- server/tool identity;
- policy versus business logic;
- preparation for remote routing.

Exercise: try an unknown server and unknown tool and confirm both are denied.

## Level 6 — remote/stateless deployment

Learn/build next:

- Streamable HTTP;
- stateless instances;
- HTTPS;
- auth;
- rate limits;
- request IDs;
- health/readiness;
- containers;
- rollback.

Exercise: deploy one read-only server to a test environment and verify no unauthenticated protected route exists.

## Level 7 — MCP Apps

Learn/build next:

- server-rendered MCP UI extension;
- sandbox boundaries;
- network policy;
- structured tool output -> compact UI.

First KUBERA target: Tender BID/REVIEW/NO-BID decision card with evidence links.

## Level 8 — business channel

Build after remote security gate:

```text
WhatsApp Business Platform
 -> channel gateway
 -> KUBERA Agent OS
 -> MCP Gateway
 -> capability servers
```

Learn:

- webhooks;
- channel identity;
- asynchronous delivery;
- customer state;
- approval flows;
- cost/usage controls.

## Level 9 — controlled writes

Only after approval architecture exists.

Pattern:

```text
prepare action
 -> human sees exact effect
 -> approval receipt
 -> write tool
 -> idempotency check
 -> external action
 -> audit receipt
```

Never implement "model says yes -> external write".

## Level 10 — reusable products

Combine the same core into vertical packs:

- AI Receptionist;
- Tender Desk;
- Local Desk;
- Collector Intelligence;
- Document Desk.

The learning goal is reached when you can explain, for each product: which surface receives the request, which agent decides, which MCP tool executes, which external source is trusted, and where human approval is required.
