import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_dependency_fault_rate_limit_exceeded(monkeypatch):
    async def mock_report(*args, **kwargs):
        from src.services.vt_client import UpstreamRateLimitError
        raise UpstreamRateLimitError(
            "VirusTotal API quota exceeded (HTTP 429)"
        )

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 429
    detail = response.json().get("detail", "").lower()
    assert "quota exceeded" in detail


def test_dependency_fault_socket_timeout(monkeypatch):
    """Upstream socket read timeout maps to HTTP 504 Gateway Timeout."""
    async def mock_report(*args, **kwargs):
        from src.services.vt_client import UpstreamServiceError
        raise UpstreamServiceError("Upstream service timed out")

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 504
    detail = response.json().get("detail", "").lower()
    assert "timed out" in detail


@pytest.mark.parametrize("status_code", [500, 502, 503])
def test_dependency_fault_upstream_outage(monkeypatch, status_code):
    """Upstream 5xx server outages map to HTTP 502 Bad Gateway."""
    async def mock_report(*args, **kwargs):
        from src.services.vt_client import UpstreamServiceError
        raise UpstreamServiceError(
            f"VirusTotal API returned HTTP {status_code}"
        )

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 502
    detail = response.json().get("detail", "").lower()
    assert "upstream service error" in detail


def test_dependency_fault_malformed_json_response(monkeypatch):
    """Upstream non-JSON payload maps to HTTP 502 Bad Gateway."""
    async def mock_report(*args, **kwargs):
        from src.services.vt_client import UpstreamServiceError
        msg = "Malformed upstream response: expected valid JSON"
        raise UpstreamServiceError(msg)

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 502
    detail = response.json().get("detail", "").lower()
    assert "upstream service error" in detail


def test_dependency_fault_network_severance(monkeypatch):
    """Upstream network disconnection maps to HTTP 502 Bad Gateway."""
    async def mock_report(*args, **kwargs):
        from src.services.vt_client import UpstreamServiceError
        msg = "Network error contacting upstream: [Errno 111]"
        raise UpstreamServiceError(msg)

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 502
    detail = response.json().get("detail", "").lower()
    assert "upstream service error" in detail
