# Quickstart

## Create a client

```python
from signtraker import SignTrakerClient

client = SignTrakerClient(subdomain="theperrygroup")
```

## List, filter, and page

```python
# Top 5 agents ordered by last name
agents = client.agents.list_agents(top=5, orderby="LastName")

# Agents 16-20 ordered by last name
page = client.agents.list_agents(top=5, skip=15, orderby="LastName")

# Filter with OData
smiths = client.agents.list_agents(filter="LastName eq 'Smith'")

# Find by email
matches = client.agents.list_agents(email="someone@example.com")
```

## Read a single record

```python
agent = client.agents.get_agent(123)
order = client.orders.get_order(456)
```

## Typed access with models

Responses are plain dictionaries. Validate them with a model for typed access:

```python
from signtraker.models import Agent

agent = Agent.model_validate(client.agents.get_agent(123))
print(agent.first_name, agent.email)
```

## Build a request body with a model

```python
from signtraker.models import CreateOrderRequest

body = CreateOrderRequest(
    agent_id=42, preset_id=7, street_name="Main St", city="Austin"
)
result = client.orders.create_order(
    body.model_dump(by_alias=True, exclude_none=True)
)
print(result["OrderId"])
```

## Handle errors

```python
from signtraker import NotFoundError, SignTrakerError

try:
    client.agents.get_agent(999999)
except NotFoundError:
    print("Not found")
except SignTrakerError as exc:
    print(exc.status_code, exc.message)
```
