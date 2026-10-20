from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    url: str = Field(
        ...,
        description="Target URL to scan",
        json_schema_extra={"example": "https://example.com"},
    )


class ScanResponse(BaseModel):
    url: str
    verdict: str
    source: str
    scan_time_ms: int
