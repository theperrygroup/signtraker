"""Main aggregator client for the SignTraker API."""

from typing import Any, Dict, Optional

from .agents import AgentsClient
from .change_orders import ChangeOrdersClient
from .credits import CreditsClient
from .enterprises import EnterprisesClient
from .offices import OfficesClient
from .order_presets import OrderPresetsClient
from .orders import OrdersClient
from .services import ServicesClient


class SignTrakerClient:
    """Primary entry point exposing all SignTraker resource groups.

    Each resource group is exposed as a lazily instantiated, cached property.
    The base URL is tenant-specific, so provide either ``base_url`` or
    ``subdomain`` (or set ``SIGNTRAKER_BASE_URL`` / ``SIGNTRAKER_SUBDOMAIN``).

    Example:
        ```python
        from signtraker import SignTrakerClient

        client = SignTrakerClient(subdomain="theperrygroup")  # reads SIGNTRAKER_API_KEY
        agents = client.agents.list_agents(top=5, orderby="LastName")
        agent = client.agents.get_agent(123)
        ```
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        *,
        subdomain: Optional[str] = None,
        load_dotenv: bool = False,
        timeout_seconds: Optional[float] = None,
        max_retries: Optional[int] = None,
        retry_backoff_seconds: Optional[float] = None,
    ) -> None:
        """Initialize the aggregator client.

        Args:
            api_key: API key; falls back to the ``SIGNTRAKER_API_KEY`` env var.
            base_url: Full API base URL (e.g.
                ``"https://acme.signtraker.com"``). Overrides ``subdomain``.
            subdomain: Tenant subdomain used to build the base URL when
                ``base_url`` is not provided.
            load_dotenv: Opt-in load of a ``.env`` file via ``python-dotenv``.
            timeout_seconds: Default timeout propagated to all sub-clients.
            max_retries: Retry attempts propagated to all sub-clients.
            retry_backoff_seconds: Backoff propagated to all sub-clients.

        Raises:
            ImportError: If ``load_dotenv`` is True but ``python-dotenv`` is not
                installed.
        """
        if load_dotenv:
            from dotenv import load_dotenv as _load_dotenv

            _load_dotenv()
        self._api_key = api_key
        self._base_url = base_url
        self._subdomain = subdomain
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries
        self._retry_backoff_seconds = retry_backoff_seconds

        self._agents: Optional[AgentsClient] = None
        self._change_orders: Optional[ChangeOrdersClient] = None
        self._credits: Optional[CreditsClient] = None
        self._enterprises: Optional[EnterprisesClient] = None
        self._offices: Optional[OfficesClient] = None
        self._order_presets: Optional[OrderPresetsClient] = None
        self._orders: Optional[OrdersClient] = None
        self._services: Optional[ServicesClient] = None

    @property
    def agents(self) -> AgentsClient:
        """Access the agents endpoints."""
        if self._agents is None:
            self._agents = AgentsClient(**self._sub_client_kwargs())
        return self._agents

    @property
    def change_orders(self) -> ChangeOrdersClient:
        """Access the change-orders endpoints."""
        if self._change_orders is None:
            self._change_orders = ChangeOrdersClient(**self._sub_client_kwargs())
        return self._change_orders

    @property
    def credits(self) -> CreditsClient:
        """Access the credits endpoints."""
        if self._credits is None:
            self._credits = CreditsClient(**self._sub_client_kwargs())
        return self._credits

    @property
    def enterprises(self) -> EnterprisesClient:
        """Access the enterprises endpoints."""
        if self._enterprises is None:
            self._enterprises = EnterprisesClient(**self._sub_client_kwargs())
        return self._enterprises

    @property
    def offices(self) -> OfficesClient:
        """Access the offices endpoints."""
        if self._offices is None:
            self._offices = OfficesClient(**self._sub_client_kwargs())
        return self._offices

    @property
    def order_presets(self) -> OrderPresetsClient:
        """Access the order-presets endpoints."""
        if self._order_presets is None:
            self._order_presets = OrderPresetsClient(**self._sub_client_kwargs())
        return self._order_presets

    @property
    def orders(self) -> OrdersClient:
        """Access the signage-orders endpoints."""
        if self._orders is None:
            self._orders = OrdersClient(**self._sub_client_kwargs())
        return self._orders

    @property
    def services(self) -> ServicesClient:
        """Access the service-orders endpoints."""
        if self._services is None:
            self._services = ServicesClient(**self._sub_client_kwargs())
        return self._services

    def _sub_client_kwargs(self) -> Dict[str, Any]:
        """Build the shared keyword arguments passed to each sub-client.

        Returns:
            The configuration keyword arguments common to every sub-client.
        """
        return {
            "api_key": self._api_key,
            "base_url": self._base_url,
            "subdomain": self._subdomain,
            "timeout_seconds": self._timeout_seconds,
            "max_retries": self._max_retries,
            "retry_backoff_seconds": self._retry_backoff_seconds,
        }
