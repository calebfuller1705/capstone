import os
from fastapi.testclient import TestClient
from src.api.main import app

os.environ.setdefault("VIRUSTOTAL_API_KEY", "unit-test-key")

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_scan_endpoint_skeleton_response():
    response = client.post("/scan", json={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["url"] == "https://example.com"
    assert data["verdict"] == "Safe"
