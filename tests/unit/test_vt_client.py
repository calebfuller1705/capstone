import pytest
from src.services.vt_client import encode_vt_url_id, get_vt_api_key


def test_encode_vt_url_id_unpadded():
    # VirusTotal v3 unpadded base64url standard test
    url = "https://example.com"
    expected = "aHR0cHM6Ly9leGFtcGxlLmNvbQ"
    assert encode_vt_url_id(url) == expected


def test_encode_vt_url_id_empty_raises():
    with pytest.raises(ValueError, match="URL cannot be empty"):
        encode_vt_url_id("")


def test_get_vt_api_key_valid(monkeypatch):
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "dummy-key-12345")
    assert get_vt_api_key() == "dummy-key-12345"


def test_get_vt_api_key_missing_or_whitespace_raises(monkeypatch):
    monkeypatch.setenv("VIRUSTOTAL_API_KEY", "   ")
    with pytest.raises(ValueError, match="missing or empty"):
        get_vt_api_key()
