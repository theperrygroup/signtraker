# Data Types & Enums

All client methods accept and return plain dictionaries. The Pydantic models
below are optional sugar for callers who want validation and typed access. They
use PascalCase aliases (matching the API JSON) with `snake_case` attributes, and
`populate_by_name` is enabled so you can construct them either way.

```python
from signtraker.models import Agent

agent = Agent.model_validate(client.agents.get_agent(123))
payload = agent.model_dump(by_alias=True, exclude_none=True)
```

## Enums

::: signtraker.enums

## Models

::: signtraker.models
