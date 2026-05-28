"""Services (service orders) API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class ServicesClient(BaseClient):
    """Client for the ``/api/services`` endpoints."""

    def list_services(
        self,
        *,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List service orders.

        Args:
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of service order records.

        Raises:
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        params = build_odata_params(
            filter=filter, top=top, skip=skip, orderby=orderby, select=select
        )
        return cast(List[Dict[str, Any]], self.get("api/services", params))

    def get_service(self, service_id: int) -> Dict[str, Any]:
        """Get a single service order by ID.

        Args:
            service_id: Unique identifier of the service order.

        Returns:
            The service order record.

        Raises:
            NotFoundError: If the service order does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.get(f"api/services/{service_id}"))

    def create_service(self, service: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a service order.

        Args:
            service: The payload, including ``InstallId``, ``PresetId``, and
                ``OverridePriceLimit``.

        Returns:
            The created service order record(s). The API returns a list.

        Raises:
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(List[Dict[str, Any]], self.post("api/services", json_data=service))
