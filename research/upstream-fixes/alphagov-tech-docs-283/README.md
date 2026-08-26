# alphagov/tech-docs-gem issue #283

Upstream issue: https://github.com/alphagov/tech-docs-gem/issues/283

## Verified current bug

The issue is still valid on the current `main` branch.

`GovukTechDocs::SourceUrls#report_issue_url` reads the custom URL from:

```ruby
config[:source_urls]&.[](:report_issue_url)
```

but project configuration from `config/tech-docs.yaml` is nested under `config[:tech_docs]`.

The existing spec also configures the legacy top-level `config[:source_urls]`, so it only verifies the workaround rather than the documented YAML path.

## Minimal compatible fix

Read the documented nested value first and preserve the existing top-level value as a fallback:

```ruby
url = config[:tech_docs][:source_urls]&.[](:report_issue_url) ||
      config[:source_urls]&.[](:report_issue_url)
```

This avoids a breaking change for projects that already use the historical workaround in `config.rb`.

## Tests required

1. custom `report_issue_url` under `config[:tech_docs][:source_urls]` is used;
2. legacy top-level `config[:source_urls]` still works;
3. documented YAML value wins when both are set;
4. default GitHub issue URL still works when neither is configured.

## Proposed upstream PR title

`Fix report_issue_url configuration from tech-docs.yaml`

## Scope

This is deliberately a small bug fix. It does not change URL query parameters or contribution-banner behaviour beyond reading configuration from the documented location while retaining backward compatibility.
