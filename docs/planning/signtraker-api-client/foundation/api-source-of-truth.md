# API Source Of Truth

## Source Priority

1. Explicit API docs URL from the user:
   `https://theperrygroup.signtraker.com/api-docs`
2. (none checked in: no local `docs/api/`, OpenAPI, or Swagger artifacts)

## Inputs Used

| Source | Path or URL | Status | Why it matters |
| --- | --- | --- | --- |
| SignTraker API docs page | `https://theperrygroup.signtraker.com/api-docs` | Used | Only authoritative contract available |
| API_CLIENT_BLUEPRINT.md | `API_CLIENT_BLUEPRINT.md` | Used | Architecture and coding standards baseline |

## Base Contract

| Area | Current answer | Canonical source |
| --- | --- | --- |
| Base URL | Tenant-specific: `https://{subdomain}.signtraker.com` (example tenant `theperrygroup`); API paths under `/api` | Docs "API SERVER" + endpoint paths |
| Authentication | API key in header `Authorization: ST-API {api_key}` | Docs "API Key Authentication" / "JSON Data Format" |
| Transport | HTTPS required; JSON request/response | Docs "Security" / "JSON Data Format" |
| Versioning | `SignTraker API 1.0.0`; no version path segment | Docs header |
| Pagination/Querying | OData query options: `$filter`, `$top`, `$skip`, `$orderby`, `$select` | Docs "OData Query Parameters" |
| Errors | Status codes 200/400/404 documented; error body shape NOT shown | Docs response tabs |
| Rate limits | Not documented | (gap) |

## Resource Inventory

| Resource group | Endpoints | Coverage status |
| --- | --- | --- |
| Agents | `GET /api/agents`, `POST /api/agents`, `GET /api/agents/{id}`, `PATCH /api/agents/{id}`, `POST /api/agents/activate?id=`, `POST /api/agents/deactivate?id=` | Implemented |
| Change Orders | `GET /api/changeorders`, `POST /api/changeorders`, `GET /api/changeorders/{id}` | Implemented |
| Credits | `GET /api/credits/awards`, `POST /api/credits/awards` | Implemented |
| Enterprise | `GET /api/enterprises` | Implemented |
| Office | `GET /api/offices` | Implemented |
| Order Presets | `GET /api/orderpresets` | Implemented |
| Orders | `GET /api/orders`, `POST /api/orders`, `GET /api/orders/{id}`, `POST /api/orders/{id}/requestremoval` | Implemented |
| Services | `GET /api/services`, `POST /api/services`, `GET /api/services/{id}` | Implemented |

Total: 21 endpoints across 8 groups.

## Endpoint-Specific Query Parameters

- `GET /api/agents`: `email` (find agent by email) plus OData options.
- `GET /api/credits/awards`: `awardedTo` (int64 agent id) plus OData options.
- `GET /api/offices`: `enterpriseId` (int64) plus OData options.
- `POST /api/agents/activate` and `/deactivate`: `id` (int64) query-string param.

## Key Schemas

- Reused `NamedRef`: `{ "Id": int, "Name": str }` (Office, Manager,
  DefaultPostType, ServiceType, PostType, Agent ref, AwardedBy, AwardedTo).
- `Agent`: Id, UserName, Email, EmailConfirmed, FirstName, LastName, IsInactive,
  IsLocked, CcEmail, InvitationSent, Office (NamedRef, required), Manager
  (NamedRef), Address, OfficePhone, CellularPhone (required), PaymentMode (enum),
  BasicInstallPrice, BrokerId, DefaultPostType (NamedRef), Notes,
  ReceiveMarketingEmails, TermsAccepted, EnableSubscription, SubscriptionPrice,
  IsManager, ManagerData.
- `Address` (agent): Street, Street2, City, State (max 2 chars), Zip,
  CountryCode (pattern `^US|CA|AU$`).
- `ManagerData`: DiscountLevel (enum), EnableRebills, InitialRentalDuration,
  RebillInterval, RebillWarningLeadTime, IsPayer, DisableStaffBillingEmails,
  CcStaff, CcDelegates, IsVirtual.
- `JobSite`: Id, StreetAddress, StreetNumber, StreetName, StreetLine2, City,
  State, Zip, CountryCode, Latitude, Longitude, Directions, ListingNumber.
- `SalesOrderRef`: `{ "Id": int, "OrderTotal": number }`.
- `ChangeOrder` / `ServiceOrder`: Id, OrderNumber, ServiceType (NamedRef), Notes,
  Status, Created, DueDate, IsDueDateDefinitive, CompletionDate, SalesOrder,
  JobSite, Agent (NamedRef).
- `SignageOrder`: Id, OrderNumber, Status, Notes, Created, DueDate,
  IsDueDateDefinitive, DateInstalled, RemovalRequestDate, RemovalDueDate,
  IsRemovalDueDateDefinitive, RemovalDate, RebillInterval, NextRebillDate,
  SalesOrder, JobSite, PostType (NamedRef), Agent (NamedRef).
- `Award`: Id, Name, AwardedBy (NamedRef), AwardedDate, AwardedTo (NamedRef),
  ExpirationDate, TotalAmount, RemainingAmount, Restrictions ([str]).
- `Enterprise` / `Office` / `OrderPreset`: `{ "Id": int, "Name": str }`.
- Create-order request: StreetNumber, StreetName, City, State, Zip, Apartment,
  Directions, ListingNumber, ExternalID, DueDate, Notes, AgentId (required),
  PresetId (required).
- Create-order result: `{ "Status": str, "Message": str, "RequestId": int,
  "OrderId": int }`.
- Create-service / create-change-order request: InstallId (required), PresetId
  (required), Notes, DueDate, OverridePriceLimit (required).
- Request-removal request: `{ "DueDate": datetime, "Notes": str }`; result
  `{ "DueDate": datetime }`.

## Enums

- `PaymentMode`: Terms, Prepay, MonthlyCC, ACH, Transfer.
- `DiscountLevel`: Standard, Bronze, Silver, Gold.
- `CountryCode`: US, CA, AU (regex `^US|CA|AU$`).
- Award `Restrictions`: Printing (documented value).
- Order/Service/ChangeOrder `Status`: only sample values shown
  (`Designing`, `Draft`, `PaymentRequired`); full closed set unknown.

## Live Verification (2026-05-28, theperrygroup tenant)

Confirmed against the live API with a real key (read-only calls):

- Auth: `Authorization: ST-API {key}` is accepted. RESOLVED.
- List container: list endpoints return a bare JSON array (not an OData
  `{ "value": [...] }` envelope). `list_agents(top=1)` returned `[]`. RESOLVED
  (gap 2).
- 404 error body: `GET /api/agents/{bogus}` returns HTTP 404 with an empty body;
  the client maps it to `NotFoundError` with a generated message. Gap 1 is
  PARTIALLY resolved (404 body is empty; 400 body shape still unconfirmed).
- Note: the test account currently exposes no agent/office rows, so field-name
  parity with the models could not be confirmed from live data.

## Contradictions And Gaps

1. (PARTIAL) Error body for 400 is still unconfirmed; 404 returns an empty body.
   The client uses a recursive message extractor and attaches `status_code` +
   `response_data`, defaulting the message when the body is empty.
2. (RESOLVED) List endpoints return bare JSON arrays. Verified live.
3. `PATCH /api/agents/{id}` is described as a JSON Merge Patch. The required
   `Content-Type` is not stated; the client sends
   `application/merge-patch+json` and allows override. Not verified live (would
   require a mutating call).
4. Rate limits / throttling are not documented.
5. Full closed value sets for order statuses are not enumerated.
6. No webhook or async callback behavior is documented.

## Follow-Up Before Treating Coverage As Complete

- Confirm the 400 error body shape and merge-patch content type against an
  account with write access and sample data.
- Update enums and models if live responses reveal additional fields/values.
