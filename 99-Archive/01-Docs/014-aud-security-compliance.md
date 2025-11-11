# Security & Compliance Audit

**Date:** 2025-10-05
**Directory:** /home/jeremy/projects/bobs-brain
**Auditor:** Claude AI

## Executive Summary

**Overall Security Posture: 6/10** - Moderate Risk

✅ **Strengths:**
- No active .env file in working directory
- .env properly gitignored
- No hardcoded secrets in active code
- Secrets use environment variables

🚨 **Critical Issues:**
- Hardcoded password in deployment script: `deploy_phase5.sh`
- Hardcoded API keys in archived code (18 files)
- .env file was committed to git history
- No SECURITY.md policy
- No security scanning in CI/CD

## Security Issues Identified

### 🔴 CRITICAL (Immediate Action Required)

#### Issue 1: Hardcoded Password in Active Deployment Script

**Location:** `deploy_phase5.sh:line X`
```bash
--set-env-vars="NEO4J_PASSWORD=bobshouse123" \
```

**Risk Level:** CRITICAL
- Production password exposed in code
- Committed to git repository
- Visible in git history
- Anyone with repo access can see password

**Impact:**
- Unauthorized database access
- Data breach potential
- Compliance violation

**Remediation:**
```bash
# Replace hardcoded password with Secret Manager reference
--set-env-vars="NEO4J_PASSWORD=$(gcloud secrets versions access latest --secret=neo4j-password)" \

# OR use environment variable
export NEO4J_PASSWORD=$(gcloud secrets versions access latest --secret=neo4j-password)
--set-env-vars="NEO4J_PASSWORD=${NEO4J_PASSWORD}" \
```

#### Issue 2: .env File in Git History

**Evidence:**
```bash
git log --all --pretty=format: --name-only --diff-filter=A | grep "\.env$"
.env
```

**Risk Level:** HIGH
- .env file was committed at some point
- Potentially contains secrets in git history
- Anyone with repo access can retrieve historical .env

**Remediation:**
```bash
# Check if .env contains secrets in history
git log --all -p -- .env | head -50

# If secrets found, clean history with git-filter-repo
git filter-repo --path .env --invert-paths --force

# Rotate ALL secrets that were in that .env file
```

#### Issue 3: Hardcoded API Keys in Archived Code

**Locations Found (18 files in `archive/deprecated_bobs/`):**

1. **Google API Keys (3 instances):**
   - `bob_gemini_simple.py`: `AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo`
   - `bob_vertex_native.py`: `AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo`
   - `bob_graphiti_gemini.py`: `AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo`

2. **Neo4j Passwords (3 instances):**
   - `bob_vertex_native.py`: `BobBrain2025`
   - `bob_graphiti_gemini.py`: `BobBrain2025`
   - `bob_memory.py`: `BobBrain2025`

3. **Placeholder OpenAI Keys (2 instances):**
   - `bob_vertex_native.py`: `sk-placeholder`
   - `bob_graphiti_gemini.py`: `sk-placeholder`

**Risk Level:** HIGH
- Real API keys exposed in code
- Real database passwords in code
- Committed to git history
- Can't be removed without history rewrite

**Remediation:**
1. **IMMEDIATELY:** Rotate all exposed credentials:
   - Revoke Google API key `AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo`
   - Change Neo4j password `BobBrain2025`

2. **Remove hardcoded secrets from archive:**
   - Replace with `<REDACTED>` or remove lines
   - Commit changes
   - Consider removing archive entirely if no historical value

3. **Clean git history (if private repo):**
   ```bash
   git filter-repo --replace-text <(echo 'AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo==>REDACTED')
   git filter-repo --replace-text <(echo 'BobBrain2025==>REDACTED')
   ```

### 🟡 HIGH Priority

#### Issue 4: No Security Policy

**Missing:** `SECURITY.md`

**Impact:**
- No clear vulnerability reporting process
- No security contact information
- No supported versions documented
- Unprofessional for open-source

**Remediation:** Create SECURITY.md with:
- Security contact email
- Vulnerability reporting process
- Supported versions
- Security best practices
- Disclosure timeline

#### Issue 5: No Security Scanning in CI/CD

**Current CI/CD:** (from README)
- Lint checks ✅
- Type checking ✅
- Tests ✅
- Coverage ✅
- **Security scanning** ❌

**Recommended Tools:**
- `bandit` - Python security linter
- `safety` - Dependency vulnerability scanner
- `gitleaks` - Secret scanning
- `trivy` - Container scanning

**Add to CI:**
```yaml
- name: Security Scan
  run: |
    pip install bandit safety
    bandit -r src/
    safety check
```

#### Issue 6: .secrets.baseline in Git History

**Evidence:** `.secrets.baseline` file was committed

**Analysis:** This is from `detect-secrets` tool (good!)
- Shows security awareness
- Establishes secret baseline
- BUT: Should verify it doesn't contain actual secrets

**Action:** Review `.secrets.baseline` for false positives

### 🟢 MEDIUM Priority

#### Issue 7: Missing Security Headers

**Current:** Flask app with CORS enabled

**Missing Security Features:**
- Content Security Policy (CSP)
- X-Frame-Options
- X-Content-Type-Options
- Strict-Transport-Security (HTTPS only)

**Recommendation:**
```python
from flask_talisman import Talisman

# Add to src/app.py
Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self'",
    }
)
```

#### Issue 8: API Key Authentication Could Be Stronger

**Current:** Single API key in environment variable
```python
API_KEY = os.getenv("BB_API_KEY")
if key != API_KEY:
    return jsonify({"error": "unauthorized"}), 401
```

**Issues:**
- Single shared key (no per-user keys)
- No key rotation mechanism
- No rate limiting per key
- Keys in environment variables (better than hardcoded, but not ideal)

**Recommendations:**
- Use JWT tokens with expiration
- Implement key rotation
- Store keys in Secret Manager
- Add per-key rate limiting

## Gitignore Analysis

### Current .gitignore

**Covered:**
- `.env` ✅
- `verify_*.py.env` ✅
- Python cache files (via general Python patterns)

**Missing Patterns:**
```
# Secrets and credentials
*.pem
*.key
*.crt
**/secrets/
**/credentials/
service-account*.json
gcp-key*.json

# Environment files
.env.local
.env.*.local
.env.production

# IDE secrets
.vscode/settings.json
.idea/workspace.xml

# Cloud credentials
.gcloud/
.config/gcloud/
```

## Compliance Assessment

### License Compliance

**License:** MIT License ✅
- Permissive license
- Properly included
- No compliance issues

### Data Privacy

**Assessment:**
- Circle of Life collects interaction data
- No PII handling visible in code ✅
- No GDPR-specific requirements identified
- Slack integration may collect user data ⚠️

**Recommendations:**
- Document data retention policy
- Add privacy notice if collecting user data
- Implement data deletion mechanism
- GDPR compliance if EU users

### Dependency Licenses

**Not Assessed:** Need to check all dependencies

**Action Required:**
```bash
pip install pip-licenses
pip-licenses --format=markdown > claudes-docs/reports/licenses.md
```

## Risk Assessment Matrix

| Risk | Severity | Likelihood | Impact | Priority |
|------|----------|------------|--------|----------|
| Hardcoded password in deploy script | CRITICAL | HIGH | HIGH | P0 |
| API keys in git history | HIGH | MEDIUM | HIGH | P0 |
| .env in git history | HIGH | MEDIUM | HIGH | P0 |
| No security scanning | MEDIUM | HIGH | MEDIUM | P1 |
| No SECURITY.md | LOW | HIGH | LOW | P2 |
| Weak auth mechanism | MEDIUM | LOW | MEDIUM | P2 |
| Missing security headers | LOW | MEDIUM | LOW | P3 |

## Remediation Roadmap

### Phase 1: CRITICAL - Immediate Action (Today)

**Time: 1 hour**

1. **Rotate Exposed Credentials (30 min)**
   ```bash
   # Revoke Google API key
   gcloud services api-keys delete AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo

   # Change Neo4j password
   # (in Neo4j console or via cypher query)

   # Generate new secrets
   gcloud secrets create neo4j-password --data-file=- <<< "$(openssl rand -base64 32)"
   ```

2. **Fix Deployment Script (15 min)**
   ```bash
   # Update deploy_phase5.sh to use Secret Manager
   sed -i 's/NEO4J_PASSWORD=bobshouse123/NEO4J_PASSWORD=$(gcloud secrets versions access latest --secret=neo4j-password)/' deploy_phase5.sh

   git add deploy_phase5.sh
   git commit -m "security: remove hardcoded password from deployment script"
   git push
   ```

3. **Redact Archived Secrets (15 min)**
   ```bash
   # Replace API keys in archive with REDACTED
   find archive/ -type f -name "*.py" -exec sed -i 's/AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo/<REDACTED>/g' {} +
   find archive/ -type f -name "*.py" -exec sed -i 's/BobBrain2025/<REDACTED>/g' {} +

   git add archive/
   git commit -m "security: redact hardcoded secrets from archived code"
   git push
   ```

### Phase 2: HIGH - Within 24 Hours

**Time: 2 hours**

1. **Create SECURITY.md (30 min)**
   - Security contact
   - Reporting process
   - Supported versions
   - Best practices

2. **Add Security Scanning to CI (30 min)**
   ```yaml
   # Add to .github/workflows/ci.yml
   - name: Security Scan
     run: |
       pip install bandit safety gitleaks
       bandit -r src/ -f json -o security-report.json
       safety check --json
       gitleaks detect --source . --verbose
   ```

3. **Clean Git History (1 hour)** - OPTIONAL, only if private repo
   ```bash
   git filter-repo --replace-text secrets-to-redact.txt --force
   ```

### Phase 3: MEDIUM - Within 1 Week

**Time: 4 hours**

1. **Implement Stronger Auth (2 hours)**
   - JWT tokens
   - Key rotation
   - Secret Manager integration

2. **Add Security Headers (1 hour)**
   - Flask-Talisman
   - CSP, HSTS, etc.

3. **Dependency Audit (1 hour)**
   - License compliance
   - Vulnerability scanning
   - Update policy

## TaskWarrior Commands

```bash
task add project:dir-audit +SECURITY priority:H due:today "Rotate exposed Google API key and Neo4j password"
task add project:dir-audit +SECURITY priority:H due:today "Remove hardcoded password from deploy_phase5.sh"
task add project:dir-audit +SECURITY priority:H due:today "Redact secrets from archived code files"
task add project:dir-audit +SECURITY priority:H due:tomorrow "Create SECURITY.md with vulnerability reporting process"
task add project:dir-audit +SECURITY priority:H due:tomorrow "Add security scanning to CI/CD pipeline (bandit, safety)"
task add project:dir-audit +SECURITY priority:M due:1week "Implement JWT-based authentication"
task add project:dir-audit +SECURITY priority:M due:1week "Add Flask security headers (Talisman)"
task add project:dir-audit +SECURITY priority:M due:1week "Audit dependency licenses and vulnerabilities"
task add project:dir-audit +SECURITY priority:L "Consider cleaning git history with filter-repo (private repo only)"
```

## Compliance Score

| Area | Score | Status |
|------|-------|--------|
| Secret Management | 3/10 | ❌ Hardcoded secrets |
| Access Control | 5/10 | ⚠️ Basic auth, needs improvement |
| Security Policy | 0/10 | ❌ No SECURITY.md |
| Vulnerability Management | 2/10 | ❌ No scanning |
| Data Privacy | 7/10 | ✅ No PII issues detected |
| License Compliance | 8/10 | ✅ MIT, needs dep audit |

**Overall: 4.2/10** - Significant improvements needed

## Next Steps

1. ⏳ **TODAY:** Rotate all exposed credentials (P0)
2. ⏳ **TODAY:** Fix hardcoded password in deploy script (P0)
3. ⏳ **TODAY:** Redact secrets from archive (P0)
4. ⏳ **TOMORROW:** Create SECURITY.md (P1)
5. ⏳ **TOMORROW:** Add security scanning to CI (P1)
6. ⏳ **THIS WEEK:** Improve auth and add security headers (P2)
7. ⏳ **THIS WEEK:** Dependency security audit (P2)

## Critical Recommendations

1. **IMMEDIATE:** This is not a drill - rotate credentials NOW
   - Google API key `AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo` must be revoked
   - Neo4j password `BobBrain2025` must be changed
   - These are in public git history

2. **HIGH PRIORITY:** Never commit secrets again
   - Use pre-commit hooks (gitleaks, detect-secrets)
   - Use Secret Manager for all credentials
   - Review code before committing

3. **ESTABLISH:** Security baseline
   - Create SECURITY.md
   - Add security scanning to CI
   - Regular security audits
   - Incident response plan

## Conclusion

**The project has serious security issues that require immediate attention.**

The good news: No active .env file, environment variables used correctly in modern code.

The bad news: Hardcoded secrets in deployment scripts and git history, no security policy, no security scanning.

**Action required within 24 hours to prevent potential security incidents.**
