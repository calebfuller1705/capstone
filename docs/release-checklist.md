# Release Checklist ? v1.0.0

Total release execution wall-clock time: **11 minutes 40 seconds** (Phases 1-8 verified `2026-11-20`).

---

## Phase 1 ? Freeze (`01:45`)

- [x] Every change intended for v1.0.0 is merged to the default branch (`main`).
- [x] CI is green on that exact commit ? not on "a commit like it."
- [x] The full test suite passes locally *and* in CI (`71 passed`); no skipped tests added this week.
- [x] Every open defect is either fixed or deliberately deferred **in writing**, with an ID, a severity, and a one-line reason (`docs/backlog.md` and `docs/handoff.md` ?5).
- [x] `docs/requirements.md` traceability: every Must-have requirement is marked done, or explicitly moved out of v1.0.0 scope with a note.

## Phase 2 ? Configuration and secrets (`01:30`)

- [x] `.env.example` lists **every** variable the app reads, with a comment per variable: what it does, required or optional, where to get it, safe local value.
- [x] No real secret is in the working tree: `git ls-files | xargs grep -InE '(api[_-]?key|secret|password|token)\s*[:=]'`
- [x] No real secret is in the history either: historical commit `304cde0e` key was rotated and revoked in Week 14 Rep 8 (`docs/handoff.md` ?4 #6).
- [x] `.env`, `.env.*`, `*.pem`, `*.key`, and credential files are in `.gitignore`.
- [x] Every secret the deploy needs exists in `.env` / host secret store, not in a tracked file.

## Phase 3 ? Reproducibility (`02:30`)

- [x] Dependencies are pinned (`requirements.lock` committed with exact versions across all 59 packages).
- [x] The documented setup path runs from a **fresh clone** with no manual steps that are not written down (`02 min 41 s` in Rep 1, `14 min 54 s` full simulation in Rep 12).
- [x] The setup path runs on an environment that is **not your development machine** (verified in GitHub Actions `ubuntu-24.04` runner and isolated clean-room clone).
- [x] `README.md` prerequisites match reality ? including versions (Python `3.12?3.14`, Git, pip/venv, VirusTotal v3 API key).

## Phase 4 ? Version and tag (`01:20`)

- [x] Version number chosen and justified (`v1.0.0`: all Must-have requirements complete, 71/71 tests green, full handoff package verified).
- [x] Version string updated everywhere it appears (`src/api/main.py`, `README.md`, `docs/runbook.md`, `CHANGELOG.md`).
- [x] `CHANGELOG.md` has a dated `[1.0.0]` section: Added / Changed / Fixed / Known issues, with requirement and defect IDs.
- [x] Annotated tag created and pushed: `git tag -a v1.0.0 -m "v1.0.0 ? Complete Phishing URL Scanner capstone release and successor handoff"` then `git push origin v1.0.0`.
- [x] Release published on the tag, with notes a stranger can read, and the built artifact attached if your project ships one.

## Phase 5 ? Legal (`01:10`)

- [x] `LICENSE` exists at the repository root and names a real license (`MIT License`).
- [x] The SPDX identifier appears in `README.md` (`SPDX-License-Identifier: MIT`).
- [x] Third-party licenses inventoried in `THIRD-PARTY-NOTICES.md` across all 59 packages; `MPL-2.0` (`certifi`) and notice obligations documented.
- [x] Institution intellectual-property policy checked: Concordia University Wisconsin student-authored software remains student IP under MIT open-source release.

## Phase 6 ? Deploy and verify (`01:45`)

- [x] Deployed and verified from a clean tag checkout (`v1.0.0`) rather than dirty working files (`docs/deployment.md`).
- [x] Smoke test run against the live server (`GET /health` -> `200 OK`, `POST /scan` -> `200 OK` with `"verdict":"Safe"`).
- [x] Health/liveness check returns success (`{"status":"ok"}`); Uvicorn access/startup logs verified.
- [x] Clean-room successor walkthrough completed (`Rep 12`, `14:54`) and top 3 documentation defects fixed in `README.md`.

## Phase 7 ? Rollback (`00:50`)

- [x] The previous known-good version is identified by tag: `v0.9.0-rc.2`.
- [x] Rollback procedure written as numbered commands in `docs/runbook.md` ?2.4.
- [x] Rollback **rehearsed once**, end to end, with the wall-clock time recorded (`6.43s` in Rep 10, `docs/rollback-transcript.txt`).
- [x] Data question answered honestly: the system is 100% stateless (`CON-04`, `migrations/0001-stateless.sql`), so rolling back code leaves zero database state behind.

## Phase 8 ? Close the loop (`00:50`)

- [x] `docs/deployment.md` updated with actual local & CI deployment procedures.
- [x] Hours logged for this release in `docs/hours-log.csv`.
- [x] Handoff guide (`docs/handoff.md`) updated with all Week 14 findings, groomed top 5 issues, and `v1.0.0` metadata.
- [x] Anything previously remembered instead of read is codified in code guards, tests, `docs/runbook.md`, and `docs/handoff.md` ?4 & ?7.
