#!/usr/bin/env python3
"""Summarize a capstone hours log. No dependencies; Python 3.8+.

Usage:  python3 hours_report.py docs/hours-log.csv [--budget 240]

Reads the columns written by the Week 1 template:
    date,start,end,hours,phase,hat,task,estimate_hours,blocked_hours,notes

Prints hours by ISO week, by phase, by hat, the running total against the
240-hour budget, and your estimate-to-actual ratio -- the number that tells you
how wrong your Week 7 schedule is going to be.
"""

import csv
import sys
from collections import defaultdict
from datetime import date


def num(row, key):
    try:
        return float((row.get(key) or "0").strip() or 0)
    except ValueError:
        return 0.0


def bucket(rows, key):
    out = defaultdict(float)
    for r in rows:
        out[(r.get(key) or "unlabeled").strip() or "unlabeled"] += num(r, "hours")
    return out


def show(title, table, width=34):
    print("\n" + title)
    print("-" * (width + 10))
    for name, hrs in sorted(table.items(), key=lambda kv: -kv[1]):
        print(f"  {name[:width]:<{width}}{hrs:8.2f} h")


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    path = argv[0]
    budget = 240.0
    if "--budget" in argv:
        budget = float(argv[argv.index("--budget") + 1])

    with open(path, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if (r.get("date") or "").strip()]

    if not rows:
        print(f"{path}: no dated rows yet. Log a session before you report on it.")
        return 1

    weeks = defaultdict(float)
    for r in rows:
        try:
            y, m, d = (int(p) for p in r["date"].split("-"))
            iso = date(y, m, d).isocalendar()
            weeks[f"{iso[0]}-W{iso[1]:02d}"] += num(r, "hours")
        except (ValueError, KeyError):
            weeks["unparsed-date"] += num(r, "hours")

    total = sum(num(r, "hours") for r in rows)
    est = sum(num(r, "estimate_hours") for r in rows)
    blocked = sum(num(r, "blocked_hours") for r in rows)

    print(f"\nHOURS REPORT  --  {path}")
    print(f"{len(rows)} sessions across {len(weeks)} calendar weeks")

    show("BY CALENDAR WEEK", weeks, width=16)
    show("BY PHASE", bucket(rows, "phase"))
    show("BY HAT", bucket(rows, "hat"))

    print("\nBUDGET")
    print("-" * 44)
    pct = (total / budget * 100) if budget else 0
    print(f"  logged                        {total:8.2f} h  ({pct:.1f}% of {budget:.0f})")
    print(f"  remaining                     {budget - total:8.2f} h")
    print(f"  blocked (in the logged total) {blocked:8.2f} h")
    if est > 0:
        print(f"  estimated                     {est:8.2f} h")
        print(f"  estimate-to-actual ratio      {total / est:8.2f}  (1.00 = calibrated)")
    else:
        print("  estimate-to-actual ratio           n/a  (fill estimate_hours BEFORE you start)")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))