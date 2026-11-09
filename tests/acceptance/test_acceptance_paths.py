from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_FR_INP_01_AC1_valid_http_url_submission():
    """FR-INP-01-AC1: Valid HTTP URL returns standard scan schema."""
    response = client.post("/scan", json={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "http://example.com"
    assert data["verdict"] in ("Safe", "Unsafe", "Ambiguous")


def test_FR_INP_01_AC2_valid_https_url_submission():
    """FR-INP-01-AC2: Valid HTTPS URL accepted."""
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 200
    assert response.json()["verdict"] in ("Safe", "Unsafe", "Ambiguous")


def test_FR_INP_03_AC1_boundary_max_length_rejection():
    """FR-INP-03-AC1: URLs exceeding 2048 chars rejected with HTTP 422."""
    long_url = "https://example.com/" + ("a" * 2050)
    response = client.post("/scan", json={"url": long_url})
    assert response.status_code == 422


def test_FR_INP_03_AC2_boundary_empty_url_rejection():
    """FR-INP-03-AC2: Empty string URL payload rejected with HTTP 422."""
    response = client.post("/scan", json={"url": ""})
    assert response.status_code == 422


def test_FR_INP_04_AC1_non_web_scheme_rejection():
    """FR-INP-04-AC1: Non-HTTP/HTTPS protocol schemes rejected with 422."""
    response = client.post("/scan", json={"url": "javascript:alert('xss')"})
    assert response.status_code == 422

    file_res = client.post("/scan", json={"url": "file:///etc/passwd"})
    assert file_res.status_code == 422


def test_FR_EVAL_01_AC1_ssrf_intranet_rejection():
    """FR-EVAL-01-AC1: Loopback and RFC 1918 addresses rejected with 422."""
    response = client.post(
        "/scan", json={"url": "http://127.0.0.1:8000/internal"}
    )
    assert response.status_code == 422
    assert "intranet" in response.json().get("detail", "").lower()


def test_FR_UI_01_AC1_health_endpoint_contract():
    """FR-UI-01-AC1: Health check returns status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_FR_EVAL_02_AC1_seeded_malware_returns_unsafe(monkeypatch):
    """FR-EVAL-02-AC1: Seeded malware URL returns Unsafe verdict."""
    async def mock_malicious_report(url, api_key, client=None):
        return {
            "url": url,
            "verdict": "Unsafe",
            "positives": 15,
            "total_engines": 72,
            "scan_date": "2026-11-09 12:00:00 UTC",
            "cached": True,
            "malicious_count": 15,
            "suspicious_count": 2,
            "harmless_count": 50,
            "undetected_count": 5,
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_malicious_report)

    response = client.post(
        "/scan", json={"url": "http://malware.testing.google.test/test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Unsafe"
    assert data["positives"] == 15
    assert data["total_engines"] == 72


def test_FR_EVAL_02_AC2_borderline_url_returns_ambiguous(monkeypatch):
    """FR-EVAL-02-AC2: Single detection returns Ambiguous verdict."""
    async def mock_borderline_report(url, api_key, client=None):
        return {
            "url": url,
            "verdict": "Ambiguous",
            "positives": 1,
            "total_engines": 70,
            "scan_date": "2026-11-09 12:00:00 UTC",
            "cached": True,
            "malicious_count": 1,
            "suspicious_count": 0,
            "harmless_count": 65,
            "undetected_count": 4,
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_borderline_report)

    response = client.post(
        "/scan", json={"url": "https://borderline-site.example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Ambiguous"
    assert data["positives"] == 1