"""Quickstart example for the signtraker client.

Set ``SIGNTRAKER_API_KEY`` and ``SIGNTRAKER_SUBDOMAIN`` in the environment, then:

    python examples/quickstart.py
"""

from signtraker import SignTrakerClient


def main() -> None:
    """List the first few agents and print their names."""
    client = SignTrakerClient()  # reads SIGNTRAKER_API_KEY + SIGNTRAKER_SUBDOMAIN
    agents = client.agents.list_agents(top=5, orderby="LastName")
    print(f"Fetched {len(agents)} agent(s).")
    for agent in agents:
        print(f"- {agent.get('FirstName')} {agent.get('LastName')}")


if __name__ == "__main__":
    main()
