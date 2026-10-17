# Operational Runbook

## Credential Rotation Plan: VirusTotal API Key

1. **Source:** VirusTotal Developer Portal (`https://www.virustotal.com/gui/user/<username>/apikey`).
2. **Rotation Procedure:** Log into the VirusTotal console, navigate to API Key settings, click **Revoke Key**, generate a new API key, and update the repository secret (`VIRUSTOTAL_API_KEY`) under GitHub **Settings > Secrets and variables > Actions**.
3. **Escalation & Notification:** Log the security incident in the project defect/risk log and notify the capstone instructor/lead evaluator via email immediately.
4. **Estimated Rotation Duration:** Under 5 minutes from detection to active redeployment.
