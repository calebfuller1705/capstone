# Specification Baseline v1.0

**Declared:** 2026-10-14  
**Declared by:** Caleb Fuller, author and moderator of record  
**Git tag:** `spec-baseline-v1.0`  
**Commit:** `HEAD` (run `git rev-parse --short HEAD` after committing rework)  
**Review report:** `docs/review/2026-10-14-design-review-report.md`  

---

## Artifacts Frozen at This Baseline

| Artifact | Repo Path | Version | State at Freeze |
|---|---|---|---|
| Project Charter | `docs/charter.md` | 1.1 | Approved |
| Requirements Specification | `docs/requirements.md` | 1.0 | Approved |
| Technical Specification | `docs/architecture.md` | 0.2 | Approved with rework |
| Architecture Decision Records | `docs/adr/ADR-001..0004` | 1.0 | Approved |
| Work Breakdown and Schedule | `docs/plan.md` | 1.0 | Approved |
| Risk Register | `docs/risk-register.md` | 1.0 | Approved |
| Definition of Done | `docs/definition-of-done.md` | 1.0 | Approved |

---

## Open Items Carried Past the Baseline

| ID | Description | Disposition | Due |
|---|---|---|---|
| **DR-010** | VirusTotal API v3 cached report lookup (`GET /api/v3/urls/{id}`) vs. fresh submission (`POST /api/v3/urls`) | Deferred via CR-001 | Week 10 (Iteration 1) |

---

## What This Means From Today

As of tag `spec-baseline-v1.0`, the system scope, interface schemas, stateless constraints (`CON-04`, `NFR-SEC-02`), and 57.0-hour build plan are formally frozen and can only be altered through an approved Change Request in `docs/change-requests/`. Implementation code in `src/`, test scripts in `tests/`, and local working notes are deliberately unfrozen to support rapid iteration during Week 9. If the running application in Week 16 diverges from this specification, the difference must trace directly to an approved CR in `CHANGELOG.md`, not undocumented drift.