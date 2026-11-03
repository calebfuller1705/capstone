"""Contract, property invariant, golden set, and failure path tests for VirusTotal API."""

import httpx
import pytest
from src.services.vt_client import (
    fetch_url_report,
    UpstreamServiceError,
    UpstreamRateLimitError,
)

FAKE_API_KEY = "test_api_key_00000000000000000000000000000000"
TEST_URL = "https://example.com"

# 3. GOLDEN SET: 5 Fixed Historical Engine Distribution Fixtures

GOLDEN_FIXTURES = [
    {
        "id": "GOLDEN-01-CLEAN",
        "raw": {"data": {"attributes": {"last_analysis_stats": {"harmless": 72, "malicious": 0, "suspicious": 0, "undetected": 15}, "last_analysis_date": 1730000000}}},
        "expected_verdict": "Safe"
    },
    {
        "id": "GOLDEN-02-BORDERLINE",
        "raw": {"data": {"attributes": {"last_analysis_stats": {"harmless": 65, "malicious": 1, "suspicious": 0, "undetected": 10}, "last_analysis_date": 1730000001}}},
        "expected_verdict": "Ambiguous"
    },
    {
        "id": "GOLDEN-03-MALICIOUS",
        "raw": {"data": {"attributes": {"last_analysis_stats": {"harmless": 30, "malicious": 8, "suspicious": 4, "undetected": 5}, "last_analysis_date": 1730000002}}},
        "expected_verdict": "Unsafe"
    },
    {
        "id": "GOLDEN-04-MINIMAL",
        "raw": {"data": {"attributes": {"last_analysis_stats": {"harmless": 50, "malicious": 0, "suspicious": 0, "undetected": 0}, "last_analysis_date": 1730000003}}},
        "expected_verdict": "Safe"
    },
    {
        "id": "GOLDEN-05-HEAVY-THREAT",
        "raw": {"data": {"attributes": {"last_analysis_stats": {"harmless": 0, "malicious": 55, "suspicious": 12, "undetected": 2}, "last_analysis_date": 1730000004}}},
        "expected_verdict": "Unsafe"
    }
]


# 1. STRUCTURE & 2. PROPERTY TESTS

@pytest.mark.parametrize("fixture", GOLDEN_FIXTURES, ids=lambda f: f["id"])
@pytest.mark.asyncio
async def test_structure_and_properties_on_golden_set(fixture):
    """
    1. STRUCTURE: Output parses; required keys present; types and ranges correct.
    2. PROPERTY: Invariants hold true across every valid output.
    """
    async def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=fixture["raw"])

    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport) as client:
        result = await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)

    assert isinstance(result, dict)
    for required_key in ("url", "verdict", "positives", "total_engines", "scan_date", "cached"):
        assert required_key in result, f"Missing required key: {required_key}"

    assert isinstance(result["url"], str)
    assert isinstance(result["verdict"], str)
    assert isinstance(result["positives"], int)
    assert isinstance(result["total_engines"], int)
    assert isinstance(result["cached"], bool)

    assert result["verdict"] in {"Safe", "Unsafe", "Ambiguous"}
    assert result["total_engines"] >= 0
    assert 0 <= result["positives"] <= result["total_engines"], (
        f"Invariant broken: positives ({result['positives']}) > total ({result['total_engines']})"
    )
    assert result["verdict"] == fixture["expected_verdict"]


# 4. FAILURE PATHS
@pytest.mark.asyncio
async def test_failure_path_rate_limit_429():
    """Failure 1: HTTP 429 quota exhaustion raises UpstreamRateLimitError."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": {"code": "QuotaExceededError", "message": "Quota exceeded"}})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(UpstreamRateLimitError) as exc_info:
            await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)
        assert "quota exceeded" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_failure_path_timeout():
    """Failure 2: Upstream timeout raises UpstreamServiceError within budget."""
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Connection timed out after 5.0s")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(UpstreamServiceError) as exc_info:
            await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)
        assert "timed out" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_failure_path_malformed_json():
    """Failure 3: Upstream returns invalid non-JSON body (e.g. gateway HTML error)."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html>502 Bad Gateway Nginx</html>", headers={"Content-Type": "text/html"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(UpstreamServiceError) as exc_info:
            await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)
        assert "malformed" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_failure_path_missing_attributes_key():
    """Failure 4: Upstream returns valid JSON but omits attributes or stats."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": {}})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        result = await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)
        assert result["verdict"] == "Safe"
        assert result["total_engines"] == 0
        assert result["positives"] == 0


@pytest.mark.asyncio
async def test_failure_path_upstream_503_service_down():
    """Failure 5: Upstream returns HTTP 503 Service Unavailable."""
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(503, text="Service Temporarily Unavailable")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as client:
        with pytest.raises(UpstreamServiceError) as exc_info:
            await fetch_url_report(TEST_URL, FAKE_API_KEY, client=client)
        assert "503" in str(exc_info.value)