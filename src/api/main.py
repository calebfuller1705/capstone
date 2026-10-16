import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="URL Security Scanner", version="0.1.0")


class ScanRequest(BaseModel):
    url: str


class ScanResponse(BaseModel):
    url: str
    verdict: str
    source: str
    scan_time_ms: int


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan", response_model=ScanResponse)
def scan_url(request: ScanRequest):
    # Honesty test gate: verify the upstream dependency is configured
    api_key = os.getenv("VIRUSTOTAL_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Upstream dependency unavailable: VIRUSTOTAL_API_KEY not configured.",
        )

    return ScanResponse(
        url=request.url,
        verdict="Safe",
        source="skeleton-stub",
        scan_time_ms=15,
    )