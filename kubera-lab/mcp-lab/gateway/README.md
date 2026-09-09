# KUBERA MCP Gateway Reference

This directory is the control-plane reference for remote KUBERA MCP deployment.

## What exists now

`server.ts` is a runnable MCP v2 stdio reference exposing two gateway-policy tools:

- `list-approved-routes`
- `authorize-route`

It implements a **deny-by-default registry** for the starter KUBERA servers. It deliberately does **not** proxy requests yet.

## Why no proxy in v0.1

A production proxy introduces authentication, tenant identity, network routing, retries, timeouts, quotas, observability and failure semantics. Those controls must be designed before arbitrary upstream forwarding is enabled.

## Planned remote path

```text
MCP client
  -> HTTPS
  -> authenticated gateway
  -> route/tool policy
  -> rate limit
  -> selected stateless MCP service
  -> source/database
```

## Production requirements before HTTP proxying

- HTTPS termination;
- OAuth/machine-auth decision for the target product;
- subject and tenant binding;
- per-tool authorization;
- upstream server allow-list;
- no arbitrary URL proxy parameter;
- connect/read/overall timeouts;
- request/response size limits;
- per-client quotas;
- structured audit events;
- circuit breaker/retry policy;
- health/readiness checks;
- secret manager;
- container/non-root runtime;
- rollback documentation.

## Local run

```bash
npm install
npm run typecheck
npm start
```

## Important distinction

The gateway is policy and routing. Business logic belongs in capability servers such as Tender MCP or ONS MCP.
