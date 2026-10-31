import json
import os
import pytest
from pydantic import ValidationError
from src.api.schemas import ScanRequest
from src.services.vt_client import encode_vt_url_id

FIXTURE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures", "test_data_hostile.json")


def load_hostile_records():
    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["records"]


@pytest.mark.parametrize("record", load_hostile_records(), ids=lambda r: r["id"])
def test_hostile_input_handling(record):
    raw_url = record["url"]

    if record["id"] in ("HOSTILE-007", "HOSTILE-008", "HOSTILE-011"):
        with pytest.raises(ValidationError):
            ScanRequest(url=raw_url)
    else:
        req = ScanRequest(url=raw_url)
        assert req.url == raw_url

        encoded = encode_vt_url_id(req.url)
        assert isinstance(encoded, str)
        assert not encoded.endswith("=")