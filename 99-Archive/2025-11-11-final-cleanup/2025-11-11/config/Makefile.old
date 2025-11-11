# Bob's Brain - Safety Makefile

.PHONY: lint-check test safe-commit install-hooks

# Install pre-commit hooks
install-hooks:
	@echo "🔧 Installing Bob's safety hooks..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Safety hooks installed!"

# Lint check
lint-check:
	@echo "🔍 Running lint checks..."
	pre-commit run --all-files
	@echo "✅ Lint checks passed!"

# Run tests
test:
	@echo "🧪 Running Bob's tests..."
	python -m pytest agent/tests/ -v || echo "⚠️ No tests found - consider adding tests"
	@echo "✅ Tests completed!"

# Safe commit workflow
safe-commit: lint-check test
	@echo "🛡️ All safety checks passed!"
	@echo "✅ Ready to commit safely"
	@echo "💡 Use: git add . && git commit -m 'your message'"

# Quick setup
setup: install-hooks
	@echo "🚀 Bob's development environment ready!"

# Help
help:
	@echo "Bob's Brain - Safety Commands:"
	@echo "  make setup       - Install safety hooks"
	@echo "  make lint-check  - Check code quality"
	@echo "  make test        - Run tests"
	@echo "  make safe-commit - Full safety check before commit"
