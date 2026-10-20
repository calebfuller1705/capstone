import base64
import os


def get_vt_api_key() -> str:
    """Retrieve and validate the VirusTotal API key."""
    api_key = os.getenv("VIRUSTOTAL_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "VIRUSTOTAL_API_KEY environment variable is missing or empty."
        )
    return api_key


def encode_vt_url_id(url: str) -> str:
    """
    Encode target URL into an unpadded base64url string per VirusTotal v3 spec.
    """
    if not url:
        raise ValueError("URL cannot be empty.")
    encoded = base64.urlsafe_b64encode(url.encode("utf-8")).decode("utf-8")
    return encoded.rstrip("=")
