# Five ready upstream contributions

This directory contains concrete, reviewable fixes prepared for five UK public-service open-source targets.

| Target | Concrete fix | State |
|---|---|---|
| LocalGov Drupal | Opt-in multilingual-services implementation using Drupal core language modules and language-switcher block | Prototype/spec ready; follows issue #927 |
| GOV.UK Frontend | Count grapheme clusters instead of UTF-16 code units in Character Count | Production patch ready; test adaptation still needed upstream |
| NHS Service Manual | Add pre-upload file-type hint guidance and fix malformed HTML | Patch ready; directly matches issue #2497 |
| NHS England leaflet-geomaps-NHS | Remove tracked `.Rhistory` / `.Rproj.user` and add standard R `.gitignore` | Patch ready |
| NHS Digital Website Design System | Fix README typos and replace obsolete `master` release branch with actual `main` | Patch ready |

## Submission order

1. **NHS Service Manual** — strongest first contribution: existing issue, tiny patch, accessibility benefit.
2. **NHS Digital Website Design System** — tiny documentation fix, very low risk.
3. **NHS England leaflet-geomaps-NHS** — clean repository hygiene fix, but repository is less active.
4. **GOV.UK Frontend** — technically valuable but requires adapting the regression test to existing test fixtures and maintainers may want a compatibility decision before merge.
5. **LocalGov Drupal** — continue issue #927 with this implementation direction; get maintainer agreement on module vs recipe before coding against their package structure.

## Important

These files are not claims of accepted upstream contributions. They are contribution-ready patches/prototypes prepared from current upstream code. A contribution becomes external only after it is submitted to the upstream project's issue/PR workflow and accepted or discussed there.
