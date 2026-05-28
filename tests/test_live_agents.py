"""Opt-in live integration tests against the real SignTraker API.

These tests are skipped unless a real API key is present in the environment
(``SIGNTRAKER_API_KEY`` or the brand-spelled ``SIGNTRACKER_API_KEY``). They make
read-only calls only. Provide a host via ``SIGNTRAKER_BASE_URL`` or
``SIGNTRAKER_SUBDOMAIN``; otherwise the ``theperrygroup`` tenant is used.

Run them with, for example:

    SIGNTRAKER_API_KEY=... SIGNTRAKER_SUBDOMAIN=theperrygroup pytest -m live
"""

import os

import pytest

from signtraker import SignTrakerClient

_API_KEY = os.getenv("SIGNTRAKER_API_KEY") or os.getenv("SIGNTRACKER_API_KEY")
_BASE_URL = os.getenv("SIGNTRAKER_BASE_URL") or os.getenv("SIGNTRACKER_BASE_URL")
_SUBDOMAIN = (
    os.getenv("SIGNTRAKER_SUBDOMAIN")
    or os.getenv("SIGNTRACKER_SUBDOMAIN")
    or "theperrygroup"
)

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not _API_KEY, reason="No SignTraker API key set in the environment"
    ),
]


@pytest.fixture
def live_client() -> SignTrakerClient:
    """Build a client pointed at the real API using environment credentials.

    Returns:
        A configured :class:`SignTrakerClient`.
    """
    return SignTrakerClient(api_key=_API_KEY, base_url=_BASE_URL, subdomain=_SUBDOMAIN)


def test_list_agents_live(live_client: SignTrakerClient) -> None:
    """Listing a single agent returns a JSON list from the live API."""
    agents = live_client.agents.list_agents(top=1)
    assert isinstance(agents, list)


def test_list_offices_live(live_client: SignTrakerClient) -> None:
    """Listing offices returns a JSON list from the live API."""
    offices = live_client.offices.list_offices(top=1)
    assert isinstance(offices, list)
