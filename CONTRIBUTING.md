# Contributing to Bob's Brain

First off, thank you for considering contributing to Bob's Brain! It's people like you that make Bob's Brain such a great tool.

## Code of Conduct

This project and everyone participating in it are governed by our Code of Conduct. By participating, you are expected to uphold this code.

## Development Setup

### Prerequisites
- Python 3.11+
- pipenv or poetry
- Docker (optional, for containerized development)
- Google Cloud SDK (for deployment)

### Local Development Environment

1. Clone the repository:
```bash
git clone https://github.com/your-username/bobs-brain.git
cd bobs-brain
```

2. Set up virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Standards

### Style Guide
- We use Black for code formatting
- Use `isort` for import sorting
- Use `mypy` for type checking
- Maximum line length: 120 characters

### Running Code Quality Checks
```bash
make lint-check     # Run linters
make type-check    # Run type checking
make test          # Run comprehensive test suite
```

## Testing

### Test Requirements
- All new code must have unit tests
- Aim for at least 65% test coverage
- Use pytest for testing
- Write clear, descriptive test names

### Running Tests
```bash
pytest                  # Run all tests
pytest tests/           # Run specific test directory
pytest tests/test_ai.py # Run specific test file
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run all tests and checks: `make safe-commit`
5. Commit your changes with a clear, descriptive commit message
   - Use conventional commits: `type(scope): description`
   - Example: `feat(ai): add new learning capability`
6. Push to your fork
7. Open a Pull Request

### Commit Message Convention
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code formatting, no code change
- `refactor`: Code restructuring without changing behavior
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

## Reporting Bugs or Suggesting Enhancements

1. Check existing issues to avoid duplicates
2. Use the issue template
3. Provide a clear and descriptive title
4. Include steps to reproduce the issue
5. Describe the expected vs. actual behavior
6. Include system details (Python version, OS, etc.)

## Questions?

If you have questions or need help, please open an issue with the `question` label.

## Thank You!

Your contributions make Bob's Brain better for everyone. We appreciate your help!
