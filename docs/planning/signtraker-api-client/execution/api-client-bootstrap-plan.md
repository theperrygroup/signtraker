# API Client Bootstrap Plan

## Goal

- Recreate a typed Python API client baseline for the SignTraker API from the
  available API docs, covering all 8 resource groups.

## Current Focus

- Phase 6 - Parity audit and release readiness.

## Ordered Phases

### Phase 0 - Source Audit
- Inputs: SignTraker API docs URL, API_CLIENT_BLUEPRINT.md.
- Deliverables: planning tree, `foundation/api-source-of-truth.md`,
  `foundation/source-of-truth-matrix.md`, repo rules.
- Exit criteria: contract and gaps recorded.

### Phase 1 - Foundation And Packaging
- Inputs: source audit, blueprint sections 4-5, 11.
- Deliverables: `pyproject.toml`, `signtraker/__init__.py`, `exceptions.py`,
  `base_client.py`, `_odata.py`, `py.typed`, `.gitignore`.
- Exit criteria: package imports; auth + base-URL resolution + error mapping
  work.

### Phase 2 - Endpoint Inventory And Models
- Inputs: endpoint inventory, schemas, enums.
- Deliverables: `enums.py`, `models.py`, 8 resource modules, `client.py`
  wiring, `__init__.py` exports.
- Exit criteria: all 21 endpoints callable through `SignTrakerClient`.

### Phase 3 - Tests And Coverage
- Inputs: implemented modules.
- Deliverables: mocked tests per module + base/client/exceptions/models/odata,
  opt-in live tests.
- Exit criteria: full suite passes; coverage at target.

### Phase 4 - Docs And Examples
- Inputs: implemented API surface.
- Deliverables: MkDocs site, API page per group, getting-started, guides,
  reference, development, examples.
- Exit criteria: `mkdocs build --strict` passes.

### Phase 5 - Workflows And Release
- Inputs: package + docs.
- Deliverables: CI, deployment, security, docs, release workflows; Dependabot.
- Exit criteria: workflows parse; version parity logic present.

### Phase 6 - Parity Audit
- Inputs: everything above.
- Deliverables: full local validation session, refreshed trackers/ledger.
- Exit criteria: validation green; release gated on explicit go-ahead.
