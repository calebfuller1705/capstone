import json
import random

SEED = 20261104
random.seed(SEED)

DOMAINS = [
    "sharepoint.com", "slack.com", "atlassian.net", "github.com", "salesforce.com",
    "service-now.com", "zoom.us", "box.com", "okta.com", "aws.amazon.com",
    "login.microsoftonline.com", "dropbox.com", "hubspot.com", "zendesk.com", "stripe.com"
]

PATHS = [
    "auth/v2/verify", "workspace/document/edit", "api/v1/tokens", "dashboard/analytics",
    "reports/quarterly/export", "assets/cdn/vendor/bundle", "oauth/callback",
    "secure/download/attachment", "settings/profile/security", "webhook/receiver/event"
]

records = []
for i in range(1, 501):
    domain = random.choice(DOMAINS)
    path = random.choice(PATHS)
    proto = "https" if i % 15 != 0 else "http"
    query = f"?client_id=corp_{i:04d}&session={random.randint(100000, 999999)}&ref=email"
    url = f"{proto}://{domain}/{path}{query}"
    records.append({"id": f"PERF-{i:03d}", "url": url, "expected_verdict": "Safe"})

with open("tests/fixtures/perf_seed_500.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

print(f"Generated 500 realistic records in tests/fixtures/perf_seed_500.json (seed {SEED})")