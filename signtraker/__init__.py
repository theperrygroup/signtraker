"""signtraker - Typed Python client for the SignTraker API.

Example:
    ```python
    from signtraker import SignTrakerClient

    client = SignTrakerClient(subdomain="theperrygroup")  # reads SIGNTRAKER_API_KEY
    for agent in client.agents.list_agents(top=5, orderby="LastName"):
        print(agent["FirstName"], agent["LastName"])
    ```
"""

from .agents import AgentsClient
from .base_client import BaseClient
from .change_orders import ChangeOrdersClient
from .client import SignTrakerClient
from .credits import CreditsClient
from .enterprises import EnterprisesClient
from .enums import (
    AwardRestriction,
    CountryCode,
    DiscountLevel,
    PaymentMode,
    SortDirection,
)
from .exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    SignTrakerConfigError,
    SignTrakerError,
    ValidationError,
)
from .models import (
    Agent,
    AgentAddress,
    Award,
    ChangeOrder,
    ChangeOrderCreateRequest,
    CreateOrderRequest,
    CreateOrderResult,
    Enterprise,
    JobSite,
    ManagerData,
    NamedRef,
    Office,
    OrderPreset,
    RequestRemovalRequest,
    RequestRemovalResult,
    SalesOrderRef,
    ServiceOrder,
    ServiceOrderCreateRequest,
    SignageOrder,
    SignTrakerModel,
)
from .offices import OfficesClient
from .order_presets import OrderPresetsClient
from .orders import OrdersClient
from .services import ServicesClient

__version__ = "0.1.0"

__all__ = [
    # Clients
    "SignTrakerClient",
    "BaseClient",
    "AgentsClient",
    "ChangeOrdersClient",
    "CreditsClient",
    "EnterprisesClient",
    "OfficesClient",
    "OrderPresetsClient",
    "OrdersClient",
    "ServicesClient",
    # Enums
    "PaymentMode",
    "DiscountLevel",
    "CountryCode",
    "AwardRestriction",
    "SortDirection",
    # Models
    "SignTrakerModel",
    "NamedRef",
    "Agent",
    "AgentAddress",
    "ManagerData",
    "JobSite",
    "SalesOrderRef",
    "ChangeOrder",
    "ServiceOrder",
    "SignageOrder",
    "Award",
    "Enterprise",
    "Office",
    "OrderPreset",
    "CreateOrderRequest",
    "CreateOrderResult",
    "ServiceOrderCreateRequest",
    "ChangeOrderCreateRequest",
    "RequestRemovalRequest",
    "RequestRemovalResult",
    # Exceptions
    "SignTrakerError",
    "SignTrakerConfigError",
    "AuthenticationError",
    "ValidationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
]
