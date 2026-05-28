"""Orders (signage) API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class OrdersClient(BaseClient):
    """Client for the ``/api/orders`` endpoints."""

    def list_orders(
        self,
        *,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List signage orders.

        Args:
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of signage order records.

        Raises:
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        params = build_odata_params(
            filter=filter, top=top, skip=skip, orderby=orderby, select=select
        )
        return cast(List[Dict[str, Any]], self.get("api/orders", params))

    def get_order(self, order_id: int) -> Dict[str, Any]:
        """Get a single signage order by ID.

        Args:
            order_id: Unique identifier of the signage order.

        Returns:
            The signage order record.

        Raises:
            NotFoundError: If the order does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.get(f"api/orders/{order_id}"))

    def create_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """Create a signage order.

        Note:
            This functionality applies to National Accounts only; individual
            Licensee portals do not have Order Presets available.

        Args:
            order: The order payload. Required fields include ``AgentId`` and
                ``PresetId``.

        Returns:
            The create result (``Status``, ``Message``, ``RequestId``,
            ``OrderId``).

        Raises:
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.post("api/orders", json_data=order))

    def request_removal(
        self, order_id: int, removal_request: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Request removal of an installed signage order.

        Args:
            order_id: Unique identifier of the signage order.
            removal_request: Optional payload with ``DueDate`` and ``Notes``.

        Returns:
            The result payload (typically ``{"DueDate": ...}``).

        Raises:
            NotFoundError: If the order does not exist.
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(
            Dict[str, Any],
            self.post(
                f"api/orders/{order_id}/requestremoval",
                json_data=removal_request or {},
            ),
        )
