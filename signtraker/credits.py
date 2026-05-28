"""Credits API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class CreditsClient(BaseClient):
    """Client for the ``/api/credits`` endpoints."""

    def list_awards(
        self,
        *,
        awarded_to: Optional[int] = None,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List credit awards, optionally filtered to a specific recipient.

        Args:
            awarded_to: Agent ID to filter awards granted to that agent.
            filter: OData ``$filter`` expression.
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of award records.

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
            extra={"awardedTo": awarded_to},
        )
        return cast(List[Dict[str, Any]], self.get("api/credits/awards", params))

    def create_award(self, award: Dict[str, Any]) -> Dict[str, Any]:
        """Create a credit award.

        Args:
            award: The award payload. ``Restrictions`` may include ``Printing``.

        Returns:
            The created award record.

        Raises:
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.post("api/credits/awards", json_data=award))
