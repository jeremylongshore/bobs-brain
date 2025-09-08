# Bob's Brain - Enhanced Makefile
# Professional development workflow for all Bob versions

.PHONY: help setup test lint format clean docker version benchmark ci all

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
FLAKE8 := $(PYTHON) -m flake8
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Version selector
VERSION ?= current

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

#################################
# Help & Information
#################################

help: ## Show this help message
	@echo "$(BLUE)🤖 Bob's Brain - Development Makefile$(NC)"
	@echo "$(BLUE)=====================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Version-specific targets:$(NC)"
	@echo "  $(GREEN)run-v1$(NC)               Run Bob v1 (Basic CLI)"
	@echo "  $(GREEN)run-v2$(NC)               Run Bob v2 (Slack Bot)"
	@echo "  $(GREEN)test-v1$(NC)              Test Bob v1"
	@echo "  $(GREEN)test-v2$(NC)              Test Bob v2"
	@echo ""
	@echo "$(YELLOW)Docker targets:$(NC)"
	@echo "  $(GREEN)docker-v1$(NC)            Build & run Bob v1 in Docker"
	@echo "  $(GREEN)docker-v2$(NC)            Build & run Bob v2 in Docker"
	@echo "  $(GREEN)docker-all$(NC)           Run all versions in Docker"

#################################
# Setup & Installation
#################################

setup: ## Complete development environment setup
	@echo "$(BLUE)🔧 Setting up Bob's Brain development environment...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt 2>/dev/null || true
	$(PIP) install pre-commit pytest black flake8 mypy
	pre-commit install
	@echo "$(GREEN)✅ Development environment ready!$(NC)"

install-hooks: ## Install git pre-commit hooks
	@echo "$(BLUE)🔧 Installing git hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Git hooks installed!$(NC)"

deps: ## Install all dependencies
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed!$(NC)"

#################################
# Code Quality
#################################

lint: ## Run linting checks
	@echo "$(BLUE)🔍 Running lint checks...$(NC)"
	$(FLAKE8) . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(FLAKE8) . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(GREEN)✅ Lint checks passed!$(NC)"

format: ## Format code with black
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	$(BLACK) .
	@echo "$(GREEN)✅ Code formatted!$(NC)"

format-check: ## Check code formatting without changes
	@echo "$(BLUE)🎨 Checking code format...$(NC)"
	$(BLACK) --check .
	@echo "$(GREEN)✅ Code format check passed!$(NC)"

type-check: ## Run type checking with mypy
	@echo "$(BLUE)🔍 Running type checks...$(NC)"
	mypy versions/ --ignore-missing-imports || true
	@echo "$(GREEN)✅ Type check completed!$(NC)"

#################################
# Testing
#################################

test: ## Run all tests
	@echo "$(BLUE)🧪 Running all tests...$(NC)"
	$(PYTEST) tests/ -v --color=yes
	@echo "$(GREEN)✅ All tests passed!$(NC)"

test-v1: ## Test Bob v1 specifically
	@echo "$(BLUE)🧪 Testing Bob v1...$(NC)"
	$(PYTEST) tests/test_v1_basic.py -v --color=yes
	@echo "$(GREEN)✅ Bob v1 tests passed!$(NC)"

test-v2: ## Test Bob v2 specifically
	@echo "$(BLUE)🧪 Testing Bob v2...$(NC)"
	$(PYTEST) tests/test_v2_unified.py -v --color=yes
	@echo "$(GREEN)✅ Bob v2 tests passed!$(NC)"

test-coverage: ## Run tests with coverage report
	@echo "$(BLUE)📊 Running tests with coverage...$(NC)"
	$(PYTEST) tests/ --cov=versions --cov-report=html --cov-report=term
	@echo "$(GREEN)✅ Coverage report generated in htmlcov/$(NC)"

#################################
# Running Bob Versions
#################################

run-v1: ## Run Bob v1 (Basic CLI)
	@echo "$(BLUE)🤖 Starting Bob v1 (Basic CLI)...$(NC)"
	cd versions/v1-basic && $(PYTHON) run_bob.py

run-v2: ## Run Bob v2 (Slack Bot)
	@echo "$(BLUE)🤖 Starting Bob v2 (Slack Bot)...$(NC)"
	cd versions/v2-unified && ./start_unified_bob_v2.sh

run-selector: ## Run interactive version selector
	@echo "$(BLUE)🎯 Starting version selector...$(NC)"
	$(PYTHON) scripts/version-selector.py

#################################
# Docker Operations
#################################

docker-build: ## Build all Docker images
	@echo "$(BLUE)🐳 Building Docker images...$(NC)"
	$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✅ Docker images built!$(NC)"

docker-v1: ## Run Bob v1 in Docker
	@echo "$(BLUE)🐳 Running Bob v1 in Docker...$(NC)"
	$(DOCKER_COMPOSE) --profile v1 up

docker-v2: ## Run Bob v2 in Docker
	@echo "$(BLUE)🐳 Running Bob v2 in Docker...$(NC)"
	$(DOCKER_COMPOSE) --profile v2 up

docker-all: ## Run all versions in Docker
	@echo "$(BLUE)🐳 Running all Bob versions...$(NC)"
	$(DOCKER_COMPOSE) --profile all up

docker-stop: ## Stop all Docker containers
	@echo "$(BLUE)🛑 Stopping Docker containers...$(NC)"
	$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✅ Containers stopped!$(NC)"

docker-clean: ## Clean Docker volumes and images
	@echo "$(YELLOW)⚠️  Cleaning Docker resources...$(NC)"
	$(DOCKER_COMPOSE) down -v
	docker image prune -f
	@echo "$(GREEN)✅ Docker cleaned!$(NC)"

#################################
# Benchmarks & Performance
#################################

benchmark: ## Run performance benchmarks
	@echo "$(BLUE)📊 Running performance benchmarks...$(NC)"
	$(PYTHON) tests/benchmarks.py 2>/dev/null || echo "$(YELLOW)⚠️  Benchmarks not implemented yet$(NC)"

#################################
# CI/CD Commands
#################################

ci: lint test ## Run CI checks (lint + test)
	@echo "$(GREEN)✅ CI checks passed!$(NC)"

safe-commit: lint format-check test ## Full safety check before commit
	@echo "$(GREEN)🛡️ All safety checks passed!$(NC)"
	@echo "$(GREEN)✅ Ready to commit safely$(NC)"
	@echo "$(BLUE)💡 Use: git add . && git commit -m 'your message'$(NC)"

pre-release: ci docker-build ## Prepare for release
	@echo "$(BLUE)📦 Preparing release...$(NC)"
	@echo "$(GREEN)✅ Ready for release!$(NC)"

#################################
# Cleanup
#################################

clean: ## Clean temporary files and caches
	@echo "$(BLUE)🧹 Cleaning temporary files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete 2>/dev/null || true
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf .mypy_cache
	@echo "$(GREEN)✅ Cleaned!$(NC)"

clean-all: clean docker-clean ## Deep clean including Docker
	@echo "$(GREEN)✅ Deep clean completed!$(NC)"

#################################
# Development Utilities
#################################

version: ## Show Bob versions
	@echo "$(BLUE)📌 Bob's Brain Versions:$(NC)"
	@echo "  v1-basic:  Simple CLI Assistant"
	@echo "  v2-unified: Enterprise Slack Bot"
	@echo ""
	@echo "$(BLUE)📦 Package versions:$(NC)"
	@$(PYTHON) --version
	@$(PIP) show slack-sdk 2>/dev/null | grep Version || echo "slack-sdk: not installed"
	@$(PIP) show chromadb 2>/dev/null | grep Version || echo "chromadb: not installed"

logs: ## Show recent logs
	@echo "$(BLUE)📜 Recent logs:$(NC)"
	tail -n 50 logs/*.log 2>/dev/null || echo "$(YELLOW)No logs found$(NC)"

#################################
# Composite Targets
#################################

all: setup lint test ## Complete setup, lint, and test
	@echo "$(GREEN)✅ All tasks completed!$(NC)"

dev: setup run-selector ## Setup and run version selector
	@echo "$(GREEN)✅ Development mode ready!$(NC)"

prod: docker-v2 ## Production deployment (Docker v2)
	@echo "$(GREEN)✅ Production deployment started!$(NC)"

.PHONY: help setup test lint format clean docker version benchmark ci all
.PHONY: install-hooks deps format-check type-check
.PHONY: test-v1 test-v2 test-coverage
.PHONY: run-v1 run-v2 run-selector
.PHONY: docker-build docker-v1 docker-v2 docker-all docker-stop docker-clean
.PHONY: safe-commit pre-release clean-all version logs dev prod