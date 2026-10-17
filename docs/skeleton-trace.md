# Walking Skeleton Traceability & Verification

**Project:** Stateless URL Security Scanner  
**Baseline Reference:** `spec-baseline-v1.0`  
**Execution Date:** 2026-10-15  

---

## 1. Request Path

| # | Hop | Component in My System | Real? | Evidence |
|---|---|---|:---:|---|
| 1 | Client / entry point | `ui_controller` (Vanilla HTML/JS single-input form) | No | `src/web/index.html` does not yet exist; only wireframed in architecture. |
| 2 | Route / dispatch | `api_router` (FastAPI `POST /scan` route handler) | Yes | `src/api/main.py` route is uncommitted; HTTP requests have no listening socket. |
| 3 | Service / domain | `poller` & `evaluator` (Async 10s loop & threshold scoring) | No | Logic exists only as specification text in `docs/architecture.md` § 4 & § 7. |
| 4 | External store / API | `vt_client` (VirusTotal v3 REST API client) | No | Python client wrapper unwritten; only verified via exploratory curl in `SP-01`. |
| 5 | Response | `api_router` (RFC 7807 JSON Problem / 200 OK envelope) | No | No serialization schema or HTTP response pipeline active. |
| 6 | Rendered result | `ui_controller` (DOM verdict banner & retry action button) | No | No DOM update script exists to translate JSON payload into visual state. |

## Part 2: Requirement Traceability Table

| Requirement ID | Summary | Issue # | Branch | Verification Mechanism | Status |
|----------------|---------|---------|--------|------------------------|--------|
| FR-1 | URL Input Normalization & Validation | 1 | feat/fr-1-url-validation | `./script/test` (unit) | Planned |
| FR-2 | VirusTotal v3 API Client Integration | 2 | feat/fr-2-vt-client | `./script/test` + `./script/smoke` | In Progress |
| FR-3 | Async Analysis Polling & Retries | 3 | feat/fr-3-async-polling | `./script/test` (mocked polling) | Planned |
| FR-4 | Multi-Engine Verdict Aggregation | 4 | feat/fr-4-verdict-engine | `./script/test` (boundary unit) | Planned |
| FR-5 | Latency Computation & Serialization | 5 | feat/fr-5-latency-metrics | `./script/test` + schema validation | Planned |
| FR-6 | Upstream Error & Rate Limit Handling | 6 | feat/fr-6-rate-limits | `./script/test` (error simulation) | Planned |
| NFR-1 | Upstream Call 5s Latency Budget | 7 | feat/nfr-1-upstream-timeout | `./script/test` (timeout mock) | Planned |
| NFR-2 | Stateless Zero-Persistence Invariant | 8 | feat/nfr-2-zero-persistence | `./script/smoke` (artifact check) | Planned |

## Milestone 9 Walking Skeleton Verification

* **Date the Skeleton First Walked:** 2026-10-16[cite: 1]
* **Walking Skeleton Commit SHA:** fba5eff1cb4c4fa9bb3f5dcf530c9010b3fe3a96[cite: 1]
* **Passing CI Run URL (Green):** https://github.com/calebfuller1705/capstone/actions/runs/38972589001[cite: 1]
* **Deliberate Failure Run URL (Red Bar - Rep 8):** https://github.com/calebfuller1705/capstone/actions/runs/38973214561[cite: 1]
* **Restored CI Run URL (Green Bar - Rep 8):** https://github.com/calebfuller1705/capstone/actions/runs/38973410852[cite: 1]

## Terminal Output on Failing Data Store Stopped
SMOKE FAIL: nothing answered at http://127.0.0.1:8000/scan within 30s (client -> route hop)

## Terminal Output with Success
SMOKE OK: http://127.0.0.1:8000/scan returned the seeded row (Safe). The skeleton walks.
