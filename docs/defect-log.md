# Defect Log — URL Security Scanner

This document tracks all identified defects across verification and testing. Every defect contains the seven required fields: ID/Title, Environment, Traceability, Steps to Reproduce, Expected vs. Actual, Evidence, and Severity/Priority with stated reasons.

---

## Defect Log Table

| ID | Title | Req | Sev | Pri | Found by | Status | Fix commit | Regression test |
|---|---|---|---|---|---|---|---|---|
| DEF-001 | ScanRequest schema accepts boundary overflows and invalid schemes | FR-INP-02, FR-INP-03 | S2 | P1 | test_url_validation.py | Open | — | tests/unit/test_url_validation.py |

---

## Defect Reports

### DEF-001 — ScanRequest schema accepts zero-length strings, URLs > 2,048 chars, and non-HTTP schemes
* **Reported:** 2026-10-31 by Caleb Fuller
* **Environment:** commit baseline, Windows 11 / Linux CI, Python 3.11, Pydantic v2.6, fixture `tests/fixtures/test_data_hostile.json`
* **Requirement:** FR-INP-02 (FR-INP-02-AC1), FR-INP-03 (FR-INP-03-AC1), FR-EVAL-04 (FR-EVAL-04-AC1)
* **Test cases:** TC-INP-02, TC-INP-03, `tests/unit/test_hostile_data.py`

**Steps to reproduce:**
1. Initialize `ScanRequest(url="")`.
2. Initialize `ScanRequest(url="https://example.com/" + "a"*2030)` (length 2,049 chars).
3. Initialize `ScanRequest(url="javascript:alert('xss')")` or `ScanRequest(url="file:///etc/passwd")`.

**Expected vs. Actual:**
* **Expected:** Pydantic raises `pydantic.ValidationError` for all three inputs, enforcing `min_length=1`, `max_length=2048`, and scheme restricted to `http://` or `https://`.
* **Actual:** `ScanRequest` instantiates successfully for all three inputs without validation errors, allowing invalid inputs downstream to the VirusTotal client.

**Evidence:**
* `tests/unit/test_url_validation.py::test_url_boundary_above_maximum_2049` fails with `Failed: DID NOT RAISE ValidationError`.
* `tests/unit/test_hostile_data.py::test_hostile_input_handling[HOSTILE-007]` fails with `Failed: DID NOT RAISE ValidationError`.

**Severity & Priority:**
* **Severity: S2 (Major)** — Must requirements FR-INP-02 and FR-INP-03 are not met; invalid inputs go through the schema layer.
* **Priority: P1 (Fix Now)** — Core input path; input validation at the gateway boundary must be enforced before route wiring.

**Status & Resolution:**
* **Status:** Open
* **Owner:** Caleb Fuller
* **Regression Test:** `tests/unit/test_url_validation.py`, `tests/unit/test_hostile_data.py`