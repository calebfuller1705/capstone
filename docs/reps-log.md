## Week 13 Reps

## Rep 1 — Score your README before you touch it

Score key: 2 = present and complete, 1 = present but thin or vague, 0 = missing

 1. What it is / who it is for: 1
 2. Demo (screenshot, GIF, session): 0
 3. Prerequisites with versions: 1
 4. Install: 1
 5. Configure: 1
 6. Run (+ the action that proves it works): 1
 7. Test: 1
 8. Project layout: 1
 9. Troubleshooting: 0
10. License: 0
11. Contact / further reading: 0
TOTAL: 7 / 22

**Widget Comparison:**
- Self-Score: 6 / 22 (~27%)
- README Grader Widget Score: 48 / 100
- Projected Time to First Successful Run: 1h 13m (Target: 15 min)
- Grader Flags:
  - ⚑ Configuration referenced but not explained (−6 pts)
  - ✕ Missing: Screenshot/demo, Project layout, Troubleshooting, License, Contact
  - ~ Thin: Configure, Run, Test

  ## Rep 2 — Pin what you actually have

### Prerequisites Table

| Requirement | Tested-On Version | Check Command | What Breaks and How You Will Recognize It |
|---|---|---|---|
| **Python** | `Python 3.14.2` | `python --version` (Windows) or `python3 --version` | Running Python < 3.12 fails during dependency installation or Pydantic V2 model validation in `src/api/schemas.py`. If Python is not installed or not added to `PATH`, running the command prints `'python' is not recognized as an internal or external command` (Windows) or `command not found: python3` (macOS/Linux). |
| **Git** | `git version 2.47.0.windows.2` | `git --version` | Without Git, the reader cannot clone the repository or checkout tags like `v0.9.0-rc.1`. The terminal prints `'git' is not recognized as an internal or external command`. |
| **pip / venv** | Bundled with Python 3.14 (`pip 24.3.1`) | `python -m pip --version` | Without `venv` (common on clean Debian/Ubuntu Linux installs), creating the virtual environment fails with: `The virtual environment was not created successfully because ensurepip is not available. You need to install the python3-venv package`. |
| **VirusTotal v3 API Key** | v3 Public API (64-character hex string) | `echo $env:VIRUSTOTAL_API_KEY` (PS) or `echo $VIRUSTOTAL_API_KEY` (Bash) | Automated tests run offline via mocks and pass without a key. However, live scans submitted through the UI or `/scan` will fail with an HTTP 401 Unauthorized upstream error from VirusTotal if the key is missing, empty, or malformed.

## Rep 3 — Find the invisible accounts and the personal paths

### Pass 1: Mechanical Audit (Personal Paths & Undocumented Ports)

Audit command executed:
```powershell
Get-ChildItem -Recurse -Include README.md,*.md docs,README.md | Select-String -Pattern "C:\\Users|/home/|localhost:[0-9]{4}|127\.0\.0\.1"

Audit Findings:
Personal absolute paths (C:\Users, /home/): 0 hits. No machine-specific developer paths exist in README.md or docs/.
Loopback IP / Localhost (127.0.0.1, localhost:8000):
Legitimate security test targets: Appears across docs/security-review.md, docs/iteration-1-plan.md, and test traceability matrices as an SSRF boundary test case (blocking loopback access).
Local runtime address: Appears in README.md and docs/skeleton-trace.md referring to the default Uvicorn bind address (http://127.0.0.1:8000).

| External dependency | Where you get it | Free? (verify with vendor) | What happens without it |
|VirusTotal v3 API Key|Register a free Community account at virustotal.com and copy the 64-character API key from your user profile API settings.|Yes (Free public tier provides 4 requests/min, 500 requests/day, 15.5k requests/month as of Fall 2026; verify current quotas with vendor).|Automated test suites (pytest tests/) continue to pass because they run offline using mock HTTP transports. However, live URL submissions from the web UI (/) or POST /scan will fail with upstream 401 Unauthorized errors from VirusTotal.|
|PyPI (Python Package Index)|Public package registry accessed automatically by pip.|Yes (Public internet access required).|Running pip install -r requirements.txt fails if the machine is behind an unconfigured corporate proxy or completely offline, blocking initial environment setup.|
