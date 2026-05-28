# Workflow And Release Readiness

Snapshot date: `2026-05-28`

## Surfaces

| Surface | Status |
| --- | --- |
| `.github/workflows/ci.yml` | complete |
| `.github/workflows/unified-deployment.yml` | complete |
| `.github/workflows/security-audit.yml` | complete |
| `.github/workflows/docs.yml` | complete |
| `.github/workflows/release.yml` | complete |
| `.github/dependabot.yml` | complete |

## Quality Gates In CI

- Black, isort, flake8, mypy --strict, pytest + coverage, build, twine check,
  `mkdocs build --strict`.

## Version Parity

- `pyproject.toml` and `signtraker/__init__.py` must match the release tag.

## Release

- PyPI publish via API token. Status: ready (publish is gated on explicit
  go-ahead).
