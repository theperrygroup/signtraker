# ADR: Package Identity And Versioning

## Status

Accepted (2026-05-28).

## Context

A new typed Python client for the SignTraker API is being created from the API
docs. The product is branded "SignTracker" but the API host domain is
`signtraker.com` (no second `c`).

## Decision

- Distribution and import package name: `signtraker` (matches the API host /
  brand domain). Chosen by the user.
- Aggregator client class: `SignTrakerClient`.
- Base exception: `SignTrakerError`.
- Environment variable prefix: `SIGNTRAKER_` (`SIGNTRAKER_API_KEY`,
  `SIGNTRAKER_BASE_URL`, `SIGNTRAKER_SUBDOMAIN`, `SIGNTRAKER_TIMEOUT_SECONDS`,
  `SIGNTRAKER_MAX_RETRIES`, `SIGNTRAKER_RETRY_BACKOFF_SECONDS`).
- Version is single-sourced in exactly two places that must match:
  `pyproject.toml` `[project].version` and `signtraker/__init__.py`
  `__version__`. Initial version `0.1.0`.
- Python support: `>=3.10` (the latest mypy no longer targets 3.9, and 3.9 is
  near end-of-life). Runtime deps: `requests`, `pydantic>=2`,
  `typing-extensions`. Optional `dotenv` extra.

## Consequences

- The release pipeline must verify both version locations match the tag.
- Because the host is tenant-specific, there is no hardcoded default base URL;
  see `rules-and-ownership-adr.md`.
