"""Tests for the exception hierarchy."""

from signtraker.exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    SignTrakerConfigError,
    SignTrakerError,
    ValidationError,
)


class TestExceptions:
    """Construction and inheritance of the exception classes."""

    def test_base_attributes(self) -> None:
        """The base error stores message, status code, and response data."""
        err = SignTrakerError("boom", 400, {"Message": "boom"})
        assert err.message == "boom"
        assert err.status_code == 400
        assert err.response_data == {"Message": "boom"}
        assert str(err) == "boom"

    def test_defaults(self) -> None:
        """Status code and response data default to None."""
        err = SignTrakerError("oops")
        assert err.status_code is None
        assert err.response_data is None

    def test_subclasses_inherit_base(self) -> None:
        """Every typed error is a SignTrakerError."""
        for klass in (
            SignTrakerConfigError,
            AuthenticationError,
            ValidationError,
            NotFoundError,
            RateLimitError,
            ServerError,
            NetworkError,
        ):
            instance = klass("msg")
            assert isinstance(instance, SignTrakerError)
