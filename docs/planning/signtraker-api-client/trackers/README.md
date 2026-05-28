# Trackers

Live readiness scoreboards for the `signtraker` client. Read these alongside
`../execution/execution-plan.md`.

## Read Order

1. `readiness-overview.md` for the aggregate picture.
2. The focused tracker for the surface you are touching.

## Focused Trackers

| Tracker | Covers |
| --- | --- |
| `endpoint-inventory-readiness.md` | Resource groups, endpoint coverage, model mapping, auth |
| `coverage-and-tests-readiness.md` | pytest setup, mocking, coverage |
| `docs-parity-readiness.md` | README, MkDocs nav, API pages, examples |
| `workflow-release-readiness.md` | CI, release, docs deploy, security, dependency automation |

## Grade Rules

- `complete`: the tracked slice is checked in.
- `in progress`: partially landed.
- `planned`: proposal only.
- `complete` never means "verified live against the API".

## Update Rule

Update the focused tracker first, then `readiness-overview.md`, then the
execution ledger.
