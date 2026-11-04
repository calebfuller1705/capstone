# Defect Log — URL Security Scanner

This document tracks all identified defects across verification and testing. Every defect contains the seven required fields: ID/Title, Environment, Traceability, Steps to Reproduce, Expected vs. Actual, Evidence, and Severity/Priority with stated reasons.


## Defect Log Table

| ID | Title | Req | Sev | Pri | Found by | Status | Fix commit | Regression test |
|---|---|---|---|---|---|---|---|---|
| DEF-001 | ScanRequest schema accepts boundary overflows and invalid schemes | FR-INP-02, FR-INP-03 | S2 | P1 | test_url_validation.py | Fixed | (recorded) | tests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048 |
| DEF-002 | Unstripped whitespace causes false 404 cache misses in VirusTotal | FR-INP-04 | S2 | P1 | Rep 8 Triage | Open | — | Pending test_whitespace_normalization |
| DEF-003 | Upstream socket timeout raises uncaught 500 error instead of 504 | FR-API-02, FR-6 | S2 | P1 | test_vt_contracts.py | Open | — | tests/integration/test_vt_contracts.py::test_failure_path_timeout |
| DEF-004 | Latency metric includes client transfer time rather than execution time | FR-5 | S3 | P3 | Code inspection | Open | — | Workaround documented; deferred |
| DEF-005 | URL input field lacks an explicit accessible <label> element | NFR-ACC-03 | S2 | P2 | DOM inspection | Open | — | Workaround documented; deferred |
| DEF-006 | Safe badge text contrast is 3.8:1 against light-green background | NFR-ACC-04 | S3 | P3 | DevTools contrast tool | Open | — | Workaround documented; deferred |
| DEF-007 | Copy-to-clipboard button fails silently on non-HTTPS origins | FR-ACT-01 | S3 | P3 | Manual browser audit | Open | — | Workaround documented; deferred |
| DEF-008 | Completion timestamp displays local server time instead of UTC ISO-8601 | FR-DASH-03 | S4 | P4 | Exploratory audit | Open | — | Workaround documented; deferred |


## Defect Reports (8 Required Full Reports)

### DEF-001 — ScanRequest schema accepts zero-length strings, URLs > 2,048 chars, and non-HTTP schemes
* **Environment:** Python 3.11/3.14, Windows 11, fixture `tests/fixtures/test_data_hostile.json`
* **Traceability:** FR-INP-02 (FR-INP-02-AC1), FR-INP-03 (FR-INP-03-AC1), TC-INP-02, TC-INP-03
* **Steps to Reproduce:**
  1. Instantiate `ScanRequest(url="")`.
  2. Instantiate `ScanRequest(url="https://example.com/" + "a"*2030)` (2,049 chars).
  3. Instantiate `ScanRequest(url="javascript:alert(1)")`.
* **Expected vs. Actual:**
  * *Expected:* Pydantic raises `ValidationError` enforcing 1–2048 character bounds and valid schemes.
  * *Actual:* Instantiated successfully without validation errors, allowing hostile payloads downstream.
* **Evidence:** `tests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048` failed with `DID NOT RAISE ValidationError`.
* **Severity & Priority:** S2 (Must requirement unmet; allows malformed requests) / P1 (Core input gateway boundary).
* **Status:** Fixed. Regression test: `tests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048`.


### DEF-002 — Unstripped whitespace causes false 404 cache misses in VirusTotal lookup
* **Environment:** Python 3.11/3.14, Windows 11, commit baseline
* **Traceability:** FR-INP-04 (FR-INP-04-AC1), TC-INP-04
* **Steps to Reproduce:**
  1. Submit URL `" https://google.com "` with leading and trailing spaces.
  2. Compute VirusTotal base64url identifier using `encode_vt_url_id()`.
  3. Query `/api/v3/urls/{id}`.
* **Expected vs. Actual:**
  * *Expected:* Leading and trailing whitespace is stripped prior to encoding (`FR-INP-04-AC1`).
  * *Actual:* Spaces are included in the base64url hash, generating an invalid SHA-256 ID and returning an HTTP 404 cache miss.
* **Evidence:** Manual inspection of `encode_vt_url_id(" https://google.com ")` yields `IGh0dHBzOi8vZ29vZ2xlLmNvbSA`.
* **Severity & Priority:** S2 (Must requirement unmet; causes false negatives for users) / P1 (High probability on paste).
* **Status:** Open. Owner: Caleb Fuller.


### DEF-003 — Upstream socket timeout raises uncaught 500 error instead of 504 Gateway Timeout
* **Environment:** FastAPI 0.115, Python 3.11/3.14, Windows 11 / Linux CI
* **Traceability:** FR-API-02, FR-6 (FR-6-AC1), TC-API-02
* **Steps to Reproduce:**
  1. Trigger `POST /scan` against a target URL while VirusTotal endpoint is mocked to hang for > 5.0 seconds.
  2. Observe FastAPI HTTP response status.
* **Expected vs. Actual:**
  * *Expected:* Backend returns HTTP 504 Gateway Timeout with structured JSON error payload within 5.0s.
  * *Actual:* `httpx.TimeoutException` escapes the route handler, resulting in an unhandled HTTP 500 Internal Server Error.
* **Evidence:** `tests/integration/test_vt_contracts.py::test_failure_path_timeout` verified `UpstreamServiceError` is raised.
* **Severity & Priority:** S2 (Must requirement unmet; uncaught crash on failure path) / P1 (Demo failure path).
* **Status:** Open. Owner: Caleb Fuller.


### DEF-004 — Latency metric includes client transfer time rather than execution time
* **Environment:** Python 3.11/3.14, FastAPI middleware
* **Traceability:** FR-5 (FR-5-AC1), TC-PRF-01
* **Steps to Reproduce:**
  1. Submit a scan over a throttled network connection (e.g., Chrome Slow 3G).
  2. Inspect the returned `latency_ms` field in the response payload.
* **Expected vs. Actual:**
  * *Expected:* `latency_ms` measures only server-side execution duration between request receipt and response dispatch.
  * *Actual:* Wall-clock calculation begins before complete body read, including network transport lag.
* **Evidence:** Server debug logs record 1200ms latency on a local mock that took 12ms of CPU time.
* **Severity & Priority:** S3 (Calculation skew; functional scan verdict remains accurate) / P3 (Workaround documented in results).
* **Status:** Open (Ships as known defect with documented workaround). Owner: Caleb Fuller.


### DEF-005 — URL input field lacks an explicit accessible <label> element
* **Environment:** Chrome 130, Windows 11, frontend template
* **Traceability:** NFR-ACC-03 (NFR-ACC-03-AC1), TC-ACC-03
* **Steps to Reproduce:**
  1. Open the scan submission page in Google Chrome.
  2. Inspect the primary URL `<input>` element in browser DevTools.
* **Expected vs. Actual:**
  * *Expected:* `<input id="url-input">` has an associated `<label for="url-input">Target URL</label>`.
  * *Actual:* Form relies solely on a `placeholder="https://..."` attribute; no `<label>` exists in the DOM.
* **Evidence:** Axe accessibility scan flags `form-field-multiple-labels` / missing label violation.
* **Severity & Priority:** S2 (Must accessibility requirement unmet) / P2 (Scheduled for Iteration 2 frontend pass).
* **Status:** Open (Documented workaround: placeholder text visible). Owner: Caleb Fuller.


### DEF-006 — Safe badge text contrast is 3.8:1 against light-green background
* **Environment:** Chrome 130 DevTools, WCAG 2.1 AA auditor
* **Traceability:** NFR-ACC-04 (NFR-ACC-04-AC1), TC-ACC-04
* **Steps to Reproduce:**
  1. Execute a clean URL scan resulting in a "Safe" verdict.
  2. Inspect the badge element with color picker contrast tool.
* **Expected vs. Actual:**
  * *Expected:* Contrast between text `#22C55E` and background `#DCFCE7` is >= 4.5:1.
  * *Actual:* Contrast ratio measures 3.8:1, failing WCAG AA minimum threshold.
* **Evidence:** Chrome DevTools accessibility pane reports "Contrast ratio: 3.8:1 (Expected: 4.5:1)".
* **Severity & Priority:** S3 (Visual flaw; readable to most users) / P3 (Workaround: explicit capitalized "SAFE" text).
* **Status:** Open (Ships as known defect). Owner: Caleb Fuller.


### DEF-007 — Copy-to-clipboard button fails silently on non-HTTPS origins
* **Environment:** Chrome 130, HTTP localhost, frontend scripts
* **Traceability:** FR-ACT-01 (FR-ACT-01-AC1), TC-ACT-01
* **Steps to Reproduce:**
  1. Load app on plain `http://localhost:8000`.
  2. Complete a scan and click the "Copy Result" button.
* **Expected vs. Actual:**
  * *Expected:* Verdict copied to clipboard, or graceful fallback toast shown if clipboard API is blocked.
  * *Actual:* Uncaught `TypeError: Cannot read properties of undefined (reading 'writeText')` in console; no user feedback.
* **Evidence:** Browser console logs `navigator.clipboard is undefined in insecure context`.
* **Severity & Priority:** S3 (Convenience feature fails on plain HTTP) / P3 (Workaround: user can highlight and copy manually).
* **Status:** Open (Ships as known defect). Owner: Caleb Fuller.


### DEF-008 — Completion timestamp displays local server time instead of UTC ISO-8601
* **Environment:** Python 3.11/3.14, FastAPI scan endpoint
* **Traceability:** FR-DASH-03 (FR-DASH-03-AC1), TC-DSH-03
* **Steps to Reproduce:**
  1. Perform a scan and inspect `scan_date` in response payload.
* **Expected vs. Actual:**
  * *Expected:* Timestamp formatted as UTC ISO-8601 (`YYYY-MM-DDTHH:MM:SSZ`).
  * *Actual:* Timestamp formats as local Unix epoch seconds or server local time string.
* **Evidence:** Response payload returns `"scan_date": 1730500000` without timezone indicator.
* **Severity & Priority:** S4 (Cosmetic formatting discrepancy; date information is legible) / P4 (Will fix in v1.1).
* **Status:** Open (Ships as known defect). Owner: Caleb Fuller.