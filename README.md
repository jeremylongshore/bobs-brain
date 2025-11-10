<div align="center">

# Bob's Brain - Vertex AI Agent Engine

### Production-Ready AI Assistant with Google ADK + Slack Integration

[![Version](https://img.shields.io/badge/version-0.4.0-green.svg)](https://github.com/jeremylongshore/bobs-brain/releases)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-orange.svg)](https://cloud.google.com/vertex-ai)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**Production AI agent powered by Google Vertex AI Agent Engine with Slack integration and 5GB knowledge base**

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Slack Integration](#-slack-integration)

---

**Last Updated:** 2025-11-10

</div>

## 🎯 What is Bob's Brain?

Bob's Brain is a **production-ready AI assistant** deployed on **Google Cloud Platform** using:

- **Vertex AI Agent Engine** - Fully managed agent runtime with auto-scaling, observability, and enterprise features
- **Google ADK (Agent Development Kit)** - Framework for building production AI agents with tool calling and memory
- **Gemini 2.5 Flash** - High-performance LLM for intelligent responses
- **Vertex AI Search** - RAG-powered knowledge retrieval from 5GB knowledge base (303 files)
- **Memory Bank** - Long-term memory with governance, TTL, and audit trails
- **Slack Integration** - Cloud Functions Gen2 webhook for team collaboration

---

## ✨ Features

### Core Capabilities

- **Intelligent Conversation** - Natural language understanding with context awareness
- **Knowledge Retrieval (RAG)** - Semantic search across 5GB knowledge base via Vertex AI Search
- **Long-Term Memory** - Vertex AI Memory Bank with topic-based filtering and governance
- **Slack Integration** - Real-time responses in Slack channels and DMs
- **Auto-Scaling** - Vertex AI Agent Engine scales from 1-10 instances automatically
- **Observability** - Full telemetry with Cloud Logging, Trace, and monitoring
- **Session Management** - Per-user-per-channel conversation context
- **Tool Calling** - Extensible tools for web search, calculations, and more

### Advanced Features (Vertex AI Agent Engine)

- **Managed Runtime** - No infrastructure management required
- **Memory Bank Governance**:
  - Granular TTL (30/90/365 days)
  - Topic-based filtering (USER_PERSONAL_INFO, USER_PREFERENCES, etc.)
  - Revision history and audit trails
  - Memory rollback for compliance
  - GDPR right to erasure and access
- **Agent-to-Agent (A2A) Protocol** - Coordinate with peer agents
- **Enterprise Security** - VPC controls, IAM policies, API key authentication

---

## 🚀 Quick Start

### Prerequisites

- Google Cloud Project with billing enabled
- Python 3.12+
- `uv` package manager (recommended) or `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain/bob-vertex-agent

# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -r requirements.txt
```

### Deploy to Vertex AI Agent Engine

```bash
# Set your GCP project
export PROJECT_ID=your-gcp-project

# Deploy agent to Agent Engine
make deploy

# ✅ Your agent is now live!
# Access the playground: https://console.cloud.google.com/vertex-ai/agents
```

### Deploy Slack Webhook (Optional)

```bash
# Deploy Cloud Function Gen2 webhook
cd slack-webhook
gcloud functions deploy slack-webhook \
  --gen2 \
  --runtime=python312 \
  --region=us-central1 \
  --source=. \
  --entry-point=slack_events \
  --trigger-http \
  --allow-unauthenticated \
  --project=$PROJECT_ID \
  --set-env-vars=PROJECT_ID=$PROJECT_ID

# Configure Slack Events API with the webhook URL
```

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Slack (User Mentions @Bob)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │ POST /slack/events
                       ▼
┌─────────────────────────────────────────────────────────────┐
│         Cloud Functions Gen2 (Slack Webhook)                 │
│  • Immediate HTTP 200 acknowledgment (no duplicates)         │
│  • Signature verification                                    │
│  • Event parsing                                             │
└──────────────────────┬──────────────────────────────────────┘
                       │ REST API Call
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        Vertex AI Agent Engine (Bob's Brain)                  │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Agent Engine App (ADK)                             │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • Query Understanding & Routing                    │    │
│  │ • Tool Calling (Web Search, Calculations, etc.)    │    │
│  │ • Session Management (per-user-per-channel)        │    │
│  └────────────────────────────────────────────────────┘    │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Vertex AI Search (RAG)                             │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • 5GB Knowledge Base (303 files)                   │    │
│  │ • Semantic Search                                   │    │
│  │ • Re-ranking with Vertex AI Rank                   │    │
│  │ • Citation Support                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Memory Bank (Long-Term Memory)                     │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • Granular TTL (30/90/365 days)                    │    │
│  │ • Topic-Based Filtering                            │    │
│  │ • Revision History & Audit Trails                  │    │
│  │ • Memory Rollback for Compliance                   │    │
│  └────────────────────────────────────────────────────┘    │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Gemini 2.5 Flash (LLM)                             │    │
│  ├────────────────────────────────────────────────────┤    │
│  │ • High-Performance Inference                       │    │
│  │ • Context-Aware Responses                          │    │
│  │ • Streaming Output                                  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  • Auto-Scaling: 1-10 instances                             │
│  • Observability: Cloud Logging + Trace                     │
│  • Session Service: Conversation context per user/channel   │
└─────────────────────────────────────────────────────────────┘
                       │ Response
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Slack (Bot Posts Response)                      │
└─────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Agent Runtime** | Vertex AI Agent Engine | Managed agent hosting with auto-scaling |
| **Agent Framework** | Google ADK (Agent Development Kit) | Production agent framework |
| **LLM** | Gemini 2.5 Flash | High-performance language model |
| **Knowledge** | Vertex AI Search | RAG-powered semantic search (5GB, 303 files) |
| **Memory** | Memory Bank | Long-term memory with governance |
| **Slack Integration** | Cloud Functions Gen2 | Serverless webhook handler |
| **Language** | Python 3.12+ | Agent implementation |
| **Package Manager** | uv | Fast, reliable dependency management |

---

## 💬 Slack Integration

### Features

- **Real-Time Responses** - Instant replies to @mentions and DMs
- **Conversation Memory** - Last 10 messages per user stored in session
- **Knowledge Grounding** - RAG-powered context from 5GB knowledge base
- **Duplicate Prevention** - Immediate HTTP 200 acknowledgment (fixed Oct 2025)
- **Signature Verification** - Secure webhook validation
- **Error Handling** - Graceful fallbacks and retry logic

### Setup

1. **Create Slack App** at https://api.slack.com/apps
2. **Enable Events** and subscribe to:
   - `message.channels`
   - `message.im`
   - `app_mention`
3. **Deploy Cloud Function** (see Quick Start above)
4. **Configure Event URL** with your Cloud Function URL
5. **Install App** to workspace and invite @Bob to channels

### Architecture

```
User Message → Slack Events API → Cloud Function → Agent Engine → Gemini → Response
                                        ↓                 ↓
                                  Signature           Vertex AI
                                  Verification        Search (RAG)
                                                          ↓
                                                     Memory Bank
```

---

## 📊 Knowledge Base

Bob's Brain includes a **5GB knowledge base** with **303 files** across multiple domains:

### Top Knowledge Domains

| Domain | Size | Files | Topics |
|--------|------|-------|--------|
| **Intent Solutions Landing** | 1008K | 50+ | AI DevOps, SaaS, landing pages |
| **N8N Workflows** | 864K | 80+ | Automation, workflows, integrations |
| **Diagnostic Platform** | 448K | 40+ | BigQuery, data pipelines, analytics |
| **Hybrid AI Stack** | 412K | 30+ | Multi-cloud AI, cost optimization |
| **IAMS** | 256K | 20+ | Agent systems, A2A protocol |
| **Google Vertex AI** | 50K+ | 5+ | Memory Bank, Agent Engine, ADK |

### Recent Additions (2025-11-10)

- ✅ **Memory Bank Governance Guide** - Comprehensive tutorial on TTL, topic filtering, revision history, rollback, and GDPR compliance

---

## 🛠️ Development

### Local Testing

```bash
# Test agent locally
cd bob-vertex-agent
uv run python test_agent_direct.py

# Test REST API
uv run python test_agent_api.py

# Test with custom query
uv run -m app.agent_engine_app --query "What is Vertex AI Memory Bank?"
```

### Common Commands

```bash
# Deploy agent to Agent Engine
make deploy

# Check deployment status
make status

# View logs
make logs

# Clean up
make clean
```

### Configuration

Key environment variables (set in Cloud Functions or locally):

```bash
PROJECT_ID=bobs-brain                # GCP project ID
AGENT_ENGINE_ID=5828234061910376448  # Agent Engine instance ID
SLACK_BOT_TOKEN=xoxb-...             # Slack bot token (for webhook)
SLACK_SIGNING_SECRET=...             # Slack signing secret (for webhook)
```

---

## 🔐 Security

- ✅ **VPC Controls** - Private endpoints for Agent Engine
- ✅ **IAM Policies** - Service account with least privilege
- ✅ **API Key Auth** - Secure agent queries
- ✅ **Slack Signature Verification** - Webhook validation
- ✅ **Data Encryption** - At-rest and in-transit (Google Cloud managed)
- ✅ **Audit Logging** - Full telemetry and trace data
- ✅ **Memory Bank Governance** - Data retention, TTL, and compliance features

---

## 📈 Performance & Scale

- **Response Time**: < 3 seconds typical queries
- **Concurrent Users**: 1-10 instances (auto-scaling)
- **Knowledge Base**: 5GB, 303 files via Vertex AI Search
- **Memory Capacity**: Unlimited with Memory Bank TTL governance
- **Uptime**: 99.9% on Google Cloud infrastructure

---

## 🚀 Production Features

### Vertex AI Agent Engine Benefits

1. **Managed Runtime** - No servers to manage, automatic scaling
2. **Enterprise Observability** - Cloud Logging, Trace, and monitoring
3. **Memory Bank** - Long-term memory with governance:
   - Granular TTL (30/90/365 days)
   - Topic-based filtering
   - Revision history and audit trails
   - Memory rollback for compliance
4. **Session Service** - Conversation context per user/channel
5. **Agent-to-Agent (A2A) Protocol** - Multi-agent coordination
6. **Security** - VPC controls, IAM policies, encryption

### CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy-bob-complete.yml
- Security scanning (Bandit, TruffleHog)
- Agent Engine deployment
- Slack webhook deployment
- Integration tests
- CHANGELOG updates
```

**WIF (Workload Identity Federation)** - Keyless authentication from GitHub Actions to GCP

---

## 📖 Documentation

### Key Files

- **`bob-vertex-agent/CLAUDE.md`** - Complete developer guide
- **`bob-vertex-agent/CHANGELOG.md`** - Version history
- **`bob-vertex-agent/DEPLOYMENT_GUIDE.md`** - Deployment instructions
- **`knowledge-base/google-vertex-ai/tutorials/memory-bank-governance-guide.md`** - Memory Bank reference

### External Resources

- [Vertex AI Agent Engine Docs](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview)
- [Google ADK GitHub](https://github.com/google/adk-python)
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
- [Memory Bank Tutorial](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank)

---

## 🎯 Use Cases

### Individual Use

- **Personal AI Assistant** - Answer questions, research, summarization
- **Knowledge Management** - Query your personal knowledge base
- **Learning Companion** - Explain concepts, provide examples

### Team Use

- **Slack Bot** - Team Q&A, documentation search, onboarding
- **Knowledge Hub** - Centralized team knowledge with RAG
- **Workflow Automation** - Integrate with tools, APIs, databases

### Enterprise Use

- **Customer Support** - AI-powered support agent with knowledge base
- **Internal IT Support** - Answer employee questions, troubleshooting
- **Sales Enablement** - Product knowledge, competitive intelligence

---

## 🔧 Technology Stack

<div align="center">

| Component | Technology | Version |
|-----------|-----------|---------|
| **AI Platform** | Vertex AI Agent Engine | Latest |
| **Agent Framework** | Google ADK | Latest |
| **LLM** | Gemini 2.5 Flash | Latest |
| **Knowledge** | Vertex AI Search | Latest |
| **Memory** | Memory Bank | Latest |
| **Slack Integration** | Cloud Functions Gen2 | Latest |
| **Language** | Python | 3.12+ |
| **Package Manager** | uv | Latest |
| **Infrastructure** | Terraform | Latest (optional) |

</div>

---

## 🐛 Troubleshooting

### Agent Not Responding

1. Check Agent Engine status:
   ```bash
   gcloud ai reasoning-engines describe 5828234061910376448 \
     --project=bobs-brain \
     --region=us-central1
   ```

2. View logs:
   ```bash
   make logs
   # Or: gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" --limit=20
   ```

### Slack Duplicate Responses

If seeing duplicate responses, ensure Cloud Function has immediate HTTP 200 acknowledgment enabled (fixed Oct 2025).

### Knowledge Base Not Working

1. Verify Vertex AI Search datastore is configured
2. Check knowledge base ingestion status
3. Test direct Vertex AI Search query

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:

- [Google ADK](https://github.com/google/adk-python) - Agent Development Kit
- [Vertex AI](https://cloud.google.com/vertex-ai) - Google Cloud AI Platform
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) - Inspiration

---

## 📞 Get in Touch

- **GitHub Issues**: [Report bugs or request features](https://github.com/jeremylongshore/bobs-brain/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/jeremylongshore/bobs-brain/discussions)

---

<div align="center">

**Made with ❤️ using Google Cloud + ADK + Gemini**

⭐ **Star this repo** if you find it useful!

**Last Updated:** 2025-11-10

</div>
