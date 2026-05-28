"""Pydantic data models for SignTraker API payloads.

Models are optional sugar: every client method also accepts and returns plain
dictionaries. The models give IDE support and validation for callers who want
it. Because the API uses PascalCase JSON keys, each field declares a PascalCase
alias while keeping a Pythonic ``snake_case`` attribute name. ``populate_by_name``
is enabled, so you may construct a model with either the alias or the attribute
name.

Example:
    ```python
    from signtraker.models import Agent

    agent = Agent.model_validate(client.agents.get_agent(123))
    print(agent.first_name, agent.email)
    payload = agent.model_dump(by_alias=True, exclude_none=True)
    ```
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .enums import DiscountLevel, PaymentMode


class SignTrakerModel(BaseModel):
    """Base model enabling alias population and tolerance of unknown fields."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")


class NamedRef(SignTrakerModel):
    """A lightweight ``{Id, Name}`` reference used throughout the API."""

    id: Optional[int] = Field(default=None, alias="Id", description="Identifier")
    name: Optional[str] = Field(default=None, alias="Name", description="Display name")


class AgentAddress(SignTrakerModel):
    """Postal address for an agent."""

    street: Optional[str] = Field(default=None, alias="Street")
    street2: Optional[str] = Field(default=None, alias="Street2")
    city: Optional[str] = Field(default=None, alias="City")
    state: Optional[str] = Field(
        default=None, alias="State", description="2-character state/province code"
    )
    zip: Optional[str] = Field(default=None, alias="Zip")
    country_code: Optional[str] = Field(
        default=None, alias="CountryCode", description="One of US, CA, AU"
    )


class ManagerData(SignTrakerModel):
    """Manager-specific settings attached to an agent."""

    discount_level: Optional[DiscountLevel] = Field(default=None, alias="DiscountLevel")
    enable_rebills: Optional[bool] = Field(default=None, alias="EnableRebills")
    initial_rental_duration: Optional[int] = Field(
        default=None, alias="InitialRentalDuration"
    )
    rebill_interval: Optional[int] = Field(default=None, alias="RebillInterval")
    rebill_warning_lead_time: Optional[int] = Field(
        default=None, alias="RebillWarningLeadTime"
    )
    is_payer: Optional[bool] = Field(default=None, alias="IsPayer")
    disable_staff_billing_emails: Optional[bool] = Field(
        default=None, alias="DisableStaffBillingEmails"
    )
    cc_staff: Optional[bool] = Field(default=None, alias="CcStaff")
    cc_delegates: Optional[bool] = Field(default=None, alias="CcDelegates")
    is_virtual: Optional[bool] = Field(default=None, alias="IsVirtual")


class Agent(SignTrakerModel):
    """An agent record (used for both responses and create/update bodies)."""

    id: Optional[int] = Field(default=None, alias="Id")
    user_name: Optional[str] = Field(default=None, alias="UserName")
    email: Optional[str] = Field(default=None, alias="Email")
    email_confirmed: Optional[bool] = Field(default=None, alias="EmailConfirmed")
    first_name: Optional[str] = Field(default=None, alias="FirstName")
    last_name: Optional[str] = Field(default=None, alias="LastName")
    is_inactive: Optional[bool] = Field(default=None, alias="IsInactive")
    is_locked: Optional[bool] = Field(default=None, alias="IsLocked")
    cc_email: Optional[str] = Field(
        default=None,
        alias="CcEmail",
        description="Emails to BCC on notifications; semi-colon separated",
    )
    invitation_sent: Optional[bool] = Field(default=None, alias="InvitationSent")
    office: Optional[NamedRef] = Field(default=None, alias="Office")
    manager: Optional[NamedRef] = Field(default=None, alias="Manager")
    address: Optional[AgentAddress] = Field(default=None, alias="Address")
    office_phone: Optional[str] = Field(default=None, alias="OfficePhone")
    cellular_phone: Optional[str] = Field(default=None, alias="CellularPhone")
    payment_mode: Optional[PaymentMode] = Field(default=None, alias="PaymentMode")
    basic_install_price: Optional[float] = Field(
        default=None, alias="BasicInstallPrice"
    )
    broker_id: Optional[str] = Field(default=None, alias="BrokerId")
    default_post_type: Optional[NamedRef] = Field(default=None, alias="DefaultPostType")
    notes: Optional[str] = Field(default=None, alias="Notes")
    receive_marketing_emails: Optional[bool] = Field(
        default=None, alias="ReceiveMarketingEmails"
    )
    terms_accepted: Optional[bool] = Field(default=None, alias="TermsAccepted")
    enable_subscription: Optional[bool] = Field(
        default=None, alias="EnableSubscription"
    )
    subscription_price: Optional[float] = Field(default=None, alias="SubscriptionPrice")
    is_manager: Optional[bool] = Field(default=None, alias="IsManager")
    manager_data: Optional[ManagerData] = Field(default=None, alias="ManagerData")


class JobSite(SignTrakerModel):
    """A job-site (property) location attached to an order."""

    id: Optional[int] = Field(default=None, alias="Id")
    street_address: Optional[str] = Field(default=None, alias="StreetAddress")
    street_number: Optional[str] = Field(default=None, alias="StreetNumber")
    street_name: Optional[str] = Field(default=None, alias="StreetName")
    street_line2: Optional[str] = Field(default=None, alias="StreetLine2")
    city: Optional[str] = Field(default=None, alias="City")
    state: Optional[str] = Field(default=None, alias="State")
    zip: Optional[str] = Field(default=None, alias="Zip")
    country_code: Optional[str] = Field(default=None, alias="CountryCode")
    latitude: Optional[float] = Field(default=None, alias="Latitude")
    longitude: Optional[float] = Field(default=None, alias="Longitude")
    directions: Optional[str] = Field(default=None, alias="Directions")
    listing_number: Optional[str] = Field(default=None, alias="ListingNumber")


class SalesOrderRef(SignTrakerModel):
    """A reference to a sales order with its total."""

    id: Optional[int] = Field(default=None, alias="Id")
    order_total: Optional[float] = Field(default=None, alias="OrderTotal")


class ChangeOrder(SignTrakerModel):
    """A change order or service order summary record."""

    id: Optional[int] = Field(default=None, alias="Id")
    order_number: Optional[int] = Field(default=None, alias="OrderNumber")
    service_type: Optional[NamedRef] = Field(default=None, alias="ServiceType")
    notes: Optional[str] = Field(default=None, alias="Notes")
    status: Optional[str] = Field(default=None, alias="Status")
    created: Optional[datetime] = Field(default=None, alias="Created")
    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
    is_due_date_definitive: Optional[bool] = Field(
        default=None, alias="IsDueDateDefinitive"
    )
    completion_date: Optional[datetime] = Field(default=None, alias="CompletionDate")
    sales_order: Optional[SalesOrderRef] = Field(default=None, alias="SalesOrder")
    job_site: Optional[JobSite] = Field(default=None, alias="JobSite")
    agent: Optional[NamedRef] = Field(default=None, alias="Agent")


class ServiceOrder(ChangeOrder):
    """A service order record (same shape as a change order)."""


class SignageOrder(SignTrakerModel):
    """A signage order record."""

    id: Optional[int] = Field(default=None, alias="Id")
    order_number: Optional[int] = Field(default=None, alias="OrderNumber")
    status: Optional[str] = Field(default=None, alias="Status")
    notes: Optional[str] = Field(default=None, alias="Notes")
    created: Optional[datetime] = Field(default=None, alias="Created")
    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
    is_due_date_definitive: Optional[bool] = Field(
        default=None, alias="IsDueDateDefinitive"
    )
    date_installed: Optional[datetime] = Field(default=None, alias="DateInstalled")
    removal_request_date: Optional[datetime] = Field(
        default=None, alias="RemovalRequestDate"
    )
    removal_due_date: Optional[datetime] = Field(default=None, alias="RemovalDueDate")
    is_removal_due_date_definitive: Optional[bool] = Field(
        default=None, alias="IsRemovalDueDateDefinitive"
    )
    removal_date: Optional[datetime] = Field(default=None, alias="RemovalDate")
    rebill_interval: Optional[int] = Field(default=None, alias="RebillInterval")
    next_rebill_date: Optional[datetime] = Field(default=None, alias="NextRebillDate")
    sales_order: Optional[SalesOrderRef] = Field(default=None, alias="SalesOrder")
    job_site: Optional[JobSite] = Field(default=None, alias="JobSite")
    post_type: Optional[NamedRef] = Field(default=None, alias="PostType")
    agent: Optional[NamedRef] = Field(default=None, alias="Agent")


class Award(SignTrakerModel):
    """A credit award record."""

    id: Optional[int] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Name")
    awarded_by: Optional[NamedRef] = Field(default=None, alias="AwardedBy")
    awarded_date: Optional[datetime] = Field(default=None, alias="AwardedDate")
    awarded_to: Optional[NamedRef] = Field(default=None, alias="AwardedTo")
    expiration_date: Optional[datetime] = Field(default=None, alias="ExpirationDate")
    total_amount: Optional[float] = Field(default=None, alias="TotalAmount")
    remaining_amount: Optional[float] = Field(default=None, alias="RemainingAmount")
    restrictions: Optional[List[str]] = Field(default=None, alias="Restrictions")


class Enterprise(SignTrakerModel):
    """An enterprise (``{Id, Name}``)."""

    id: Optional[int] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Name")


class Office(SignTrakerModel):
    """An office (``{Id, Name}``)."""

    id: Optional[int] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Name")


class OrderPreset(SignTrakerModel):
    """An order preset (``{Id, Name}``)."""

    id: Optional[int] = Field(default=None, alias="Id")
    name: Optional[str] = Field(default=None, alias="Name")


class CreateOrderRequest(SignTrakerModel):
    """Request body for creating a signage order (National Accounts)."""

    street_number: Optional[str] = Field(default=None, alias="StreetNumber")
    street_name: Optional[str] = Field(default=None, alias="StreetName")
    city: Optional[str] = Field(default=None, alias="City")
    state: Optional[str] = Field(default=None, alias="State")
    zip: Optional[str] = Field(default=None, alias="Zip")
    apartment: Optional[str] = Field(default=None, alias="Apartment")
    directions: Optional[str] = Field(default=None, alias="Directions")
    listing_number: Optional[str] = Field(default=None, alias="ListingNumber")
    external_id: Optional[str] = Field(default=None, alias="ExternalID")
    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
    notes: Optional[str] = Field(default=None, alias="Notes")
    agent_id: int = Field(alias="AgentId", description="Agent identifier (required)")
    preset_id: int = Field(
        alias="PresetId", description="Order preset identifier (required)"
    )


class CreateOrderResult(SignTrakerModel):
    """Result returned when creating a signage order."""

    status: Optional[str] = Field(default=None, alias="Status")
    message: Optional[str] = Field(default=None, alias="Message")
    request_id: Optional[int] = Field(default=None, alias="RequestId")
    order_id: Optional[int] = Field(default=None, alias="OrderId")


class _PresetCreateRequest(SignTrakerModel):
    """Shared body for preset-based service/change-order creation."""

    install_id: int = Field(alias="InstallId", description="Install identifier")
    preset_id: int = Field(alias="PresetId", description="Preset identifier")
    notes: Optional[str] = Field(default=None, alias="Notes")
    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
    override_price_limit: bool = Field(
        alias="OverridePriceLimit", description="Override the preset price limit"
    )


class ServiceOrderCreateRequest(_PresetCreateRequest):
    """Request body for creating a service order."""


class ChangeOrderCreateRequest(_PresetCreateRequest):
    """Request body for creating a change order (National Accounts)."""


class RequestRemovalRequest(SignTrakerModel):
    """Request body for requesting signage removal."""

    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
    notes: Optional[str] = Field(default=None, alias="Notes")


class RequestRemovalResult(SignTrakerModel):
    """Result returned when requesting signage removal."""

    due_date: Optional[datetime] = Field(default=None, alias="DueDate")
