# Scoping Decision — Phishing Verification Platform

**Author:** Caleb Fuller  ·  **Date:** 2026-08-31  ·  **Course week:** 2

---

## 1. Problem

For everyday corporate employees who face ambiguous internal and external emails, the problem is accidentally following malicious links or wasting time trying to figure out spoofed messages, which costs real dollars in incident remediation and lost productivity. Today they manually reread messages, guess based on past training, or escalate directly to the helpdesk, which falls short because it relies on fallible human memory and takes up valuable staff time for routine triage.

## 2. Evidence a user exists

Interviewed Corporate Employee on 2026-08-29, 10 minutes, past-tense questions only.
Full write-up in `docs/interviews/2026-08-29-interview.md`.

- "However, after looking at it for a bit longer, it was harder to tell whether or not it was a phishing email."
- "There are a few, however, that look like they are coming from inside the company and I have no clue whether it is real."
- "So, I end up taking extra time or have to bother IT about whether or not it’s real."

## 3. Chosen scope — Must features

| # | Feature | Hours |
|---|---|---:|
| 1 | User Input & Validation UI | 8 |
| 2 | VirusTotal API Integration | 14 |
| 3 | Risk Scoring Engine | 15 |
| 4 | Plain-English Results Dashboard | 10 |
| | **Feature total** | **47** |
| | Walking skeleton + continuous integration | 6 |
| | Deployment + clean-machine test | 4 |
| | **Construction total** | **57** |

Plan: 60 hours. Hard ceiling: 75. My number: 57. This leaves 3 hours of planned slack; if that is taken up, I will reduce the styling complexity of the results dashboard to stay under the ceiling.

## 4. Should features — built only if there is room

1. **URLScan.io Fallback API (12 hours, Week 11):** Secondary verification. This is cut first when I fall behind.
2. **Historical Scan Log (8 hours, Week 12):** Local browser storage of past checked links. Cut second.

## 5. Out of scope — will not be built

Active directory integration · Browser extension · Mobile app version · Custom email client · Real-time inbox quarantine · Automated IT ticket creation · User login accounts.

## 6. Accepted tradeoffs

I am using a single security vendor (VirusTotal) instead of a consensus model. This costs the user a wider safety net if a new threat isn't in that specific database yet. I accepted it to keep the project under the 60-hour construction budget and reduce novelty load. I will revisit this if the single API fails to catch 80% of test cases during the elaboration phase.

## 7. Rejected candidates

**Rejected: Candidate B (Open-Source Vulnerability Scanner).** Passed the 60-hour sizing gate (46 hours) but was rejected because it solved a developer problem instead of addressing the issues of everyday corporate end-users. Deferred.

**Rejected: Candidate C (Password Hygiene Auditor).** Passed the sizing gate (41 hours) but was rejected because the scope felt too small to defend for a full 16-week engineering project, and k-anonymity hashing did not have the user-facing UI challenge I want to tackle. Closed, not deferred.

## 8. Hour budget, reconciled

| Weeks | Phase | Hours |
|---|---|---:|
| 1–2 | Inception | 30 |
| 3–4 | Requirements | 30 |
| 5–6 | Design | 30 |
| 7 | Planning | 15 |
| 8 | Design review + midterm | 15 |
| 9–12 | Construction + verification | 60 |
| 13 | Documentation | 15 |
| 14 | Deployment + handoff | 15 |
| 15–16 | Presentation + delivery | 30 |
| | **Total** | **240** |

My construction total fits safely under the 60-hour plan because I chose to cut the secondary URLScan.io API integration during the Rep 11 scope cut to save ~12 hours.

## 9. The one hard part

The one hard part will probably be mapping the technical VirusTotal JSON attributes to one, plain-English risk score. This means I will need to translate arbitrary threshold values (like vendor flags and community votes) into a specific boolean decision that an everyday employee can trust without needing to have a background in IT.

## 10. Risks and the scope-cut trigger

| Risk | Likelihood | What it costs me | Early warning sign |
|---|---|---|---|
| CI/CD API Rate Limiting | High | Broken pipelines and paused testing | VirusTotal gives back an HTTP 429 status code during automated GitHub Actions runs. |
| The UI Iteration Trap | High | Wasted hours tweaking CSS instead of logic | Spending more than 3 consecutive hours adjusting the results dashboard layout. |
| API Key Leaks | Medium | Revoked keys and deployment delays | Failed deployment builds on GitHub Actions due to authentication errors. |

**Scope-cut trigger.** If the main VirusTotal API integration is not returning live data in the deployed environment by 2026-10-16, I will cut the detailed JSON breakdown view first, then the visual risk meters. Decided now, in advance, so I do not have to decide it while panicking.

---

**Signed:** Caleb Fuller, 2026-08-31
**AI use for this document:** Prompted LLM to synthesize the previous days' interview notes, hour estimations, and pre-mortem risks into the required course template. I kept the generated risk tables and hour calculations. Logged in `docs/ai-usage-log.md`.