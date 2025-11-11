# Security Policy

## Supported Versions

We currently support the following versions of Bob's Brain with security updates:

| Version | Supported          |
|---------|-------------------|
| 5.0.x   | :white_check_mark:|
| 4.x.x   | :x:               |
| < 4.0   | :x:               |

## Reporting a Vulnerability

### Responsible Disclosure Policy

We take the security of Bob's Brain seriously and appreciate your help in identifying and addressing potential vulnerabilities.

#### How to Report a Security Issue

1. **DO NOT** create a public GitHub issue for security vulnerabilities.
2. Send an email to `security@bobsbrain.ai` with the subject line "Security Vulnerability Report".
3. Include the following details in your report:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested mitigation strategies
   - Your contact information (optional)

#### What to Expect

- We aim to acknowledge receipt of your vulnerability report within 48 hours.
- Our security team will review and assess the reported issue.
- We will provide an estimated timeline for resolution.
- We may contact you for additional information or clarification.

### Disclosure Process

- Once a security issue is confirmed, we will:
  1. Develop a fix
  2. Test the fix thoroughly
  3. Release a security update
  4. Coordinate a responsible public disclosure

### Security Best Practices

#### For Users
- Always use the latest version of Bob's Brain
- Keep your API keys and credentials confidential
- Use environment variables or secret management systems
- Enable MFA where possible
- Regularly audit and rotate credentials

#### For API Keys
- Use Google Secret Manager or similar secure key storage
- Never commit API keys to version control
- Use read-only or scoped keys when possible
- Rotate keys periodically
- Set up key usage monitoring and alerts

## Bug Bounty and Recognition

While we do not currently have a formal bug bounty program, we appreciate and will acknowledge security researchers who help improve Bob's Brain's security.

Significant security contributions may be recognized in our documentation or release notes.

## Contact

For urgent security matters: `security@bobsbrain.ai`

## Legal

This security policy is subject to change. Last updated: 2025-10-05
