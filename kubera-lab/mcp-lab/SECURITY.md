# KUBERA MCP LAB Security Baseline

## Threat model

MCP connects models to tools. That creates a trust boundary between untrusted/nondeterministic model output and systems that may contain real data or perform real actions.

Primary risks:

- prompt-driven misuse of a legitimate tool;
- arbitrary URL or filesystem access;
- credential leakage;
- over-broad tool permissions;
- tool result injection;
- replay/duplicate writes;
- excessive logging of private data;
- unauthenticated remote access;
- dependency/supply-chain compromise;
- confused-deputy behavior across tenants or users.

## Mandatory controls

### 1. Least privilege
A server receives only permissions required by its narrow purpose. Read-only servers do not receive write credentials.

### 2. Allow-list external destinations
Tools must not accept arbitrary hosts from a model. External domains/endpoints are fixed or validated against configuration.

### 3. No secrets in model arguments
Passwords, access tokens, API secrets and session cookies are resolved from server-side secret storage/environment configuration, never requested as ordinary tool parameters.

### 4. Approval receipts for writes
Consequential actions require a machine-verifiable approval object issued by the KUBERA control layer. Free-form model text such as "approved" is insufficient.

### 5. Input and output validation
Typed schemas bound strings, lists, IDs, sizes and accepted enum values. Errors are explicit and safe.

### 6. Provenance
Externally sourced facts should carry source identity, URL where appropriate, retrieval time and evidence hash.

### 7. Privacy-minimal logs
Default audit records contain request/tool identity, decision, timing and hashes — not full private prompts or credentials.

### 8. Rate limits and budgets
Remote servers need per-client and per-tool quotas. Expensive tools also need execution/time/result-size bounds.

### 9. Tenant/user isolation
If multiple customers ever use a remote KUBERA service, tenant identity must be explicit and server-side enforced. The model cannot choose another tenant ID freely.

### 10. Dependency discipline
Pin production dependencies, run vulnerability updates, preserve upstream licenses and avoid copying unreviewed MCP server code into KUBERA.

## Side-effect classes

| Class | Meaning | Public lab status |
|---|---|---|
| `READ_ONLY` | retrieves/calculates without external mutation | allowed |
| `PREPARE_ONLY` | creates drafts/checklists locally | allowed |
| `WRITE_REQUIRES_APPROVAL` | changes an external system | design only |
| `PROHIBITED` | bypasses auth/safety or handles unsupported sensitive operations | never exposed |

## Remote authorization

Remote deployment must use HTTPS and an explicit authorization layer. Authorization decisions should be enforceable by server/tool identity, not only by a generic "logged in" flag.

Recommended policy inputs:

- authenticated subject/client;
- server name;
- tool name;
- tenant/workspace scope;
- side-effect class;
- approval receipt when required;
- rate-limit state.

## Gateway deny-by-default

Unknown server: deny.
Unknown tool: deny.
Missing subject in protected remote mode: deny.
Write-class tool without valid approval: deny.
Arbitrary external URL: deny.
Oversized input/result: deny or truncate safely according to contract.

## Prompt injection boundary

External webpages, tender descriptions, documents and database content are data, not instructions to the MCP control plane. A tool result must never be allowed to redefine gateway policy, secret handling or approval requirements.

## Incident response

For any suspected compromise:

1. disable affected remote route/tool;
2. revoke relevant credentials;
3. preserve minimal audit/evidence records;
4. determine affected users/data/systems;
5. patch and test;
6. rotate credentials;
7. redeploy;
8. document failure mode in KUBERA Failure Memory.

## Production gate

A remote MCP server cannot be labelled production-ready until auth, allow-lists, rate limits, secret storage, structured logging, health checks, tests, deployment rollback and incident ownership are documented and exercised.
