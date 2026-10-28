# Iteration 1 Self-Review: `src/api/main.py`

* **File Under Review:** `src/api/main.py`
* **Review Date:** 2026-10-19
* **Target Requirement Baseline:** FR-1, FR-2, FR-4, FR-5

## The Four Passes

| Pass | Findings | Fixed / Logged / Accepted |
| :--- | :--- | :--- |
| **1 Diff (Mechanical)** | 1. Inline Pydantic schemas (`ScanRequest`, `ScanResponse`) mess up the route handler file instead of living in `src/api/schemas.py`.<br>2. Direct call to `os.getenv` puts environment parsing straight to route execution.<br>3. Hardcoded return values (`source="skeleton-stub"`, `scan_time_ms=15`). | **Logged:** Scheduled taking out of models to `src/api/schemas.py` during Slice 1 refactoring.<br>**Accepted with reason:** Stubbed return values remain until FR-2 and FR-4 land. |
| **2 Stranger (Comprehension)**| 1. `ScanRequest.url` is an untyped string with no docstrings or rules. Magic number `15` for `scan_time_ms` is not explained.<br>3. The HTTP 503 error message says the key is missing but gives no clue to check `.env.example`. | **Fixed:** Updated error detail to reference `.env.example`.<br>**Logged:** Documented `url` field specification in Issue #1 (`FR-1`). |
| **3 Adversary (Destruction)** | 1. **Malformed URL string:** Submitting empty string `""`, `javascript:alert(1)`, or a 5,000-character string passes through FastAPI with HTTP 200 because `url` is unconstrained `str`.<br>2. **SSRF / Loopback:** Submitting `http://127.0.0.1:8000` or private RFC 1918 subnets (`10.0.0.0/8`) is accepted.<br>3. **Key Whitespace:** If `VIRUSTOTAL_API_KEY="   "`, the truthy check passes but upstream calls will fail.<br>4. **Slow Upstream:** Route has no timeout handling, upstream hang locks the worker thread. | **Logged as defect DEF-001:** Unchecked `url` field accepted by `ScanRequest` (transferred to Issue #1 / `FR-1`).<br>**Logged as defect DEF-002:** Missing strip check on empty whitespace environment variable.<br>**Logged to Issue #7 / `NFR-1`:** Timeout enforcement on upstream client calls. |
| **4 Contract (Traceability)** | 1. `FR-1 AC-1` (reject non-http/https schemes): **No line of code satisfies this.**<br>2. `FR-5 AC-1` (compute end-to-end execution latency in milliseconds): **No line of code satisfies this** (returns static `15`).<br>3. `FR-2 AC-1` (unpadded base64 SHA-256 identifier): **No line of code satisfies this.** | **Logged:** Verified that all three gaps correspond exactly to open sprint backlog issues (#1, #4, and #2) and are not falsely claimed as complete. |

## Rep 6 — A prompt contract, not a wish

Wish prompt:      write a python function to get url scan results from virustotal
Contract prompt:  saved at prompts/2026-10-22-vt-lookup.txt
Assumptions the model listed that I had not stated: (1) Assumed response dictionary paths always nest under data.attributes.last_analysis_stats; (2) Assumed client lifecycle instantiates and closes a single-use httpx.AsyncClient when client is None; (3) Assumed custom exceptions inherit from base VTClientError; (4) Assumed transport errors (httpx.RequestError) map to UpstreamServiceError.

## Rep 7 — Explain it, break it, rewrite it

Target: `fetch_url_report` in `src/services/vt_client.py`

Lines I stalled on:        Managing `httpx.AsyncClient` lifecycle in the `finally:` block (ensuring `await client.aclose()` executes only when a local client was created), and syntax for chained exception causes (`raise UpstreamServiceError(...) from exc`).
What broke it:             1. Missing `.get()` guards on partial JSON payloads (a response without `attributes` raised `KeyError`); 2. Sending an empty string caused `encode_vt_url_id` to fail; 3. Simulated upstream 5-second socket hang caused unhandled `httpx.TimeoutException` until explicitly caught.
Could I rewrite it?        yes — and what I had to look up: the exact exception names in `httpx` (`httpx.TimeoutException` vs `httpx.RequestError`)[cite: 1].

## Rep 8 — Write both ai-usage entries

### Bad Entry (Rushed)
| 2026-10-22 | Gemini | virustotal api client | python code for virustotal | tweaked it | needed it to work |

### Proper Entry (Committed to docs/ai-usage.md)
| 2026-10-22 | Gemini | "Write an async function fetch_url_report(url, api_key, client) that calls VT v3 GET /urls/{id} with 5s timeout, 404 returning None, custom typed exceptions, and no disk writes." | An async client wrapper querying VirusTotal v3 with status code checks, timeout handling, and custom exception classes. | Replaced direct dict lookups with chained `.get()` accessors, added `should_close_client` logic to safely await `client.aclose()`, injected the client parameter for test mocking, and wrapped line lengths under 79 characters. | The assistant's raw draft would crash with a `KeyError` on partial JSON payloads and leak client sockets under high request volume; explicit mocking injection was needed to test hostile inputs under `pytest`. |

## Rep 9 — Rewrite Five Bad Commit Messages

| Actual message | What it should have said |
| :--- | :--- |
| `33be093 docs: complete week 4 block c reps, reformatted a few things, committed yesterday's work as well` | `docs(requirements): define NFR-1 latency and NFR-2 zero-persistence verification criteria`<br><br>Specify automated test bounds and measurement methods for 10s latency cap and memory-only execution to satisfy Milestone 4 audit gates.<br><br>Closes #4. Traces to NFR-1, NFR-2. |
| `252e7eb Wrote ADR 0001 for backend framework selection; will continue after my roommate reads ADR 0001` | `docs(adr): record ADR-0001 selecting FastAPI for URL scanner backend`<br><br>Document architecture trade-offs against Flask and Django, selecting FastAPI for native async I/O and Pydantic v2 schemas required by stateless scanning.<br><br>Closes #5. Traces to NFR-1. |
| `ef984c7 Finished traceability matrix, built my  DoD, and wrapped up Week 4` | `docs(governance): establish requirements traceability matrix and Definition of Done`<br><br>Map all functional requirements to verification tests and define a 10-point quality gate for iteration merges to prevent untested code entering main.<br><br>Closes #6. Traces to FR-1..FR-6. |
| `2728db8 Logged hours and locked in Reps 5-9 with API spike` | `feat(spike): validate VirusTotal v3 API endpoint latency and base64url encoding`<br><br>Verify that the unpadded base64url URL identifier format works against VirusTotal /api/v3/urls/{id} and establish the 5.0-second timeout baseline.<br><br>Closes #2. Traces to FR-2, NFR-1. |
| `8558d66 Started MS6 with Reps 1-4 and the diagrams` | `docs(arch): add C4 Context and Container diagrams for scanner system`<br><br>Model structural boundaries between browser client, FastAPI service, and VirusTotal v3 upstream API to establish architectural baseline v0.1.<br><br>Closes #3. Traces to FR-2, FR-5. |

## Rep 10 — Reconstruct one honest day, then run the report

### 1. Reconstructed Session
* **Target Date:** 2026-10-17 (Milestone 9 completion)
* **Evidence:** Commits `b5a188e` (14:14) and `8de6673` (14:16) shipping walking skeleton traceability and updating project status.
* **Row Added to `docs/hours-log.csv`:**
  `2026-10-17,13:45,14:30,0.75,construction,developer,[reconstructed from commits] Ship Milestone 9 walking skeleton and traceability,0.75,0.00,Reconstructed from commits b5a188e and 8de6673: verified walking skeleton traceability matrix and updated project status,yes`

### 2. Report Findings & Metrics Summary
* **Total Logged:** 133.00 hours across 53 sessions in 9 calendar weeks (55.4% of 240h target budget).
* **Remaining Budget:** 107.00 hours.
* **Calibration (Estimate-to-Actual Ratio):** 1.07 (estimated 124.75h vs. actual 133.00h, showing an honest 6.6% underestimation bias).

#### Top Phase Distribution
* **Requirements:** 34.00 h (25.6%)
* **Inception:** 22.00 h (16.5%)
* **Construction:** 18.50 h (13.9%)
* **Architecture:** 15.50 h (11.7%)
* **Design:** 15.25 h (11.5%)
* **Review:** 15.00 h (11.3%)
* **Planning:** 12.75 h (9.6%)

## Rep 11 — Secret hunting and process fix

### Audit Results
* **History Pattern Search:** `git log --all --oneline -- '*.env' '*.env.*' '*credentials*' '*secrets*'` matched commits `7673bc2` and `6b1e6ab`. Inspection via `git show --name-only` confirmed the committed files were `.env.example` and `docs/.env.example` (sanitized templates containing placeholder variable names only).
* **Working Tree & History Grep:** All literal matches for `api_key` in the codebase and git history belong to test mocks in `tests/unit/test_vt_client.py` using dummy values (`"dummy-key-12345"`). No real secrets exist in repository history.

### Rep 11 Form
Credentials my project uses:  `VIRUSTOTAL_API_KEY`
Read from:                    env var (`os.getenv("VIRUSTOTAL_API_KEY")` in `src/services/vt_client.py`)
In history?                   no (confirmed `.env.example` and `docs/.env.example` were templates only; test fixtures use `"dummy-key-12345"`)
Ignore file covers:           `.env`, `.env.*` (with `!.env.example` allowlisted) in `.gitignore`

## Rep 12 — The five-minute demo, rehearsed and recorded

Act 1 opening line (write it verbatim): "This system is a stateless, zero-persistence URL scanner designed to provide immediate threat intelligence without logging query history or writing user data to disk."
Act 2 script steps: 1. curl -s http://127.0.0.1:8000/health 2. python -c "from src.services.vt_client import encode_vt_url_id; print(encode_vt_url_id('https://example.com'))" 3. pytest tests/unit/test_vt_client.py -k "test_fetch_url_report_success" -v 4. pytest tests/unit/test_vt_client.py -k "test_fetch_url_report_404" -v
Act 2 failure path shown: Upstream 5.0-second socket timeout via pytest tests/unit/test_vt_client.py -k "timeout" raising typed UpstreamServiceError without leaking TCP connections.
Act 3 what is NOT done, and when it is scheduled: Browser HTML submission form (FR-1) and background rescan worker queue (FR-4); scheduled for Iteration 2 (Weeks 11–12).
Recorded fallback saved at: docs/demo/iteration-1-demo.mp4