# ADR 0003 — Hosting Provider Selection

- **Status:** Accepted
- **Date:** 2026-09-22
- **Decider:** Caleb Fuller
- **Requirements affected:** CON-01, CON-03
- **Related ADRs:** ADR 0001 (Backend Framework)

## Context

The application needs to be accessible through public internet for grading, but runs under a zero-dollar budget (CON-03). Because the solo developer time budget (CON-01) is highly compacted, the chosen host must let me do automated deployments directly from a Git repository to save wasting hours on manual server configurations.

## Options considered

| Option | Weighted score | The detail that decided it |
|---|---:|---|
| Render | 4.40 | Native CI/CD integration that runs a Python web service automatically with a GitHub push. |
| PythonAnywhere | 3.20 | Needs manual logging into a browser-based bash console to pull updates and restart the server. |

## Decision

I will use Render's Free Web Service tier to host the backend. It outscored PythonAnywhere mainly because of its modern deployment pipeline, which reduces the operational overhead during the development cycle by a lot.

## Consequences

**Positive**
- Fully satisfies CON-03 ($0 budget).
- Automates the CI/CD pipeline, saving maybe 10-15 minutes per deployment.

**Negative**
- Render's free tier instances shut down after 15 minutes of inactivity. 
- The first request after a spin-down will take up to 50 seconds to respond while it reboots, which would result in a poor user experience for the grader.

**Mitigation:** I will document this cold-start latency in the project's `README.md` and other instructions so the user does not assume the application is broken. 

## Revisit trigger

If Render changes its free tier to require a credit card on file, or if the cold-start time consistently goes over 60 seconds (causing API timeout errors), I will abort Render and move to a local Docker deployment for the final demonstration.

## Verification

| Claim in this ADR | Source | Checked on |
|---|---|---|
| Render Free Tier includes 1 Web Service, spins down after 15m | [Render Pricing](https://render.com/pricing) | 2026-09-22 |