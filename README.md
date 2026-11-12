# Capstone — Phishing URL Scanner

Senior capstone by Caleb Fuller, Fall 2026. A stateless, zero-persistence web application that evaluates URLs against the VirusTotal v3 threat intelligence API to deliver real-time Safe or Unsafe verdicts without storing user browsing history.

Corporate employees, IT helpdesk staff, and security reviewers frequently encounter suspicious links in emails and messages, yet pasting unverified URLs into public web tools or logging scan histories risks leaking sensitive internal destinations. Phishing URL Scanner solves this problem by providing a fast, zero-persistence web interface and REST API that evaluates URLs against the VirusTotal v3 threat intelligence engine and immediately discards all request data from memory once a Safe or Unsafe verdict is returned.

- **Status:** Working (`v0.9.0-rc.1` release candidate). End-to-end URL safety scanner with VirusTotal v3 integration, zero-persistence SSRF guard, full fault degradation, clean-clone verification (60/60 tests green), and Keep a Changelog release notes.
- **What it does not do:** No database persistence, user accounts, or historical scan logs (strictly stateless per privacy constraint `CON-04`); no recursive redirect unshortening for shortened links (`bit.ly`/`tinyurl`, deferred via CR-003 to `docs/backlog.md` item B-01 for `v1.1`).

## Current Status (Milestone 13)
- **Shipped:** `v0.9.0-rc.1` release candidate + full Milestone 13 operational and architectural documentation set.
- **Cut:** Deferred recursive redirect unshortening (`B-01`) and persistent server-side action logging (`B-04`) to `v1.1`.
- **Hours:** planned 15.0 / actual 14.0 (from `docs/hours-log.csv`)
- **Blocked on:** nothing
- **Ship confidence:** green

---

## Video Walkthrough Demo
Follow the link to view the video demonstration of the project: https://drive.google.com/file/d/1DrOW6yAYi_dGco_4G4RLE_AlnN27SuQi/view?usp=sharing

## Demo

Sample terminal session starting the Uvicorn server and verifying a live URL scan:

```text
$ .\.venv\Scripts\python -m uvicorn src.api.main:app --reload
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Application startup complete.

$ curl -s -X POST [http://127.0.0.1:8000/scan](http://127.0.0.1:8000/scan) -H "Content-Type: application/json" -d '{"url":"[https://example.com](https://example.com)"}'
{"url":"[https://example.com](https://example.com)","verdict":"Safe","positives":0,"total_engines":0,"scan_date":"N/A","cached":false,"raw_details":{}}
```

### Prerequisites Table

**Tested on Python 3.14.2 (supports Python 3.12+), Git 2.47.0, and pip 24.3.1.**

| Requirement | Tested-On Version | Check Command | What Breaks and How You Will Recognize It |
|---|---|---|---|
| **Python** | Python 3.14.2 (supports 3.12+) | `python --version` (Windows) or `python3 --version` (macOS/Linux) | Running Python `< 3.12` fails during dependency installation or Pydantic V2 model validation in `src/api/schemas.py`. If Python is not installed or not added to `PATH`, running the command prints `'python' is not recognized as an internal or external command` (Windows) or `command not found: python3` (macOS/Linux). |
| **Git** | git version 2.47.0.windows.2 | `git --version` | Without Git, the reader cannot clone the repository or checkout tags like `v0.9.0-rc.1`. The terminal prints `'git' is not recognized as an internal or external command`. |
| **pip / venv** | Bundled with Python 3.14 (pip 24.3.1) | `python -m pip --version` | Without `venv` (common on clean Debian/Ubuntu Linux installs), creating the virtual environment fails with: `The virtual environment was not created successfully because ensurepip is not available. You need to install the python3-venv package`. |
| **VirusTotal v3 API Key** | v3 Public API (64-character hex string) | `echo $env:VIRUSTOTAL_API_KEY` (PS) or `echo $VIRUSTOTAL_API_KEY` (Bash) | Automated tests run offline via mocks and pass without a key. However, live scans submitted through the UI or `/scan` will fail with an HTTP `401 Unauthorized` upstream error from VirusTotal if the key is missing, empty, or malformed. |


### Install
1. Installation
Step 1: Clone the repository
Bash
git clone https://github.com/calebfuller1705/capstone.git
cd capstone

Expected: Cloning into 'capstone'... followed by Resolving deltas: 100% (xx/xx), done. — takes about 3 seconds.

If you see: fatal: destination path 'capstone' already exists, change into the existing directory (cd capstone) or remove the duplicate directory before cloning.

Step 2: Create a virtual environmentPowerShell

PowerShell
python -m venv .venv

Bash
python3 -m venv .venv

Expected: Silent prompt return with .venv/ created in the repository root — takes about 2 seconds.

If you see: 'python' is not recognized as an internal or external command, verify Python 3.12+ is installed and that the "Add Python to PATH" checkbox was enabled during installation.

If you see (Linux): The virtual environment was not created successfully because ensurepip is not available, install the system package via sudo apt install python3-venv.

Step 3: Upgrade pip and install dependenciesPowerShell
PowerShell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip install -r requirements.txt

Bash
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

Expected: Successfully installed fastapi-... httpx-... pydantic-... pytest-... uvicorn-... — takes about 12 seconds.

If you see: WARNING: There was an error checking the latest version of pip, ignore it; dependency installation completes successfully regardless of pip upgrade notices.

If you see: ERROR: Could not find a version that satisfies the requirement, confirm your virtual environment uses Python 3.12+ via .\.venv\Scripts\python --version.

## Configuration

Step 1: Initialize the local environment filePowerShell
PowerShell
Copy-Item .env.example .env

Bash
cp .env.example .env

Expected: Silent prompt return — takes <1 second.

If you see: cp: .env.example: No such file or directory, ensure your current shell directory is the project root (Get-Location on PowerShell or pwd on Bash should terminate in \capstone).

Step 2: Set VirusTotal API credentials
Open .env and assign your key: VIRUSTOTAL_API_KEY=<your-api-key>

Sample ./.env file contents:

Code snippet
VIRUSTOTAL_API_KEY=<your-api-key>
FRONTEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)

Expected: Offline test suites (pytest tests/) bypass external calls using mock transports and pass without an active key.

If you see: Live scan submissions return HTTP 401 Unauthorized or UI banner Invalid or missing VirusTotal API key, confirm your 64-character hex key contains no leading/trailing quotes, spaces, or stray line breaks.


## Running the Application

Start the FastAPI server from the repository root with your virtual environment activated (or by calling the `.venv` interpreter directly):

```bash
# With virtual environment activated (Windows / macOS / Linux)
python -m uvicorn src.api.main:app --reload

# Or directly via .venv (Windows PowerShell)
.\.venv\Scripts\python -m uvicorn src.api.main:app --reload

# Or directly via .venv (macOS / Linux)
./.venv/bin/uvicorn src.api.main:app --reload
```

What a working start looks like:
Within ~1.5 seconds, Uvicorn binds to port 8000 and prints:

INFO:     Will watch for changes in: ['...']
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process [...] using StatReload
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.


If you see: ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): address already in use (or [Errno 98] on Linux), stop the lingering process on port 8000 or append --port 8001.

If you see: ERROR: [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000): address already in use (or [Errno 98] on Linux), terminate the lingering process on port 8000 or append --port 8001 to bind to an alternate port.   

Verification Action   

Prove the entire application pipeline functions end-to-end rather than merely confirming process startup:

Option A: Browser Interface
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in a browser.Enter [https://example.com](https://example.com) into the URL input bar and click Scan URL.

Expected: Within 1 second, the UI renders a green Verdict: Safe badge showing 0 detections across engines, confirming routing, template rendering, and scanner logic.

**Note that in this method, your terminal in VS Code shows the results of the scan in your local terminal.**

Option B: CLI Scan Request
In a separate terminal, execute:Bashcurl -s -X POST http://127.0.0.1:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'

Expected:JSON{"url":"https://example.com","verdict":"Safe","positives":0,"total_engines":0,"scan_date":"N/A","cached":false,"raw_details":{}}
Response returns in <1 second with HTTP 200.

If you see: curl: (7) Failed to connect to 127.0.0.1 port 8000, confirm the Uvicorn terminal process did not exit with an unhandled exception.

## Test
Execute the full offline verification suite (unit, integration, security boundary, and acceptance tests):

PowerShell
.\.venv\Scripts\python -m pytest tests/ -v
macOS / Linux (Bash):

Bash
./.venv/bin/pytest tests/ -v

Expected: ======================= 60 passed in ~6.0s ======================= with exit code 0.

Known failures: None. All 60 tests run offline via internal mock transports without requiring internet access or a VirusTotal API key.

## Project Layout
capstone/
├── docs/
│   ├── adr/                    # Architecture Decision Records and index
│   ├── ai-usage.md             # AI tool usage log and successor risk notes
│   ├── architecture.md         # System overview (§0) and technical specification
│   ├── charter.md              # Scope, constraints, non-goals, and working agreement
│   ├── defect-log.md           # Verified defects, severity ratings, and status
│   ├── definition-of-done.md   # Quality gates and completion checklist
│   ├── hours-log.csv           # Work session time log
│   ├── onboarding.md           # Developer orientation, feature map, and first issue
│   └── runbook.md              # Operational procedures and defect-mined failure catalogue
├── migrations/
│   └── 0001-stateless.sql      # Empty sentinel confirming zero-database architecture
├── src/
│   ├── api/
│   │   ├── main.py             # FastAPI routes, rate limiting, and RFC 7807 error envelopes
│   │   └── schemas.py          # Pydantic request/response models and URL validation
│   ├── services/
│   │   └── vt_client.py        # VirusTotal v3 HTTP client and polling loop
│   └── static/
│       ├── app.js              # Client-side validation, fetch logic, and DOM state
│       ├── index.html          # Accessible single-page UI markup
│       └── styles.css          # Application styling
└── tests/
    ├── acceptance/             # End-to-end acceptance path tests
    ├── fixtures/               # Happy, boundary, hostile, and performance JSON fixtures
    ├── integration/            # Upstream contract, fault, and frontend tests
    ├── security/               # SSRF and input boundary security tests
    └── unit/                   # Isolated schema, client, health, and linter tests


## Troubleshooting
Live scan fails with HTTP 401 Unauthorized: Your VIRUSTOTAL_API_KEY in .env is missing, malformed, or wrapped in quotes. Copy a fresh 64-character hex key from your VirusTotal profile into .env without quotes and restart Uvicorn.

Scan times out with HTTP 504 Gateway Timeout: VirusTotal's public API exceeded the 3.0-second socket timeout or 10.0-second polling window. Wait 15 seconds (public free tier is capped at 4 requests/minute) and click Retry Scan.

Server fails to start with address already in use (Errno 10048 / Errno 98): Another local server is bound to port 8000. Terminate the lingering process or launch with --port 8001.

"Copy Result" button does nothing: Browsers restrict navigator. Clipboard on insecure non-localhost HTTP origins. Access the app via http://127.0.0.1:8000 or http://localhost:8000.

## License
This project is released under the MIT License for academic evaluation and educational reuse.

## Contact and Further Reading
Author: Caleb Fuller (github.com/calebfuller1705/capstone)

Post-Graduation Contact: calebfuller1705@gmail.com

Architecture Overview: docs/architecture.md

Operational Runbook: docs/runbook.md

Developer Onboarding: docs/onboarding.md

Decision Records: docs/adr/README.md

Defect Log: docs/defect-log.md

Definition of Done: docs/definition-of-done.md