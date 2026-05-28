# Client

The aggregator `SignTrakerClient` is the primary entry point. It lazily creates
and caches one sub-client per resource group. All sub-clients subclass
`BaseClient`, which owns the HTTP transport.

::: signtraker.client.SignTrakerClient

::: signtraker.base_client.BaseClient
