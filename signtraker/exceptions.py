"""Custom exceptions for the SignTraker API client.

The hierarchy is rooted at :class:`SignTrakerError`. Every error carries the
HTTP ``status_code`` (when applicable) and the parsed ``response_data`` so
callers can inspect the failure without re-parsing the response.
"""

from typing import Any, Dict, Optional


class SignTrakerError(Exception):
    """Base exception for all SignTraker API errors.

    Attributes:
        message: Human-readable error message.
        status_code: HTTP status code associated with the error, if any.
        response_data: Parsed response payload associated with the error, if any.
    """

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


class SignTrakerConfigError(SignTrakerError):
    """Raised when the client is misconfigured (e.g. no base URL/subdomain)."""


class AuthenticationError(SignTrakerError):
    """Raised when authentication fails or is missing (HTTP 401/403)."""


class ValidationError(SignTrakerError):
    """Raised when request validation fails (HTTP 400)."""


class NotFoundError(SignTrakerError):
    """Raised when a requested resource does not exist (HTTP 404)."""


class RateLimitError(SignTrakerError):
    """Raised when the API rate limit is exceeded (HTTP 429)."""


class ServerError(SignTrakerError):
    """Raised on server-side failures (HTTP 5xx)."""


class NetworkError(SignTrakerError):
    """Raised when the network request fails before a response is received."""
