# Security Policy

## Reporting a Vulnerability

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email:
```
security@intentsolutions.io
```

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: 1-3 days
  - High: 1 week
  - Medium: 2 weeks
  - Low: Next release

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

Only the latest 1.x version receives security updates.

## Security Best Practices

### For Contributors

#### Never Commit Secrets
```bash
# Blocked by .gitignore:
.env
.env.local
.env.*.local
*.pem
*.key
*.cert
```

#### Pre-Commit Checks
```bash
# Before committing, verify no secrets:
git diff --cached | grep -E "API_KEY|SECRET|PASSWORD|TOKEN"

# If found, remove from staged files
```

#### Dependency Security
```bash
# Check for vulnerabilities
bun audit

# Update dependencies regularly
bun update
```

### For Deployment

#### Environment Variables
Use Netlify Environment Variables (never commit .env files):

1. Netlify → Site settings → Environment variables
2. Add key-value pairs
3. Reference in code: `import.meta.env.VITE_API_KEY`

#### Secrets Management
- Use Netlify secrets for API keys
- Rotate credentials quarterly
- Use different keys for dev/staging/production

### For Users

#### Browsing Security
- Always use HTTPS: https://intentsolutions.io
- Verify SSL certificate (padlock icon)
- Report suspicious behavior immediately

#### Data Privacy
- This is a static landing page
- No personal data collected or stored
- No cookies used (except Netlify analytics if enabled)

## Security Headers

The following security headers are configured in `netlify.toml`:

### X-Frame-Options: DENY
Prevents clickjacking attacks by disallowing site in iframes.

### X-Content-Type-Options: nosniff
Prevents MIME sniffing attacks.

### Referrer-Policy: strict-origin-when-cross-origin
Controls referrer information sent with requests.

### Permissions-Policy
Restricts browser features:
```
geolocation=()
microphone=()
camera=()
```

### Content-Security-Policy (CSP)
Prevents XSS attacks:
```
default-src 'self'
script-src 'self' 'unsafe-inline'
style-src 'self' 'unsafe-inline'
img-src 'self' data: https:
font-src 'self' data:
```

**Note**: `unsafe-inline` required for Vite dev mode. Consider stricter policy in production.

### Strict-Transport-Security (HSTS)
Enforces HTTPS for 1 year:
```
max-age=31536000; includeSubDomains; preload
```

## Known Security Considerations

### Client-Side Only
- All code runs in browser (static site)
- No backend = no database injection attacks
- No authentication = no credential theft
- No API = no API abuse

### Dependencies
- 57 shadcn/ui components with dependencies
- Regular updates recommended
- Monitor for CVEs via GitHub Dependabot (when enabled)

### Build-Time Security
- TypeScript strict mode enabled (type safety)
- No eval() or dangerous functions
- Content escaped by React by default

## Compliance

### Open Source License
- MIT License (see `03-LICENSE.md`)
- No attribution required beyond license file

### Data Privacy
- **GDPR**: No personal data collected (N/A)
- **CCPA**: No personal data sold (N/A)
- **ePrivacy**: No cookies used (compliant)

### Accessibility
- WCAG 2.1 Level AA target (in progress)
- Keyboard navigation supported
- Screen reader compatible

## Incident Response

### If You Discover a Vulnerability

1. **Email** security@intentsolutions.io immediately
2. **Do not** disclose publicly until fix is released
3. **Cooperate** with our security team
4. **Receive** acknowledgment in CHANGELOG (if desired)

### Our Process

1. **Triage**: Assess severity within 48 hours
2. **Fix**: Develop patch based on severity
3. **Test**: Verify fix resolves issue
4. **Deploy**: Push to production
5. **Disclose**: Publish advisory with credit

## Security Roadmap

### Planned Improvements

#### Phase 1 (Next 2 Weeks)
- [ ] Enable GitHub Dependabot alerts
- [ ] Add pre-commit hook for secret detection
- [ ] Implement CSP reporting

#### Phase 2 (Next Month)
- [ ] Add automated security scanning (GitHub Actions)
- [ ] Implement SBOM generation
- [ ] Add security.txt file

#### Phase 3 (Next Quarter)
- [ ] Penetration testing (when adding backend)
- [ ] Bug bounty program (when adding sensitive features)
- [ ] SOC 2 compliance (if needed for enterprise clients)

## Contact

**Security Email**: security@intentsolutions.io
**Response Time**: 48 hours
**PGP Key**: Contact for key if needed for encrypted communication

---
**Last Updated**: October 4, 2025
**Security Version**: 1.0.0
**Next Review**: January 4, 2026
