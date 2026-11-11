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

### Prerequisites Table

| Requirement | Tested-On Version | Check Command | What Breaks and How You Will Recognize It |
|---|---|---|---|
| **Python** | `Python 3.14.2` | `python --version` (Windows) or `python3 --version` | Running Python < 3.12 fails during dependency installation or Pydantic V2 model validation in `src/api/schemas.py`. If Python is not installed or not added to `PATH`, running the command prints `'python' is not recognized as an internal or external command` (Windows) or `command not found: python3` (macOS/Linux). |
| **Git** | `git version 2.47.0.windows.2` | `git --version` | Without Git, the reader cannot clone the repository or checkout tags like `v0.9.0-rc.1`. The terminal prints `'git' is not recognized as an internal or external command`. |
| **pip / venv** | Bundled with Python 3.14 (`pip 24.3.1`) | `python -m pip --version` | Without `venv` (common on clean Debian/Ubuntu Linux installs), creating the virtual environment fails with: `The virtual environment was not created successfully because ensurepip is not available. You need to install the python3-venv package`. |
| **VirusTotal v3 API Key** | v3 Public API (64-character hex string) | `echo $env:VIRUSTOTAL_API_KEY` (PS) or `echo $VIRUSTOTAL_API_KEY` (Bash) | Automated tests run offline via mocks and pass without a key. However, live scans submitted through the UI or `/scan` will fail with an HTTP 401 Unauthorized upstream error from VirusTotal if the key is missing, empty, or malformed.

### Install, Configure, Run, and Verification
1. Installation
## Step 1: Clone the repository
Bash
git clonehttps://github.com/calebfuller1705/capstone.git
cd capstone

Expected: Cloning into 'capstone'... followed by Resolving deltas: 100% (xx/xx), done. — takes about 3 seconds.

If you see: fatal: destination path 'capstone' already exists, change into the existing directory (cd capstone) or remove the duplicate directory before cloning.

## Step 2: Create a virtual environmentPowerShell

### PowerShell
python -m venv .venv

### Bash
python3 -m venv .venv

# Expected: Silent prompt return with .venv/ created in the repository root — takes about 2 seconds.

# If you see: 'python' is not recognized as an internal or external command, verify Python 3.12+ is installed and that the "Add Python to PATH" checkbox was enabled during installation.

# If you see (Linux): The virtual environment was not created successfully because ensurepip is not available, install the system package via sudo apt install python3-venv.

## Step 3: Upgrade pip and install dependenciesPowerShell
### PowerShell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

### Bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

### Expected: Successfully installed fastapi-... httpx-... pydantic-... pytest-... uvicorn-... — takes about 12 seconds.

If you see: WARNING: There was an error checking the latest version of pip, ignore it; dependency installation completes successfully regardless of pip upgrade notices.

If you see: ERROR: Could not find a version that satisfies the requirement, confirm your virtual environment uses Python 3.12+ via .\.venv\Scripts\python --version.

2. Configuration

## Step 1: Initialize the local environment filePowerShell
# PowerShell
Copy-Item .env.example .env

# Bash
cp .env.example .env

Expected: Silent prompt return — takes <1 second.

If you see: cp: .env.example: No such file or directory, ensure your current shell directory is the project root (Get-Location on PowerShell or pwd on Bash should terminate in \capstone).

## Step 2: Set VirusTotal API credentials
Open .env and assign your key: Code snippetVIRUSTOTAL_API_KEY=your_64_character_hex_key_here

Expected: Offline test suites (pytest tests/) bypass external calls using mock transports and pass without an active key.

If you see: Live scan submissions return HTTP 401 Unauthorized or UI banner Invalid or missing VirusTotal API key, confirm your 64-character hex key contains no leading/trailing quotes, spaces, or stray line breaks.

3. Run the Application

## Start the local Uvicorn development server:

# PowerShell
.\.venv\Scripts\python -m uvicorn src.api.main:app --reload

# Bash
./.venv/bin/uvicorn src.api.main:app --reload


Expected:PlaintextINFO:     Will watch for changes in: ['...']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

Ready to receive requests in ~1.5 seconds.

If you see: ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): address already in use (or [Errno 98] on Linux), terminate the lingering process on port 8000 or append --port 8001 to bind to an alternate port.   

# 4. Verification Action   

Prove the entire application pipeline functions end-to-end rather than merely confirming process startup:

# Option A: Browser Interface
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.Enter [https://example.com](https://example.com) into the URL input bar and click Scan URL.

Expected: Within 1 second, the UI renders a green Verdict: Safe badge showing 0 detections across engines, confirming routing, template rendering, and scanner logic.

# Option B: CLI Scan Request
In a separate terminal, execute:Bashcurl -s -X POST http://127.0.0.1:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

Expected:JSON{"url":"https://example.com","verdict":"Safe","positives":0,"total_engines":0,"scan_date":"N/A","cached":false,"raw_details":{}}
Response returns in <1 second with HTTP 200.

If you see: curl: (7) Failed to connect to 127.0.0.1 port 8000, confirm the Uvicorn terminal process did not exit with an unhandled exception.