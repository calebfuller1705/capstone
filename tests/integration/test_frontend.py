from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_frontend_seam_index_html_delivery():
    """Verify that root GET / serves the single-page application shell."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("Content-Type", "")
    assert "<title>URL Security Scanner</title>" in response.text
    assert 'id="scan-form"' in response.text
    assert 'id="url-input"' in response.text
    assert 'id="results-card"' in response.text


def test_frontend_seam_static_assets_delivered():
    """Verify that the static CSS and JS assets are reachable and properly typed."""
    css_res = client.get("/static/styles.css")
    assert css_res.status_code == 200
    assert "text/css" in css_res.headers.get("Content-Type", "")
    assert "--color-primary" in css_res.text

    js_res = client.get("/static/app.js")
    assert js_res.status_code == 200
    assert any(mime in js_res.headers.get("Content-Type", "") for mime in ["javascript", "application/x-javascript"])
    assert "scan-form" in js_res.text
    assert "fetch(\"/scan\"" in js_res.text


def test_frontend_seam_complete_scan_roundtrip(monkeypatch):
    """Verify end-to-end API response contract required by the front-end DOM controller."""
    async def mock_report(url, api_key, client=None):
        return {
            "url": url,
            "scan_id": "u-mocked-12345",
            "malicious_count": 0,
            "suspicious_count": 0,
            "harmless_count": 72,
            "undetected_count": 14,
            "engine_results": {
                "Google Safe Browsing": {"category": "harmless", "result": "clean"},
                "Kaspersky": {"category": "harmless", "result": "clean"}
            }
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)

    response = client.post("/scan", json={"url": "https://trusted-site.org"})
    assert response.status_code == 200
    data = response.json()

    assert "malicious_count" in data
    assert "suspicious_count" in data
    assert "harmless_count" in data
    assert "undetected_count" in data
    assert "engine_results" in data
    assert "Google Safe Browsing" in data["engine_results"]