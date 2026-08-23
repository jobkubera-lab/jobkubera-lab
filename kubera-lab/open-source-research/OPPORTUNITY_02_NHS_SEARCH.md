# Opportunity 02 — NHS Search for People Who Do Not Know NHS Terminology

Target issue: https://github.com/nhsuk/nhsuk-service-manual/issues/2631

## Problem

The NHS Service Manual is actively investigating search, autocomplete, live filtering and select-with-search patterns. A common access problem is that people often know what they need in everyday language but do not know the official NHS service or clinical term.

## Research question

Can NHS search patterns better help a user move from plain everyday wording to the correct service or information category without turning the interface into a diagnostic system?

## Proposed KUBERA contribution

Create a UX/search research matrix using non-clinical examples such as:

- official service name vs everyday wording;
- spelling errors;
- abbreviations;
- non-native-English phrasing;
- transliterated terms;
- autocomplete accessibility with keyboard and screen readers;
- no-JavaScript fallback;
- safe wording when confidence is low.

## Safety boundary

This work is about navigation and information retrieval, not diagnosis or treatment recommendations.

## Safe next step

Study the existing search-pattern work in issue #2631, prepare a short evidence-backed comment that adds a distinct limited-English/plain-language perspective, and only propose implementation after maintainer feedback.
