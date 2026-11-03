# Capstone — TBD

Senior capstone by Caleb Fuller, Fall 2026. 

## Current Status (Milestone 11)
- Shipped: Milestone 11 complete: Test engineering practices, automated verification suites, and dress rehearsal gates passed. Authored comprehensive test plan (`docs/test-plan.md`) covering 4 test levels and checkable exit criteria. Generated deterministic test fixtures (`tools/generate_test_data.py`, seed 20261031) yielding 50 records across happy, boundary, and hostile families. Established 7-field defect tracking standard in `docs/defect-log.md`. Resolved `DEF-001` (URL length constraints on [FR-INP-03]) through a strict 3-commit Red-Green-Prove regression cycle (`test_tc_inp_03_url_length_exceeds_2048` proven red on pre-fix commit). Conducted empirical AI test generation audit exposing change detector failure modes (2 vs. 7 errors across spec vs. code contexts). Implemented VirusTotal v3 seam verification in `tests/integration/test_vt_contracts.py` with structure checks, property invariants, 5 golden set fixtures, and 5 stubbed failure paths (429, timeout, malformed HTML/JSON, missing attributes, 503). Completed 45-minute unscripted exploratory testing ("pesticide check") discovering `DEF-011` through `DEF-015` and adding client-side concurrency and debounce testing to the test plan. Executed clean-room verification dress rehearsal in a fresh clone (`capstone-rehearsal`) with 28 passing tests (100% green in 2.39s), generated `docs/test-results.md`, verified 35% Must requirement coverage via `tools/coverage_report.py`, audited exit criteria, and documented operational workarounds for all open items.
- Cut: 15 unverified Must requirements ([FR-INP-01], [FR-UI-01], [FR-UI-02], [NFR-ACC-01..05], etc.) and 3 exploratory defects (`DEF-011` submit debounce, `DEF-014` raw 422 banner display, `DEF-015` keyboard focus indicator) explicitly deferred to Iteration 2 frontend web UI construction and accessibility styling passes (Milestone 12).
- Hours: actual 11.75 h (Milestone 11 total)
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
