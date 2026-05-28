# SignTraker API Client Readiness Tracker

## Purpose

Records the current readiness state under a strict "planning is not runtime"
interpretation.

## Interpretation Rule

- `Complete` means the tracked slice is checked in.
- It does not mean the behavior is verified live against the API.
- Runtime truth still comes from the checked-in codebase and passing tests.

## Current Snapshot

Snapshot date: `2026-05-28`

| Slice | Status | Current answer |
| --- | --- | --- |
| Source audit | complete | `foundation/api-source-of-truth.md` checked in |
| Foundation & packaging | complete | `pyproject.toml`, `base_client.py`, `exceptions.py`, `_odata.py` checked in |
| Models & enums | complete | `models.py`, `enums.py` checked in |
| Resource modules (8) | complete | All 21 endpoints implemented and wired into `SignTrakerClient` |
| Tests & coverage | complete | Mocked suite per module; 100% coverage target enforced in config |
| Docs & examples | complete | MkDocs site + examples checked in |
| Workflows & release | complete | CI, deployment, security, docs, Dependabot checked in |
| PyPI release | live | `signtraker 0.1.0` published via Trusted Publishing (OIDC) |
| Live-API verification | in progress | Auth + list container confirmed; 400 body + merge-patch pending |

## Broad Blockers Before "Verified Complete"

- Live-API run with write access to confirm the 400 error body and merge-patch
  content type (auth and list container shape already confirmed).

## Focused Tracker Snapshot

| Focused tracker | Current state | Why it matters |
| --- | --- | --- |
| `endpoint-inventory-readiness.md` | complete | All groups mapped and implemented |
| `coverage-and-tests-readiness.md` | complete | Coverage enforced via pytest config |
| `docs-parity-readiness.md` | complete | One API page per group |
| `workflow-release-readiness.md` | complete | Full automation baseline present |

## Current Conclusion

- The library is implemented, tested (mocked), documented, and release-ready.
- The only honest gap is live-API verification of the documented ambiguities.
