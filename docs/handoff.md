# Handoff Guide — Phishing URL Scanner

Audience: the engineer who inherits this project and **cannot ask you a question.**

---

## 0. Thirty-second orientation

- **What it is:** A stateless, zero-persistence FastAPI web application and REST service that evaluates URLs against the VirusTotal v3 threat intelligence API to return real-time `Safe`, `Unsafe`, or `Unknown` verdicts without storing browsing history (`CON-04`).
- **Who uses it:** Corporate employees, IT helpdesk staff, and security reviewers verifying suspicious links from emails or chat messages without leaking internal destinations to public web forms or server logs.
- **Status as of 2026-11-20:** Shipped, version `v1.0.0`.
- **Deployed at:** Not deployed to a hosted cloud URL — runs locally on `http://127.0.0.1:8000` (see `docs/deployment.md` and `README.md`).
- **Start here:** `README.md` to run it, `docs/architecture.md` to understand it, this file to take it over.

## 1. Day one — get it running (target: under 30 minutes)

| Step | Command | Expected result | If it fails |
|---|---|---|---|
| 1 | `git clone https://github.com/calebfuller1705/capstone.git && cd capstone` | 53 tracked files cloned into `./capstone` | Verify Git is installed (`git --version`) and do not copy Markdown link brackets around the URL (`ISSUE-DOC-01`). |
| 2 | `./script/setup` (Git Bash/Linux/macOS) or `python -m venv .venv && .\.venv\Scripts\python.exe -m pip install -r requirements.lock` (PowerShell) | ends with `Successfully installed ... fastapi-0.143.2 ... uvicorn-0.54.0` (~12s) | Ensure Python is `3.12–3.14` (Python `3.15+` on Windows lacks pre-built `pydantic-core` wheels). |
| 3 | `Copy-Item .env.example .env` (PowerShell) or `cp .env.example .env` (Bash), then set `VIRUSTOTAL_API_KEY` | `.env` filled from `.env.example` and passes `python tools/check_config.py .env.example .env` | See §3 for VirusTotal key acquisition and ownership; `validate_startup_config()` blocks blank or placeholder keys. |
| 4 | `./script/start` (Bash) or `.\.venv\Scripts\python.exe -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000` (PowerShell) | `INFO: Uvicorn running on http://127.0.0.1:8000` and `Application startup complete.` | See `docs/runbook.md` §2 (port `8000` already in use `Errno 10048`, or missing `VIRUSTOTAL_API_KEY`). |
| 5 | `.\.venv\Scripts\python.exe -m pytest tests/ -v` (or `./script/test`) and live `POST /scan` with `{"url":"https://example.com"}` | 71 tests pass in ~8s (`exit code 0`), plus live `/scan` returns `HTTP 200` with `"verdict":"Safe"` | Check `docs/runbook.md` §3 (`401`/`502` invalid key, `429` free-tier rate limit, or `504` upstream timeout). |

## 2. Week one — a ramp that ends in a merged change

1. **Read** `docs/architecture.md` (20 min) and the ADR index in `docs/adr/README.md` (`ADR-0001` through `ADR-0006`).
2. **Trace one request** end to end: **submit a public URL and receive a normalized threat verdict**.
   Files in order: `src/static/index.html` + `src/static/app.js` (`submitScan()`) → `src/api/schemas.py` (`ScanRequest`) → `src/api/main.py` (`scan_url()` + `is_private_or_intranet_url()`) → `src/services/vt_client.py` (`fetch_url_report()`).
3. **Fix the starter issue:** `ISSUE-DOC-04` (`docs/backlog.md` §1) — small, real, has testable acceptance criteria, and touches 2 files (`src/api/main.py` and `tests/unit/test_health.py`). It is labeled `good-first-issue` on purpose.
4. **Ship it:** branch (`git checkout -b fix/issue-doc-04-favicon-route`), test (`pytest tests/ -v` and `flake8 src/ tests/`), open a pull request, watch `.github/workflows/ci.yml` go green, merge, and tag if needed.

## 3. Accounts, keys, and who pays for what

| Thing | Where it lives | Currently owned by | Cost | Rotation / transfer step |
|---|---|---|---|---|
| Source repository | `https://github.com/calebfuller1705/capstone` | Caleb Fuller (`calebfuller1705`) | Free tier ($0/mo) | Transfer GitHub repository ownership in Settings → General → Transfer ownership, then verify `.github/workflows/ci.yml` permissions. |
| Deploy target | Local workstation / classroom evaluation host (`http://127.0.0.1:8000`; see `docs/deployment.md`) | Caleb Fuller (local clone) | $0/mo (self-hosted local process) | Clone tagged release (`git checkout v1.0.0`) onto successor host and start single-worker Uvicorn process. |
| Database | None — strictly stateless zero-persistence architecture (`CON-04`, `ADR-0005`, `migrations/0001-stateless.sql`) | Not applicable | $0/mo | Backups: None required; all cache state (`300s` TTL) lives in process RAM and resets cleanly on restart. |
| `VIRUSTOTAL_API_KEY` | Local untracked `.env` (CI uses dummy `ci-smoke-test-key` in `.github/workflows/ci.yml`) | Caleb Fuller (personal VirusTotal free account) | Free public tier ($0/mo; 4 lookups/min, 500/day) | Register a new free VirusTotal v3 account (`virustotal.com` → Sign up → Profile → API Key), place the new 64-char hex key in `.env`, verify `POST /scan` returns `HTTP 200`, and deactivate the old account key AFTER the new one is live (rehearsed in Rep 8). |
| Model / LLM API keys | None — application makes zero runtime LLM/model calls | Not applicable | $0/mo | Not applicable (see §6). |

> Every row with a person's name in it is a liability. Before this project is
> truly handed off, every one of those names must change.

## 4. Landmines — things that will bite you

1. **POSIX `./script/*` scripts do not execute natively in Windows PowerShell.** Actually: `./script/setup`, `./script/start`, `./script/test`, and `./script/smoke` use `#!/usr/bin/env bash` (`ADR-0006`). Do: Run `./script/*` inside **Git Bash (`MINGW64`)** on Windows, or invoke `.\.venv\Scripts\python.exe` directly in PowerShell as documented in `README.md` (`ISSUE-DOC-02`).
2. **Python `3.15+` fails dependency installation on Windows.** Actually: `pydantic-core==2.50.1` lacks pre-built Windows binary wheels for Python `3.15+` and falls back to compiling Rust/C extensions (`Microsoft Visual C++ 14.0 required`). Do: Pin Python `3.12–3.14` (`.python-version` specifies `3.14`), enforced at runtime by `tools/check_config.py`.
3. **Scaling past 1 Uvicorn worker breaks rate-limit protection and wastes VirusTotal quota.** Actually: The in-memory `300s` TTL cache (`src/services/vt_client.py`) and request state live in per-process RAM, and VirusTotal's free tier allows only 4 requests/minute. Do: Never pass `--workers > 1` in `docs/runbook.md` §1.
4. **VirusTotal public free-tier accounts have no single-click "Regenerate Key" button.** Actually: Rotating a compromised key requires provisioning a new VirusTotal account key first, updating `.env`, and retiring the old key afterward. Do: Follow the zero-downtime key rotation procedure in `docs/runbook.md` §3.2 (rehearsed in Rep 8).
5. **`migrations/0001-stateless.sql` is intentionally empty (comments only).** Actually: Privacy constraint `CON-04` and `ADR-0005` prohibit any database tables or disk persistence of scanned URLs. Do: Do not delete `migrations/0001-stateless.sql` or add `CREATE TABLE` DDL; `tests/unit/test_tribal_guards.py` fails CI if violated.
6. **Historical commit `304cde0e` triggers secret-scanner alerts on an already-revoked key.** Actually: Commit `304cde0e` contained an early VirusTotal key (`750524a7135eea8e...`) that was revoked and rotated during Week 14 Rep 8. Do: Treat `304cde0e` as a known rotated historical artifact; never rewrite published `main` history unless policy mandates `git-filter-repo`.
7. **Placeholder `VIRUSTOTAL_API_KEY` values intentionally abort server startup.** Actually: `validate_startup_config()` in `src/api/main.py` rejects template/mock strings (`YourVirusTotalAPIKeyHere`, `ci-smoke-test-key`, etc.) unless `PYTEST_CURRENT_TEST` or `CI=true` is set. Do: Paste a real 64-character hex VirusTotal key into `.env` before running locally (`tests/unit/test_tribal_guards.py`).

## 5. Known defects and deferred work

Pull the live list from `docs/backlog.md` and `docs/defect-log.md`; this is the shape of it as of `2026-11-20`.

| ID | Severity | Summary | Why it is still open |
|---|---|---|---|
| `B-01` / `KI-001` | Low | Shortened URLs (`bit.ly`, `tinyurl.com`) evaluate the shortener domain rather than recursively following redirects to the final destination URL. | Deliberately deferred to `v1.1` (`CR-003`) to prevent redirect-loop SSRF vectors and stay within the 5.0s upstream timeout budget. |
| `B-04` / `FR-SYS-02` | Low | Server-side file logging of scan verdicts and upstream API error codes is not implemented. | Deliberately deferred to `v1.1` (`CR-005`) because disk logging conflicts with zero-retention privacy constraint `CON-04` and requires log rotation infrastructure. |
| `ISSUE-DOC-04` | Low | Browser requests to `GET /favicon.ico` log an HTTP `404 Not Found` line in Uvicorn console output. | Cosmetic noise only (`good-first-issue` starter task for successor week-one onboarding in §2). |
| `B-05` | Medium | `requirements.lock` pins `httpx==0.28.1` and `starlette==1.8.0`, emitting a `StarletteDeprecationWarning` about `httpx2` / `HTTP_422_UNPROCESSABLE_CONTENT` during `pytest`. | Deferred to `v1.1` dependency refresh so `v1.0.0` stays pinned to the verified `requirements.lock` matrix. |
| `B-06` | Medium | The `300s` in-memory URL verdict cache has no bounded max-size eviction (`LRU`) if a high-volume burst submits thousands of distinct URLs. | Deferred to `v1.1`; current single-workstation usage is bounded by VirusTotal's `4 req/min` (`500/day`) quota. |

## 6. AI dependencies

This section does not apply at runtime: **Phishing URL Scanner makes zero runtime calls to any AI, LLM, or machine-learning model.** All URL threat verdicts are deterministic aggregations of VirusTotal v3 engine counts (`src/services/vt_client.py`). Development-time AI assistance is logged separately in `docs/ai-usage.md`.

## 7. What only I know (bus-factor register)

| Knowledge | Consequence if lost | Now written down at |
|---|---|---|
| Outbound license is MIT (`SPDX-License-Identifier: MIT`), and `certifi` is `MPL-2.0` while 21 dependencies store PEP 639 licenses in `.dist-info/licenses/` | Successor could misstate license compatibility or violate notice retention during redistribution | `LICENSE`, `README.md`, and `THIRD-PARTY-NOTICES.md` |
| Timed rollback procedure to a known-good annotated Git tag (`6.43s` verified recovery in Rep 10) | Incident responder could waste minutes manually reverting files or corrupting untracked `.env` | `docs/runbook.md` §2.4 and `docs/rollback-transcript.txt` |
| Configuration contract validator (`tools/check_config.py`) checks `.env` keys against `.env.example` and enforces Python `3.12–3.14` | Silent misconfiguration or mysterious Windows wheel build failures on Python `3.15+` | `README.md` §Prerequisites & §Configuration, plus `tools/check_config.py` |
| Duplicate `[url](url)` Markdown autolinks inside fenced code blocks broke verbatim copy-paste setup (`ISSUE-DOC-01`–`03` found in Rep 12 clean-room simulation) | New developers stall within 2 minutes on `git clone`, `uvicorn`, and PowerShell `Invoke-RestMethod` verification | Fixed in `README.md` and recorded in `docs/defect-log.md` |
| CI smoke test passes `VIRUSTOTAL_API_KEY="ci-smoke-test-key"` with `CI=true`, whereas local startup rejects placeholder keys | Modifying `validate_startup_config()` without preserving the `CI=true` check breaks `.github/workflows/ci.yml` | `src/api/main.py` (`validate_startup_config`) and `tests/unit/test_tribal_guards.py` |

## 8. If nobody picks this up

- **Deployment & infrastructure:** Because the application runs locally on demand (`http://127.0.0.1:8000`) with zero cloud servers, databases, or paid subscriptions, nothing remains running or incurs billing if abandoned.
- **Data & accounts:** Zero user data is stored anywhere (`CON-04`). Caleb Fuller will deactivate the personal VirusTotal free-tier API key associated with this project after final Fall 2026 grading completes (`2026-12-18`).
- **Repository archival & deprecation notice:** If no successor adopts the repository by `2027-01-15`, Caleb Fuller (`calebfuller1705`) will archive `https://github.com/calebfuller1705/capstone` on GitHub (Settings → Archive this repository) and prepend the following notice to `README.md`:
  > **ARCHIVED (`2027-01-15`):** This Fall 2026 senior capstone repository is archived and unmaintained. Threat intelligence schemas against VirusTotal v3 may drift over time; fork and update `requirements.lock` before use.

---

**Maintainer of record:** Caleb Fuller · **Handoff date:** 2026-11-20 · **This file last verified against a real run on:** 2026-11-20