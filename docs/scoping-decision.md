# scoping-decision
Dependency,Candidate,Exercised,Result,Key?,Rate limit,Terms read
VirusTotal Public API,A,curl -X GET [https://www.virustotal.com/api/v3/urls/](https://www.virustotal.com/api/v3/urls/){id},200 OK,Yes,500 requests per day,2026-08-29
urlscan.io API,A,curl -X POST [https://urlscan.io/api/v1/scan/](https://urlscan.io/api/v1/scan/),200 OK,Yes,Returns X-Rate-Limit HTTP headers on each request,2026-08-29
OSV.dev API,B,curl -X POST [https://api.osv.dev/v1/query](https://api.osv.dev/v1/query),200 OK,No,No limits currently applied,2026-08-29
Have I Been Pwned Passwords API,C,curl [https://api.pwnedpasswords.com/range/21BD1](https://api.pwnedpasswords.com/range/21BD1),200 OK,No,No rate limit on the Pwned Passwords API,2026-08-29
