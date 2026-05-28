# Foundation Docs

Durable rules and the API contract for the `signtraker` client. These outrank
trackers and execution notes.

## Files

| File | Role |
| --- | --- |
| `api-source-of-truth.md` | Authoritative API contract, endpoint inventory, and gaps |
| `source-of-truth-matrix.md` | Per-topic canonical vs secondary source and confidence |
| `package-and-versioning-adr.md` | Package identity, naming, and version source-of-truth decisions |
| `rules-and-ownership-adr.md` | Repo rules, ownership boundaries, and deviations from the blueprint |

## Rule

Before implementing or changing API behavior, read `api-source-of-truth.md` and
`source-of-truth-matrix.md`. If sources disagree, prefer the higher-precedence
source and record the contradiction here before coding.
