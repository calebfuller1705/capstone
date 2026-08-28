For              small business admins and non-profit IT coordinators
who              manage staff accounts and shared credentials
the problem is   staff reusing personal passwords that have been compromised in major data breaches
which costs      costly account takeovers, ransomware infections, or thousands of dollars in lost business data
Today they       ask staff to "pick strong passwords" or enforce 90-day password resets
which falls short because  it does not actually verify if the password is currently sitting on a hacker forum.

### Must-Have Features & Hour Estimates

1. **Walking Skeleton & CI Pipeline (12 hours)**
   - Basic Flask app with secure form submission and automated CI checks.
2. **Client-Side SHA-1 Hasher & K-Anonymity Splitter (8 hours)**
   - Logic to compute SHA-1 hash of the submitted password, extract the first 5 hex characters (prefix), and hold the remaining 35 characters (suffix) locally.
3. **Have I Been Pwned (HIBP) API Client (10 hours)**
   - Backend integration to query `https://api.pwnedpasswords.com/range/{hash_prefix}`, process the pipe-delimited text response, and handle rate-limiting.
4. **Local Hash Matching Engine (10 hours)**
   - Engine that matches the local suffix against the returned breached hash list to find breach count without ever sending the full password.
5. **Auditor Summary Dashboard (14 hours)**
   - Visual output showing breach frequency, password entropy score, and plain-language password strength recommendations.

**Total Construction Hours:** 54 hours