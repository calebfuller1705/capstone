# Rep 1: Invisible Work Inventory

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

# Rep 2: Decompose One Work Package Properly

| Task | Name | Reqs | O | M | P | E | Done when | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-1.1** | Submit URL to VT through API | FR-SYS-01, NFR-SEC-01 | 1 | 2 | 4 | 2.2 | Backend is able to POST to VT and retrieves base64 analysis ID using local `.env` key. | (Repo Setup) |
| **T-1.2** | Polling Loop & Timeout Clock | FR-API-02, NFR-PERF-01 | 2 | 3 | 6 | 3.3 | System polls VT `/analyses/{id}` every ~2s, stopping exactly at 10.0s with a 504 if still queued. | T-1.1 |
| **T-1.3** | JSON Parsing & Evaluator | FR-UI-01, FR-UI-02 | 1 | 2 | 4 | 2.2 | VT JSON response is parsed safely; Safe/Unsafe answer is returned based on `stats.malicious > 0`. | T-1.2 |
| **T-1.4** | Upstream Error Degradation | FR-API-01 | 1 | 2.5 | 5 | 2.7 | 429 Rate Limit and 500 Internal errors from VT are caught and mapped to our custom error envelope. | T-1.1 |

# Rep 3: The Bad-WBS Autopsy

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

# Rep 4: Three-Point Estimate Everything

**WP-3: Frontend UI & Client Logic**
| Task | Name | Reqs | O | M | P | E | Done when | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-3.1** | HTML/CSS Scaffold | FR-INP-01 | 1.0 | 2.0 | 3.0 | 2.0 | Input field and submit button; basic styling done. | None |
| **T-3.2** | Async Fetch & DOM Updates | FR-UI-01 | 2.0 | 3.0 | 5.0 | 3.2 | Client successfully POSTs to API and shows spinning loading state until 200 OK comes back. | T-2.1 |
| **T-3.3** | Client-Side Error States | FR-INP-02 | 1.0 | 2.0 | 4.0 | 2.2 | Network drops or 400/429/504 HTTP codes correctly show user-friendly error messages in the DOM. | T-3.2 |
| **T-3.4** | Accessibility Pass | NFR-ACC-* | 1.0 | 2.0 | 4.0 | 2.2 | Keyboard-only navigation works; screen reader will announce verdict; contrast is 4.5:1. | T-3.1 |

**WP-4: CI, Deployment, & Documentation**
| Task | Name | Reqs | O | M | P | E | Done when | Depends on |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-4.1** | Repository CI & Spec-Check | (Internal) | 1.0 | 1.5 | 3.0 | 1.7 | GitHub Actions runs `spec-check.py` on every push and blocks on failure. | None |
| **T-4.2** | Render Deployment & Secrets | NFR-REL-01 | 1.0 | 2.5 | 6.0 | 2.8 | API Service is live on Render; VirusTotal API key is securely put in through environment variables. | T-2.1 |
| **T-4.3** | README & Handoff Guide | (Internal) | 2.0 | 3.0 | 5.0 | 3.2 | A stranger can clone the repo, put in their own VT key, and run it locally just from the instructions. | T-4.2 |

# Rep 5: The Spread Test

| Task | O | P | P/O | Verdict (split / spike) | Spike cap | Spike deliverable |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **T-1.4** (Upstream Error Degradation) | 1.0 | 5.0 | 5.0 | Spike | 1.5h | A short Python script proving how to catch a `urllib3` timeout or 500 error without crashing FastAPI. |
| **T-4.2** (Render Deployment & Secrets) | 1.0 | 6.0 | 6.0 | Spike | 2.0h | A dummy FastAPI "Hello World" sent to Render that successfully reads one `.env` variable. |

# Rep 6: Compute Your Calibration Factor

**Calibration Factor:** 1.16x

# Rep 7: Run the Checker

**Verdict:** `VERDICT: OVER BUDGET by 2.6 h - cut, defer, or re-estimate`
**First Week Exceeded:** (N/A - The plan never exceeds raw capacity)

### Rep 8: Build the Capacity Table


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


# Rep 9: Declare the Buffer and Find the Gap

**Available** 57.0 h · **Buffer (25%)** 14.25 h · **Plannable** 42.75 h
**Calibrated WBS total** 45.4 h · **Gap** 2.65 h over budget

### Rep 10: The Risk Register

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