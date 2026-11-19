# Changelog

## Specification Changes Since Baseline v1.0

| CR | Date | Change | Requirements | Hours | Decision |
|---|---|---|---|---:|---|
| **CR-001** | 2026-10-14 | VirusTotal cache pre-check (`GET /api/v3/urls/{id}`) before polling | `FR-SYS-01`, `FR-API-02` | +2.0 | Approved (Sched: W10) |
| **CR-002** | 2026-11-06 | Quick-copy scan summary to clipboard | `FR-INP-01`, `NFR-USAB-01` | +1.5 | Approved (Sched: W12) |
| **CR-003** | 2026-11-06 | Batch CSV URL file upload | `FR-INP-01`, `FR-EVAL-01` | +10.0 | Deferred (Backlog: B-03) |
| **CR-004** | 2026-11-06 | User accounts and persistent scan history | `CON-04`, `NFR-SEC-02` | +14.0 | Rejected (Violates CON-04) |

## [Unreleased]

## [0.9.0-rc.1] - 2026-11-07

### Added
- URL safety evaluation: submitting a public domain returns an immediate Safe, Unsafe, or Ambiguous visual verdict card with positive engine counts (FR-INP-01, FR-UI-01, FR-UI-02, FR-EVAL-02).
- One-click clipboard copy: users can copy the final scan verdict text directly to their operating system clipboard for support tickets (FR-ACT-01, CR-002).
- Automatic protocol handling: URLs entered without an explicit `http://` or `https://` prefix default to HTTP instead of throwing an input validation error (FR-EVAL-04).

### Changed
- Configuration management: API keys are now loaded automatically from a local `.env` file via `python-dotenv`. Setup action required: copy `.env.example` to `.env`, set `VIRUSTOTAL_API_KEY`, and run `pip install -r requirements.txt` (FR-SYS-01, NFR-MNT-01).
- API timeout threshold: upstream queries abort after 5.0 seconds with an explicit timeout notice instead of hanging indefinitely (FR-API-02, NFR-PERF-01).

### Fixed
- Submitting URLs longer than 2,048 characters caused unhandled backend 500 crashes; now rejected at the boundary with an informative HTTP 422 length error (DEF-001, FR-INP-03).
- Submitting private intranet domains (such as `localhost` or `192.168.1.1`) returned unhandled network errors; now rejected with an explicit "Unscannable intranet URL" safety alert (FR-EVAL-01).
- Unhandled backend exceptions previously exposed raw internal tracebacks to the client browser; now sanitized to generic error feedback (NFR-SEC-01).

### Security
- Hardened SSRF boundary: blocked requests resolving to RFC 1918 private subnets, loopback interfaces, and cloud link-local metadata addresses (FR-EVAL-01, NFR-SEC-01).
- Zero data persistence audit verified: server disk and logs retain zero bytes of submitted URL strings or user session identifiers (CON-04, NFR-SEC-02).

### Known issues
- KI-001 (Low): Shortened URLs (e.g., `bit.ly`, `tinyurl.com`) evaluate the redirector domain rather than tracing through to the destination landing page. Workaround: Expand shortened links before scanning. Tracked in `docs/backlog.md` as B-01 for v1.1.

## [0.9.0-rc.2] - 2026-11-19

### Added
- Fail-fast startup configuration guard: `validate_startup_config()` in FastAPI's `lifespan` handler (`src/api/main.py`) and pre-flight checks in `script/start` abort server boot immediately with an actionable remediation message when `VIRUSTOTAL_API_KEY` is missing or blank (`FR-SYS-01`, `NFR-MNT-01`, `DEF-004`).
- Environment contract & drift detector: completed `.env.example` variable documentation and added `tools/check_config.py` to detect missing required keys or undocumented `.env` lookups before runtime (`FR-SYS-01`, `NFR-MNT-01`).
- Reproducible single-path setup & dependency lockfile: added `requirements.lock` (37 pinned packages), hardened `script/setup` with prerequisite checks and next-step output, and recorded ADR-0006 committing to `./script/setup` as the sole supported setup path (`NFR-MNT-01`).
- Outbound SPDX license (`MIT` in `LICENSE`), third-party dependency license inventory (`THIRD-PARTY-NOTICES.md` across 59 packages), and one-page operator handoff (`docs/handoff.md`) (`NFR-MNT-01`).

### Changed
- Dependency installation contract: `README.md` and `script/setup` now install strictly from pinned `requirements.lock` rather than floating `requirements.txt` (`NFR-MNT-01`).
- Secret hygiene & credential rotation: hardened `.gitignore` to exclude `.venv/`, `.env.*` variants (preserving `!.env.example`), `*.pem`, and `*.key`, and rotated the historical VirusTotal v3 API key exposed in commit `304cde0e` (`NFR-SEC-01`, `DEF-005`).

### Fixed
- Silent startup misconfiguration: eliminated delayed runtime `401`/`502` failures on `POST /scan` when `.env` was absent by failing fast at process startup (`DEF-004`, `FR-SYS-01`).
- Historical secret exposure risk: removed global Windows environment fallback reliance and rotated the compromised VirusTotal API key (`DEF-005`, `NFR-SEC-01`).

### Known issues
- KI-001 (Low): Shortened URLs (e.g., `bit.ly`, `tinyurl.com`) evaluate the redirector domain rather than tracing through to the destination landing page. Workaround: Expand shortened links before scanning. Tracked in `docs/backlog.md` as `B-01` for `v1.1`.
- KI-002 (Low): `docs/runbook.md` lacks a numbered tag-checkout rollback procedure (`F-06`), requiring operators to improvise `git checkout <tag>` during rollbacks until updated.