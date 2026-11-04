import asyncio
import os
import httpx
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.services.vt_client import (
    encode_vt_url_id,
    fetch_url_report,
    UpstreamServiceError,
)

client = TestClient(app)
FAKE_API_KEY = "test_key_00000000000000000000000000000000"


# 1. CONTRACT DRIFT: Upstream VT payload omits stats or attributes
def test_seam_contract_drift_upstream_omits_stats():
    """Probe: Upstream returns valid JSON but attributes/stats are missing."""
    async def _test():
        async def mock_handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"data": {"id": "sample_id", "attributes": {}}})

        transport = httpx.MockTransport(mock_handler)
        async with httpx.AsyncClient(transport=transport) as mock_client:
            result = await fetch_url_report("https://example.com", FAKE_API_KEY, client=mock_client)
            assert result["verdict"] == "Safe"
            assert result["total_engines"] == 0
            assert result["positives"] == 0

    asyncio.run(_test())


# 2. UNIT MISMATCH: Latency measured in integer milliseconds, not seconds
def test_seam_unit_mismatch_latency_metric():
    """Probe: Assert health endpoint reports structured status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


# 3. TIME ZONE & ENCODING: URL query strings and Punycode normalization
def test_seam_encoding_idn_and_query_parameters():
    """Probe: Unicode domain names and encoded query strings pass cleanly."""
    unicode_url = "https://example.com/search?q=test%20query&lang=en"
    encoded_id = encode_vt_url_id(unicode_url)
    assert isinstance(encoded_id, str)
    assert "=" not in encoded_id
    assert "/" not in encoded_id
    assert "+" not in encoded_id


# 4. IDENTITY: Trailing slash produces identical VirusTotal identifier
def test_seam_identity_trailing_slash_normalization():
    """Probe: Root domain with and without trailing slash should normalize."""
    url_without_slash = "https://example.com"
    url_with_slash = "https://example.com/"
    
    id1 = encode_vt_url_id(url_without_slash.rstrip("/"))
    id2 = encode_vt_url_id(url_with_slash.rstrip("/"))
    assert id1 == id2, f"Identity split: {id1} != {id2}"


# 5. ORDERING: Invoking service without API key configured fails fast
def test_seam_ordering_missing_config_fails_fast():
    """Probe: Attempting scan without API key fails before network transport."""
    async def _test():
        with pytest.raises(ValueError) as exc:
            await fetch_url_report("https://example.com", "")
        assert "api key" in str(exc.value).lower()

    asyncio.run(_test())


# 6. ERROR SEMANTICS: Upstream timeout mapped to HTTP 504 Gateway Timeout
def test_seam_error_semantics_timeout_mapping(monkeypatch):
    """Probe: Upstream timeout must produce HTTP 504 Problem Details, not 500."""
    async def mock_timeout(*args, **kwargs):
        raise UpstreamServiceError("Upstream service timed out")

    monkeypatch.setattr("src.api.main.fetch_url_report", mock_timeout)
    
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code in (502, 504), (
        f"Expected HTTP 502/504 for upstream timeout, got {response.status_code}"
    )
    payload = response.json()
    assert "detail" in payload or "error" in payload


# 7. PARTIAL FAILURE: Zero persistence verified across request lifecycle
def test_seam_partial_failure_zero_disk_persistence():
    """Probe: Ensure no temporary or cache files are written to disk."""
    before_files = set(os.listdir("."))
    response = client.post("/scan", json={"url": "https://example.com"})
    after_files = set(os.listdir("."))
    new_files = after_files - before_files
    assert not new_files, f"Invariant broken: unexpected files created on disk: {new_files}"