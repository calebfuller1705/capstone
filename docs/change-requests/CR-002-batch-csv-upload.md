# CR-002 — Advisor asks for batch CSV URL file upload

| Field | Value |
|---|---|
| Raised by | friend, Week 12 check-in |
| Date raised | 2026-11-06 |
| Baseline affected | spec-baseline-v1.0 |
| Request | "Security analysts need to upload a CSV file with 100+ URLs to scan all of them in bulk." |

## Impact analysis

- **Cost:** 6 build + 3 test + 1 doc = 10 h; 26.5 h remain before the Week-14 freeze
- **Blast radius:** new FR; `src/api/main.py`, `src/services/vt_client.py`, and `src/static/app.js`; one new multipart endpoint `POST /scan/batch`; requires an asynchronous task queue (Celery/Redis) to avoid exhausting VirusTotal's 4 req/min rate limit; invalidates latency benchmarks in `docs/performance.md`; modifies `docs/architecture.md` and README.md
- **Risk:** accept -> 10 of 26.5 remaining hours go to rate-limiting infrastructure, starving the deployment and hardening buffer in Weeks 13-14, or immediately triggers upstream HTTP 429 quota exhaustion during demos; refuse -> analysts with bulk lists must invoke the single-URL REST endpoint via custom shell script

## Decision

| Field | Value |
|---|---|
| Disposition | DEFER -> docs/backlog.md as B-03, "post-handoff v1.1, ~10 h, requires async queue and paid VT tier" |
| Decided by | Caleb Fuller, 2026-11-06 |
| Rationale | The feature is valuable for enterprise workflows, but unviable under the current 4 req/min public API tier and remaining budget. Deferring keeps it findable, sized, and tied to clear prerequisites. |

## Applied

- [x] Requirements specification unchanged; bulk ingestion remains out of scope for v1.0
- [x] Backlog entry B-03 written with the 10 h estimate and rate-limit prerequisite
- [x] Row added to the change table at the top of CHANGELOG.md
- [x] Traces: documented in Week-12 status memo and explained to friend who looks at the project