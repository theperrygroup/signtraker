"""Orders workflow example: list orders and build a create request.

The create call is commented out so the example is safe to run read-only.

Set ``SIGNTRAKER_API_KEY`` and ``SIGNTRAKER_SUBDOMAIN`` in the environment, then:

    python examples/orders_workflow.py
"""

from signtraker import SignTrakerClient
from signtraker.models import CreateOrderRequest


def main() -> None:
    """List recent signage orders and show how to build a create request."""
    client = SignTrakerClient()

    orders = client.orders.list_orders(top=5, orderby="Created")
    print(f"Fetched {len(orders)} order(s).")
    for order in orders:
        print(f"- #{order.get('OrderNumber')} status={order.get('Status')}")

    # Build (but do not send) a create request payload.
    request = CreateOrderRequest(
        agent_id=42,
        preset_id=7,
        street_number="123",
        street_name="Main St",
        city="Austin",
        state="TX",
        zip="78701",
    )
    payload = request.model_dump(by_alias=True, exclude_none=True)
    print("Prepared create-order payload:", payload)

    # Uncomment to actually create an order (National Accounts only):
    # result = client.orders.create_order(payload)
    # print("Created order:", result.get("OrderId"))


if __name__ == "__main__":
    main()
