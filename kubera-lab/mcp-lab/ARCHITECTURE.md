# KUBERA MCP LAB Architecture

## Goal

Expose KUBERA capabilities as small, auditable MCP servers without turning transport code into product logic.

## Layers

```text
1. SURFACES
   Chat / Web / WhatsApp / CLI / future voice

2. AGENT / ORCHESTRATION
   KUBERA Agent OS
   - intent
   - planning
   - tool selection
   - human approval

3. MCP CONTROL PLANE
   KUBERA MCP Gateway
   - server allow-list
   - tool allow-list
   - auth boundary
   - routing
   - rate limits
   - request IDs

4. CAPABILITY SERVERS
   Evidence MCP
   ONS MCP
   Tender MCP
   Local MCP
   Collector MCP
   Document MCP
   Business MCP

5. SOURCE / SYSTEM LAYER
   Evidence Ledger
   ONS official APIs
   Find a Tender / Contracts Finder
   council official sources
   approved databases / customer systems
```

## Server contract

Every KUBERA MCP server should declare:

- server identity and version;
- scope and non-goals;
- tools/resources/prompts;
- side-effect class (`READ_ONLY`, `PREPARE_ONLY`, `WRITE_REQUIRES_APPROVAL`);
- external domains it may contact;
- data retained, if any;
- error contract;
- evidence/provenance output where applicable.

## Stateless remote design

Remote servers should assume requests can land on any replica. Application state belongs in explicit storage, not implicit MCP sessions. Correlation should use request IDs and durable job/evidence IDs.

For remote deployments:

```text
Client
  -> HTTPS
  -> Gateway / policy
  -> stateless MCP instance
  -> explicit database / ledger / official API
```

This lets ordinary load balancing, rolling deploys and horizontal scaling work without sticky-session dependence.

## Local versus remote

### Local / stdio
Use for:

- learning;
- development;
- private file/data tools;
- single-user experiments;
- integration tests.

### Remote / Streamable HTTP
Use when:

- multiple clients need access;
- the service must run 24/7;
- a WhatsApp/web surface needs it;
- centralized auth/rate-limit/observability are required.

Remote mode is not enabled merely because code can listen on a port. Security and operational gates must pass first.

## Gateway responsibilities

The gateway may:

- resolve logical server names to endpoints;
- deny unknown servers/tools;
- authenticate clients;
- attach request IDs;
- enforce per-tool policy and quotas;
- expose health/metadata;
- collect minimal audit telemetry.

The gateway must not:

- contain domain business logic;
- fabricate tool results;
- bypass human approval;
- proxy arbitrary URLs supplied by the model;
- log raw secrets or unnecessary private content.

## Write actions

KUBERA divides tools into three classes:

### READ_ONLY
Examples: retrieve statistics, read tender notice, calculate score.

### PREPARE_ONLY
Examples: draft bid pack, prepare booking request, prepare message.

### WRITE_REQUIRES_APPROVAL
Examples: send message, create booking, submit form, change CRM record.

The current public MCP Lab implements the first two only. Future write-capable servers must receive an approval receipt generated outside the model's free-form text.

## Provenance pattern

Externally sourced facts should return or link to:

```json
{
  "source": "official_source_name",
  "source_url": "https://...",
  "retrieved_at": "...",
  "evidence_hash": "sha256..."
}
```

This is the bridge between MCP capability execution and the KUBERA Evidence Ledger.

## Expansion pattern

New capability:

```text
problem
 -> source authority
 -> narrow tool contract
 -> policy class
 -> local implementation
 -> tests
 -> evidence model
 -> remote auth/rate-limit design
 -> gateway registration
 -> production review
```

Do not skip from idea directly to public remote endpoint.
