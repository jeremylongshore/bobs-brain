# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email security reports to: jeremy@intentconsulting.ai
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Any suggested fixes (if applicable)

### What to Expect

- **Response Time**: We will acknowledge receipt within 24 hours
- **Investigation**: We will investigate and respond within 5 business days
- **Resolution**: Critical vulnerabilities will be addressed within 7 days
- **Disclosure**: We follow responsible disclosure practices

### Security Considerations for N8N Workflows

This project contains N8N workflow configurations that may process sensitive data:

- **Data Handling**: Ensure all CSV URLs use HTTPS
- **API Security**: Validate all webhook endpoints before deployment
- **Email Security**: Use secure SMTP configurations with proper authentication
- **Environment Variables**: Never commit sensitive credentials to the repository

### Scope

Security issues we consider in scope:
- Credential exposure in workflow configurations
- Insecure data transmission
- Input validation vulnerabilities
- Authentication/authorization bypasses

Out of scope:
- Issues in third-party N8N platform itself
- General N8N configuration recommendations
- Performance issues without security impact

## Security Best Practices

When deploying this workflow:

1. **Environment Variables**: Store all credentials as environment variables
2. **HTTPS Only**: Ensure all external URLs use HTTPS
3. **Input Validation**: Validate all webhook inputs
4. **Access Control**: Restrict webhook access to trusted sources
5. **Regular Updates**: Keep N8N platform updated to latest version

Thank you for helping keep our project secure!