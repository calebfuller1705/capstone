# CR-005 — Scope Cut: Defer Server-Side Action Logging (FR-SYS-02)

| Field | Value |
|---|---|
| Raised by | Caleb Fuller, Week 12 Capacity Audit |
| Date raised | 2026-11-06 |
| Baseline affected | spec-baseline-v1.0, FR-SYS-02 |
| Request | "Cut FR-SYS-02 from v1.0 scope to balance the remaining build capacity against non-negotiable documentation and deployment deadlines." |

## Mandatory Fields

- **What:** FR-SYS-02 (Action Logging)
- **Why:** 5.0 h estimated; 10.0 h remain; Week 13 documentation (14.0 h) and Week 14 deployment (14.0 h) are not optional
- **Where it went:** docs/backlog.md B-04 , sized at 5.0 h, acceptance criteria retained intact
- **Reader must know:** Scanned URLs and risk scores will not be written to server disk or local log files; the application remains strictly stateless under CON-04 and NFR-SEC-02

## Impact analysis

- **Cost:** -5.0 h build/test/doc; restores remaining build workload to 10.0 h (matching the 10.0 h capacity ceiling)
- **Blast radius:** removes local file I/O from backend dispatch in `src/api/main.py`; touches `docs/requirements.md`, `docs/backlog.md`, and `CHANGELOG.md`; eliminates potential disk-persistence leakage
- **Risk:** accept -> IT helpdesk analysts cannot retroactively inspect local log files to track internal scan history; refuse -> project runs out of hours in Weeks 13–14, forcing an incomplete documentation set or failed cloud deployment

## Decision

| Field | Value |
|---|---|
| Disposition | DEFER -> docs/backlog.md as B-04, "post-handoff v1.1, ~5.0 h, requires dedicated audit database" |
| Decided by | Caleb Fuller, 2026-11-06 |
| Rationale | Arithmetic forces a 5.0 h scope reduction. Cutting FR-SYS-02 protects core end-user validation (FR-EVAL-04, FR-EVAL-02) while eliminating an architectural contradiction with zero-persistence constraint CON-04. |

## Applied

- [x] FR-SYS-02 marked as Deferred in docs/requirements.md (row retained)
- [x] Backlog entry B-04 created with original acceptance criteria in docs/backlog.md
- [x] Row added to the change table in CHANGELOG.md
- [x] Traces: documented in Week-12 reps log