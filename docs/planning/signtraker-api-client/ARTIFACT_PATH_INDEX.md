# SignTraker API Client Artifact Path Index

## Purpose

- This file is the canonical naming and path index for the planning set.
- This file is not the current-status ledger.
- Future prompts should use this file instead of hardcoded path assumptions.

## Canonical Role Index

### Planning Root

- Actual repo path: `docs/planning/signtraker-api-client/`
- Already exists: `YES`
- Canonical for future prompts: `YES`
- Confidence: `High`

### Landing README

- Actual repo path: `docs/planning/signtraker-api-client/README.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### Artifact Path Index

- Actual repo path: `docs/planning/signtraker-api-client/ARTIFACT_PATH_INDEX.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### API Source Of Truth

- Actual repo path: `docs/planning/signtraker-api-client/foundation/api-source-of-truth.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### Master Readiness Tracker

- Actual repo path: `docs/planning/signtraker-api-client/trackers/readiness-overview.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### Execution Plan (live ledger)

- Actual repo path: `docs/planning/signtraker-api-client/execution/execution-plan.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### Active Plan

- Actual repo path: `docs/planning/signtraker-api-client/execution/api-client-bootstrap-plan.md`
- Already exists: `YES`
- Canonical for future prompts: `YES`

### Phase Proof Files

- Actual repo path: `docs/planning/signtraker-api-client/execution/api_client_PHASE_##_<slug>.md`
- Already exists: `YES` (phases 00-06)
- Canonical for future prompts: `YES`

## Runtime Artifact Homes

- Import package: `signtraker/`
- Tests: `tests/`
- Docs site: `docs/` with config `mkdocs.yml`
- Examples: `examples/`
- Repo rules: `.cursor/rules/`
- Workflows: `.github/workflows/`
- Dependency automation: `.github/dependabot.yml`
- Package metadata + version source 1: `pyproject.toml`
- Version source 2: `signtraker/__init__.py`
- Requirements mirrors: `requirements.txt`, `requirements-dev.txt`, `docs/requirements.txt`

## Directory Structure

```text
docs/planning/signtraker-api-client/
  README.md
  ARTIFACT_PATH_INDEX.md
  foundation/
  trackers/
  execution/
```
