# Capstone — TBD

Senior capstone by Caleb Fuller, Fall 2026. 

## Current Status (Milestone 10)
- Shipped: Milestone 10 complete: Iteration 1 development and verification gates passed. Implemented Slice 1 ([FR-2]) with an async VirusTotal v3 client (`src/services/vt_client.py`), deterministic unpadded base64url encoding, a 5.0-second fail-fast timeout ([NFR-1]), and typed error handling for 404 cache misses, 429 rate limits, and network timeouts. Extracted typed Pydantic v2 schemas (`src/api/schemas.py`). 10 automated unit and adversary tests passing green (100% pass rate). Completed 10-point Definition of Done checklist, 4-pass self-review (`docs/review/iteration-1-self-review.md`), amber-zone AI usage audit (`docs/ai-usage.md`), commit hygiene audit with 5 Conventional Commit rewrites, hours log weekly rollup audit (`tools/hours_report.py`), credential search confirming zero history leaks and in-memory credential boundaries ([NFR-2]), deterministic seed data (`docs/demo-seed.json`), and rehearsed 5-minute demo script with video fallback. Closed GitHub issue #2 and verified #9.
- Cut: Target URL input validation ([FR-1]), asynchronous scan submission queue ([FR-3]), multi-engine detection aggregation ([FR-4]), latency reporting ([FR-5]), and route-level HTTP status code exception mapping ([FR-6]) explicitly deferred to Iteration 2 (Milestones 11–12).
- Hours: actual 13.5 h
- Blocked on: nothing
- Ship confidence: green

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
