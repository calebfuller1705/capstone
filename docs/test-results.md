# Test Results & Verification Metrics — Milestone 11 Rehearsal

**Date:** 2026-11-03  
**Commit SHA:** 31f7332  
**Execution Environment:** Clean clone (\capstone-rehearsal\), Python 3.14 / 3.11, Windows 11  
**Command:** \pytest -v\  

## 1. Test Suite Execution Summary (Step 3)

| Metric | Measured Value |
|---|---|
| **Total Tests** | 28 passed |
| **Failures / Errors** | 0 |
| **Duration** | 2.39s |
| **Suite Status** | **100% Green** |


## 2. Verified Requirement Coverage Output (Step 4)

\\\	ext
Traceability matrix: docs/traceability-matrix.csv
Requirements:        30
Verified:            8  (27%)
Must requirements:   23
Verified Musts:      8  (35%)

TEST EXISTS BUT NEVER RUN (this is not coverage):
  FR-ACT-01    Could   FR-ACT-01-AC1
  FR-DASH-01   Must    FR-DASH-01-AC1
  FR-DASH-02   Should  FR-DASH-02-AC1
  FR-DASH-03   Should  FR-DASH-03-AC1
  FR-EVAL-01   Must    FR-EVAL-01-AC1
  FR-EVAL-02   Should  FR-EVAL-02-AC1
  FR-EVAL-03   Could   FR-EVAL-03-AC1
  FR-EVAL-04   Must    FR-EVAL-04-AC1
  FR-INP-01    Must    FR-INP-01-AC1
  FR-INP-04    Must    FR-INP-04-AC1
  FR-SYS-02    Should  FR-SYS-02-AC1
  FR-UI-01     Must    FR-UI-01-AC1
  FR-UI-02     Must    FR-UI-02-AC1
  NFR-ACC-01   Must    NFR-ACC-01-AC1
  NFR-ACC-02   Must    NFR-ACC-02-AC1
  NFR-ACC-03   Must    NFR-ACC-03-AC1
  NFR-ACC-04   Must    NFR-ACC-04-AC1
  NFR-ACC-05   Must    NFR-ACC-05-AC1
  NFR-PERF-01  Must    NFR-PERF-01-AC1
  NFR-PRI-01   Must    NFR-PRI-01-AC1
  NFR-REL-01   Must    NFR-REL-01-AC1
  NFR-USE-01   Should  NFR-USE-01-AC1

UNVERIFIED MUST REQUIREMENTS -- exit criteria not met:
  FR-DASH-01
  FR-EVAL-01
  FR-EVAL-04
  FR-INP-01
  FR-INP-04
  FR-UI-01
  FR-UI-02
  NFR-ACC-01
  NFR-ACC-02
  NFR-ACC-03
  NFR-ACC-04
  NFR-ACC-05
  NFR-PERF-01
  NFR-PRI-01
  NFR-REL-01
\\\

## 3. Exit Criteria Audit & \"Ships with Known Defects\" (Steps 5 & 6)

### Audit of Exit Criteria
- [ ] **100% of Must requirements verified:** **NOT MET (35% verified).** 8 of 23 Musts verified. The remaining 15 Must criteria depend on frontend web UI components and browser accessibility wiring scheduled for Iteration 2.
- [x] **0 open defects at severity S1:** **MET.** Zero data corruption, zero leaked credentials, and zero fatal crashes.
- [ ] **0 open defects at severity S2:** **NOT MET.** 3 open S2 defects discovered during Rep 12 unscripted testing (documented below).
- [x] **Every open S3/S4 defect appears in defect log with workaround:** **MET.** Tracked in \docs/defect-log.md\.
- [x] **Every defect fixed this iteration has a named regression test:** **MET.** \DEF-001\ verified by \	ests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048\ (proven failing on pre-fix code).
- [x] **Full suite runs from one documented command:** **MET.** \pytest -v\ runs offline with zero API quota consumption.
- [x] **Latency constraints:** **MET.** 5.0-second fail-fast timeout verified on upstream hangs.

### Ships with Known Defects Entry

| Defect / Scope Item | Severity / Priority | Operational Workaround & Disposition |
|---|---|---|
| **15 Unverified Must Requirements** (\FR-INP-01\, \FR-UI-01..02\, \NFR-ACC-01..05\, etc.) | S2 / P2 | **Context:** These govern interactive DOM events, WCAG contrast, and screen reader announcements.<br>**Workaround:** Core backend endpoints (\POST /scan\, \GET /health\) are verified; full browser wiring is slated for Iteration 2. |
| **DEF-011: Submit button lacks debounce** | S2 / P2 | **Context:** Rapid multi-clicks submit concurrent requests.<br>**Workaround:** Acceptable for single-operator test runs; button disablement state scheduled for Iteration 2 Slice 2. |
| **DEF-014: Raw 422 error object in banner** | S2 / P2 | **Context:** Pydantic 422 JSON validation payload displays as \[object Object]\ in frontend banner.<br>**Workaround:** Status code is correct (HTTP 422); JSON error structure readable in browser DevTools. |
| **DEF-015: Missing focus ring on copy button** | S2 / P2 | **Context:** Custom button lacks \:focus-visible\ styling.<br>**Workaround:** Usable via keyboard (\Tab\ + \Enter\); explicit outline CSS queued for accessibility pass. |