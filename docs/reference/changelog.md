# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-28

### Added

- Initial release of the `signtraker` client.
- `SignTrakerClient` aggregator with lazy, cached sub-clients.
- Full coverage of all 8 resource groups (21 endpoints): agents, change orders,
  credits, enterprises, offices, order presets, orders, and services.
- Shared `BaseClient` transport with `ST-API` auth, tenant base-URL resolution,
  configurable timeouts and retries, and typed error mapping.
- Pydantic v2 models and shared enums.
- OData query helper (`filter`/`top`/`skip`/`orderby`/`select`).
- 100% unit-test coverage with mocked HTTP, plus opt-in live tests.
