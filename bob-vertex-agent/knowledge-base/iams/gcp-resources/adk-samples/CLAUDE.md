# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **Agent Development Kit (ADK) Samples** repository, containing production-ready sample agents built with Google's [Agent Development Kit](https://google.github.io/adk-docs/). The repository demonstrates agent architectures ranging from simple conversational bots to complex multi-agent orchestration workflows across various industry verticals.

**Repository Status:** Transitioning to live/production repository. Follow production best practices for all development work.

## Quick Start for Production Development

**Before writing any code:**

1. **Never commit secrets**
   ```bash
   # Verify .gitignore includes .env files
   git status --ignored | grep .env
   ```

2. **Use Secret Manager for credentials**
   ```bash
   # Store secrets in GCP Secret Manager
   gcloud secrets create my-api-key --data-file=-
   # (paste your key, then Ctrl+D)
   ```

3. **Replace mock tools with production implementations**
   - Check `tools/tools.py` for mock functions
   - Implement real API calls with proper error handling
   - Use Secret Manager for API credentials

4. **Test thoroughly before deployment**
   ```bash
   poetry install
   make lint && make test
   # Run evaluations if available
   python eval/test_eval.py
   ```

5. **Set up monitoring and alerts**
   - Enable Cloud Monitoring for deployed agents
   - Set budget alerts in Cloud Console
   - Configure error reporting

## Prerequisites

Before working with any agent in this repository:

1. **ADK Installation Required:** All agents require the Agent Development Kit to be installed. See the [ADK Installation Guide](https://google.github.io/adk-docs/get-started/installation).

2. **Python Requirements:**
   - Python 3.9+ (most agents require 3.10+)
   - [Poetry](https://python-poetry.org/docs/#installation) for dependency management

3. **Google Cloud Setup (Recommended):**
   - Active Google Cloud project
   - Vertex AI API enabled
   - Proper credentials configured
   - See [ADK Quickstart](https://google.github.io/adk-docs/get-started/quickstart/#python) for setup

4. **Environment Configuration:**
   - **Local Development Only:** Use `.env` files created from `.env.example` for testing
   - **Production/Live:** **MUST use Google Secret Manager** - never use `.env` in production
   - Common variables:
     ```
     GOOGLE_GENAI_USE_VERTEXAI=1
     GOOGLE_CLOUD_PROJECT=<your-project-id>
     GOOGLE_CLOUD_LOCATION=<your-location>
     GOOGLE_CLOUD_STORAGE_BUCKET=<your-bucket>
     ```
   - **Critical:** Never commit `.env` files. Add to `.gitignore` immediately.

## Repository Structure

```
adk-samples/
├── python/agents/          # 27+ Python agent samples
│   ├── llm-auditor/       # Example: multi-agent with critic/reviser
│   ├── customer-service/  # Advanced single-agent with tools
│   ├── data-science/      # Multi-agent for data analysis
│   └── [other agents]/
├── java/agents/           # Java agent samples
│   ├── software-bug-assistant/
│   └── time-series-forecasting/
└── .github/workflows/     # CI/CD for automated testing
```

## Common Development Commands

### Working with an Agent

All commands should be run from the **specific agent's directory** (e.g., `python/agents/llm-auditor/`):

```bash
# 1. Navigate to agent directory
cd python/agents/<agent-name>

# 2. Install dependencies
poetry install

# 3. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 4. Run agent locally (CLI mode)
# Run from the agent's core code directory (e.g., llm_auditor/)
cd <agent_name>/
adk run .

# 5. Run agent with web UI
# Run from the agent's main directory
cd ..
adk web
# Then open browser and select agent from dropdown

# 6. Run evaluations (if available)
cd eval/
python test_eval.py

# 7. Run unit tests (if available)
cd tests/
pytest

# 8. Deploy to Vertex AI Agent Engine
cd deployment/
python deploy.py
```

### Testing Infrastructure

The repository uses automated CI/CD testing via GitHub Actions:

```bash
# Tests run automatically on PRs for agents with:
# - [tool.agent-starter-pack] section in pyproject.toml
# - deployment_targets defined

# Local testing follows the same pattern:
make install    # Install dependencies
make lint       # Run linting
make test       # Run tests
make backend    # Start backend server
```

## Agent Architecture Patterns

### Standard Directory Structure

Each agent follows this pattern (hyphens in folder name, underscores in code):

```
agent-name/                         # Main directory (kebab-case)
├── agent_name/                     # Core code (snake_case)
│   ├── __init__.py                # Package initialization
│   ├── agent.py                   # Main agent logic
│   ├── prompt.py                  # Agent prompts
│   ├── tools/                     # Custom tools
│   ├── sub_agents/                # Sub-agent definitions
│   │   ├── critic/
│   │   │   ├── agent.py
│   │   │   ├── prompt.py
│   │   │   └── tools/
│   │   └── reviser/
│   └── shared_libraries/          # Shared helper functions
├── deployment/                    # Deployment scripts
│   └── deploy.py
├── eval/                          # Evaluation data/scripts
│   ├── data/*.test.json
│   └── test_eval.py
├── tests/                         # Unit tests
│   └── test_agents.py
├── .env.example                   # Environment template
├── pyproject.toml                 # Poetry dependencies
├── agent_pattern.png              # Architecture diagram
└── README.md                      # Agent-specific docs
```

### Agent Types and Complexity

| Type | Description | Example |
|------|-------------|---------|
| **Single Agent** | One agent handling all tasks | `personalized-shopping` |
| **Multi Agent** | Coordinated agents with specialized roles | `llm-auditor`, `data-science` |
| **Sequential Agent** | Agents executing in sequence | `google-trends-agent` |

| Complexity | Characteristics |
|-----------|-----------------|
| **Easy** | Basic tool usage, simple workflows |
| **Intermediate** | Multiple tools, moderate logic |
| **Advanced** | Complex orchestration, external systems |

## Key Technical Concepts

### Agent Components

1. **Agent Definition (`agent.py`):**
   - Defines model, tools, and instructions
   - Coordinates sub-agents (if multi-agent)
   - Manages agent behavior and flow

2. **Prompts (`prompt.py`):**
   - System instructions guiding agent behavior
   - Defines personality, capabilities, and constraints

3. **Tools (`tools/`):**
   - Custom functions the agent can call
   - Interface with external systems (APIs, databases)
   - Must be mocked for demonstration or implemented for production

4. **Sub-agents (`sub_agents/`):**
   - Specialized agents for specific tasks
   - Used in multi-agent architectures
   - Each has its own agent.py and prompt.py

### Environment Variables and Secret Management

**Local Development (.env files):**
Common variables across agents:
- `GOOGLE_GENAI_USE_VERTEXAI=1` - Use Vertex AI instead of Gemini API
- `GOOGLE_CLOUD_PROJECT` - Your GCP project ID
- `GOOGLE_CLOUD_LOCATION` - GCP region (e.g., `us-central1`)
- `GOOGLE_CLOUD_STORAGE_BUCKET` - For deployment artifacts

**Production Deployment (Secret Manager):**
For production agents, use Google Secret Manager:
```python
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """Retrieve secret from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

Some deployment scripts include `google-cloud-secret-manager` as a requirement for production use. Sample agents demonstrate `.env` patterns for ease of getting started, but production deployments should always use Secret Manager for sensitive credentials.

### Dependencies (pyproject.toml)

Standard dependencies:
```toml
[tool.poetry.dependencies]
python = "^3.10"
google-adk = "^1.0.0"
google-cloud-aiplatform = {extras = ["adk", "agent-engines"], version = "^1.93.0"}
google-genai = "^1.9.0"
pydantic = "^2.10.6"
python-dotenv = "^1.0.1"

[tool.poetry.group.dev.dependencies]
google-adk = {version = "^1.0.0", extras = ["eval"]}
pytest = "^8.3.5"
```

## Important Notes for Development

### Folder Naming Convention
- **Main directory:** Uses hyphens (e.g., `llm-auditor/`)
- **Code directory:** Uses underscores (e.g., `llm_auditor/`)
- This is enforced by Poetry's project structure

### Secret Management (CRITICAL FOR PRODUCTION)
- **Local Development Only:** Use `.env` files for local testing
- **Production/Live Repository:** **MUST use Google Secret Manager**
- **Never commit:**
  - `.env` files
  - API keys
  - Service account keys
  - Any credentials or secrets
- Ensure `.gitignore` includes `.env` files
- All deployment scripts must include `google-cloud-secret-manager` as a dependency
- Use workload identity or service accounts with minimal required permissions

### Tool Implementation (PRODUCTION CRITICAL)
**Warning:** Sample agents use **mocked tools** for demonstration only.

**For production agents, you MUST:**
1. **Replace all mock tools** with actual backend integrations in `tools/tools.py`
2. **Implement real API calls** with proper error handling, retries, and timeouts
3. **Add authentication** using Secret Manager for credentials
4. **Implement rate limiting** and backoff strategies
5. **Add comprehensive logging** for debugging and monitoring
6. **Test edge cases** including API failures, timeouts, and malformed responses
7. **Document dependencies** and external service requirements

### Running Agents
- **CLI mode:** Run `adk run .` from the `agent_name/` subdirectory
- **Web UI:** Run `adk web` from the `agent-name/` main directory
- Always check the agent's specific README for exact paths

### Testing Philosophy
- Agents with `[tool.agent-starter-pack]` in pyproject.toml are auto-tested
- Tests verify: linting, unit tests, backend startup
- CI uses Docker containers for consistency

### Deployment Targets
Agents can deploy to:
- **Agent Engine:** Vertex AI Agent Engine (managed service)
- **Cloud Run:** Serverless container platform
- Specified in `pyproject.toml` under `[tool.agent-starter-pack.settings]`

## Production Best Practices

**This repository is transitioning to production use. All development must follow these practices:**

### 1. Secret Management
```python
# PRODUCTION PATTERN - Use Secret Manager
from google.cloud import secretmanager

def get_secret(project_id: str, secret_id: str) -> str:
    """Retrieve secrets from Secret Manager in production."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Store secrets in Secret Manager:
# gcloud secrets create api-key --data-file=-
# gcloud secrets add-iam-policy-binding api-key \
#   --member="serviceAccount:SERVICE_ACCOUNT@PROJECT.iam.gserviceaccount.com" \
#   --role="roles/secretmanager.secretAccessor"
```

### 2. Security Requirements
- **Never commit secrets** - Use `.gitignore` for `.env`, `*.key`, `credentials.json`
- **Service Accounts:** Use workload identity or service accounts with least-privilege IAM roles
- **API Keys:** Restrict by IP, referrer, or API service
- **Authentication:** Implement proper authentication for all agent endpoints
- **Audit Logging:** Enable Cloud Audit Logs for all production agents

### 3. Code Quality Standards
```bash
# Run before every commit
make lint          # Must pass
make test          # Must pass
make type-check    # If available

# CI/CD will enforce these checks
```

### 4. Deployment Standards
- **Environment Separation:** Use separate GCP projects for dev/staging/production
- **Version Control:** Tag all production deployments with semantic versioning
- **Rollback Plan:** Always test rollback procedures before production deployment
- **Monitoring:** Set up Cloud Monitoring alerts for errors, latency, and cost
- **Rate Limiting:** Implement rate limiting on all production agents

### 5. Tool Implementation for Production
```python
# REPLACE mocked tools with actual implementations
# Example: Instead of mock responses, use real API calls

# BAD - Demo/Mock Pattern:
def search_database(query: str) -> dict:
    return {"results": ["mock_result_1", "mock_result_2"]}

# GOOD - Production Pattern:
def search_database(query: str) -> dict:
    """Production implementation with error handling."""
    api_key = get_secret(PROJECT_ID, "database-api-key")
    try:
        response = requests.post(
            DATABASE_API_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"query": query},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Database query failed: {e}")
        raise
```

### 6. Cost Management
- **Budget Alerts:** Set up billing alerts in Google Cloud Console
- **Quotas:** Configure API quotas to prevent runaway costs
- **Monitoring:** Track Vertex AI API usage and costs daily
- **Optimization:** Use appropriate model sizes (don't use Gemini Pro when Flash suffices)

### 7. Testing Requirements
- **Unit Tests:** All custom tools must have unit tests
- **Integration Tests:** Test agent flows end-to-end
- **Evaluation:** Run eval tests before production deployment
- **Load Testing:** Test agent performance under expected production load
- **Security Testing:** Scan for vulnerabilities using Cloud Security Scanner

### 8. Documentation Requirements
For each production agent:
- Architecture diagram showing data flow
- Security model documentation
- Runbook for common operations
- Incident response procedures
- Cost breakdown and optimization strategies

## Agent Categories and Use Cases

The repository includes agents across multiple verticals:

| Vertical | Agents | Key Features |
|----------|--------|--------------|
| **Retail** | customer-service, brand-search-optimization, personalized-shopping | E-commerce, inventory, recommendations |
| **Financial Services** | financial-advisor, fomc-research, auto-insurance-agent | Risk analysis, market research, claims |
| **Healthcare** | medical-pre-authorization | Document analysis, policy compliance |
| **Horizontal** | data-science, data-engineering, llm-auditor, software-bug-assistant | Cross-industry tools and workflows |
| **Academia** | academic-research | Publication discovery, research areas |
| **Media** | short-movie-agents | Video generation, content creation |

## Contributing

This project follows Google's contribution guidelines:

1. **CLA Required:** Sign the [Contributor License Agreement](https://cla.developers.google.com/)
2. **Code Review:** All submissions require GitHub PR review
3. **Community Guidelines:** Follow [Google's Open Source Community Guidelines](https://opensource.google/conduct/)

## Security Checklist for Production

Before deploying to production, verify:

```bash
# 1. Check .gitignore is comprehensive
cat .gitignore | grep -E '\.env|\.key|credentials|secret'

# 2. Scan for accidentally committed secrets
git log --all --full-history -- "**/*.env" "**/*.key" "**/*credentials*"

# 3. Verify no secrets in code
grep -r "api.*key\s*=\s*['\"]" python/agents/ --include="*.py"
grep -r "password\s*=\s*['\"]" python/agents/ --include="*.py"

# 4. Check Secret Manager setup
gcloud secrets list --project=YOUR_PROJECT_ID

# 5. Verify service account permissions (least privilege)
gcloud projects get-iam-policy YOUR_PROJECT_ID

# 6. Enable audit logging
gcloud logging read "protoPayload.serviceName=secretmanager.googleapis.com" --limit 10
```

**Additional .gitignore entries for production:**
```
# Service Account Keys
*.json
!package.json
!package-lock.json
!tsconfig.json
credentials.json
service-account*.json
*-key.json

# Secret files
secrets/
.secrets/
*.pem
*.key
*.cert

# Terraform sensitive files
terraform.tfvars
*.tfvars.json

# Cloud credentials
.google-credentials
google-credentials.json
```

## Additional Resources

- **ADK Documentation:** https://google.github.io/adk-docs/
- **ADK Python:** https://github.com/google/adk-python
- **ADK Java:** https://github.com/google/adk-java
- **GitHub Issues:** https://github.com/google/adk-samples/issues
- **GCP Secret Manager:** https://cloud.google.com/secret-manager/docs
- **GCP Security Best Practices:** https://cloud.google.com/security/best-practices

## Repository Status

**Live/Production Repository:** This repository is being used for production agents. All contributors must follow production best practices including:
- Secret Manager for all credentials
- Comprehensive testing before deployment
- Security scanning and vulnerability management
- Proper monitoring and alerting
- Documentation for all production agents
