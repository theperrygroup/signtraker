# Execution Docs

This folder holds the ordered plan and the checked-in ledger for the
`signtraker` client.

Read this alongside:

- `../trackers/README.md`
- `../trackers/readiness-overview.md`
- `../foundation/api-source-of-truth.md`

## File Roles

| File type | Use it for | Not for |
| --- | --- | --- |
| `execution-plan.md` | Live checked-in ledger, blockers, completed proof | Historical baseline sequencing |
| `api-client-bootstrap-plan.md` | Canonical current build sequence | Replacing the ledger |
| `roadmap.md` | Baseline dependency order and historical context | Freshest status snapshot |
| `api_client_PHASE_##_<slug>.md` | Durable proof for one explicit phase | Replacing the aggregate ledger |

## Fastest Answers

| Question | Open first |
| --- | --- |
| What is the latest checked-in status? | `../trackers/readiness-overview.md`, then `execution-plan.md` |
| What is the current active sequence? | `api-client-bootstrap-plan.md` |
| What is the baseline task order? | `roadmap.md` |
| Where should future proof files go? | `../ARTIFACT_PATH_INDEX.md` |

## Rules

- Treat `api-client-bootstrap-plan.md` as canonical for the current seam.
- Let focused trackers plus `readiness-overview.md` define current readiness.
- Edit `roadmap.md` only when the baseline sequence changes.
- Do not use `roadmap.md` as the current-status document.
