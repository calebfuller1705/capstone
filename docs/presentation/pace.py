#!/usr/bin/env python3
"""Rehearsal pace report for a 30-minute capstone talk."""

import csv
import io
import sys

LIMIT_MIN = 30.0
OVER_RATIO = 1.25

SAMPLE = """pass,section,planned_min,actual_min,note
1,Hook,1.5,2.6,explained the project name for 40 seconds
1,Problem,3.0,4.1,told the whole roommate story
1,Scope,2.5,2.2,fine
1,Architecture,3.0,3.4,pointed at the wrong box once
1,Decisions,3.0,4.0,defended two ADRs; only one was needed
1,Demo,7.0,11.2,searched for the barcode live instead of pre-seeding
1,Evidence,3.5,2.9,rushed it
1,Not done,1.5,0.4,mumbled it
1,Lessons,1.5,1.6,fine
1,Questions,3.5,3.5,not rehearsed
"""


def load(rows):
    passes = {}
    for row in csv.DictReader(rows):
        key = (row.get("pass") or "?").strip()
        passes.setdefault(key, []).append(
            (
                (row.get("section") or "").strip(),
                float(row.get("planned_min") or 0),
                float(row.get("actual_min") or 0),
                (row.get("note") or "").strip(),
            )
        )
    return passes


def report(passes):
    for key in sorted(passes):
        sections = passes[key]
        planned = sum(s[1] for s in sections)
        actual = sum(s[2] for s in sections)
        print("\\nPass %s  —  planned %.1f min, actual %.1f min" % (key, planned, actual))
        print("  %-14s %8s %8s %8s  %s" % ("section", "plan", "actual", "drift", "note"))
        for name, plan, act, note in sections:
            drift = act - plan
            flag = "  <== OVER" if plan and act > plan * OVER_RATIO else ""
            print("  %-14s %8.1f %8.1f %+8.1f  %s%s" % (name, plan, act, drift, note, flag))
        if actual > LIMIT_MIN:
            print("  RESULT: %.1f min — OVER the %.0f-minute limit by %.1f. Cut, do not talk faster."
                  % (actual, LIMIT_MIN, actual - LIMIT_MIN))
        else:
            print("  RESULT: %.1f min — inside the limit with %.1f to spare."
                  % (actual, LIMIT_MIN - actual))


def main(argv):
    if len(argv) > 1:
        with open(argv[1], newline="", encoding="utf-8") as fh:
            passes = load(fh)
    else:
        print("(no file given — using the built-in sample log)")
        passes = load(io.StringIO(SAMPLE))
    if not passes:
        print("No rows found. Expected: pass,section,planned_min,actual_min,note")
        return 1
    report(passes)
    print("\\nRehearse until two consecutive passes land inside the limit without cutting anything new.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))