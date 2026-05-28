# Phase 06 - Parity Audit (Proof)

## Goal

Compare the repo against the intended baseline and record remaining gaps.

## Validation Session

- `black --check`, `isort --check-only --profile=black`
- `flake8`
- `mypy signtraker/ --strict`
- `pytest --cov=signtraker --cov-report=term-missing`
- `mkdocs build --strict`
- `python -m build`, `twine check dist/*`

## Outcome (2026-05-28)

All gates passed locally on Python 3.13:

- `black --check` and `isort --check-only`: clean.
- `flake8`: 0 issues (max-complexity 10).
- `mypy signtraker/ --strict`: success, 15 source files.
- `pytest -m "not live"`: 106 passed, 100% coverage (526 statements, 0 missed).
- `mkdocs build --strict`: success.
- `python -m build` + `twine check dist/*`: both PASSED; wheel ships `py.typed`.
- Live read-only checks: `ST-API` auth accepted; list endpoints return bare
  arrays; 404 returns an empty body mapped to `NotFoundError`.

Gap map: 400 error-body shape and merge-patch content type remain unverified
live (would require write access / sample data).

## Deferred (explicit)

- Live integration verification against a real tenant + key.
- PyPI publish of `0.1.0` (gated on explicit go-ahead).
