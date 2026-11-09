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

## Quick Start & Verification (About 5 minutes)

### Prerequisites
- Python 3.12+ (tested through Python 3.14)
- Git

---

### 1. Clone and Environment Setup

```bash
git clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git)
cd capstone

# Start environment configuration
cp .env.example .env
Note on API Keys: Automated unit, integration, and security tests run offline using internal mock transports and do not require external credentials. To execute live scans against VirusTotal v3, edit .env and set VIRUSTOTAL_API_KEY=your_64_char_key.

Windows (PowerShell)
PowerShell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

macOS / Linux (Bash)
Bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

2. Run the Test Suite
Verify all 60 acceptance, security boundary, and contract tests pass:

Bash
# Windows
.\.venv\Scripts\python -m pytest tests/ -v

macOS / Linux
./.venv/bin/pytest tests/ -v
Expected output:

Plaintext
======================= 60 passed in ~6.0s =======================

## 3. Launch the Application
Start the local Uvicorn development server:

Bash
# Windows
.\.venv\Scripts\python -m uvicorn src.api.main:app --reload

# macOS / Linux
./.venv/bin/uvicorn src.api.main:app --reload
The application serves:

Interactive UI: Open http://127.0.0.1:8000 in your browser.

Health Check: http://127.0.0.1:8000/health returns {"status":"ok"}.

4. Verify API Endpoints
In a second terminal, verify the primary scan endpoint:

Bash
curl -X POST [http://127.0.0.1:8000/scan](http://127.0.0.1:8000/scan) \
  -H "Content-Type: application/json" \
  -d '{"url":"[https://example.com](https://example.com)"}'
Expected response schema:

JSON
{
  "url": "[https://example.com](https://example.com)",
  "verdict": "Safe",
  "positives": 0,
  "total_engines": 0,
  "scan_date": "N/A",
  "cached": false,
  "raw_details": {}
}
