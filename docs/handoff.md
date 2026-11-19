# Operator & Successor Handoff — Phishing URL Scanner (`v0.9.0-rc.1`)

## 1. System Overview & Architecture
- **Purpose:** Stateless, zero-persistence web interface (`src/static/`) and FastAPI REST service (`src/api/main.py`) that evaluates target URLs against the VirusTotal v3 threat intelligence API (`src/services/vt_client.py`) and returns a normalized `Safe`, `Unsafe`, or `Unknown` verdict without persisting scan history (`CON-04`).
- **Runtime Topology:** Single-process Uvicorn/FastAPI server with a shared `httpx.AsyncClient` connection pool (`timeout=5.0s`, max 100 connections), an in-memory TTL cache (`300s`), and an SSRF guard (`is_private_or_intranet_url`) blocking loopback, RFC-1918 private, link-local, and `.local`/`.internal`/`.lan` destinations with `HTTP 422`.
- **External Dependencies:** VirusTotal v3 REST API (`https://www.virustotal.com/api/v3/urls`). No local database, Redis, or message broker.

## 2. Single Supported Setup, Verification & Run Path (ADR-0006)
- **Prerequisites:** Python `3.12–3.14` (with `venv`; avoid `3.15+` on Windows), Git, and a VirusTotal v3 API key (`64`-character hex string).
- **Bootstrap (`02 min 41 s` verified on fresh clone):**
  ```bash
  git clone [https://github.com/calebfuller1705/capstone.git](https://github.com/calebfuller1705/capstone.git) && cd capstone
  ./script/setup            # creates .venv, installs pinned requirements.lock, copies .env.example -> .env


## Configuration Contract (.env):
VIRUSTOTAL_API_KEY (required): Set in untracked .env (never commit .env). Validate drift anytime with:

Bash
python tools/check_config.py .env.example .env

Optional variables (safe defaults if unset): PORT (8000), APP_BASE_URL (http://127.0.0.1:8000), FRONTEND_URL, SMOKE_EXPECT (Safe).

## Run & Verify:
Start server: ./script/start (or .\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000)

Run automated suite (69 passed, offline mocks): ./script/test (or .\.venv\Scripts\python.exe -m pytest tests/ -v)

Live smoke check: GET /health -> {"status":"ok"}; POST /scan with {"url":"https://example.com"} -> HTTP 200 ("verdict":"Safe").

## 3. First-5-Minute Failure Triage
| Symptom / HTTP Status | Root Cause | Immediate Fix |
| Boot aborts immediately with FATAL: VIRUSTOTAL_API_KEY is not set. | .env missing or VIRUSTOTAL_API_KEY blank (validate_startup_config() in src/api/main.py) | Copy .env.example to .env, set VIRUSTOTAL_API_KEY, and re-run ./script/start. |
| POST /scan returns 502 Bad Gateway (Upstream service error) | Invalid/revoked VirusTotal API key (401) or network block | Verify VIRUSTOTAL_API_KEY in .env against VirusTotal profile; note free-tier keys rotate by issuing a new account key. |
| POST /scan returns 429 Too Many Requests | Exceeded VirusTotal free-tier quota (4 lookups/min, 500/day) | Wait 60 seconds; repeated lookups within 300s are served from the in-memory cache without hitting VirusTotal. |
| POST /scan returns 422 Unprocessable Entity | Malformed URL (> 2048 chars, missing scheme) or SSRF guard triggered (127.0.0.1, 10.x, .local | Expected security boundary (FR-EVAL-01); test with a public http:// or https:// URL. |
POST /scan returns 504 Gateway Timeout | VirusTotal v3 did not respond within 5.0s | Retry once; inspect docs/runbook.md if upstream latency persists. |

## 4. Known Limitations, Security Posture & Where Next
**Known Limitations:**
In-memory cache clears on process restart; VirusTotal free tier caps throughput at 4 req/min; shortened URLs (bit.ly/tinyurl) are evaluated at the shortener domain rather than recursively unshortened (deferred to v1.1 in docs/backlog.md item B-01).

Secret Hygiene: Commit 304cde0e previously exposed a VirusTotal key that was rotated in Rep 8; keep .env untracked and run git status before every commit.

Key Reference Docs: README.md (quickstart), docs/architecture.md (system design), docs/runbook.md (incident response), docs/adr/ (architecture decisions 0001–0006).