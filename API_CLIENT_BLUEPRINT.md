# Python API Client Library Blueprint

A complete, reusable specification for building a typed, production-grade Python
API client library for **any** HTTP/JSON API. It captures the architecture,
coding standards, testing strategy, documentation system, packaging, and CI/CD
automation that together make a maintainable, publishable client.

Feed this document to an AI (or follow it yourself) to scaffold a new library
from API documentation. Everything here is API-agnostic.

---

## 1. Purpose & How to Use

This blueprint describes a layered Python API client with:

- A shared HTTP transport layer (`BaseClient`) that owns sessions, auth,
  timeouts, retries, error handling, and file uploads.
- One thin resource module per logical API group, each subclassing the
  transport layer.
- A single aggregator client exposing each resource group as a lazily
  instantiated property.
- A typed exception hierarchy, Pydantic data models, shared enums, and a typed
  package marker (`py.typed`).
- Full test coverage with mocked HTTP, MkDocs documentation, strict linting/type
  checking, and automated PyPI + docs releases.

### Placeholder legend

Replace these placeholders consistently throughout the generated repo:

| Placeholder            | Meaning                                            | Example                         |
| ---------------------- | -------------------------------------------------- | ------------------------------- |
| `{package}`            | Import/distribution name (PEP 8, lowercase)        | `acme_api`                      |
| `{ClientName}`         | Aggregator client class name (PascalCase)          | `AcmeClient`                    |
| `{ErrorBase}`          | Base exception class name                          | `AcmeError`                     |
| `{SERVICE}`            | Env-var prefix (UPPER_SNAKE_CASE)                  | `ACME`                          |
| `{SERVICE}_API_KEY`    | Env var holding the credential                     | `ACME_API_KEY`                  |
| `{BASE_URL}`           | Default API base URL                               | `https://api.acme.com/v1`       |
| `{AUTH_HEADER}`        | Auth header name                                   | `Authorization` / `X-API-KEY`   |
| `{ResourceClient}`     | A resource group client class                      | `UsersClient`                   |
| `{resource}`           | A resource group property/module name              | `users`                         |

> Convention note: this blueprint assumes API-key auth via a request header. If
> the target API uses OAuth2 / bearer tokens / HMAC, adapt only the auth section
> of `BaseClient`; the rest of the architecture is unchanged.

---

## 2. Inputs Required Before Coding (API Source Audit)

Before writing any code, capture a single source-of-truth matrix from the API
documentation (OpenAPI/Swagger preferred, otherwise reference docs). Record:

- **Authentication**: scheme (API key header, bearer token, OAuth2), credential
  name, header format, and the environment variable that will hold it.
- **Base URL(s) & versioning**: the primary base URL and any per-service base
  URLs (some APIs route different resource groups to different hosts). Note the
  version segment (e.g. `/v1`).
- **Resource groups**: the logical grouping of endpoints (e.g. users, orders,
  billing). Each group becomes one module + one client class.
- **Endpoint inventory**: for each endpoint — HTTP method, path, path params,
  query params, request body schema, response schema, and success status code.
- **Schemas / models**: request and response object shapes worth modeling with
  Pydantic.
- **Enums**: closed value sets (statuses, types, sort fields, country/region).
- **Uploads**: any multipart/form-data endpoints and their field names.
- **Pagination**: page/offset/cursor strategy and response envelope shape.
- **Rate limits**: limits and the status code used (commonly `429`).
- **Error model**: the JSON error envelope shape(s), including any nested or
  single-key wrapper payloads, so the error-message extractor can be tuned.
- **Gaps & contradictions**: anything missing or inconsistent in the docs.

If sources disagree, prefer the most authoritative (OpenAPI > reference docs >
backlog notes) and record the gap before coding.

---

## 3. Repository Layout

```text
{package}/                      # the importable package
  __init__.py                   # public API surface, __all__, __version__
  base_client.py                # shared HTTP transport + error mapping
  client.py                     # aggregator client (lazy sub-client properties)
  exceptions.py                 # typed exception hierarchy
  enums.py                      # shared/cross-cutting enums
  models.py                     # Pydantic data models
  py.typed                      # PEP 561 marker (empty file)
  {resource}.py                 # one module per resource group (+ local enums)
  ...

tests/
  __init__.py
  test_base_client.py
  test_client.py
  test_exceptions.py
  test_models.py
  test_{resource}.py            # one test file per resource module
  test_live_*.py                # opt-in live integration tests (real API)

docs/
  index.md
  requirements.txt              # docs-only dependencies
  STYLE_GUIDE.md                # documentation writing standards
  getting-started/             # installation, authentication, quickstart
  guides/                      # task-oriented tutorials
  api/                         # one reference page per resource group
  reference/                   # data types/enums, exceptions, changelog
  development/                 # contributing, deployment
  includes/                    # shared snippets (abbreviations, etc.)
  stylesheets/ , javascripts/  # theme customizations

docs_extensions/                # optional custom MkDocs/markdown extensions
  __init__.py
  *.py

examples/                       # runnable usage examples
tools/                          # maintenance scripts (e.g. dependency sync)

.github/
  workflows/
    ci.yml                      # quality + tests + build on push/PR
    unified-deployment.yml      # version bump, PyPI publish, docs, release
    security-audit.yml          # scheduled dependency audit + remediation PR
  dependabot.yml

pyproject.toml                  # build system, metadata, tool config
MANIFEST.in                     # sdist file inclusion rules
requirements.txt                # runtime deps (mirror of pyproject core)
requirements-dev.txt            # dev deps (mirror of [dev] extra)
.flake8                         # flake8 config (if not in pyproject)
README.md
LICENSE
STYLE_GUIDE.md                  # code style standards
```

---

## 4. Core Architecture

### 4.1 BaseClient (HTTP transport)

A single base class owns all transport concerns. Every resource client
subclasses it. Responsibilities:

- Resolve the API key from the constructor arg or `{SERVICE}_API_KEY` env var;
  raise an auth error if missing.
- Resolve `base_url`, `timeout_seconds`, `max_retries`, and
  `retry_backoff_seconds` from constructor args, then env vars
  (`{SERVICE}_TIMEOUT_SECONDS`, `{SERVICE}_MAX_RETRIES`,
  `{SERVICE}_RETRY_BACKOFF_SECONDS`), then defaults.
- Create a `requests.Session` with the auth + content-type + accept headers.
- Provide a private `_request` method with a retry loop for transient `5xx`
  errors and network exceptions, plus correct multipart handling (do not set
  `Content-Type` for file uploads; let `requests` set the boundary, but preserve
  the auth header).
- Provide thin verb helpers: `get`, `post`, `put`, `patch`, `delete`, each
  accepting an optional per-request timeout override.
- Centralize response parsing and status-code-to-exception mapping in
  `_handle_response`.

Trimmed skeleton (genericize names; full error mapping in 4.2):

```python
"""Base client: shared HTTP transport and error handling."""

import os
import time
from typing import Any, Dict, List, Optional, Union

import requests

from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    {ErrorBase},
    ServerError,
    ValidationError,
)

DEFAULT_BASE_URL = "{BASE_URL}"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 0
DEFAULT_RETRY_BACKOFF_SECONDS = 0.5

ENV_TIMEOUT_SECONDS = "{SERVICE}_TIMEOUT_SECONDS"
ENV_MAX_RETRIES = "{SERVICE}_MAX_RETRIES"
ENV_RETRY_BACKOFF_SECONDS = "{SERVICE}_RETRY_BACKOFF_SECONDS"


class BaseClient:
    """Base client with shared request/response handling."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        timeout_seconds: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
    ) -> None:
        """Initialize the base client.

        Args:
            api_key: API key. Falls back to the ``{SERVICE}_API_KEY`` env var.
            base_url: API base URL. Defaults to the production URL.
            timeout_seconds: Per-request timeout. Falls back to env/default.
            max_retries: Retry attempts for transient failures.
            retry_backoff_seconds: Base backoff between retries (exponential).

        Raises:
            AuthenticationError: If no API key can be resolved.
        """
        self.api_key = api_key or os.getenv("{SERVICE}_API_KEY")
        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Set {SERVICE}_API_KEY or pass api_key."
            )
        self.base_url = base_url or DEFAULT_BASE_URL
        self.timeout_seconds = (
            float(timeout_seconds)
            if timeout_seconds is not None
            else _parse_env_float(ENV_TIMEOUT_SECONDS, DEFAULT_TIMEOUT_SECONDS)
        )
        self.max_retries = (
            int(max_retries)
            if max_retries is not None
            else _parse_env_int(ENV_MAX_RETRIES, DEFAULT_MAX_RETRIES)
        )
        self.retry_backoff_seconds = (
            float(retry_backoff_seconds)
            if retry_backoff_seconds is not None
            else _parse_env_float(
                ENV_RETRY_BACKOFF_SECONDS, DEFAULT_RETRY_BACKOFF_SECONDS
            )
        )
        self.session = requests.Session()
        self.session.headers.update(
            {
                "{AUTH_HEADER}": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json_data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        files: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make an HTTP request with retry on transient failures."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        effective_timeout = (
            float(timeout_seconds)
            if timeout_seconds is not None
            else self.timeout_seconds
        )
        retryable = {500, 502, 503, 504}
        for attempt in range(self.max_retries + 1):
            try:
                if files:
                    # Let requests set the multipart boundary; keep auth header.
                    headers = {"{AUTH_HEADER}": self.api_key, "Accept": "application/json"}
                    response = requests.request(
                        method=method, url=url, data=data, files=files,
                        params=params, headers=headers, timeout=effective_timeout,
                    )
                else:
                    response = self.session.request(
                        method=method, url=url, json=json_data, data=data,
                        params=params, timeout=effective_timeout,
                    )
                if response.status_code in retryable and attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))
                    continue
                return self._handle_response(response)
            except requests.exceptions.RequestException as exc:
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (2 ** attempt))
                    continue
                raise NetworkError(f"Network error: {exc}") from exc

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            *, timeout_seconds: Optional[float] = None) -> Any:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params,
                             timeout_seconds=timeout_seconds)

    # post / put / patch / delete mirror get, forwarding json_data/data/files.
```

Helper functions `_parse_env_float` / `_parse_env_int` read an env var and fall
back to a default on missing/invalid values.

### 4.2 Response handling & error mapping

`_handle_response` parses the body and maps status codes to typed exceptions.
Rules:

- `204 No Content` -> return `{}`.
- Parse JSON if a body exists; on invalid JSON, wrap raw text as `{"message": ...}`.
- `200` / `201` -> return parsed data.
- Otherwise normalize the payload to a dict and raise:

| Status      | Exception              |
| ----------- | ---------------------- |
| `400`       | `ValidationError`      |
| `401`       | `AuthenticationError`  |
| `403`       | `AuthenticationError`  |
| `404`       | `NotFoundError`        |
| `429`       | `RateLimitError`       |
| `500`–`599` | `ServerError`          |
| other       | `{ErrorBase}`          |

Every raised exception carries `status_code` and `response_data` for debugging.

Use a recursive `_extract_error_message` helper to find a human-readable message
regardless of the error envelope shape. It should:

- Check common direct fields (`message`, `error`, `detail`, `title`).
- Unwrap single-key wrapper objects (common in nested error envelopes).
- Recurse into nested dicts/lists, de-duplicating list messages.
- Fall back to a stringified scalar only at the top level (so numeric metadata
  like status codes never outrank a deeper real message).

### 4.3 Aggregator client

A single client class is the primary entry point. It does not subclass
`BaseClient`; instead it stores config and lazily instantiates each resource
client on first property access, caching the instance.

```python
"""Main aggregator client."""

from typing import Optional

from .users import UsersClient
# ... import each resource client


class {ClientName}:
    """Primary entry point exposing all resource groups.

    Example:
        ```python
        from {package} import {ClientName}

        client = {ClientName}()                  # reads {SERVICE}_API_KEY
        client = {ClientName}(api_key="...")      # or pass explicitly
        user = client.users.get_user("123")
        ```
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        load_dotenv: bool = False,
        timeout_seconds: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
    ) -> None:
        """Initialize the aggregator client.

        Args:
            api_key: API key; falls back to the ``{SERVICE}_API_KEY`` env var.
            base_url: Override the default API base URL.
            load_dotenv: Opt-in load of a ``.env`` file via ``python-dotenv``.
            timeout_seconds: Default timeout propagated to all sub-clients.
            max_retries: Retry attempts propagated to all sub-clients.
            retry_backoff_seconds: Backoff propagated to all sub-clients.
        """
        if load_dotenv:
            from dotenv import load_dotenv as _load_dotenv
            _load_dotenv()
        self._api_key = api_key
        self._base_url = base_url
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds
        self._users: Optional[UsersClient] = None
        # ... one cached slot per resource client

    @property
    def users(self) -> UsersClient:
        """Access the users endpoints."""
        if self._users is None:
            self._users = UsersClient(
                api_key=self._api_key,
                base_url=self._base_url,
                timeout_seconds=self._timeout_seconds,
                max_retries=self._max_retries,
                retry_backoff_seconds=self._retry_backoff_seconds,
            )
        return self._users
```

**Per-service base URLs**: if a resource group lives on a different host, omit
`base_url` when constructing that sub-client so its own module default applies
(the resource client sets its own default base URL in its `__init__`).

`load_dotenv` is opt-in to avoid import-time side effects and keep
`python-dotenv` an optional dependency.

### 4.4 Resource module pattern

One module per API group. Each defines any module-local enums and a client class
that subclasses `BaseClient`, overriding the default base URL if the group lives
on its own host.

```python
"""Users API client."""

from enum import Enum
from typing import Any, Dict, Optional

from .base_client import BaseClient


class UserSortField(Enum):
    """Sort fields for user searches."""

    ID = "ID"
    LAST_NAME = "LAST_NAME"


class UsersClient(BaseClient):
    """Client for user-related endpoints."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        timeout_seconds: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
    ) -> None:
        """Initialize the users client.

        Args:
            api_key: API key for authentication.
            base_url: Override base URL; defaults to this group's host.
            timeout_seconds: Per-request timeout.
            max_retries: Retry attempts for transient failures.
            retry_backoff_seconds: Base backoff between retries.
        """
        super().__init__(
            api_key=api_key,
            base_url=base_url or "{BASE_URL}",
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            retry_backoff_seconds=retry_backoff_seconds,
        )

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """Get a single user by ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            The user record as a dictionary.

        Raises:
            NotFoundError: If the user does not exist.
            AuthenticationError: If the API key is invalid.
            {ErrorBase}: For other API errors.
        """
        return self.get(f"users/{user_id}")
```

Method conventions: descriptive `snake_case` names, full type hints,
Google-style docstrings with `Args`/`Returns`/`Raises`, and a thin body that
delegates to a verb helper.

---

## 5. Exceptions

A single base exception carries context; typed subclasses let callers catch
specific conditions.

```python
"""Custom exceptions."""

from typing import Any, Dict, List, Optional


class {ErrorBase}(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the error.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code, if applicable.
            response_data: Parsed response payload, if available.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError({ErrorBase}):
    """Raised when authentication fails (401/403)."""


class ValidationError({ErrorBase}):
    """Raised when request validation fails (400)."""


class NotFoundError({ErrorBase}):
    """Raised when a resource is not found (404)."""


class RateLimitError({ErrorBase}):
    """Raised when the rate limit is exceeded (429)."""


class ServerError({ErrorBase}):
    """Raised on 5xx server errors."""


class NetworkError({ErrorBase}):
    """Raised when the network connection fails."""
```

Add **domain-specific** subclasses where they improve ergonomics, e.g. a
sequencing error that lists required steps, or an invalid-field error that names
the correct field. Subclass the closest semantic parent (often
`ValidationError`).

---

## 6. Models & Enums

- Use **Pydantic v2** for request/response models worth typing. Document each
  model and field; prefer `Field(..., description="...")`.
- Keep cross-cutting enums (sort direction, country/region, shared statuses) in
  `enums.py`; keep group-specific enums inside their resource module.
- Models are optional sugar — dict-based access remains valid — but they improve
  IDE support and validation for complex payloads.
- Ship `py.typed` (an empty marker file) so downstream type checkers honor the
  package's type hints (PEP 561).

```python
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """User data model."""

    id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    status: str = Field(..., description="Account status")
    created_at: Optional[str] = Field(None, description="ISO 8601 timestamp")
```

---

## 7. Public API Surface (`__init__.py`)

Re-export the aggregator client, every resource client, all exceptions, and the
commonly used enums/models. Declare `__all__` and `__version__`.

```python
"""{package} — Python API client."""

from .client import {ClientName}
from .users import UsersClient, UserSortField
from .enums import SortDirection
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    {ErrorBase},
    ServerError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "{ClientName}",
    "UsersClient",
    "UserSortField",
    "SortDirection",
    "{ErrorBase}",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]
```

`__version__` must match the version in `pyproject.toml` (see §11 single-source
rule).

---

## 8. Coding Standards

- **Docstrings**: Google style on every public class, method, and function, with
  `Args` / `Returns` / `Raises` sections.
- **Type hints**: required on all parameters and return values; run `mypy
  --strict`.
- **Import order**: (1) stdlib, (2) third-party, (3) local; import specific
  names where practical. `isort` with the `black` profile enforces this.
- **Naming**: `PascalCase` classes, `snake_case` functions/variables,
  `UPPER_SNAKE_CASE` constants, leading underscore for private members.
- **Line length**: 88 (Black default).
- **Class design**: single responsibility per resource client; public methods
  before private; group related methods.
- **Error handling**: catch transport exceptions at the transport layer; map
  status codes to typed exceptions; never leak raw `requests` exceptions to
  callers.
- **Maintenance notes**: keep a "Known API quirks" section in the code style
  guide documenting field-name/value gotchas discovered against the live API.

---

## 9. Testing

- **Framework**: `pytest`. **HTTP mocking**: the `responses` library to register
  expected requests and canned responses — no real network calls in unit tests.
- **Layout**: one `test_{resource}.py` per resource module, plus
  `test_base_client.py`, `test_client.py`, `test_exceptions.py`,
  `test_models.py`. Use a fixture to build the client with a dummy API key.
- **Coverage**: target **100%**; configure `--cov` and `--cov-report=term-missing`.
- **Assertions**: verify the exact URL/method called, request payload, and the
  parsed return value; assert that error status codes raise the correct typed
  exception.
- **Live integration tests**: keep real-API tests in clearly named
  `test_live_*.py` files, gated on a real credential, and excluded from the
  default mocked run when no key is present.

```python
"""Tests for UsersClient."""

import pytest
import responses

from {package}.users import UsersClient
from {package}.exceptions import NotFoundError


class TestUsersClient:
    """Unit tests for UsersClient."""

    @pytest.fixture
    def client(self) -> UsersClient:
        """Create a client with a dummy key."""
        return UsersClient(api_key="test_api_key")

    @responses.activate
    def test_get_user(self, client: UsersClient) -> None:
        """get_user returns the parsed user record."""
        responses.add(
            responses.GET,
            "{BASE_URL}/users/123",
            json={"id": "123", "email": "a@b.com", "status": "ACTIVE"},
            status=200,
        )
        result = client.get_user("123")
        assert result["id"] == "123"

    @responses.activate
    def test_get_user_not_found(self, client: UsersClient) -> None:
        """A 404 raises NotFoundError."""
        responses.add(responses.GET, "{BASE_URL}/users/x", status=404, json={})
        with pytest.raises(NotFoundError):
            client.get_user("x")
```

---

## 10. Documentation System

- **Generator**: MkDocs with the **Material** theme and **mkdocstrings**
  (Python handler, `docstring_style: google`) for API reference generated from
  docstrings.
- **`docs/requirements.txt`**: pin docs-only deps (`mkdocs-material`,
  `mkdocstrings[python]`, `mkdocs-minify-plugin`, `pymdown-extensions`, etc.).
- **Navigation taxonomy** (`mkdocs.yml` `nav`):
  - **Home** — landing/overview.
  - **Getting Started** — installation, authentication, quickstart.
  - **Guides** — task-oriented tutorials per workflow.
  - **API Reference** — one page per resource group.
  - **Reference** — data types & enums, exception handling, changelog.
  - **Development** — contributing, deployment.
- **Markdown extensions**: enable `admonition`, `pymdownx.superfences`,
  `pymdownx.tabbed`, `pymdownx.highlight`, `toc` with permalinks, `tables`,
  `attr_list`, snippets/includes.
- **Docs style guide**: keep `docs/STYLE_GUIDE.md` describing tone, admonition
  usage, code-tab conventions, and page structure.
- **Custom extensions**: place optional custom markdown/MkDocs extensions in
  `docs_extensions/` and register them in `mkdocs.yml` `markdown_extensions`.
- **Reference page pattern**: short overview admonition, tabbed quick-start code
  examples, then `::: {package}.{resource}` mkdocstrings auto-reference.

---

## 11. Packaging

Use `pyproject.toml` with the setuptools backend. Include project metadata,
runtime deps, an optional `dev` extra, and tool configuration in one file.

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{package}"
version = "0.1.0"
description = "Python client for the {SERVICE} API"
readme = "README.md"
license = {file = "LICENSE"}
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.5.0",
    "typing-extensions>=4.8.0",
]

[project.optional-dependencies]
dotenv = ["python-dotenv>=1.0.0"]
dev = [
    "python-dotenv>=1.0.0",
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "responses>=0.24.0",
    "black>=24.0.0",
    "flake8>=6.1.0",
    "mypy>=1.6.0",
    "isort>=5.13.0",
    "types-requests>=2.31.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["{package}*", "docs_extensions*"]
exclude = ["tests*", "venv*"]

[tool.setuptools.package-data]
{package} = ["py.typed"]

[tool.black]
line-length = 88

[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["{package}"]

[tool.mypy]
python_version = "3.9"
disallow_untyped_defs = true
disallow_incomplete_defs = true
warn_unused_ignores = true
warn_redundant_casts = true
strict_equality = true
show_error_codes = true

[tool.pytest.ini_options]
minversion = "6.0"
addopts = "-ra -q --strict-markers --cov={package} --cov-report=term-missing"
testpaths = ["tests"]

[tool.coverage.run]
source = ["{package}"]
omit = ["*/tests/*", "*/venv/*"]
```

- **`MANIFEST.in`**: include `README.md`, `LICENSE`, requirements, and
  `py.typed`; `recursive-exclude` tests/caches/build artifacts.
- **`requirements.txt` / `requirements-dev.txt`**: mirror the pyproject core and
  `dev` extra for environments that prefer plain requirements files.
- **Version single-sourcing**: the version appears in **two** places —
  `pyproject.toml` `[project].version` and `{package}/__init__.py`
  `__version__`. The release pipeline updates and verifies both must match.

---

## 12. CI/CD & Automation (GitHub Actions)

### `ci.yml` — on push/PR to main and develop

1. **Code Quality & Security** (single Python version):
   - `black --check`, `isort --check-only --profile=black`.
   - `flake8` (fail on syntax errors `E9,F63,F7,F82`; report style/complexity).
   - `mypy {package}/ --strict`.
   - `bandit -r {package}/` (security scan, non-blocking).
   - `pip-audit` against the installed dependency set.
   - Validate all YAML and TOML files parse.
2. **Test Suite** (matrix: Python 3.8–3.12), needs Quality:
   - `pytest --cov={package} --cov-report=xml --cov-report=term-missing`.
   - Upload coverage (e.g. Codecov) on the primary version.
3. **Build Package**, needs Quality + Test:
   - `python -m build` then `twine check dist/*`; upload artifacts.

### `unified-deployment.yml` — tags `v*`, main pushes, or manual dispatch

A single pipeline that branches on deployment type (release vs docs-only):

1. **Determine deployment type** from the trigger/inputs.
2. **Version bump** (manual release): validate semver, ensure the tag does not
   exist, update both version locations, commit, tag, push.
3. **Code Quality** and **Test** (reuse the CI gates).
4. **Build** the package and verify the tag version matches both version
   locations.
5. **Build Docs**: `mkdocs build --clean`, optionally regenerate an API-coverage
   include; upload as a Pages artifact.
6. **Publish to PyPI** via `pypa/gh-action-pypi-publish` (release environment +
   API token secret).
7. **Deploy Docs** to GitHub Pages.
8. **Create GitHub Release** with generated changelog and built artifacts.

### `security-audit.yml` — weekly schedule + manual

- Run `pip-audit --fix` across all requirements manifests; optionally run a
  script to sync `pyproject.toml` lower bounds with the requirements files.
- If manifests changed, open/update a remediation PR (e.g.
  `peter-evans/create-pull-request`) labeled `dependencies`/`security`.
- Upload audit JSON artifacts; fail the run if vulnerabilities remain after
  remediation.

### `dependabot.yml`

- Weekly `pip` updates for the root and `docs/` directories, plus
  `github-actions` updates. Group related deps (core, testing, linting, docs,
  actions) to reduce PR noise.

---

## 13. Build Order Checklist

Follow this order to scaffold, then implement, a new client:

1. Complete the **API source audit** (§2); resolve gaps before coding.
2. Scaffold the repo layout (§3): package dir, `tests/`, `docs/`, `.github/`,
   config files.
3. Write `exceptions.py` (§5), then `base_client.py` (§4.1–4.2).
4. Add `enums.py`, `models.py`, and `py.typed` (§6).
5. Implement one resource module + its client (§4.4), wire it into the
   aggregator client (§4.3) and `__init__.py` (§7).
6. Add `test_base_client.py`, `test_exceptions.py`, and the resource's
   `test_{resource}.py` (§9); reach 100% coverage for what exists.
7. Repeat 5–6 for each remaining resource group.
8. Author docs (§10): getting-started, one API reference page per group,
   reference pages, and guides.
9. Fill in `pyproject.toml`, `MANIFEST.in`, requirements files (§11); set the
   version in both required locations.
10. Add the workflows and Dependabot config (§12).
11. Validate locally before pushing:

```bash
black --check .
isort --check-only --profile=black --line-length=88 .
flake8 .
mypy {package}/ --strict
pytest --cov={package} --cov-report=term-missing
mkdocs build --clean
python -m build
twine check dist/*
```

12. Tag a release (`vX.Y.Z`) or dispatch the deployment workflow to publish to
    PyPI and deploy the docs.

A scaffold is **not** done until endpoint inventory, tests, docs, and coverage
all confirm coverage of the implemented surface. Do not mark API coverage
complete until those prove it.
