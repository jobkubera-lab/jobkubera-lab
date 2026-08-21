# KUBERA Plugin Gate

## Goal
Prevent “free plugin” from being interpreted as “safe plugin”.

## Required checks before sandbox install

### 1. Identity
- repository exists and is the intended upstream;
- maintainer/project identity is recorded;
- source has not silently moved to an unrelated repository.

### 2. License
- identify the plugin repository's actual license;
- record redistribution/modification obligations;
- if no usable license is present, do not copy code into KUBERA.

### 3. Source review
Look for:
- shell/process execution;
- arbitrary file reads/writes;
- credential/environment-variable access;
- network calls and telemetry;
- dynamic downloads / `curl | sh` patterns;
- obfuscated/minified payloads that are hard to review;
- persistence/startup hooks;
- package post-install scripts;
- update mechanisms and remote code loading.

### 4. Permission profile
Declare expected capabilities:

```yaml
filesystem: none | read | write
network: none | restricted | unrestricted
credentials: none | selected | broad
process_execution: false | true
external_accounts: []
```

### 5. Sandbox test
Unknown plugins should be tested outside environments containing production keys or private project data.

### 6. Human approval
No plugin becomes `ADOPTED` solely from an automated score.

## Verdicts

- `CANDIDATE` — discovered, not reviewed
- `WATCH` — interesting but not ready
- `SANDBOX_APPROVED` — permitted only in isolated test environment
- `ADOPTED` — reviewed and approved for a defined KUBERA use
- `REJECTED` — unacceptable license/security/maintenance/fit

## Future automation
GitHub Guardian + External Intelligence `Open-Source Scout` can automate discovery and evidence gathering, but Human Authority remains required for adoption.
