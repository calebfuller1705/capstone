from fastapi import FastAPI
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
    return ScanResponse(
        url=request.url,
        verdict="Safe",
        source="skeleton-stub",
        scan_time_ms=15,
    )
