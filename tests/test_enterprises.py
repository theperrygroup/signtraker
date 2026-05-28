"""Tests for EnterprisesClient."""

import responses

from signtraker import SignTrakerClient

BASE_URL = "https://test.signtraker.com"


class TestEnterprisesClient:
    """Unit tests for the enterprises endpoint."""

    @responses.activate
    def test_list_enterprises(self, client: SignTrakerClient) -> None:
        """list_enterprises returns the list and forwards OData params."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/enterprises",
            json=[{"Id": 1, "Name": "Ent"}],
            status=200,
        )
        result = client.enterprises.list_enterprises(orderby="Name")
        assert result == [{"Id": 1, "Name": "Ent"}]
        assert "%24orderby=Name" in responses.calls[0].request.url
