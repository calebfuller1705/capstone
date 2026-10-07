# Design Review Brief: URL Security Scanner

**Target:** Senior Capstone Architectural Phase Gate (Milestone 8 Baseline)  
**Materials Pinned:** Tag `spec-review-candidate` (Commit: `HEAD`)  
**Time Box:** 45 minutes reading, 45 minutes walkthrough session  

---

### 1. Bounded Reading Scope (Focus Areas Only)
Please read exclusively the following core sections (approximately 7 pages total):
* `docs/requirements.md`: Section 5 (Functional Requirements) and Section 6 (Non-Functional Requirements).
* `docs/architecture.md`: Section 4 (Container & Component Architecture), Section 5 (API Contracts & VirusTotal Polling Sequence), and Section 6 (Error Envelopes & Degradation Strategy).
* `docs/risk-register.md`: Top 5 Risks (`R-01` through `R-05`).

*You can ignore:* Styling choices, repository folder naming, and historical retrospectives from Weeks 1–3.

### 2. Review Checklist Areas
Evaluate the materials against Areas 1–3 of the standard review checklist:
1. **Requirements Completeness & Verifiability:** Are acceptance criteria unambiguous and measurable?
2. **Interface Contracts & Sequence Flows:** Are request/response payloads, HTTP status codes, and timeouts completely specified?
3. **Failure Path & Degradation:** What happens when the upstream VirusTotal API fails, times out, or returns a 429?

### 3. The Core Question I Need Answered
> **"Does the separate architecture guarantee that upstream VirusTotal 429 rate limits (4 requests/min) and 10-second polling timeouts are safely handled by the FastAPI backend without blocking worker threads, leaking secrets, or causing unhandled UI exceptions?"**

### 4. What We Are NOT Asking For
* **Styling and CSS aesthetics:** The frontend is deliberately minimal and functional.
* **Technology stack alternatives:** The choice of FastAPI, Vanilla JS, and Render is settled via Architecture Decision Records (`ADR-001` through `ADR-004`).
* **Document formatting or prose style:** Focus strictly on structural defects, missing error cases, and unbuildable interfaces.

### 5. Feedback Format
Log each finding as a single line:
`[Document & Section] | [Requirement ID or "None"] | [Defect Description] | [Severity: Critical / Major / Minor]`

*During our walkthrough, I will not debate findings.*