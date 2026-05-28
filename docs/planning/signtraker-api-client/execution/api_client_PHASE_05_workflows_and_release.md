# Phase 05 - Workflows And Release (Proof)

## Goal

Bring CI, release, docs deploy, security, and dependency automation into one
coherent baseline.

## Deliverables (checked in)

- `.github/workflows/ci.yml` (quality, test matrix, build)
- `.github/workflows/unified-deployment.yml` (version bump, PyPI, docs, release)
- `.github/workflows/security-audit.yml` (scheduled audit + remediation PR)
- `.github/workflows/docs.yml` (docs strict build/deploy)
- `.github/workflows/release.yml` (tag-driven publish)
- `.github/dependabot.yml` (pip root, docs pip, GitHub Actions)
- `MANIFEST.in`, `requirements.txt`, `requirements-dev.txt`

## Exit Criteria

- Met: workflows parse; version parity logic present between tag,
  `pyproject.toml`, and `__init__.py`.
