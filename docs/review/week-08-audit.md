# Rep 12: Week 8 Halfway Pace Audit

**Date:** 2026-10-14  
**Logged Through Week 8:** 52.25 hours  
**Course Total Budget:** 240.0 hours (120.0 h expected at Week 8 mark)  

## 1. Six-Question Audit Assessment

### 1. Hours (Logged vs. Budgeted)
* **Actual Logged:** 52.25 hours across Weeks 1–8.
* **Course Benchmark:** 120.0 hours (15.0 h/week course pace).
* **Variance:** -67.75 hours against total course expectation.
* **Phase Breakdown:** Design (15.0h, 28.7%), Review (10.75h, 20.6%), Planning (10.0h, 19.1%), Requirements (9.0h, 17.2%), Inception (5.5h, 10.5%), Unlabeled (2.0h, 3.8%).

### 2. Scope vs. Remaining Budget
* **Remaining Course Budget:** 120.0 hours (Weeks 9–16).
* **Course Overhead Deduction:** 63.0 hours reserved for coursework, quizzes, weekly milestone documentation, and final presentation.
* **Actual Available Project Build Budget:** 57.0 hours.
* **25% Declared Buffer:** 14.25 hours held strictly in reserve.
* **Plannable Build Hours:** 42.75 hours.
* **Calibrated WBS Effort:** 42.60 hours (using our 1.16x historic calibration multiplier across 25 tasks).
* **Status:** Balanced. The Must scope fits within plannable hours because `NFR-USE-01` was cut in Milestone 7 (-2.5h calibrated).

### 3. Risk Status
Every risk in `docs/risk-register.md` was audited:
* `R-01` (Render Cold-Start 50s): No trigger fired. Addressed via frontend 60s timeout handling.
* `R-02` (VirusTotal Rate-Limiting): No trigger fired. Exposure reduced via CR-001 (+2.0h) and `slowapi` rate limiting.
* `R-03` through `R-08`: Triggers remain unfired.

### 4. Environment
* **Workbench:** Python 3.12, FastAPI, Uvicorn, and Pytest local loop functional.
* **External Free Tier:** VirusTotal Community API active (500 req/day, 4 req/min). Render Free Tier operational; no credit card expiration or billing cliff.

### 5. Novelty Load
* **Total Tasks in Plan:** 25 tasks.
* **Novel Tasks (Never Performed Before):** 3 tasks.
  1. `T-1.3`: Async FastAPI background polling loop with client disconnect abort (`request.is_disconnected()`).
  2. `T-2.3`: URL-safe unpadded base64 identifier encoding for VirusTotal v3 REST interface.
  3. `T-4.2`: Render static site and Web Service environment deployment with strict CORS origin lockdown.
* **Spike Scheduled:** Handled directly in Week 9 Walking Skeleton (`WP-1`).

### 6. Stakeholder Availability
* **Status:** Corporate employee stakeholder remains engaged and confirmed for usability verification during Iteration 1 (Week 11).