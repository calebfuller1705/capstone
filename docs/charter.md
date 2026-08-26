# Project Charter — Caleb Fuller

**Owner:** Caleb Fuller · **Course:** Capstone · **Started:** 2026-08-24 · **Last revised:** 2026-08-26

## 1. Purpose

To establish a disciplined, professional engineering foundation and produce a complete software system accompanied by industry-standard documentation. By the end of the semester, a stranger will be able to clone the repository, run the application locally without errors, and read through the requirements, architecture, and handoff documents exactly as a professional team would expect.

## 2. Project (filled in Week 2, after the scoping decision)

- **One-sentence description:** <fill in Week 2>
- **Primary user:** <fill in Week 2>
- **The one thing it must do to be worth finishing:** <fill in Week 2>

## 3. Capacity and constraints

| Constraint | My reality |
|---|---|
| Hours available per week | 15 hours maximum |
| Total hours budgeted | 240 |
| Weeks that are already broken (and where those hours move) | **Week 8 (Midterms):** Move 5 hours forward to Wk 7. <br>**Week 14 (Thanksgiving):** Move 6 hours forward to Wk 13. |
| Machine (OS, RAM, disk) | Personal Windows Laptop |
| Administrator rights on that machine? | Yes |
| Money I will spend on this project | $0.00 (Strictly using free tiers for hosting/services) |
| Technologies I already know well | Python, Java, Git, HTML/CSS, Microsoft SQL Server |
| Technologies I am willing to learn (max two) | TBD after Week 2 scoping decision |
| Hard external deadlines besides this course | Midterms (Week 8) and Thanksgiving travel (Week 14) |

## 4. Definition of finished

- All 16 weeks of the Hat Map artifacts are completed and committed to the `docs/` folder.
- The repository passes a clean-clone smoke test on a new machine.
- The application can be run locally using only the instructions provided in the README.
- The total logged hours in `hours-log.csv` are within 10% of the 240-hour budget.

## 5. Non-goals — what I will NOT build or do

1. **No mobile client:** I will only target a desktop web browser. I will build on my existing knowledge of web routing and HTML templates, and I will not spend this semester learning Swift or Kotlin.
2. **No new primary database engine:** I will use a single relational database I am already familiar with, such as Microsoft SQL Server. I will not attempt to learn and integrate a NoSQL database like MongoDB.
3. **No custom interaction design from scratch:** I will use a standard component library or CSS framework. I will not spend time building complex, layered wireframes in tools like Axure RP.
4. **No real-time communication features:** The application will rely on standard HTTP request/response cycles. I will not implement WebSockets, live chat, or real-time push notifications.
5. **Strict 15-hour weekly limit:** I will not borrow time from my personal life. When the 15 project hours are up for the week, capstone work stops until Monday.

## 6. Risks to me finishing

| # | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Early warning sign | What I will do |
|---|---|---|---|---|---|
| R1 | Losing time to complex environment/cloud deployments | M | H | Spending >2 hours debugging server or deployment configuration | Fall back to local execution and basic data storage (e.g., SQLite) immediately. |
| R2 | Falling behind capacity due to midterm studying in Week 8 | H | M | Missing a scheduled capstone work block in Week 7 or 8 | Enforce the pre-planned hour shift and cut a "nice-to-have" UI feature to regain time. |
| R3 | UI design taking too much time to polish | M | M | Writing custom CSS instead of using standard components | Strictly use an off-the-shelf CSS framework and stop tweaking visual layouts. |

## 7. Working agreement

- **Sessions:** Mon/Wed 1:30-4:30 PM, Thu 1-4 PM, Fri 1-4 PM
- **Logging:** every session ends with a row in `docs/hours-log.csv`, written before I close the laptop.
- **Board:** work-in-progress limit of 2; nothing moves to Done without its stopping condition met.
- **Commits:** requirement identifier first in the subject line; one logical change per commit.
- **When I fall behind, I cut in this order:** 1. UI Polish, 2. Secondary features, 3. Automated test coverage (falling back to manual testing).
- **AI use:** governed by `docs/ai-usage.md`; every Amber-zone use is logged the day it happens.

## 8. Signature

I have counted the cost of this work as honestly as I can today, and I accept the schedule above.

**Caleb Fuller**