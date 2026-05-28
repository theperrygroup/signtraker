# Orders & Services

SignTraker models three order-like surfaces: signage **orders**, **services**,
and **change orders**. Each has its own resource group.

## Signage orders

```python
# List and read
orders = client.orders.list_orders(top=10, orderby="Created")
order = client.orders.get_order(456)

# Create (National Accounts; requires an order preset)
result = client.orders.create_order(
    {
        "AgentId": 42,
        "PresetId": 7,
        "StreetNumber": "123",
        "StreetName": "Main St",
        "City": "Austin",
        "State": "TX",
        "Zip": "78701",
    }
)
print(result["OrderId"], result["Status"])

# Request removal of installed signage
client.orders.request_removal(456, {"Notes": "Listing closed"})
```

## Services

```python
services = client.services.list_services(top=10)
service = client.services.get_service(789)

# Create a service order (returns a list of created records)
created = client.services.create_service(
    {"InstallId": 456, "PresetId": 3, "OverridePriceLimit": False}
)
```

## Change orders

```python
change_orders = client.change_orders.list_change_orders(top=10)
change_order = client.change_orders.get_change_order(321)

# Create a change order (National Accounts)
client.change_orders.create_change_order(
    {"InstallId": 456, "PresetId": 5, "OverridePriceLimit": False}
)
```

!!! note "National Accounts"
    Creating signage and change orders relies on Order Presets, which are
    available to National Accounts and not to individual Licensee portals.
