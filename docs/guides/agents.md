# Working with Agents

The `agents` resource group covers the full agent lifecycle.

## List and search

```python
agents = client.agents.list_agents(top=10, orderby="LastName")
by_email = client.agents.list_agents(email="someone@example.com")
```

## Get one

```python
agent = client.agents.get_agent(123)
```

## Create

```python
new_agent = client.agents.create_agent(
    {
        "UserName": "jdoe",
        "Email": "jdoe@example.com",
        "FirstName": "Jane",
        "LastName": "Doe",
        "CellularPhone": "555-1212",
        "PaymentMode": "Terms",
        "Office": {"Id": 1},
        "EmailConfirmed": False,
        "IsInactive": False,
        "IsLocked": False,
        "InvitationSent": False,
        "ReceiveMarketingEmails": False,
        "TermsAccepted": True,
        "EnableSubscription": False,
        "IsManager": False,
    }
)
```

You can build and validate the payload with the `Agent` model:

```python
from signtraker.models import Agent

agent = Agent(
    user_name="jdoe",
    email="jdoe@example.com",
    first_name="Jane",
    last_name="Doe",
    cellular_phone="555-1212",
    payment_mode="Terms",
    office={"Id": 1},
)
client.agents.create_agent(agent.model_dump(by_alias=True, exclude_none=True))
```

## Update (JSON Merge Patch)

Only the fields you pass are changed; everything else is left untouched. The
client sends the body as `application/merge-patch+json`.

```python
client.agents.update_agent(123, {"Notes": "VIP client"})
```

!!! warning "Update limitations"
    You cannot convert an agent to/from a manager via update, and synced
    National Account agents cannot be updated directly.

## Activate / deactivate

```python
client.agents.activate_agent(123)
client.agents.deactivate_agent(123)
```
