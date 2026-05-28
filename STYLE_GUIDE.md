# Code Style Guide

Conventions for the `signtraker` Python client. The companion prose/docs guide
is `docs/STYLE_GUIDE.md`.

## Language & Tooling

- Python `>=3.10`. Format with Black (line length 88) and isort (`black`
  profile). Lint with flake8. Type-check with `mypy --strict`.
- Run the full check set before committing:

```bash
black --check .
isort --check-only --profile=black --line-length=88 .
flake8 .
mypy signtraker/ --strict
pytest --cov=signtraker --cov-report=term-missing
```

## Docstrings & Types

- Google-style docstrings on every public class, method, and function, with
  `Args` / `Returns` / `Raises` sections.
- Full type hints on all parameters and return values.
- Do not add comments that merely restate the code.

## Naming

- `PascalCase` classes, `snake_case` functions/variables,
  `UPPER_SNAKE_CASE` constants, leading underscore for private members.
- One resource module + one client class per API group.

## Error Handling

- Catch transport exceptions at the transport layer (`base_client.py`).
- Map status codes to typed exceptions; never leak raw `requests` exceptions.

## Known API Quirks

- Auth header value is `Authorization: ST-API {api_key}` (note the `ST-API `
  prefix).
- The API host is tenant-specific (`https://{subdomain}.signtraker.com`); there
  is no universal default base URL.
- JSON keys are PascalCase (`Id`, `FirstName`); Pydantic models use aliases.
- `PATCH /api/agents/{id}` is a JSON Merge Patch
  (`Content-Type: application/merge-patch+json`).
- List endpoints' response container shape is unverified; methods return the
  raw parsed JSON.
