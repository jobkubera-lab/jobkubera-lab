# KUBERA Tender Intelligence

**Status:** public reference prototype with read-only official-source adapters. No live tender submission, no autonomous bidding, no claim of government partnership.

KUBERA Tender Intelligence turns UK public procurement opportunities into structured, evidence-backed **BID / REVIEW / NO-BID** decisions for a human operator.

It is not a separate product island. It is an operational nose for **KUBERA Agent OS** and reuses the same control model:

```text
Official procurement source
  -> read-only retrieval
  -> OCDS normalization
  -> provenance + evidence hash
  -> duplicate control
  -> capability match
  -> risk / eligibility checks
  -> BID / REVIEW / NO-BID
  -> HUMAN DECISION
```

## Why this exists

Government procurement portals contain large volumes of opportunities. A small supplier usually loses time on three things:

1. finding opportunities that actually match its capabilities;
2. discovering mandatory requirements too late;
3. drafting responses before deciding whether the opportunity is worth pursuing.

KUBERA changes the order: **retrieve -> normalize -> prove provenance -> filter -> score -> review -> draft.**

## UK Procurement Adapter v1

The v1 adapter uses official, read-only procurement data routes rather than browser scraping.

### Find a Tender

Official OCDS release-package endpoint:

`https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages`

Supported filters in this implementation:

- `updatedFrom`
- `updatedTo`
- `stages`
- `limit`
- `cursor`

Find a Tender publishes procurement data in **Open Contracting Data Standard (OCDS)** JSON. The adapter defaults to `planning,tender`, so awards do not flood the opportunity pipeline.

### Contracts Finder

Official OCDS search endpoint:

`https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search`

Supported filters in this implementation:

- `publishedFrom`
- `publishedTo`
- `stages`
- `limit`
- `cursor`

The adapter deliberately uses the published-notice retrieval route, not authenticated buyer/draft endpoints.

## Source authority

Implementation is based on the official service documentation:

- Find a Tender data/API documentation: `https://www.find-tender.service.gov.uk/Developer/Documentation`
- Find a Tender OCDS release package: `https://www.find-tender.service.gov.uk/apidocumentation/1.0/GET-ocdsReleasePackages`
- Contracts Finder API documentation: `https://www.contractsfinder.service.gov.uk/apidocumentation`
- Contracts Finder v2 release notes: `https://www.contractsfinder.service.gov.uk/apidocumentation/V2`

The adapter is intentionally **read-only**. It does not submit notices, bids, forms, declarations, attachments or credentials.

## Normalized opportunity contract

Every source is converted to one stable KUBERA shape:

```json
{
  "source": "find_a_tender",
  "source_url": "https://...",
  "notice_id": "000001-2026",
  "ocid": "ocds-...",
  "title": "AI assisted local service discovery pilot",
  "description": "...",
  "buyer": "Example Council",
  "published_date": "2026-09-09T10:00:00Z",
  "deadline": "2026-10-01T12:00:00Z",
  "estimated_value_gbp": 85000,
  "currency": "GBP",
  "requirements": ["..."],
  "tags": ["tender", "selective"],
  "cpv_codes": ["72262000"],
  "locations": ["UKI63"],
  "raw_release_id": "000001-2026",
  "evidence_hash": "sha256...",
  "retrieved_at": "..."
}
```

### Important currency rule

A value is populated into `estimated_value_gbp` **only when the source currency is GBP or unspecified**. A EUR/USD value is never silently relabelled as GBP.

## Evidence-first design

Every normalized notice receives a SHA-256 hash of its canonical source release. The ledger-ready record stores only the procurement provenance needed for audit:

- source
- source URL
- notice ID
- OCID
- buyer
- publication date
- deadline
- evidence hash
- retrieval time

The full raw description is not copied into the minimal ledger record.

This keeps the evidence layer traceable without turning it into an uncontrolled mirror of external data.

## Duplicate control

Duplicate identity is resolved in this order:

1. `ocid`
2. notice ID
3. evidence hash

This prevents the same procurement process from being repeatedly scored when the same release appears more than once in a batch.

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

The result remains intentionally conservative:

- `BID` — strong fit and no blocking requirement detected;
- `REVIEW` — interesting, but a human must inspect requirements;
- `NO_BID` — weak fit or a blocking constraint is known.

## Files

- `tender_intelligence.py` — deterministic capability/risk scoring and BID / REVIEW / NO-BID decision.
- `procurement_adapter.py` — read-only Find a Tender + Contracts Finder OCDS retrieval, normalization, provenance hashing and deduplication.
- `procurement_pipeline.py` — source -> normalize -> deduplicate -> score -> optional JSONL evidence pipeline.
- `capabilities.json` — editable KUBERA capability profile and risk rules.
- `example_opportunity.json` — example normalized UK public-sector AI opportunity.
- `test_tender_intelligence.py` — scoring regression tests.
- `test_procurement_adapter.py` — adapter/normalization/provenance regression tests with offline fixtures.

## Usage

### Score an already-normalized opportunity

```bash
python tender_intelligence.py example_opportunity.json capabilities.json
```

### Read Find a Tender and score opportunities

```bash
python procurement_pipeline.py \
  --source find_a_tender \
  --profile capabilities.json \
  --from 2026-09-01T00:00:00 \
  --to 2026-09-09T23:59:59 \
  --limit 100 \
  --evidence-jsonl evidence/procurement.jsonl
```

### Read Contracts Finder and score opportunities

```bash
python procurement_pipeline.py \
  --source contracts_finder \
  --profile capabilities.json \
  --from 2026-09-01 \
  --to 2026-09-09 \
  --limit 100 \
  --evidence-jsonl evidence/procurement.jsonl
```

## Human authority

KUBERA may:

- discover;
- retrieve official public notices;
- normalize;
- summarize;
- compare;
- deduplicate;
- score;
- prepare a compliance checklist;
- draft bid material;
- prepare clarification questions.

KUBERA must **not** submit a bid, accept legal terms, sign declarations or send external messages without explicit human approval.

## What v1 deliberately does not do

- no authenticated buyer APIs;
- no bid submission;
- no credential handling;
- no uncontrolled scraping;
- no automatic legal/compliance claims;
- no silent FX conversion;
- no LLM-only scoring without deterministic evidence;
- no claim that a matching tender is commercially winnable.

## Next engineering steps

1. Add pagination/cursor orchestration with checkpoint state.
2. Add deadline expiry and timezone-safe urgency classification.
3. Add second-pass structured requirement extraction with verifier.
4. Add CPV-aware capability mapping alongside text matching.
5. Add buyer history / award evidence as a separate read-only enrichment layer.
6. Connect evidence JSONL to the shared KUBERA Evidence Ledger contract.
7. Add a compact bid/no-bid dashboard to the Agent OS demo.

## Product rule

**KUBERA finds the opportunity, proves where it came from, evaluates the fit and prepares the work. The human decides whether to bid.**
