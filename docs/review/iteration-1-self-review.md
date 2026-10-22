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