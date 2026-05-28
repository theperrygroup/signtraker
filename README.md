# signtraker

A typed, production-grade Python client for the [SignTraker API](https://theperrygroup.signtraker.com/api-docs).

- Layered design: a shared HTTP transport (`BaseClient`) plus one thin client per resource group.
- Typed throughout: full type hints, Pydantic v2 models, and a shipped `py.typed` marker.
- Friendly errors: HTTP status codes map to a typed exception hierarchy.
- OData querying: ergonomic `filter` / `top` / `skip` / `orderby` / `select` keywords.

## Installation

```bash
pip install signtraker
```

Optional `.env` support:

```bash
pip install "signtraker[dotenv]"
```

## Authentication

The API uses an API key sent as `Authorization: ST-API <key>`. Find your key in
SignTraker under **My Profile** (contact your administrator if API access is not
enabled).

The API host is tenant-specific (`https://<subdomain>.signtraker.com`), so you
must provide either a `subdomain` or a full `base_url`.

```python
from signtraker import SignTrakerClient

# Provide the key explicitly...
client = SignTrakerClient(api_key="YOUR_KEY", subdomain="theperrygroup")

# ...or via environment variables (SIGNTRAKER_API_KEY / SIGNTRAKER_SUBDOMAIN).
client = SignTrakerClient(subdomain="theperrygroup")
```

Supported environment variables (the brand-spelled `SIGNTRACKER_*` forms are also
accepted as a fallback):

- `SIGNTRAKER_API_KEY`
- `SIGNTRAKER_BASE_URL` or `SIGNTRAKER_SUBDOMAIN`
- `SIGNTRAKER_TIMEOUT_SECONDS`, `SIGNTRAKER_MAX_RETRIES`, `SIGNTRAKER_RETRY_BACKOFF_SECONDS`

## Quickstart

```python
from signtraker import SignTrakerClient

client = SignTrakerClient(subdomain="theperrygroup")

# List the first 5 agents ordered by last name
agents = client.agents.list_agents(top=5, orderby="LastName")
for agent in agents:
    print(agent["FirstName"], agent["LastName"])

# Fetch one agent
agent = client.agents.get_agent(123)

# Find an agent by email
matches = client.agents.list_agents(email="someone@example.com")
```

Responses are plain dictionaries. For typed access, validate with a model:

```python
from signtraker.models import Agent

agent = Agent.model_validate(client.agents.get_agent(123))
print(agent.first_name, agent.email)
```

## API coverage

| Resource group | Property | Endpoints |
| --- | --- | --- |
| Agents | `client.agents` | list, get, create, update, activate, deactivate |
| Change Orders | `client.change_orders` | list, get, create |
| Credits | `client.credits` | list awards, create award |
| Enterprises | `client.enterprises` | list |
| Offices | `client.offices` | list |
| Order Presets | `client.order_presets` | list |
| Orders (signage) | `client.orders` | list, get, create, request removal |
| Services | `client.services` | list, get, create |

## Error handling

```python
from signtraker import SignTrakerClient, NotFoundError, SignTrakerError

client = SignTrakerClient(subdomain="theperrygroup")
try:
    agent = client.agents.get_agent(999999)
except NotFoundError:
    print("No such agent")
except SignTrakerError as exc:
    print(exc.status_code, exc.message)
```

## Documentation

Full documentation (API reference, guides, and examples) is built with MkDocs.
See the [`docs/`](docs/) directory or the published site.

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pip install -r docs/requirements.txt

black --check .
isort --check-only --profile=black --line-length=88 .
flake8 .
mypy signtraker/ --strict
pytest --cov=signtraker --cov-report=term-missing
mkdocs build --strict
```

Live integration tests are opt-in and run only when a real key is set in the
environment:

```bash
SIGNTRAKER_API_KEY=... SIGNTRAKER_SUBDOMAIN=theperrygroup pytest -m live
```

## License

MIT. See [LICENSE](LICENSE).
