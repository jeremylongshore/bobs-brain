# 🤝 Contributing to Bob's Brain

We love your input! We want to make contributing to Bob's Brain as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Quick Start for Contributors

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/YOUR-USERNAME/bobs-brain.git`
3. **Install** dependencies: `make install`
4. **Create** a feature branch: `git checkout -b feature/amazing-feature`
5. **Make** your changes
6. **Test** your changes: `make safe-commit`
7. **Push** to your fork: `git push origin feature/amazing-feature`
8. **Create** a Pull Request

## 🎯 Areas Where We Need Help

### 🧠 AI/ML Engineers
- **Model Fine-tuning**: Improve response quality and accuracy
- **Learning Algorithms**: Enhance the Circle of Life feedback loop
- **Memory Systems**: Optimize graph database relationships
- **Predictive Analytics**: Build maintenance prediction models

### 🌐 Data Engineers
- **Web Scrapers**: Add new data sources (forums, documentation sites)
- **Data Quality**: Implement validation and deduplication pipelines
- **ETL Optimization**: Improve data processing performance
- **API Integrations**: Connect to manufacturer APIs

### 🔧 DevOps Engineers
- **Infrastructure**: Optimize Google Cloud Run configurations
- **Monitoring**: Enhance observability and alerting
- **CI/CD**: Improve deployment pipelines
- **Cost Optimization**: Reduce operational expenses

### 📝 Technical Writers
- **Documentation**: Create user guides and tutorials
- **API Docs**: Document REST endpoints and responses
- **Architecture Guides**: Explain system design decisions
- **Troubleshooting**: Build comprehensive error resolution guides

### 🧪 QA Engineers
- **Test Coverage**: Expand unit and integration tests
- **Automation**: Build end-to-end test suites
- **Performance Testing**: Load test critical endpoints
- **Security Testing**: Vulnerability assessments

## 🛠️ Development Workflow

### Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Install Python dependencies
make install

# Set up pre-commit hooks
pre-commit install

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### Required Environment Variables

```bash
# Required for local development
SLACK_BOT_TOKEN=xoxb-your-token-here
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
PROJECT_ID=your-gcp-project-id

# Optional for testing
NEO4J_URI=bolt://localhost:7687
NEO4J_AUTH=neo4j/password
```

### Making Changes

1. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Follow our coding standards**:
   - Python: PEP 8 compliance (enforced by Black)
   - Line length: 120 characters maximum
   - Type hints required for all functions
   - Docstrings for public methods

3. **Write tests** for your changes:
   ```bash
   # Add tests in tests/ directory
   # Run tests locally
   make test
   ```

4. **Run quality checks**:
   ```bash
   make safe-commit
   ```

5. **Commit with descriptive messages**:
   ```bash
   git commit -m "feat(scraper): Add manufacturer API integration

   - Implemented API client for Bobcat parts catalog
   - Added rate limiting to prevent throttling
   - Created caching layer for frequent queries

   Resolves: #123"
   ```

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ai): Add conversation context memory
fix(slack): Resolve webhook timeout issues
docs(api): Update endpoint documentation
test(scraper): Add YouTube scraper tests
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_specific.py

# Run with coverage
python -m pytest --cov=src tests/

# Run integration tests
python scripts/testing/test_complete_flow.py
```

### Writing Tests

- **Unit tests**: Test individual functions and classes
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete user workflows

Example test structure:
```python
import pytest
from src.bob_brain_v5 import BobBrain

class TestBobBrain:
    def test_process_message_valid_input(self):
        """Test message processing with valid input."""
        bob = BobBrain()
        result = bob.process_message("Hello Bob")
        assert result is not None
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_slack_integration(self):
        """Test Slack integration functionality."""
        # Test implementation
        pass
```

## 📋 Pull Request Process

### Before Submitting

1. **Update documentation** if you've changed APIs
2. **Add tests** for new functionality
3. **Run the full test suite**: `make safe-commit`
4. **Update CHANGELOG.md** if it's a significant change
5. **Ensure CI passes** on your branch

### PR Guidelines

1. **Use descriptive titles**: "Add YouTube transcript extraction feature"
2. **Reference issues**: "Closes #123" or "Fixes #456"
3. **Provide context**: Explain what and why, not just what
4. **Keep changes focused**: One feature/fix per PR
5. **Update tests**: Ensure test coverage doesn't decrease

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Refactoring

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Breaking changes documented
```

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** and test again
3. **Check documentation** for known issues

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen

**Environment:**
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.11.2]
- Bob's Brain version: [e.g. v1.2.3]

**Additional context**
Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
Description of the problem

**Describe the solution you'd like**
Clear description of desired functionality

**Describe alternatives you've considered**
Other solutions you've thought about

**Additional context**
Any other relevant information
```

## 🏆 Recognition

Contributors are recognized in several ways:

- **README Contributors Section**: Listed with GitHub avatars
- **Release Notes**: Credited for significant contributions
- **Hall of Fame**: Special recognition for major contributions
- **Swag**: Bob's Brain stickers and shirts for active contributors

## 🔒 Security

### Reporting Security Issues

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email security concerns to [project maintainer]
2. Use GitHub's private vulnerability reporting
3. Allow 90 days for coordinated disclosure

### Security Guidelines

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Follow principle of least privilege
- Regular dependency updates for security patches

## 📚 Resources

### Documentation
- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

### Tools & Links
- [Google Cloud Console](https://console.cloud.google.com/)
- [Slack API Documentation](https://api.slack.com/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [GitHub Issues](https://github.com/jeremylongshore/bobs-brain/issues)

### Community
- [GitHub Discussions](https://github.com/jeremylongshore/bobs-brain/discussions)
- [Discord Server](https://discord.gg/bobs-brain) (coming soon)

## 📞 Getting Help

Stuck? Need help? Here's how to get support:

1. **Check Documentation**: Start with our comprehensive docs
2. **Search Issues**: Someone might have had the same problem
3. **GitHub Discussions**: Ask questions and share ideas
4. **Create an Issue**: For bugs or feature requests

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Project maintainers are responsible for clarifying standards and may take corrective action in response to unacceptable behavior.

---

## 🎉 Thank You!

Your contributions make Bob's Brain better for everyone. Whether you're fixing a typo or adding a major feature, every contribution matters.

**Happy coding! 🧠✨**