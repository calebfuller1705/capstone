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
```

## Command Verification Table (Rep 10)

| Number | Command the assistant wrote | Ran it? | Correct? | What was actually wrong |
| 1 | netstat -ano | findstr :8000 | Yes | Yes | Executed cleanly in PowerShell (returned empty because port 8000 was unbound). |
| 2 | Select-String -Path .env -Pattern "VIRUSTOTAL_API_KEY" | Yes | Yes | Executed cleanly in PowerShell and located the key in .env (redact raw key before committing). |
| 3 | \.venv\Scripts\python -m pytest tests/integration/test_vt_contracts.py -k "timeout" -v | Yes | Yes | Executed cleanly and passed (1 passed, 9 deselected in 1.48s).
| 4 | \.venv\Scripts\python -c "from src.services.vt_client import encode_vt_url_id; print(encode_vt_url_id(' [https://google.com](https://google.com) '))" | Yes | No | Two issues: (1) Markdown auto-linking wrapped the URL in [...](...) brackets during copy-paste, and (2) encode_vt_url_id() does not strip whitespace itself (DEF-002 remains open; input trimming lives in schemas.py), producing a leading space byte (IFt...) instead of aHR0. | 
| 5 | \.venv\Scripts\python -m pytest tests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048 -v | Yes | No | Failed with ERROR: not found (collected 0 items). The exact pytest function node name was inferred from the old defect report and no longer matches test_url_validation.py; running the module file or -k "2048" is required instead. |
| 6 | curl -s -X POST [http://127.0.0.1:8000/scan](http://127.0.0.1:8000/scan) -H "Content-Type: application/json" -d '{"url":"[https://example.com](https://example.com)"}' | Yes | No | Failed in Windows PowerShell because curl aliases to Invoke-WebRequest (which rejects POSIX flags like -X/-d and choked on Markdown link syntax). Requires curl.exe or Invoke-RestMethod on Windows PowerShell. |

---

## Rep 11 — Document the part that can change without your code changing

**VirusTotal v3 Public API (Volatile External Dependency)**

## What the feature does and what it does when it fails: 
Queries the VirusTotal v3 URL lookup endpoint (GET /urls/{url_id}) to retrieve multi-engine security analysis counts (malicious and suspicious) and maps them to a "Safe", "Ambiguous", or "Unsafe" verdict.
    On HTTP 404 (URL never previously scanned by VirusTotal), fetch_url_report() returns None rather than raising an exception.
    On HTTP 429 (rate limit/quota exceeded), it raises UpstreamRateLimitError, returning an HTTP 429 error envelope to the client.
    On HTTP 5xx, malformed JSON (JSONDecodeError), socket timeouts (httpx.TimeoutException), or network drops (httpx.RequestError), it raises UpstreamServiceError, degrading to an HTTP 502/504 error response without crashing the FastAPI worker.

# Exact API version/identifier and date pinned: 
VirusTotal Public API v3 ([https://www.virustotal.com/api/v3/urls/](https://www.virustotal.com/api/v3/urls/){url_id}), using unpadded URL-safe base64 identifiers (base64.urlsafe_b64encode(url.encode("utf-8")).decode("ascii").rstrip("=")). 

**Verified and pinned against live v3 responses on 2026-09-24 and re-verified 2026-11-12. Verify endpoint availability and response schema before assuming live scans run unattended.**

# Where the integration and config live: 
All upstream request logic, threshold constants, and cache controls live in src/services/vt_client.py. Authentication is loaded from the VIRUSTOTAL_API_KEY environment variable via get_vt_api_key() (configured locally in .env, never hardcoded).

# Parameters that change behavior:

DEFAULT_TIMEOUT_SECONDS = 5.0: Per-request httpx.AsyncClient socket timeout; requests exceeding 5.0 seconds abort immediately and raise UpstreamServiceError.

CACHE_TTL_SECONDS = 300.0: In-memory dictionary cache (_REPORT_CACHE) retains identical URL verdicts for 5 minutes to conserve free-tier API quota. Cache is automatically bypassed and cleared whenever _is_mock_client(client) detects a test mock or httpx.MockTransport.

MALICIOUS_DANGER_THRESHOLD = 2 and SUSPICIOUS_DANGER_THRESHOLD = 3: Evaluates "Unsafe" when malicious >= 2 or suspicious >= 3; evaluates "Ambiguous" when either counter is > 0 below those thresholds; otherwise evaluates "Safe".

# Cost and quota limits (hedged honestly):
Measured under my free VirusTotal Community account on 2026-09-24 (and checked 2026-11-12) at $0.00/month, subject to public free-tier limits of 4 requests/minute, 500 requests/day, and 15,500 requests/month. Vendor pricing, rate limits, and free-tier quotas change without notice—re-verify current limits with VirusTotal (docs.virustotal.com) before relying on these figures.

# What must not be assumed stable:

Non-deterministic external verdicts: 
VirusTotal continuously updates its underlying antivirus engines; the exact same URL can shift between "Safe", "Ambiguous", and "Unsafe" across days without any change to this codebase.

Upstream JSON schema drift: fetch_url_report() depends on data.attributes.last_analysis_stats (malicious, suspicious, harmless, undetected) and data.attributes.last_analysis_date. If VirusTotal renames or nests these keys differently, stats defaults to {} and reports "Safe" with 0 engines rather than raising a schema error.

Verification command: 
Run .\.venv\Scripts\python -m pytest tests/integration/test_vt_contracts.py -v to verify contract parsing against mock payloads, followed by a live POST /scan request against [https://example.com](https://example.com) after any upstream API change.