# SignTraker Python Client

A typed, production-grade Python client for the
[SignTraker API](https://theperrygroup.signtraker.com/api-docs).

!!! tip "Why this client"
    - Layered design: a shared HTTP transport plus one thin client per resource group.
    - Fully typed: type hints everywhere, Pydantic v2 models, and a shipped `py.typed` marker.
    - Friendly errors: HTTP status codes map to a typed exception hierarchy.
    - OData querying: ergonomic `filter` / `top` / `skip` / `orderby` / `select` keywords.

## Install

```bash
pip install signtraker
```

## A 30-second tour

```python
from signtraker import SignTrakerClient

client = SignTrakerClient(subdomain="theperrygroup")  # reads SIGNTRAKER_API_KEY

for agent in client.agents.list_agents(top=5, orderby="LastName"):
    print(agent["FirstName"], agent["LastName"])
```

## Where to go next

- [Installation](getting-started/installation.md)
- [Authentication](getting-started/authentication.md)
- [Quickstart](getting-started/quickstart.md)
- [API Reference](api/index.md)

## Resource groups

The client exposes eight resource groups, each as a lazily created property on
`SignTrakerClient`:

`agents`, `change_orders`, `credits`, `enterprises`, `offices`,
`order_presets`, `orders`, and `services`.
