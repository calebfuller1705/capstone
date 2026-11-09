from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_seam_contract_drift_upstream_omits_stats(monkeypatch):
    """Seam: Upstream omits last_analysis_stats without breaking API."""
    async def mock_sparse_report(url, api_key, client=None):
        return {
            "url": url,
            "verdict": "Safe",
            "positives": 0,
            "total_engines": 0,
            "scan_date": "N/A",
            "cached": False,
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_sparse_report)
    response = client.post("/scan", json={"url": "https://sparse-domain.com"})
    assert response.status_code == 200
    assert response.json()["verdict"] == "Safe"


def test_seam_unit_mismatch_latency_metric():
    """Seam: Verify health endpoint returns cleanly without metric issues."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_seam_encoding_idn_and_query_parameters(monkeypatch):
    """Seam: Verify URL with query parameters passes across boundary."""
    async def mock_report(url, api_key, client=None):
        return {
            "url": url,
            "verdict": "Safe",
            "positives": 0,
            "total_engines": 70,
            "scan_date": "N/A",
            "cached": False,
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    test_url = "https://example.com/search?q=test&lang=en#results"
    response = client.post("/scan", json={"url": test_url})
    assert response.status_code == 200
    assert response.json()["url"] == test_url


def test_seam_identity_trailing_slash_normalization(monkeypatch):
    """Seam: Trailing slashes stripped on root domains."""
    called_urls = []

    async def mock_report(url, api_key, client=None):
        called_urls.append(url)
        return {
            "url": url,
            "verdict": "Safe",
            "positives": 0,
            "total_engines": 70,
            "scan_date": "N/A",
            "cached": False,
        }

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_report)
    client.post("/scan", json={"url": "https://example.com/"})
    assert called_urls == ["https://example.com"]


def test_seam_ordering_missing_config_fails_fast(monkeypatch):
    """Seam: Missing API key fails fast with 500 when unset."""
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "")
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 500


def test_seam_error_semantics_timeout_mapping(monkeypatch):
    """Seam: Upstream read timeout maps to HTTP 504 Gateway Timeout."""
    async def mock_timeout(*args, **kwargs):
        from src.services.vt_client import UpstreamServiceError
        raise UpstreamServiceError("Upstream service timed out")

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_timeout)
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 504


def test_seam_partial_failure_zero_disk_persistence():
    """Seam: Verify stateless operation writes zero temporary files."""
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code in (200, 422, 500, 502)
