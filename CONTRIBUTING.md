# CONTRIBUTING

Thank you for your interest in contributing to KUBERA LAB!

This is a **professional engineering project** building practical AI systems. We welcome contributions that:
- Improve code quality and testing
- Clarify documentation
- Add new capabilities
- Report issues
- Suggest architectural improvements

---

## How to contribute

### 1. Report issues

Found a bug or architectural concern?

**Open an issue with:**
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Any relevant logs or traces
- Environment (Python version, OS, etc.)

### 2. Discuss major changes

For significant changes:
- Open an issue first
- Describe the change and why
- Wait for discussion
- Then submit a PR

This helps us align on architecture and prevents wasted effort.

### 3. Submit pull requests

**Before submitting:**
- Fork the repository
- Create a feature branch: `git checkout -b feature/your-feature`
- Make your changes
- Write or update tests
- Update documentation
- Run the full test suite

**In your PR description:**
- What does this change do?
- Why is it needed?
- How does it relate to existing code?
- Any breaking changes?
- Links to related issues

### 4. Code standards

**Python:**
- Python 3.9+ compatible
- Follow PEP 8
- Use type hints
- Write docstrings
- No external dependencies without review

**Testing:**
- Write tests for new functionality
- Run `python -m unittest discover -s tests -v`
- Aim for >80% coverage
- Test failure cases

**Documentation:**
- Update README.md if needed
- Add docstrings to functions
- Explain architectural decisions
- Link to related files

### 5. Key principles

When contributing, keep these principles in mind:

1. **Evidence before claims** — all changes should be testable and verifiable
2. **Privacy by default** — never expose internal state unnecessarily
3. **Human authority** — no automatic actions on consequential decisions
4. **Deterministic** — avoid non-determinism in core logic
5. **Reversibility** — prefer preparation over irreversible side effects

---

## Architecture guidelines

### Before you code

- Read [DZAMBALA.md](./kubera-lab/innovation-stack/DZAMBALA.md) for control-layer philosophy
- Review [KUBERA_OPERATOR.md](./kubera-lab/innovation-stack/KUBERA_OPERATOR.md) for execution rules
- Check STATUS.md for current direction

### When adding features

1. **Keep it reversible** — new code should support preparation (reversible) better than side effects
2. **Use the gates** — source → evidence → action gates for any external integration
3. **Add to evidence ledger** — log consequential decisions with sources and reasoning
4. **Require approval for irreversible actions** — no automatic sends, publishes, or deletions
5. **Support idempotency** — retries should be safe

### Code organization

```
kubera-lab/
├── innovation-stack/
│   ├── reference-implementation/    # Executable reference runtime
│   │   ├── handoff.py             # HandoffArtifact
│   │   ├── work_contract.py       # WorkContract
│   │   ├── gates.py               # Source/Evidence/Action gates
│   │   ├── executor.py            # SovereignToolExecutor
│   │   └── evidence_ledger.py     # Evidence log
│   ├── DZAMBALA.md                # Architecture
│   └── KUBERA_OPERATOR.md         # Operational rules
├── kubera-guide-global-mapping/   # Public mapping project
├── dzambala-community-compass/    # Geographic discovery
└── kubera-stones/                 # Craft work
```

---

## Testing strategy

### Unit tests

```bash
cd civic-evidence-os
PYTHONPATH=. python -m unittest discover -s tests -v
```

### Validation tests

- Test evidence gates (source, evidence, action)
- Test idempotency (same request, same result)
- Test fallback behavior (missing data)
- Test privacy (no query leakage)

### Integration tests

- End-to-end handoff flow
- Evidence ledger consistency
- Multi-agent coordination

---

## Documentation standards

- Use clear, technical language
- Explain the "why" not just the "what"
- Link to related files and concepts
- Include examples where helpful
- Mark sections [DRAFT], [STABLE], [DEPRECATED]

---

## Commit messages

Use clear, descriptive commit messages:

```
fix: Correct idempotency key conflict handling

- Check for same key + different request
- Return CONFLICT state instead of executing
- Add test for conflict detection
- Fixes #42
```

Good prefixes:
- `fix:` — bug fix
- `feat:` — new feature
- `docs:` — documentation
- `refactor:` — code cleanup
- `test:` — adding/improving tests
- `chore:` — maintenance

---

## Licensing

By contributing, you agree your work is licensed under the MIT License.

---

## Code of conduct

We expect all contributors to:
- Be respectful and inclusive
- Focus on the work, not the person
- Value clear communication
- Welcome diverse perspectives
- Acknowledge mistakes and learn from them

---

## Questions?

- Open a GitHub issue
- Email: jobkubera@gmail.com
- Telegram: [@kuberababa](https://t.me/kuberababa)

Thank you for building trustworthy AI systems! 🚀
