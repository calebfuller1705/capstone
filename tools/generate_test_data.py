#!/usr/bin/env python3
"""Deterministic Test Data Generator for URL Security Scanner."""

import argparse
import json
import os
import random
import sys

SEED = 20261031
random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "tests", "fixtures")


def build_happy_records():
    domains = [
        "example.com", "github.com", "python.org", "wikipedia.org", "fastapi.tiangolo.com",
        "mozilla.org", "cloudflare.com", "mit.edu", "w3.org", "iana.org"
    ]
    paths = [
        "", "/about", "/docs/api/v1", "/search?q=security", "/blog/2026/10/release",
        "/verify?token=abc123xyz", "/resources/whitepaper.pdf", "/status"
    ]
    schemes = ["https://", "http://"]

    records = []
    idx = 1
    for domain in domains:
        for path in paths[:3]:
            records.append({
                "id": f"HAPPY-{idx:03d}",
                "family": "happy",
                "url": f"{random.choice(schemes)}{domain}{path}",
                "description": "Standard realistic web URL"
            })
            idx += 1
    return records


def build_boundary_records():
    base = "https://example.com/"
    exact_2048 = base + "a" * (2048 - len(base))
    overflow_2049 = base + "b" * (2049 - len(base))

    return [
        {"id": "BOUND-001", "family": "boundary", "url": "", "expected_valid": False, "description": "Empty string (0 chars)"},
        {"id": "BOUND-002", "family": "boundary", "url": "h", "expected_valid": False, "description": "Single character below scheme threshold"},
        {"id": "BOUND-003", "family": "boundary", "url": "http://a.co", "expected_valid": True, "description": "Shortest valid HTTP URL (11 chars)"},
        {"id": "BOUND-004", "family": "boundary", "url": exact_2048, "expected_valid": True, "description": "Exact boundary limit (2048 chars)"},
        {"id": "BOUND-005", "family": "boundary", "url": overflow_2049, "expected_valid": False, "description": "One-character boundary overflow (2049 chars)"},
        {"id": "BOUND-006", "family": "boundary", "url": None, "expected_valid": False, "description": "Explicit null / None value"},
        {"id": "BOUND-007", "family": "boundary", "url": "   https://example.com   ", "expected_valid": True, "description": "Whitespace-padded URL (FR-INP-04)"},
        {"id": "BOUND-008", "family": "boundary", "url": "https://" + "sub." * 50 + "example.com", "expected_valid": True, "description": "Deep subdomain chain"}
    ]


def build_hostile_records():
    return [
        {"id": "HOSTILE-001", "family": "hostile", "url": "https://example.com/' OR 1=1;--", "description": "SQL injection in query/path"},
        {"id": "HOSTILE-002", "family": "hostile", "url": "https://example.com/<script>alert(1)</script>", "description": "Reflected XSS injection script tag"},
        {"id": "HOSTILE-003", "family": "hostile", "url": "https://example.com/../../../../etc/passwd", "description": "Directory traversal payload"},
        {"id": "HOSTILE-004", "family": "hostile", "url": "https://example.com/O'Brien/profile", "description": "Unescaped single apostrophe in pathname"},
        {"id": "HOSTILE-005", "family": "hostile", "url": "https://example.com/\U0001f680/security-check", "description": "Unicode and emoji in URL path"},
        {"id": "HOSTILE-006", "family": "hostile", "url": "https://example.com/%00evil-payload", "description": "URL-encoded null byte"},
        {"id": "HOSTILE-007", "family": "hostile", "url": "javascript:alert('xss')", "description": "Client script protocol injection"},
        {"id": "HOSTILE-008", "family": "hostile", "url": "file:///etc/passwd", "description": "Local filesystem URI scheme"},
        {"id": "HOSTILE-009", "family": "hostile", "url": "https://127.0.0.1:8000/internal", "description": "Localhost loopback SSRF attempt"},
        {"id": "HOSTILE-010", "family": "hostile", "url": "https://192.168.1.1/admin", "description": "RFC 1918 private subnet intranet attempt (FR-EVAL-01)"},
        {"id": "HOSTILE-011", "family": "hostile", "url": "https://example.com/" + ("A" * 10000), "description": "Buffer stress 10,000-character payload"},
        {"id": "HOSTILE-012", "family": "hostile", "url": "https://[:::1]:8080/scan", "description": "Malformed IPv6 bracket format"}
    ]


def main():
    parser = argparse.ArgumentParser(description="Deterministic Test Data Generator")
    parser.add_argument("--set", choices=["all", "happy", "boundary", "hostile"], default="all")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    data = {
        "happy": build_happy_records(),
        "boundary": build_boundary_records(),
        "hostile": build_hostile_records()
    }

    target_sets = ["happy", "boundary", "hostile"] if args.set == "all" else [args.set]

    sys.stdout.write("Generating test data fixtures...\n")
    sys.stdout.flush()

    for s in target_sets:
        out_file = os.path.join(OUTPUT_DIR, f"test_data_{s}.json")
        payload = {
            "seed": SEED,
            "family": s,
            "record_count": len(data[s]),
            "records": data[s]
        }
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        sys.stdout.write(f"seed --set {s:<8} -> {len(data[s])} records ({out_file})\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()