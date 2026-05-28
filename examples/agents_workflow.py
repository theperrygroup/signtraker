"""Agent workflow example: search, read, and (optionally) update.

Set ``SIGNTRAKER_API_KEY`` and ``SIGNTRAKER_SUBDOMAIN`` in the environment, then:

    python examples/agents_workflow.py
"""

from typing import Optional

from signtraker import NotFoundError, SignTrakerClient
from signtraker.models import Agent


def find_agent_by_email(client: SignTrakerClient, email: str) -> Optional[Agent]:
    """Find a single agent by email and return it as a typed model.

    Args:
        client: A configured SignTraker client.
        email: The email address to search for.

    Returns:
        The matching :class:`~signtraker.models.Agent`, or ``None`` if no agent
        matches.
    """
    matches = client.agents.list_agents(email=email)
    if not matches:
        return None
    return Agent.model_validate(matches[0])


def main() -> None:
    """Demonstrate searching for and reading an agent."""
    client = SignTrakerClient()
    agent = find_agent_by_email(client, "someone@example.com")
    if agent is None:
        print("No agent found for that email.")
        return

    print(f"Found agent #{agent.id}: {agent.first_name} {agent.last_name}")

    try:
        full = client.agents.get_agent(agent.id) if agent.id is not None else {}
        print("Office:", full.get("Office", {}).get("Name"))
    except NotFoundError:
        print("Agent disappeared between calls.")


if __name__ == "__main__":
    main()
