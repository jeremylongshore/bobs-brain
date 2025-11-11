# Contributing to Disposable Marketplace

Thank you for your interest in contributing to the Disposable Marketplace N8N workflow! This document provides guidelines for contributing to this project.

## Getting Started

### Prerequisites

- N8N instance (cloud or self-hosted)
- Node.js 18+ (for local testing)
- Git
- Basic understanding of N8N workflows

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/disposable-marketplace-n8n.git
   cd disposable-marketplace-n8n
   ```

2. **Install development tools**
   ```bash
   # Install jq for JSON validation
   sudo apt-get install jq  # Linux
   brew install jq          # macOS

   # Install shellcheck for script linting
   sudo apt-get install shellcheck  # Linux
   brew install shellcheck          # macOS
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your N8N instance details
   ```

4. **Import workflow into N8N**
   - Open your N8N instance
   - Go to Workflows → Import
   - Upload `workflow.json`
   - Configure required credentials (SMTP, Google Sheets)

## Making Changes

### Workflow Modifications

1. **Make changes in N8N interface**
   - Modify nodes, connections, or settings
   - Test your changes thoroughly

2. **Export updated workflow**
   - Use N8N's export feature
   - Replace `workflow.json` with the new version

3. **Validate changes**
   ```bash
   # Check JSON syntax
   jq empty workflow.json

   # Run full validation
   ./validate-workflow.sh
   ```

### Code Style Guidelines

- **JSON**: Use 2-space indentation (N8N default)
- **Shell Scripts**: Follow shellcheck recommendations
- **Commit Messages**: Use conventional commits format
  ```
  feat: add new webhook endpoint for offers
  fix: resolve CSV parsing issue
  docs: update installation guide
  ```

### Testing Your Changes

1. **Validate JSON structure**
   ```bash
   npm run validate  # or jq empty workflow.json
   ```

2. **Test the workflow end-to-end**
   ```bash
   # Update URLs in test script
   vim test-requests.sh

   # Run test script
   ./test-requests.sh
   ```

3. **Check CI pipeline locally**
   ```bash
   # Run the same checks as GitHub Actions
   shellcheck *.sh
   jq empty workflow.json
   ```

## Contribution Types

### Bug Fixes
- Fix workflow execution issues
- Resolve JSON validation errors
- Correct documentation errors

### Features
- Add new webhook endpoints
- Enhance scoring algorithms
- Improve error handling
- Add new integrations

### Documentation
- Improve setup instructions
- Add troubleshooting guides
- Create video tutorials
- Enhance API documentation

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the guidelines above
   - Test thoroughly
   - Update documentation if needed

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create PR on GitHub
   - Fill out the PR template
   - Wait for review

### PR Requirements

- [ ] All CI checks pass
- [ ] Workflow JSON is valid
- [ ] Changes are tested end-to-end
- [ ] Documentation is updated
- [ ] Breaking changes are documented

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Help others learn and contribute
- Focus on constructive feedback
- Report inappropriate behavior to jeremy@intentconsulting.ai

### Getting Help

- **Issues**: Create GitHub issues for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Email**: jeremy@intentconsulting.ai for security issues

## Development Tips

### N8N Workflow Best Practices
- Use descriptive node names
- Add notes to complex logic
- Test with small datasets first
- Use environment variables for credentials

### Common Issues
- **JSON Format**: Ensure proper formatting when exporting from N8N
- **Node Versions**: Check that node type versions match your N8N instance
- **Credentials**: Never commit sensitive data to the repository

### Useful Commands
```bash
# Validate workflow
jq empty workflow.json

# Format JSON (if needed)
jq '.' workflow.json > workflow.formatted.json

# Count workflow nodes
jq '.nodes | length' workflow.json

# Test webhook locally
curl -X POST "http://localhost:5678/webhook/test" -d '{"test": "data"}'
```

## Release Process

1. Features are merged to `master`
2. Releases are tagged semantically (v1.0.0, v1.1.0)
3. Release notes document breaking changes
4. Workflow compatibility is maintained when possible

Thank you for contributing! 🚀