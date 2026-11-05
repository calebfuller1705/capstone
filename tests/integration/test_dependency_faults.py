import httpx
import pytest
from fastapi.testclient import TestClient
from src.api.main import app, http_resources

client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_shared_client():
    """Ensure the FastAPI shared httpx client is initialized for tests."""
    if "client" not in http_resources or http_resources["client"].is_closed:
        http_resources["client"] = httpx.AsyncClient(timeout=5.0)
    yield


# 1. UPSTREAM RATE LIMITING (HTTP 429)
def test_dependency_fault_rate_limit_exceeded(monkeypatch):
    """Verify that upstream 429 responses map to an actionable 429 envelope."""
    async def mock_get(*args, **kwargs):
        request = httpx.Request("GET", "https://www.virustotal.com/api/v3/urls/dummy")
        return httpx.Response(status_code=429, request=request, json={
            "error": {"code": "QuotaExceededError", "message": "API quota exceeded"}
        })

    shared_client = http_resources["client"]
    monkeypatch.setattr(shared_client, "get", mock_get)

    response = client.post("/scan", json={"url": "https://quota-test-unique.com"})
    assert response.status_code == 429
    data = response.json()
    assert "quota exceeded" in data["detail"].lower()


# 2. UPSTREAM TIMEOUT (HTTP 504 GATEWAY TIMEOUT)
def test_dependency_fault_socket_timeout(monkeypatch):
    """Verify that socket/read timeouts return HTTP 504 Gateway Timeout."""
    async def mock_timeout(*args, **kwargs):
        request = httpx.Request("GET", "https://www.virustotal.com/api/v3/urls/dummy")
        raise httpx.ReadTimeout("Upstream socket timed out after 5000ms", request=request)

    shared_client = http_resources["client"]
    monkeypatch.setattr(shared_client, "get", mock_timeout)

    response = client.post("/scan", json={"url": "https://timeout-test-unique.com"})
    assert response.status_code == 504
    data = response.json()
    assert "timed out" in data["detail"].lower()


# 3. UPSTREAM INTERNAL OUTAGE (HTTP 500 / 503 -> 502 BAD GATEWAY)
@pytest.mark.parametrize("status_code", [500, 502, 503])
def test_dependency_fault_upstream_outage(monkeypatch, status_code):
    """Verify upstream 5xx errors map to HTTP 502 Bad Gateway."""
    async def mock_upstream_crash(*args, **kwargs):
        request = httpx.Request("GET", "https://www.virustotal.com/api/v3/urls/dummy")
        return httpx.Response(status_code=status_code, request=request, text="Internal Server Error")

    shared_client = http_resources["client"]
    monkeypatch.setattr(shared_client, "get", mock_upstream_crash)

    response = client.post("/scan", json={"url": f"https://outage-test-{status_code}.com"})
    assert response.status_code == 502
    data = response.json()
    assert "upstream service error" in data["detail"].lower()


# 4. MALFORMED / POISONED PAYLOAD (HTML ERROR RETURNED AS JSON)
def test_dependency_fault_malformed_json_response(monkeypatch):
    """Verify that HTML error pages or non-JSON payloads map safely to 502."""
    async def mock_html_response(*args, **kwargs):
        request = httpx.Request("GET", "https://www.virustotal.com/api/v3/urls/dummy")
        return httpx.Response(
            status_code=200,
            request=request,
            text="<html><body>502 Bad Gateway: Host Unreachable</body></html>",
            headers={"Content-Type": "text/html"}
        )

    shared_client = http_resources["client"]
    monkeypatch.setattr(shared_client, "get", mock_html_response)

    response = client.post("/scan", json={"url": "https://garbage-json-test.com"})
    assert response.status_code == 502
    data = response.json()
    assert "malformed upstream response" in data["detail"].lower()


# 5. CONNECTION SEVERANCE / DNS RESOLUTION FAILURE
def test_dependency_fault_network_severance(monkeypatch):
    """Verify complete DNS or network connection failure maps safely to 502."""
    async def mock_connect_error(*args, **kwargs):
        request = httpx.Request("GET", "https://www.virustotal.com/api/v3/urls/dummy")
        raise httpx.ConnectError("Failed to resolve 'www.virustotal.com' (Name or service not known)", request=request)

    shared_client = http_resources["client"]
    monkeypatch.setattr(shared_client, "get", mock_connect_error)

    response = client.post("/scan", json={"url": "https://network-severance-test.com"})
    assert response.status_code == 502
    data = response.json()
    assert "network error contacting upstream" in data["detail"].lower()