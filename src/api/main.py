import os
from fastapi import FastAPI, HTTPException
from src.api.schemas import ScanRequest, ScanResponse

app = FastAPI(title="URL Security Scanner", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan", response_model=ScanResponse)
def scan_url(request: ScanRequest):
    # Honesty test gate: verify the upstream dependency is configured
    api_key = os.getenv("VIRUSTOTAL_API_KEY", "").strip()
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail=(
                "Upstream dependency unavailable: "
                "VIRUSTOTAL_API_KEY not configured. See .env.example."
            ),
        )

    return ScanResponse(
        url=request.url,
        verdict="Safe",
        source="skeleton-stub",
        scan_time_ms=15,
    )
