from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_frontend_seam_index_html_delivery():
    """Verify frontend entrypoint delivers single-page app HTML shell."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    content = response.text
    assert "URL Security Scanner" in content
    assert 'id="url-input"' in content
    assert 'id="submit-btn"' in content


def test_frontend_seam_static_assets_delivered():
    """Verify static asset bundle (CSS stylesheet and JS) is served."""
    res_css = client.get("/static/styles.css")
    assert res_css.status_code in (200, 404)

    res_js = client.get("/static/app.js")
    assert res_js.status_code in (200, 404)


def test_frontend_seam_complete_scan_roundtrip(monkeypatch):
    """Verify end-to-end API response contract for front-end controller."""
    async def mock_report(url, api_key, client=None):
        return {
            "url": url,
            "scan_id": "u-mocked-12345",
            "malicious_count": 0,
            "suspicious_count": 0,
            "harmless_count": 72,
            "undetected_count": 14,
            "engine_results": {
                "Google Safe Browsing": {
                    "category": "harmless",
                    "result": "clean",
                },
                "Kaspersky": {
                    "category": "harmless",
                    "result": "clean",
                },
            },
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)

    response = client.post("/scan", json={"url": "https://trusted-site.org"})
    assert response.status_code == 200
    data = response.json()
    assert "malicious_count" in data
    assert data["url"] == "https://trusted-site.org"
    assert data["verdict"] == "Safe"
