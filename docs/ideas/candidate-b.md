For              junior software developers and student project teams
who              use tons of third-party open-source libraries in their code
the problem is   accidentally putting in packages with known, critical security vulnerabilities (CVEs)
which costs      hours of lost time rewriting code after a getting some type of security fail, or a compromised server
Today they       assume packages are safe unless their hosting provider catches them after deployment
which falls short because  it requires deploying vulnerable code to the internet/other stakeholders before knowing the threat exists.

### Must-Have Features & Hour Estimates

1. **Walking Skeleton & CI Pipeline (12 hours)**
   - Minimal web app with file upload handling, basic styling, and automated GitHub Actions testing.
2. **Dependency File Parser (10 hours)**
   - Backend parser to extract package names and exact versions from uploaded `requirements.txt` (Python) and `package.json` (Node.js) files.
3. **OSV.dev API Client (12 hours)**
   - Service to batch-query the Open Source Vulnerabilities (OSV) API, parse JSON vulnerability payloads, and handle network timeouts/errors.
4. **Vulnerability Aggregator & Classifier (14 hours)**
   - Logic to parse CVSS severity scores, map CVE identifiers, and group findings by severity (Critical / High / Medium / Low).
5. **Report Generation & Remediation View (12 hours)**
   - Dashboard displaying identified CVEs with the specific patched/safe version recommended for upgrade.

**Total Construction Hours:** 60 hours