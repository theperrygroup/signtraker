"""Helpers for building OData query parameters.

The SignTraker API supports the OData query options ``$filter``, ``$top``,
``$skip``, ``$orderby`` and ``$select`` on its list endpoints. This module
converts ergonomic Python keyword arguments into the ``$``-prefixed query
parameters the API expects, and merges any endpoint-specific parameters.
"""

from typing import Any, Dict, Optional, Sequence, Union

ODataValue = Union[str, Sequence[str]]


def _normalize_csv(value: ODataValue) -> str:
    """Normalize a string or sequence of strings into a comma-separated string.

    Args:
        value: Either a raw string (returned unchanged) or a sequence of
            strings that will be joined with commas.

    Returns:
        A comma-separated string suitable for an OData query parameter.
    """
    if isinstance(value, str):
        return value
    return ",".join(str(item) for item in value)


def build_odata_params(
    *,
    filter: Optional[str] = None,
    top: Optional[int] = None,
    skip: Optional[int] = None,
    orderby: Optional[ODataValue] = None,
    select: Optional[ODataValue] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build an OData query-parameter dictionary.

    Args:
        filter: Value for ``$filter`` (e.g. ``"LastName eq 'Smith'"``).
        top: Value for ``$top`` (maximum number of records to return).
        skip: Value for ``$skip`` (number of records to skip).
        orderby: Value for ``$orderby``; a string or a sequence of strings
            joined with commas (e.g. ``"LastName"`` or ``["LastName", "Id"]``).
        select: Value for ``$select``; a string or a sequence of strings joined
            with commas (e.g. ``"Id,LastName"`` or ``["Id", "LastName"]``).
        extra: Additional endpoint-specific query parameters. Keys whose values
            are ``None`` are omitted.

    Returns:
        A dictionary of query parameters. Keys with ``None`` values are omitted
        so the dictionary can be passed directly to the transport layer.
    """
    params: Dict[str, Any] = {}
    if filter is not None:
        params["$filter"] = filter
    if top is not None:
        params["$top"] = top
    if skip is not None:
        params["$skip"] = skip
    if orderby is not None:
        params["$orderby"] = _normalize_csv(orderby)
    if select is not None:
        params["$select"] = _normalize_csv(select)
    if extra:
        for key, value in extra.items():
            if value is not None:
                params[key] = value
    return params
