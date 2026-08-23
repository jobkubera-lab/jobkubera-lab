# NHS.UK Frontend Proposal

## Suggested issue title

`Proposal: multilingual and plain-language support patterns for NHS.UK frontend`

## Suggested issue body

### Summary

I would like to propose a design-system-level exploration of multilingual and plain-language support patterns for NHS.UK frontend, focused on reusable frontend primitives rather than service-specific translation logic.

The goal is to make NHS services easier to use for people who do not speak English as a first language, while keeping accessibility, consistency and clinical safety in scope.

### Problem to explore

NHS services often need to communicate complex health information. Even when pages are technically accessible, users can still struggle with:

- unfamiliar medical terminology
- switching between translated and English content
- understanding which language a page or component is currently using
- finding equivalent plain-language wording for clinical terms
- navigating services when their search terms differ from the terminology used by the service

This is broader than WCAG conformance alone and may benefit from reusable frontend guidance/components.

### Suggested scope for NHS.UK frontend

#### 1. Language selector / language-status pattern

A documented, accessible pattern for:

- showing the current language
- linking to available translated versions
- preserving language context across navigation where the consuming service supports it
- exposing language names correctly to assistive technology

This would be a presentation pattern only; translation management would remain the responsibility of the consuming service.

#### 2. Plain-language medical-term pattern

Explore a reusable pattern for pairing a clinical term with a short plain-language explanation, for example:

> Hypertension (high blood pressure)

Potential implementations could include visible supporting text or an accessible disclosure pattern. The important part would be guidance on when to use it, rather than introducing a clinical glossary into the frontend package itself.

#### 3. Guidance for synonym-friendly content and search metadata

Search behaviour is normally outside the scope of a frontend component library, but the design system could document content patterns that make downstream search more robust, such as:

- common-language synonyms
- alternative spellings
- abbreviations and expanded terms
- language metadata

This would allow consuming NHS services to implement fuzzy or semantic search without coupling search infrastructure to `nhsuk-frontend`.

### Why I think this belongs at design-system level

The value would be consistency. Individual NHS services can already build their own language selectors and terminology helpers, but without a shared pattern those implementations can diverge in accessibility and behaviour.

I am **not** proposing that `nhsuk-frontend` itself becomes a translation platform, search engine or AI symptom checker.

### Possible first step

A small discovery could answer:

1. Are there existing NHS services with successful multilingual UI patterns that could be standardised?
2. Is a language-selector pattern in scope for this library?
3. Would a plain-language medical-term pattern be useful as guidance, a component, or a content standard?
4. What accessibility and user-research evidence would maintainers want before implementation?

If maintainers think this is in scope, I would be happy to help with a focused prototype and tests following the repository contribution standards.

---

**Author:** SHCHEGLOV NIKOLA  
**Target repository:** https://github.com/nhsuk/nhsuk-frontend/issues