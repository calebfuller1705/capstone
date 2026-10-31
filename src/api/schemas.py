import re
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, field_validator

DISALLOWED_SCHEMES = ("javascript:", "file:", "data:", "vbscript:", "about:")


class ScanRequest(BaseModel):
    """Payload submitted by client for URL scanning."""
    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Target URL to inspect (1 to 2,048 characters)."
    )

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> str:
        if v is None:
            raise ValueError("URL cannot be null")
        v_clean = v.strip()
        if not v_clean:
            raise ValueError("URL cannot be empty or contain only whitespace")
        if len(v_clean) > 2048:
            raise ValueError("URL length cannot exceed 2048 characters")
        
        lower_val = v_clean.lower()
        if lower_val.startswith(DISALLOWED_SCHEMES) or re.match(r"^[a-zA-Z0-9_\-\.]+:(?!//)", v_clean):
            raise ValueError("Unsupported or dangerous URI scheme")
            
        return v_clean


class ScanResponse(BaseModel):
    """Analysis results payload returned to client."""
    url: str
    verdict: str = Field(..., description="Verdict: Safe, Unsafe, or Ambiguous")
    positives: int = Field(default=0, ge=0)
    total_engines: int = Field(default=0, ge=0)
    scan_date: Optional[str] = None
    permalink: Optional[str] = None
    cached: bool = False
    raw_details: Optional[Dict[str, Any]] = None