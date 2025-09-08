# Contributing to Bob's Brain

First off, thank you for considering contributing to Bob's Brain! 🤖

Bob has evolved through many iterations, and your contributions help make him even better. Whether you're fixing bugs, adding features, or improving documentation, every contribution is valued.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Versioning](#versioning)

## Code of Conduct

By participating in this project, you agree to:
- Be respectful and inclusive
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/bobs-brain.git
   cd bobs-brain
   ```

2. **Set up your environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Explore Bob's versions**
   ```bash
   ./scripts/version-selector.py
   ```

## How to Contribute

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- Bob version affected (v1-basic, v2-unified, etc.)
- Detailed steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)
- Relevant logs or error messages

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- Clear use case explanation
- Why this enhancement would be useful
- Possible implementation approach
- Which Bob version(s) it affects

### 🔧 Adding a New Bob Version

To add a new Bob version:

1. Create directory: `versions/vX-description/`
2. Add version-specific code and requirements
3. Update `scripts/version-selector.py`
4. Document in `VERSIONS.md`
5. Add tests in `tests/test_vX_description.py`
6. Create Docker configuration if applicable

## Development Process

### 1. Branch Strategy

```
main (protected)
├── develop (integration branch)
├── feature/your-feature-name
├── bugfix/issue-description
└── hotfix/critical-fix
```

### 2. Development Workflow

1. Create a feature branch from `develop`
   ```bash
   git checkout -b feature/amazing-feature develop
   ```

2. Make your changes
   - Write/update tests
   - Update documentation
   - Follow style guidelines

3. Test your changes
   ```bash
   make test
   make lint-check
   ```

4. Commit your changes (see commit message guidelines)

5. Push to your fork
   ```bash
   git push origin feature/amazing-feature
   ```

6. Create a Pull Request to `develop` branch

## Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to all functions and classes

Example:
```python
def process_message(self, message: str, user_id: str) -> str:
    """
    Process incoming message and generate response.
    
    Args:
        message: The user's input message
        user_id: Unique identifier for the user
        
    Returns:
        Generated response string
    """
    # Implementation here
```

### Code Organization

- Keep versions isolated in their directories
- Shared utilities go in `utils/` (if needed)
- Tests mirror the source structure
- Documentation stays up-to-date with code

## Commit Messages

Follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc.
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

### Examples
```
feat(v2): Add rate limiting to Slack responses

Implements exponential backoff for Slack API calls to prevent
rate limit errors during high traffic periods.

Closes #123
```

```
fix(v1): Correct ChromaDB connection timeout

Increases timeout from 5s to 30s to handle larger knowledge bases.
```

## Pull Request Process

1. **Before submitting:**
   - Ensure all tests pass
   - Update documentation
   - Add your changes to CHANGELOG.md (if exists)
   - Self-review your code

2. **PR Title Format:**
   ```
   [Version] Type: Brief description
   ```
   Examples:
   - `[v2] feat: Add conversation export feature`
   - `[v1] fix: Handle empty knowledge base gracefully`
   - `[All] docs: Update installation instructions`

3. **PR Description Template:**
   ```markdown
   ## Summary
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] Added new tests
   - [ ] Tested on Python 3.9+
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No hardcoded secrets
   ```

4. **Review Process:**
   - At least one approval required
   - CI checks must pass
   - Address all review comments
   - Squash commits if requested

## Versioning

### For Bob Versions
- Major versions (v1, v2): Significant architecture changes
- Minor updates: Features within a version
- Patches: Bug fixes

### For Repository
We use [SemVer](http://semver.org/):
- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible functionality
- PATCH: Backwards-compatible bug fixes

## Testing Guidelines

### Writing Tests
```python
# tests/test_v1_basic.py
def test_feature_name():
    """Test description"""
    # Arrange
    bob = BobBrain()
    
    # Act
    result = bob.process("test input")
    
    # Assert
    assert result is not None
    assert "expected" in result
```

### Running Tests
```bash
# All tests
pytest

# Specific version
pytest tests/test_v1_basic.py

# With coverage
pytest --cov=versions --cov-report=html
```

## Documentation

### Where to Document
- **Code**: Inline comments and docstrings
- **Features**: Update README.md and VERSIONS.md
- **API Changes**: Update relevant documentation
- **Examples**: Add to `examples/` directory

### Documentation Style
- Use clear, concise language
- Include code examples
- Explain the "why" not just the "what"
- Keep it up-to-date

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in PR comments
- Contact maintainers

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in commit messages

---

Thank you for contributing to Bob's Brain! Together we're building an amazing AI assistant that helps businesses thrive. 🚀

*Remember: Bob started simple and evolved through contributions like yours!*