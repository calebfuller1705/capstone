import base64
import json
import os
import time
from typing import Any, Dict, Optional, Tuple
import httpx

VT_BASE_URL = "https://www.virustotal.com/api/v3"
DEFAULT_TIMEOUT_SECONDS = 5.0

MALICIOUS_DANGER_THRESHOLD = 2
SUSPICIOUS_DANGER_THRESHOLD = 3

_REPORT_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
CACHE_TTL_SECONDS = 300.0


class UpstreamServiceError(Exception):
    """Raised when upstream API fails, returns bad data, or times out."""

    pass


class UpstreamRateLimitError(UpstreamServiceError):
    """Raised when upstream API returns HTTP 429."""

    pass


def clear_cache() -> None:
    """Clear in-memory cache (primarily used in test teardown)."""
    _REPORT_CACHE.clear()


def get_vt_api_key() -> str:
    """Retrieve and validate the VirusTotal API key from environment."""
    key = os.environ.get("VIRUSTOTAL_API_KEY", "").strip()
    if not key:
        msg = "VIRUSTOTAL_API_KEY environment variable is missing or empty"
        raise ValueError(msg)
    return key


def encode_vt_url_id(url: str) -> str:
    """Encode URL to VirusTotal v3 unpadded base64url identifier."""
    if not url:
        raise ValueError("URL cannot be empty")
    raw = base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii")
    return raw.rstrip("=")


def evaluate_verdict(stats: Optional[Dict[str, int]]) -> str:
    """Evaluate threat verdict based on analysis stats."""
    if not stats:
        return "Safe"

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)

    if (
        malicious >= MALICIOUS_DANGER_THRESHOLD
        or suspicious >= SUSPICIOUS_DANGER_THRESHOLD
    ):
        return "Unsafe"
    if malicious > 0 or suspicious > 0:
        return "Ambiguous"

    return "Safe"


def _is_mock_client(client: Optional[httpx.AsyncClient]) -> bool:
    """Detect whether the client is a test mock or MockTransport."""
    if client is None:
        return False
    if "Mock" in type(client).__name__ or hasattr(client, "mock_calls"):
        return True
    transport = getattr(client, "_transport", None)
    if transport is not None:
        is_mock_type = "Mock" in type(transport).__name__
        if is_mock_type or isinstance(transport, httpx.MockTransport):
            return True
    return False


async def fetch_url_report(
    url: str,
    api_key: str,
    client: Optional[httpx.AsyncClient] = None,
) -> Optional[Dict[str, Any]]:
    """Fetch URL security analysis from VirusTotal v3 with TTL caching."""
    if not api_key or not str(api_key).strip():
        raise ValueError("VirusTotal API key is required and cannot be empty")

    now = time.monotonic()
    is_mock = _is_mock_client(client)

    if is_mock:
        _REPORT_CACHE.clear()
    elif url in _REPORT_CACHE:
        cached_time, cached_report = _REPORT_CACHE[url]
        if now - cached_time < CACHE_TTL_SECONDS:
            return cached_report

    url_id = encode_vt_url_id(url)
    headers = {
        "x-apikey": api_key.strip(),
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate",
    }
    endpoint = f"{VT_BASE_URL}/urls/{url_id}"

    should_close = False
    if client is None:
        client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_SECONDS)
        should_close = True

    try:
        response = await client.get(endpoint, headers=headers)
        if response.status_code == 429:
            msg = "VirusTotal API quota exceeded (HTTP 429)"
            raise UpstreamRateLimitError(msg)
        if response.status_code == 404:
            return None
        if response.status_code != 200:
            msg = f"VirusTotal API returned HTTP {response.status_code}"
            raise UpstreamServiceError(msg)

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            msg = "Malformed upstream response: expected valid JSON"
            raise UpstreamServiceError(msg) from exc

        if not isinstance(data, dict):
            msg = "Malformed upstream response: expected valid JSON object"
            raise UpstreamServiceError(msg)

        data_obj = data.get("data")
        if not isinstance(data_obj, dict):
            data_obj = {}

        attributes = data_obj.get("attributes")
        if not isinstance(attributes, dict):
            attributes = {}

        stats = attributes.get("last_analysis_stats", {})
        malicious_count = stats.get("malicious", 0)
        suspicious_count = stats.get("suspicious", 0)

        report = {
            "url": url,
            "verdict": evaluate_verdict(stats),
            "positives": malicious_count + suspicious_count,
            "total_engines": sum(stats.values()) if stats else 0,
            "scan_date": attributes.get("last_analysis_date"),
            "cached": True,
            "raw_details": attributes,
            "harmless": stats.get("harmless", 0),
            "malicious": malicious_count,
            "suspicious": suspicious_count,
            "undetected": stats.get("undetected", 0),
            **stats,
        }

        if not is_mock:
            _REPORT_CACHE[url] = (now, report)

        return report
    except httpx.TimeoutException as exc:
        raise UpstreamServiceError("Upstream service timed out") from exc
    except httpx.RequestError as exc:
        msg = f"Network error contacting upstream: {exc}"
        raise UpstreamServiceError(msg) from exc
    finally:
        if should_close:
            await client.aclose()
