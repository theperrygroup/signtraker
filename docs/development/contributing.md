# Contributing

## Set up

```bash
git clone https://github.com/theperrygroup/signtraker.git
cd signtraker
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pip install -r docs/requirements.txt
```

## Quality checks

Run the full set before opening a pull request:

```bash
black --check --diff --line-length=88 .
isort --check-only --diff --profile=black --line-length=88 .
flake8 .
mypy signtraker/ --strict
pytest --cov=signtraker --cov-report=term-missing
mkdocs build --strict
```

## Conventions

- Google-style docstrings and full type hints on all public code.
- One resource module + one client class per API group.
- Keep code, tests, docs, and examples in sync within the same change.
- Read the root [`STYLE_GUIDE.md`](https://github.com/theperrygroup/signtraker/blob/main/STYLE_GUIDE.md)
  and the [Style Guide](style-guide.md) page before contributing.

## Tests

- Unit tests mock HTTP with the `responses` library; no network calls.
- Live tests are marked `live` and skipped unless a real key is set:

```bash
SIGNTRAKER_API_KEY=... SIGNTRAKER_SUBDOMAIN=theperrygroup pytest -m live
```

## Source of truth

The API contract and known gaps are tracked under
`docs/planning/signtraker-api-client/foundation/`. Update those docs when API
behavior changes.
