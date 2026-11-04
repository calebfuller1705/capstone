import os
from contextlib import asynccontextmanager
import httpx
from fastapi import FastAPI, HTTPException, status
from src.api.schemas import ScanRequest, ScanResponse
from src.services.vt_client import (
    fetch_url_report,
    UpstreamServiceError,
    UpstreamRateLimitError,
)

http_resources = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle resources with tuned connection limits."""
    limits = httpx.Limits(max_keepalive_connections=50, max_connections=100, keepalive_expiry=30.0)
    http_resources["client"] = httpx.AsyncClient(timeout=5.0, limits=limits)
    yield
    client: httpx.AsyncClient = http_resources.get("client")
    if client and not client.is_closed:
        await client.aclose()


app = FastAPI(
    title="URL Security Scanner",
    description="Stateless URL safety verification against VirusTotal v3",
    version="0.9.0-rc.1",
    lifespan=lifespan
)


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Lightweight health check endpoint for monitoring."""
    return {"status": "ok", "app": "URL Security Scanner"}


@app.post("/scan", response_model=ScanResponse, status_code=status.HTTP_200_OK)
async def scan_url(request: ScanRequest):
    """Scan a target URL string against VirusTotal v3."""
    api_key = os.environ.get("VIRUSTOTAL_API_KEY", "dummy_fallback_for_mock_tests")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server configuration error: missing VIRUSTOTAL_API_KEY"
        )

    try:
        normalized_url = request.url
        if normalized_url.endswith("/") and normalized_url.count("/") == 3:
            normalized_url = normalized_url.rstrip("/")

        shared_client = http_resources.get("client")
        report = await fetch_url_report(normalized_url, api_key, client=shared_client)
        return ScanResponse(**report)

    except UpstreamRateLimitError as exc:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(exc)
        )
    except UpstreamServiceError as exc:
        if "timed out" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Upstream threat intelligence service timed out"
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Upstream service error: {exc}"
        )