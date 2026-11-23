# Run Sheet — 30-Minute Capstone Talk (Phishing URL Scanner)

Contract with the clock for the live 30-minute capstone presentation (`v1.0.0`).
Total planned time: **30:00** (26.5 minutes spoken content + 3.5 minutes reserved for Questions).

## Run Sheet

| # | Section | Min | Cum | Slides | Key line (say this even if behind) | Behind? |
|---|---|---:|---:|---|---|---|
| 1 | Hook + what it is | 1.5 | 1:30 | 1–2 | "Phishing URL Scanner checks suspicious links for security reviewers and employees and tells them whether a website is safe." | KEEP |
| 2 | Problem + user | 3.0 | 4:30 | 3–4 | "Corporate employees and IT helpdesk staff encounter suspicious links daily, and pasting internal URLs into public web tools leaks sensitive destinations." | KEEP |
| 3 | Scope: committed vs. cut | 2.5 | 7:00 | 5–6 | "I committed to all Must-have requirements across input validation, SSRF protection, and VirusTotal evaluation, and deliberately deferred redirect unshortening (`B-01`) and disk logging (`B-04`) to `v1.1`." | KEEP |
| 4 | Architecture picture | 3.0 | 10:00 | 7–8 | "Three components in one process—static web UI, FastAPI validation/SSRF boundary, and VirusTotal v3 client—with zero database persistence (`CON-04`)." | KEEP |
| 5 | The two decisions that mattered | 3.0 | 13:00 | 9–10 | "ADR-0005 and ADR-0003: zero database persistence protects user privacy (`CON-04`), and a 300-second in-memory TTL cache keeps us under VirusTotal's 4-requests-per-minute free-tier limit." | CUT ADR-0003 |
| 6 | Live demo | 6.5 | 19:30 | 11–12 | "Watch a single scripted pass verify a safe domain, flag a malicious fixture, and block an intranet SSRF attempt (`HTTP 422`)." | KEEP |
| 7 | Evidence: tests, defects, hours | 3.5 | 23:00 | 13–15 | "Seventy-one automated tests passing with zero skips, 100% of logged defects resolved or documented, and every hour tracked across 15 weeks in `docs/hours-log.csv`." | KEEP |
| 8 | What did not get done | 1.5 | 24:30 | 16 | "Recursive redirect unshortening (`FR-EVAL-03`) and opt-in server audit logging (`FR-SYS-02`) remain unbuilt because of SSRF/timeout budgets and privacy constraint `CON-04`." | KEEP |
| 9 | Lessons / next 240 hours | 2.0 | 26:30 | 17–18 | "Clean-room testing caught three copy-paste documentation defects before release, and the groomed top five backlog items in `docs/handoff.md` start with `ISSUE-DOC-04`." | CUT |
| 10 | Questions | 3.5 | 30:00 | 19 | "Repository, tagged release `v1.0.0`, and back-pocket traceability slides are ready for questions." | KEEP |
| | **Total** | **30.0** | **30:00** | **19** | | |

---