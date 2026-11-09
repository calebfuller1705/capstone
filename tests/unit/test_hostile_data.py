import pytest
from pydantic import ValidationError
from src.api.schemas import ScanRequest


def load_hostile_records():
    """Generate boundary test cases for hostile URL inputs."""
    long_payload = "https://example.com/" + ("A" * 9980)
    return [
        {"id": "HOSTILE-001", "url": "https://normal-domain.com"},
        {"id": "HOSTILE-002", "url": "http://sub.domain.org/path?k=v"},
        {"id": "HOSTILE-003", "url": "https://domain.com/path#fragment"},
        {"id": "HOSTILE-004", "url": "https://1.1.1.1/dns-query"},
        {"id": "HOSTILE-005", "url": "https://example.com:8443/api"},
        {"id": "HOSTILE-006", "url": "https://example.com/spaced%20path"},
        {"id": "HOSTILE-007", "url": "javascript:alert('xss')"},
        {"id": "HOSTILE-008", "url": "file:///etc/passwd"},
        {"id": "HOSTILE-009", "url": "https://user:pass@domain.com"},
        {"id": "HOSTILE-010", "url": "https://xn--e1afmkfd.xn--p1ai"},
        {"id": "HOSTILE-011", "url": long_payload},
        {"id": "HOSTILE-012", "url": "https://[:::1]:8080/scan"},
    ]


@pytest.mark.parametrize(
    "record", load_hostile_records(), ids=lambda r: r["id"]
)
def test_hostile_input_handling(record):
    raw_url = record["url"]
    if record["id"] in ("HOSTILE-007", "HOSTILE-008", "HOSTILE-011"):
        with pytest.raises(ValidationError):
            ScanRequest(url=raw_url)
    else:
        req = ScanRequest(url=raw_url)
        assert req.url == raw_url
