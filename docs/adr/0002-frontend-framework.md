# ADR 0002 — Frontend Framework Selection

- **Status:** Accepted
- **Date:** 2026-09-22
- **Decider:** Caleb Fuller
- **Requirements affected:** CON-01, CON-02, NFR-ACC-01
- **Related ADRs:** ADR 0001 (Backend Framework)

## Context

The URL Security Scanner needs a web interface to take in user input and display security results. As a solo developer with a strict 57-hour budget (CON-01, CON-02) who has already spent the "Innovation Token" on learning FastAPI (ADR 0001), the frontend needs to have a zero novelty load. On top of that, the frontend must be 100% manual accessibility compliance (NFR-ACC-01) without needing complex framework-specific workarounds.

## Options considered

| Option | Weighted score | The detail that decided it |
|---|---:|---|
| Vanilla HTML/JS | 4.40 | Zero build pipeline required; allows me to do direct 1:1 authoring of semantic, accessible DOM elements. |
| React | 2.40 | Requires setting up a bundler (Vite), managing state, and learning JSX accessibility syntax, which could hurt me when it comes to my time budget. |

## Decision

I will use Vanilla HTML and JavaScript for the frontend. I am choosing to reject React, even with its prevelance in entry-level job postings, because the overhead of a build pipeline and state management goes over the time constraints of a solo capstone project.

## Consequences

**Positive**
- Zero compilation time and no build pipeline to maintain.
- Gives me complete control over HTML semantics for NFR-ACC-01 compliance.

**Negative**
- Takes out the opportunity to show React competency for future employers.
- Manual DOM manipulation (`document.getElementById`, etc.) can become messy if the UI grows in how complex it is.

**Mitigation:** I will strictly limit the UI scope to just one search input, a loading state, and a static results table, which limits the risk of DOM issues.

## Revisit trigger

If writing the manual JavaScript DOM updates takes up more than 8 hours of the Work Breakdown Structure, I will think about pulling in a lightweight library (like Alpine.js) to handle state.

## Verification

| Claim in this ADR | Source | Checked on |
|---|---|---|
| Vanilla JS requires no license or build tools | [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) | 2026-09-22 |