"""Base client: shared HTTP transport and error handling for SignTraker.

Every resource client subclasses :class:`BaseClient`, which owns the
``requests`` session, authentication, base-URL resolution, timeouts, retries,
and the mapping of HTTP status codes to typed exceptions.
"""

import os
import time
from typing import Any, Dict, List, NoReturn, Optional, Union

import requests

from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    SignTrakerConfigError,
    SignTrakerError,
    ValidationError,
)

DEFAULT_DOMAIN = "signtraker.com"
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_RETRIES = 0
DEFAULT_RETRY_BACKOFF_SECONDS = 0.5

ENV_API_KEY = "SIGNTRAKER_API_KEY"
ENV_BASE_URL = "SIGNTRAKER_BASE_URL"
ENV_SUBDOMAIN = "SIGNTRAKER_SUBDOMAIN"
ENV_TIMEOUT_SECONDS = "SIGNTRAKER_TIMEOUT_SECONDS"
ENV_MAX_RETRIES = "SIGNTRAKER_MAX_RETRIES"
ENV_RETRY_BACKOFF_SECONDS = "SIGNTRAKER_RETRY_BACKOFF_SECONDS"

# Brand-spelled fallbacks ("SignTracker" with a "c"). The canonical prefix is
# SIGNTRAKER_, but users naturally type the product brand, so these are honored.
ENV_API_KEY_ALT = "SIGNTRACKER_API_KEY"
ENV_BASE_URL_ALT = "SIGNTRACKER_BASE_URL"
ENV_SUBDOMAIN_ALT = "SIGNTRACKER_SUBDOMAIN"

_RETRYABLE_STATUS = frozenset({500, 502, 503, 504})
_MAX_MESSAGE_DEPTH = 6


def _getenv_with_alias(primary: str, alias: str) -> Optional[str]:
    """Read an environment variable, falling back to a brand-spelled alias.

    Args:
        primary: The canonical (``SIGNTRAKER_``) environment variable name.
        alias: The brand-spelled (``SIGNTRACKER_``) fallback name.

    Returns:
        The value of ``primary`` if set, otherwise the value of ``alias``, or
        ``None`` if neither is set.
    """
    value = os.getenv(primary)
    if value is not None:
        return value
    return os.getenv(alias)


def _parse_env_float(name: str, default: float) -> float:
    """Read a float from an environment variable, falling back to a default.

    Args:
        name: Environment variable name.
        default: Value returned when the variable is missing or invalid.

    Returns:
        The parsed float, or ``default`` on missing/invalid values.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _parse_env_int(name: str, default: int) -> int:
    """Read an int from an environment variable, falling back to a default.

    Args:
        name: Environment variable name.
        default: Value returned when the variable is missing or invalid.

    Returns:
        The parsed int, or ``default`` on missing/invalid values.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


_MESSAGE_KEYS = (
    "message",
    "error",
    "detail",
    "title",
    "Message",
    "Error",
    "Detail",
    "Title",
)


def _join_messages(items: List[Any], depth: int) -> Optional[str]:
    """Extract and join de-duplicated messages from a sequence of values.

    Args:
        items: The values to search.
        depth: Current recursion depth (each item is searched at ``depth + 1``).

    Returns:
        A ``"; "``-joined message string, or ``None`` if no message was found.
    """
    messages: List[str] = []
    for item in items:
        found = _extract_error_message(item, depth + 1)
        if found and found not in messages:
            messages.append(found)
    return "; ".join(messages) if messages else None


def _extract_from_dict(payload: Dict[str, Any], depth: int) -> Optional[str]:
    """Find a message inside a dict by known keys, wrappers, then recursion.

    Args:
        payload: The dict to search.
        depth: Current recursion depth.

    Returns:
        A human-readable message, or ``None`` if none could be found.
    """
    for key in _MESSAGE_KEYS:
        if key in payload:
            found = _extract_error_message(payload[key], depth + 1)
            if found:
                return found
    if len(payload) == 1:
        (only_value,) = payload.values()
        found = _extract_error_message(only_value, depth + 1)
        if found:
            return found
    return _join_messages(list(payload.values()), depth)


def _extract_error_message(payload: Any, _depth: int = 0) -> Optional[str]:
    """Recursively find a human-readable message in an error payload.

    The SignTraker API does not document its error envelope, so this helper
    searches common message fields (in both ``camelCase`` and ``PascalCase``),
    unwraps single-key wrapper objects, and recurses into nested structures.

    Args:
        payload: Parsed response payload (dict, list, or scalar).
        _depth: Internal recursion depth guard.

    Returns:
        A human-readable message, or ``None`` if none could be found.
    """
    if _depth > _MAX_MESSAGE_DEPTH:
        return None
    if isinstance(payload, str):
        return payload.strip() or None
    if isinstance(payload, dict):
        return _extract_from_dict(payload, _depth)
    if isinstance(payload, list):
        return _join_messages(payload, _depth)
    if _depth == 0 and payload is not None:
        return str(payload)
    return None


class BaseClient:
    """Base client with shared request/response handling.

    Resolves authentication and the tenant-specific base URL, then exposes thin
    HTTP verb helpers used by every resource client.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        subdomain: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
    ) -> None:
        """Initialize the base client.

        The base URL is resolved from the first available of: ``base_url``,
        ``subdomain`` (expanded to ``https://{subdomain}.signtraker.com``), the
        ``SIGNTRAKER_BASE_URL`` env var, or the ``SIGNTRAKER_SUBDOMAIN`` env var.

        Args:
            api_key: API key. Falls back to the ``SIGNTRAKER_API_KEY`` env var.
            base_url: Full API base URL (e.g.
                ``"https://acme.signtraker.com"``). Overrides ``subdomain``.
            subdomain: Tenant subdomain used to build the base URL when
                ``base_url`` is not provided.
            timeout_seconds: Per-request timeout. Falls back to env/default.
            max_retries: Retry attempts for transient failures.
            retry_backoff_seconds: Base backoff between retries (exponential).

        Raises:
            AuthenticationError: If no API key can be resolved.
            SignTrakerConfigError: If no base URL or subdomain can be resolved.
        """
        self.api_key = api_key or _getenv_with_alias(ENV_API_KEY, ENV_API_KEY_ALT)
        if not self.api_key:
            raise AuthenticationError(
                "API key is required. Set SIGNTRAKER_API_KEY or pass api_key."
            )
        self.base_url = self._resolve_base_url(base_url, subdomain)
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
                "Authorization": f"ST-API {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    @staticmethod
    def _resolve_base_url(base_url: Optional[str], subdomain: Optional[str]) -> str:
        """Resolve the tenant-specific base URL.

        Args:
            base_url: Explicit base URL, if provided.
            subdomain: Explicit tenant subdomain, if provided.

        Returns:
            The resolved base URL with any trailing slash removed.

        Raises:
            SignTrakerConfigError: If neither a base URL nor a subdomain can be
                resolved from arguments or environment variables.
        """
        resolved = base_url or _getenv_with_alias(ENV_BASE_URL, ENV_BASE_URL_ALT)
        if resolved:
            return resolved.rstrip("/")
        chosen_subdomain = subdomain or _getenv_with_alias(
            ENV_SUBDOMAIN, ENV_SUBDOMAIN_ALT
        )
        if chosen_subdomain:
            return f"https://{chosen_subdomain}.{DEFAULT_DOMAIN}"
        raise SignTrakerConfigError(
            "A base URL is required. Pass base_url or subdomain, or set "
            "SIGNTRAKER_BASE_URL or SIGNTRAKER_SUBDOMAIN."
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        data: Optional[Any] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make an HTTP request with retries on transient failures.

        Args:
            method: HTTP method (``GET``, ``POST``, ``PUT``, ``PATCH``,
                ``DELETE``).
            endpoint: Path relative to the base URL (e.g. ``"api/agents"``).
            json_data: JSON-serializable request body.
            data: Raw request body (used instead of ``json_data`` when set).
            params: Query-string parameters.
            headers: Per-request header overrides merged over the session
                headers (e.g. a different ``Content-Type``).
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload (a dict, list, or ``{}`` for empty
            responses).

        Raises:
            NetworkError: If the request fails after exhausting retries.
            SignTrakerError: Or a subclass, based on the response status code.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        effective_timeout = (
            float(timeout_seconds)
            if timeout_seconds is not None
            else self.timeout_seconds
        )
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=json_data,
                    data=data,
                    params=params,
                    headers=headers,
                    timeout=effective_timeout,
                )
                if (
                    response.status_code in _RETRYABLE_STATUS
                    and attempt < self.max_retries
                ):
                    time.sleep(self.retry_backoff_seconds * (2**attempt))
                    continue
                return self._handle_response(response)
            except requests.exceptions.RequestException as exc:
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * (2**attempt))
                    continue
                raise NetworkError(f"Network error: {exc}") from exc
        raise NetworkError(
            "Request failed after exhausting retries."
        )  # pragma: no cover

    def _handle_response(self, response: requests.Response) -> Any:
        """Parse a response and map error status codes to typed exceptions.

        Args:
            response: The HTTP response to handle.

        Returns:
            The parsed payload for successful responses (``{}`` for ``204``).

        Raises:
            ValidationError: On HTTP 400.
            AuthenticationError: On HTTP 401/403.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            ServerError: On HTTP 5xx.
            SignTrakerError: On any other non-success status code.
        """
        if response.status_code == 204:
            return {}
        try:
            payload: Any = response.json() if response.content else {}
        except ValueError:
            payload = {"message": response.text}

        if 200 <= response.status_code < 300:
            return payload
        self._raise_for_status(response.status_code, payload)

    @staticmethod
    def _raise_for_status(status: int, payload: Any) -> NoReturn:
        """Map a non-success status code to a typed exception and raise it.

        Args:
            status: The HTTP status code.
            payload: The parsed (or wrapped) response payload.

        Raises:
            ValidationError: On HTTP 400.
            AuthenticationError: On HTTP 401/403.
            NotFoundError: On HTTP 404.
            RateLimitError: On HTTP 429.
            ServerError: On HTTP 5xx.
            SignTrakerError: On any other non-success status code.
        """
        if isinstance(payload, dict):
            response_data: Dict[str, Any] = payload
        else:
            response_data = {"detail": payload}
        message = (
            _extract_error_message(payload) or f"Request failed with status {status}"
        )
        if status == 400:
            raise ValidationError(message, status, response_data)
        if status in (401, 403):
            raise AuthenticationError(message, status, response_data)
        if status == 404:
            raise NotFoundError(message, status, response_data)
        if status == 429:
            raise RateLimitError(message, status, response_data)
        if 500 <= status < 600:
            raise ServerError(message, status, response_data)
        raise SignTrakerError(message, status, response_data)

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make a ``GET`` request.

        Args:
            endpoint: Path relative to the base URL.
            params: Query-string parameters.
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload.
        """
        return self._request(
            "GET", endpoint, params=params, timeout_seconds=timeout_seconds
        )

    def post(
        self,
        endpoint: str,
        *,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make a ``POST`` request.

        Args:
            endpoint: Path relative to the base URL.
            json_data: JSON-serializable request body.
            params: Query-string parameters.
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload.
        """
        return self._request(
            "POST",
            endpoint,
            json_data=json_data,
            params=params,
            timeout_seconds=timeout_seconds,
        )

    def put(
        self,
        endpoint: str,
        *,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make a ``PUT`` request.

        Args:
            endpoint: Path relative to the base URL.
            json_data: JSON-serializable request body.
            params: Query-string parameters.
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload.
        """
        return self._request(
            "PUT",
            endpoint,
            json_data=json_data,
            params=params,
            timeout_seconds=timeout_seconds,
        )

    def patch(
        self,
        endpoint: str,
        *,
        json_data: Optional[Union[Dict[str, Any], List[Any]]] = None,
        params: Optional[Dict[str, Any]] = None,
        content_type: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make a ``PATCH`` request.

        Args:
            endpoint: Path relative to the base URL.
            json_data: JSON-serializable request body.
            params: Query-string parameters.
            content_type: Optional ``Content-Type`` override (e.g.
                ``"application/merge-patch+json"`` for JSON Merge Patch).
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload.
        """
        headers = {"Content-Type": content_type} if content_type is not None else None
        return self._request(
            "PATCH",
            endpoint,
            json_data=json_data,
            params=params,
            headers=headers,
            timeout_seconds=timeout_seconds,
        )

    def delete(
        self,
        endpoint: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """Make a ``DELETE`` request.

        Args:
            endpoint: Path relative to the base URL.
            params: Query-string parameters.
            timeout_seconds: Per-request timeout override.

        Returns:
            The parsed response payload.
        """
        return self._request(
            "DELETE", endpoint, params=params, timeout_seconds=timeout_seconds
        )
