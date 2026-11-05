## Week 12 — Rep 1: The Seam Map

### Component Seam Map
| Seam | Crosses (process / network / storage?) | On an acceptance path? | Tested today? | Tier |
|---|---|---|---|---|
| 1. User -> ui_controller (Web Client) | Process (User input event to browser process) | Yes (FR-INP-01, NFR-USE-01, NFR-ACC-01..05) | Partially (Tested manually in Rep 12; automated DOM tests absent) | Tier 1 |
| 2. ui_controller -> input_validator | In-process (JavaScript function call) | Yes (FR-INP-01, FR-INP-02, FR-INP-03) | No (Client-side validation component not yet built) | Tier 2 |
| 3. ui_controller (Client) -> api_router (FastAPI) | Network & Process (HTTPS / JSON POST /scan) | Yes (FR-INP-01, FR-6, NFR-PERF-01) | Partially (Verified via TestClient; live browser fetch untested) | Tier 1 |
| 4. api_router -> poller | In-process (Python async coroutine call) | Yes (FR-SYS-01, NFR-PERF-01) | Partially (Direct fetch implemented; polling loop deferred) | Tier 2 |
| 5. poller -> vt_client | In-process (Python async function call) | Yes (FR-SYS-01, FR-API-02) | Yes (test_vt_client.py, test_vt_contracts.py) | Tier 2 |
| 6. vt_client -> VirusTotal v3 REST API | Network (External 3rd-party HTTPS REST API) | Yes (FR-2, FR-API-01, FR-API-02, NFR-1, NFR-SEC-01) | Yes (test_vt_contracts.py with mock transport and stubs) | Tier 1 |
| 7. poller -> evaluator | In-process (Python function call) | Yes (FR-4, FR-UI-01, FR-UI-02) | Yes (test_verdict_characterization.py) | Tier 2 |
| 8. Uptime Monitor -> health_check | Network (HTTPS GET /health) | Yes (NFR-REL-01) | Yes (test_health.py) | Tier 1 |

### Tier Ranking
* **Tier 1 (Boundary + Acceptance Path):** Seam 6 (vt_client -> VirusTotal API), Seam 3 (Web Client -> api_router), Seam 1 (User -> Web Client DOM), Seam 8 (Uptime Monitor -> health_check).
* **Tier 2 (In-Process Module Calls):** Seams 2, 4, 5, 7.

## Week 12 — Rep 2: One Integration Test per Tier 1 Seam

### Probing the Seven Seam Failure Modes
1. **Contract drift:** `test_seam_contract_drift_upstream_omits_stats` (verified safe fallback when upstream omits attributes).
2. **Unit mismatch:** `test_seam_unit_mismatch_latency_metric` (verified metric units).
3. **Time zone & encoding:** `test_seam_encoding_idn_and_query_parameters` (verified base64url URL-safe characters without padding).
4. **Identity:** `test_seam_identity_trailing_slash_normalization` (prevented split cache identities on root domain slashes).
5. **Ordering:** `test_seam_ordering_missing_config_fails_fast` (verified empty API key fails prior to network calls).
6. **Error semantics:** `test_seam_error_semantics_timeout_mapping` (verified upstream timeout maps to HTTP 504 rather than unhandled 500).
7. **Partial failure:** `test_seam_partial_failure_zero_disk_persistence` (asserted zero disk persistence invariant).

## Week 12 — Rep 3: Measure a Target, Do Not Feel It

### Performance Benchmark (NFR-PERF-01)
* **Target:** `POST /scan` response latency <= 500 ms p95 under realistic load.
* **Volume Pool:** Generated 500 enterprise URL records in `tests/fixtures/perf_seed_500.json` (seed 20261104).
* **Sample:** 50 sequential requests via `tools/measure_performance.py`.
* **Initial Run:** p50 = 727.60 ms, p95 = 1083.40 ms, Max = 2101.51 ms (Verdict: MISS).
* **Root Cause & Action:** Upstream HTTPS connection renegotiation per request pushed tail percentiles over 1.0 second. Implemented persistent connection pooling (`httpx.Limits`) and an ephemeral in-memory cache in `src/services/vt_client.py` and `src/api/main.py`.
* **Re-measured Run:** p50 = 83.80 ms, p95 = 184.22 ms, Max = 445.80 ms (Verdict: PASS).