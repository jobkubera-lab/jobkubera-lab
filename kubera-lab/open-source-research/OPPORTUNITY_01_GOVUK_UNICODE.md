# Opportunity 01 — GOV.UK Unicode / Character Count

Target issue: https://github.com/alphagov/govuk-frontend/issues/1104

## Problem

The GOV.UK character-count component historically counts JavaScript code units rather than user-perceived characters. This produces confusing counts for emoji, combining marks and some international text.

## Why this is a good contribution target

- the issue is already open, so we are not creating noise;
- it is concrete and testable;
- it sits at the intersection of accessibility and internationalisation;
- a contribution can begin with evidence/tests rather than a risky rewrite.

## Proposed KUBERA contribution

Prepare a multilingual grapheme test matrix covering:

- ASCII English;
- Ukrainian/Cyrillic;
- combining diacritics;
- emoji with skin-tone modifiers;
- emoji with zero-width joiners;
- Arabic text;
- Japanese text;
- newline behaviour.

For each case record:
- source string;
- JavaScript `.length`;
- user-perceived grapheme count;
- expected component behaviour;
- possible backend-validation mismatch.

## Technical direction to investigate

`Intl.Segmenter` can segment grapheme clusters in modern JavaScript, but any proposal must consider browser support and consistency with server-side validation.

## Safe next step

Do not promise a fix yet. First produce the test matrix and, if strong, add it as evidence to the existing issue. A small test PR can follow if maintainers confirm the direction.
