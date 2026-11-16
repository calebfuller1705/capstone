#!/usr/bin/env python3
"""doc_lint.py — a blunt instrument for finding the documentation smells a grader will find first.

Usage:  python3 doc_lint.py README.md
        python3 doc_lint.py docs/runbook.md
        python3 doc_lint.py docs/operations.md --profile runbook

A README and a runbook are graded against different section lists, so the linter carries one
profile for each. The profile is picked from the filename — anything named like a runbook or
an operations doc gets the runbook list, everything else gets the README list — and
`--profile readme|runbook` overrides that guess when your filename does not give it away.

It is not a judge of prose. It catches the mechanical failures: missing sections, hand-waving,
hard-coded personal paths, unpinned prerequisites, leaked secrets, commands with no expected output.
Exit code 1 if any ERROR is reported. Clean output is necessary, not sufficient.
"""
import re
import sys

README_SECTIONS = [
    ("what it is / who it is for", r"what (this|it) is|about|overview|who (this|it) is for"),
    ("demo or screenshot", r"demo|screenshot|preview|in action"),
    ("prerequisites", r"prerequisit|requirement|before you (start|begin)"),
    ("install", r"install|setup|set up|getting started"),
    ("configure", r"config|environment variable|\.env"),
    ("run", r"\brun\b|usage|start"),
    ("test", r"\btest"),
    ("project layout", r"layout|structure|repository map|project tree"),
    ("troubleshooting", r"troubleshoot|common (problems|issues)|faq"),
    ("license", r"licen[sc]e"),
    ("contact", r"contact|author|maintainer|support"),
]

# A runbook is written for the operator at 2 a.m., not for the newcomer choosing a project.
# It is not supposed to have a demo, a licence, or a project layout, so it is not asked for them.
RUNBOOK_SECTIONS = [
    ("where it runs", r"where it runs|environment|deploy|where it lives|hosts?\b"),
    ("start, stop, restart", r"start|stop|restart|shut ?down"),
    ("health check", r"health|is it alive|smoke (test|check)|liveness"),
    ("routine operations", r"routine|operations|back ?up|restore|maintenance"),
    ("normal readings", r"normal|baseline|expected (load|readings|behavio)|what good looks like"),
    ("failure catalogue", r"failure|incident|when it breaks|troubleshoot|known (problems|issues)"),
    ("escalation", r"escalat|who to (call|contact)|on.?call|contact"),
    ("last verified", r"last verified|verified on|last tested|last reviewed"),
]

PROFILES = {"readme": README_SECTIONS, "runbook": RUNBOOK_SECTIONS}
RUNBOOKISH = re.compile(r"(?i)(runbook|run-book|operations|ops[_-]?guide|oncall|on-call)")

HAND_WAVING = [
    "just run", "simply run", "simply install", "should just work", "should work",
    "you're good to go", "youre good to go", "obviously", "easy", "as usual",
    "the usual way", "etc.", "and so on", "self-explanatory",
]

PERSONAL_PATH = re.compile(r"(/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|[A-Z]:\\\\?Users\\\\?)")
SECRETISH = re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_-]{12,}")
VERSIONISH = re.compile(r"\d+\.\d+")
EXPECTED = re.compile(r"(?i)expected|you should see|output:|prints|returns")


def report(kind, line_no, message):
    where = f"line {line_no}" if line_no else "document"
    print(f"{kind:<7} {where:<12} {message}")


def pick_profile(path):
    """Guess from the filename — not the whole path, or a repo in ~/operations/ fools it."""
    filename = path.replace("\\", "/").rsplit("/", 1)[-1]
    return "runbook" if RUNBOOKISH.search(filename) else "readme"


def main(path, profile=None):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as exc:
        print(f"cannot read {path}: {exc}")
        return 2
    profile = profile or pick_profile(path)
    sections = PROFILES[profile]
    print(f"profile: {profile} (override with --profile readme|runbook)\n")
    lines = text.splitlines()
    errors = 0

    headings = [ln for ln in lines if ln.lstrip().startswith("#")]
    heading_blob = "\n".join(headings).lower()
    for name, pattern in sections:
        if not re.search(pattern, heading_blob):
            report("ERROR", 0, f"no heading found for required section: {name}")
            errors += 1

    for i, line in enumerate(lines, 1):
        low = line.lower()
        for phrase in HAND_WAVING:
            if phrase in low:
                report("WARN", i, f"hand-waving phrase {phrase!r} — say what actually happens")
        if PERSONAL_PATH.search(line):
            report("ERROR", i, "hard-coded personal path — nobody else has this directory")
            errors += 1
        if SECRETISH.search(line):
            report("ERROR", i, "possible real secret in documentation — use a placeholder")
            errors += 1

    prereq = re.search(r"(?is)^#+ .*(prerequisit|requirement).*$(.*?)(^#+ |\Z)", text, re.M)
    if prereq and not VERSIONISH.search(prereq.group(2)):
        report("ERROR", 0, "prerequisites section names no versions — pin what you tested on")
        errors += 1

    fences = len(re.findall(r"^```", text, re.M)) // 2
    if fences and not EXPECTED.search(text):
        report("WARN", 0, f"{fences} code blocks, no expected output anywhere — a command "
                          "without a success signal cannot be verified")

    print(f"\n{path}: {errors} error(s). Sections found ({profile} profile): "
          f"{sum(1 for _, p in sections if re.search(p, heading_blob))}/{len(sections)}")
    return 1 if errors else 0


def parse_args(argv):
    """Returns (path, profile) or None if the arguments do not make sense."""
    path, profile = None, None
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg == "--profile":
            if not rest:
                return None
            profile = rest.pop(0)
        elif arg.startswith("--profile="):
            profile = arg.split("=", 1)[1]
        elif arg.startswith("-"):
            return None
        elif path is None:
            path = arg
        else:
            return None
    if path is None or (profile is not None and profile not in PROFILES):
        return None
    return path, profile


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    if args is None:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(*args))