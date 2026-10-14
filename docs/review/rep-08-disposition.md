# Rep 8: Defect Disposition Report

**Log File:** `docs/review/defect-log.csv`  
**Total Findings Logged:** 19  

---

## 1. Breakdown by Severity and Disposition

| Severity | Fix Now (Week 8) | Deferred (Week 10) | Rejected | Total |
| :--- | :---: | :---: | :---: | :---: |
| **Critical** | 0 | 0 | 1 (`DR-015`) | **1** |
| **Major** | 5 (`DR-001`, `DR-002`, `DR-004`, `DR-009`, `DR-013`) | 1 (`DR-010`) | 1 (`DR-017`) | **7** |
| **Minor** | 10 (`DR-003`, `DR-005`, `DR-006`, `DR-007`, `DR-008`, `DR-011`, `DR-012`, `DR-014`, `DR-018`, `DR-019`) | 0 | 1 (`DR-016`) | **11** |
| **Total** | **15** | **1** | **3** | **19** |

* **Active Rework Set (Due Week 8):** 15 defects (all reworked and verified).
* **Carried Open / Deferred (Due Week 10):** 1 defect (`DR-010`).
* **Rejected:** 3 defects (`DR-015`, `DR-016`, `DR-017` with written technical justifications).

---

## 2. The Disposition I Am Least Comfortable With

**Finding:** `DR-010` — *VT API v3 has a difference between submitting a URL for re-analysis and fetching an existing cached report; polling the analysis ID on an already-scanned URL burns analysis quota unnecessarily.*  
**Disposition:** **Deferred** (Due Week 10 under `CR-001`).

### Rationale
Deferring `DR-010` is technically uncomfortable because it leaves an inefficiency in place during Week 9 testing: every URL scan will make a full submission and polling request against VirusTotal, burning 2 requests out of our 4 req/min limit even if the URL was scanned five minutes earlier. 

However, implementing cached report lookups requires branching execution paths (`GET /urls/{id}` $\rightarrow$ check for 200 vs 404 $\rightarrow$ fallback to `POST /urls`). Attempting to build that dual path during Week 9 risks missing the Walking Skeleton gate (`T-1.1`–`T-1.5`), which must prove end-to-end connectivity first. Deferring `DR-010` to Week 10 under formal change control (`CR-001`) protects the build sequence, but leaves an operational rate-limit penalty in place for one week.