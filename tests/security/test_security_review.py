from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_security_secrets_not_leaked_in_scan_response(monkeypatch):
    """Verify that private API keys are never echoed in scan responses."""
    fake_key = "secret_vt_token_999888777"
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", fake_key)

    async def mock_report(url, api_key, client=None):
        return {
            "url": url,
            "verdict": "Safe",
            "positives": 0,
            "total_engines": 70,
            "scan_date": "2026-11-01",
            "cached": False,
            "raw_details": {"vendor_key": "safe"},
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert fake_key not in response.text


def test_security_input_ssrf_private_ip_rejection():
    """Verify SSRF filter blocks private and loopback address lookups."""
    restricted_targets = [
        "http://127.0.0.1/admin",
        "http://localhost:8080",
        "http://169.254.169.254/latest/meta-data",
        "http://192.168.1.1/router",
        "http://10.0.0.1/internal",
    ]
    for target in restricted_targets:
        res = client.post("/scan", json={"url": target})
        assert res.status_code == 422, f"Failed to restrict SSRF for {target}"


def test_security_input_oversized_payload_rejected():
    """Verify that URLs exceeding 2048 characters are rejected."""
    long_url = "https://example.com/" + ("a" * 2050)
    response = client.post("/scan", json={"url": long_url})
    msg = f"Buffer boundary failure: got {response.status_code}"
    assert response.status_code in (400, 422), msg


def test_security_authorization_no_object_by_id_endpoints():
    """Verify that the API exposes no endpoints returning cached scans."""
    blocked_probes = ["/scan/1", "/scans/recent", "/admin", "/users"]
    for path in blocked_probes:
        res = client.get(path)
        assert res.status_code in (404, 405), f"Exposed endpoint: {path}"


def test_security_error_no_stack_traces_leaked(monkeypatch):
    """Verify unexpected upstream failures return sanitized errors."""
    def crash_scan(*args, **kwargs):
        conn_str = "postgresql://user:pass@internal-db:5432 failed"
        raise RuntimeError(f"Database connection string {conn_str}")

    monkeypatch.setattr("src.api.main.fetch_url_report", crash_scan)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert "postgresql://" not in response.text
