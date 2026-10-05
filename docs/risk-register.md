# Risk Register

## Scales
**Likelihood** — 1 rare · 2 unlikely · 3 even odds · 4 likely · 5 near certain
**Impact** (hours lost) — 1 = under 2 h · 2 = 2–5 h · 3 = 5–12 h · 4 = 12–25 h · 5 = over 25 h / cannot ship.
**Exposure** = Likelihood × Impact. 

---

**R-01** — Because I am deploying a separated FastAPI backend and frontend to Render for the first time, CORS or environment variable configuration may not cooperate, delaying the Week 14 deployment and eating at my safety buffer.
· technical/novelty · L 4 · I 4 · **E 16**
· **Trigger:** the Week 9 walking skeleton deployment spike takes more than 2.0 hours to successfully read an `.env` variable.
· **Owner:** Caleb. · **Response:** avoid — deploy the walking skeleton spike in Week 9, not Week 14, so the unknown config friction is taken care of five weeks early.
· **Contingency:** go back to a local-only Docker deployment for the final demo, formally dropping requirement NFR-REL-01.
· **Status:** open. Reviewed weekly.

**R-02** — Because the project is strictly constrained to a 57-hour build budget and my historical calibration factor is 1.16x, I may go through my 14.25-hour buffer before Week 14, which would give me no time for final testing.
· schedule · L 3 · I 5 · **E 15**
· **Trigger:** the `plan-check.py` output shows "plannable hours" going below 0.0 during any Monday planning session.
· **Owner:** Caleb. · **Response:** cut out by Week 8 — push one non-critical task now (during MS7 scope cuts) to save my 25% buffer, and re-run the checker script weekly.
· **Contingency:** cutting the UI styling and accessibility pass (WP-3) to ship a bare-bones, unstyled HTML form that just shows the API works.
· **Status:** open.

**R-03** — Because the free VirusTotal API only lets me make 4 calls per minute, local testing of the 10-second polling loop may trigger rate limits, slowing down development progress and hurting the final demo.
· technical/dependency · L 4 · I 3 · **E 12**
· **Trigger:** any HTTP `429` status code that shows up in the FastAPI terminal logs or the browser network tab.
· **Owner:** Caleb. · **Response:** mitigate by Week 10 — implement the upstream error catch early to catch 429s gracefully, and count on a local mock JSON response for UI testing.
· **Contingency:** use a hardcoded JSON fixture of a "Safe" and "Unsafe" result for the final project demo so it never actually touches the VT network.
· **Status:** open.

**R-04** — Because Python's standard `time.sleep()` stops the main thread, the 10-second polling loop may stop the entire FastAPI server, causing timeouts for any concurrent requests.
· technical/architecture · L 3 · I 4 · **E 12**
· **Trigger:** a local test with two browser tabs submitting a URL results in one tab hanging indefinitely until the other finishes.
· **Owner:** Caleb. · **Response:** mitigate by Week 11 — use `asyncio.sleep()` in the polling loop and test with requests early.
· **Contingency:** downgrade the system requirements to synchronous blocking, documenting that the scanner only supports one user at a time.
· **Status:** open.

**R-05** — Because I am juggling my capstone alongside wedding planning, normal coursework, and life events, I may miss consecutive planned work days, which could push tasks past their weekly gates.
· schedule/personal · L 3 · I 3 · **E 9**
· **Trigger:** the Sunday `docs/hours-log.csv` entry shows fewer than 6.0 hours logged for the entire week.
· **Owner:** Caleb. · **Response:** accept — I have put in a strict 25% project buffer (14.25 hours) specifically to absorb weeks where life events limit my ability to get work done.
· **Contingency:** draw from the project buffer, document the draw in `docs/plan.md`, and drop the lowest-priority feature in the backlog to compensate.
· **Status:** open.

**R-06** — Because I am using a public GitHub repository, my VT API key might accidentally be committed in the source code, in which my key could be taken by VirusTotal (done before).
· data/security · L 2 · I 4 · **E 8**
· **Trigger:** A GitHub automated secret-scanning alert email is received.
· **Owner:** Caleb. · **Response:** avoid — make `.gitignore` exclude `.env` files before the very first commit in Week 8.
· **Contingency:** immediately move the API key in the VT dashboard and update the Render environment variables.
· **Status:** open.

**R-07** — Because VirusTotal may update their JSON response schema without me knowing, the Python dictionary parsing logic may give me a `KeyError`, crashing the scanning endpoint.
· dependency · L 2 · I 3 · **E 6**
· **Trigger:** A 500 Internal Server Error appears when scanning a previously working URL.
· **Owner:** Caleb. · **Response:** get rid of by Week 10 — use defensive `.get()` methods for all JSON parsing with safe fallback values.
· **Contingency:** check VT documentation for schema changes and use a hotfix for the parsing logic.
· **Status:** open.

**R-08** — Because Render's free tier goes to sleep after 15 minutes of inactivity, the very first user to hit the UI might experience a 50+ second load time, causing them to assume the app is broken and leave.
· technical · L 5 · I 1 · **E 5**
· **Trigger:** The browser network tab shows a pending request taking > 30 seconds.
· **Owner:** Caleb. · **Response:** stop by Week 11 — build a loading state in the UI so the user knows the system is working, even if it's waking up.
· **Contingency:** hit the Render URL myself 2 minutes before any live demonstration to pre-warm the server.
· **Status:** open.