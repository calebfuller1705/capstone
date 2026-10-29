#!/usr/bin/env python3
"""Verified-requirement coverage from a test traceability matrix."""

import csv
import os
import sys
from collections import defaultdict

PASS = "pass"

REQUIRED_COLUMNS = (
    "req_id",
    "req_priority",
    "acceptance_criterion_id",
    "test_case_id",
    "status",
)


class MatrixSchemaError(Exception):
    """Raised when the CSV is not a Week 11 test traceability matrix."""

    def __init__(self, missing, found):
        self.missing = list(missing)
        self.found = list(found)
        super().__init__(f"missing column(s): {', '.join(self.missing)}")


def cell(row, name):
    """Column value as a stripped string; tolerates short or ragged rows."""
    return (row.get(name) or "").strip()


def load(path):
    # utf-8-sig strips any Windows PowerShell BOM (\ufeff) automatically
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        header = list(reader.fieldnames or [])
        missing = [name for name in REQUIRED_COLUMNS if name not in header]
        if missing:
            raise MatrixSchemaError(missing, header)
        return [row for row in reader if cell(row, "req_id")]


def summarize(rows):
    criteria = defaultdict(list)
    for row in rows:
        key = (
            cell(row, "req_id"),
            cell(row, "req_priority"),
            cell(row, "acceptance_criterion_id"),
        )
        criteria[key].append(
            (cell(row, "test_case_id"), cell(row, "status").lower())
        )

    untested, failing, not_run, verified_ac = [], [], [], set()
    for key, results in criteria.items():
        if not any(tc for tc, _ in results):
            untested.append(key)
        elif any(status == PASS for _, status in results):
            verified_ac.add(key)
        elif any(status == "fail" for _, status in results):
            failing.append(key)
        else:
            not_run.append(key)

    requirements = defaultdict(list)
    for key in criteria:
        requirements[(key[0], key[1])].append(key)
    verified_req = {
        r for r, acs in requirements.items() if all(a in verified_ac for a in acs)
    }
    return requirements, verified_req, untested, failing, not_run


def pct(part, whole):
    return 0.0 if not whole else 100.0 * part / whole


def show(title, keys):
    if not keys:
        return
    print(f"\n{title}")
    for req_id, priority, ac_id in sorted(keys):
        print(f"  {req_id:<12} {priority:<7} {ac_id}")


def main(argv):
    default = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "traceability-matrix.csv"
    )
    path = argv[1] if len(argv) > 1 else default
    try:
        rows = load(path)
    except FileNotFoundError:
        print(f"No such file: {path}", file=sys.stderr)
        return 2
    except MatrixSchemaError as error:
        print(
            f"{path}: missing column(s): {', '.join(error.missing)}",
            file=sys.stderr,
        )
        print(
            f"  found:    {', '.join(error.found) or '(no header row)'}",
            file=sys.stderr,
        )
        print(f"  expected: {', '.join(REQUIRED_COLUMNS)}", file=sys.stderr)
        return 2

    requirements, verified, untested, failing, not_run = summarize(rows)

    musts = {r for r in requirements if r[1].lower() == "must"}
    verified_musts = musts & verified
    print(f"Traceability matrix: {path}")
    print(f"Requirements:        {len(requirements)}")
    print(
        f"Verified:            {len(verified)} "
        f" ({pct(len(verified), len(requirements)):.0f}%)"
    )
    print(f"Must requirements:   {len(musts)}")
    print(
        f"Verified Musts:      {len(verified_musts)} "
        f" ({pct(len(verified_musts), len(musts)):.0f}%)"
    )

    show("NO TEST CASE AT ALL (write these first):", untested)
    show("TESTED AND FAILING (open a defect if you have not):", failing)
    show("TEST EXISTS BUT NEVER RUN (this is not coverage):", not_run)

    unverified_musts = sorted(musts - verified)
    if unverified_musts:
        print("\nUNVERIFIED MUST REQUIREMENTS -- exit criteria not met:")
        for req_id, priority in unverified_musts:
            print(f"  {req_id}")
        return 1
    print("\nAll Must requirements verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))