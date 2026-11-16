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
| Date | 2026-11-15 |
| Tester name | Caleb Fuller (Solo Dress Rehearsal) |
| Machine / OS | Personal Laptop / Windows 11 |
| Repository URL and commit SHA | `https://github.com/calebfuller1705/capstone.git` (`09e3db0`) || Time to acceptance action | 20 minutes and 43 seconds|
| Solo friction found | None. |

---

## Part B: Graded Clean-Machine Run

### 1. Run header

| Field | Value |
|---|---|
| Date | 2026-11-15 |
| Tester name | Jacob Miller |
| Tester's background | Roommate; Education major with some background in the basics of CS |
| Machine / OS | Personal Laptop / Windows 11|
| Environment type | fresh container / cloud dev environment / borrowed laptop / new user account |
| Repository URL and commit SHA | `https://github.com/calebfuller1705/capstone.git` (`09e3db0`) |
| Observer | Caleb Fuller |

### 2. Stopwatch

| Checkpoint | Target | Actual | Notes |
|---|---|---|---|
| Repository opened | 0:00 | 0:00 | N/A |
| Prerequisites installed / confirmed | 10:00 | 12:30 | N/A |
| Dependencies installed | 13:00 | 18:00 | N/A |
| Configuration complete (`.env` filled) | 17:00 | 22:00 | N/A |
| Application running | 20:00 | Not finished | Not finished |
| Acceptance action completed | 25:00 | | |
| Test suite run and green | 30:00 | | |

### 3. The acceptance action

> **Acceptance action:** Clone the repository using only `README.md`, configure `.env`, start the local Uvicorn server, submit `https://example.com` via the web UI at `http://127.0.0.1:8000` (or `POST /scan`), confirm a `"Safe"` verdict is returned, and run `pytest tests/ -v` with all 60 tests passing.

- **Result:** FAIL
- **Stopped at checkpoint (if FAIL):** Application running

### 4. Friction log

# | Time | What the tester did or said | Root cause in the docs | Severity
1 | Before start of timer | Cloned repo inside a pre-created capstone directory, ending up in C:\Users\capst\capstone\capstone. | README.md Install Step 1 did not warn users to clone from a parent folder rather than creating capstone manually first. | slow
2 | ~8:00 | Installed Python 3.15; pip install -r requirements.txt crashed with error: Microsoft Visual C++ 14.0 or greater is required building pyyaml. | README.md Prerequisites stated supports Python 3.12+ instead of capping at 3.14, and PyYAML (only used by doc_lint.py) lacked cp315 Windows wheels. | blocker
3 | ~18:00 | .\.venv\Scripts\pip threw ObjectNotFound when .venv creation hadn't completed or pip.exe wasn't resolved. | README.md Install Step 3 invoked .\.venv\Scripts\pip directly instead of the safer .\.venv\Scripts\python.exe -m pip. | slow
4 | ~24:00 | Ran python -m uvicorn src.api.main:app --reload; server crashed with ModuleNotFoundError: No module named 'dotenv' from global Python315. | README.md listed bare python -m uvicorn before .venv activation, AND python-dotenv was missing from requirements.txt. | blocker

*Severity definitions: **blocker** = could not proceed without help; **slow** = proceeded but lost time or guessed; **cosmetic** = noticed something wrong that did not cost time.*

### 5. Fixes applied

| Friction # | Document changed | Change made | Commit |
|---|---|---|---|
| 1 | `README.md` | Added explicit note under Install Step 1 warning users to clone from a parent workspace folder rather than manually creating an empty `capstone` folder first (preventing `capstone\capstone` double-nesting). | `3fbc676` |
| 2 | `README.md`, `requirements.txt` | Pinned supported Python versions in Prerequisites to `3.12–3.14` (explicitly excluding `3.15+` on Windows), deduplicated `python-dotenv`, and switched `uvicorn[standard]` to `uvicorn` so `PyYAML` C-extensions do not fail to compile without Visual C++ Build Tools. | `3fbc676` |
| 3 | `README.md` | Standardized Install Step 3 commands on `.\.venv\Scripts\python.exe -m pip` instead of invoking `.\.venv\Scripts\pip` directly. | `3fbc676` |
| 4 | `README.md` | Removed the unactivated bare `python -m uvicorn` command under Running the Application so testers always invoke `.\.venv\Scripts\python.exe -m uvicorn` rather than global Python. | `3fbc676` |

### 6. Re-run

| Field | Value |
|---|---|
| Date of re-run | 2026-11-16 |
| Tester | Jacob Miller |
| Time to acceptance action | 33:28 |
| Remaining blockers | None. |

### 7. Signed statement

> On 2026-11-16, Jacob Miller cloned this repository onto his personal laptop and, using only the documentation in this repository, reached the acceptance action (running the Phishing URL Scanner locally, verifying a `"Safe"` scan verdict for `https://example.com`, and passing all 60 automated tests) in ~33 minutes without assistance from the author.