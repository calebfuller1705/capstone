# Test Results & Verification Metrics

**Date:** 2026-10-29  
**Baseline Commit:** $sha  
**Checker Command:** `python tools/coverage_report.py docs/traceability.csv`  

## 1. Verified Requirement Coverage (Baseline)

| Metric | Measured Value | Exit Criteria Target | Status |
|---|---|---|---|
| **Total Requirements** | **30** | 30 | Baseline established |
| **Verified Requirements** | **6** (20%) | 30 (100%) | In Progress |
| **Must Requirements** | **23** | 23 | Baseline established |
| **Verified Must Requirements** | **6** (26%) | 23 (100%) | In Progress |


## 2. The Three Bad Buckets (Rep 5 Audit)

### Bucket 1: No Test Case at All (Unverified Promises)
* **Count:** 0. Every requirement has an assigned test case ID.

### Bucket 2: Tested and Failing (Active Defects)
* **Count:** 2 criteria
  * `FR-INP-02-AC1` (`TC-INP-02`): Empty URL input accepted by schema.
  * `FR-INP-03-AC1` (`TC-INP-03`): URL exceeding 2,048 characters accepted by schema.
* **Resolution:** Logged under `DEF-001` in `docs/defect-log.md`.

### Bucket 3: Test Exists, Never Run (Intentions, Not Coverage)
* **Count:** 22 criteria (17 Must, 3 Should, 2 Could).
* **Scope:** UI display elements (`FR-UI-01`, `FR-UI-02`), client input flow (`FR-INP-01`), accessibility contracts (`NFR-ACC-01` through `05`), and performance benchmarks (`NFR-PERF-01`).