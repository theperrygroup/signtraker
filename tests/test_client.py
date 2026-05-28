"""Tests for the SignTrakerClient aggregator."""

import pytest

from signtraker import SignTrakerClient
from signtraker.agents import AgentsClient
from signtraker.change_orders import ChangeOrdersClient
from signtraker.credits import CreditsClient
from signtraker.enterprises import EnterprisesClient
from signtraker.offices import OfficesClient
from signtraker.order_presets import OrderPresetsClient
from signtraker.orders import OrdersClient
from signtraker.services import ServicesClient

BASE_URL = "https://test.signtraker.com"

_PROPERTIES = [
    ("agents", AgentsClient),
    ("change_orders", ChangeOrdersClient),
    ("credits", CreditsClient),
    ("enterprises", EnterprisesClient),
    ("offices", OfficesClient),
    ("order_presets", OrderPresetsClient),
    ("orders", OrdersClient),
    ("services", ServicesClient),
]


class TestSignTrakerClient:
    """Aggregator wiring and configuration propagation."""

    @pytest.mark.parametrize("name,klass", _PROPERTIES)
    def test_property_type_and_caching(
        self, client: SignTrakerClient, name: str, klass: type
    ) -> None:
        """Each sub-client property returns the right type and is cached."""
        sub = getattr(client, name)
        assert isinstance(sub, klass)
        assert getattr(client, name) is sub

    def test_config_propagates_to_sub_clients(self) -> None:
        """Constructor config flows to sub-clients."""
        client = SignTrakerClient(
            api_key="k",
            subdomain="acme",
            timeout_seconds=11,
            max_retries=2,
            retry_backoff_seconds=0,
        )
        assert client.agents.base_url == "https://acme.signtraker.com"
        assert client.agents.timeout_seconds == 11.0
        assert client.agents.max_retries == 2
        assert client.agents.session.headers["Authorization"] == "ST-API k"

    def test_load_dotenv_invokes_loader(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """When load_dotenv is True the dotenv loader is invoked."""
        called = {}
        monkeypatch.setattr(
            "dotenv.load_dotenv",
            lambda *args, **kwargs: called.setdefault("loaded", True),
        )
        client = SignTrakerClient(api_key="k", base_url=BASE_URL, load_dotenv=True)
        assert called.get("loaded") is True
        assert client.agents.base_url == BASE_URL
