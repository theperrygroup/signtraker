"""Enterprises API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class EnterprisesClient(BaseClient):
    """Client for the ``/api/enterprises`` endpoints."""

    def list_enterprises(
        self,
        *,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List enterprises.

        Args:
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of enterprise records (each ``{Id, Name}``).

        Raises:
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        params = build_odata_params(
            filter=filter, top=top, skip=skip, orderby=orderby, select=select
        )
        return cast(List[Dict[str, Any]], self.get("api/enterprises", params))
