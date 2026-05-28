# SignTraker API Client Docs

This directory is the canonical operating guide for the `signtraker` Python API
client planning set.

## Role

- This tree is docs-only. Runtime code lives under `signtraker/`, tests under
  `tests/`, docs site under `docs/`, automation under `.github/`.
- Runtime truth comes from checked-in code, not roadmap items alone.

## Interpretation Rules

- Planning complete is not the same as shipped.
- Readiness does not by itself prove runtime ownership.
- The active plan (`execution/api-client-bootstrap-plan.md`) may outrank the
  historical roadmap for the current seam.

## Current Status Snapshot

Snapshot date: `2026-05-28`

| Lens | Current answer |
| --- | --- |
| Planning foundation | Checked in (source audit complete) |
| Runtime feature or implementation truth | Full client implemented across all 8 resource groups |
| Highest-risk remaining surface | Live-API verification of error envelope, list container, merge-patch content type |

## Fastest Reality Check

- `foundation/api-source-of-truth.md`: the authoritative API contract and gaps.
- `execution/api-client-bootstrap-plan.md`: the canonical active build sequence.
- `execution/execution-plan.md`: the live checked-in ledger.

## Start Here

1. `foundation/api-source-of-truth.md`
2. `execution/api-client-bootstrap-plan.md`
3. `trackers/readiness-overview.md`
4. `execution/execution-plan.md`
5. `execution/roadmap.md` only for historical sequencing
6. `ARTIFACT_PATH_INDEX.md` for canonical paths

## Directory Guide

| Folder or file | Role | Open first when you need |
| --- | --- | --- |
| `foundation/` | Durable decisions and the API source of truth | Contract or policy questions |
| `trackers/` | Live readiness scoreboards | Current blockers |
| `execution/` | Execution navigation and ledger | Next implementation slice |
| `execution/api-client-bootstrap-plan.md` | Canonical active sequence | The current build |
| `ARTIFACT_PATH_INDEX.md` | Naming and path index | Canonical artifact homes |

## Document Precedence

1. `foundation/` wins for durable rules and the API contract.
2. The active plan doc wins for the current focused execution seam.
3. Focused trackers plus `execution/execution-plan.md` win for live status.
4. `execution/roadmap.md` is baseline sequencing, not the freshest status.
5. `ARTIFACT_PATH_INDEX.md` wins for exact paths and naming.

## Update Order

1. Relevant phase proof doc, if needed
2. Relevant focused tracker
3. `trackers/readiness-overview.md`
4. `execution/execution-plan.md`
5. Relevant `foundation/` doc, if durable rules changed
6. `README.md` or `ARTIFACT_PATH_INDEX.md` only if navigation or canonical paths changed

## Working Rules

- Keep this tree docs-only.
- Keep status language honest.
- Do not scatter related planning across multiple initiative roots.
