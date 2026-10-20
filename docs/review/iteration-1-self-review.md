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