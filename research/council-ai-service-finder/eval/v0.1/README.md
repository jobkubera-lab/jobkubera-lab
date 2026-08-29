# Council AI Service Finder — Evaluation Harness

A deterministic research harness for mapping ordinary resident language to a controlled catalogue of council services without inventing unsupported services or advice.

## Current architecture

The project now contains three transparent retrieval controls:

- `evaluate_baseline.py` — IDF-weighted lexical baseline;
- `evaluate_bm25.py` — dependency-free BM25 comparison;
- `retrieval_v2.py` — structured intent retrieval with anchor evidence, multilingual morphology, multi-intent fallback and hard safety fallbacks.

## Retrieval v2

The v2 matcher addresses the failure modes found during baseline validation without introducing an LLM dependency.

### Anchor evidence

Each service has service-defining anchors in `intent_lexicon_v2.json`. Context words can improve an already-supported match but cannot create a service match on their own.

Example: `low income` is context, not proof of Council Tax Support. A tax anchor such as `council tax`, `local tax` or `tax bill` is required.

### Multilingual morphology

Service-specific Ukrainian and Polish stems support common inflection patterns for the multilingual services currently covered by the evaluation set. This keeps the behaviour deterministic and locally testable.

### Multi-intent handling

If two distinct services both have strong anchor evidence, v2 returns a conservative `multi_intent` fallback rather than arbitrarily selecting one service.

### Safety fallback

Known classes of authoritative legal-conclusion requests and prompt-injection instructions are hard-fallback cases before service selection.

## Frozen regression gate

`frozen_postfix_validation_v1.jsonl` contains 32 resident-style cases covering all 20 catalogue services plus multilingual, out-of-scope, adversarial and multi-intent requests.

After the structural v2 remediation, the unchanged frozen set records:

- Precision@1: **1.000 (26/26)**
- Fallback accuracy: **1.000 (6/6)**
- False-positive fallback cases: **0**
- Multi-intent case: **correct fallback**

See `FROZEN_POSTFIX_VALIDATION_RESULTS.md` for the full remediation record and the earlier IDF/BM25 controls.

These are regression results. A future external-quality benchmark should be authored independently after v2 is frozen and measured before any further tuning.

## Files

- `service_catalogue.json` — controlled 20-service evaluation catalogue
- `intent_lexicon_v2.json` — service anchors, support evidence and multilingual stems
- `queries.jsonl` — original synthetic evaluation set
- `multilingual_challenge.jsonl` — multilingual regression challenge
- `frozen_postfix_validation_v1.jsonl` — frozen post-fix regression gate
- `evaluate_baseline.py` — IDF baseline
- `evaluate_bm25.py` — BM25 baseline
- `retrieval_v2.py` — structured retrieval v2
- `test_evaluate_baseline.py` — baseline tests
- `test_evaluate_bm25.py` — BM25 tests
- `test_retrieval_v2.py` — v2 architecture and safety regression tests

## Core invariants

1. Return only controlled service IDs.
2. No service match without service-defining evidence.
3. Ambiguous/multi-intent input falls back rather than choosing arbitrarily.
4. Anonymous/offline deterministic operation remains possible.
5. Retrieval decisions remain explainable through matched anchors/support terms.
6. No production claim is inferred from a synthetic catalogue; council deployment requires council-approved service data and an external validation gate.
