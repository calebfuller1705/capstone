# Invisible Work Inventory

| Invisible work package | In my WBS already? | Rough hours |
| :--- | :--- | :--- |
| Repository scaffold + CI | [ ] yes  [x] no | 2.0 |
| Error handling + edge cases (all from Week 6) | [x] yes  [ ] no | 4.0 |
| Accessibility pass | [x] yes  [ ] no | 2.5 |
| Secrets, config, deployment (Render) | [ ] yes  [x] no | 3.0 |
| Reviewing AI-made code | [ ] yes  [x] no | 5.0 |
| README / runbook / handoff guide | [ ] yes  [x] no | 3.0 |
| *Specific 1: Render 50s cold-start UI mitigation* | [x] yes  [ ] no | 1.5 |
| *Specific 2: VT API key local `.env` setup* | [ ] yes  [x] no | 0.5 |
| *Specific 3: API rate-limit mocking for local dev* | [ ] yes  [x] no | 2.0 |

# Decompose One Work Package Properly

| Task | Name | Reqs | O | M | P | E | Done when | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-1.1** | Submit URL to VT through API | FR-SYS-01, NFR-SEC-01 | 1 | 2 | 4 | 2.2 | Backend is able to POST to VT and retrieves base64 analysis ID using local `.env` key. | (Repo Setup) |
| **T-1.2** | Polling Loop & Timeout Clock | FR-API-02, NFR-PERF-01 | 2 | 3 | 6 | 3.3 | System polls VT `/analyses/{id}` every ~2s, stopping exactly at 10.0s with a 504 if still queued. | T-1.1 |
| **T-1.3** | JSON Parsing & Evaluator | FR-UI-01, FR-UI-02 | 1 | 2 | 4 | 2.2 | VT JSON response is parsed safely; Safe/Unsafe answer is returned based on `stats.malicious > 0`. | T-1.2 |
| **T-1.4** | Upstream Error Degradation | FR-API-01 | 1 | 2.5 | 5 | 2.7 | 429 Rate Limit and 500 Internal errors from VT are caught and mapped to our custom error envelope. | T-1.1 |

# The Bad-WBS Autopsy

**The Bad WBS:**
1. Set up project (1 week)
2. Build backend (3 weeks)
3. Build frontend (3 weeks)
4. Add AI features (1 week)
5. Test and deploy (1 week)

**Five Distinct Defects:**
1. **Neighborhoods, not deliverables:** "Build backend" is a neighborhood, not a deliverable. It hides lots of different tasks.
2. **Testing as a final phase:** Testing is pushed into the last week instead of being done with every task. When the build runs late, testing will be skipped altogether.
3. **No requirement traces:** Nothing points to the FRs or NFRs from the specification. If scope needs to be cut, you won't know what requirement is being taken away from.
4. **Vague, single-point estimates:** "3 weeks" is not an estimate (Is that 15 hours? 60 hours?). There are no O/M/P estimates in hours to make up for uncertainty.
5. **No "Done-When" conditions:** There is no objective gate to determine when "Build frontend" is truly complete, which brings in scope creep.

**Rewriting Item 2 ("Build backend") as a Proper Work Package:**

**WP-2: API Service & URL Validation**
| Task | Name | Reqs | O | M | P | E | Done when | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-2.1** | FastAPI Router & CORS Setup | FR-SYS-01 | 1 | 2 | 3 | 2.0 | `POST /scan` accepts JSON and returns a 200 OK with a dummy payload. | (Repo Setup) |
| **T-2.2** | URL Validation & Intranet Blocking | FR-INP-01, 03, 04, FR-EVAL-01 | 2 | 3 | 5 | 3.2 | Strings > 2048 chars, missing domains, or local IPs return exact 400/422 status codes. | T-2.1 |
| **T-2.3** | VirusTotal Polling Integration | FR-API-02, NFR-PERF-01 | 3 | 4 | 7 | 4.3 | System submits URL, polls VT asynchronously, and returns Safe/Unsafe verdict within 10s. | T-2.2 |
| **T-2.4** | Global Error Envelope & Degradation | FR-API-01 | 1 | 2 | 4 | 2.2 | Upstream 429/500 errors map cleanly to the custom system error envelope and do not crash the app. | T-2.3 |

# Three-Point Estimate Everything

# Work Breakdown Structure (WBS)

| ID | Task Name | Req | Dep | Done-When | O | M | P | E |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **WP-1** | **VT API Integration** |
| T-1.1 | Register VT API & Setup Postman | NFR-01 | None | API key is active and gives 200 in Postman | 0.5 | 1.0 | 2.0 | 1.08 |
| T-1.2 | Write sync Python script to hit VT | FR-01 | T-1.1 | Script puts URL score in console | 0.5 | 1.0 | 2.0 | 1.08 |
| T-1.3 | Implement 10-second polling loop | FR-02 | T-1.2 | Script  waits for `queued` status | 1.0 | 2.0 | 4.0 | 2.17 |
| T-1.4 | Parse JSON for score/stats | FR-03 | T-1.3 | Script prints integer values for malicious/clean | 1.0 | 2.0 | 4.0 | 2.17 |
| T-1.5 | Catch 429 errors safely | NFR-02 | T-1.3 | Script gives error on rate limit instead of crashing | 1.0 | 2.5 | 5.0 | 2.67 |

| **WP-2** | **FastAPI Backend Service** |
| T-2.1 | FastAPI project scaffold & CORS | NFR-03 | None | GET `/` returns 200 via browser | 1.0 | 2.0 | 3.0 | 2.00 |
| T-2.2 | POST `/scan` endpoint skeleton | FR-04 | T-2.1 | Endpoint takes JSON and returns dummy 200 | 1.0 | 1.5 | 3.0 | 1.67 |
| T-2.3 | Pydantic validation for URL input | FR-05 | T-2.2 | Endpoint doesn't take malformed URLs (422 error) | 1.0 | 1.5 | 2.0 | 1.50 |
| T-2.4 | Make VT loop into async route | FR-06 | T-1.4, T-2.2 | Endpoint gives VT score for valid URL | 2.0 | 3.0 | 5.0 | 3.17 |
| T-2.5 | Global error envelope wrapper | NFR-04 | T-2.4 | Internal errors return JSON format | 1.0 | 2.0 | 4.0 | 2.17 |

| **WP-3** | **Frontend UI** |
| T-3.1 | HTML index structure & form | FR-07 | None | Form shows locally in browser | 0.5 | 1.0 | 2.0 | 1.08 |
| T-3.2 | CSS layout & styling baseline | NFR-05 | T-3.1 | Flexbox layout lines up with wireframe | 0.5 | 1.0 | 1.0 | 0.92 |
| T-3.3 | JS fetch logic to hit POST `/scan` | FR-08 | T-2.1, T-3.1 | JS logs from JSON via local FastAPI | 1.0 | 1.5 | 3.0 | 1.67 |
| T-3.4 | Dynamic DOM loading state | FR-09 | T-3.3 | UI shows spinning wheel while waiting for response | 1.0 | 1.5 | 3.0 | 1.67 |
| T-3.5 | Client-side error state rendering | FR-10 | T-3.3 | Red error 500/400 response | 1.0 | 1.5 | 3.0 | 1.67 |
| T-3.6 | Accessibility Pass (DEFERRED) | NFR-06 | T-3.2 | Axe DevTools gives me 0 violations | 1.0 | 2.0 | 4.0 | 2.17 |

| **WP-4** | **CI/CD & Deployment** |
| T-4.1 | "Hello World" Deploy Spike | NFR-07 | None | Dummy app is live on Render domain | 1.0 | 2.5 | 6.0 | 2.83 |
| T-4.2 | Render `render.yaml` configuration | NFR-08 | T-4.1 | Render dashboard comes from IaC file | 0.5 | 1.0 | 2.0 | 1.08 |
| T-4.3 | Secret/Env setup on Render | NFR-09 | T-4.2 | Production app is able to read VT API Key | 0.5 | 1.0 | 2.0 | 1.08 |
| T-4.4 | Deploy finalized combined code | FR-11 | T-2.4, T-3.5 | Fully working app on live URL | 1.0 | 1.5 | 3.0 | 1.67 |

| **WP-5** | **Testing & QA** |
| T-5.1 | Create offline VT mock JSON | NFR-10 | T-1.4 | Local testing does not build onto VT quota | 0.5 | 1.0 | 1.5 | 1.00 |
| T-5.2 | Unit test URL Pydantic validator | NFR-11 | T-2.3 | Pytest suite has 5 valid/invalid cases | 0.5 | 1.0 | 2.0 | 1.08 |
| T-5.3 | End-to-end manual test matrix | NFR-12 | T-4.4 | Safe, Malicious, and Timeout states verified | 1.0 | 1.0 | 1.0 | 1.00 |

| **WP-6** | **Project Handoff** |
| T-6.1 | OpenAPI/Swagger review | NFR-13 | T-2.5 | UI shows all expected endpoints | 0.5 | 1.0 | 1.5 | 1.00 |
| T-6.2 | README & architecture diagram | NFR-14 | T-4.4 | Repo has setup instructions and diagram | 1.0 | 1.5 | 2.0 | 1.50 |


# The Spread Test

| Task | O | P | P/O | Verdict (split / spike) | Spike cap | Spike deliverable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-1.4** (Upstream Error Degradation) | 1.0 | 5.0 | 5.0 | Spike | 1.5h | A short Python script proving how to catch a `urllib3` timeout or 500 error without crashing FastAPI. |
| **T-4.2** (Render Deployment & Secrets) | 1.0 | 6.0 | 6.0 | Spike | 2.0h | A dummy FastAPI "Hello World" sent to Render that successfully reads one `.env` variable. |

# Compute Your Calibration Factor

**Calibration Factor:** 1.16x

# Schedule & Gates

| Week | Work Package Focus | Weekly Gate (Must be true to proceed) |
| :--- | :--- | :--- |
| **Week 8** | WP-1: VT API Polling | A local Python script is able to retrieve a VT score. |
| **Week 9** | WP-4: Deployment Spike | A dummy FastAPI "Hello World" is live on Render. |
| **Week 10** | WP-2: API Service | FastAPI gives the VT score over local HTTP on port 8000. |
| **Week 11** | WP-3: Frontend UI | The browser UI POSTs to the local backend. |
| **Week 12** | Integration & Bugs | UI and Backend are successfully combined on Render. |
| **Week 13+** | Buffer & QA | N/A (Buffer weeks to absorb overruns). |

# Run the Checker

**Verdict:** `VERDICT: OVER BUDGET by 2.6 h - cut, defer, or re-estimate`
**First Week Exceeded:** (N/A - The plan never exceeds raw capacity)
**Burn-Down Baseline (Adjusted after fixing the over):**
| Week | Capacity | Ideal | Projected |
| :--- | :--- | :--- | :--- |
| 8 | 6.5 | 42.8 | 45.4 |
| 9 | 6.5 | 36.3 | 38.9 |
| 10 | 6.5 | 29.8 | 32.4 |
| 11 | 6.5 | 23.3 | 25.9 |
| 12 | 6.5 | 16.8 | 19.4 |
| 13 | 6.5 | 10.3 | 12.9 |
| 14 | 6.5 | 3.8 | 6.4 |
| 15 | 6.5 | -2.7 | -0.1 |

# Build the Capacity Table

| Week | Course overhead | Known losses | Available for the project |
| :--- | :--- | :--- | :--- |
| **8** | 0h | 0h | 6.5h |
| **9** | 0h | 0h | 6.5h |
| **10** | 0h | 0h | 6.5h |
| **11** | 0h | 0h | 6.5h |
| **12** | 0h | 0h | 6.5h |
| **13** | 0h | 0h | 6.5h |
| **14** | 0h | 0h | 6.5h |
| **15** | 0h | 0h | 6.5h |
| **16** | 0h | 0h | 5.0h |
| **Total** | | | **57.0h** |


# Declare the Buffer and Find the Gap

**Available** 57.0 h · **Buffer (25%)** 14.25 h · **Plannable** 42.75 h
**Calibrated WBS total** 45.4 h · **Gap** 2.65 h over budget

# The Risk Register

| ID | Risk | Category | L | I | E | Trigger | Owner | Response |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Budget Exceeded:** Because of the 57-hour limit, the project runs out of hours before being finished. | Schedule | 4 | 5 | 20 | Remaining capacity < 0 in `plan-check` | Me | **Mitigate:** Cut scope in Milestone 7 and track hours strictly. |
| **R-02** | **VT Rate Limit:** Because VT stops free API calls (4/min), heavy testing or demo usage brings back 429 errors. | Dependency | 4 | 4 | 16 | 429 status code returned by VT | Me | **Mitigate:** Catch 429s and mock for local dev. |
| **R-03** | **Render Cold Start:** Because Render spins down free tiers, the 50s cold start brings a 504 gateway timeout on the UI. | Technical | 4 | 3 | 12 | 504 Timeout on first load | Me | **Mitigate:** Async fetch with spinning UI state. |
| **R-04** | **Async Blocking:** Because Python `time.sleep()` blocks, the polling loop stops the entire FastAPI server. | Technical | 3 | 4 | 12 | Server stops responding during polling | Me | **Mitigate:** Spike async HTTP exception handling early. |
| **R-05** | **Wedding/Personal:** Because of wedding planning and other life events, I miss consecutive planned work days. | Personal | 3 | 4 | 12 | Logged < 8 hours for the week | Me | **Accept:** Built the 25% project buffer to absorb life events. |
| **R-06** | **CORS Blocking:** Because the frontend and backend are separate, Render blocks requests through CORS. | Technical | 3 | 3 | 9 | Browser console CORS blocked error | Me | **Mitigate:** Config FastAPI CORS middleware early. |
| **R-07** | **Schema Change:** Because VT is a third party, their JSON response structure is different from documentation. | Dependency | 2 | 3 | 6 | `KeyError` when parsing JSON | Me | **Mitigate:** Defensive dictionary `.get()` parsing (T-1.3). |
| **R-08** | **API Key Leak:** Because the repo is public, my VT API key is accidentally put on GitHub. | Security | 1 | 5 | 5 | GitHub secret scanning alert | Me | **Avoid:** Configure `.env` and `.gitignore` before first commit. |


# The Breadth Pass, and Its Price

**Audit of AI Generation:**
*   Tasks proposed: **18** | kept: **12** | genuinely new to me: **3**
*   Risks proposed: **15** | kept: **5** | genuinely new to me: **2**
*   Of the durations it produced: how many were identical? **Almost all (it defaulted to "2 hours" or "1 day" for everything)** | spread given? **0**

# Budget What AI Costs You

**Estimating T-2.3 (VirusTotal Polling Integration):**
*   **T-2.3 by hand:** O: 3.0 | M: 4.0 | P: 7.0 -> **E: 4.33 h**
*   **T-2.3 generated:** generation: 0.5 h + review: 1.0 h + debugging: 2.5 h = **4.0 h**

### Final Scope Decision

| Cut / Deferred | Requirements | Hours Recovered | MoSCoW (Before & After) | Why |
| :--- | :--- | :--- | :--- | :--- |
| **Formal First-Time User Usability Testing Sessions** | NFR-USE-01 | 2.5 calibrated hours | NFR-USE-01 was the lowest-priority requirement in the specification. Deferring external stopwatch sessions and usability stumble analysis protects the 25% deployment buffer without compromising any functional, security, or accessibility requirements. |