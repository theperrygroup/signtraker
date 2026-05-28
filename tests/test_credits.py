"""Tests for CreditsClient."""

import json

import responses

from signtraker import SignTrakerClient

BASE_URL = "https://test.signtraker.com"


class TestCreditsClient:
    """Unit tests for the credits endpoints."""

    @responses.activate
    def test_list_awards(self, client: SignTrakerClient) -> None:
        """list_awards forwards the awardedTo filter and returns the list."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/credits/awards",
            json=[{"Id": 1, "Name": "Spring"}],
            status=200,
        )
        result = client.credits.list_awards(awarded_to=123, top=10)
        assert result == [{"Id": 1, "Name": "Spring"}]
        url = responses.calls[0].request.url
        assert "awardedTo=123" in url
        assert "%24top=10" in url

    @responses.activate
    def test_create_award(self, client: SignTrakerClient) -> None:
        """create_award posts the payload and returns the created award."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/credits/awards",
            json={"Id": 2},
            status=200,
        )
        payload = {"Name": "Spring", "TotalAmount": 100, "Restrictions": ["Printing"]}
        assert client.credits.create_award(payload) == {"Id": 2}
        assert json.loads(responses.calls[0].request.body) == payload
