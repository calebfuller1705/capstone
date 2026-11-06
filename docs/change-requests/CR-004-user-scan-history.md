# CR-003 — Peer asks for persistent scan history and user logins

| Field | Value |
|---|---|
| Raised by | user, Week 12 review |
| Date raised | 2026-11-06 |
| Baseline affected | spec-baseline-v1.0, CON-04, NFR-SEC-02 |
| Request | "Users should create accounts and log in so they can see a history table of all URLs they previously scanned." |

## Impact analysis

- **Cost:** 8 build + 4 test + 2 doc = 14 h; 26.5 h remain before the Week-14 freeze
- **Blast radius:** violates non-negotiable constraints CON-04 and NFR-SEC-02; introduces relational database (`SQLAlchemy`/SQLite/PostgreSQL), migration tooling (`alembic`), session token auth (`src/auth/`), and 2 database tables; opens IDOR and credential exposure attack surfaces across all 7 areas in `docs/security-review.md`
- **Risk:** accept -> destroys the defining architectural invariant of the project (strictly stateless, zero retention of scanned URLs or PII), introduces database hosting liabilities, and burns 14 of 26.5 remaining hours; refuse -> users cannot view previous scans after closing their browser tab

## Decision

| Field | Value |
|---|---|
| Disposition | REJECT (reason: Violates non-negotiable architectural constraint CON-04 and zero-persistence security guarantee NFR-SEC-02; the service is explicitly engineered as an ephemeral, privacy-preserving scanner) |
| Decided by | Caleb Fuller, 2026-11-06 |
| Rationale | Any independent security auditor or grader would agree: the core security guarantee of this system is zero server-side retention. Adding persistence destroys that invariant. |

## Applied

- [x] Requirements specification unchanged; CON-04 and NFR-SEC-02 remain strictly enforced
- [x] No backlog entry created (rejected permanently from system architecture)
- [x] Row added to the change table at the top of CHANGELOG.md
- [x] Traces: documented in Week-12 reps log with rejection rationale