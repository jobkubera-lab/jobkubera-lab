# KUBERA Agent OS

What we show a customer. What we build next. What already exists in this GitHub.

## One sentence

KUBERA takes a real work task, checks sources, prepares the result, and waits for the human before any external action.

## Why a customer pays

Teams already have ChatGPT, search and ten tabs. They still lose time on:

- unchecked answers
- agents that post or send too early
- no trace of why a result appeared

KUBERA sells the missing layer: **verified groundwork + human authority**.

## What the demo must show in 5 minutes

1. Customer types a task in plain language.
2. System splits work (research / match / draft).
3. It returns: result, sources, confidence as an engineering score not a promise.
4. It prepares an action (email, reply, listing, form link).
5. Nothing is sent until the customer approves.
6. A log stores the decision hash, not raw private text.

If a slide cannot point to a running step, cut the slide.

## Borrowed from the market — used as rules, not copies

| Others ship | We take as a rule | Already in this GitHub |
|---|---|---|
| Parallel workers + one report (Grok Workflows) | Split task, merge one brief | Agent Fabric workers + Civic/Compass outputs |
| Chat surface + server agent (Vercel + Claude Managed Agents) | One session per job, many channels later | CLI + website as first surfaces |
| Independent check / skeptics | Second pass before the brief is trusted | verifier / safety fallbacks |
| Privacy aliases + no raw logs (Brave / Anthropic Insights style) | Hash the query, allow-list profile tags | evidence.jsonl, ResidentProfile rules |
| Hardware / explicit sign-off (wallet pattern) | External write needs approval | Trust Mesh ActionIntent idea |
| Voice as an output only (ElevenLabs) | Voice later, not the brain | not built — do not demo |

Do not paste their code. Do not use their names in the customer pitch except “the market already works this way”.

## Product shape

```
Task in
  → plan
  → workers (bounded)
  → check
  → brief + draft action
  → human approve / reject
  → receipt in ledger
```

Noses (pluggable, one at a time):

- work & documents (visa, CV, employer letter) — templates already exist
- local verified lookup (council / events) — code already exists
- research brief for a business question — docs exist, runtime thin
- later: voice out, chat adapters, paid sign-off

## What is already built (say this to a funder)

- Civic Evidence OS: tested lookup, fallbacks, no form submit
- Assisted plain-text channel
- Optional profile with consent and erasure
- Community Compass: manual event seeds + validation
- Agent Fabric reference: worker budget, approval gate, hash ledger
- Public site + migration/job libraries

Status line to say out loud: **tested prototypes, not a live council system, not a bank, not auto-publish.**

## What to build before the first paid pilot (only this)

1. One demo page: task box → brief → approve button that does not send.
2. One YAML/JSON job record: task, sources, score, action draft, approved true/false.
3. Three canned demos: “find official service”, “draft a reply to an employer”, “weekend events list”.
4. One-page pitch PDF from this file. No extra architecture novels.

## Do not build for the pitch

New repos, modules 19–30, live posting, payments, scraping Compass, “Merton official partner”, eligibility engine.

## Ask to the customer

Pilot 4–6 weeks. One workflow they already do by hand. Fixed fee. We plug their sources into this OS. They keep the approve button.
