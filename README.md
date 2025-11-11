# 🤖 Bob's Brain

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-green.svg)](https://github.com/jeremylongshore/bobs-brain/releases)
[![Template](https://img.shields.io/badge/template-ready-brightgreen.svg)](https://github.com/jeremylongshore/bobs-brain/generate)

**Production-ready template for building intelligent Slack AI agents with Google ADK, Vertex AI, and modern LLM frameworks.**

[Quick Start](#-quick-start) • [Architecture](#-architecture) • [Documentation](000-docs/) • [Examples](#-features) • [Contributing](#-contributing)

</div>

---

## 🎯 What is Bob's Brain?

Bob's Brain is a **battle-tested, production-grade template** for building AI agents that work in Slack. Born from real-world deployments, it gives you everything you need to create intelligent assistants that your team will actually use.

### Why This Template?

✅ **Actually Works in Production** - Not just a demo, this has handled real Slack conversations
✅ **Multiple Implementation Paths** - ADK, Vertex AI Agent Engine, or custom Flask
✅ **Knowledge Base Ready** - Semantic search, RAG, and conversation memory built-in
✅ **Cloud Native** - Terraform IaC, Cloud Run deployment, GitHub Actions CI/CD
✅ **Learn by Example** - 4 complete implementations archived for reference

### Perfect For

- 🏢 **Teams** building internal Slack assistants
- 🎓 **Learners** studying AI agent architectures
- 🚀 **Builders** who want production-ready starting points
- 🔬 **Researchers** exploring multi-agent patterns

---

## 🏗️ Architecture

Bob's Brain uses a **clean, flat scaffold** designed for clarity and extensibility:

```
bobs-brain/
├── adk/               # Google ADK agent definitions & tools
├── my_agent/          # Core agent logic and conversation handlers
├── service/           # API services, webhooks, runtime
├── infra/             # Terraform IaC for GCP deployment
├── scripts/           # Deployment automation and helpers
├── tests/             # Comprehensive test suite
├── 000-docs/          # Architecture docs, AARs, runbooks
└── 99-Archive/        # Reference implementations (Flask, Genkit, etc.)
```

### What Goes Where?

| Directory | Purpose | Examples |
|-----------|---------|----------|
| **adk/** | ADK agent configs, tool definitions | `agent.yaml`, custom tools |
| **my_agent/** | Business logic, conversation flow | Message handlers, decision logic |
| **service/** | HTTP endpoints, Slack webhooks | FastAPI/Flask services, event handlers |
| **infra/** | Infrastructure as Code | `main.tf`, GCP resources, environments |
| **scripts/** | Automation, deployment | `deploy.sh`, `setup-env.sh` |
| **tests/** | All test code | Unit, integration, e2e tests |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Google Cloud account (for deployment)
- Slack workspace with admin access

### 1. Clone & Setup

```bash
# Use this template
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment
cp .env.example .env

# Edit .env with your credentials
# - SLACK_BOT_TOKEN
# - SLACK_SIGNING_SECRET
# - GOOGLE_PROJECT_ID
# - GOOGLE_APPLICATION_CREDENTIALS
```

### 3. Choose Your Path

#### **Option A: Google ADK (Recommended)**

Build agents using Google's official Agent Development Kit:

```bash
# Set up ADK agent
cd adk/
# Add your agent configuration
# Deploy to Vertex AI Agent Engine
```

#### **Option B: Custom Service**

Build your own service layer:

```bash
# Develop your service
cd service/
# Run locally
python app.py
```

#### **Option C: Learn from Archives**

Study complete implementations:

```bash
# Explore archived implementations
cd 99-Archive/2025-11-11-final-cleanup/
# - 2025-11-10-adk-agent/        (ADK implementation)
# - 2025-11-10-bob-vertex-agent/ (Vertex AI)
# - 2025-11-10-genkit-agent/     (Genkit framework)
# - 2025-11-11/                  (Flask modular v5)
```

### 4. Deploy to Production

```bash
# Deploy with Terraform
cd infra/
terraform init
terraform plan
terraform apply

# Or use deployment scripts
./scripts/deploy.sh production
```

---

## ✨ Features

### 🧠 **Knowledge Base Integration**

- **Vector Search** - Semantic search over documentation
- **RAG (Retrieval-Augmented Generation)** - Context-aware responses
- **Conversation Memory** - Multi-turn dialogue with context

### 💬 **Slack Integration**

- **Event Handling** - Respond to mentions, DMs, reactions
- **Rich Messages** - Blocks, attachments, interactive components
- **Thread Support** - Maintain conversation context in threads

### ☁️ **Cloud Native**

- **Google Cloud** - Cloud Run, Vertex AI, Secret Manager
- **Infrastructure as Code** - Terraform modules included
- **CI/CD** - GitHub Actions workflows for testing & deployment

### 🔧 **Developer Experience**

- **Multiple LLM Providers** - Claude, Gemini, GPT-4, Groq
- **Local Development** - Test without deploying
- **Comprehensive Tests** - Unit, integration, e2e coverage
- **Observability** - Structured logging, error tracking

---

## 📚 Documentation

### Essential Reading

- **[000-docs/](000-docs/)** - Primary documentation directory
  - Architecture decision records
  - After-action reports (AARs)
  - Operational runbooks
  - Deployment guides

### Key Documents

| Document | Description |
|----------|-------------|
| [001-AA-REPT-night-wrap-2025-11-11.md](000-docs/001-AA-REPT-night-wrap-2025-11-11.md) | Repository restructuring AAR |
| [050-AA-REPT-final-cleanup.md](000-docs/050-AA-REPT-final-cleanup.md) | Canonical structure enforcement |

### Learning Path

1. **Start Here** - Read this README
2. **Understand Structure** - Review [000-docs/](000-docs/)
3. **Pick Implementation** - Choose ADK, Vertex, or Custom
4. **Study Archives** - Learn from complete implementations in [99-Archive/](99-Archive/)
5. **Build Your Agent** - Customize and deploy

---

## 🛠️ Development

### Available Commands

```bash
# Run tests
make test

# Format code
make fmt

# Type checking
make type-check

# Security scan
make security-check

# Run all checks before commit
make check-all

# Deploy to Cloud Run
make deploy
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=my_agent --cov-report=html

# Run integration tests
pytest tests/integration/ -v
```

### Local Development

```bash
# Start development server
python service/app.py

# With hot reload
uvicorn service.app:app --reload

# Test Slack webhook locally (requires ngrok)
ngrok http 8000
# Update Slack webhook URL to ngrok URL
```

---

## 🗂️ Archive: Reference Implementations

The `99-Archive/` directory contains **4 complete, production-tested implementations** preserved for learning:

### 1. **Flask Modular Agent (v5)** - `2025-11-11/`
- Modular Flask architecture
- Multi-provider LLM support (Claude, Gemini, GPT-4, Groq, Ollama)
- Circle-of-Life learning system
- LlamaIndex knowledge integration

### 2. **Vertex AI Agent Engine** - `2025-11-10-bob-vertex-agent/`
- Google Cloud managed agent
- Vertex AI Gemini integration
- Cloud Functions webhooks
- Production deployment ready

### 3. **ADK Implementation** - `2025-11-10-adk-agent/`
- Google Agent Development Kit
- Agent Starter Pack patterns
- Tool definitions and schemas
- A2A (Agent-to-Agent) protocol

### 4. **Genkit Framework** - `2025-11-10-genkit-agent/`
- Full-stack AI framework
- TypeScript/JavaScript implementation
- Firebase integration
- Prompt engineering patterns

**Why Keep Archives?**

Each implementation teaches different patterns:
- **Flask**: Traditional web framework approach
- **Vertex AI**: Fully managed Google Cloud solution
- **ADK**: Official Google agent framework
- **Genkit**: Modern full-stack AI development

Study them, learn from them, and choose your path.

---

## 🤝 Contributing

### This is a Template Repository

Bob's Brain is designed to be **forked and customized**. Here's how to make it yours:

1. **Fork or Use Template** - Click "Use this template" on GitHub
2. **Customize** - Adapt to your use case
3. **Deploy** - Ship your agent to production
4. **Share Back** - Submit PRs if you add reusable features

### Contribution Guidelines

- Follow the canonical structure
- Document in `000-docs/` using the [Document Filing System v2.0](000-docs/README.md)
- Add tests for new features
- Update README if you change architecture

---

## 🏷️ Versioning & Releases

We follow [Semantic Versioning](https://semver.org/):

- **v0.4.0** (Current) - Canonical scaffold structure
- **v0.5.1** - Night Wrap repository cleanup
- **v1.0.0** - Flask v5 modular agent
- **v5.0.0** - Sovereign modular agent
- **v6.1.0** - Latest archived implementation

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

**TL;DR**: Fork it, customize it, deploy it, sell it. Just keep the license notice.

---

## 🌟 Related Projects

- [Google ADK](https://github.com/google/adk-python) - Official Google Agent Development Kit
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine) - Managed agent platform
- [Genkit](https://firebase.google.com/docs/genkit) - Full-stack AI framework
- [LangChain](https://www.langchain.com/) - LLM application framework

---

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/jeremylongshore/bobs-brain/issues)
- **Discussions**: [GitHub Discussions](https://github.com/jeremylongshore/bobs-brain/discussions)
- **Documentation**: [000-docs/](000-docs/)

---

## 🎓 Learning Resources

### Architecture Patterns

- **Multi-Agent Systems** - See ADK implementation
- **RAG (Retrieval-Augmented Generation)** - Study knowledge base integration
- **Event-Driven Design** - Review Slack webhook handlers
- **Infrastructure as Code** - Explore Terraform modules

### Best Practices

- **Document Everything** - See our [000-docs/](000-docs/) structure
- **Test Comprehensively** - Review [tests/](tests/) directory
- **Archive Thoughtfully** - Learn from [99-Archive/](99-Archive/)
- **Version Rigorously** - Check [CHANGELOG.md](CHANGELOG.md)

---

<div align="center">

**Built with ❤️ for the AI agent community**

[⭐ Star this repo](https://github.com/jeremylongshore/bobs-brain) • [🍴 Fork it](https://github.com/jeremylongshore/bobs-brain/fork) • [📖 Read the docs](000-docs/)

---

**Version 0.4.0** • Last Updated: 2025-11-11 • [Release Notes](https://github.com/jeremylongshore/bobs-brain/releases/tag/v0.4.0)

</div>
