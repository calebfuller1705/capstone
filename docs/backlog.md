## B-04 — Server-Side Action Audit Logging (`FR-SYS-02`)
* **Original Requirement:** FR-SYS-02 — Action Logging (Should)
* **Deferred From:** Week 12 Scope Cut (CR-005, 2026-11-06)
* **Estimated Effort:** 5.0 h
* **Destination:** Post-Capstone Release v1.1
* **Retained Acceptance Criteria:**
  - Given the API returns a risk score, when the system computes the final verdict, then it appends a new line to a local text file containing the domain and the score.
  - Given the backend encounters an API error, when the error occurs, then it appends a new line to a local text file recording the error code.
* **Prerequisites for Implementation:** Requires dedicated disk volume provisioning, file rotation policies, and formal re-evaluation against privacy constraint CON-04 and zero-retention guarantee NFR-SEC-02.