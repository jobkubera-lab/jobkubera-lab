# KUBERA Tender Intelligence

**Status:** public reference prototype with read-only official-source adapters and v1.1 procurement intelligence. No live tender submission, no autonomous bidding, no claim of government partnership.

KUBERA Tender Intelligence turns UK public procurement opportunities into structured, evidence-backed **BID / REVIEW / NO-BID** decisions for a human operator.

```text
Official procurement source
  -> read-only retrieval
  -> OCDS normalization
  -> provenance + evidence hash
  -> duplicate control
  -> pagination + checkpoint
  -> deadline intelligence
  -> CPV intelligence
  -> requirement verification
  -> buyer intelligence
  -> win-gap analysis
  -> draft bid pack
  -> HUMAN DECISION
```

## v1.1 capabilities

### Pagination + checkpoint
The v1.1 pipeline can follow source cursors across multiple pages and persists per-source checkpoint state. The checkpoint stores cursor, high-watermark, processed count and update time. This prevents every run from behaving like a first run.

### Deadline intelligence
Every opportunity is classified as `CLOSED`, `CRITICAL`, `URGENT`, `ACTIVE`, `EARLY` or `UNKNOWN`. Closed opportunities are forced to `NO_BID` in the v1.1 pipeline.

### CPV intelligence
CPV codes are matched by deterministic prefix rules from `v11_config.json`. Text matching remains useful, but CPV gives a second procurement-native signal.

### Requirement verifier
Requirements are separated into `MANDATORY`, `DESIRABLE` and `REVIEW` using explicit language markers. The verifier is deliberately conservative: ambiguous clauses are not silently treated as mandatory.

### Buyer intelligence
The v1.1 layer accepts read-only award-history records and can identify recurring suppliers for the same buyer. No award history means `unknown`, not a guessed conclusion.

### Win-gap analysis
Tender requirements are compared with a documented KUBERA evidence map. Each item becomes `EVIDENCED`, `GAP` or `REVIEW`, with a concrete action. A mandatory unmet condition remains a blocker for human review.

### Bid pack generator
For each opportunity v1.1 can prepare a **draft-only** pack containing:

- opportunity summary;
- BID / REVIEW / NO-BID qualification;
- deadline intelligence;
- CPV matches;
- buyer history summary;
- mandatory / desirable / review requirements;
- win-gap analysis;
- go/no-go checklist;
- proposed response sections;
- blockers before bid.

Every bid pack contains `human_approval_required: true`. It is preparation, not submission.

## UK Procurement Adapter

Official read-only OCDS routes:

- Find a Tender: `https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages`
- Contracts Finder: `https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search`

The adapter normalizes both sources into one stable KUBERA opportunity contract, generates a SHA-256 evidence hash and deduplicates by OCID, notice ID, then evidence hash.

A value is populated into `estimated_value_gbp` only when the source currency is GBP or unspecified. Other currencies are never silently relabelled as GBP.

## Files

- `tender_intelligence.py` — deterministic base scoring.
- `procurement_adapter.py` — Find a Tender + Contracts Finder retrieval and normalization.
- `procurement_pipeline.py` — v1 intake pipeline.
- `intelligence_v11.py` — deadline, CPV, requirement, buyer, gap and bid-pack intelligence.
- `procurement_pipeline_v11.py` — paginated v1.1 orchestration with checkpoint state.
- `capabilities.json` — base capability/risk profile.
- `v11_config.json` — CPV map, evidence keywords and capability evidence.
- `test_tender_intelligence.py` — base scoring tests.
- `test_procurement_adapter.py` — adapter tests.
- `test_intelligence_v11.py` — v1.1 regression tests.

## Example v1.1 run

```bash
python procurement_pipeline_v11.py \
  --source find_a_tender \
  --profile capabilities.json \
  --v11-config v11_config.json \
  --checkpoint state/procurement_checkpoint.json \
  --from 2026-09-01T00:00:00 \
  --to 2026-09-09T23:59:59 \
  --limit 100 \
  --max-pages 5 \
  --evidence-jsonl evidence/procurement.jsonl
```

Optional buyer award-history enrichment:

```bash
  --award-history evidence/buyer_awards.json
```

## Human authority

KUBERA may discover, retrieve, normalize, compare, score, verify, prepare checklists and draft response material.

KUBERA must **not** submit a bid, accept legal terms, sign declarations, make unsupported compliance claims or send external messages without explicit human approval.

## Product rule

**KUBERA finds the opportunity, proves where it came from, evaluates the fit, identifies the gaps and prepares the bid work. The human decides whether to bid.**
