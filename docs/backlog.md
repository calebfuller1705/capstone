# Product & Engineering Backlog — Phishing URL Scanner

Top five groomed open issues prioritized for post-`v1.0.0` maintenance and successor onboarding. Issue #1 (`ISSUE-DOC-04`) is labeled **`good-first-issue`** and assigned as the successor's Week 1 starter task in `docs/handoff.md` §2.

---

## 1. `ISSUE-DOC-04` — Return `204 No Content` for `GET /favicon.ico` to Eliminate Uvicorn `404` Log Noise [`good-first-issue`]
- **Requirement / Defect ID:** `ISSUE-DOC-04` (observed during Rep 12 clean-room browser verification)
- **Severity / Priority:** Low (Week 1 Starter Issue — `good-first-issue`)
- **Estimated Effort:** 1.0 h
- **Files Most Likely Involved:** `src/api/main.py`, `tests/unit/test_health.py`
- **Acceptance Criteria:**
  - Given the FastAPI server is running, when a browser requests `GET /favicon.ico`, then the endpoint returns HTTP `204 No Content` with an empty response body instead of logging `404 Not Found`.
  - Given `pytest tests/ -v` and `flake8 src/ tests/` are executed, when the new unit test for `GET /favicon.ico` runs, then all tests and lint checks pass with exit code `0`.

---

## 2. `B-01` — Recursive Redirect Unshortening for Shortened URLs (`FR-EVAL-03` / `KI-001`)
- **Requirement / Defect ID:** `FR-EVAL-03` / `KI-001` (Deferred via `CR-003` to `v1.1`)
- **Severity / Priority:** Medium
- **Estimated Effort:** 4.0 h
- **Files Most Likely Involved:** `src/services/vt_client.py`, `src/api/main.py`, `src/api/schemas.py`, `tests/security/test_security_review.py`
- **Acceptance Criteria:**
  - Given a shortened URL (e.g., `https://bit.ly/...` or `https://tinyurl.com/...`), when submitted to `POST /scan`, then the service resolves up to 3 HTTP `301`/`302` redirects using `HEAD` requests within a `2.0s` sub-budget before querying VirusTotal v3.
  - Given any intermediate or final redirect hop resolves to a loopback, RFC-1918 private, or link-local IP address, when redirect expansion runs, then the SSRF guard (`is_private_or_intranet_url`) immediately aborts and returns HTTP `422 Unprocessable Entity` (`FR-EVAL-01`).

---

## 3. `B-04` — Optional Opt-In Server-Side Action Audit Logging (`FR-SYS-02`)
- **Requirement / Defect ID:** `FR-SYS-02` (Deferred via `CR-005` to `v1.1`)
- **Severity / Priority:** Low
- **Estimated Effort:** 5.0 h
- **Files Most Likely Involved:** `src/api/main.py`, `.env.example`, `tools/check_config.py`, `tests/integration/test_tier1_seams.py`
- **Acceptance Criteria:**
  - Given `ENABLE_AUDIT_LOG=false` (the default), when `POST /scan` executes, then zero bytes are written to disk (`CON-04` and `NFR-SEC-02` remain satisfied).
  - Given `ENABLE_AUDIT_LOG=true` is explicitly configured by an operator, when a scan completes or fails with an upstream error, then the server appends a single timestamped line containing the hostname (never full query/path secrets) and HTTP status/verdict to a rotating log file.

---

## 4. `B-05` — Upgrade `Starlette` / `FastAPI` Constants to Clear `HTTP_422_UNPROCESSABLE_CONTENT` Deprecation Warnings
- **Requirement / Defect ID:** `B-05` (`NFR-MNT-01` Dependency Hygiene)
- **Severity / Priority:** Medium
- **Estimated Effort:** 1.5 h
- **Files Most Likely Involved:** `src/api/main.py`, `requirements.txt`, `requirements.lock`, `tests/acceptance/test_acceptance_paths.py`
- **Acceptance Criteria:**
  - Given `src/api/main.py` raises HTTP `422` validation errors, when `status.HTTP_422_UNPROCESSABLE_CONTENT` is used and `requirements.lock` is refreshed, then `.\.venv\Scripts\python.exe -m pytest tests/ -v` completes with `0` Starlette deprecation warnings.
  - Given a clean virtual environment is built from the updated `requirements.lock`, when `./script/test` and `./script/smoke` run, then all 71+ tests pass cleanly.

---

## 5. `B-06` — Bounded LRU Eviction for the In-Memory VirusTotal Verdict Cache (`NFR-PERF-02`)
- **Requirement / Defect ID:** `B-06` (`NFR-PERF-02` Memory Stability)
- **Severity / Priority:** Medium
- **Estimated Effort:** 2.0 h
- **Files Most Likely Involved:** `src/services/vt_client.py`, `tests/unit/test_vt_client.py`
- **Acceptance Criteria:**
  - Given the in-memory URL verdict cache reaches its maximum capacity (`MAX_CACHE_ENTRIES = 1024`), when a new URL report is cached, then the oldest entry is evicted so process memory remains bounded during long-lived runs.
  - Given a cached entry is older than `300` seconds, when the same URL is requested again, then the stale entry is evicted and refreshed from VirusTotal v3.