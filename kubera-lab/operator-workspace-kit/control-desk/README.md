# KUBERA Control Desk — static demo

This directory is a **static, mock-data demonstration** of a future KUBERA operator interface. It is intentionally provider-neutral and performs no network calls or external actions.

## Views

- **Agents** — explicit agent/session states with approval/failure surfaced first.
- **Setup** — visible inventory of repository guidance, skills and deterministic gates.
- **Improve** — repeated correction evidence, target artifact, exact diff preview and a simulated approve/dismiss decision.

The Approve button only changes the browser UI. It does **not** write files, create PRs or execute tools.

## Run locally

From this directory:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Design boundary

The visual design and code are original KUBERA work. The demo does not copy another product's source code, branding, UI assets or proprietary implementation.

## Runtime relationship

The real reference implementation for correction clustering, proposal promotion, exact review and provider-neutral agent state lives in:

`kubera-lab/innovation-stack/reference-implementation/src/kubera_innovation/improvement_loop.py`
