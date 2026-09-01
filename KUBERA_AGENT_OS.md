# KUBERA Agent OS

What we show a customer. What we build next. What already exists in this GitHub.

## One sentence

KUBERA takes a real work task, checks sources, prepares the result, and waits for the human before any external action.

## Core

One core:

```text
Task
  → check
  → draft
  → human approve / reject
  → receipt in ledger
```

The core stays the same. The customer can use several existing KUBERA attachments around it.

## Existing attachments

1. **Work / visa** — existing job, visa, CV, letter and prompt libraries; `kuberajob` is the public work site.
2. **Place / events** — Mitcham mapping and Community Compass with manually verified event data.
3. **Official lookup** — Civic Evidence OS for controlled Merton service lookup with tests and conservative fallback behaviour.
4. **Agent control** — Agent Fabric / Trust Mesh for bounded workers, approval gates and hash-ledger mechanics.
5. **Client research** — existing product/research briefs plus worker/checking patterns.
6. **Later attachments** — voice output, chat channels and wallet/sign-off ideas only when the existing core needs them; they are not a new core.

## What the demo should show

A single customer-facing OS with several directions, not one Merton widget:

- Work / visa draft
- Place / events
- Official lookup
- Approve / ledger

The demo may use prepared examples, but it must keep the same operating rule: checked groundwork first, external action only after the human.

## Borrowed from the market — used as rules, not copies

- parallel workers can produce one merged brief;
- one session should represent one job;
- a second checker should challenge important output;
- logs should store hashes/controlled metadata rather than raw private task text;
- external writes require explicit human approval.

Do not paste third-party code. These are operating rules, not cloned products.

## Repository map inside the OS

- `kubera-lab/dzambala-community-compass/` — Place / events attachment.
- `kubera-lab/innovation-stack/reference-implementation/` — Agent Fabric / control reference.
- `KUBERA_LOCAL_DESK.md` — local civic product canon.
- `REPO_MAP.md` — workspace map.
- `KUBERA_PRODUCT.md` — product brief / customer language.
- `kubera-lab/agent-os-demo/` — customer-facing multi-direction demo.
- `kubera-improved-website/civic-evidence-os/` — Official lookup attachment in the existing public-site repository.
- `kubera-ai-prompts`, `kubera-visa-playbooks`, `kubera-migration-templates`, `kuberajob` — Work / visa content and public surface.

## Backlog, not separate products

Innovation-stack modules 01–18 are idea/backlog material. Do not expand them into new customer-facing products or more module families. Reuse a detail only when an existing attachment needs it.

## Status

**Prototype.** Existing components are tested prototypes, reference implementations, content libraries or public-site work. KUBERA is not a live council service, does not make official eligibility decisions, and does not auto-publish or auto-submit forms.

## Customer pitch

Show the OS plus several attachments already connected to the same rule:

**Here is the task. Here are the checked sources. Here is the prepared action. Without the approval button, the system stays silent.**
