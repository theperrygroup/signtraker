"""Tests for ChangeOrdersClient."""

import json

import pytest
import responses

from signtraker import SignTrakerClient
from signtraker.exceptions import NotFoundError

BASE_URL = "https://test.signtraker.com"


class TestChangeOrdersClient:
    """Unit tests for the change-orders endpoints."""

    @responses.activate
    def test_list_change_orders(self, client: SignTrakerClient) -> None:
        """list_change_orders returns the list and forwards OData params."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/changeorders",
            json=[{"Id": 1}],
            status=200,
        )
        assert client.change_orders.list_change_orders(top=2) == [{"Id": 1}]
        assert "%24top=2" in responses.calls[0].request.url

    @responses.activate
    def test_get_change_order(self, client: SignTrakerClient) -> None:
        """get_change_order returns a single record."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/changeorders/4",
            json={"Id": 4},
            status=200,
        )
        assert client.change_orders.get_change_order(4) == {"Id": 4}

    @responses.activate
    def test_get_change_order_not_found(self, client: SignTrakerClient) -> None:
        """A 404 raises NotFoundError."""
        responses.add(
            responses.GET, f"{BASE_URL}/api/changeorders/9", json={}, status=404
        )
        with pytest.raises(NotFoundError):
            client.change_orders.get_change_order(9)

    @responses.activate
    def test_create_change_order(self, client: SignTrakerClient) -> None:
        """create_change_order posts the payload."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/changeorders",
            json={"Id": 5},
            status=200,
        )
        payload = {"InstallId": 1, "PresetId": 2, "OverridePriceLimit": False}
        assert client.change_orders.create_change_order(payload) == {"Id": 5}
        assert json.loads(responses.calls[0].request.body) == payload
