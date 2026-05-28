# Error Handling

Every API failure raises a subclass of `SignTrakerError`. Each exception carries
the HTTP `status_code` and the parsed `response_data` for debugging.

## Exception mapping

| HTTP status | Exception |
| --- | --- |
| 400 | `ValidationError` |
| 401, 403 | `AuthenticationError` |
| 404 | `NotFoundError` |
| 429 | `RateLimitError` |
| 5xx | `ServerError` |
| other non-2xx | `SignTrakerError` |
| network failure | `NetworkError` |
| missing base URL/subdomain | `SignTrakerConfigError` |

## Catching errors

```python
from signtraker import (
    SignTrakerClient,
    NotFoundError,
    ValidationError,
    SignTrakerError,
)

client = SignTrakerClient(subdomain="theperrygroup")

try:
    client.agents.get_agent(999999)
except NotFoundError:
    print("Agent not found")
except ValidationError as exc:
    print("Bad request:", exc.message)
except SignTrakerError as exc:
    print("API error", exc.status_code, exc.message)
    print("Raw payload:", exc.response_data)
```

## Retries

Transient failures (HTTP 500/502/503/504 and network errors) can be retried
automatically with exponential backoff:

```python
client = SignTrakerClient(
    subdomain="theperrygroup", max_retries=3, retry_backoff_seconds=0.5
)
```

Retries default to off (`max_retries=0`).
