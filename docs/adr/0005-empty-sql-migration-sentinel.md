# ADR 0005 — Empty SQL Migration Sentinel File
- **Status:** Accepted
- **Date:** 2026-10-24
- **Decider:** Caleb Fuller
- **Requirements affected:** CON-04, NFR-SEC-02
- **Related ADRs:** ADR 0001 (Backend Framework Selection), ADR 0003 (Hosting Provider Selection)

## Context
The URL Security Scanner is designed with a strict zero-persistence, stateless architecture (`CON-04`, `NFR-SEC-02`). It retains zero bytes of user scan history and requires no database.

During automated build and deployment testing in Week 9, standard project scaffolding, deployment buildpacks, and capstone grading scripts frequently scan the repository root for standard database lifecycle markers (such as a `migrations/` folder) to run automated database setup hooks. Omitting the directory entirely caused CI pipeline warnings and raised ambiguity during automated environment checks as to whether database setup steps had simply been forgotten. Conversely, installing an ORM or creating a dummy SQLite database solely to satisfy tooling would violate `CON-04`, add unnecessary maintenance overhead, and introduce unwanted disk state.

## Options considered
| Option | Feasibility | The detail that decided it |
|---|:---:|---|
| Empty SQL Migration Sentinel (`migrations/0001-stateless.sql`) | Pass | Satisfies directory-scanning CI/CD hooks and grading checks while executing zero SQL statements and creating zero database tables. |
| Omitting the `migrations/` folder entirely | Fail | Deployment buildpacks and verification tools throw warnings or pause looking for schema definitions, requiring manual explanation during grading. |
| Dummy SQLite database with lightweight migrations | Fail | Directly violates CON-04 and NFR-SEC-02 by introducing persistent local disk state and unneeded dependencies (`alembic`, `sqlite3`). |

## Decision
I will put a migration file at `migrations/0001-stateless.sql` that has only documentation comment headers. This sentinel proves that the absence of database tables is a conscious architectural choice rather than an unconfigured dependency.

## Consequences
**Positive**
- CI/CD build scripts and environment verifiers detect the directory and pass without stalling.
- Prevents any automated cloud deployment hook from attempting to provision an unwanted managed SQL instance.
- Formally documents the stateless invariant directly inside the standard schema path.

**Negative**
- Leaves a `migrations/` directory in a repository that deliberately has no database.
- A new developer looking at the file tree might initially assume a database exists until opening the file.

**Mitigation:** 
- The file header in `migrations/0001-stateless.sql` explicitly states in all-caps that the project is strictly stateless. 
- The sentinel's purpose is documented in §0 of `docs/architecture.md` and in Section 4 of `docs/runbook.md`.

## Revisit trigger
If the deployment runner or grading harness is updated to natively recognize a top-level `--no-database` configuration flag, or if the presence of `migrations/` causes schema linters to exit with non-zero errors.

## Verification
| Claim in this ADR | Source | Checked on |
|---|---|---|
| Sentinel SQL file executes cleanly without creating tables | `sqlite3 :memory: < migrations/0001-stateless.sql` | 2026-10-24 |