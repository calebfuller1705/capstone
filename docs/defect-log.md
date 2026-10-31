# Defect Log — URL Security Scanner

This document tracks all identified defects across verification and testing. Every defect contains the seven required fields: ID/Title, Environment, Traceability, Steps to Reproduce, Expected vs. Actual, Evidence, and Severity/Priority with stated reasons.

---

## Defect Log Table

| ID | Title | Req | Sev | Pri | Found by | Status | Fix commit | Regression test |
|---|---|---|---|---|---|---|---|---|
| DEF-001 | ScanRequest schema accepts boundary overflows and invalid schemes | FR-INP-02, FR-INP-03 | S2 | P1 | test_url_validation.py | Fixed | (pending) | tests/unit/test_url_validation.py, tests/unit/test_hostile_data.py |

---

## Closed Defect Reports

### DEF-001 — ScanRequest schema accepts zero-length strings, URLs > 2,048 chars, and non-HTTP schemes
* **Reported:** 2026-10-31 by Caleb Fuller
* **Environment:** Windows 11 / Linux CI, Python 3.11, Pydantic v2.6, fixture `tests/fixtures/test_data_hostile.json`
* **Requirement:** FR-INP-02 (FR-INP-02-AC1), FR-INP-03 (FR-INP-03-AC1), FR-EVAL-04 (FR-EVAL-04-AC1)
* **Test cases:** TC-INP-02, TC-INP-03, `tests/unit/test_hostile_data.py`

**Steps to reproduce:**
1. Initialize `ScanRequest(url="")`.
2. Initialize `ScanRequest(url="https://example.com/" + "a"*2030)` (length 2,049 chars).
3. Initialize `ScanRequest(url="javascript:alert('xss')")` or `ScanRequest(url="file:///etc/passwd")`.

**Expected vs. Actual:**
* **Expected:** Pydantic raises `pydantic.ValidationError` for all three inputs, enforcing `min_length=1`, `max_length=2048`, and scheme restricted from dangerous protocols.
* **Actual:** `ScanRequest` instantiated without validation errors, passing malformed inputs downstream.

**Evidence:**
* `tests/unit/test_url_validation.py::test_url_boundary_above_maximum_2049` failed with `Failed: DID NOT RAISE ValidationError`.
* `tests/unit/test_hostile_data.py::test_hostile_input_handling[HOSTILE-007]` failed with `Failed: DID NOT RAISE ValidationError`.

**Severity & Priority:**
* **Severity: S2** — Must requirements FR-INP-02 and FR-INP-03 were unmet.
* **Priority: P1** — Core input path required schema hardening before route integration.

**Status & Resolution:**
* **Status:** Fixed
* **Resolution:** Added `Field(min_length=1, max_length=2048)` and `@field_validator("url")` with whitespace trimming and disallowed scheme filtering (`javascript:`, `file:`, etc.) in `src/api/schemas.py`.
* **Owner:** Caleb Fuller
* **Regression Test:** `tests/unit/test_url_validation.py`, `tests/unit/test_hostile_data.py`


## Rep 8 - Triage Ten Defects


# Defect Triage Table
| ID | Title | Sev | Pri | Estimate | Justification |
|---|---|---|---|---|---|
| DEF-001 | ScanRequest accepts empty strings, length > 2048, and non-HTTP schemes | S2 | P1 | 1.0 h | Must requirement unmet; crashes upstream lookup |
| DEF-002 | Unstripped whitespace causes false 404 cache misses in VirusTotal | S2 | P1 | 0.5 h | Must requirement unmet; spaces corrupt base64url hash |
| DEF-003 | Upstream timeout raises uncaught 500 error instead of 504 Gateway Timeout | S2 | P1 | 1.5 h | Must requirement unmet; demo failure path |
| DEF-005 | URL input field lacks explicit accessible <label> element | S2 | P2 | 0.5 h | Must requirement unmet; screen readers fail context |
| DEF-009 | Deep subdomain chains cause 3+ second validation lag | S2 | P2 | 2.0 h | Critical performance bug approaching ReDoS |
| DEF-006 | "Safe" badge green text contrast is 3.8:1 (WCAG < 4.5:1) | S3 | P3 | 0.75 h | Accessibility gap; readable text icon workaround |
| DEF-007 | Copy button fails silently on non-HTTPS origins | S3 | P3 | 1.0 h | Secondary convenience feature; manual copy works |
| DEF-004 | Latency metric includes client transfer time | S3 | P3 | 1.0 h | Calculation skew; metric still renders |
| DEF-008 | Completion timestamp displays local time instead of UTC | S4 | P4 | 0.5 h | Minor formatting bug; time is still legible |
| DEF-010 | Footer copyright year hardcoded | S4 | P4 | 0.25 h | Cosmetic branding text; zero functional harm |

### Triage Decision (6-Hour Budget)
* **Fix Order (5.5 hours):** DEF-002 (0.5h) -> DEF-001 (1.0h) -> DEF-005 (0.5h) -> DEF-003 (1.5h) -> DEF-009 (2.0h)
* **Ships With Known Defects:** DEF-004, DEF-006, DEF-007, DEF-008, DEF-010