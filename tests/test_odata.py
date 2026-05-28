"""Tests for the OData query-parameter helper."""

from signtraker._odata import _normalize_csv, build_odata_params


class TestNormalizeCsv:
    """Normalization of string and sequence values."""

    def test_string_passthrough(self) -> None:
        """A string value is returned unchanged."""
        assert _normalize_csv("Id,Name") == "Id,Name"

    def test_sequence_joined(self) -> None:
        """A sequence is joined with commas."""
        assert _normalize_csv(["Id", "Name"]) == "Id,Name"


class TestBuildODataParams:
    """Construction of OData query-parameter dictionaries."""

    def test_all_options(self) -> None:
        """All supported options are mapped to their $-prefixed keys."""
        params = build_odata_params(
            filter="LastName eq 'Smith'",
            top=5,
            skip=15,
            orderby=["LastName", "Id"],
            select="Id,LastName",
        )
        assert params == {
            "$filter": "LastName eq 'Smith'",
            "$top": 5,
            "$skip": 15,
            "$orderby": "LastName,Id",
            "$select": "Id,LastName",
        }

    def test_empty(self) -> None:
        """No arguments yields an empty dict."""
        assert build_odata_params() == {}

    def test_extra_drops_none(self) -> None:
        """Extra params with None values are omitted."""
        params = build_odata_params(extra={"email": "a@b.com", "skip_me": None})
        assert params == {"email": "a@b.com"}
