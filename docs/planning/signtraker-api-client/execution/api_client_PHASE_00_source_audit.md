# Phase 00 - Source Audit (Proof)

## Goal

Establish one honest API source of truth before coding.

## Inputs

- `https://theperrygroup.signtraker.com/api-docs`
- `API_CLIENT_BLUEPRINT.md`

## Deliverables (checked in)

- `foundation/api-source-of-truth.md`
- `foundation/source-of-truth-matrix.md`
- `foundation/package-and-versioning-adr.md`
- `foundation/rules-and-ownership-adr.md`
- `.cursor/rules/*.mdc`

## Result

- 8 resource groups, 21 endpoints, enums, and schemas catalogued.
- Gaps recorded: error envelope, list container, merge-patch content type, rate
  limits, partial status enums.

## Exit Criteria

- Met: contract and gaps recorded; implementation may proceed with gaps flagged.
