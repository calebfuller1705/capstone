| **CR-005** | 2026-11-06 | Defer server action logging to local disk | FR-SYS-02 | -5.0 | Deferred (Backlog: B-04) |

## [Unreleased]

## [1.0.0] - 2026-11-20

### Added
- Complete successor handoff package (`docs/handoff.md`), deployment runbook (`docs/deployment.md`), and release checklist (`docs/release-checklist.md`) for `v1.0.0` release.
- Automated startup guards (`validate_startup_config()` placeholder key rejection with `CI=true` exemption) and stateless migration sentinel verification (`tests/unit/test_tribal_guards.py`).
- Third-party license inventory (`THIRD-PARTY-NOTICES.md`) covering all 59 pinned packages with explicit `SPDX-License-Identifier: MIT` declarations.

### Changed
- Upgraded automated test suite from 60 to 71 passing unit, integration, security, and acceptance tests (`requirements.lock` pinned).
- Updated application metadata (`src/api/main.py`) and operational documentation (`README.md`, `docs/runbook.md`) to `v1.0.0`.

### Fixed
- Resolved copy-paste setup and verification blockers (`ISSUE-DOC-01` through `ISSUE-DOC-03`) discovered during the clean-room successor simulation (`README.md`).
- Fixed GitHub Actions CI smoke-test startup check so `CI=true` runs boot cleanly while local placeholder keys fail fast.

### Known issues
- `KI-001` / `B-01` (Low): Shortened URLs (`bit.ly`, `tinyurl.com`) evaluate the shortener domain rather than tracing redirects (deferred to `v1.1` via `CR-003`).
- `B-04` (Low): Server-side file logging remains disabled per zero-persistence privacy constraint `CON-04` (deferred to `v1.1` via `CR-005`).
- `ISSUE-DOC-04` (Low): `GET /favicon.ico` returns `404` in console logs (labeled `good-first-issue` for successor onboarding).

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