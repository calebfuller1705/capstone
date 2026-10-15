# Capstone — TBD

Senior capstone by Caleb Fuller, Fall 2026. 

## Current Status (Milestone 7)
* **Shipped:** Milestone 7 complete: Project Plan baselined (`docs/plan.md`). Made a 6-work-package, 25-task Work Breakdown Structure (WBS) with three-point PERT estimates, weekly gates, and a burn-down baseline. I have my 25% project buffer (14.25 h) against a 57.0 h build capacity (Weeks 8–16), computed a 1.16x calibration factor, audited AI efficiency, and baselined an 8-item Risk Register (`docs/risk-register.md`).
* **Cut:** Deferred `NFR-USE-01` (First-Time User Usability Testing Sessions) from Should to Won't to recover 2.5 calibrated hours, successfully closed my budget gap to fit within the 42.75 h plannable capacity and protecting the full 25% deployment buffer. Flagged for change control at the Week-8 review.
* **Hours:** actual 12.5
* **Blocked on:** nothing
* **Ship confidence:** green

## What is here
- `docs/charter.md` — scope, constraints, non-goals, risks, working agreement
- `docs/hours-log.csv` — every work session, logged the day it happens
- `docs/ai-usage.md` — which AI tools are used on this project, and how
- `docs/` — one document per life-cycle phase; each header says the week it is written
- `src/`, `tests/` — empty until Week 9
- **Definition of Done:** View the [Definition of Done](docs/definition-of-done.md) checklist for all work items.

## How to run it

## Run it (about five minutes)

Requires Python 3.12 (pinned in `.python-version`) and Git. No administrator rights or database installation required.

On Windows, execute the commands below in **Git Bash**[cite: 1]:

```bash
# 1. Clone repository
git clone <this repo>
cd capstone

# 2. Setup environment and install locked dependencies
./script/setup

# 3. Execute automated test suite
./script/test

# 4. Start local development server
./script/start

# Verifying Success
# 1. Health Endpoint
#Open http://127.0.0.1:8000/health in your browser. You should see:

JSON
{"status":"ok"}

#2. Walking Skeleton Scan Route

# In a separate terminal, test the real request dispatch hop:
Bash
curl -X POST [http://127.0.0.1:8000/scan](http://127.0.0.1:8000/scan) \
  -H "Content-Type: application/json" \
  -d '{"url":"[https://example.com](https://example.com)"}'

# Expected response:
JSON
{
  "url": "[https://example.com](https://example.com)",
  "verdict": "Safe",
  "source": "skeleton-stub",
  "scan_time_ms": 15
}