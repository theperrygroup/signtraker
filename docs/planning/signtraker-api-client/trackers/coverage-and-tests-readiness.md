# Coverage And Tests Readiness

Snapshot date: `2026-05-28`

## Harness

- Framework: `pytest`. HTTP mocking: `responses`. Status: complete.
- Fixtures: `tests/conftest.py` builds clients with a dummy key + subdomain.

## Suites

| Suite | Status |
| --- | --- |
| `test_base_client.py` | complete |
| `test_client.py` | complete |
| `test_exceptions.py` | complete |
| `test_models.py` | complete |
| `test_odata.py` | complete |
| `test_<resource>.py` (8) | complete |
| `test_live_*.py` (opt-in) | complete (skipped without real key) |

## Coverage

- Verified 100% locally on Python 3.13: 526 statements, 0 missed, 106 tests
  passing (`pytest -m "not live"`).
- Enforced via `--cov` in `pyproject.toml`; CI re-proves it on the 3.10-3.13
  matrix.
