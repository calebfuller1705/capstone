# Feature areas and the identifier scheme

AREA CODE,AREA NAME,ONE SENTENCE OF SCOPE
INP,Input,Everything about the user submitting and validating a URL.
API,External APIs,Everything about securely querying VirusTotal and handling network responses.
EVAL,Risk Scoring,Everything about translating raw JSON thresholds into a boolean safe/unsafe verdict.
DASH,Dashboard,Everything about loading the final risk score in plain English for a non-technical user.

# The persona set, with evidence

| Persona | Who | Needs | Constraining behavior | Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Corporate Employee** (Primary) | A non-technical office worker who frequently receives external emails. | To instantly know if a link is safe to click without parsing technical data. | Will close the app and escalate to the IT helpdesk if the results are confusing or take too long to load. | Interview 2026-08-29; quoted stating they "have no clue whether it is real." |
| **The next maintainer** | The person who clones the repository in Week 17 knowing nothing about it. | To understand what every feature was for, from the document alone. | Will fail the deployment test if environment variables and API keys are not clearly documented in a setup file. | The course's own handoff test. |

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

### FR-INP-01 — URL Submission
**Priority:** Must
**Requirement:** A user shall be able to submit a URL string for analysis.
**Rationale:** The corporate employee needs a mechanism to pass the suspicious link to the system.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
* Given a user on the main dashboard, when they submit a correctly formatted URL (e.g., starting with `https://`), then the system initiates the API call and displays the loading indicator[cite: 1].
* Given a user on the main dashboard, when they submit a string containing spaces or lacking a valid domain format, then the system rejects the input and displays a "Malformed URL" error message without calling the API[cite: 1].

### FR-INP-02 — Empty Submission Rejection
**Priority:** Must
**Requirement:** The system shall reject empty submissions and prompt the user to enter a valid URL.
**Rationale:** Prevents wasted API calls and gives immediate feedback to the employee.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given a user on the main dashboard, when they click submit with an empty input field, then the system prevents the network request and displays a "Blank field" error[cite: 1].
* Given a user on the main dashboard, when they enter only whitespace characters and click submit, then the system prevents the network request and displays a "Blank field" error[cite: 1].

### FR-API-01 — Rate Limit Handling
**Priority:** Must
**Requirement:** The system shall display a specific rate-limit error message when the VirusTotal API returns an HTTP 429 status code.
**Rationale:** Corporate employees need to know the daily limit was hit so they try again tomorrow instead of escalating to IT.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given the backend makes a query to VirusTotal, when the API returns an HTTP 429 status code, then the system displays the text "You have reached the daily request limit, please try again tomorrow.".
* Given the backend makes a query to VirusTotal, when the API returns an HTTP 500 status code, then the system displays the text "500 Error. Please try again."[cite: 1, 2].

### FR-API-02 — API Timeout
**Priority:** Must
**Requirement:** The system shall abort the VirusTotal API call and display a failure message if a response is not received within 10 seconds.
**Rationale:** Employees need to be freed to move on with their work if the external service hangs.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given the system is waiting for a VirusTotal response, when the API returns the data in under 10 seconds, then the dashboard displays the final safe/unsafe verdict[cite: 1].
* Given the system is waiting for a VirusTotal response, when 10 seconds elapse with no data returned, then the system aborts the network request and displays a timeout failure message[cite: 1].

### FR-EVAL-01 — Unscannable URL Fallback
**Priority:** Must
**Requirement:** The system shall return a "cannot be analyzed" message when the submitted URL resolves to a local intranet address.
**Rationale:** Employees need to know when a link wasn't scanned rather than receiving a false positive or false negative.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given a user submits a local intranet link (e.g., `http://intranet.local`), when the system parses the domain, then it bypasses the API call and explicitly states that the URL could not be analyzed[cite: 1, 2].
* Given a user submits a standard public domain, when the system parses the domain, then it proceeds to execute the VirusTotal API call[cite: 1].

### FR-EVAL-02 — Ambiguous Risk State
**Priority:** Should
**Requirement:** The system shall classify a URL as "ambiguous" if the VirusTotal threshold does not conclusively meet the defined safe or unsafe criteria.
**Rationale:** Provides a middle ground for links that trigger some, but not definitive, security flags.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given the API returns a risk score that falls strictly between your mathematically defined "safe" and "unsafe" thresholds, when the dashboard renders the result, then it displays the "ambiguous/warning" state[cite: 1, 2].
* Given the API returns a risk score that explicitly meets the "unsafe" numeric threshold, when the dashboard renders the result, then it displays a red "unsafe" visual indicator[cite: 1, 2].

### FR-DASH-01 — Asynchronous Loading Indicator
**Priority:** Must
**Requirement:** The system shall display a visual loading indicator while the VirusTotal API request is in flight.
**Rationale:** Users will abandon the check and escalate to IT if they think the application is frozen.
**Source:** Interview 2026-08-29
**Acceptance Criteria:**
* Given a valid URL submission is accepted, when the network request to VirusTotal is initiated, then the screen displays a spinning wheel and cycles through security tips[cite: 1].
* Given the loading indicator is active, when the API request resolves or hits the 10-second timeout, then the spinning wheel and tips immediately disappear and are replaced by the verdict[cite: 1].

### FR-DASH-02 — Successive Submissions
**Priority:** Should
**Requirement:** A user shall be able to submit a new URL directly from the results dashboard without navigating back to the initial submission page.
**Rationale:** Reduces friction for employees who have multiple links to check in one sitting.
**Source:** My recorded decision 2026-09-02
**Acceptance Criteria:**
* Given a user is viewing a finalized risk verdict, when they click the "Upload another URL" button, then the system clears the current results and presents a blank submission field without requiring a page reload[cite: 1].
* Given a user is viewing a finalized risk verdict, when they click the "Upload another URL" button, then the previous URL's data is cleared from the dashboard to ensure the new submission is not confused with the old one[cite: 1].