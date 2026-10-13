# Rep 7: Adversarial AI Review and Verification Report

**Input Package:** Pinned tag `spec-review-candidate`  
**Execution:** Hostile prompt pass focused on unhandled error states and interface omissions.  

## 1. Verification & Fabrication Analysis

* **Total AI Findings:** 6
* **Confirmed Defects:** 3 (`DR-013`, `DR-014`, `DR-018`)
* **Rejected Findings:** 2 (`DR-015`, `DR-016`)
* **Fabricated Findings:** 1 (`DR-017`)
* **Fabrication Rate** 16.7%

### What This Means for Week 12
A 16.7% fabrication rate shows that even though an assistant is fast at finding boundary conditions (such as missing `http/https` scheme restrictions or client disconnects), it generates things that just aren't there with identical surface fluency. In `DR-017`, it invented Section 7.3 and requirement `FR-DAT-04` with complete confidence. 

During Week 12 construction and debugging, this means every AI-generated error diagnosis or code suggestion needs to be verified by opening the source code and reading the runtime stack trace. Looking at this unverified assistant response as authoritative gives me  hours spent fixing non-existent bugs or putting in phantom requirements.

## 2. Human vs. Assistant Defect Comparison

### The Human Finding Missed by AI
**Finding:** `DR-010` — *VirusTotal API v3 cached report lookup vs. analysis re-submission.*  
The human reviewer caught that submitting a URL to `/api/v3/urls` gives me an analysis ID that needs to be polled, but hashing the URL and making a direct `GET` to `/api/v3/urls/{id}` immediately retrieves any pre-existing report, saving quota. The assistant did not see this.

### Why the Assistant Could Not Have Found It
The assistant evaluates internal document consistency: it looks at whether Document A traces to Document B and whether the text matches typical software engineering patterns. Because my `docs/architecture.md` described a syntactically valid flow that matched `docs/requirements.md`, the model accepted the logic as sound. The assistant does not have operational experience with the third-party VirusTotal API's economic model. It has never used an active API quota in production, dealt with free-tier throttling, or combined with the actual endpoints. The human reviewer, having built real-world things with that, saw an inefficiency that no internal document cross-check could show.