# KUBERA Tender Intelligence

**Status:** public reference prototype. No live tender submission, no autonomous bidding, no claim of government partnership.

KUBERA Tender Intelligence turns public procurement opportunities into a structured, evidence-backed **BID / REVIEW / NO-BID** decision for a human operator.

It is not a separate product island. It is a new operational nose for **KUBERA Agent OS** and reuses the existing KUBERA control philosophy:

```text
Tender source
  -> normalize
  -> evidence record
  -> capability match
  -> risk / eligibility checks
  -> score
  -> draft bid brief
  -> HUMAN DECISION
```

## Problem

Government procurement portals contain thousands of opportunities. A small supplier usually loses time on three things:

1. finding opportunities that actually fit;
2. discovering mandatory requirements too late;
3. writing bids before deciding whether the opportunity is worth pursuing.

KUBERA changes the order: **filter first, prove the fit, then draft.**

## Target sources

Initial UK source adapters are intended for:

- Find a Tender
- Contracts Finder
- future regional adapters: Public Contracts Scotland, Sell2Wales and eTendersNI

The public reference implementation deliberately accepts normalized JSON rather than scraping websites. Live adapters should use official APIs, feeds or permitted retrieval routes where available.

## KUBERA capability map

The default profile focuses on work KUBERA can realistically support:

- AI assistants and controlled agent workflows
- automation / RPA-style process improvement
- data processing and analytics
- civic / local-government digital services
- websites, forms and lightweight portals
- accessibility and digital-service improvement
- document automation
- AI evaluation, assurance and evidence trails
- user research / service discovery
- technical support and small digital projects

## Decision model

Each opportunity is evaluated on six dimensions:

| Dimension | Meaning |
|---|---|
| Capability fit | Does the work match what KUBERA can actually deliver? |
| Buyer / public-sector relevance | Is it a public-service, local-government or adjacent digital problem? |
| SME suitability | Is the opportunity explicitly or practically accessible to a small supplier? |
| Evidence readiness | Can KUBERA point to prototypes, repositories, tests or documented methods? |
| Delivery risk | Are scale, certifications, security, insurance or staffing requirements too high? |
| Commercial practicality | Is the likely contract size / workload sensible for the current stage? |

The result is intentionally conservative:

- `BID` — strong fit and no blocking requirement detected;
- `REVIEW` — interesting, but a human must inspect requirements;
- `NO_BID` — weak fit or a blocking constraint is known.

## Evidence-first integration

Every scored opportunity can carry:

- source URL;
- buyer;
- notice / reference ID;
- publication and deadline dates;
- extracted requirements;
- matched capabilities;
- missing evidence;
- blocking conditions;
- score explanation.

These fields are designed to flow into the KUBERA Evidence Ledger rather than becoming an opaque LLM judgement.

## Human authority

KUBERA may:

- discover;
- summarize;
- compare;
- score;
- prepare a compliance checklist;
- draft answers;
- prepare a clarification question.

KUBERA must **not** submit a bid, accept legal terms, sign declarations or send external messages without explicit human approval.

## Files

- `tender_intelligence.py` — normalized opportunity model, deterministic scoring and decision output.
- `capabilities.json` — editable KUBERA capability profile and risk rules.
- `example_opportunity.json` — example normalized UK public-sector AI opportunity.
- `test_tender_intelligence.py` — basic regression tests.

## Example

```bash
python tender_intelligence.py example_opportunity.json capabilities.json
```

Example output shape:

```json
{
  "decision": "BID",
  "score": 82,
  "matched_capabilities": ["ai", "automation", "data"],
  "blockers": [],
  "review_reasons": [],
  "evidence_record": {
    "source_url": "...",
    "buyer": "Example Council",
    "notice_id": "EXAMPLE-001"
  }
}
```

## Next engineering steps

1. Add read-only adapters for official UK procurement feeds / APIs.
2. Store normalized notices as append-only evidence records.
3. Add deadline and duplicate detection.
4. Add requirement extraction with a second-pass verifier.
5. Add bid/no-bid dashboard to the Agent OS demo.
6. Add reusable response library only after real bid requirements are observed.

## Product rule

**KUBERA finds the opportunity, proves the fit and prepares the work. The human decides whether to bid.**
