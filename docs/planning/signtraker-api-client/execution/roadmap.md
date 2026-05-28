# SignTraker API Client Task Roadmap

This roadmap converts the initiative into a phased, dependency-aware task plan.

Treat this file as the baseline dependency map. For the freshest checked-in
status, use `execution-plan.md` plus the focused trackers.

## Scope And Evidence

- Source references:
  - `https://theperrygroup.signtraker.com/api-docs`
  - `API_CLIENT_BLUEPRINT.md`
- Primary code anchors:
  - `signtraker/base_client.py`, `signtraker/client.py`, resource modules.
- Historical blockers at roadmap creation:
  - Undocumented error envelope and list container shape.

## Harsh Sequencing Rule

- Do not implement resource modules before `base_client.py` auth + base-URL
  resolution exist. Do not claim coverage before tests pass.

## Phase 0 - Source Audit

### P0-001 - Capture API contract
- Why: one honest source of truth before coding.
- Files: `foundation/api-source-of-truth.md`, `foundation/source-of-truth-matrix.md`.
- Dependency prerequisites: none.
- Severity: high.
- Feature domain: planning.
- Type: `DOCS-ONLY`.
- Acceptance criteria: all groups, enums, and gaps recorded.

## Phase 1 - Foundation And Packaging

### P1-001 - Transport and packaging
- Why: every resource client subclasses the transport layer.
- Files: `pyproject.toml`, `signtraker/base_client.py`, `signtraker/exceptions.py`,
  `signtraker/_odata.py`, `signtraker/__init__.py`, `signtraker/py.typed`.
- Dependency prerequisites: P0-001.
- Severity: high.
- Type: implementation.
- Acceptance criteria: client constructs; auth header and base-URL resolution
  behave; status codes map to typed errors.

## Phase 2 - Endpoint Inventory And Models

### P2-001 - Models and enums
- Files: `signtraker/models.py`, `signtraker/enums.py`.
- Dependency prerequisites: P1-001.
- Type: implementation.
- Acceptance criteria: models round-trip PascalCase JSON.

### P2-002 - Resource modules and aggregator
- Files: 8 resource modules + `signtraker/client.py`.
- Dependency prerequisites: P2-001.
- Type: implementation.
- Acceptance criteria: all 21 endpoints reachable via `SignTrakerClient`.

## Phase 3 - Tests And Coverage

### P3-001 - Mocked test suite
- Files: `tests/`.
- Dependency prerequisites: P2-002.
- Type: implementation.
- Acceptance criteria: suite passes; coverage at target.

## Phase 4 - Docs And Examples

### P4-001 - MkDocs site and examples
- Files: `mkdocs.yml`, `docs/`, `examples/`.
- Dependency prerequisites: P2-002.
- Type: implementation.
- Acceptance criteria: `mkdocs build --strict` passes.

## Phase 5 - Workflows And Release

### P5-001 - Automation
- Files: `.github/workflows/*`, `.github/dependabot.yml`.
- Dependency prerequisites: P3-001, P4-001.
- Type: implementation.
- Acceptance criteria: workflows parse; version parity enforced.

## Phase 6 - Parity Audit

### P6-001 - Validation and release readiness
- Files: trackers + ledger.
- Dependency prerequisites: all above.
- Type: mixed.
- Acceptance criteria: validation session green.
