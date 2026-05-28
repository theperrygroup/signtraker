"""Tests for OrdersClient."""

import json

import pytest
import responses

from signtraker import SignTrakerClient
from signtraker.exceptions import NotFoundError

BASE_URL = "https://test.signtraker.com"


class TestOrdersClient:
    """Unit tests for the signage-orders endpoints."""

    @responses.activate
    def test_list_orders(self, client: SignTrakerClient) -> None:
        """list_orders returns the list and forwards OData params."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/orders",
            json=[{"Id": 1}],
            status=200,
        )
        assert client.orders.list_orders(top=1) == [{"Id": 1}]
        assert "%24top=1" in responses.calls[0].request.url

    @responses.activate
    def test_get_order(self, client: SignTrakerClient) -> None:
        """get_order returns a single record."""
        responses.add(
            responses.GET, f"{BASE_URL}/api/orders/8", json={"Id": 8}, status=200
        )
        assert client.orders.get_order(8) == {"Id": 8}

    @responses.activate
    def test_get_order_not_found(self, client: SignTrakerClient) -> None:
        """A 404 raises NotFoundError."""
        responses.add(responses.GET, f"{BASE_URL}/api/orders/9", json={}, status=404)
        with pytest.raises(NotFoundError):
            client.orders.get_order(9)

    @responses.activate
    def test_create_order(self, client: SignTrakerClient) -> None:
        """create_order posts the payload and returns the create result."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/orders",
            json={"Status": "Draft", "OrderId": 5},
            status=200,
        )
        payload = {"AgentId": 1, "PresetId": 2, "StreetName": "Main"}
        result = client.orders.create_order(payload)
        assert result == {"Status": "Draft", "OrderId": 5}
        assert json.loads(responses.calls[0].request.body) == payload

    @responses.activate
    def test_request_removal_with_body(self, client: SignTrakerClient) -> None:
        """request_removal posts the provided payload."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/orders/8/requestremoval",
            json={"DueDate": "2024-01-02T00:00:00.000Z"},
            status=200,
        )
        body = {"Notes": "remove please"}
        result = client.orders.request_removal(8, body)
        assert "DueDate" in result
        assert json.loads(responses.calls[0].request.body) == body

    @responses.activate
    def test_request_removal_default_body(self, client: SignTrakerClient) -> None:
        """request_removal defaults to an empty body when none is given."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/orders/8/requestremoval",
            json={},
            status=200,
        )
        assert client.orders.request_removal(8) == {}
        assert json.loads(responses.calls[0].request.body) == {}
