"""Tests for the BaseClient transport layer."""

import pytest
import requests
import responses

from signtraker.base_client import (
    BaseClient,
    _extract_error_message,
    _parse_env_float,
    _parse_env_int,
)
from signtraker.exceptions import (
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    SignTrakerConfigError,
    SignTrakerError,
    ValidationError,
)

BASE_URL = "https://test.signtraker.com"


@pytest.fixture
def base(api_key: str) -> BaseClient:
    """Build a BaseClient wired to the test base URL with no retry backoff.

    Args:
        api_key: The dummy API key fixture.

    Returns:
        A configured :class:`BaseClient`.
    """
    return BaseClient(api_key=api_key, base_url=BASE_URL, retry_backoff_seconds=0)


class TestConfiguration:
    """Authentication and base-URL resolution."""

    def test_missing_api_key_raises(self) -> None:
        """Constructing without a key raises AuthenticationError."""
        with pytest.raises(AuthenticationError):
            BaseClient(base_url=BASE_URL)

    def test_api_key_from_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The API key is read from the environment when not passed."""
        monkeypatch.setenv("SIGNTRAKER_API_KEY", "env_key")
        client = BaseClient(base_url=BASE_URL)
        assert client.session.headers["Authorization"] == "ST-API env_key"

    def test_missing_base_url_raises(self, api_key: str) -> None:
        """No base URL or subdomain raises SignTrakerConfigError."""
        with pytest.raises(SignTrakerConfigError):
            BaseClient(api_key=api_key)

    def test_base_url_from_env(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """The base URL is read from SIGNTRAKER_BASE_URL."""
        monkeypatch.setenv("SIGNTRAKER_BASE_URL", "https://env.signtraker.com/")
        client = BaseClient(api_key=api_key)
        assert client.base_url == "https://env.signtraker.com"

    def test_subdomain_argument(self, api_key: str) -> None:
        """A subdomain argument builds the tenant URL."""
        client = BaseClient(api_key=api_key, subdomain="acme")
        assert client.base_url == "https://acme.signtraker.com"

    def test_subdomain_from_env(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """The subdomain is read from SIGNTRAKER_SUBDOMAIN."""
        monkeypatch.setenv("SIGNTRAKER_SUBDOMAIN", "acme")
        client = BaseClient(api_key=api_key)
        assert client.base_url == "https://acme.signtraker.com"

    def test_base_url_trailing_slash_stripped(self, api_key: str) -> None:
        """A trailing slash is removed from the base URL."""
        client = BaseClient(api_key=api_key, base_url=f"{BASE_URL}/")
        assert client.base_url == BASE_URL

    def test_api_key_from_brand_alias_env(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """The brand-spelled SIGNTRACKER_API_KEY is honored as a fallback."""
        monkeypatch.setenv("SIGNTRACKER_API_KEY", "brand_key")
        client = BaseClient(base_url=BASE_URL)
        assert client.session.headers["Authorization"] == "ST-API brand_key"

    def test_base_url_from_brand_alias_env(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """The brand-spelled SIGNTRACKER_BASE_URL is honored as a fallback."""
        monkeypatch.setenv("SIGNTRACKER_BASE_URL", "https://brand.signtraker.com")
        client = BaseClient(api_key=api_key)
        assert client.base_url == "https://brand.signtraker.com"

    def test_subdomain_from_brand_alias_env(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """The brand-spelled SIGNTRACKER_SUBDOMAIN is honored as a fallback."""
        monkeypatch.setenv("SIGNTRACKER_SUBDOMAIN", "brand")
        client = BaseClient(api_key=api_key)
        assert client.base_url == "https://brand.signtraker.com"

    def test_config_from_env_values(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """Timeout/retry settings are read from the environment."""
        monkeypatch.setenv("SIGNTRAKER_TIMEOUT_SECONDS", "12.5")
        monkeypatch.setenv("SIGNTRAKER_MAX_RETRIES", "3")
        monkeypatch.setenv("SIGNTRAKER_RETRY_BACKOFF_SECONDS", "0.25")
        client = BaseClient(api_key=api_key, base_url=BASE_URL)
        assert client.timeout_seconds == 12.5
        assert client.max_retries == 3
        assert client.retry_backoff_seconds == 0.25

    def test_explicit_config_overrides_env(
        self, monkeypatch: pytest.MonkeyPatch, api_key: str
    ) -> None:
        """Explicit arguments win over environment variables."""
        monkeypatch.setenv("SIGNTRAKER_MAX_RETRIES", "9")
        client = BaseClient(
            api_key=api_key,
            base_url=BASE_URL,
            timeout_seconds=5,
            max_retries=1,
            retry_backoff_seconds=0,
        )
        assert client.timeout_seconds == 5.0
        assert client.max_retries == 1


class TestEnvParsing:
    """Environment-variable parsing helpers."""

    def test_parse_env_float_missing(self) -> None:
        """Missing variables fall back to the default."""
        assert _parse_env_float("SIGNTRAKER_DOES_NOT_EXIST", 1.5) == 1.5

    def test_parse_env_float_invalid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Invalid values fall back to the default."""
        monkeypatch.setenv("SIGNTRAKER_TMP_FLOAT", "abc")
        assert _parse_env_float("SIGNTRAKER_TMP_FLOAT", 2.0) == 2.0

    def test_parse_env_int_missing(self) -> None:
        """Missing variables fall back to the default."""
        assert _parse_env_int("SIGNTRAKER_DOES_NOT_EXIST", 7) == 7

    def test_parse_env_int_invalid(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Invalid values fall back to the default."""
        monkeypatch.setenv("SIGNTRAKER_TMP_INT", "x")
        assert _parse_env_int("SIGNTRAKER_TMP_INT", 4) == 4


class TestVerbs:
    """HTTP verb helpers and response parsing."""

    @responses.activate
    def test_get_dict(self, base: BaseClient) -> None:
        """GET returns a parsed dict body."""
        responses.add(
            responses.GET, f"{BASE_URL}/api/thing", json={"Id": 1}, status=200
        )
        assert base.get("api/thing") == {"Id": 1}

    @responses.activate
    def test_get_list(self, base: BaseClient) -> None:
        """GET returns a parsed list body."""
        responses.add(
            responses.GET, f"{BASE_URL}/api/things", json=[{"Id": 1}], status=200
        )
        assert base.get("api/things", params={"$top": 1}) == [{"Id": 1}]

    @responses.activate
    def test_get_with_timeout_override(self, base: BaseClient) -> None:
        """A per-request timeout override is accepted."""
        responses.add(responses.GET, f"{BASE_URL}/api/thing", json={}, status=200)
        assert base.get("api/thing", timeout_seconds=1.0) == {}

    @responses.activate
    def test_post(self, base: BaseClient) -> None:
        """POST forwards a JSON body and query params."""
        responses.add(
            responses.POST, f"{BASE_URL}/api/thing", json={"ok": True}, status=200
        )
        assert base.post("api/thing", json_data={"a": 1}, params={"id": 5}) == {
            "ok": True
        }

    @responses.activate
    def test_put(self, base: BaseClient) -> None:
        """PUT forwards a JSON body."""
        responses.add(
            responses.PUT, f"{BASE_URL}/api/thing", json={"ok": True}, status=200
        )
        assert base.put("api/thing", json_data={"a": 1}) == {"ok": True}

    @responses.activate
    def test_patch_default_content_type(self, base: BaseClient) -> None:
        """PATCH without a content_type override keeps the session header."""
        responses.add(
            responses.PATCH, f"{BASE_URL}/api/thing", json={"ok": True}, status=200
        )
        base.patch("api/thing", json_data={"a": 1})
        assert responses.calls[0].request.headers["Content-Type"] == "application/json"

    @responses.activate
    def test_patch_content_type_override(self, base: BaseClient) -> None:
        """PATCH applies a content_type override."""
        responses.add(
            responses.PATCH, f"{BASE_URL}/api/thing", json={"ok": True}, status=200
        )
        base.patch(
            "api/thing",
            json_data={"a": 1},
            content_type="application/merge-patch+json",
        )
        assert (
            responses.calls[0].request.headers["Content-Type"]
            == "application/merge-patch+json"
        )

    @responses.activate
    def test_delete(self, base: BaseClient) -> None:
        """DELETE issues a delete request."""
        responses.add(responses.DELETE, f"{BASE_URL}/api/thing", status=204)
        assert base.delete("api/thing") == {}


class TestResponseHandling:
    """Status-code parsing and error mapping."""

    @responses.activate
    def test_204_returns_empty(self, base: BaseClient) -> None:
        """A 204 response returns an empty dict."""
        responses.add(responses.GET, f"{BASE_URL}/api/x", status=204)
        assert base.get("api/x") == {}

    @responses.activate
    def test_empty_body_returns_empty(self, base: BaseClient) -> None:
        """A 200 with no body returns an empty dict."""
        responses.add(responses.GET, f"{BASE_URL}/api/x", body="", status=200)
        assert base.get("api/x") == {}

    @responses.activate
    def test_invalid_json_wrapped(self, base: BaseClient) -> None:
        """Invalid JSON is wrapped as a message dict."""
        responses.add(responses.GET, f"{BASE_URL}/api/x", body="not json", status=200)
        assert base.get("api/x") == {"message": "not json"}

    @responses.activate
    @pytest.mark.parametrize(
        "status,exc",
        [
            (400, ValidationError),
            (401, AuthenticationError),
            (403, AuthenticationError),
            (404, NotFoundError),
            (429, RateLimitError),
            (500, ServerError),
            (418, SignTrakerError),
        ],
    )
    def test_status_maps_to_exception(
        self, base: BaseClient, status: int, exc: type
    ) -> None:
        """Each error status maps to the correct typed exception."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/x",
            json={"Message": "boom"},
            status=status,
        )
        with pytest.raises(exc) as info:
            base.get("api/x")
        assert info.value.status_code == status
        assert info.value.response_data == {"Message": "boom"}
        assert "boom" in str(info.value)

    @responses.activate
    def test_error_non_dict_payload(self, base: BaseClient) -> None:
        """A non-dict error body is normalized into response_data."""
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/x",
            json=["bad1", "bad2"],
            status=400,
        )
        with pytest.raises(ValidationError) as info:
            base.get("api/x")
        assert info.value.response_data == {"detail": ["bad1", "bad2"]}
        assert info.value.message == "bad1; bad2"

    @responses.activate
    def test_error_default_message(self, base: BaseClient) -> None:
        """An empty error body falls back to a generated message."""
        responses.add(responses.GET, f"{BASE_URL}/api/x", json={}, status=500)
        with pytest.raises(ServerError) as info:
            base.get("api/x")
        assert info.value.message == "Request failed with status 500"


class TestRetries:
    """Retry behavior for transient failures."""

    @responses.activate
    def test_retry_on_5xx_then_success(self, api_key: str) -> None:
        """A retryable 503 is retried and then succeeds."""
        client = BaseClient(
            api_key=api_key,
            base_url=BASE_URL,
            max_retries=1,
            retry_backoff_seconds=0,
        )
        responses.add(responses.GET, f"{BASE_URL}/api/x", status=503)
        responses.add(responses.GET, f"{BASE_URL}/api/x", json={"ok": True}, status=200)
        assert client.get("api/x") == {"ok": True}
        assert len(responses.calls) == 2

    @responses.activate
    def test_retry_exhausted_raises(self, api_key: str) -> None:
        """An exhausted 5xx retry raises ServerError."""
        client = BaseClient(
            api_key=api_key,
            base_url=BASE_URL,
            max_retries=1,
            retry_backoff_seconds=0,
        )
        responses.add(responses.GET, f"{BASE_URL}/api/x", status=503)
        responses.add(responses.GET, f"{BASE_URL}/api/x", status=503)
        with pytest.raises(ServerError):
            client.get("api/x")

    @responses.activate
    def test_network_error_then_success(self, api_key: str) -> None:
        """A connection error is retried and then succeeds."""
        client = BaseClient(
            api_key=api_key,
            base_url=BASE_URL,
            max_retries=1,
            retry_backoff_seconds=0,
        )
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/x",
            body=requests.exceptions.ConnectionError("boom"),
        )
        responses.add(responses.GET, f"{BASE_URL}/api/x", json={"ok": True}, status=200)
        assert client.get("api/x") == {"ok": True}

    @responses.activate
    def test_network_error_exhausted_raises(self, api_key: str) -> None:
        """An exhausted connection error raises NetworkError."""
        client = BaseClient(
            api_key=api_key,
            base_url=BASE_URL,
            max_retries=1,
            retry_backoff_seconds=0,
        )
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/x",
            body=requests.exceptions.ConnectionError("boom"),
        )
        responses.add(
            responses.GET,
            f"{BASE_URL}/api/x",
            body=requests.exceptions.ConnectionError("boom"),
        )
        with pytest.raises(NetworkError):
            client.get("api/x")


class TestExtractErrorMessage:
    """Direct tests for the recursive error-message extractor."""

    def test_direct_key(self) -> None:
        """A direct PascalCase message key is found."""
        assert _extract_error_message({"Message": "x"}) == "x"

    def test_single_key_wrapper_and_list_dedupe(self) -> None:
        """Single-key wrappers are unwrapped and list messages de-duplicated."""
        payload = {"errors": {"Email": ["required", "required"]}}
        assert _extract_error_message(payload) == "required"

    def test_multiple_values_joined(self) -> None:
        """Multiple nested values are joined."""
        assert _extract_error_message({"a": "x", "b": "y"}) == "x; y"

    def test_list_joined(self) -> None:
        """A top-level list joins its messages."""
        assert _extract_error_message(["x", "y"]) == "x; y"

    def test_empty_collections_return_none(self) -> None:
        """Empty containers yield no message."""
        assert _extract_error_message({}) is None
        assert _extract_error_message([]) is None

    def test_whitespace_string_returns_none(self) -> None:
        """A whitespace-only string yields no message."""
        assert _extract_error_message("   ") is None

    def test_scalar_at_top_level(self) -> None:
        """A scalar at the top level is stringified."""
        assert _extract_error_message(404) == "404"

    def test_none_returns_none(self) -> None:
        """None yields no message."""
        assert _extract_error_message(None) is None

    def test_depth_guard(self) -> None:
        """Excessively nested payloads stop recursing and yield no message."""
        payload: object = {"message": "deep"}
        for _ in range(8):
            payload = {"wrap": payload}
        assert _extract_error_message(payload) is None
