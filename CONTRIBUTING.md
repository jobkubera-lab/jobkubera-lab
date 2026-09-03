# CONTRIBUTING

KUBERA LAB is a public engineering workspace for the active KUBERA / DZAMBALA reference runtime, Civic Evidence work, Community Compass, and supporting research artifacts.

The product rule is fixed:

> **KUBERA prepares. The human remains the authority.**

## Scope

Contributions are welcome when they improve an existing active project, fix a verified defect, strengthen tests, or make documentation more accurate.

Do not:

- create Innovation Stack modules 19+;
- turn modules 01–18 into new parallel products;
- claim the reference runtime is a live council, bank, autonomous publisher, or production deployment;
- add send/publish/pay/delete/sign integrations without a separate explicit review;
- change the root profile `README.md` unless the repository owner explicitly asks for that exact change.

The current active direction is recorded in [`STATUS.md`](./STATUS.md).

## Development workflow

1. Start from an up-to-date `main` branch.
2. Create one focused feature/fix branch.
3. Keep one logical change per PR.
4. Add or update tests for behavior changes.
5. Run the relevant test suite before opening the PR.
6. Document limitations and failure modes; do not replace them with production claims.

For architectural changes, read first:

- [`kubera-lab/innovation-stack/DZAMBALA.md`](./kubera-lab/innovation-stack/DZAMBALA.md)
- [`kubera-lab/innovation-stack/KUBERA_OPERATOR.md`](./kubera-lab/innovation-stack/KUBERA_OPERATOR.md)
- [`STATUS.md`](./STATUS.md)

## Python compatibility

The public reference runtime requires **Python 3.11+** and CI currently tests **Python 3.11, 3.12, and 3.13**.

Use:

- type hints for public APIs;
- deterministic behavior in control-path code;
- standard-library solutions where practical;
- no new runtime dependency without review;
- fail-closed behavior for authorization, evidence, privacy, and tool-safety checks.

## Reference runtime layout

```text
kubera-lab/innovation-stack/reference-implementation/
├── pyproject.toml
├── examples/
├── src/
│   └── kubera_innovation/
│       ├── handoff.py
│       ├── work_contract.py
│       ├── execution_controls.py
│       ├── authorization_grant.py
│       ├── evidence_ledger.py
│       ├── tool_executor.py
│       └── local_draft_adapter.py
└── tests/
```

`SovereignToolExecutor` is the reference choke point for tool execution. Application/example code must not bypass it to call a side-effecting adapter directly.

## Run the reference tests

From the repository root:

```bash
cd kubera-lab/innovation-stack/reference-implementation
python -m pip install -e .
python -m unittest discover -s tests -v
python -m kubera_innovation demo --json
```

The same unit-test and safe-demo path is exercised by GitHub Actions across Python 3.11–3.13.

## Coverage

CI measures **source-only branch coverage** for `kubera_innovation`. The first source-only baseline measured **86%**. The workflow therefore enforces a conservative **85% fail-under floor** and also includes the safe CLI demo in the coverage run.

Do not claim a higher percentage unless a current CI report supports it.

## Control-path requirements

For consequential tool work, preserve the enforced sequence:

```text
Handoff
→ WorkContract
→ Privacy / validation
→ ledger-backed Source Gate
→ Evidence Gate
→ Action Gate / signed approval when required
→ Idempotency reserve
→ ToolAdapter
→ completion state
→ ActionLogger
→ Evidence Ledger
```

Required behavior includes:

- missing source/evidence fails closed;
- irreversible operations require exact signed approval;
- same idempotency key + same completed request does not repeat the side effect;
- pending/unknown external state is reconciled before retry;
- same key + different request conflicts;
- secrets/private context are not intentionally exported through tool payloads.

## Documentation rules

- Describe what exists, not what is merely planned.
- Put roadmap items in `STATUS.md`, not in historical release notes.
- Link claims to code, tests, PRs, or verified sources when appropriate.
- Keep the root profile `README.md` owner-controlled and unchanged unless explicitly authorized.
- Do not add vendor branding or copy third-party guides into KUBERA documentation.

## Security reports

For suspected vulnerabilities, follow [`SECURITY.md`](./SECURITY.md). Do not publish credentials, private data, exploitable secrets, or sensitive reproduction material in a public issue.

## Licensing

This repository currently does **not** contain a root `LICENSE` file. Do not assume that contributions or repository content are licensed under MIT or another open-source license unless the repository owner explicitly adds one.

A repository-wide license choice is an owner decision and is not implied by this contribution guide.

## Commit and PR quality

Prefer clear messages such as:

```text
fix: block pending idempotency replay
feat: add read-only lookup adapter behind executor
test: cover exact approval fingerprint conflict
docs: correct runtime testing instructions
```

A PR should state:

- what changed;
- why it is needed;
- files/behavior affected;
- tests run;
- any remaining limitation or manual step.

## Conduct

Keep review technical, specific, respectful, and evidence-based.
