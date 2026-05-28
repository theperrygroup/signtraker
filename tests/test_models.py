"""Tests for the Pydantic data models."""

from datetime import datetime

from signtraker.models import (
    Agent,
    Award,
    ChangeOrder,
    ChangeOrderCreateRequest,
    CreateOrderRequest,
    CreateOrderResult,
    Enterprise,
    JobSite,
    Office,
    OrderPreset,
    RequestRemovalRequest,
    RequestRemovalResult,
    SalesOrderRef,
    ServiceOrder,
    ServiceOrderCreateRequest,
    SignageOrder,
)

AGENT_PAYLOAD = {
    "Id": 7,
    "UserName": "jdoe",
    "Email": "j@d.com",
    "FirstName": "Jane",
    "LastName": "Doe",
    "Office": {"Id": 1, "Name": "HQ"},
    "Address": {"State": "TX", "CountryCode": "US"},
    "PaymentMode": "ACH",
    "CellularPhone": "555-1212",
    "ManagerData": {"DiscountLevel": "Gold", "IsVirtual": True},
}


class TestAgentModel:
    """Round-tripping of the Agent model."""

    def test_validate_from_pascal_case(self) -> None:
        """The model parses PascalCase API payloads."""
        agent = Agent.model_validate(AGENT_PAYLOAD)
        assert agent.id == 7
        assert agent.first_name == "Jane"
        assert agent.office is not None and agent.office.name == "HQ"
        assert agent.payment_mode is not None and agent.payment_mode.value == "ACH"
        assert agent.manager_data is not None
        assert agent.manager_data.discount_level is not None
        assert agent.manager_data.discount_level.value == "Gold"
        assert agent.address is not None and agent.address.state == "TX"

    def test_dump_by_alias(self) -> None:
        """The model serializes back to PascalCase keys."""
        agent = Agent.model_validate(AGENT_PAYLOAD)
        dumped = agent.model_dump(by_alias=True, exclude_none=True)
        assert dumped["FirstName"] == "Jane"
        assert dumped["Office"]["Name"] == "HQ"

    def test_extra_fields_preserved(self) -> None:
        """Unknown fields are preserved (extra='allow')."""
        agent = Agent.model_validate({**AGENT_PAYLOAD, "NewField": 123})
        dumped = agent.model_dump(by_alias=True)
        assert dumped["NewField"] == 123


class TestOrderModels:
    """Order-related models and request bodies."""

    def test_change_order_parses_datetime(self) -> None:
        """Timestamp fields parse into datetime objects."""
        order = ChangeOrder.model_validate(
            {
                "Id": 1,
                "Status": "PaymentRequired",
                "Created": "2024-01-02T03:04:05.000Z",
            }
        )
        assert isinstance(order.created, datetime)
        assert order.status == "PaymentRequired"

    def test_service_order_is_change_order(self) -> None:
        """ServiceOrder shares the ChangeOrder shape."""
        service = ServiceOrder.model_validate({"Id": 2})
        assert isinstance(service, ChangeOrder)
        assert service.id == 2

    def test_signage_order(self) -> None:
        """SignageOrder parses its richer field set."""
        order = SignageOrder.model_validate(
            {
                "Id": 9,
                "Status": "Designing",
                "JobSite": {"Id": 3, "City": "Austin"},
                "PostType": {"Id": 1, "Name": "Standard"},
            }
        )
        assert order.id == 9
        assert order.job_site is not None and order.job_site.city == "Austin"
        assert order.post_type is not None and order.post_type.name == "Standard"

    def test_create_order_request_required_fields(self) -> None:
        """CreateOrderRequest serializes required and provided fields only."""
        req = CreateOrderRequest(agent_id=3, preset_id=9, street_name="Main")
        assert req.model_dump(by_alias=True, exclude_none=True) == {
            "StreetName": "Main",
            "AgentId": 3,
            "PresetId": 9,
        }

    def test_create_order_result(self) -> None:
        """CreateOrderResult parses the creation envelope."""
        result = CreateOrderResult.model_validate(
            {"Status": "Draft", "Message": "ok", "RequestId": 5, "OrderId": 11}
        )
        assert result.order_id == 11 and result.status == "Draft"

    def test_preset_create_requests(self) -> None:
        """Service and change-order create bodies share the preset shape."""
        service = ServiceOrderCreateRequest(
            install_id=1, preset_id=2, override_price_limit=False
        )
        change = ChangeOrderCreateRequest(
            InstallId=3, PresetId=4, OverridePriceLimit=True
        )
        assert service.install_id == 1 and service.override_price_limit is False
        assert change.install_id == 3 and change.override_price_limit is True

    def test_request_removal_models(self) -> None:
        """Request-removal request and result models round-trip."""
        req = RequestRemovalRequest(notes="please remove")
        assert req.model_dump(by_alias=True, exclude_none=True) == {
            "Notes": "please remove"
        }
        result = RequestRemovalResult.model_validate(
            {"DueDate": "2024-01-02T00:00:00.000Z"}
        )
        assert isinstance(result.due_date, datetime)


class TestSimpleModels:
    """The lightweight reference models."""

    def test_named_models(self) -> None:
        """Enterprise/Office/OrderPreset/SalesOrderRef parse ``{Id, Name}``."""
        assert Enterprise.model_validate({"Id": 1, "Name": "Ent"}).name == "Ent"
        assert Office.model_validate({"Id": 2, "Name": "Off"}).id == 2
        assert OrderPreset.model_validate({"Id": 3, "Name": "P"}).name == "P"
        assert (
            SalesOrderRef.model_validate({"Id": 4, "OrderTotal": 9.5}).order_total
            == 9.5
        )

    def test_job_site(self) -> None:
        """JobSite parses its address fields."""
        site = JobSite.model_validate({"Id": 1, "Latitude": 30.1, "Longitude": -97.7})
        assert site.latitude == 30.1 and site.longitude == -97.7

    def test_award(self) -> None:
        """Award parses references and restrictions."""
        award = Award.model_validate(
            {
                "Id": 1,
                "Name": "Spring",
                "AwardedTo": {"Id": 5, "Name": "Jane"},
                "Restrictions": ["Printing"],
            }
        )
        assert award.awarded_to is not None and award.awarded_to.id == 5
        assert award.restrictions == ["Printing"]
