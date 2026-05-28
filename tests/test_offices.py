"""Tests for OfficesClient."""

import responses

from signtraker import SignTrakerClient

BASE_URL = "https://test.signtraker.com"


class TestOfficesClient:
    """Unit tests for the offices endpoint."""

    @responses.activate
    def test_list_offices(self, client: SignTrakerClient) -> None:
        """list_offices forwards the enterpriseId filter and returns the list."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/offices",
            json=[{"Id": 1, "Name": "HQ"}],
            status=200,
        )
        result = client.offices.list_offices(enterprise_id=42, top=3)
        assert result == [{"Id": 1, "Name": "HQ"}]
        url = responses.calls[0].request.url
        assert "enterpriseId=42" in url
        assert "%24top=3" in url
