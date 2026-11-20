## Log of all Reps from Week 14

## Rep 1 - The Hostile Inventory
| What it is | Why it works on my machine | What a stranger would have to do |
| VIRUSTOTAL_API_KEY in Windows User Environment (Env:) | Set globally in my Windows user environment variables weeks ago, so FastAPI and pytest always found a valid 64-character hex key even when .env was missing or unconfigured. | Register a free VirusTotal v3 account, generate a 64-character API key, copy .env.example to .env, and set VIRUSTOTAL_API_KEY=<key> (or pass it in the shell). |
| Gitignored local .env file (87 bytes) | Exists in the repository root (C:\Users\fulle\capstone\.env) with my local PORT, FRONTEND_URL, and VIRUSTOTAL_API_KEY. Copy .env.example to .env (Copy-Item .env.example .env or cp .env.example .env) and populate the values manually. |
| Python 3.14.2 runtime (.python-version) | Pre-installed on Windows (Python 3.14.2) and added to PATH, matching .python-version (3.14.2). | Install Python 3.12–3.14 (avoiding 3.15+ on Windows due to missing pre-built binary wheels for compiled dependencies). |
| Local .venv/ virtual environment (Python 3.14.2) | Created a few months ago with fastapi, uvicorn, httpx, pydantic, pytest, pytest-asyncio, and flake8 already installed. | Run python -m venv .venv and install pinned packages via pip install -r requirements.lock (or ./script/setup). |
| Git 2.47.0 + .gitattributes LF rules | Installed on Windows (git version 2.47.0.windows.2) and already configured with my GitHub credentials. |Install Git 2.47+ and clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git) into a parent directory. |
| Bash shell for ./script/* (setup, lint, test, build, start, smoke) | Git Bash / WSL is available on my machine to run POSIX #!/usr/bin/env bash scripts directly. | On Windows without WSL/Git Bash, either run scripts through Git Bash (bash ./script/setup) or execute the equivalent PowerShell .venv\Scripts\python.exe commands from README.md. |
| Local Uvicorn server on 127.0.0.1:8000 (PORT=8000) | Hardcoded default in .env.example, script/start, script/smoke, and README.md; port 8000 is normally free on my laptop. | Start Uvicorn explicitly (uvicorn src.api.main:app --port 8000), or override PORT / --port 8001 if another local service occupies port 8000. |
| FRONTEND_URL=http://localhost:8000 CORS origin | Configured in .env.example and README.md so CORSMiddleware allows browser requests from localhost:8000 / 127.0.0.1:8000. | Update FRONTEND_URL in .env (or host environment) to match the exact origin URL if accessing from a custom port or hosted domain. |
| Outbound HTTPS access to [https://www.virustotal.com/api/v3](https://www.virustotal.com/api/v3) | My laptop has unrestricted outbound internet access and a non-exhausted free-tier VirusTotal v3 quota (4 req/min, 500 req/day). | Ensure outbound port 443 access to virustotal.com for live scans (offline unit/integration tests use httpx.MockTransport and CI test keys). |
| PowerShell curl alias (Invoke-WebRequest) vs curl.exe | I know to use curl.exe or Invoke-RestMethod on Windows PowerShell rather than plain curl -X POST. | On Windows PowerShell, invoke curl.exe (not curl) when running the README.md CLI verification commands, or run them in Bash. |


## Rep 2 - Pin what Floats
| Direct Dependency (requirements.txt) | Constraint Type in requirements.txt | Pinned Lock Version (requirements.lock) | Notes / Compatibility Risk |
| fastapi | Floating (>=0.115.0) | fastapi==0.143.2 (with starlette==1.8.0) | Unbounded >= allows major/minor Starlette jumps; Starlette 1.8.0 already emits HTTP_422_UNPROCESSABLE_ENTITY deprecation warnings in test logs. |
| uvicorn | Floating (>=0.31.0) | "uvicorn==0.54.0 (with h11==0.16.0, httptools==0.9.0)" | ASGI server flags or worker lifecycle defaults can shift across minor releases if unpinned. |
| pydantic | Floating (>=2.9.2) | pydantic==2.14.1 (with pydantic_core==2.50.1) | Relies on compiled Rust pydantic_core wheels; floating into a future major version (3.x) would break ScanRequest field validators. |
| httpx | Floating (>=0.27.2) | httpx==0.28.1 (with httpcore==1.0.9) | 0.28.x already deprecated app= transport shortcuts (StarletteDeprecationWarning in TestClient); 1.0.0 would break MockTransport or client kwargs. |
| slowapi | Floating (>=0.1.9) | slowapi==0.1.10 (with limits==5.8.0) | Wraps Starlette request state for per-IP rate limiting; sensitive to Starlette/FastAPI middleware signature changes. |
| python-dotenv | Floating (>=1.0.0) | python-dotenv==1.2.4 | Loads .env overrides at startup; low churn, but pinned in requirements.lock for deterministic parsing. |
| pytest | Floating (>=8.3.3) | pytest==9.1.1 (with pluggy==1.7.0) | Already crossed major version 8 -> 9 in the lockfile; future major versions (10.x) can alter async fixture/plugin hooks. |
| pytest-asyncio | Floating (>=0.24.0) | pytest-asyncio==1.4.1.post1 | Already crossed 0.24 -> 1.4 (Mode.STRICT default); floating across major versions broke async event-loop scope behavior before pinning. |
| flake8 | Floating (>=7.1.1) | flake8==7.4.1 (pycodestyle==2.15.0, pyflakes==4.0.3) | New lint rules in 8.x could fail ./script/lint in CI on previously clean code. |


## Rep 4 Summary - Make Required Config Fail Loudly
Before: Uvicorn booted silently without VIRUSTOTAL_API_KEY and passed GET /health (200 OK), failing only later inside scan_url() (src/api/main.py:101) with HTTP 500: Server configuration error: missing VIRUSTOTAL_API_KEY when a user submitted POST /scan.

After: FastAPI's lifespan() hook calls validate_startup_config() (and ./script/start checks .env), aborting boot immediately with FATAL: VIRUSTOTAL_API_KEY is not set. Copy .env.example to .env and fill it in, then re-run. See README.md -> "Configuration".

# Rep 5 Summary - Amnesia Test
Fresh-Clone Amnesia Test (2026-11-18, $env:TEMP\capstone-amnesia-test):

Cloned [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git) into an isolated temporary directory, copied .env.example to .env, created a clean .venv, installed all 37 pinned packages from requirements.lock, verified tools/check_config.py .env.example .env (0 required missing, 0 undocumented), ran pytest tests/ -q (69 passed in 6.60s), booted Uvicorn on port 8011, and verified GET /health ({"status":"ok"}) and POST /scan ("verdict":"Safe").

Total wall-clock time: 02 min 41.41 s (clone → running → smoke verified).

# Rep 7 - The Secret Hunt
| Location | Finding Type | Redacted Value / Entropy | Classification | Action Required |
| Commit 304cde0e (.env.example) | 64-char hex VIRUSTOTAL_API_KEY | 750524a7135eea8e... (H = 3.80) | Real historical secret | Revoke in VirusTotal portal & rotate to a new key (Rep 8) |
| .github/workflows/ci.yml:52 | Mock CI token | ci-smoke-test-ke... (H = 3.18) | Safe synthetic fixture | None (offline CI mock key) |
| tests/integration/test_vt_contracts.py:9 | Test fixture token | test_api_key_000... (H = 1.74) | Safe synthetic fixture | None (unit/integration mock) |
| "README.md:105,110 & docs/runbook.md:138" | Documentation placeholder | <your-api-key>... (H = 3.52–3.98) | Safe doc placeholder | None |
| Working tree (all tracked files) | Active real secrets | None (0 real findings) | Clean | ".gitignore hardened for .env.*, *.pem, *.key"|

# Rep 8 - Rotate One Key on Purpose

Credential Rotated: VIRUSTOTAL_API_KEY (replaced exposed historical key 750524a7135eea8e... found in commit 304cde0e with a fresh VirusTotal v3 API key stored strictly in untracked local .env).

Verification: tools/check_config.py .env.example .env exited 0 (0 required missing, 4 warnings, 0 undocumented), git status remained clean, and POST /scan ([https://example.com](https://example.com)) returned 200 OK (verdict: Safe, total_engines: 93).

# Auditor Results
- **Target Persona:** Stranger who is new to this stack
- **Monday Baseline Score:** ~50 / 100 (unpinned shell scripts, unverified rollback timing, 3 copy-paste setup defects in `README.md`, undocumented bus-factor traps)
- **Friday `v1.0.0` Final Score:** **95 / 100 — Ready to hand off**
  - Environment reproducibility: **25 / 25** (complete)
  - Configuration and secrets: **15 / 20** (working tree clean; historical commit `304cde0e` key rotated/revoked in Rep 8 and documented in `docs/handoff.md` §4 #6)
  - Documentation completeness: **20 / 20** (complete)
  - Issue and backlog hygiene: **15 / 15** (complete)
  - Knowledge only in your head: **20 / 20** (complete)

### Artifacts Shipped for `v1.0.0`
- **`docs/handoff.md`:** Complete 8-section successor handoff guide (`§0`–`§8`, zero placeholders) integrating the Rep 3 config contract, Rep 8 VirusTotal key rotation procedure, Rep 9 `MIT` / `THIRD-PARTY-NOTICES.md` license audit, Rep 10 `6.43s` rollback drill, Rep 11 bus-factor register, and Rep 12 clean-room documentation fixes.
- **`docs/backlog.md`:** Top 5 open issues groomed with requirement/defect IDs, acceptance criteria, and file paths (`ISSUE-DOC-04` labeled `good-first-issue` for Week 1 onboarding).
- **`docs/deployment.md` & `docs/release-checklist.md`:** Walked all 8 release phases (`11m 40s` total) and pushed annotated tag **`v1.0.0`**.