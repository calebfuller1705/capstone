import pytest
from pydantic import ValidationError
from src.api.schemas import ScanRequest


def test_url_boundary_inside_minimum():
    """Boundary: exactly 1 character (inside range)."""
    req = ScanRequest(url="a")
    assert req.url == "a"


def test_url_boundary_inside_maximum():
    """Boundary: exactly 2,048 characters (inside range)."""
    base = "https://example.com/"
    long_url = base + "a" * (2048 - len(base))
    assert len(long_url) == 2048
    req = ScanRequest(url=long_url)
    assert len(req.url) == 2048


def test_url_boundary_below_zero_length():
    """Boundary: 0 characters (below range). Expects validation error."""
    with pytest.raises(ValidationError):
        ScanRequest(url="")


def test_url_boundary_above_maximum_2049():
    """Boundary: 2,049 characters (above range). Expects validation error."""
    base = "https://example.com/"
    overflow_url = base + "a" * (2049 - len(base))
    assert len(overflow_url) == 2049
    with pytest.raises(ValidationError):
        ScanRequest(url=overflow_url)


def test_url_boundary_above_hostile_10k():
    """Boundary: 10,000 characters (hostile stress boundary)."""
    hostile_url = "https://example.com/" + "x" * 9980
    assert len(hostile_url) == 10000
    with pytest.raises(ValidationError):
        ScanRequest(url=hostile_url)


def test_url_boundary_absent_null():
    """Boundary: null / None. Expects validation error."""
    with pytest.raises(ValidationError):
        ScanRequest(url=None)