# Phase 02 - Endpoint Inventory And Models (Proof)

## Goal

Map the API surface onto modules, clients, and models.

## Deliverables (checked in)

- `signtraker/enums.py` (`PaymentMode`, `DiscountLevel`, `CountryCode`,
  `AwardRestriction`, `SortDirection`)
- `signtraker/models.py` (Pydantic v2 models with PascalCase aliases)
- Resource modules: `agents.py`, `change_orders.py`, `credits.py`,
  `enterprises.py`, `offices.py`, `order_presets.py`, `orders.py`, `services.py`
- `signtraker/client.py` (lazy cached sub-client properties)
- `signtraker/__init__.py` exports + `__all__`

## Coverage

- 21 endpoints across 8 groups reachable via `SignTrakerClient`.

## Exit Criteria

- Met: all endpoints callable; models round-trip PascalCase JSON.
