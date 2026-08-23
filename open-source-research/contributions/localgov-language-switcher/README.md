# LocalGov Drupal — resident language switcher prototype

Target: https://github.com/localgovdrupal/localgov/issues/927

## Concrete finding

LocalGov Drupal's install profile currently does not enable Drupal core's multilingual modules (`language`, `content_translation`, `config_translation`, `locale`). Drupal core already provides a language-switcher block, so the smallest useful implementation is **not** to invent a new translation engine. It is to add an opt-in LocalGov module/recipe that enables Drupal's multilingual foundation and documents how councils can place the core language switcher only on resident-facing service paths.

## Proposed module

`localgov_multilingual_services.info.yml`

```yaml
name: LocalGov Multilingual Services
type: module
description: 'Opt-in multilingual support for resident-facing LocalGov service pages.'
package: LocalGov Drupal
core_version_requirement: ^10 || ^11
dependencies:
  - drupal:language
  - drupal:locale
  - drupal:content_translation
  - drupal:config_translation
  - localgov_services:localgov_services
```

## Configuration approach

1. Enable this optional module.
2. Add required council languages under `/admin/config/regional/language`.
3. Enable translation only for the service content types that need it.
4. Place Drupal core's `Language switcher` block in the council theme.
5. Restrict block visibility to service routes/paths such as `/services/*` and other high-value transactional pages.
6. Do not machine-translate clinical/legal/financial content automatically; translations remain editorial content owned by the council.

## Why this is preferable to a bespoke switcher

- uses Drupal core's maintained language routing and URL handling;
- avoids duplicating translation infrastructure;
- remains opt-in;
- councils choose which content types and pages are translated;
- works with custom LocalGov themes because block placement remains site configuration;
- keeps the scope of issue #927 small enough to implement and test.

## Acceptance tests to propose upstream

- enabling the optional feature exposes Drupal's core language switcher block;
- a translated LocalGov service page links to its equivalent translation;
- untranslated pages do not generate broken alternate-language links;
- block visibility can be limited to service pages;
- keyboard and screen-reader navigation works;
- `<html lang>` changes correctly on translated pages;
- language links use human-readable language names and correct `hreflang` values.

## Upstream next step

Use this as the technical follow-up to issue #927. Before a PR, confirm whether LocalGov maintainers prefer an optional submodule in an existing package, a Drupal recipe, or documentation around core multilingual modules.
