# Definition of Done

## What this is

One checklist. It applies to **every** work item — every card, issue, or task — before that item may be moved to Done. It is not a plan and it is not per-feature acceptance criteria; those live with each requirement in `docs/requirements.md`.

## The honesty rule

If you will not do an item every single time, take it off the list. A definition of done that you routinely skip is worse than no definition of done, because it teaches you that written commitments are decorative.

Eight to twelve items. Every item must be answerable **yes or no** by someone who is not you.

---

## The checklist

An item is Done when all of the following are true:

- [ ] It points to a requirement ID in `docs/requirements.md`, and `docs/traceability.csv` is updated so `check-traceability.py` still brings back 0 blockers.
- [ ] Every acceptance criterion for that requirement goes, checked by running it manually locally.
- [ ] No secret, API key, token, or real user data shows up in the repository.
- [ ] Error paths are dealt with: the biggest issue a user is most likely to hit gives a message that names what failed.
- [ ] New user-facing updates are keyboard-operable, labeled, and pass the 4.5:1 contrast check.
- [ ] Any behavior change a random person would need to know shows up in `README.md` or `docs/requirements.md`.
- [ ] Any use of an AI assistant is recorded in `docs/ai-usage.md`, and every generated line was read and made sense.
- [ ] Time worked on the project is written to `docs/hours-log.csv` right after.
- [ ] The thing made is run through once end to end from a clean state without giving any exceptions.
- [ ] The task card in GitHub is moved to 'Done' to keep up with the work schedule.
- [ ] The code is merged and pushed to GitHub.

---

## What a bad definition of done looks like

Keep this next to yours as a warning:

- [ ] It works.
- [ ] Code is clean.
- [ ] Tested.
- [ ] Documented if needed.

Every one of these is unverifiable by anyone but the author, which means the list enforces nothing. "If needed" is where documentation goes to die.

---

**Adopted:** 2026-09-14 **Revised:** <YYYY-MM-DD, with a one-line reason>
