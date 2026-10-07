# Rep 2: Traceability Spot-Check

## Forward Traceability Matrix

| Req ID | Requirement Summary | Spec Section | Task / WP | Verification Method | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FR-SYS-01** | Submit URL to VirusTotal API | `docs/architecture.md` § 5.1 | T-1.1, T-2.2 | Integration test: HTTP POST returns base64 analysis ID | **Complete** |
| **FR-API-01** | Upstream Error Degradation (429/500) | `docs/architecture.md` § 5.3 | T-1.5, T-2.5 | Pytest mock simulating HTTP 429 returns clean error envelope | **Complete** |
| **FR-API-02** | 10-Second Polling Loop & Timeout | `docs/architecture.md` § 5.2 | T-1.3, T-2.4 | Automated test shows 504 status after 10.0 s queued state | **Complete** |
| **FR-INP-01** | Input Validation (Max 2048 Chars) | `docs/architecture.md` § 4.2 | T-2.3, T-5.2 | Unit test showing HTTP 422 on strings > 2048 chars | **Complete** |
| **FR-INP-03** | Intranet / Private IP Blocking (SSRF) | `docs/architecture.md` § 4.2 | T-2.3, T-5.2 | Pytest checking rejection of `127.0.0.1` and `10.0.0.0/8` | **Complete** |
| **FR-UI-01** | Display Safe/Unsafe Scan Verdict | `docs/architecture.md` § 6.1 | T-3.3, T-3.4 | Manual DOM inspection confirming dynamic text update | **Complete** |
| **NFR-PERF-01**| End-to-End Response Time p95 < 10.0s | `docs/architecture.md` § 5.2 | T-5.3 | 20 manual timed submissions logged in browser DevTools | **Complete** |
| **NFR-SEC-01** | Zero Plaintext Credentials in Repo | `docs/architecture.md` § 3.1 | T-4.3 | Local `git grep` check and browser network payload inspection | **Complete** |
| **NFR-SEC-02** | Zero Persistence / Stateless Server | `docs/architecture.md` § 2.2 | T-2.1 | Code audit confirming no database engine or disk writes | **Complete** |
| **NFR-USE-01** | First-Time User Flow < 30 Seconds | `docs/architecture.md` § 6.1 | Deferred | Timed stopwatch user sessions (Formal testing dropped) | **Partial** |

### Reverse Traceability (Gold Plating Audit)
* **Component Audited:** `GET /health/detailed-stats` (Internal diagnostics endpoint returning memory usage and worker thread count).
* **Trace Result:** Traces to zero requirements in `docs/requirements.md`. While convenient for debugging, this is unrequested functionality that adds maintenance overhead to the FastAPI router.
* **Disposition:** Flagged as Gold Plating. Stripped from the baseline scope to avoid burning 1.5 unbudgeted hours.

### Analysis of Gaps and Partials
The single non-complete item in the forward trace is `NFR-USE-01` (Usability Testing), which is marked **Partial** because its formal verification tasks were gotten rid of during Milestone 7 to balance the 57-hour build budget. What non-complete items have in common in this project is that they are on the human-process and UI-polish periphery. They do not challenge the core architectural path—submitting a URL, safely polling an asynchronous third-party API, handling rate limits, and displaying a verdict without crashing. Because the scanner's UI is a single input form with an accessible submit button, usability validation can be handled informally during end-to-end integration (T-5.3) rather than with separate stopwatch sessions.