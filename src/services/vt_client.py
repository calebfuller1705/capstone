import base64
import json
from typing import Any, Dict, Optional
import httpx

VT_BASE_URL = "https://www.virustotal.com/api/v3"
DEFAULT_TIMEOUT_SECONDS = 5.0

MALICIOUS_DANGER_THRESHOLD = 2
SUSPICIOUS_DANGER_THRESHOLD = 3


class UpstreamServiceError(Exception):
    """Raised when upstream API fails, returns malformed data, or times out."""
    pass


class UpstreamRateLimitError(UpstreamServiceError):
    """Raised when upstream API returns HTTP 429."""
    pass


def encode_vt_url_id(url: str) -> str:
    """Encode URL to VirusTotal v3 unpadded base64url identifier."""
    return base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")


def evaluate_verdict(stats: Optional[Dict[str, int]]) -> str:
    """Evaluate threat verdict based on analysis stats."""
    if not stats:
        return "Safe"

    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)

    if malicious >= MALICIOUS_DANGER_THRESHOLD or suspicious >= SUSPICIOUS_DANGER_THRESHOLD:
        return "Unsafe"
    if malicious > 0 or suspicious > 0:
        return "Ambiguous"

    return "Safe"


async def fetch_url_report(
    url: str,
    api_key: str,
    client: Optional[httpx.AsyncClient] = None
) -> Dict[str, Any]:
    """Fetch URL security analysis from VirusTotal v3."""
    url_id = encode_vt_url_id(url)
    headers = {
        "x-apikey": api_key,
        "Accept": "application/json",
    }
    endpoint = f"{VT_BASE_URL}/urls/{url_id}"

    should_close = False
    if client is None:
        client = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT_SECONDS)
        should_close = True

    try:
        response = await client.get(endpoint, headers=headers)
        if response.status_code == 429:
            raise UpstreamRateLimitError("VirusTotal API quota exceeded (HTTP 429)")
        if response.status_code != 200:
            raise UpstreamServiceError(f"VirusTotal API returned HTTP {response.status_code}")

        try:
            data = response.json()
        except (json.JSONDecodeError, ValueError) as exc:
            raise UpstreamServiceError("Malformed upstream response: expected valid JSON") from exc

        attributes = data.get("data", {}).get("attributes", {})
        stats = attributes.get("last_analysis_stats", {})

        return {
            "url": url,
            "verdict": evaluate_verdict(stats),
            "positives": stats.get("malicious", 0) + stats.get("suspicious", 0),
            "total_engines": sum(stats.values()) if stats else 0,
            "scan_date": attributes.get("last_analysis_date"),
            "cached": True,
            "raw_details": attributes
        }
    except httpx.TimeoutException as exc:
        raise UpstreamServiceError("Upstream service timed out") from exc
    except httpx.RequestError as exc:
        raise UpstreamServiceError(f"Network error contacting upstream: {exc}") from exc
    finally:
        if should_close:
            await client.aclose()