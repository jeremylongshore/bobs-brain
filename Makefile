# Bob's Brain - CRITICAL DEVELOPMENT RULES Makefile

.PHONY: lint-check test safe-commit setup-hooks help feature

# CRITICAL: Check current branch is NOT main
check-branch:
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" = "main" ]; then \
		echo "❌ CRITICAL ERROR: Cannot work on main branch!"; \
		echo "🔧 Create feature branch: make feature BRANCH=your-feature-name"; \
		exit 1; \
	fi
	@echo "✅ Branch check passed: $$(git rev-parse --abbrev-ref HEAD)"

# Set up CRITICAL git hooks
setup-hooks:
	@echo "🔧 Setting up CRITICAL DEVELOPMENT RULES..."
	@chmod +x .git/hooks/pre-commit-main-guard
	@echo "✅ Main branch protection enabled"

# Lint check with error handling
lint-check:
	@echo "🔍 Running CRITICAL lint checks..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 bob_agent/ *.py --max-line-length=120 --ignore=E501,W503,F401,W293,W291,W292,E722,F541,E231,E211,E203,E117,E221,E251 --exclude=venv_bob,__pycache__,.git || exit 1; \
	else \
		echo "⚠️ Installing flake8..."; \
		pip install flake8; \
		flake8 bob_agent/ *.py --max-line-length=120 --ignore=E501,W503,F401,W293,W291,W292,E722,F541,E231,E211,E203,E117,E221,E251 --exclude=venv_bob,__pycache__,.git || exit 1; \
	fi
	@echo "✅ Lint checks PASSED"

# Python syntax test
test:
	@echo "🧪 Running CRITICAL Python syntax checks..."
	@python3 -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('**/*.py', recursive=True) if not f.startswith('.')]"
	@echo "✅ Python syntax tests PASSED"

# CRITICAL safe commit process
safe-commit: check-branch lint-check test
	@echo "🎯 ALL CRITICAL SAFETY CHECKS PASSED!"
	@echo "✅ Ready to commit on branch: $$(git rev-parse --abbrev-ref HEAD)"

# Create feature branch (CRITICAL RULE)
feature:
	@if [ -z "$(BRANCH)" ]; then \
		echo "❌ Usage: make feature BRANCH=feature-name"; \
		exit 1; \
	fi
	@git checkout -b feature/$(BRANCH)
	@echo "✅ Created feature branch: feature/$(BRANCH)"

# Setup everything
setup: setup-hooks
	@echo "🚀 CRITICAL DEVELOPMENT RULES configured!"

# Help
help:
	@echo "🧠 Bob's Brain - CRITICAL DEVELOPMENT RULES:"
	@echo "  make setup-hooks  - Enable main branch protection"
	@echo "  make feature BRANCH=name - Create feature branch"
	@echo "  make lint-check   - Run CRITICAL lint checks"
	@echo "  make test         - Run CRITICAL syntax tests"
	@echo "  make safe-commit  - Full CRITICAL safety check"
	@echo "  make check-branch - Verify not on main branch"
