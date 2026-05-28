"""Error-handling example for the signtraker client.

Set ``SIGNTRAKER_API_KEY`` and ``SIGNTRAKER_SUBDOMAIN`` in the environment, then:

    python examples/error_handling.py
"""

from signtraker import NotFoundError, SignTrakerClient, SignTrakerError


def main() -> None:
    """Demonstrate catching typed errors from the client."""
    client = SignTrakerClient(max_retries=2, retry_backoff_seconds=0.5)

    try:
        client.agents.get_agent(999_999_999)
    except NotFoundError:
        print("Expected: agent not found (404).")
    except SignTrakerError as exc:
        print(f"API error {exc.status_code}: {exc.message}")
        print("Raw payload:", exc.response_data)


if __name__ == "__main__":
    main()
