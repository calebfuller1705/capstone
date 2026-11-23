# Deck Outline — 20 Slides for 30 Minutes (`v1.0.0`)

Target: 20 main slides (ceiling 22) + 4 back-pocket Q&A slides, exported to `docs/presentation/deck.pdf`.

| # | Slide | The one thing on it | Sourced from |
|---|---|---|---|
| 1 | Title | Phishing URL Scanner, Caleb Fuller, one-line description, November 2026 (`v1.0.0`) | `README.md` |
| 2 | What it is | One sentence, 19 words, zero jargon | `docs/presentation/one-liner.md` |
| 3 | The problem | Phishing triage risk + privacy leak in public scanners | `docs/requirements.md` §1–2 |
| 4 | Who it is for | Corporate Employee, IT Helpdesk Analyst, Technical Maintainer | `docs/requirements.md` §2 |
| 5 | What I committed to | 100% of Must-have requirements (`FR-INP`, `FR-EVAL`, `FR-ACT`, `CON-04`) | `docs/requirements.md` |
| 6 | What I cut, on purpose | `B-01` redirect unshortening (`CR-003`), `B-04` disk logging (`CR-005`), user accounts (`CON-04`) | `CHANGELOG.md` & `docs/backlog.md` |
| 7 | Architecture | Single-process context/component diagram (Browser UI -> FastAPI SSRF guard -> VirusTotal v3) | `docs/architecture.md` |
| 8 | The data model | Stateless zero-DB model (`ADR-0005`), `ScanRequest`/`ScanResponse`, 300s RAM TTL cache | `src/api/schemas.py` & `ADR-0005` |
| 9 | Decision 1 (`ADR-0005`) | Stateless zero-persistence design vs. SQLite/Postgres | `docs/adr/0005-empty-sql-migration-sentinel.md` |
| 10 | Decision 2 (`ADR-0003`) | Single-worker Uvicorn + 300s TTL cache vs. multi-worker cloud hosting | `docs/adr/0003-hosting-provider.md` |
| 11 | The hard part | Cutting `POST /scan` p95 from `1083.40 ms` to `184.22 ms` via connection pooling + cache | `docs/performance.md` |
| 12 | Demo agenda | Three scripted checks: Safe URL (`200`), SSRF intranet block (`422`), length boundary + copy | `docs/presentation/demo-script.md` |
| 13 | **DEMO** | Solid dark/black slide during live execution | `docs/presentation/demo-script.md` |
| 14 | Verification | 71 of 71 automated tests passing (`0` skipped) + front-end coverage gap noted | `pytest tests/ -v` |
| 15 | Defects | 8 logged (`1` fixed `DEF-001`, `7` open, `0` S1 critical; worst open `DEF-002` S2) | `docs/defect-log.md` |
| 16 | Non-functional evidence | `POST /scan` p95 = `184.22 ms` (`< 500 ms` `NFR-PERF-01`) over 50 volume-seed requests | `docs/performance.md` |
| 17 | What did not get done | `FR-EVAL-03` (`B-01`, ~4 h), `FR-SYS-02` (`B-04`, ~5 h), `B-06` LRU cache (~2 h) | `docs/backlog.md` |
| 18 | Hours, honestly | `197.75 h` across 78 sessions (`2026-11-17`) + clean-clone contract debugging overrun (`3.75 h`) | `docs/hours-log.csv` |
| 19 | If I had 240 more hours | Ranked top 3 from `docs/handoff.md`: `ISSUE-DOC-04` (1 h), `B-01` (4 h), `B-06` (2 h) | `docs/handoff.md` §2 & §5 |
| 20 | Questions | `github.com/calebfuller1705/capstone` (`v1.0.0`), `docs/handoff.md`, contact info | `README.md` |
| 21–24 | Back-pocket slides | Full requirements traceability, risk register, `docs/ai-usage.md` summary, `THIRD-PARTY-NOTICES.md` | `docs/` |