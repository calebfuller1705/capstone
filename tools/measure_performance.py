import json
import os
import statistics
import sys
import time

# Ensure project root is in sys.path regardless of how the script is invoked
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from fastapi.testclient import TestClient
from src.api.main import app

FIXTURE_PATH = os.path.join(PROJECT_ROOT, "tests", "fixtures", "perf_seed_500.json")
SAMPLE_COUNT = 50


def measure():
    if not os.path.exists(FIXTURE_PATH):
        print(f"Error: Missing fixture file: {FIXTURE_PATH}", file=sys.stderr)
        sys.exit(2)

    with open(FIXTURE_PATH, "r", encoding="utf-8") as f:
        pool = json.load(f)

    samples = pool[:SAMPLE_COUNT]

    with TestClient(app) as client:
        # Warmup ASGI router
        client.get("/health")

        latencies = []
        for entry in samples:
            url = entry["url"]
            start = time.perf_counter()
            response = client.post("/scan", json={"url": url})
            elapsed_ms = (time.perf_counter() - start) * 1000.0

            if response.status_code != 200:
                print(f"Warning: Non-200 status {response.status_code} on {url}", file=sys.stderr)
            latencies.append(elapsed_ms)

    latencies.sort()
    p50 = statistics.median(latencies)
    p95_idx = int(len(latencies) * 0.95) - 1
    p95 = latencies[p95_idx]

    print("\n---------------- NFR-PERF-01 BENCHMARK ----------------")
    print(f"Volume pool:     {len(pool)} records")
    print(f"Sample run:      {SAMPLE_COUNT} consecutive requests")
    print(f"Min latency:     {latencies[0]:.2f} ms")
    print(f"Median (p50):    {p50:.2f} ms")
    print(f"95th %ile (p95): {p95:.2f} ms")
    print(f"Max latency:     {latencies[-1]:.2f} ms")
    print(f"Target:          <= 500.00 ms at p95")
    verdict = "PASS" if p95 <= 500.0 else "MISS"
    print(f"Verdict:         {verdict}")
    print("------------------------------------------------------\n")
    return p50, p95, verdict


if __name__ == "__main__":
    measure()