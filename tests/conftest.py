"""Shared pytest fixtures for the signtraker test suite."""

from typing import Iterator

import pytest

from signtraker import SignTrakerClient

API_KEY = "test_api_key"
BASE_URL = "https://test.signtraker.com"

_ENV_VARS = (
    "SIGNTRAKER_API_KEY",
    "SIGNTRAKER_BASE_URL",
    "SIGNTRAKER_SUBDOMAIN",
    "SIGNTRAKER_TIMEOUT_SECONDS",
    "SIGNTRAKER_MAX_RETRIES",
    "SIGNTRAKER_RETRY_BACKOFF_SECONDS",
    "SIGNTRACKER_API_KEY",
    "SIGNTRACKER_BASE_URL",
    "SIGNTRACKER_SUBDOMAIN",
)


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove SignTraker environment variables so tests stay hermetic.

    Args:
        monkeypatch: The pytest monkeypatch fixture.
    """
    for name in _ENV_VARS:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def base_url() -> str:
    """Return the base URL used across mocked tests.

    Returns:
        The test base URL.
    """
    return BASE_URL


@pytest.fixture
def api_key() -> str:
    """Return the dummy API key used across mocked tests.

    Returns:
        The test API key.
    """
    return API_KEY


@pytest.fixture
def client() -> Iterator[SignTrakerClient]:
    """Build an aggregator client wired to the test base URL.

    Yields:
        A configured :class:`SignTrakerClient` instance.
    """
    yield SignTrakerClient(api_key=API_KEY, base_url=BASE_URL, retry_backoff_seconds=0)
