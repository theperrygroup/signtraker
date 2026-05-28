"""Tests for ServicesClient."""

import json

import pytest
import responses

from signtraker import SignTrakerClient
from signtraker.exceptions import NotFoundError

BASE_URL = "https://test.signtraker.com"


class TestServicesClient:
    """Unit tests for the service-orders endpoints."""

    @responses.activate
    def test_list_services(self, client: SignTrakerClient) -> None:
        """list_services returns the list and forwards OData params."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/services",
            json=[{"Id": 1}],
            status=200,
        )
        assert client.services.list_services(skip=2) == [{"Id": 1}]
        assert "%24skip=2" in responses.calls[0].request.url

    @responses.activate
    def test_get_service(self, client: SignTrakerClient) -> None:
        """get_service returns a single record."""
        responses.add(
            responses.GET, f"{BASE_URL}/api/services/3", json={"Id": 3}, status=200
        )
        assert client.services.get_service(3) == {"Id": 3}

    @responses.activate
    def test_get_service_not_found(self, client: SignTrakerClient) -> None:
        """A 404 raises NotFoundError."""
        responses.add(responses.GET, f"{BASE_URL}/api/services/9", json={}, status=404)
        with pytest.raises(NotFoundError):
            client.services.get_service(9)

    @responses.activate
    def test_create_service_returns_list(self, client: SignTrakerClient) -> None:
        """create_service posts the payload and returns a list of records."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/services",
            json=[{"Id": 7}],
            status=200,
        )
        payload = {"InstallId": 1, "PresetId": 2, "OverridePriceLimit": True}
        assert client.services.create_service(payload) == [{"Id": 7}]
        assert json.loads(responses.calls[0].request.body) == payload
