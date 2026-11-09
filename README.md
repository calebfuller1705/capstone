# Capstone — Phishing URL Scanner

Senior capstone by Caleb Fuller, Fall 2026. 

## Current Status (Milestone 11)
Shipped:     v0.9.0-rc.1 release candidate: end-to-end URL safety scanner with VirusTotal v3 integration, zero-persistence SSRF guard, full fault degradation, clean-clone verification (60/60 tests green), and Keep a Changelog release notes.
Cut:         Deferred recursive redirect unshortening for shortened links (bit.ly/tinyurl) via CR-003 to docs/backlog.md (B-01) for v1.1.
Hours:       planned 15.0 / actual 14.0        (from docs/hours-log.csv)
Blocked on:  nothing
Ship confidence: green

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
