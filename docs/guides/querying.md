# Querying & OData

List endpoints accept the OData query options supported by the SignTraker API.
The client exposes them as ergonomic keyword arguments and converts them to the
`$`-prefixed parameters the API expects.

| Keyword | OData param | Example |
| --- | --- | --- |
| `filter` | `$filter` | `filter="LastName eq 'Smith'"` |
| `top` | `$top` | `top=5` |
| `skip` | `$skip` | `skip=15` |
| `orderby` | `$orderby` | `orderby="LastName"` or `orderby=["LastName", "Id"]` |
| `select` | `$select` | `select="Id,LastName"` or `select=["Id", "LastName"]` |

`orderby` and `select` accept either a string or a sequence of strings (joined
with commas).

## Examples

```python
# Top 5 agents by last name
client.agents.list_agents(top=5, orderby="LastName")

# Page: records 16-20
client.agents.list_agents(top=5, skip=15, orderby="LastName")

# Filter
client.agents.list_agents(filter="LastName eq 'Smith'")

# Select only specific fields
client.agents.list_agents(select=["Id", "FirstName", "LastName"])
```

## Endpoint-specific filters

Some list endpoints expose dedicated query parameters in addition to OData:

```python
client.agents.list_agents(email="someone@example.com")
client.offices.list_offices(enterprise_id=42)
client.credits.list_awards(awarded_to=123)
```

!!! note "Response shape"
    List endpoints return a JSON array of records (verified against the live
    API). Methods return the parsed list directly.
