# Security Policy

## Supported Versions

This project follows semantic versioning. The following versions are currently supported with security updates:

| Version | Status | Support Until |
|---------|--------|---|
| 0.12.x | Current | Active |
| 0.11.x | Deprecated | 2025-12-31 |
| < 0.11 | Unsupported | End of life |

**Current Version:** 0.12.0

### End of Life Schedule

- **0.11.x**: Security updates only until 2025-12-31, then end of life
- **0.10.x and earlier**: No security updates

We recommend upgrading to the latest version (0.12.x) to receive all security patches and updates.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

### Reporting Process

If you discover a security vulnerability in Bob's Brain, please report it by emailing:

**Email:** jeremy@intentsolutions.io

**Include in your report:**
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Affected version(s)
- Potential impact
- Any suggested fix (optional)

### Response Timeline

We aim to respond to security reports according to the following timeline:

- **Initial Response:** Within 48 hours
- **Status Update:** Within 72 hours
- **Fix Release:** Within 14 days (for confirmed vulnerabilities)
- **Public Disclosure:** After fix is released or 90 days (whichever comes first)

## Security Considerations

### Authentication & Authorization

Bob's Brain agents authenticate to Google Cloud Platform using:
- **Workload Identity Federation (WIF)** for GitHub Actions deployments
- **Service account credentials** for Agent Engine runtime (injected via GCP Secret Manager)
- **SPIFFE IDs** for inter-agent communication (R7 compliance)

All production credentials are:
- Never committed to source control
- Injected via environment variables or Secret Manager
- Rotated regularly per GCP best practices
- Audited in Cloud Audit Logs

### Code Analysis

This project uses automated security scanning:
- **Pre-commit hooks** for dependency vulnerability detection
- **Dependency checking** in CI/CD (GitHub Actions)
- **Type checking** (mypy) to catch unsafe patterns
- **Drift detection** to prevent forbidden imports or unsafe patterns

### Dependencies

Bob's Brain maintains a minimal dependency footprint:
- **Core:** Google ADK 1.18.0+, Vertex AI SDK
- **Development:** pytest, black, flake8, mypy
- **Infrastructure:** Terraform (for GCP resource management)

All dependencies are:
- Version-pinned in `requirements.txt`
- Scanned for vulnerabilities on each release
- Updated regularly with security patches

Check current dependencies:
```bash
pip list
pip show google-adk
```

### Deployment Security

All deployments use **CI-only deployment pattern** (R4 compliance):
- GitHub Actions with Workload Identity Federation
- Infrastructure as Code (Terraform) with state encryption
- Secrets managed via Google Cloud Secret Manager
- Agent Engine (managed service) with network isolation

**Never perform manual deployments with personal credentials.**

### Memory & State Management

Sensitive data handling follows ADK best practices:
- Session state stored in Vertex AI Session Service (encrypted at rest)
- Long-term knowledge in Vertex AI Memory Bank (encrypted)
- No sensitive data in logs or error messages
- Automatic session expiration policies

### Agent-to-Agent Communication

Inter-agent communication (A2A) is authenticated with:
- SPIFFE workload identities
- JWT token validation
- Correlation ID tracking for audit trails
- Network policies via VPC Service Controls (when deployed)

## Vulnerability Disclosure Policy

We follow responsible vulnerability disclosure principles:

1. **Private Reporting:** Report to jeremy@intentsolutions.io
2. **Confidentiality:** Vulnerability details kept confidential until patch is released
3. **Timeframe:** We commit to fixing confirmed vulnerabilities within 14 days
4. **Acknowledgment:** Reporters credited in release notes (if desired)
5. **Coordinated Disclosure:** Public disclosure only after fix is available

## Security Best Practices for Users

When using Bob's Brain in production:

1. **Keep Updated:** Run the latest version (0.12.x) for security patches
2. **Secrets Management:** Use Google Cloud Secret Manager, never hardcode credentials
3. **Service Accounts:** Create service accounts with least-privilege IAM roles
4. **Audit Logs:** Enable Cloud Audit Logs for all agent activities
5. **Network Security:** Deploy within VPC with appropriate firewall rules
6. **Monitoring:** Set up alerts for failed authentications or unusual agent behavior
7. **Dependency Scanning:** Regularly scan dependencies with `pip audit`

## Known Security Limitations

### Out of Scope

Bob's Brain does not provide:
- Encryption key management (use Google Cloud KMS)
- User authentication/authorization (defer to external IdP)
- Data loss prevention (implement organizational policies separately)
- Compliance certifications (SOC 2, ISO 27001 depend on deployment environment)

These should be handled at the infrastructure level by your organization.

## Security Updates

Security updates are released with patch version bumps (e.g., 0.12.1, 0.12.2):
- Available on GitHub Releases
- Documented in CHANGELOG.md
- Pushed to PyPI (if packaged)

To update:
```bash
pip install --upgrade bob-brain  # If packaged as wheel
# Or: git pull origin main && pip install -r requirements.txt
```

## Compliance

This project is designed to support compliance with:
- **Google Cloud Security Best Practices:** Follows ADK/Vertex guidelines
- **OWASP Secure Coding:** Type hints, input validation, no code injection
- **CIS Benchmarks:** Leverages Google Cloud's certified security controls
- **Least Privilege:** Agent service accounts have minimal required permissions

Specific compliance (SOC 2, ISO 27001, HIPAA, PCI-DSS) depends on deployment environment and your organization's policies.

## Security Advisories

For security advisories and updates, check:
- **GitHub Security Advisories:** https://github.com/yourusername/bobs-brain/security
- **Project Releases:** https://github.com/yourusername/bobs-brain/releases
- **CHANGELOG:** `CHANGELOG.md` (security section)

---

**Last Updated:** 2025-12-03
**Policy Version:** 1.0
**Status:** Active
