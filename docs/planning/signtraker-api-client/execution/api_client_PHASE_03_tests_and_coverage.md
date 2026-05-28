# Phase 03 - Tests And Coverage (Proof)

## Goal

Define a full test harness and honest coverage story.

## Deliverables (checked in)

- `tests/conftest.py` (client fixtures with dummy key + subdomain)
- `tests/test_base_client.py`, `tests/test_client.py`,
  `tests/test_exceptions.py`, `tests/test_models.py`, `tests/test_odata.py`
- One `tests/test_<resource>.py` per resource group
- `tests/test_live_agents.py` (opt-in; skipped without a real key)

## Coverage

- `--cov=signtraker --cov-report=term-missing` configured in `pyproject.toml`.
- Target 100%; CI proves it on the matrix.

## Exit Criteria

- Met: full mocked suite passes locally.
