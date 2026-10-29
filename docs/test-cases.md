## Initial Acceptance Test Cases (Rep 2)

### TC-001 — Unpadded Base64url Encoding
* **Verifies:** `FR-2-AC1` | **Level:** Unit | **Data:** `docs/demo-seed.json` (`benign-sample`)
* **Preconditions:** `src.services.vt_client.encode_vt_url_id` imported; no network I/O or API credentials required.
* **Steps:**
  1. Call `encode_vt_url_id("https://example.com")`.
  2. Inspect the returned string value.
  3. Verify character set and suffix termination.
* **Expected:** Returns string `"aHR0cHM6Ly9leGFtcGxlLmNvbQ"` with zero trailing `=` padding characters.
* **Fails if:** Output retains trailing `=` characters (e.g. `"aHR0cHM6Ly9leGFtcGxlLmNvbQ=="`), causing upstream VirusTotal v3 endpoint lookups to fail with HTTP 400 Bad Request.

### TC-002 — Upstream HTTP 429 Rate-Limit Propagation
* **Verifies:** `FR-6-AC2` | **Level:** Integration | **Data:** Mocked HTTP 429 response with `Retry-After: 60`
* **Preconditions:** FastAPI TestClient or async httpx transport wired with mock transport returning HTTP 429 Too Many Requests on upstream calls.
* **Steps:**
  1. Dispatch `POST /scan` with payload `{"url": "https://example.com"}`.
  2. Upstream client catches HTTP 429 from VirusTotal stub.
  3. Inspect FastAPI HTTP response status code, headers, and JSON body.
* **Expected:** HTTP status 429 Too Many Requests; header `Retry-After` is preserved as `60`; response body is `{"detail": "Upstream rate limit exceeded; retry after 60s"}`.
* **Fails if:** Unhandled `UpstreamRateLimitError` crashes the route handler into an unhandled HTTP 500 Internal Server Error, or swallowing the exception returns HTTP 200 with empty scan stats.

### TC-003 — Asynchronous Scan Submission on Cache Miss
* **Verifies:** `FR-3-AC1` | **Level:** Acceptance | **Data:** `docs/demo-seed.json` (`unseen-sample`)
* **Preconditions:** VirusTotal report endpoint returns HTTP 404 cache miss; mock VT `/api/v3/urls` submission endpoint configured to return HTTP 200 `{"data": {"id": "u-scan-job-98765", "type": "analysis"}}`.
* **Steps:**
  1. Submit `POST /scan` with payload `{"url": "https://nonexistent-random-domain-2026-test.org/check"}`.
  2. Service attempts report lookup, receives 404 (`None`), and immediately dispatches POST submission to upstream `/urls`.
  3. Inspect final response status and JSON payload.
* **Expected:** HTTP status 202 Accepted with response `{"status": "queued", "analysis_id": "u-scan-job-98765", "target_url": "https://nonexistent-random-domain-2026-test.org/check"}`.
* **Fails if:** Route fails with HTTP 404 Not Found, crashes on missing dictionary keys, or hangs indefinitely attempting to synchronously poll the scan until completion (violating NFR-1's 5.0-second fail-fast budget).

### Boundary Partition Table
| Partition | Representative | Boundary values worth a test |
|---|---|---|
| Below the range (< 1 char) | `""` (0 characters) | Empty string `""` (length 0) |
| Inside the range (1 to 2,048 chars) | `"https://example.com/check"` (25 chars) | `"h"` (length 1), URL of 2,048 characters |
| Above the range (> 2,048 chars) | 3,000 characters | 2,049 characters, hostile 10,000 characters |
| Absent / null | `None` | `None`, missing key `{}` |

