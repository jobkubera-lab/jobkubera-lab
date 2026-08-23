# KUBERA Open Source Research

A public research portfolio for identifying real problems in serious open-source public-service projects, analysing existing work, proposing useful improvements and tracking external contributions.

## Method

We do not spam maintainers with generic ideas.

For each target:
1. inspect the repository and active work;
2. search existing issues and PRs;
3. identify an evidence-backed gap;
4. decide whether to open a new issue, join an existing issue, or prepare a prototype/PR;
5. record the result publicly.

---

# Current research targets

## 1. LocalGov Drupal

Repository: https://github.com/localgovdrupal/localgov

### Status
Active target. First external proposal published.

### Existing KUBERA contribution
**Issue #927 — Feature request: language switcher for resident-facing service pages**  
https://github.com/localgovdrupal/localgov/issues/927

The proposal focuses on opt-in multilingual access for high-value resident-facing service and transactional pages rather than attempting to translate an entire council website.

### Next research
- investigate Drupal multilingual/content-translation capabilities already available to LocalGov deployments;
- identify where a lightweight language navigation module would belong;
- define accessibility, fallback-language and content-governance requirements;
- prepare a minimal non-production prototype only if maintainers show interest.

**Priority: HIGH**

---

## 2. GOV.UK / GDS — GOV.UK Frontend

Repository: https://github.com/alphagov/govuk-frontend

### Finding
Do **not** open another generic language-switcher issue. GOV.UK is already actively working on language navigation and RTL support.

Relevant active work:
- Language switcher final review — https://github.com/alphagov/govuk-frontend/issues/7320
- RTL support for Details — https://github.com/alphagov/govuk-frontend/issues/7303
- Language-switcher alignment options — https://github.com/alphagov/govuk-frontend/issues/7245
- Localisation of summary-list action text — https://github.com/alphagov/govuk-frontend/issues/2649
- Localisation of error-message content order — https://github.com/alphagov/govuk-frontend/issues/2650
- Unicode/grapheme character counting — https://github.com/alphagov/govuk-frontend/issues/1104

### Best KUBERA opportunity
**Internationalisation edge-case research pack.**

Instead of proposing a duplicate feature, contribute test cases and analysis for:
- Ukrainian/Cyrillic input;
- Arabic/RTL layouts;
- Chinese/Japanese punctuation and spacing;
- emoji and combined Unicode graphemes;
- translated visually-hidden accessibility text.

Potential deliverable: a compact cross-language test matrix linked to existing issues, followed by targeted tests or documentation PRs.

**Priority: VERY HIGH** — strongest route to a credible external contribution because real open issues already exist.

---

## 3. NHS Service Manual / NHS.UK Design System

Repository: https://github.com/nhsuk/nhsuk-service-manual

### Finding
The project has substantial active work around accessibility, inclusive design and search. A generic accessibility suggestion would be redundant.

Relevant active work:
- Search/autocomplete/filter patterns — https://github.com/nhsuk/nhsuk-service-manual/issues/2631
- Accessibility retesting — https://github.com/nhsuk/nhsuk-service-manual/issues/2637
- Accessibility guidance review — https://github.com/nhsuk/nhsuk-service-manual/issues/1948
- Inclusive design guidance — https://github.com/nhsuk/nhsuk-service-manual/issues/1079
- Making accessibility checklist easier to use — https://github.com/nhsuk/nhsuk-service-manual/issues/2067
- Accessibility of Dragon voice-control interaction — https://github.com/nhsuk/nhsuk-service-manual/issues/2039

### Best KUBERA opportunities

#### A. Search patterns for users who do not know NHS terminology
Research how autocomplete/search suggestions behave when a resident uses everyday language instead of NHS/clinical terminology.

Example research question:
> Can search patterns help a user who knows the problem but not the official service name reach the correct NHS service without creating unsafe medical inference?

This should remain an information-retrieval/UX proposal, **not medical diagnosis**.

#### B. Inclusive-design evidence for limited-English users
Before opening a new issue, prepare evidence showing whether current inclusive-design guidance sufficiently covers limited-English proficiency, interpreters, translated content and language selection. If a real gap remains, propose a narrow guidance addition.

**Priority: VERY HIGH**

---

## 4. NHS England

Organisation: https://github.com/nhsengland

### Finding
NHS England has many repositories, so treating the whole organisation as one project is too broad. We need to enter through specific repos where KUBERA has relevant experience.

Candidate repository:
- `leaflet-geomaps-NHS` — https://github.com/nhsengland/leaflet-geomaps-NHS

It demonstrates NHS geographic mapping with Leaflet. It currently has no open issues and has seen little recent code activity, so it is **not a good place to send a cold feature request now**.

### Better KUBERA approach
Create an independent research/prototype case study around accessible public-service mapping:
- keyboard-accessible map alternatives;
- list view synchronized with map results;
- plain-language location descriptions;
- multilingual place/service labels;
- evidence/source metadata for service locations;
- fallback when maps cannot be used.

Then use the prototype as evidence when a genuinely active NHS mapping/geospatial repository or team appears.

**Priority: MEDIUM** — research first, outreach later.

---

## 5. NHS Digital Website Design System

Repository: https://github.com/NHS-digital-website/design-system

### Finding
The repository describes accessible UI code for NHS Digital sites, but currently has **0 open issues** and its last recorded push was in December 2024. That makes it a poor target for unsolicited feature proposals in 2026.

### Decision
Do not spend reputation capital opening speculative issues here yet.

Instead:
- study reusable accessibility patterns;
- compare it with the actively maintained `nhsuk/nhsuk-service-manual` work;
- direct new contributions to the active NHS.UK design-system community unless this repository becomes active again.

**Priority: LOW / WATCH**

---

# Shortlist: strongest contribution opportunities

| Rank | Target | Contribution idea | Action |
|---|---|---|---|
| 1 | GOV.UK Frontend | Unicode/grapheme test cases for character count | Join issue #1104 with evidence/tests |
| 2 | GOV.UK Frontend | Cross-language localisation test matrix | Join #2649/#2650 and related language-navigation work |
| 3 | NHS Service Manual | Search for users who do not know official NHS terminology | Research against #2631 before commenting |
| 4 | NHS Service Manual | Limited-English inclusion gap analysis | Audit current inclusive-design guidance before opening anything |
| 5 | LocalGov Drupal | Resident-facing language navigation | Track and develop issue #927 |
| 6 | LocalGov Drupal | Accessibility + translation fallback specification | Add only after maintainer response / research |
| 7 | NHS England | Accessible geospatial service-discovery prototype | Build independent case study first |

# Outreach doctrine

We do not approach maintainers with “we sell AI services”.

Our sequence is:

**Research → evidence → useful issue/comment → prototype/test → PR → relationship → possible collaboration.**

Commercial credibility is a consequence of useful public work, not the opening line.

# Success metrics

Track:
- external issues opened after duplicate checking;
- meaningful maintainer replies;
- comments that add evidence to existing issues;
- prototypes referenced by maintainers;
- PRs opened;
- PRs merged;
- accepted documentation/research contributions;
- recurring relationships with maintainers or public-service teams.

# Current external record

- LocalGov Drupal issue #927: OPEN — https://github.com/localgovdrupal/localgov/issues/927

This portfolio should be updated as external discussions progress.
