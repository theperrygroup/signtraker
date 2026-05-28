# Authentication

## API key

The SignTraker API authenticates with an API key sent in the `Authorization`
header using the `ST-API` scheme:

```text
Authorization: ST-API <your-key>
```

Find your key in SignTraker under **My Profile**. If you do not see a key, API
access may not be enabled for your account — contact your SignTraker
administrator.

The client sets this header for you; you only supply the raw key.

## Tenant-specific host

Each SignTraker account is served from its own subdomain
(`https://<subdomain>.signtraker.com`). There is no universal default, so you
must provide one of:

=== "Subdomain"

    ```python
    from signtraker import SignTrakerClient

    client = SignTrakerClient(api_key="YOUR_KEY", subdomain="theperrygroup")
    ```

=== "Full base URL"

    ```python
    from signtraker import SignTrakerClient

    client = SignTrakerClient(
        api_key="YOUR_KEY", base_url="https://theperrygroup.signtraker.com"
    )
    ```

If neither a base URL nor a subdomain can be resolved, the client raises
`SignTrakerConfigError`.

## Environment variables

Instead of passing values explicitly, you can set environment variables. The
canonical (no-"c") names are preferred; the brand-spelled `SIGNTRACKER_*` forms
are also accepted as a fallback.

| Variable | Purpose |
| --- | --- |
| `SIGNTRAKER_API_KEY` | API key |
| `SIGNTRAKER_BASE_URL` | Full base URL |
| `SIGNTRAKER_SUBDOMAIN` | Tenant subdomain |
| `SIGNTRAKER_TIMEOUT_SECONDS` | Per-request timeout (default 30) |
| `SIGNTRAKER_MAX_RETRIES` | Retry attempts for transient failures (default 0) |
| `SIGNTRAKER_RETRY_BACKOFF_SECONDS` | Base backoff between retries (default 0.5) |

```python
from signtraker import SignTrakerClient

client = SignTrakerClient()  # reads SIGNTRAKER_API_KEY + SIGNTRAKER_SUBDOMAIN
```

To load values from a `.env` file (requires the `dotenv` extra):

```python
client = SignTrakerClient(load_dotenv=True)
```
