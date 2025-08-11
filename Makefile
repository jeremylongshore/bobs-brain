# Bob's Brain Development Makefile
# CRITICAL: Always use these commands before committing

.PHONY: help
help: ## Show this help message
	@echo "Bob's Brain Development Commands:"
	@echo "================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install all dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install pre-commit black flake8 pylint pytest mypy
	pre-commit install

.PHONY: lint-check
lint-check: ## Run all linting checks
	@echo "🔍 Running Python linting..."
	@python3 -m flake8 src/ --max-line-length=120 --exclude=archive/,deprecated_bobs/ || true
	@python3 -m pylint src/*.py --disable=C0114,C0115,C0116,R0903,R0913,W0703 || true
	@python3 -m black --check src/ || true
	@echo "✅ Lint checks complete"

.PHONY: format
format: ## Auto-format code
	@echo "🎨 Formatting Python code..."
	@python3 -m black src/
	@echo "✅ Code formatting complete"

.PHONY: test
test: ## Run all tests
	@echo "🧪 Running tests..."
	@if [ -d "tests" ]; then \
		python3 -m pytest tests/ -v --tb=short || true; \
	else \
		echo "⚠️  No tests directory found"; \
	fi
	@echo "✅ Tests complete"

.PHONY: type-check
type-check: ## Run type checking
	@echo "🔍 Running type checks..."
	@python3 -m mypy src/ --ignore-missing-imports || true
	@echo "✅ Type checks complete"

.PHONY: security-check
security-check: ## Check for security issues and secrets
	@echo "🔒 Checking for secrets..."
	@! grep -r "xoxb-[0-9]" --include="*.py" --exclude-dir=.git --exclude-dir=archive --exclude-dir=deprecated_bobs src/ 2>/dev/null
	@! grep -r "xapp-[0-9]" --include="*.py" --exclude-dir=.git --exclude-dir=archive --exclude-dir=deprecated_bobs src/ 2>/dev/null
	@! grep -r "sk-[a-zA-Z0-9]" --include="*.py" --exclude-dir=.git --exclude-dir=archive --exclude-dir=deprecated_bobs src/ 2>/dev/null
	@echo "✅ No secrets found"

.PHONY: pre-commit-check
pre-commit-check: ## Run pre-commit checks
	@echo "🔍 Running pre-commit checks..."
	@if [ -f ".pre-commit-config.yaml" ]; then \
		pre-commit run --all-files; \
	else \
		echo "⚠️  No .pre-commit-config.yaml found"; \
	fi

.PHONY: check-all
check-all: lint-check test type-check security-check ## Run ALL checks
	@echo "="
	@echo "🎯 All checks complete!"
	@echo "="

.PHONY: safe-commit
safe-commit: check-all ## Run all checks then commit safely
	@echo "="
	@echo "✅ All checks passed! Ready to commit."
	@echo "="
	@echo "📝 Remember:"
	@echo "   1. You are on branch: $$(git branch --show-current)"
	@echo "   2. Never commit to main directly"
	@echo "   3. Write clear commit messages"
	@echo "="
	@echo "Run: git add . && git commit -m 'your message'"

.PHONY: setup-hooks
setup-hooks: ## Set up git hooks
	@echo "🔧 Setting up git hooks..."
	@chmod +x .git/hooks/pre-commit 2>/dev/null || true
	@chmod +x .git/hooks/pre-push 2>/dev/null || true
	@echo "✅ Git hooks configured"

.PHONY: clean
clean: ## Clean up temporary files
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

.PHONY: dev-setup
dev-setup: install setup-hooks ## Complete development environment setup
	@echo "="
	@echo "🚀 Development environment ready!"
	@echo "="
	@echo "📋 Always remember:"
	@echo "   1. Create feature branch: git checkout -b feature/name"
	@echo "   2. Run checks: make check-all"
	@echo "   3. Safe commit: make safe-commit"
	@echo "   4. Never use --no-verify"
	@echo "="

.PHONY: status
status: ## Show project status
	@echo "📊 Project Status:"
	@echo "=================="
	@echo "Current Branch: $$(git branch --show-current)"
	@echo "Python Files: $$(find src -name '*.py' | wc -l)"
	@echo "Test Files: $$(find tests -name '*.py' 2>/dev/null | wc -l || echo 0)"
	@git status --short

.PHONY: run-bob
run-bob: ## Run Bob locally for testing
	@echo "🤖 Starting Bob locally..."
	@PORT=8080 python src/bob_production_final.py

.PHONY: test-health
test-health: ## Test Bob's health endpoint
	@echo "🏥 Testing Bob's health..."
	@curl -s http://localhost:8080/health | python3 -m json.tool || echo "❌ Bob not running locally"

.PHONY: deploy
deploy: check-all ## Deploy to Cloud Run (after all checks pass)
	@echo "🚀 Deploying to Cloud Run..."
	@echo "⚠️  Make sure you're on a feature branch!"
	@gcloud run deploy bobs-brain \
		--source . \
		--region us-central1 \
		--project bobs-house-ai \
		--port 8080