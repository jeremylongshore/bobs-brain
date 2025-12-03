# Contributing to Bob's Brain

Thank you for considering a contribution to Bob's Brain. This document provides guidelines and instructions for participating in the project.

## Table of Contents

- [Development Setup](#development-setup)
- [Architecture Fundamentals](#architecture-fundamentals)
- [Code Standards](#code-standards)
- [Commit Conventions](#commit-conventions)
- [Pull Request Process](#pull-request-process)
- [Testing Requirements](#testing-requirements)
- [Documentation Standards](#documentation-standards)

---

## Development Setup

### Prerequisites

- **Python 3.12+** (required for type hints and language features)
- **Google Cloud SDK** (`gcloud` CLI)
- **Virtual environment** (venv, conda, or equivalent)
- **Git** (for version control)

### Local Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bobs-brain.git
   cd bobs-brain
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development tools (pytest, black, flake8)
   ```

4. **Configure your environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your GCP project ID and other required variables
   ```

5. **Run setup verification:**
   ```bash
   make check-all  # Runs lint, type checks, tests, and compliance audits
   ```

---

## Architecture Fundamentals

Bob's Brain enforces **Hard Mode** architectural rules that ensure production-grade ADK and Vertex AI compliance. These rules are non-negotiable and enforced by CI/CD.

### Hard Mode Rules (R1-R8)

**R1: ADK-Only Framework**
- All agents must use Google ADK (`google.adk.agents.LlmAgent`)
- No mixing with LangChain, CrewAI, AutoGen, or custom frameworks
- ADK tools via `google.adk.tools` only

**R2: Vertex AI Agent Engine Runtime**
- Agents deploy to Vertex AI Agent Engine exclusively
- No self-hosted runners or custom orchestration
- Inline source deployment pattern (no serialization)

**R3: Gateway Separation**
- Cloud Run services act as REST proxies only
- No embedded agent runners in service layer
- Clean separation of API gateway and agent compute

**R4: CI-Only Deployments**
- Deployments only via GitHub Actions
- Workload Identity Federation (WIF) for authentication
- No manual `gcloud` deployments to production

**R5: Dual Memory Wiring**
- Session state via `VertexAiSessionService`
- Long-term knowledge via `VertexAiMemoryBankService`
- Automatic persistence with `after_agent_callback`

**R6: Single Documentation Folder**
- All docs in `000-docs/` directory
- Follow NNN-CC-ABCD naming convention
- No scattered README files across codebase

**R7: SPIFFE ID Propagation**
- Workload identity in AgentCard definitions
- Identity headers in all inter-agent communication
- Audit trail for all agent-to-agent calls

**R8: Drift Detection**
- Automated checks on every commit
- Blocks PRs with forbidden imports or patterns
- Runs first in CI pipeline before other checks

**Reference:** See `000-docs/6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md` for complete specification.

---

## Code Standards

### Python Style & Structure

**Type Hints (Required)**
```python
# All functions must have type hints
from typing import Optional, Dict, Any

def process_agent_result(
    result: Dict[str, Any],
    session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Process agent result with type safety."""
    return result
```

**Agent Factory Pattern**
```python
# agents/my_agent/agent.py
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

def get_agent() -> LlmAgent:
    """Factory function for agent creation."""
    tools = [
        FunctionTool(my_tool_function)
    ]

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",
        name="my_agent",
        instruction="Your system prompt here",
        tools=tools
    )

    return agent

# Module-level export for ADK CLI
root_agent = get_agent()
```

**Memory Wiring (R5 Compliance)**
```python
# Include session and memory bank setup
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService

def after_agent_callback(ctx):
    """Automatic session persistence (R5)."""
    # Save session to Memory Bank
    pass

agent = LlmAgent(
    ...,
    after_agent_callback=after_agent_callback
)
```

### Code Organization

**Agent Directory Structure:**
```
agents/
├── my_agent/
│   ├── agent.py           # Main agent definition (must export root_agent)
│   ├── tools.py           # Custom tools
│   ├── config.py          # Agent configuration
│   ├── prompts.py         # Prompt templates
│   └── __init__.py        # Package init
├── another_agent/
│   └── ...
└── __init__.py
```

**Import Conventions**
```python
# ADK imports
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.sessions import VertexAiSessionService

# Standard library
from typing import Optional, Dict, Any
from dataclasses import dataclass

# Project imports
from agents.common.tools import shared_tool
```

### Docstrings

Use Google-style docstrings (ADK introspects these for tool schemas):

```python
def create_task(
    title: str,
    description: str,
    priority: int = 1
) -> Dict[str, str]:
    """Create a task in the system.

    Args:
        title: The task title (max 100 characters).
        description: Detailed task description.
        priority: Priority level (1=low, 5=high). Defaults to 1.

    Returns:
        Dictionary with task ID and creation timestamp.

    Raises:
        ValueError: If title is empty or priority outside valid range.
    """
    # Implementation
    pass
```

### Linting & Formatting

**Code formatting:**
```bash
# Auto-format with Black
black agents/ tests/

# Check style with Flake8
flake8 agents/ tests/ --max-line-length=100
```

**Type checking:**
```bash
# Run mypy for type safety
mypy agents/ --strict
```

**Pre-commit hooks:**
The repo includes `.pre-commit-config.yaml`. Install hooks:
```bash
pre-commit install
pre-commit run --all-files  # Manual run
```

---

## Commit Conventions

Use **Conventional Commits** format for all commits:

```
<type>(<scope>): <subject>

<optional body>

<optional footer>
```

### Commit Types

- **feat** - New feature or capability
- **fix** - Bug fix
- **refactor** - Code restructuring (no feature change)
- **test** - Test additions or fixes
- **docs** - Documentation changes
- **ci** - CI/CD pipeline changes
- **chore** - Maintenance, dependency updates

### Commit Examples

**Good commits:**
```bash
git commit -m "feat(agents): add iam-adk-specialist agent with compliance auditing"
git commit -m "fix(memory): correct Memory Bank session persistence in after_callback"
git commit -m "docs(000-docs): add Hard Mode rules specification and architectural reference"
git commit -m "test(drift-detection): add test cases for forbidden import detection"
git commit -m "ci(workflows): add ARV checks to deployment pipeline"
```

**Bad commits:**
```bash
git commit -m "updates"
git commit -m "fix stuff"
git commit -m "working on agent"  # Vague and incomplete
```

### Scope Guidelines

- Use agent names: `agents`, `iam-adk`, `iam-issue`
- Use subsystem names: `memory`, `tools`, `config`
- Use doc types: `000-docs`, `CLAUDE.md`
- Use infrastructure: `terraform`, `workflows`, `docker`

---

## Pull Request Process

### Before Opening a PR

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/short-description
   # Example: feature/iam-adk-specialist
   ```

2. **Test locally:**
   ```bash
   make test              # Run test suite
   make lint-check        # Style and type checking
   make check-all         # Comprehensive check
   ```

3. **Ensure all checks pass:**
   - Linting (Black, Flake8)
   - Type checking (mypy)
   - Unit tests (pytest, 70% minimum coverage)
   - Drift detection (no forbidden imports)
   - ARV checks (Agent Readiness Verification)

4. **Update relevant documentation:**
   - Add tests for new functionality
   - Update `000-docs/` if changing architecture
   - Update CHANGELOG.md for user-facing changes

### Opening a PR

1. **Push your branch:**
   ```bash
   git push origin feature/short-description
   ```

2. **Create PR with clear description:**
   - Reference any related issues
   - Describe what changed and why
   - List any breaking changes
   - Include testing approach

3. **PR Title Format:**
   ```
   [Type]: Brief description

   Examples:
   [Feature]: Add iam-adk-specialist agent
   [Fix]: Correct Memory Bank persistence bug
   [Docs]: Add Hard Mode rules documentation
   ```

4. **PR Description Template:**
   ```markdown
   ## Description
   What does this PR do?

   ## Related Issues
   Fixes #123

   ## Changes Made
   - Change 1
   - Change 2

   ## Testing
   How was this tested?

   ## Breaking Changes
   - Breaking change 1 (if any)

   ## Checklist
   - [ ] Tests pass locally
   - [ ] Code follows style guidelines
   - [ ] Type hints are complete
   - [ ] Documentation updated
   - [ ] No forbidden imports (drift detection)
   ```

### PR Review Process

- Code review by maintainers
- All CI checks must pass
- At least one approval required
- Automated checks cannot be overridden
- Maintain 70% minimum test coverage

---

## Testing Requirements

### Test Coverage Minimum

**Requirement: 70% code coverage across all agent modules**

### Test Organization

```
tests/
├── unit/
│   ├── agents/
│   │   └── test_my_agent.py
│   ├── tools/
│   │   └── test_my_tool.py
│   └── memory/
│       └── test_session_service.py
├── integration/
│   ├── test_agent_engine_deployment.py
│   └── test_a2a_communication.py
└── conftest.py  # Shared fixtures
```

### Writing Tests

**Unit test example:**
```python
import pytest
from agents.my_agent.agent import get_agent

class TestMyAgent:
    """Test suite for my_agent."""

    @pytest.fixture
    def agent(self):
        """Create agent instance for testing."""
        return get_agent()

    def test_agent_initialization(self, agent):
        """Test agent creates successfully."""
        assert agent is not None
        assert agent.name == "my_agent"

    def test_tool_registration(self, agent):
        """Test all required tools are registered."""
        tool_names = [tool.name for tool in agent.tools]
        assert "required_tool" in tool_names
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agents --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/agents/test_my_agent.py -v

# Run tests matching pattern
pytest tests/ -k "test_agent" -v

# Watch mode (requires pytest-watch)
ptw
```

### Integration Testing

For Agent Engine deployment testing:
```bash
# Dry-run deployment checks
make check-inline-deploy-ready

# Smoke test (post-deployment)
make smoke-bob-agent-engine-dev
```

---

## Documentation Standards

### Doc Filing System (v3.0)

All documentation follows the **NNN-CC-ABCD naming convention:**

- **NNN** = Sequential number (001-999)
- **CC** = Category (PP, AT, AA, DR, etc.)
- **ABCD** = Document type (4-letter abbreviation)
- **description** = 1-4 words, kebab-case

### Category Codes

- **PP** = Product & Planning
- **AT** = Architecture & Technical
- **AA** = After-Action (Reports, Plans)
- **DR** = Documentation & Reference
- **TQ** = Testing & Quality
- **OD** = Operations & Deployment

### Document Types

- **ARCH** = Architecture design
- **PLAN** = Phase planning document
- **REPT** = After-Action Report
- **STND** = Standard specification
- **AUDT** = Audit or assessment
- **PROC** = Procedure or runbook

### Examples

- `001-AA-PLAN-agent-development-phase.md` - Phase planning
- `002-AT-ARCH-a2a-communication-design.md` - Architecture design
- `003-DR-STND-hard-mode-rules.md` - Standard specification
- `004-AA-REPT-phase-1-completion.md` - After-Action Report

### Documentation Guidelines

**In documentation:**
- Use clear, technical language
- Include code examples where relevant
- Link to related standards and specs
- Add timestamps (creation and last update)
- Keep document focused on single topic

**Header format:**
```markdown
# Document Title

**Document ID:** NNN-CC-ABCD-description
**Phase:** Phase name or status
**Status:** Draft / In Progress / Canonical Standard
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**Purpose:** One sentence describing document purpose
```

---

## Getting Help

### Resources

- **Issue Tracker:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Documentation:** `/000-docs/` directory
- **Main Reference:** `000-docs/6767-000-DR-INDEX-bobs-brain-standards-catalog.md`
- **Hard Mode Rules:** `000-docs/6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md`

### Questions or Issues

1. Check existing issues and discussions
2. Review documentation in `000-docs/`
3. Ask in GitHub Discussions
4. File an issue with clear reproduction steps

---

## Code of Conduct

This project adheres to the Contributor Covenant Code of Conduct. By participating, you agree to uphold this code.

---

**Last Updated:** 2025-12-03
**Version:** 1.0
**Status:** Active
