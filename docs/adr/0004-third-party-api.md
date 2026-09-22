# ADR 0004 — Third-Party Security API Selection

- **Status:** Accepted
- **Date:** 2026-09-22
- **Decider:** Caleb Fuller
- **Requirements affected:** FR-SYS-01, NFR-SEC-01
- **Related ADRs:** None

## Context

To make its primary system function (FR-SYS-01), the app needs to analyze user-submitted URLs against a known database of threats. Building and maintaining a threat intelligence database is not in the scope at all for a 16-week, solo-developer capstone project. Therefore, the threat analysis must come from a reliable third-party API that gives a good free tier.

## Options considered

| Option | Feasibility (SP-01) | The detail that decided it |
|---|:---:|---|
| VirusTotal API v3 | Pass | Successfully brought back malicious/harmless integer counts in under 1 second during SP-01. |
| Google Safe Browsing | Untested | Maintained as Plan B if VirusTotal rate limits is too restrictive. |

## Decision

I will pull in the VirusTotal v3 Public API for all threat analysis. Spike SP-01 showed that the API is responsive, the JSON structure is predictable, and the authentication token can be easily managed as a backend environment variable. 

## Consequences

**Positive**
- Instantly fulfills the core functional requirement (FR-SYS-01) without needing database architecture.
- The 500 requests/day free quota will be more than fine for development and grading.

**Negative**
- The v3 API needs a two-step asynchronous polling process for new URLs (submit URL, receive ID, query ID).

**Mitigation:** The frontend must need a loading indicator (FR-DASH-01) to accommodate the variable latency of the two-step API hop. I have put in 2 extra hours to handle the logic in FastAPI.

## Revisit trigger

If the VirusTotal API takes away my free-tier key, or if the API consistently returns HTTP 429 (Rate Limit) errors during routine testing, I will go to Plan B and rewrite the backend integration to use the Google Safe Browsing API.

## Verification

| Claim in this ADR | Source | Checked on |
|---|---|---|
| VirusTotal Public API allows 500 requests per day | [VirusTotal API Docs](https://docs.virustotal.com/reference/public-vs-premium-api) | 2026-09-22 |