# Capstone — TBD

Senior capstone by Caleb Fuller, Fall 2026. 

## Current Status (Milestone 9)
- **Shipped:** Milestone 9 complete: Walking Skeleton and CI pipeline verified (`v0.1.0-skeleton`). Built standard repository structure (`docs/`, `src/api/`, `tests/`), full POSIX `script/` contract (`setup`, `lint`, `test`, `build`, `start`, `smoke`), runtime pinning (`.python-version`, `requirements.lock`), automated 5-stage GitHub Actions CI, upstream dependency honesty check (`VIRUSTOTAL_API_KEY` 503 gate), 8 requirement-traced issues (`[FR-1]` through `[NFR-2]`), clean secrets audit, and rotation runbook (`docs/runbook.md`).
- **Cut:** None; upstream VirusTotal v3 client integration kept as an honestly labeled stub in the request path pending Sprint 1 implementation.
- **Hours:** actual 13.00 h
- **Blocked on:** nothing
- **Ship confidence:** green

## What is here
- `docs/charter.md` — scope, constraints, non-goals, risks, working agreement
- `docs/hours-log.csv` — every work session, logged the day it happens
- `docs/ai-usage.md` — which AI tools are used on this project, and how
- `docs/` — one document per life-cycle phase; each header says the week it is written
- `src/`, `tests/` — empty until Week 9
- **Definition of Done:** View the [Definition of Done](docs/definition-of-done.md) checklist for all work items.

## How to run it

## Run it (about five minutes)

Requires: Python 3.12 (pinned in `.python-version`)

```bash
git clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git)
cd capstone
cp .env.example .env              # provides default development settings
./script/setup                    # installs pinned dependencies from requirements.lock
./script/start                    # serves API on [http://127.0.0.1:8000](http://127.0.0.1:8000)

# In a second terminal, verify the system by running:
./script/smoke

# Success looks like: SMOKE OK: http://127.0.0.1:8000/scan returned the seeded row (Safe). The skeleton walks.

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
