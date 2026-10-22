import base64
import os
import httpx


class VTClientError(Exception):
    """Base exception for VirusTotal client operations."""

    pass


class UpstreamRateLimitError(VTClientError):
    """Raised when VirusTotal responds with HTTP 429."""

    pass


class UpstreamServiceError(VTClientError):
    """Raised on upstream 5xx, timeouts, or network disconnects."""

    pass


def get_vt_api_key() -> str:
    """Retrieve and validate the VirusTotal API key from environment."""
    api_key = os.getenv("VIRUSTOTAL_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "VIRUSTOTAL_API_KEY environment variable is missing or empty."
        )
    return api_key


def encode_vt_url_id(url: str) -> str:
    """
    Encode target URL into unpadded base64url string per VirusTotal v3 spec.
    """
    if not url:
        raise ValueError("URL cannot be empty.")
    encoded = base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8")
    return encoded.rstrip("=")


async def fetch_url_report(
    url: str,
    api_key: str,
    client: httpx.AsyncClient | None = None,
) -> dict | None:
    """
    Query VirusTotal v3 for existing URL analysis stats.
    Returns analysis dictionary on 200, None on 404 (unseen URL).
    """
    vt_id = encode_vt_url_id(url)
    endpoint = f"https://www.virustotal.com/api/v3/urls/{vt_id}"
    headers = {"x-apikey": api_key, "Accept": "application/json"}

    should_close_client = False
    if client is None:
        client = httpx.AsyncClient(timeout=5.0)
        should_close_client = True

    try:
        response = await client.get(endpoint, headers=headers)

        if response.status_code == 200:
            payload = response.json()
            return (
                payload.get("data", {})
                .get("attributes", {})
                .get("last_analysis_stats", {})
            )

        if response.status_code == 404:
            return None

        if response.status_code == 429:
            raise UpstreamRateLimitError("VirusTotal API quota exceeded.")

        if response.status_code >= 500:
            raise UpstreamServiceError(
                f"VirusTotal server error (HTTP {response.status_code})."
            )

        raise UpstreamServiceError(
            f"Unexpected upstream response (HTTP {response.status_code})."
        )

    except httpx.TimeoutException as exc:
        raise UpstreamServiceError(
            "Upstream connection to VirusTotal timed out."
        ) from exc
    except httpx.RequestError as exc:
        raise UpstreamServiceError(
            "Failed to connect to VirusTotal upstream."
        ) from exc
    finally:
        if should_close_client:
            await client.aclose()
