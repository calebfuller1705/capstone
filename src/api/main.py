import ipaddress
import os
from contextlib import asynccontextmanager
from pathlib import Path
from urllib.parse import urlparse
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.api.schemas import ScanRequest, ScanResponse
from src.services.vt_client import (
    fetch_url_report,
    UpstreamServiceError,
    UpstreamRateLimitError,
)

load_dotenv()

http_resources = {}
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def is_private_or_intranet_url(url: str) -> bool:
    """Validate target URL against loopback, private IP, or metadata."""
    try:
        parsed = urlparse(url)
        hostname = parsed.hostname
        if not hostname:
            return False

        hostname_lower = hostname.lower()
        if hostname_lower in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return True

        internal_suffixes = (".local", ".internal", ".lan")
        if any(hostname_lower.endswith(s) for s in internal_suffixes):
            return True

        try:
            ip = ipaddress.ip_address(hostname_lower)
            return (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
                or ip.is_unspecified
            )
        except ValueError:
            return False
    except Exception:
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle resources with connection pooling."""
    limits = httpx.Limits(
        max_keepalive_connections=50,
        max_connections=100,
        keepalive_expiry=30.0,
    )
    http_resources["client"] = httpx.AsyncClient(timeout=5.0, limits=limits)
    yield
    client: httpx.AsyncClient = http_resources.get("client")
    if client and not client.is_closed:
        await client.aclose()


app = FastAPI(
    title="URL Security Scanner",
    description="Stateless URL safety verification against VirusTotal v3",
    version="0.9.0-rc.1",
    lifespan=lifespan,
)

# Mount static asset bundle
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", include_in_schema=False)
async def serve_index():
    """Serve the single-page application shell."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"status": "ok", "app": "URL Security Scanner"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Lightweight health check endpoint for monitoring."""
    return {"status": "ok"}


@app.post("/scan", response_model=ScanResponse, status_code=status.HTTP_200_OK)
async def scan_url(request: ScanRequest):
    """Scan a target URL string against VirusTotal v3."""
    api_key = os.environ.get("VIRUSTOTAL_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: missing VIRUSTOTAL_API_KEY",
        )

    normalized_url = request.url
    if normalized_url.endswith("/") and normalized_url.count("/") == 3:
        normalized_url = normalized_url.rstrip("/")

    # Guard against SSRF to private and internal networks (FR-EVAL-01)
    if is_private_or_intranet_url(normalized_url):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                "Unscannable intranet URL: private, loopback, and metadata "
                "addresses are restricted (FR-EVAL-01)"
            ),
        )

    try:
        shared_client = http_resources.get("client")
        report = await fetch_url_report(
            normalized_url, api_key, client=shared_client
        )
        if report is None:
            report = {
                "url": normalized_url,
                "verdict": "Unknown",
                "positives": 0,
                "total_engines": 0,
                "scan_date": "N/A",
                "cached": False,
                "raw_details": {},
            }
        return ScanResponse(**report)

    except HTTPException:
        raise
    except UpstreamRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc),
        )
    except UpstreamServiceError as exc:
        if "timed out" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Upstream threat intelligence service timed out",
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream service error: {exc}",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected internal error occurred while processing the request",
        )