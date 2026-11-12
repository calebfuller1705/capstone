# Runbook — Phishing URL Scanner

**System:** Phishing URL Scanner (Stateless Security Gateway)  
**Host Environment:** Local Uvicorn development server (`127.0.0.1:8000`) and React frontend  
**Last Verified:** 2026-11-11 by Caleb Fuller  
**Status:** Operational (v0.9.0-rc.1)

---

## 1. System Overview & Where It Runs

| Environment | Where | Who has access | How to get in |
| Local | developer machine ([http://127.0.0.1:8000](http://127.0.0.1:8000)) | anyone with the repo | see README.md
| Staging | none| N/A | N/A
| Production | Render web service (or local workstation for evaluation) | Caleb Fuller | Render Dashboard via GitHub OAuth or local launch via README.md

Where the data actually lives: None. The system is strictly stateless (CON-04, NFR-SEC-02); scan state, timeout clocks, and in-memory rate-limiting counters reside transiently in Python process RAM and are discarded immediately upon response transmission. No database host, table, or persistent storage bucket exists.

Where the logs actually live: Standard output (stdout) / terminal console stream running the Uvicorn process

## 2. Start, Stop, and Restart

### Start Backend
```powershell
# Windows (PowerShell)
.\.venv\Scripts\python -m uvicorn src.api.main:app --reload --port 8000
Bash
# macOS / Linux (Bash)
./.venv/bin/uvicorn src.api.main:app --reload --port 8000
Stop Service
Press CTRL+C in the terminal executing the Uvicorn process.
```

### Restart Service
If running with --reload, saving any file in src/ triggers an automatic reload. For a manual restart:

Press CTRL+C in the running terminal.

Verify process release via netstat -ano | findstr :8000 (Windows) or lsof -i :8000 (macOS/Linux).

Re-run the start command above.

## 3. Health Check
Execute a direct HTTP GET against the unauthenticated health endpoint:

Bash
curl -s [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
Healthy Output: {"status":"ok"} with HTTP status 200 OK (latency < 20ms).

Unhealthy Output: Connection refused (curl: (7) Failed to connect...), HTTP 500 Internal Server Error, or response hanging past 2.0 seconds.

## 4. Routine Operations
|Task | Command | How often | Expected result | 
| Back up the data | N/A| Never | Stateless architecture (CON-04, NFR-SEC-02); 0 bytes of persistent scan history or database tables exist to back up. |
| Restore from a backup | N/A | on demand | Stateless; disaster recovery consists of restarting Uvicorn and verifying curl -s [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health) returns {"status":"ok"}. |
| Apply a schema change | Inspect migrations/0001-stateless.sql | on release | Confirmed sentinel file remains empty with documentation header; verifies no database tables or migrations are provisioned. | 
| Rotate a key or secret | 1. Revoke old key at virustotal.com 2. Generate new key 3. Update VIRUSTOTAL_API_KEY in .env 4. Restart Uvicorn | Every 90 days or right away with exposure| Run curl -s -X POST [http://127.0.0.1:8000/scan](http://127.0.0.1:8000/scan) -H "Content-Type: application/json" -d '{"url":"[https://example.com](https://example.com)"}' and verify HTTP 200 with "verdict": "Safe".
| Seed demo data | N/A | for demos | System relies on static fixture files (tests/fixtures/test_data_hostile.json) for automated tests, or live target entries ([https://example.com](https://example.com)) for manual UI demonstrations.   

## 5. Normal Readings & Baseline Telemetry
Under normal operating conditions:

Startup Time: 1.2 to 2.0 seconds from command execution to Application startup complete.

Idle Memory: ~45 MB to 65 MB resident set size (RSS).

Scan Latency: 800ms to 2,500ms for live VirusTotal queries; < 50ms for local mock runs.

Harmless Noise: StatReload file detection logs during active development; pip wheel update notices during environment activation.

## 6. Failure Catalogue

# F-01 — Upstream socket timeout raises uncaught 500 error
Symptom: httpx.TimeoutException or unhandled UpstreamServiceError in terminal output; API returns HTTP 500 Internal Server Error instead of a structured 504.

First check: Check backend console for httpx.ReadTimeout or execute curl -s -X POST http://127.0.0.1:8000/scan -H "Content-Type: application/json" -d '{"url":"https://example.com"}' → healthy returns HTTP 200 with verdict JSON within 3 seconds.

Likely cause: VirusTotal API response latency exceeded the 3.0s client timeout during peak traffic, triggering uncaught exception handling (DEF-003).

Fix: Confirm network connectivity to https://www.virustotal.com. Verify src/services/ timeout handling is catching httpx.TimeoutException and returning an RFC 7807 error envelope with status 504.

Verify: Submit a scan via the web UI; verify the UI shows an error banner: "Timeout: Analysis took too long" alongside an active [Retry Scan] button.

If that fails: External upstream service is degraded. Check status at virustotal.com and escalate.

# F-02 — False 404 cache misses or scan errors on pasted URLs
Symptom: Submitting a known benign or malicious URL returns a 404 cache miss from VirusTotal or fails analysis lookup.

First check: Check backend debug log for the computed base64 ID; compare with base64.urlsafe_b64encode("https://example.com".encode()).decode().strip("=").

Likely cause: Leading or trailing whitespace was included in the user's input string before base64 hashing, producing an invalid SHA-256 identifier (DEF-002).

Fix: Ensure input normalization (url.strip()) executes prior to ID generation in src/api/schemas.py and service routing.

Verify: Run pytest tests/unit/test_url_validation.py -k test_whitespace → passes with 0 failures.

If that fails: Check whether trailing slashes on domain roots are being stripped symmetrically (DR-019).

# F-03 — Schema validation fails silently or crashes on long / malformed URLs
Symptom: Terminal displays unhandled validation exceptions or accepts URLs exceeding 2,048 characters, resulting in upstream payload rejections.

First check: Run pytest tests/unit/test_url_validation.py::test_tc_inp_03_url_length_exceeds_2048 → healthy is PASSED.

Likely cause: Pydantic model in src/api/schemas.py is missing string length constraints (max_length=2048) or URI scheme validation regex (DEF-001).

Fix: Restore boundary constraints in ScanRequest schema:

Python
url: str = Field(..., min_length=1, max_length=2048)
Verify: Submit a 2,049-character string; verify API returns HTTP 400 Bad Request with error detail code malformed_url.

If that fails: Review FastAPI error handler middleware in src/api/main.py.

# F-04 — Copy button fails silently in React interface
Symptom: Clicking "Copy Result" produces no visual feedback, and the clipboard remains unchanged.

First check: Open browser DevTools Console (F12); healthy displays no uncaught promises. Unhealthy logs TypeError: Cannot read properties of undefined (reading 'writeText').

Likely cause: The browser is accessing the application over an insecure origin (e.g., plain HTTP over a non-localhost LAN IP), which blocks navigator.clipboard access (DEF-007).

Fix: Access the web application strictly via http://localhost:8000 or http://127.0.0.1:8000, which browsers treat as secure contexts, or instruct users to highlight and copy the text manually.

Verify: Click "Copy Result" while on http://127.0.0.1:8000; verify clipboard contains the scan verdict string.

If that fails: Check browser site permissions to confirm clipboard access is not blocked.

# F-05 — Upstream HTTP 401 Unauthorized / Missing API Key
Symptom: UI displays Invalid or missing VirusTotal API key; backend logs show upstream HTTP 401 Unauthorized responses from VirusTotal.

First check: Run echo $env:VIRUSTOTAL_API_KEY (PowerShell) or inspect the local .env file to verify a 64-character hex string exists.

Likely cause: .env was not created from .env.example, or the key contains invalid whitespace, quotes, or expired credentials.

Fix:

Generate or copy a valid key from virustotal.com profile settings.

Paste into .env as VIRUSTOTAL_API_KEY=<your-virustotal-api-key>.

Restart Uvicorn.

DESTRUCTIVE ACTION WARNING:

STOP! Do NOT run git add . or commit .env to git.

Committing real API keys to version control permanently exposes credentials in git history. If an active key is committed, it must be revoked and rotated immediately on VirusTotal's management portal. Ensure .env remains in .gitignore.

Verify: Execute a live scan for https://example.com; verify API returns HTTP 200 with "verdict": "Safe".

If that fails: Check VirusTotal API quota limits (4 requests/min, 500 requests/day).

## 7. Escalation and the things only a human can decide

- **Data loss suspected → stop.** Do not restart. While this system is strictly stateless and maintains no persistent database or disk-backed user history (CON-04, NFR-SEC-02), suspected unauthorized process memory inspection or unexpected disk writing of scanned URLs must be treated as a data privacy breach. Terminate the Uvicorn process immediately (`CTRL+C`), preserve the existing terminal session transcript and `.env` file, and contact Caleb Fuller before restarting.
- **A third-party service is down →** Check [VirusTotal Status](https://status.virustotal.com/). The system degrades gracefully by failing fast on a 3.0-second socket timeout: the API catches `httpx.TimeoutException`, returns an HTTP 504 Gateway Timeout RFC 7807 error envelope, and the React frontend renders *"Timeout: Analysis took too long"* with an active **[Retry Scan]** button rather than crashing the worker process.
- **A secret may be exposed → rotate first, investigate second.**
  1. Log into your VirusTotal Community account at `https://www.virustotal.com/gui/user/<username>/apikey`.
  2. Revoke the existing key and generate a fresh 64-character hex API key.
  3. Update `.env` with `VIRUSTOTAL_API_KEY=<new_key>` and restart Uvicorn.
  4. Inspect git history via `git log -S "<old_key>" --all` to verify the credential was never committed to version control. If committed, purge git history using `git-filter-repo` before pushing any commits upstream.
- **Contact:** Caleb Fuller (`calebfuller1705`), response time < 4 hours during active project milestones. After Week 14/16 course handoff, custody transfers to the capstone repository archive maintainer.

## 8. Last verified

This runbook was executed end to end on November 11, 2026 by Caleb Fuller on Windows 11 (PowerShell 7, Python 3.14.2, Uvicorn 0.32.0).  
Anything not verified on that date is marked **UNVERIFIED** in the text above.
