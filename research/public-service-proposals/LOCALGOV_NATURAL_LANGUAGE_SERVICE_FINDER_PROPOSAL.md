# LocalGov Drupal Proposal

## Suggested issue title

`Proposal: provider-neutral natural-language service finder for LocalGov Drupal`

## Suggested issue body

### Summary

I would like to propose an optional, provider-neutral service-discovery layer for LocalGov Drupal that helps residents find council services using ordinary language rather than requiring them to know the council's exact terminology or information architecture.

Example:

> “I need to get rid of an old sofa”

The system should be able to surface relevant council content such as bulky-waste collection or a household recycling centre, while keeping the council's published service pages as the source of truth.

### Problem to explore

Council service content can use formal or locally specific terminology. Residents may search with different words, incomplete phrases, spelling mistakes or descriptions of a problem rather than the service name.

A reusable LocalGov Drupal approach could reduce the need for every council to build its own synonym lists, semantic search integration and user interface from scratch.

### Proposed architecture

#### Phase 1 — retrieval-first MVP

1. Index LocalGov service content through Drupal/Search API-compatible metadata.
2. Accept a natural-language resident query.
3. Retrieve a small candidate set using deterministic search, synonyms and/or semantic embeddings.
4. Rank the candidates and return 2–5 relevant existing service pages.
5. Always link back to the council's authoritative content.

The MVP should work without requiring a generative model.

#### Phase 2 — optional LLM reranking / clarification

Add a provider adapter that can optionally:

- rerank already-retrieved service candidates
- classify user intent
- ask a short clarification question when the query is ambiguous
- produce a concise explanation of why a result may be relevant

The integration should be provider-neutral rather than hard-coded to one vendor. Councils should be able to choose a hosted model, local model or no LLM at all.

### Safety and governance requirements

For a public-sector module, I think the following should be first-class requirements:

- **Published council content remains the source of truth.** The model must not invent services, eligibility rules, prices or deadlines.
- **No automatic eligibility decision from an LLM.** Eligibility should come from explicit council rules or authoritative service content.
- **Data minimisation.** Do not send unnecessary personal information to an external model.
- **Provider abstraction.** Avoid vendor lock-in.
- **Auditability.** Record which content/result IDs were retrieved and what ranking step was applied.
- **Graceful fallback.** If the AI/semantic layer is unavailable, normal LocalGov search must continue to work.
- **Accessibility and progressive enhancement.** The service finder must remain usable on keyboard, assistive technology and low-capability devices.
- **Cost controls.** Hosted-model usage should have configurable request/token budgets rather than assuming a fixed vendor price.

### Possible module boundary

A module such as `localgov_service_finder` could expose:

- a query form/block
- a retrieval interface
- configurable synonym/intent metadata
- an optional semantic index adapter
- an optional LLM/reranker adapter
- structured result cards that point only to real Drupal content entities
- logging/metrics hooks for councils to evaluate whether residents actually find the correct service

### Evaluation before claiming impact

Rather than assuming a savings figure, a pilot could measure:

- successful task completion
- search reformulation rate
- zero-result rate
- click-through to the correct service
- time to reach the correct service
- accessibility/usability findings
- support-contact deflection, where a participating council can measure it reliably

### Suggested first step

Would LocalGov maintainers/councils be interested in a small proof of concept using a limited set of service content and a provider-neutral retrieval interface?

If there is interest, I would be happy to help define the MVP, build tests and document the architecture in line with LocalGov Drupal contribution standards.

---

**Author:** SHCHEGLOV NIKOLA  
**Target repository:** https://github.com/localgovdrupal/localgov/issues