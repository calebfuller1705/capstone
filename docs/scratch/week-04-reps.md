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