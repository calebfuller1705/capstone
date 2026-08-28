The problem of checking whether a suspicious email or link is a phishing attempt
affects non-technical everyday employees and consumers
the impact of which is a constant level of uncertainty that causes ignored legitimate emails, dangerous clicks, and compromised personal data
which costs roughly 1.5 - 2 hours of mandatory HR retraining per clicked link, or the total loss of a compromised online account
a successful solution would analyze a pasted URL or email header to give a clear, plain-English risk score
and would be evaluated by a user successfully deciding to trash or keep a test email in under 30 seconds without asking IT for help or clarity.

### Must-Have Features & Hour Estimates

1. **Walking Skeleton & CI/CD Pipeline (12 hours)**
   - Local Flask/Python server setup, basic HTML template rendering, and automated deployment to a free tier host with GitHub Actions.
2. **User Input & Validation UI (8 hours)**
   - A clean web form where the user can paste a suspicious URL or block of email text, with basic regex validation to extract the link.
3. **VirusTotal API Integration (14 hours)**
   - Backend logic to securely give the extracted URL to the VirusTotal Public API, handle the JSON response, and manage the 4-request-per-minute rate limit.
4. **URLScan.io API Integration (12 hours)**
   - Secondary API call to URLScan to get domain age, server location, and screenshot data of the malicious site without the user having to click on it.
5. **Risk Scoring Engine (15 hours)**
   - A custom algorithm that weighs the responses from both APIs to generate a simple "Safe", "Suspicious", or "Malicious" score. 
6. **Plain-English Results Dashboard (10 hours)**
   - UI that displays the traffic-light score (Red/Yellow/Green) and 2-3 bullet points explaining why it is dangerous without using IT lingo.

**Total Estimated Construction Hours:** 71 hours 