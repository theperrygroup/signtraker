"""Tests for AgentsClient."""

import json

import pytest
import responses

from signtraker import SignTrakerClient
from signtraker.exceptions import NotFoundError

BASE_URL = "https://test.signtraker.com"


class TestAgentsClient:
    """Unit tests for the agents endpoints."""

    @responses.activate
    def test_list_agents(self, client: SignTrakerClient) -> None:
        """list_agents sends OData and email params and returns the list."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/agents",
            json=[{"Id": 1, "LastName": "Smith"}],
            status=200,
        )
        result = client.agents.list_agents(
            email="a@b.com", top=5, skip=15, orderby="LastName", select="Id"
        )
        assert result == [{"Id": 1, "LastName": "Smith"}]
        url = responses.calls[0].request.url
        assert "%24top=5" in url
        assert "%24skip=15" in url
        assert "%24orderby=LastName" in url
        assert "%24select=Id" in url
        assert "email=a%40b.com" in url

    @responses.activate
    def test_get_agent(self, client: SignTrakerClient) -> None:
        """get_agent returns the agent record."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/agents/7",
            json={"Id": 7, "FirstName": "Jane"},
            status=200,
        )
        assert client.agents.get_agent(7) == {"Id": 7, "FirstName": "Jane"}

    @responses.activate
    def test_get_agent_not_found(self, client: SignTrakerClient) -> None:
        """A 404 raises NotFoundError."""
        responses.add(responses.GET, f"{BASE_URL}/api/agents/99", json={}, status=404)
        with pytest.raises(NotFoundError):
            client.agents.get_agent(99)

    @responses.activate
    def test_create_agent(self, client: SignTrakerClient) -> None:
        """create_agent posts the payload and returns the created agent."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/agents",
            json={"Id": 12},
            status=200,
        )
        payload = {"UserName": "jdoe", "Email": "j@d.com"}
        assert client.agents.create_agent(payload) == {"Id": 12}
        assert json.loads(responses.calls[0].request.body) == payload

    @responses.activate
    def test_update_agent_uses_merge_patch(self, client: SignTrakerClient) -> None:
        """update_agent sends a merge-patch with the changes."""
        responses.add(
            responses.PATCH,
            f"{BASE_URL}/api/agents/7",
            json={"Id": 7, "FirstName": "Janet"},
            status=200,
        )
        result = client.agents.update_agent(7, {"FirstName": "Janet"})
        assert result["FirstName"] == "Janet"
        request = responses.calls[0].request
        assert request.headers["Content-Type"] == "application/merge-patch+json"
        assert json.loads(request.body) == {"FirstName": "Janet"}

    @responses.activate
    def test_activate_agent(self, client: SignTrakerClient) -> None:
        """activate_agent posts to the activate endpoint with the id param."""
        responses.add(
            responses.POST, f"{BASE_URL}/api/agents/activate", json={}, status=200
        )
        assert client.agents.activate_agent(7) == {}
        assert "id=7" in responses.calls[0].request.url

    @responses.activate
    def test_deactivate_agent(self, client: SignTrakerClient) -> None:
        """deactivate_agent posts to the deactivate endpoint with the id param."""
        responses.add(
            responses.POST,
            f"{BASE_URL}/api/agents/deactivate",
            json={},
            status=200,
        )
        assert client.agents.deactivate_agent(7) == {}
        assert "id=7" in responses.calls[0].request.url
