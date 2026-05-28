# ADR: Rules, Ownership, And Blueprint Deviations

## Status

Accepted (2026-05-28).

## Context

The client follows `API_CLIENT_BLUEPRINT.md`, but the SignTraker API has traits
the generic blueprint does not assume.

## Decisions

### Deviations from the blueprint

1. **Auth header value is prefixed.** The blueprint sets `{AUTH_HEADER}: {key}`.
   SignTraker requires `Authorization: ST-API {key}`. `BaseClient` builds the
   header value as `f"ST-API {api_key}"`.
2. **No universal base URL.** The host is tenant-specific
   (`https://{subdomain}.signtraker.com`). `BaseClient` resolves the host from,
   in order: explicit `base_url`, explicit `subdomain`, `SIGNTRAKER_BASE_URL`,
   `SIGNTRAKER_SUBDOMAIN`. If none resolve, it raises `SignTrakerConfigError`.
3. **OData querying.** A shared helper (`signtraker/_odata.py`) converts
   `filter/top/skip/orderby/select` keyword arguments into the `$`-prefixed
   query params and merges endpoint-specific params.
4. **Merge-patch.** `PATCH /api/agents/{id}` sends
   `Content-Type: application/merge-patch+json` (overridable) per the docs'
   "JSON Merge Patch" description.

### Ownership boundaries

- Runtime code: `signtraker/`.
- Tests: `tests/`.
- Docs site: `docs/` + `mkdocs.yml`.
- Examples: `examples/`.
- Automation: `.github/`.
- Planning (docs-only): `docs/planning/signtraker-api-client/`.
- Repo rules: `.cursor/rules/`.

### Rule files

Repo-local Cursor rules are generated under `.cursor/rules/`:
`styleguide.mdc`, `api-source-truth.mdc`, `api-client-implementation.mdc`,
`docs-tests-sync.mdc`, `release-quality-contract.mdc`.

## Consequences

- Constructors take both `base_url` and `subdomain`; documentation must explain
  precedence.
- Models use PascalCase aliases because the API uses PascalCase JSON keys.
