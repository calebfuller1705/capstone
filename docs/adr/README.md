# Architecture Decision Record (ADR) Index

This index tracks all significant architectural choices made across the life cycle of the URL Security Scanner. Decisions are immutable records of context, tradeoffs, and consequences at the time they were made.

| ADR | Decision | Status | Consequence you would notice |
|---|---|---|---|
| [0001](0001-backend-framework-selection.md) | FastAPI over Flask for backend HTTP routing | Accepted | Modern async-first routes and built-in Pydantic schema validation; requires managing `async`/`await` syntax and Pydantic validation exceptions. |
| [0002](0002-frontend-framework-selection.md) | Vanilla HTML/JavaScript over React for the web client | Accepted | Zero build pipeline, no bundler (Vite/Webpack), and instant loads; UI state updates require manual DOM manipulation (`document.getElementById`). |
| [0003](0003-hosting-provider-selection.md) | Render Free Web Service over PythonAnywhere | Accepted | Native Git-push CI/CD deployment automation; free-tier instances spin down after 15 minutes of inactivity, introducing an initial ~50s cold-start penalty. |
| [0004](0004-third-party-security-api-selection.md) | VirusTotal API v3 over Google Safe Browsing | Accepted | Immediate threat intelligence without maintaining an internal database; requires a two-step polling loop and adheres to a 500 req/day free public quota. |
| [0005](0005-empty-sql-migration-sentinel.md) | Empty SQL migration sentinel file over omitting migration directory | Accepted | Guarantees CI/CD deployment runners and course verification scripts do not fail or attempt to auto-provision a database; leaves a migration directory in a strictly stateless app. |