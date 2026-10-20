# Definition of Done — URL Security Scanner

Copy this into your repository as `docs/definition-of-done.md` and adapt the
bracketed parts to your stack. Then reference it from your pull-request template
so you cannot merge without seeing it.

## The template (adapt, do not delete lines)

A task is DONE when ALL of the following are true:

1. The acceptance criteria on its requirement are met, verbatim. (`FR-__ AC-__`)
2. At least one automated test in `tests/` exercises the new behavior and passes under `pytest`.
3. The full test suite passes locally (`./script/lint`, `./script/test`, `./script/smoke`) AND in CI on the pushed branch.
4. Errors and edge cases named in the technical specification are handled (malformed URLs, RFC 3986 violations, upstream 429 rate limits, 503 outages, timeouts).
5. The four-pass self-review below is complete; findings fixed or logged.
6. No secrets, credentials, or personal data appear anywhere in the diff (`VIRUSTOTAL_API_KEY` read strictly from environment; zero disk persistence).
7. Any assistant contribution is recorded in `docs/ai-usage.md`.
8. The issue links to its requirement id and has been moved on the board.
9. Docs touched: `README.md`, `docs/runbook.md`, or `.env.example` updated if this
   changed how the system is built, run, or configured.
10. Hours are logged in `docs/hours-log.csv` with a real description.


## The bad version, and what each line costs you

# Definition of Done
Code is written        <- unfalsifiable; that is what makes it a task
It works               <- under what input? on whose machine? which criterion?
Committed to GitHub    <- a commit proves a file changed, not that work finished

Nothing there can be checked by anyone but the author, which means it earns
nothing on a rubric a stranger applies.


## Worked example — URL Security Scanner, FR-2 (integrate VirusTotal API client)

| Check | Evidence |
|---|---|
| 1 | AC-1 unpadded base64url SHA-256 identifier generated; AC-2 `x-apikey` header sent; AC-3 returns engine stats |
| 2 | `tests/unit/test_vt_client.py::test_lookup_200`, `test_lookup_404`, `test_lookup_timeout` |
| 3 | Run #24 green on `feat/fr-2-vt-client` |
| 4 | Upstream 404 (unseen URL), 429 (quota hit), and 5-second socket timeout handled per tech spec §3.2 |
| 5 | Four passes done 2026-10-19; 2 findings fixed, DEF-002 logged and deferred |
| 6 | Key read from `VIRUSTOTAL_API_KEY`; zero disk caching; `git diff --staged` reviewed hunk by hunk |
| 7 | `docs/ai-usage.md` entry 2026-10-19 (client draft, ~35 of 80 lines kept) |
| 8 | Issue #2 closed, labeled `FR-2`, moved to Done on GitHub board |
| 9 | `README.md` prerequisites and `.env.example` verified for `VIRUSTOTAL_API_KEY` |
| 10 | 2.50 h construction + 0.75 h debugging logged 2026-10-19 in `docs/hours-log.csv` |


## The four-pass self-review (check 5, expanded)

**Pass 1 — Diff (mechanical).** `git diff --staged` and `git diff --staged --stat`.
Hunt debug prints, commented-out blocks, files staged by accident, hard-coded
hosts, and TODOs you forgot. Five minutes; finds about half of everything.

**Pass 2 — Stranger (comprehension).** Read from the entry point (`src/api/main.py`) as if you had
never seen it. Flag ambiguous names, functions doing three jobs, magic numbers,
nesting deeper than three.

**Pass 3 — Adversary (destruction).** For every input ask what the worst version
looks like:

| Input | Hostile version |
|---|---|
| target URL field | empty · 10,000 chars · emoji · `javascript:...` · private IP (`127.0.0.1`, `10.0.0.1`) · padded whitespace |
| scan timeout / latency | zero · negative · float precision · upstream timeout > 5.0 s |
| engine statistics | missing keys · 0 engines reported · 100+ engines reported · unexpected category strings |
| network call | slow (>5s) · timed out · 500 · 429 · valid HTTP, HTML error page |
| headers / auth | empty `VIRUSTOTAL_API_KEY` · invalid token · extra whitespace |

Fix now, log a defect, or accept with a written reason. All three are fine.
Silence is not.

**Pass 4 — Contract (traceability).** Read each acceptance criterion out loud and
point at the line of code that satisfies it. No line, no criterion met.

**Adopted:** 2026-09-14 **Revised:** <2026-10-19, Week 10 modifications as in Milestone>
