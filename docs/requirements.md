**Author:** Caleb Fuller  **Version:** 1.0  **Date:** 2026-09-02
**Status:** Draft

---

## 1. Purpose and Scope

The URL Security Scanner is a simple, stateless web app that exists for non-technical corporate employees. Its main purpose is to let staff quickly evaluate suspicious links before clicking on them, utilizing the VirusTotal API to give an immediate, plain-language "Safe" or "Unsafe" answer. This takes out the guesswork from handling potentially harmful email links and takes out the burden of basic triage on the IT helpdesk.

Explicitly outside the boundary of this release are user authentication, persistent user accounts, and individual scan history storage. The structure is strictly stateless to take out data liability and reduce complexity. Consequently, no admin dashboards for tracking employee scanning behaviors or historical analytics will be built.

# 2. Stakeholders and Personas

| Persona | Who they are | What they need from the system | Evidence they exist |
|---|---|---|---|
| Corporate Employee | A non-technical office worker receiving suspicious emails | A definitive Safe/Unsafe verdict without technical jargon | Interview 2026-08-29 |
| IT/Helpdesk Analyst | A technical support staff member handling escalations | Reduced ticket volume for baseline URL safety checks | Interview 2026-08-29 |
| Technical Maintainer | The developer inheriting the repository | Clear documentation on API credentials and application deployment | Capstone project parameters |


# 3. Definitions
AREA CODE,AREA NAME,ONE SENTENCE OF SCOPE
INP,Input,Everything about the user submitting and validating a URL.
API,External APIs,Everything about securely querying VirusTotal and handling network responses.
EVAL,Risk Scoring,Everything about translating raw JSON thresholds into a boolean safe/unsafe verdict.
DASH,Dashboard,Everything about loading the final risk score in plain English for a non-technical user.


### FR-INP-01 — URL Submission
**Priority:** Must
**Requirement:** A user shall be able to submit a URL string for analysis.
**Rationale:** The corporate employee needs a mechanism to pass the suspicious link to the system.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given a user on the main dashboard, when they submit a URL string starting with exactly http:// or https:// followed by a standard domain format, then the system initiates the API call and displays the loading indicator.
- Given a user on the main dashboard, when they submit a string containing spaces, a raw IP address, or lacking the http(s):// prefix, then the system rejects the input and displays a "Malformed URL" error message without calling the API.

### FR-INP-02 — Empty Submission Rejection
**Priority:** Must
**Requirement:** The system shall reject empty submissions and prompt the user to enter a valid URL.
**Rationale:** Prevents wasted API calls and gives immediate feedback to the employee.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given a user on the main dashboard, when they click submit with an empty input field, then the system prevents the network request and displays a "Blank field" error.
- Given a user on the main dashboard, when they enter only whitespace characters and click submit, then the system prevents the network request and displays a "Blank field" error.

### FR-API-01 — Rate Limit Handling
**Priority:** Must
**Requirement:** The system shall display a specific rate-limit error message when the VirusTotal API returns an HTTP 429 status code.
**Rationale:** Corporate employees need to know the daily limit was hit so they try again tomorrow instead of escalating to IT.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given the backend makes a query to VirusTotal, when the API returns an HTTP 429 status code, then the system displays the text "You have reached the daily request limit, please try again tomorrow."
- Given the backend makes a query to VirusTotal, when the API returns an HTTP 500 status code, then the system displays the text "500 Error. Please try again."

### FR-API-02 — API Timeout
**Priority:** Must
**Requirement:** The system shall abort the VirusTotal API call and display a failure message if a response is not received within 10 seconds.
**Rationale:** Employees need to be freed to move on with their work if the external service hangs.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given the system is waiting for a VirusTotal response, when the API returns the data in under 10 seconds, then the dashboard displays the final safe/unsafe verdict.
- Given the system is waiting for a VirusTotal response, when 10 seconds elapse with no data returned, then the system aborts the network request and displays a timeout failure message.

### FR-EVAL-01 — Unscannable URL Fallback
**Priority:** Must
**Requirement:** The system shall return a "cannot be analyzed" message when the submitted URL resolves to a local intranet address.
**Rationale:** Employees need to know when a link wasn't scanned rather than receiving a false positive or false negative.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given a user submits a local intranet link (e.g., `http://intranet.local`), when the system parses the domain, then it bypasses the API call and explicitly states that the URL could not be analyzed.
- Given a user submits a standard public domain, when the system parses the domain, then it proceeds to execute the VirusTotal API call.

### FR-EVAL-02 — Ambiguous Risk State
**Priority:** Should
**Requirement:** The system shall classify a URL as "ambiguous" if the VirusTotal threshold does not conclusively meet the defined safe or unsafe criteria.
**Rationale:** Provides a middle ground for links that trigger some, but not definitive, security flags.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given the API returns a risk score that falls strictly between your mathematically defined "safe" and "unsafe" thresholds, when the dashboard renders the result, then it displays the "ambiguous/warning" state.
- Given the API returns a risk score that explicitly meets the "unsafe" numeric threshold, when the dashboard renders the result, then it displays a red "unsafe" visual indicator.

### FR-DASH-01 — Asynchronous Loading Indicator
**Priority:** Must
**Requirement:** The system shall display a visual loading indicator while the VirusTotal API request is in flight.
**Rationale:** Users will abandon the check and escalate to IT if they think the application is frozen.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given a valid URL submission is accepted, when the network request to VirusTotal is initiated, then the screen displays a spinning wheel and cycles through a hardcoded array of three local security tips, rotating every 3 seconds.
- Given the loading indicator is active, when the API request resolves or hits the 10-second timeout, then the spinning wheel and tips immediately disappear and are replaced by the verdict.

### FR-DASH-02 — Successive Submissions
**Priority:** Should
**Requirement:** A user shall be able to submit a new URL directly from the results dashboard without navigating back to the initial submission page.
**Rationale:** Reduces friction for employees who have multiple links to check in one sitting.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
- Given a user is viewing a finalized risk verdict, when they click the "Upload another URL" button, then the system clears the current results and presents a blank submission field without requiring a page reload.
- Given a user is viewing a finalized risk verdict, when they click the "Upload another URL" button, then the previous URL's data is cleared from the dashboard to ensure the new submission is not confused with the old one.

### FR-UI-01 — Safe Result Rendering
**Priority:** Must
**Requirement:** The system shall display the word "Safe" alongside a green visual element when the API risk score falls below the danger threshold.
**Rationale:** The corporate employee needs immediate visual confirmation.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given the API score evaluates to safe, when the dashboard renders the result, then the exact text "Safe" appears on the screen.
- Given the API score evaluates to safe, when the dashboard renders the result, then the primary indicator color is green.

### FR-UI-02 — Unsafe Result Rendering
**Priority:** Must
**Requirement:** The system shall display the word "Unsafe" alongside a red visual element when the API risk score meets the danger threshold.
**Rationale:** The corporate employee requires clear danger signals to avoid clicking malicious links.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given the API score evaluates to unsafe, when the dashboard renders the result, then the exact text "Unsafe" appears on the screen.
- Given the API score evaluates to unsafe, when the dashboard renders the result, then the primary indicator color is red.

### FR-INP-03 — Long URL Rejection
**Priority:** Must
**Requirement:** The system shall reject a submitted URL exceeding 2,048 characters.
**Rationale:** Prevents buffer overflow attacks or excessive memory consumption.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given a user pastes a URL containing 2,049 characters, when they submit the form, then the system blocks the request and displays a length error.
- Given a user pastes a URL containing exactly 2,048 characters, when they submit the form, then the system initiates the API request.

### FR-INP-04 — Whitespace Trimming
**Priority:** Must
**Requirement:** The system shall strip leading and trailing whitespace characters from the URL string prior to validation.
**Rationale:** Employees frequently highlight and copy extra spaces accidentally from email clients.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given a user submits a valid URL surrounded by spaces, when the system receives the string, then it removes the spaces and executes the scan.
- Given a user submits a valid URL with a trailing newline character, when the system receives the string, then it removes the newline and executes the scan.

### FR-EVAL-03 — Shortened URL Resolution
**Priority:** Could
**Requirement:** The system shall follow HTTP redirects to resolve shortened URLs to their final destination before querying VirusTotal.
**Rationale:** Attackers frequently hide malicious domains behind shorteners like bit.ly.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given a user submits a shortened URL, when the system evaluates it, then the backend performs a redirect trace to find the final domain.
- Given the backend finds the final domain, when the trace completes, then it sends the final domain to the VirusTotal API instead of the shortener domain.

### FR-ACT-01 — Copy Verdict Text
**Priority:** Could
**Requirement:** A user shall be able to copy the final verdict text to their operating system clipboard.
**Rationale:** Corporate employees often need to paste the result back into an IT support ticket.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given a finalized risk verdict is visible, when the user clicks the copy interface element, then the text string of the verdict is placed in their clipboard.
- Given a finalized risk verdict is visible, when the user clicks the copy interface element, then the interface displays a brief "Copied" confirmation text.

### FR-SYS-01 — Credential Obfuscation
**Priority:** Must
**Requirement:** The backend server shall exclude the external API key from all network traffic sent to the client browser.
**Rationale:** The technical maintainer must protect the organization's API quota from theft.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
- Given a user inspects the browser network tab, when the dashboard loads, then the external API key is entirely absent from the payloads.
- Given a user submits a URL, when the frontend makes the request to the backend, then the external API key is entirely absent from the payloads.

### FR-SYS-02 — Action Logging
**Priority:** Should
**Requirement:** The backend server shall write the scanned domain name and the resulting risk score to a local text file.
**Rationale:** IT Helpdesk needs a minimal audit trail to retroactively investigate localized phishing campaigns.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given the API returns a risk score, when the system computes the final verdict, then it appends a new line to a local text file containing the domain and the score.
- Given the backend encounters an API error, when the error occurs, then it appends a new line to a local text file recording the error code.

### FR-DASH-03 — Scan Timestamp
**Priority:** Should
**Requirement:** The system shall display the exact time and date of the completed scan alongside the final verdict.
**Rationale:** Employees need proof of when they checked the link for compliance purposes.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given the system receives the final API payload, when the verdict renders, then the current local system time is displayed.
- Given the system receives the final API payload, when the verdict renders, then the current local system date is displayed.

### FR-EVAL-04 — Protocol Enforcement
**Priority:** Must
**Requirement:** The system shall forcibly prepend `http://` to submissions that lack a protocol prefix but otherwise contain a valid domain.
**Rationale:** Employees often copy links missing the protocol, causing unnecessary validation rejections.
**Source:** My recorded decision 2026-09-07
**Acceptance Criteria:**
- Given a user submits a string like `example.com` without a protocol, when the system validates it, then it alters the string to `http://example.com` before proceeding.
- Given a user submits a string like `https://example.com`, when the system validates it, then it leaves the prefix completely intact.


## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement (metric · threshold · condition) | Priority | How it is measured |
|---|---|---|---|
| NFR-PERF-01 | The URL scan result page gives an end-to-end response time p95 under 10.0 s with a valid domain submitted over a basic Wi-Fi connection. | Must | 20 manual URL submissions timed via browser tools network tab; record p95 in the measurements log. |

### 6.2 Reliability

| ID | Requirement (metric · threshold · condition) | Priority | How it is measured |
|---|---|---|---|
| NFR-REL-01 | The running URL scanner app gets a health check pass rate of at least 29 out of 30 consecutive days during the final four weeks on the free hosting tier. | Must | A scheduled automated ping that logs pass/fail to a text file. |

### 6.3 Usability

| ID | Requirement (metric · threshold · condition) | Priority | How it is measured |
|---|---|---|---|
| NFR-USE-01 | A first-time Corporate Employee user finishes the task in under 30 seconds. | Should | Two sessions with a stopwatch; time and find any UI stumbles recorded in notes. |

### 6.4 Security & Privacy

| ID | Requirement (metric · threshold · condition) | Priority | How it is measured |
|---|---|---|---|
| NFR-SEC-01 | Exactly 0 shown credentials, API keys, or tokens show up in the repo at any time, or during any user request. | Must | A local `grep` search for secrets across the full  history; manual inspection of the browser network tab. |
| NFR-SEC-02 | The system stores 0 bytes of user-specific scanned URL history to the server disk or database after a user successfully scans a URL and closes the browser. | Must | Manual  review of the backend routing to make sure no database write operations are around for user sessions. |
| NFR-PRI-01 | 100% of the time, the UI gives a clear disclaimer right next to the submit button stating: "Warning: URLs scanned here are shared publicly. Do not submit internal company links." | Must | Manual visual inspection of the deployed URL input form on page load. |

### 6.5 Accessibility

| ID | Requirement (metric · threshold · condition) | Priority | How it is measured |
|---|---|---|---|
| NFR-ACC-01 | 100% of interactive controls are reachable by keyboard alone in a logical order with a focus indicator that can be seen, using only `Tab`, `Shift+Tab`, `Space`, and `Enter` during the core URL submission and result-copying flow. | Must | Unplug the mouse; run the scan-and-copy flow; write down every situation the focus ring goes away or a control is skipped. |
| NFR-ACC-02 | Screen reader result announcement happens 100% of the time when the final scan result (Safe, Unsafe, Ambiguous, Error) appears on the screen after the API completes and UI moves from loading. | Must | Run a test URL with a screen reader active. |
| NFR-ACC-03 | 100% of form input have an associated descriptive text label on the primary URL submission form. | Must | Manual DOM inspection in browser developer tools. |
| NFR-ACC-04 | All body text and important UI text have a ratio of >= 4.5:1 against the background on all UI states and result displays. | Must | Run a WCAG contrast checker tool on the hex codes that I used for the green/red text against the background color of the app. |
| NFR-ACC-05 | 0 occurrences of information, severity, or state changes are shown by color alone when displaying the final scan answer. | Must | Set device running the test's display to grayscale and go through the main URL flow; making sure that the text specifically shows the result without just using the green or red hues. |

## 7. Out of Scope (the Won't-Have List)

| Not building | Why not | Revisit when |
|---|---|---|
| Full Email Text Parser | Extracting URLs from raw email bodies introduces complex string parsing and MIME-type handling that threatens the 57-hour budget. | Revisit in Week 14 only if the core construction budget has unused hours remaining. |
| User Accounts & Scan History | Retaining a history of checked links requires a database, an authentication system, and session management, which exceeds the scope of a stateless utility tool. | Will not be revisited this release; the application remains strictly stateless. |
| Secondary API Integration | Adding a fallback API (like urlscan.io) increases integration time and test surface area unnecessarily for the baseline requirement. | Revisit in Week 12 if the VirusTotal integration is completed comfortably under its 14-hour budget. |
| Raw IP Address Scanning | Validating and scanning raw IPs requires different API endpoints and risk-scoring metrics than standard domain URLs. | Revisit post-launch as a potential v2.0 feature. |
| Browser Extension | Building an extension to automatically scan links inside an email client requires a completely different tech stack and deployment model than a standalone web app. | Will not be revisited this semester. |


## 8. Open Questions

| Question | Owner | Date Added | Target Resolution |
| :--- | :--- | :--- | :--- |
| What exact mathematical threshold of VirusTotal vendor flags or community votes turns a link from "safe" to "unsafe"? | Caleb | 2026-09-02 | |
| How are URL shorteners (like `bit.ly`) handled—does the app automatically resolve the redirect, or does it only scan the short link itself? | Caleb | 2026-09-02 | |
| If the backend loses connection to the internet mid-query, what is the observable result on the frontend? | Caleb | 2026-09-02 | |
| Does the app support scanning raw IP addresses, or only standard domain URLs? | Caleb | 2026-09-02 | |
| How are the API keys injected into the application during the clean-machine deployment test? | Caleb | 2026-09-02 | |
| What constitutes a "malformed" URL during the input validation step (e.g., missing https://, spaces in the text)? | Caleb | 2026-09-02 | |
| Are there any specific characters (like <script>) that the input field must actively sanitize to prevent cross-site scripting (XSS)? | Caleb | 2026-09-02 | |


## 9. Document Change Log

| Date | Version | Change | Reason |
|---|---|---|---|
| 2026-09-03 | 1.0 | Initial specification | Milestone 3 |
| 2026-09-07 | 1.0 | Ambiguity pass after external | Updated FR-INP-01 and FR-DASH-01 criteria for absolute clarity |

