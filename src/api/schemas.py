from datetime import datetime, timezone
from typing import Any, Dict, Optional, Union
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ScanRequest(BaseModel):
    """Schema for incoming URL scan submission with boundary checks."""

    url: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Target HTTP or HTTPS URL to scan",
    )

    @field_validator("url")
    @classmethod
    def validate_url_scheme_and_content(cls, v: str) -> str:
        trimmed = v.strip() if v else ""
        if not trimmed:
            raise ValueError("URL cannot be empty or whitespace")

        if ":" in v:
            candidate = v.split(":", 1)[0].lower()
            if candidate.isalpha() and candidate not in ("http", "https"):
                raise ValueError(f"Unsupported scheme: {candidate}")
        return v


class ScanResponse(BaseModel):
    """Schema for finalized scan verdict and engine statistics."""

    model_config = ConfigDict(extra="allow")

    url: str
    verdict: str = "Safe"
    positives: int = 0
    total_engines: int = 0
    scan_date: Union[str, int] = "N/A"
    cached: bool = False
    raw_details: Optional[Dict[str, Any]] = None

    # Front-end seam and legacy mock compatibility fields
    malicious_count: Optional[int] = None
    suspicious_count: Optional[int] = None
    harmless_count: Optional[int] = None
    undetected_count: Optional[int] = None
    scan_id: Optional[str] = None
    engine_results: Optional[Dict[str, Any]] = None

    @model_validator(mode="before")
    @classmethod
    def populate_defaults_from_legacy(cls, data: Any) -> Any:
        """Derive standard fields if receiving legacy or test mock payloads."""
        if isinstance(data, dict):
            if "positives" not in data and "malicious_count" in data:
                data["positives"] = data["malicious_count"]

            if data.get("malicious_count") is None:
                data["malicious_count"] = data.get(
                    "malicious", data.get("positives", 0)
                )
            if data.get("suspicious_count") is None:
                data["suspicious_count"] = data.get("suspicious", 0)
            if data.get("harmless_count") is None:
                data["harmless_count"] = data.get("harmless", 0)
            if data.get("undetected_count") is None:
                data["undetected_count"] = data.get("undetected", 0)

            if not data.get("total_engines"):
                mal = data.get("malicious_count", 0) or 0
                susp = data.get("suspicious_count", 0) or 0
                harm = data.get("harmless_count", 0) or 0
                undet = data.get("undetected_count", 0) or 0
                total = mal + susp + harm + undet
                data["total_engines"] = total if total > 0 else 0

            if "verdict" not in data:
                pos = data.get("positives", 0)
                data["verdict"] = "Safe" if pos == 0 else "Unsafe"
            if "scan_date" not in data:
                data["scan_date"] = "N/A"
        return data

    @field_validator("scan_date", mode="before")
    @classmethod
    def normalize_scan_date(cls, value: Any) -> str:
        """Convert integer Unix epoch timestamps to formatted UTC strings."""
        if value is None:
            return "N/A"
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value, tz=timezone.utc)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        return str(value)
