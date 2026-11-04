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