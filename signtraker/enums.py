"""Shared enumerations for the SignTraker API.

These mirror the closed value sets documented by the API. Where the API only
publishes a partial set of values (for example order statuses), the affected
field is modeled as a plain string in :mod:`signtraker.models` instead of an
enum.
"""

from enum import Enum


class PaymentMode(str, Enum):
    """Billing/payment mode for an agent."""

    TERMS = "Terms"
    PREPAY = "Prepay"
    MONTHLY_CC = "MonthlyCC"
    ACH = "ACH"
    TRANSFER = "Transfer"


class DiscountLevel(str, Enum):
    """Manager discount level."""

    STANDARD = "Standard"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"


class CountryCode(str, Enum):
    """Supported country codes (API pattern ``^US|CA|AU$``)."""

    US = "US"
    CA = "CA"
    AU = "AU"


class AwardRestriction(str, Enum):
    """Restrictions that may be placed on a credit award."""

    PRINTING = "Printing"


class SortDirection(str, Enum):
    """Sort direction usable in OData ``$orderby`` clauses."""

    ASC = "asc"
    DESC = "desc"
