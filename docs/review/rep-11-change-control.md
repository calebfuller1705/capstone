# Rep 11: Change Control Governance & Threshold Rule

## The Five Changes That Require a Formal Change Request (CR)
1. **Must Requirement Alteration:** Any addition, deletion, or material rewording of a Must requirement in `docs/requirements.md` (e.g., shifting `NFR-USE-01` or changing validation criteria).
2. **Interface or Contract Modification:** Any modification to HTTP verbs, endpoint routes, JSON request/response keys, status codes, or error envelope structures in `docs/architecture.md`.
3. **Budget or Schedule Deviation:** Any shift in weekly schedule gates or any work package scope adjustment exceeding 4.0 cumulative hours.
4. **Technology Stack Change:** Any swap of backend framework, hosting platform, CSS architecture, or third-party API provider (e.g., switching from Render to Fly.io, or replacing FastAPI).
5. **Definition of Done Changes:** Any alteration to quality criteria, required test coverage, or linting gates in `docs/definition-of-done.md`.

## The One Kind of Change That Deliberately Does Not
* **Internal Implementation Mechanics & Code Refactoring:** Optimizing private helper function signatures, variable naming, comment clarifications, typographical fixes in documentation, or adding unit test cases that verify existing contracts. These require only a standard git commit with a clear commit message.