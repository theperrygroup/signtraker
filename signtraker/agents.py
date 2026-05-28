"""Agents API client."""

from typing import Any, Dict, List, Optional, cast

from ._odata import ODataValue, build_odata_params
from .base_client import BaseClient


class AgentsClient(BaseClient):
    """Client for the ``/api/agents`` endpoints."""

    def list_agents(
        self,
        *,
        email: Optional[str] = None,
        filter: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None,
        orderby: Optional[ODataValue] = None,
        select: Optional[ODataValue] = None,
    ) -> List[Dict[str, Any]]:
        """List agents, optionally filtered, sorted, and paged.

        Args:
            email: Find an agent by exact email address.
            filter: OData ``$filter`` expression (e.g. ``"LastName eq 'Smith'"``).
            top: OData ``$top`` (maximum number of records to return).
            skip: OData ``$skip`` (number of records to skip).
            orderby: OData ``$orderby`` value or sequence of fields.
            select: OData ``$select`` value or sequence of fields.

        Returns:
            The list of matching agent records.

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
            extra={"email": email},
        )
        return cast(List[Dict[str, Any]], self.get("api/agents", params))

    def get_agent(self, agent_id: int) -> Dict[str, Any]:
        """Get a single agent by ID.

        Args:
            agent_id: Unique identifier of the agent.

        Returns:
            The agent record.

        Raises:
            NotFoundError: If the agent does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.get(f"api/agents/{agent_id}"))

    def create_agent(self, agent: Dict[str, Any]) -> Dict[str, Any]:
        """Create an agent.

        Args:
            agent: The agent payload. Required fields include ``UserName``,
                ``Email``, ``FirstName``, ``LastName``, ``CellularPhone``,
                ``PaymentMode``, and an ``Office`` reference.

        Returns:
            The created agent record.

        Raises:
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(Dict[str, Any], self.post("api/agents", json_data=agent))

    def update_agent(self, agent_id: int, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Update an agent using a JSON Merge Patch.

        Only the fields present in ``changes`` are modified; omitted fields
        remain unchanged. You may not convert an agent to/from a manager with
        this method, and synced National Account agents cannot be updated
        directly.

        Args:
            agent_id: Unique identifier of the agent to update.
            changes: The partial agent payload to merge.

        Returns:
            The updated agent record.

        Raises:
            NotFoundError: If the agent does not exist.
            ValidationError: If the payload is invalid.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(
            Dict[str, Any],
            self.patch(
                f"api/agents/{agent_id}",
                json_data=changes,
                content_type="application/merge-patch+json",
            ),
        )

    def activate_agent(self, agent_id: int) -> Dict[str, Any]:
        """Activate an agent.

        Args:
            agent_id: Unique identifier of the agent to activate.

        Returns:
            The parsed response payload (empty when the API returns no body).

        Raises:
            NotFoundError: If the agent does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(
            Dict[str, Any],
            self.post("api/agents/activate", params={"id": agent_id}),
        )

    def deactivate_agent(self, agent_id: int) -> Dict[str, Any]:
        """Deactivate an agent.

        Args:
            agent_id: Unique identifier of the agent to deactivate.

        Returns:
            The parsed response payload (empty when the API returns no body).

        Raises:
            NotFoundError: If the agent does not exist.
            AuthenticationError: If the API key is invalid.
            SignTrakerError: For other API errors.
        """
        return cast(
            Dict[str, Any],
            self.post("api/agents/deactivate", params={"id": agent_id}),
        )
