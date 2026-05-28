"""Change Orders API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class ChangeOrdersClient(BaseClient):
    """Client for the ``/api/changeorders`` endpoints."""

    def list_change_orders(
        self,
        *,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List change orders.

        Args:
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of change order records.

        Raises:
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        params = build_odata_params(
            filter=filter, top=top, skip=skip, orderby=orderby, select=select
        )
        return cast(List[Dict[str, Any]], self.get("api/changeorders", params))

    def get_change_order(self, change_order_id: int) -> Dict[str, Any]:
        """Get a single change order by ID.

        Args:
            change_order_id: Unique identifier of the change order.

        Returns:
            The change order record.

        Raises:
            NotFoundError: If the change order does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.get(f"api/changeorders/{change_order_id}"))

    def create_change_order(self, change_order: Dict[str, Any]) -> Dict[str, Any]:
        """Create a change order.

        Note:
            This functionality applies to National Accounts only; individual
            Licensee portals do not have Order Presets available.

        Args:
            change_order: The payload, including ``InstallId``, ``PresetId``,
                and ``OverridePriceLimit``.

        Returns:
            The created change order record.

        Raises:
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(
            Dict[str, Any],
            self.post("api/changeorders", json_data=change_order),
        )
