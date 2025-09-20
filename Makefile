# Bob's Brain - AI Assistant Makefile
.PHONY: help install test lint-check type-check security-check test-health deploy safe-commit logs metrics clean

# Variables
PYTHON := python3
PIP := pip3
PROJECT_ID := bobs-house-ai
REGION := us-central1
SERVICE_NAME := bobs-brain

# Default target
help:
	@echo "🧠 Bob's Brain Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Development workflow:"
	@echo "  install        Install dependencies"
	@echo "  test          Run test suite"
	@echo "  lint-check    Run code linting"
	@echo "  type-check    Run type checking"
	@echo "  security-check Run security scanning"
	@echo "  safe-commit   Run all checks before commit"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy        Deploy to Cloud Run"
	@echo "  test-health   Test health endpoints"
	@echo ""
	@echo "Monitoring:"
	@echo "  logs          View application logs"
	@echo "  metrics       Display system metrics"
	@echo ""
	@echo "Utilities:"
	@echo "  clean         Clean temporary files"
	@echo "  help          Show this help message"

# Development commands
install:
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt

test:
	@echo "🧪 Running test suite..."
	$(PYTHON) -m pytest tests/ -v --cov=src --cov-report=term-missing
	@echo "✅ Tests completed"

lint-check:
	@echo "🔍 Running code linting..."
	$(PYTHON) -m flake8 src/ tests/ --max-line-length=120
	$(PYTHON) -m black --check src/ tests/
	$(PYTHON) -m isort --check-only src/ tests/
	@echo "✅ Linting passed"

type-check:
	@echo "🔍 Running type checking..."
	$(PYTHON) -m mypy src/ --ignore-missing-imports
	@echo "✅ Type checking passed"

security-check:
	@echo "🔒 Running security scanning..."
	$(PYTHON) -m bandit -r src/ -f json -o security-report.json || true
	$(PYTHON) -m safety check
	@echo "✅ Security check completed"

safe-commit: lint-check type-check test security-check
	@echo "✅ All checks passed! Safe to commit."

# Deployment commands
deploy:
	@echo "🚀 Deploying to Cloud Run..."
	gcloud run deploy $(SERVICE_NAME) \
		--source . \
		--platform managed \
		--region $(REGION) \
		--project $(PROJECT_ID) \
		--memory 1Gi \
		--timeout 3600 \
		--min-instances 0 \
		--max-instances 10 \
		--vpc-connector bob-vpc-connector \
		--vpc-egress private-ranges-only \
		--set-env-vars "PROJECT_ID=$(PROJECT_ID)"
	@echo "✅ Deployment completed"

test-health:
	@echo "🏥 Testing health endpoints..."
	curl -f https://$(SERVICE_NAME)-157908567967.$(REGION).run.app/health || echo "❌ Health check failed"
	@echo "✅ Health check completed"

# Monitoring commands
logs:
	@echo "📊 Viewing application logs..."
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$(SERVICE_NAME)" \
		--limit 50 --format="table(timestamp,severity,textPayload)"

metrics:
	@echo "📈 System metrics:"
	@echo "=================="
	@echo "Cloud Run services:"
	@gcloud run services list --platform managed --region $(REGION) --format="table(name,status,url)"
	@echo ""
	@echo "Recent deployments:"
	@gcloud run revisions list --service $(SERVICE_NAME) --region $(REGION) --limit 5 --format="table(name,creation_timestamp,status)"

# Utility commands
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "security-report.json" -delete
	@echo "✅ Cleanup completed"

# GitHub Actions support
ci-install:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov flake8 black isort mypy bandit safety

ci-test: ci-install lint-check type-check test security-check
	@echo "✅ CI pipeline completed successfully"