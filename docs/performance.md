# Performance Record — URL Security Scanner

This document tracks empirical measurements for non-functional requirements. In accordance with Section 12.2, all measurements are performed against realistic volume data using sample sizes of at least 30 requests and evaluated against tail percentiles (p50 and p95) rather than arithmetic averages.

---

## Non-Functional Target Measurements

| ID | Target | Method (load, env, sample) | p50 | p95 | Verdict | Action |
|---|---|---|---|---|---|---|
| **NFR-PERF-01** (Initial) | `POST /scan` < 500 ms p95 | 50 consecutive requests from 500-record volume pool (`perf_seed_500.json`), local clean ASGI runtime | 727.60 ms | 1083.40 ms | **MISS** | Ad-hoc client transport allocation paid TCP/TLS handshake penalties on every outbound call. Replaced with connection pooling and an ephemeral in-memory cache. |
| **NFR-PERF-01** (Re-measured) | `POST /scan` < 500 ms p95 | 50 consecutive requests from 500-record volume pool (`perf_seed_500.json`), local clean ASGI runtime | 83.80 ms | 184.22 ms | **PASS** | Socket keepalive and in-memory cache eliminated external transport churn; p95 dropped from 1083.40 ms to 184.22 ms (83% reduction). |
| **NFR-REL-01** | `GET /health` < 100 ms p95 | 30 requests, clean runtime | 2.80 ms | 7.40 ms | **PASS** | In-memory health probe requires zero external I/O; cleared target with no action required. |

---

## Measurement Protocol
* **Volume Seed:** `tests/fixtures/perf_seed_500.json` (500 synthetic enterprise URLs, fixed seed `20261104`)
* **Measurement Tool:** `tools/measure_performance.py`
* **Sample Count:** 50 consecutive requests outside the editor session
* **Tail Metric:** 95th percentile ($\text{p95}$) evaluated against the 500 ms ceiling
