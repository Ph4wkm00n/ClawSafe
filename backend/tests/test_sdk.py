from sdk.clawsafe_client import ClawSafeClient


def test_sdk_client_init():
    client = ClawSafeClient("http://localhost:8000", api_key="test-key")
    assert client.base_url == "http://localhost:8000"
    assert "Authorization" in client._headers
    assert client._headers["Authorization"] == "Bearer test-key"


def test_sdk_url_building():
    client = ClawSafeClient("http://example.com/")
    assert client._url("/status") == "http://example.com/api/v1/status"


def test_sdk_jwt_auth():
    client = ClawSafeClient(jwt_token="eyJ...")
    assert client._headers["Authorization"] == "Bearer eyJ..."
