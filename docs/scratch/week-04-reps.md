## Rep 1: Five Adjectives, Four Fields

| Adjective | Metric | Threshold | Condition | Measurement method |
| :--- | :--- | :--- | :--- | :--- |
| **Fast** | End-to-end response time | p95 under 10.0 seconds | When searching a new, uncached URL via the VirusTotal API over standard Wi-Fi. | 20 manual URL submissions  will be timed through browser dev tools network tab; record p95 in the measurements log. |
| **Simple** | Time to get through main task | Under 30 seconds | First-time non-technical user (Corporate Employee) given a test link to evaluate. | Two observed sessions with a stopwatch; time and any UI issues recorded in usability notes. |
| **Secure** | Exposed API keys / tokens | Exactly 0 | At any commit in the Git history, and during any client request. | A local repo for secrets across all history; plus one manual inspection of the browser network tab payloads. |
| **Stateless** | User-specific scan history stored on the server | Exactly 0 bytes | After a user successfully scans a URL, gets their answer, and closes the browser. | Manual code review of the backend routing to make sure there are no database write operations exist for user sessions. |
| **Reliable** | Health check pass rate | 29 out of 30 consecutive days | During the final four weeks of the semester, running on the deployed free hosting tier. | A scheduled automated ping logging pass/fail to a text file. |


## Rep 2: The Percentile Drill

* **Mean:** 0.97s
* **p95:** 2.90s
* **Max:** 9.20s


## Rep 3: Diagnose and Rewrite

### 1. "The application should have good performance."
* **Defects:** unmeasurable, missing condition, no measurement method.
* **Rewrite:** `NFR-PERF-01` (Must) — The URL scan result page renders a p95 under 10.0 s with a valid domain sent over a standard office Wi-Fi connection. Measured by: 20 manual URL submissions timed via browser dev tools network tab; record p95 in the measurements log.

### 2. "The system must be highly available and scalable."
* **Defects:** compound, aspirational not verifiable, enterprise target copied to a student project, no measurement method.
* **Rewrite (Availability):** `NFR-REL-01` (Must) — The deployed URL scanner app answers a health check successfully on at least 29 of 30 consecutive daily checks during the final four weeks. Measured by: a scheduled uptime monitor ping logging pass/fail to a text file.
* **Rewrite (Scalability):** `NFR-PERF-02` (Could) — The system successfully processes 5  URL submissions without dropping the connection or exceeding the 10-second timeout. Measured by: submitting a URL simultaneously across 5 separate browser tabs and verifying a 200 OK response on all of them.

### 3. "The UI shall be intuitive."
* **Defects:** unmeasurable, aspirational not verifiable, missing condition, no measurement method.
* **Rewrite:** `NFR-USE-01` (Should) — A first-time user (Corporate Employee), given a test link, completes the scan and states the result (Safe/Unsafe) without assistance in under 30 seconds. Measured by: two observed sessions with people who have not seen the app; time and stumbles recorded with a stopwatch.

### 4. "User data will be kept safe."
* **Defects:** compound, unmeasurable, missing condition, no measurement method.
* **Rewrite (Secrets):** `NFR-SEC-01` (Must) — No credential, API key, or token appears in the repository at any commit in history. Measured by: a local `grep` search for secrets across the full git history.
* **Rewrite (Statelessness):** `NFR-SEC-02` (Must) — The system stores 0 bytes of user-specific scanned URL history to the server disk or database. Measured by: manual code review of the backend routing to verify no consistent write operations exist for user sessions.

### 5. "The code should follow best practices."
* **Defects:** aspirational not verifiable, unmeasurable, no measurement method.
* **Rewrite:** `NFR-MNT-01` (Must) — The repo clones and starts a local development server in under 10 minutes on a clean machine. Measured by: executing the `README.md` setup steps on a fresh environment and timing it with a stopwatch.

### 6. "The app should work on mobile."
* **Defects:** missing condition, no measurement method.
* **Rewrite:** `NFR-POR-01` (Must) — The core URL submission form and results dashboard come in without horizontal scrolling and are fully functional on an iOS Safari viewport (390x844). Measured by: manual smoke test of the main flow using browser dev tools mobile device.


## Rep 4: The Data Inventory

| Data element | Why you need it | Where it lives | How long you keep it | How a user gets rid of it |
| :--- | :--- | :--- | :--- | :--- |
| **Submitted URLs** | Needed to evaluate security risk | In-memory while moving, and on VirusTotal's servers | *Verify* (VirusTotal policy) | *Verify* (VirusTotal policy) |
| **API Keys (VirusTotal)** | Needed to authenticate to the API | Environment variables / Server config | Until project is done / rotation | Manual get deleted from server config |
| **Action Log (Domains/Scores)** | IT Helpdesk audit trail (`FR-SYS-02`) | Local .txt file on the server | Life of the server instance | Admin must manually delete the file |
| **Server Access Logs (IPs)** | Standard web hosting operations | Hosting provider's logging system | *Verify* (Host policy of whatever I end up choosing) | *Verify* (Host policy) |


## Rep 5: The Mouse-Unplugged Pass

**Stuck Points for the URL Scanner:**
1. **Invisible Focus:** Tabbing from the URL input field to the "Submit" button might not show a clear outline, which would make it impossible to know where the cursor is.
2. **Silent Results:** When the API finishes after a few seconds and renders "Safe" or "Unsafe" on the screen, a keyboard/screen-reader user wouldn't know the page updated unless focus is intentionally moved to the result.
3. **Unreachable Copy Button:** Unless the "Copy Verdict" button (FR-ACT-01) is an actual button, the `Tab` key goes right over it.

**Accessibility Requirements (NFRs):**

### NFR-ACC-01 — Keyboard Navigation & Focus
**Priority:** Must
**Requirement:** 100% of controls on the URL scanner page will be reachable and able to run by keyboard alone, in a logical order, with a highly visible focus indicator.
**Metric:** Percentage of interactive controls reachable by keyboard.
**Threshold:** 100%.
**Condition:** Using only the `Tab`, `Shift+Tab`, `Space`, and `Enter` keys during the core URL submission and result-copying flow.
**Method:** Unplug the mouse; complete the scan-and-copy flow; write down every spot the focus ring goes away or a control is skipped.

### NFR-ACC-02 — Dynamic Result Announcement
**Priority:** Must
**Requirement:** The system will programmatically announce the final scan verdict (Safe, Unsafe, Ambiguous, Error) to all technologies immediately when it renders on the screen.
**Metric:** Screen reader result announcement.
**Threshold:** 100% of the time upon result render.
**Condition:** When the API completes and the UI moves from loading to the final verdict.
**Method:** Run a test URL with a screen reader active or manually inspect the DOM to make sure the results container uses `aria-live="polite"`.

### NFR-ACC-03 — Semantic Form Labels
**Priority:** Must
**Requirement:** The main URL input field will need to be associated with a descriptive text label.
**Metric:** Percentage of form inputs with an associated `<label>`.
**Threshold:** 100%.
**Condition:** On the primary URL submission form.
**Method:** Manual DOM inspection in browser developer tools to make sure the `<label for="url-input">` matches the `<input id="url-input">`.

## Rep 6: Contrast and Grayscale

**Simulated Grayscale & Contrast Failures:**
1. **Color-Only Severity:** If a URL comes back as dangerous and the UI only turns the background red without specifically writing "Unsafe" or showing a warning icon, a user with red-green colorblindness will not understand what is going on. 
2. **Low Contrast Text:** A bright lime green "Safe" on a white background would probably fail the contrast ratio, which would make the text unreadable.

**Accessibility Requirements (NFRs):**

### NFR-ACC-04 — Text Contrast Ratio
**Priority:** Must
**Requirement:** All body text and important UI text will have a contrast ratio of at least 4.5:1 against whatever background it is on.
**Metric:** Contrast ratio.
**Threshold:** >= 4.5:1.
**Condition:** Over all UI states and result displays (Safe/Unsafe).
**Method:** Run a WCAG contrast checker tool on the specific hex codes used for the green/red text against the background color.

### NFR-ACC-05 — Color Independence
**Priority:** Must
**Requirement:** The system shall never convey information, severity, or state changes by color alone.
**Metric:** Occurrences of color-only information.
**Threshold:** Exactly 0.
**Condition:** During the display of the final scan verdict.
**Method:** Set the operating system display to grayscale and complete the core URL scan flow; verify that the text explicitly communicates the result without relying on the green or red hues.


## Rep 7: The Prohibitions, and the History Check

**Security Prohibitions:**
* `NFR-SEC-01` (Must) — No credential, API key, or token shows up in the repo at any point.
* `NFR-SEC-02` (Must) — The system stores 0 bytes of user-specific scanned URL history to the server or database.

**History Check Result:**
Ran the history scanner on the repo and came back with nothing. The history is clean of secrets. I'm pretty sure I had a false positive, however.

**Definition of Done Addition:**
To make sure this doesn't happen in the future, I will be adding this exact line to my Definition of Done: "No secret, key, or real user data was added to the repo."


## Rep 8: Constraints, Assumptions, and Dependencies

### Constraints (Limits I did not choose and cannot change)
| ID | Constraint | Source | What it rules out |
| :--- | :--- | :--- | :--- |
| **CON-01** | ~57 hours of effort across 16 weeks | Course | Complex custom UI frameworks or massive scope expansions |
| **CON-02** | Solo developer | Course | Any plan that relies on different workstreams or pair programming |
| **CON-03** | Zero budget for paid services | Course/Self | Premium VirusTotal API tiers or paid hosting plans |
| **CON-04** | Stateless architecture | Project Charter | User accounts, consistent relational databases, or login systems |

### Assumptions (Bets that need to be verified)
| ID | Assumption | Owner | Verify by | If it is false |
| :--- | :--- | :--- | :--- | :--- |
| **ASM-01** | VirusTotal free tier limit (4 calls/minute) is good enough for a demo | Me | Week 5 | Build a queue or be able to reject rapid requests |
| **ASM-02** | Free hosting tier keeps the app reachable for a live demo | Me | Week 5 | Demo run locally and record a fallback video |
| **ASM-03** | Non-technical employees will know the Safe/Unsafe UI | Me | Week 9 | Redesign the result messaging and color scheme |

### Dependencies (Outside code/services that will eventually fail)
| ID | Dependency | Pinned | Failure mode | Fallback |
| :--- | :--- | :--- | :--- | :--- |
| **DEP-01** | VirusTotal API | v3 | Rate limit exceeded or API issues | System displays "Scan currently unavailable" without completely shutting down |
| **DEP-02** | Web Hosting Provider | Free Tier | Service goes down while doing my demo | Run the app through localhost |


## Rep 9: Verify One Obligation at the Source

| Obligation | Source URL | Date Checked | What it requires of me |
| :--- | :--- | :--- | :--- |
| **VirusTotal Data Sharing (Free Tier)** | `https://docs.virustotal.com/docs/historic-privacy-policy` | 2026-09-10 | Any URL submitted through the free API is stored in the VirusTotal Corpus and shared with global security partners. I will have to warn users not to submit proprietary or private internal URLs so that they are at the very least aware. |


## Rep 10: The Enumeration Pass, and the Cull

**New Privacy Requirement (Given to me by AI):**
*`NFR-PRI-01` (Must) — The UI shall display a clear, visible disclaimer immediately adjacent to the submit button stating: "Warning: URLs scanned here are shared publicly with third-party security researchers. Do not submit internal or proprietary company links."
    * **Metric:** Presence of disclaimer text.
    * **Threshold:** 100% visibility on the main form.
    * **Condition:** On page load for all users.
    * **Method:** Manual visual inspection of the deployed URL input form.