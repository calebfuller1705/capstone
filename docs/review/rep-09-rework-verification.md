# Rep 9: Defect Rework Verification Report

**Verification Date:** 2026-10-14  
**Verifier:** Caleb Fuller (Acting Configuration Moderator)  
**Target Document:** `docs/architecture.md` (Updated to v0.2) and `docs/plan.md`  

---

## 1. Rework Verification Matrix

| Defect ID | Original Finding Text | Location in `docs/architecture.md` | Verification Evidence | Status |
| :--- | :--- | :--- | :--- | :---: |
| **DR-001** | Section has POST /api/v1/scan accepts URL string but does not say whether URL must be base64-encoded before submitting to VirusTotal /urls endpoint | `docs/architecture.md` § 5.1 & § 7.1 | Added explicit RFC 4648 unpadded URL-safe base64 encoding algorithm (`base64.urlsafe_b64encode().strip("=")`) to upstream ID spec and Flow 1 step 3. | **Verified** |
| **DR-002** | Error envelope gives generic 500 status code but does not specify upstream 429 response body structure or Retry-After header propagation | `docs/architecture.md` § 5.1 & § 8 | Documented RFC 7807 error envelope with explicit `retry_after` integer field and upstream header propagation in Section 5 status-code policy. | **Verified** |
| **DR-003** | Input validation schema gives max length 2048 chars but does not say whether leading or trailing whitespace is taken out before regex validation | `docs/architecture.md` § 5.1 & § 8 (Edge Case 3) | Added explicit rule under Request contract: leading and trailing whitespace is stripped before length check and regex matching. | **Verified** |
| **DR-004** | Sequence diagram shows polling stopping at 10.0s, but does not give exact HTTP status sent back to client when polling runs out while still 'queued' | `docs/architecture.md` § 5.1 & § 7.2 | Standardized on HTTP 504 Gateway Timeout across Section 5 error policy and Section 7 Flow 3 failure table. | **Verified** |
| **DR-005** | CORS configuration has wildcard '*' for local development without defining origin lockdown for the Render static site domain | `docs/architecture.md` § 3 | Added Container Configuration Policies explicitly restricting production CORS to `FRONTEND_URL` environment variable. | **Verified** |
| **DR-006** | UI state section talks about a loading spinner, but doesn't have a maximum client-side timeout abort threshold if backend drops connection without giving an error envelope | `docs/architecture.md` § 8 (Edge Case 2) | Updated Edge Case 2 to define an explicit 12.0s `AbortController` timeout on client `fetch` calls. | **Verified** |
| **DR-007** | Auditor Area 2 check flagged that HTTP 422 Unprocessable Entity and HTTP 429 schemas are not documented in the interface contract | `docs/architecture.md` § 5.1 | Added detailed JSON schemas for 422 (intranet/unsupported scheme) and 429 (rate-limited) in Section 5 status-code policy. | **Verified** |
| **DR-008** | Auditor Area 6 check says that Week 12 deployment gate relies on manual inspection instead of an automated verification script | `docs/plan.md` § Schedule Gate Week 12 | Updated Week 12 gate criteria in `docs/plan.md` to require an automated `curl -I https://scanner.onrender.com/health` smoke test returning HTTP 200. | **Verified** |
| **DR-009** | Frontend has no rate-limiting or CAPTCHA; an attacker or bot can script requests against POST /api/v1/scan and use the 4 req/min VirusTotal API tier right away for all users | `docs/architecture.md` § 4 & § 5.1 | Added `slowapi` in-memory rate limiting (2 requests/minute per client IP) to `api_router` and `POST /scan` contract. | **Verified** |
| **DR-011** | If a scan gives an HTTP 504 Gateway Timeout, the UI leaves the user stuck with no 'Retry' button, forcing a hard page refresh which clears form state | `docs/architecture.md` § 7.2 & § 8 (Edge Case 11) | Added active `[Retry Scan]` button requirement to Flow 3 step 6b and Edge Case 11 to preserve form state on timeouts. | **Verified** |
| **DR-012** | Section 5.3 does not talk about backend behavior if VirusTotal comes back with an unexpected HTTP 403 Forbidden | `docs/architecture.md` § 5.1 & § 8 | Mapped upstream 401/403 to sanitized HTTP 502 Bad Gateway (`upstream_error`) with critical server alert logging. | **Verified** |
| **DR-013** | Input validation regex checks domain format but does not restrict URL schemes, allowing dangerous or unsupported protocols through to the scanner | `docs/architecture.md` § 5.1 | Restricted allowed schemes to strictly `http://` and `https://` under Section 5 Request rules. | **Verified** |
| **DR-014** | FastAPI background polling loop does not have handling for client disconnect; if a user navigates away, the server continues polling VT for 10s, burning rate limit quota | `docs/architecture.md` § 4 & § 7.2 | Added `request.is_disconnected()` check to `poller` component and Flow 3 failure table (Step 5b). | **Verified** |
| **DR-018** | UI specification does not mandate explicit 'for' and 'id' pairing between the form label and the URL input element | `docs/architecture.md` § 3 & `docs/requirements.md` § 6.5 | Mandated `<label for="url-input">` and `<input id="url-input">` matching in Container Configuration Policies. | **Verified** |
| **DR-019** | Trailing slash normalization creates mismatched base64 identifiers for VirusTotal cache lookups | `docs/architecture.md` § 5.1 | Added explicit canonicalization rule: strip trailing slashes from domain roots prior to base64 encoding. | **Verified** |

---

## 2. The Finding Whose Fix Created a Second Finding

**Original Finding:** `DR-013` (Input validation regex checks domain format but does not restrict URL schemes).  
**Secondary Finding:** `DR-019` (Trailing slash normalization creates mismatched base64 identifiers).

### How It Happened
While writing the protocol scheme rules for `DR-013` in Section 5 (`POST /scan`), testing the URL canonicalization showed me that standard Python URL parsing libraries (such as `urllib.parse`) automatically normalize bare domain names by adding a trailing root slash (e.g., `https://example.com` becomes `https://example.com/`).

Under `DR-001`, VirusTotal v3 resource identifiers are generated by base64-encoding the URL string:
* `base64("https://example.com")` $\rightarrow$ `aHR0cHM6Ly9leGFtcGxlLmNvbQ`
* `base64("https://example.com/")` $\rightarrow$ `aHR0cHM6Ly9leGFtcGxlLmNvbS8`

If a user submits `https://example.com` without a slash, but the backend normalizer adds a trailing slash prior to encoding, the resulting base64 token will not match VirusTotal's indexed identifier, resulting in a false cache miss.

### Resolution
Logged as `DR-019` and resolved by putting in an explicit rule to Section 5.1: trailing slashes are stripped from domain root URLs prior to base64 encoding.