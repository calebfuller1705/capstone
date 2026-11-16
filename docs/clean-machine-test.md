# The Clean-Machine Test — Protocol and Observer Log

## Rules

1. **A clean machine.** A fresh container, a fresh cloud development environment, a classmate's laptop, or a new user account on your own machine. Nothing your project installed is already there.
2. **A real tester who is not you.** Someone who has never run this project.
3. **You are silent.** You may watch. You may not speak, point, type, or "just fix that one thing." The moment you help, the test is over and the result is void.
4. **The docs are the only input.** The tester gets the repository URL and nothing else. No verbal setup, no Discord message, no "oh you also need to…".
5. **The clock runs** from the moment the tester opens the repository to the moment they complete the acceptance action in section 3. Stop the clock at 60 minutes and record the failure.
6. **Every stumble gets logged**, including the ones that are the tester's fault. Especially those.

---

## Part A: Solo Dress Rehearsal (Pre-Test)

| Field | Value |
|---|---|
| Date | 2026-11-16 |
| Tester name | Caleb Fuller (Solo Dress Rehearsal) |
| Machine / OS / Environment | Personal Laptop / Windows 11 /|
| Repository URL and commit SHA | `https://github.com/calebfuller1705/capstone.git` (`09e3db0`) || Time to acceptance action | 20 minutes and 43 seconds|
| Solo friction found | None. |

---

## Part B: Graded Clean-Machine Run

### 1. Run header

| Field | Value |
|---|---|
| Date | 2026-11-16 |
| Tester name | |
| Tester's background | |
| Machine / OS / architecture | |
| Environment type | fresh container / cloud dev environment / borrowed laptop / new user account |
| Repository URL and commit SHA | `https://github.com/calebfuller1705/capstone.git` (`09e3db0`) |
| Observer (you) | Caleb Fuller |

### 2. Stopwatch

| Checkpoint | Target | Actual | Notes |
|---|---|---|---|
| Repository opened | 0:00 | | |
| Prerequisites installed / confirmed | 0:05 | | |
| Dependencies installed | 0:08 | | |
| Configuration complete (`.env` filled) | 0:11 | | |
| Application running | 0:13 | | |
| **Acceptance action completed** | **0:15** | | |
| Test suite run and green | 0:20 | | |

### 3. The acceptance action

> **Acceptance action:** Clone the repository using only `README.md`, configure `.env`, start the local Uvicorn server, submit `https://example.com` via the web UI at `http://127.0.0.1:8000` (or `POST /scan`), confirm a `"Safe"` verdict is returned, and run `pytest tests/ -v` with all 60 tests passing.

- **Result:** PASS / FAIL
- **Stopped at checkpoint (if FAIL):**

### 4. Friction log

| # | Time | What the tester did or said | Root cause in the docs | Severity (blocker / slow / cosmetic) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

*Severity definitions: **blocker** = could not proceed without help; **slow** = proceeded but lost time or guessed; **cosmetic** = noticed something wrong that did not cost time.*

### 5. Fixes applied

| Friction # | Document changed | Change made | Commit |
|---|---|---|---|
| | | | |

### 6. Re-run

| Field | Value |
|---|---|
| Date of re-run | |
| Tester | |
| Time to acceptance action | |
| Remaining blockers | |

### 7. Signed statement

> On {{date}}, {{tester name}} cloned this repository onto {{machine}} and, using only the documentation in this repository, reached the acceptance action (running the Phishing URL Scanner locally, verifying a `"Safe"` scan verdict for `https://example.com`, and passing all 60 automated tests) in {{N}} minutes without assistance from the author.