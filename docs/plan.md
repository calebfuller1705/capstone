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

### Rep 3: The Bad-WBS Autopsy

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