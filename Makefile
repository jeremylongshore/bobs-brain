.PHONY: run fmt test check-all lint type-check security-check install dev-install

# Development commands
run:
	BB_API_KEY=test python -m flask --app src.bob_brain_v5 run --host 0.0.0.0 --port 8080

dev-run:
	BB_API_KEY=test FLASK_ENV=development python -m flask --app src.bob_brain_v5 run --host 0.0.0.0 --port 8080 --debug

# Code quality
fmt:
	isort src tests
	black src tests --line-length=120

lint:
	flake8 src tests --max-line-length=120

type-check:
	mypy --ignore-missing-imports src

security-check:
	bandit -r src
	safety check

# Testing
test:
	BB_API_KEY=test PYTHONPATH=src pytest -q

test-verbose:
	BB_API_KEY=test PYTHONPATH=src pytest -v

test-coverage:
	BB_API_KEY=test PYTHONPATH=src pytest --cov=src --cov-report=html

# All checks (pre-commit)
check-all: lint type-check security-check test

# Installation
install:
	pip install -r requirements.txt

dev-install:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black isort mypy bandit safety

# Clean up
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/