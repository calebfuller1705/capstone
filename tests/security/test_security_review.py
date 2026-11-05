"""Automated security verification tests for Milestone 12 Security Review (Rep 4)."""

import os
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


# 1. SECRETS: Verify API keys are never leaked in response bodies or headers
def test_security_secrets_not_leaked_in_scan_response():
    """Verify that VIRUSTOTAL_API_KEY is not exposed in JSON or response headers."""
    response = client.post("/scan", json={"url": "https://example.com"})
    raw_text = response.text
    headers_text = str(response.headers)
    active_key = os.environ.get("VIRUSTOTAL_API_KEY", "dummy_fallback_for_mock_tests")

    assert active_key not in raw_text, "CRITICAL: API key leaked in response body!"
    assert active_key not in headers_text, "CRITICAL: API key leaked in response headers!"


# 2. INPUT & SSRF: Unscannable intranet/private addresses blocked (FR-EVAL-01)
def test_security_input_ssrf_private_ip_rejection():
    """Verify that private RFC 1918 addresses, loopbacks, and cloud metadata are rejected."""
    hostile_urls = [
        "http://127.0.0.1:8000/admin",
        "http://localhost:3000",
        "http://192.168.1.1/router",
        "http://10.0.0.1/internal",
        "http://169.254.169.254/latest/meta-data/"
    ]
    for url in hostile_urls:
        response = client.post("/scan", json={"url": url})
        assert response.status_code in (400, 422), (
            f"SSRF failure: Hostile private URL {url} was not blocked (got {response.status_code})"
        )


# 3. INPUT BOUNDS: Enforce 2048-character payload limit (FR-INP-03)
def test_security_input_oversized_payload_rejected():
    """Verify that URLs exceeding 2048 characters are rejected immediately."""
    long_url = "https://example.com/" + ("a" * 2050)
    response = client.post("/scan", json={"url": long_url})
    assert response.status_code in (400, 422), (
        f"Buffer boundary failure: Oversized URL was not rejected (got {response.status_code})"
    )


# 4. AUTHORIZATION / IDOR: Object enumeration and state access impossible
def test_security_authorization_no_object_by_id_endpoints():
    """Verify that no ID-based endpoints exist that permit cross-user object access."""
    response_get = client.get("/scan/12345")
    assert response_get.status_code in (404, 405)

    response_report = client.get("/analyses/sample-vt-analysis-id")
    assert response_report.status_code in (404, 405)


# 5. ERROR DISCLOSURE: Unhandled exceptions do not reveal stack traces
def test_security_error_no_stack_traces_leaked(monkeypatch):
    """Verify that unexpected upstream failures return sanitized error messages."""
    def crash_scan(*args, **kwargs):
        raise RuntimeError("Database connection string postgresql://user:pass@internal-db:5432 failed")

    monkeypatch.setattr("src.api.main.fetch_url_report", crash_scan)
    response = client.post("/scan", json={"url": "https://example.com"})

    assert "postgresql://" not in response.text
    assert "Traceback" not in response.text
