#!/usr/bin/env python3
"""check_config.py — verify your project's configuration contract."""

import os
import re
import sys

PLACEHOLDERS = {"", "changeme", "change-me", "todo", "tbd", "xxx",
                "your-key-here", "<fill me in>", "replace-me", "none"}
SECRETISH = re.compile(r"(SECRET|TOKEN|KEY|PASSWORD|PASSWD|CREDENTIAL|DSN)", re.I)

ENV_LOOKUPS = [
    re.compile(r"""os\.environ\.get\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""os\.environ\[\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""os\.getenv\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""process\.env\.([A-Z][A-Z0-9_]+)"""),
    re.compile(r"""process\.env\[\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""System\.getenv\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""Environment\.GetEnvironmentVariable\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""\bENV\s*(?:\[|\.fetch\()\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""os\.(?:Getenv|LookupEnv)\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""\bgetenv\(\s*["']([A-Z][A-Z0-9_]+)["']"""),
    re.compile(r"""\$_ENV\[\s*["']([A-Z][A-Z0-9_]+)["']"""),
]

SOURCE_EXTS = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java",
               ".kt", ".rb", ".go", ".cs", ".php", ".rs", ".swift", ".c",
               ".cc", ".cpp", ".h", ".hpp", ".sh", ".bash"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "venv", ".venv", "__pycache__",
             "dist", "build", "target", "vendor", "coverage", ".next", ".gradle",
             ".idea", ".mypy_cache", ".pytest_cache", "bin", "obj"}
MAX_BYTES = 512 * 1024


def parse(path):
    """Return {NAME: (default, required, doc)} from a dotenv-style file."""
    entries, comment = {}, []
    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            if line.strip().startswith("#"):
                comment.append(line.strip().lstrip("#").strip())
            elif not line.strip():
                comment = []
            else:
                name, _, default = line.partition("=")
                doc = " ".join(comment).strip()
                entries[name.strip()] = (default.strip(), "OPTIONAL" not in doc.upper(), doc)
                comment = []
    return entries


def scan_sources(root):
    """Return ({NAME: first file that reads it}, number of files scanned)."""
    used, scanned = {}, 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in SOURCE_EXTS:
                continue
            full = os.path.join(dirpath, filename)
            try:
                if os.path.getsize(full) > MAX_BYTES:
                    continue
                with open(full, "r", encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError:
                continue
            scanned += 1
            where = os.path.relpath(full, root)
            for pattern in ENV_LOOKUPS:
                for name in pattern.findall(text):
                    used.setdefault(name, where)
    return used, scanned


def main(argv):
    args = argv[1:]
    scan_root, do_scan = ".", True
    positional = []
    i = 0
    while i < len(args):
        if args[i] == "--no-scan":
            do_scan = False
        elif args[i] == "--scan":
            i += 1
            if i >= len(args):
                print("FATAL: --scan needs a directory")
                return 2
            scan_root = args[i]
        else:
            positional.append(args[i])
        i += 1

    contract_path = positional[0] if positional else ".env.example"

    try:
        contract = parse(contract_path)
    except OSError as err:
        print("FATAL: cannot read the contract: %s" % err)
        return 2

    try:
        values = parse(positional[1]) if len(positional) > 1 else None
    except OSError as err:
        print("FATAL: cannot read the values file: %s" % err)
        return 2

    def lookup(name):
        if values is not None:
            return values[name][0] if name in values else None
        return os.environ.get(name)

    problems, drift, notes = [], [], []
    flagged = set()
    for name, (_default, required, doc) in sorted(contract.items()):
        actual = lookup(name)
        if actual is None or actual.strip().lower() in PLACEHOLDERS:
            (problems if required else notes).append(
                "%-28s %s%s" % (name, "MISSING" if required else "unset (optional)",
                                " — " + doc[:60] if doc else ""))
            flagged.add(name)
        elif not doc:
            notes.append("%-28s set, but UNCOMMENTED — no comment above it in the contract" % name)
            flagged.add(name)
        elif SECRETISH.search(name) and len(actual) < 12:
            notes.append("%-28s set, but suspiciously short for a secret" % name)
            flagged.add(name)

    used, scanned = ({}, 0)
    if do_scan:
        used, scanned = scan_sources(scan_root)
        for name in sorted(used):
            if name not in contract:
                drift.append("%-28s UNDOCUMENTED — read by %s, absent from the contract"
                             % (name, used[name]))
        if scanned:
            for name in sorted(contract):
                if name not in used and name not in flagged:
                    notes.append("%-28s in the contract but not found in the scanned source "
                                 "(a framework may read it indirectly — confirm before "
                                 "deleting)" % name)

    print("contract: %s   variables: %d" % (contract_path, len(contract)))
    if do_scan:
        print("scanned:  %d source file(s) under %s   lookups found: %d"
              % (scanned, scan_root, len(used)))
    for line in problems:
        print("  FAIL  " + line)
    for line in drift:
        print("  warn  " + line)
    for line in notes:
        print("  warn  " + line)
    print("%d required missing, %d warnings, %d undocumented."
          % (len(problems), len(drift) + len(notes), len(drift)))
    if not do_scan:
        print("note: source scan skipped — the UNDOCUMENTED check did not run.")
    elif scanned == 0:
        print("note: no source files scanned under %s, so the UNDOCUMENTED count above is "
              "0 because nothing was read, not because your contract is complete. "
              "Run this from your project root or pass --scan <dir>." % scan_root)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
