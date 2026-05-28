# Deployment

Releases are automated with GitHub Actions.

## Versioning

The version is single-sourced in two places that must match:

- `pyproject.toml` `[project].version`
- `signtraker/__init__.py` `__version__`

The release pipeline verifies both match the git tag.

## Release flow

1. Bump the version in both locations (or use the workflow's version-bump input).
2. Commit and tag `vX.Y.Z`.
3. Pushing the tag triggers `release.yml` / `unified-deployment.yml`, which:
   - runs quality checks, tests, and the package build;
   - publishes to PyPI via the `pypa/gh-action-pypi-publish` action; and
   - builds and deploys the documentation to GitHub Pages.

## Manual build

```bash
python -m build
twine check dist/*
```

## Docs

```bash
mkdocs build --strict
mkdocs gh-deploy   # publish to GitHub Pages
```
