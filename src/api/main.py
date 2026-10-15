from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

app = FastAPI(title="URL Security Scanner", version="0.1.0")

# DR-005: Lock down CORS to FRONTEND_URL
allowed_origins = [os.getenv("FRONTEND_URL", "http://localhost:8000")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScanRequest(BaseModel):
    url: str = Field(..., max_length=2048, description="Target URL to analyze")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/scan")
async def scan_url(payload: ScanRequest):
    # DR-003: Take out any whitespace
    cleaned_url = payload.url.strip()
    
    # Real route response
    return {
        "url": cleaned_url,
        "verdict": "Safe",
        "source": "skeleton-stub",
        "scan_time_ms": 15
    }