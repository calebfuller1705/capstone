import pytest
import httpx
from unittest.mock import AsyncMock, MagicMock
from src.services.vt_client import (
    encode_vt_url_id,
    get_vt_api_key,
    fetch_url_report,
    UpstreamRateLimitError,
    UpstreamServiceError,
)


def test_encode_vt_url_id_unpadded():
    url = "https://example.com"
    expected = "aHR0cHM6Ly9leGFtcGxlLmNvbQ"
    assert encode_vt_url_id(url) == expected


def test_encode_vt_url_id_empty_raises():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        encode_vt_url_id("")


def test_get_vt_api_key_valid(monkeypatch):
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "dummy-key-12345")
    assert get_vt_api_key() == "dummy-key-12345"


def test_get_vt_api_key_missing_or_whitespace_raises(monkeypatch):
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "   ")
    with pytest.raises(ValueError, match="missing or empty"):
        get_vt_api_key()


@pytest.mark.anyio
async def test_fetch_url_report_200_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 0,
                    "suspicious": 0,
                    "harmless": 70,
                    "undetected": 10,
                }
            }
        }
    }
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    stats = await fetch_url_report(
        "https://example.com", "dummy-key", client=mock_client
    )
    assert stats["harmless"] == 70
    assert stats["malicious"] == 0


@pytest.mark.anyio
async def test_fetch_url_report_404_returns_none():
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    result = await fetch_url_report(
        "https://unseen-url.com", "dummy-key", client=mock_client
    )
    assert result is None


@pytest.mark.anyio
async def test_fetch_url_report_429_rate_limit():
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.return_value = mock_response

    with pytest.raises(UpstreamRateLimitError, match="quota exceeded"):
        await fetch_url_report(
            "https://example.com", "dummy-key", client=mock_client
        )


@pytest.mark.anyio
async def test_fetch_url_report_timeout():
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_client.get.side_effect = httpx.TimeoutException(
        "Connection timed out"
    )

    with pytest.raises(UpstreamServiceError, match="timed out"):
        await fetch_url_report(
            "https://example.com", "dummy-key", client=mock_client
        )
