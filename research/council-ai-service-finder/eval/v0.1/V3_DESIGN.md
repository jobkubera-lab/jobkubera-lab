# Council AI Service Finder — Retrieval v3 Design

## Purpose

Retrieval v3 is a deterministic, evidence-first routing layer for council service discovery. It is designed to improve classes of failures found in v2 without tuning against wording from disclosed blind evaluation queries.

## Changes from v2

1. **Token-boundary matching** — anchors match complete tokens/phrases, preventing `shop` from matching `shops` or arbitrary substrings.
2. **Conservative morphology** — declared stems match only token prefixes and stems shorter than four characters are ignored.
3. **Safety fallback** — legal-conclusion, prompt-injection, council impersonation and fabricated official-action requests return a safe fallback rather than a service.
4. **Explicit ambiguity** — tied or near-tied evidence returns `ambiguous_tie` instead of choosing a service by alphabetical order.
5. **Reproducibility** — v2 remains unchanged so results can be reproduced and compared.

## Validation discipline

- Disclosed blind-query wording must not be copied into anchors, stems, supports, thresholds or guards.
- Previously disclosed evaluation sets may be used diagnostically to identify *classes* of failure, not to tune exact query wording.
- Claims about retrieval quality require a fresh held-out evaluation set that was not visible while v3 rules or lexicons were written.
- Regression metrics and held-out metrics must be reported separately.
- A perfect regression score must never be presented as evidence of generalisation.

## Current architecture

`query -> normalize/tokenize -> safety guard -> deterministic service scoring -> ambiguity/multi-intent gate -> service or safe fallback`

The service catalogue remains controlled. v3 does not allow a language model to invent services or official decisions.

## Future architecture boundary

The routing contract should allow additional retrievers later without changing the safety/evidence contract:

- deterministic lexical retriever (current)
- Solr/OpenSearch adapter
- multilingual semantic retriever
- optional provider-neutral LLM intent adapter

All future retrievers should return candidates plus evidence/confidence. A separate decision layer should determine whether evidence is sufficient to return a service.

## Non-goals for v3

v3 is **not** production-ready, not a complete multilingual NLP system, and not evidence of LocalGov Drupal acceptance. It is an experimental retrieval iteration intended for honest independent validation.
