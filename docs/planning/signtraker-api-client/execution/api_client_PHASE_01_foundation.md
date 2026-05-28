# Phase 01 - Foundation And Packaging (Proof)

## Goal

Make package identity, metadata, and runtime primitives coherent.

## Deliverables (checked in)

- `pyproject.toml` (PEP 621 metadata, deps, tool config, `py.typed` data)
- `signtraker/__init__.py` (`__version__`, public exports)
- `signtraker/exceptions.py` (`SignTrakerError` hierarchy + `SignTrakerConfigError`)
- `signtraker/base_client.py` (ST-API auth, base-URL/subdomain resolution,
  retries, verb helpers, `_handle_response`, recursive error extractor)
- `signtraker/_odata.py` (OData query param builder)
- `signtraker/py.typed`
- `.gitignore`

## Settled Questions

- Package name `signtraker`; version single-sourced in `pyproject.toml` and
  `__init__.py`.
- Auth header value `ST-API {key}`.
- Base URL resolved from `base_url` / `subdomain` / env; else
  `SignTrakerConfigError`.

## Exit Criteria

- Met: package imports; transport, auth, and error mapping behave under tests.
