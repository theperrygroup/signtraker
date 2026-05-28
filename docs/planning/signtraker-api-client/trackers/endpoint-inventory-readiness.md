# Endpoint Inventory Readiness

Snapshot date: `2026-05-28`

## Auth Understanding

- `Authorization: ST-API {key}` header. Status: complete.

## Resource Coverage

| Group | Module | Endpoints | Status |
| --- | --- | --- | --- |
| Agents | `signtraker/agents.py` | list, create, get, update, activate, deactivate | complete |
| Change Orders | `signtraker/change_orders.py` | list, create, get | complete |
| Credits | `signtraker/credits.py` | list awards, create award | complete |
| Enterprise | `signtraker/enterprises.py` | list | complete |
| Office | `signtraker/offices.py` | list | complete |
| Order Presets | `signtraker/order_presets.py` | list | complete |
| Orders | `signtraker/orders.py` | list, create, get, request removal | complete |
| Services | `signtraker/services.py` | list, create, get | complete |

## Model Mapping

- Shared `NamedRef` and per-domain models in `signtraker/models.py`. Status:
  complete (PascalCase aliases, Pydantic v2).

## Gaps

- List response container shape unverified (see source-of-truth gap 2).
