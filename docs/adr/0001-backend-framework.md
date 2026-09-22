# ADR 0001 — Backend Framework Selection

- **Status:** Accepted
- **Date:** 2026-09-22
- **Decider:** Caleb Fuller
- **Requirements affected:** CON-01, CON-02, CON-04, NFR-SEC-01
- **Related ADRs:** None

## Context

The URL Security Scanner needs to work as stateless architecture (CON-04) to fit in a strict 57-hour budget by a solo developer (CON-01, CON-02). The backend's main structural responsibility is to securely hold the VirusTotal API key (NFR-SEC-01), take a URL from the frontend, pass it to the external API, and return the raw JSON results without storing any session data or database state. 

Because the frontend will be written in Vanilla HTML/JS with a novelty load of zero, I have the ability to spend one "Innovation Token" on the backend. While I have built multi-route HTTP web servers using Flask before (meaning a zero-hour learning curve), Flask is becoming viewed as the long-term route in 2026 job markets for API-only backends. My secondary project goal is to help built job-board relevance and employability, which leads me toward modern, async-first frameworks. The decision depends on whether the employability benefits of a modern framework are greater than the strict 57-hour time budget risk of a new technology.

## Options considered

| Option | Weighted score | The detail that decided it |
|---|---:|---|
| FastAPI | 4.20 | Gives support for stateless API routes, auto-generated OpenAPI documentation, and high growth in 2026 job data. |
| Flask | 4.15 | No learning curve, but requires manual JSON formatting and is less prevalent when it comes to modern API-centric job postings. |

## Decision

I will use FastAPI for the backend HTTP routing. It barely outscored Flask by 0.05 points. I am choosing to take on the novelty load of a new framework because the built-in Pydantic serialization supports the stateless API requirement that I have (CON-04) better than Flask, and it will help my employability goals.

## Consequences

**Positive**
- Fully satisfies CON-04 (stateless architecture) without extra middleware.
- Makes sure the VirusTotal API key is never exposed to the client browser (NFR-SEC-01).

**Negative**
- Puts my novelty load count at 1.
- Brings new syntax concepts I have not built before, specifically Python `async`/`await` patterns and Pydantic schema validation.

- **Mitigation:** I have put in 4 explicit learning hours in my Work Breakdown Structure that is for FastAPI routing and Render deployment spikes, stopping the risk from hurting feature development.

## Revisit trigger

If I cannot successfully make a basic FastAPI route to the Render free tier and receive a `200 OK` JSON response within 4 total hours of active development/spiking, I will stop and fall back to Flask to protect the 57-hour budget.

## Verification

| Claim in this ADR | Source | Checked on |
|---|---|---|
| FastAPI is free for commercial/academic use (MIT License) | [FastAPI GitHub License](https://github.com/tiangolo/fastapi/blob/master/LICENSE) | 2026-09-22 |
| FastAPI is deployable on Render Web Services | [Render FastAPI Docs](https://render.com/docs/deploy-fastapi) | 2026-09-22 |