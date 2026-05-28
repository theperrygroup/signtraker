"""Offices API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class OfficesClient(BaseClient):
    """Client for the ``/api/offices`` endpoints."""

    def list_offices(
        self,
        *,
        enterprise_id: Optional[int] = None,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List offices, optionally scoped to an enterprise.

        Args:
            enterprise_id: Enterprise ID to filter offices to that enterprise.
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of office records (each ``{Id, Name}``).

        Raises:
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        params = build_odata_params(
            filter=filter,
            top=top,
            skip=skip,
            orderby=orderby,
            select=select,
            extra={"enterpriseId": enterprise_id},
        )
        return cast(List[Dict[str, Any]], self.get("api/offices", params))
