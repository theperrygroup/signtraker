# Source Of Truth Matrix

| Topic | Canonical source | Secondary source | Confidence | Follow-up |
| --- | --- | --- | --- | --- |
| Authentication | SignTraker API docs (`Authorization: ST-API {key}`) | API_CLIENT_BLUEPRINT.md (auth section) | High | None |
| Base URL / host | SignTraker API docs ("API SERVER") | User-provided URL `theperrygroup.signtraker.com` | High | Host is tenant-specific; no universal default |
| Resource grouping | SignTraker API docs section headings | API_CLIENT_BLUEPRINT.md | High | None |
| Endpoint inventory | SignTraker API docs | — | High | None |
| Request/response schemas | SignTraker API docs example schemas | — | Medium | Single-object examples on list endpoints |
| Enums | SignTraker API docs "Allowed" lists | — | Medium | Status enums partially enumerated |
| Pagination / querying | SignTraker API docs (OData) | Microsoft OData docs | High | None |
| Error model | — | API_CLIENT_BLUEPRINT.md error-mapping convention | Low | Needs live example |
| Rate limits | — | — | Low | Undocumented; confirm live |
| Uploads / downloads | — | — | High | None present in this API |
| Webhooks | — | — | High | None present in this API |
