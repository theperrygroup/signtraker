"""Tests for OrderPresetsClient."""

import responses

from signtraker import SignTrakerClient

BASE_URL = "https://test.signtraker.com"


class TestOrderPresetsClient:
    """Unit tests for the order-presets endpoint."""

    @responses.activate
    def test_list_order_presets(self, client: SignTrakerClient) -> None:
        """list_order_presets returns the list and forwards OData params."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/orderpresets",
            json=[{"Id": 1, "Name": "Basic"}],
            status=200,
        )
        result = client.order_presets.list_order_presets(filter="Name eq 'Basic'")
        assert result == [{"Id": 1, "Name": "Basic"}]
        assert "%24filter=" in responses.calls[0].request.url
