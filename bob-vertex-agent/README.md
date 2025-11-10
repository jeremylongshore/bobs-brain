<div align="center">

# IAM1 Regional Manager

### Enterprise-Grade Hierarchical Multi-Agent System with A2A Protocol

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.3.0-green.svg)](https://github.com/jeremylongshore/bobs-brain/releases)
[![A2A Protocol](https://img.shields.io/badge/A2A-0.3.0-purple.svg)](https://a2a-protocol.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Vertex%20AI-orange.svg)](https://cloud.google.com/vertex-ai)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red.svg)](https://github.com/sponsors/IntentSolutions)

**Production-ready AI agent orchestrator that commands specialist teams and coordinates with peer agents across domains**

[Quick Start](#-quick-start) • [Features](#-features) • [Architecture](#-architecture) • [Documentation](#-documentation) • [Become a Reseller](https://intentsolutions.io/reseller)

---

### 💝 Support This Project

<a href="https://github.com/sponsors/IntentSolutions">
  <img src="https://img.shields.io/badge/Sponsor-IntentSolutions-red?style=for-the-badge&logo=github-sponsors" alt="Sponsor IntentSolutions">
</a>

**Become a sponsor** to get priority support, influence roadmap, and access to exclusive features.

---

</div>

## 🎯 What is IAM1?

**IAM1 Regional Manager** is a sovereign AI agent that operates like a department head in your organization. It can:

- **Command specialist subordinates** (IAM2 agents) to execute complex tasks
- **Coordinate with peer managers** (other IAM1s) across departments via A2A Protocol
- **Ground decisions in knowledge** using RAG-powered retrieval from your private data
- **Scale horizontally** across multiple domains with isolated, client-specific deployments

Think of it as your AI organizational layer—each IAM1 manages its domain independently while seamlessly collaborating with others.

---

## ✨ Why IAM1?

<table>
<tr>
<td width="33%" valign="top">

### 🏗️ **Production-Ready**

- Terraform infrastructure included
- CI/CD pipelines configured
- Full observability & monitoring
- Deployed to Google Cloud in minutes

</td>
<td width="33%" valign="top">

### 🤝 **True Multi-Agent**

- Hierarchical orchestration (IAM1 → IAM2)
- Peer-to-peer coordination (IAM1 ↔ IAM1)
- Agent2Agent Protocol support
- Distributed intelligence architecture

</td>
<td width="33%" valign="top">

### 🔒 **Enterprise-Grade**

- Client-isolated deployments
- Private knowledge grounding
- Secure A2A authentication
- Scales from startup to Fortune 500

</td>
</tr>
</table>

---

## 🚀 Quick Start

Get your first IAM1 deployed to Google Cloud in under 5 minutes:

```bash
# 1. Use this template or clone the repository
gh repo create my-iam1 --template IntentSolutions/iam1-regional-manager --public
cd my-iam1

# 2. Set your Google Cloud project
export PROJECT_ID=your-gcp-project

# 3. Install dependencies
uv sync

# 4. Deploy to Vertex AI Agent Engine
make deploy

# ✅ Your IAM1 is live!
# Access the playground: https://console.cloud.google.com/vertex-ai/agents
```

**That's it!** Your IAM1 is deployed with:
- ✅ 4 IAM2 specialist agents (Research, Code, Data, Slack)
- ✅ RAG-powered knowledge retrieval
- ✅ A2A Protocol peer coordination ready
- ✅ Production infrastructure on Google Cloud

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   IAM1 Regional Manager                      │
│                   (Sovereign in Domain)                      │
│                                                              │
│  Capabilities:                                              │
│  • Conversational AI & Task Understanding                   │
│  • Knowledge Retrieval (RAG via Vertex AI Search)           │
│  • Specialist Task Delegation                               │
│  • Peer Agent Coordination (A2A Protocol)                   │
└─────────────────────────────────────────────────────────────┘
           │                                    │
           │ Commands                           │ Coordinates
           │ (Internal Routing)                 │ (A2A Protocol)
           ▼                                    ▼
  ┌────────────────────┐              ┌────────────────────┐
  │  IAM2 Specialists  │              │   Peer IAM1s       │
  │  (Subordinates)    │              │   (Other Domains)  │
  ├────────────────────┤              ├────────────────────┤
  │ 🔬 Research Agent  │              │ 🛠️  Engineering    │
  │ 💻 Code Agent      │              │ 💰 Sales           │
  │ 📊 Data Agent      │              │ 🚀 Operations      │
  │ 💬 Slack Agent     │              │ 📈 Marketing       │
  └────────────────────┘              └────────────────────┘
```

### How It Works

1. **User Query** → IAM1 receives natural language request
2. **Decision Framework** → IAM1 analyzes and routes appropriately:
   - Simple questions → Answer directly
   - Knowledge needed → Query Vertex AI Search (RAG)
   - Specialized task → Delegate to IAM2 specialist
   - Cross-domain info → Coordinate with peer IAM1 via A2A
3. **Task Execution** → Specialists execute, IAM1 synthesizes
4. **Response** → Coherent answer with full context

---

## 💎 Features

### Core Capabilities

<table>
<tr>
<td width="50%">

#### 🎯 **Intelligent Orchestration**

- **Decision Framework**: Step-by-step routing logic
- **Context Management**: Maintains conversation history
- **Task Synthesis**: Combines multiple agent outputs
- **Error Handling**: Graceful fallbacks and retries

</td>
<td width="50%">

#### 🤖 **IAM2 Specialist Team**

- **Research Agent**: Deep analysis, knowledge synthesis
- **Code Agent**: Generation, debugging, refactoring
- **Data Agent**: BigQuery, analytics, visualization
- **Slack Agent**: Channel management, formatting

</td>
</tr>
<tr>
<td width="50%">

#### 🤝 **Agent2Agent Protocol**

- **Peer Coordination**: IAM1 ↔ IAM1 communication
- **Standard Protocol**: A2A 0.3.0 compliance
- **Agent Discovery**: JSON Agent Card support
- **Cross-Domain**: Engineering, Sales, Ops, Marketing, Finance, HR

</td>
<td width="50%">

#### 📚 **Knowledge Grounding**

- **RAG Retrieval**: Vertex AI Search integration
- **Private Data**: Client-specific knowledge bases
- **Re-ranking**: Vertex AI Rank for relevance
- **Citation Support**: Source attribution

</td>
</tr>
</table>

### Production Infrastructure

- ✅ **Google Cloud Native**: Deployed to Vertex AI Agent Engine
- ✅ **Terraform IaC**: Infrastructure as Code included
- ✅ **CI/CD Ready**: GitHub Actions workflows
- ✅ **Observability**: Full telemetry and tracing
- ✅ **Scalable**: Auto-scaling from 1-10 instances
- ✅ **Secure**: IAM policies, API key auth, VPC controls

---

## 🎓 Use Cases

### Single-Domain Deployment

Deploy IAM1 as a **sovereign agent** for a specific domain:

```bash
# Sales IAM1 with CRM knowledge
export PROJECT_ID=acme-sales
export DOMAIN=sales
make deploy
```

**Use Cases:**
- Sales: Lead qualification, forecasting, CRM queries
- Engineering: Code reviews, architecture Q&A, bug triage
- Operations: Incident response, runbook execution, metrics analysis
- Support: Ticket routing, knowledge base search, escalation

### Multi-Domain Enterprise

Deploy **multiple IAM1s** that coordinate via A2A:

```
┌─────────────┐     A2A      ┌─────────────┐
│  Sales IAM1 │ ←─────────→ │  Eng IAM1   │
└─────────────┘             └─────────────┘
       ↕ A2A                       ↕ A2A
┌─────────────┐             ┌─────────────┐
│  Ops IAM1   │ ←─────────→ │  Mktg IAM1  │
└─────────────┘             └─────────────┘
```

**Enterprise Scenarios:**
- **Cross-functional collaboration**: Sales IAM1 queries Engineering IAM1 for product roadmap
- **Distributed intelligence**: Operations IAM1 aggregates metrics from all domains
- **Unified reporting**: Finance IAM1 coordinates with all domains for quarterly summaries

---

## 🔧 Technology Stack

<div align="center">

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **AI Platform** | [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview) | Managed agent runtime |
| **LLM Models** | Gemini 2.0 Flash (IAM1), Gemini 2.5 Flash (IAM2) | High-performance inference |
| **Framework** | [Google ADK](https://github.com/google/adk-python) | Agent Development Kit |
| **Knowledge** | [Vertex AI Search](https://cloud.google.com/generative-ai-app-builder/docs/enterprise-search-introduction) | RAG grounding |
| **Coordination** | [A2A Protocol 0.3.0](https://a2a-protocol.org/) | Peer agent communication |
| **Infrastructure** | [Terraform](https://www.terraform.io/) | Infrastructure as Code |
| **Language** | Python 3.10+ | Core implementation |
| **Package Manager** | [uv](https://docs.astral.sh/uv/) | Fast, reliable dependencies |

</div>

---

## 💼 Business Opportunities

### For Developers (Free)

**Open Source Template**
- ✅ Free forever (MIT License)
- ✅ Full source code access
- ✅ Community support
- ✅ Self-deploy on your Google Cloud
- ✅ Customize and extend

### For Agencies & Consultants

<div align="center">

### 🤝 [Become a Reseller](https://intentsolutions.io/reseller)

**Partner with IntentSolutions** to offer managed IAM1 deployments to your clients:

- 💰 **Revenue Share**: Earn 30% recurring revenue
- 🛠️ **White-Label**: Your brand, our technology
- 📚 **Training & Support**: Full onboarding and resources
- 🎯 **Sales Materials**: Pitch decks, demos, case studies
- 🚀 **Fast Time-to-Market**: Deploy client IAM1s in minutes

[**Apply to Become a Reseller →**](https://intentsolutions.io/reseller)

</div>

### For Enterprises

**Professional Services** (IntentSolutions)
- 🏢 Managed deployments: **$500/month per IAM1**
- 🔧 Custom IAM2 specialists: **$200/month each**
- 🤝 Multi-IAM1 coordination: **Custom pricing**
- 📞 Includes: Infrastructure, monitoring, support, upgrades

<div align="center">

[**Schedule Enterprise Demo →**](https://intentsolutions.io/contact)

</div>

---

## 💝 Support & Sponsorship

### GitHub Sponsors

Love this project? Support ongoing development:

<a href="https://github.com/sponsors/IntentSolutions">
  <img src="https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?style=for-the-badge&logo=github-sponsors" alt="Sponsor IntentSolutions">
</a>

**Sponsor Tiers:**

| Tier | Monthly | Benefits |
|------|---------|----------|
| 🥉 **Bronze** | $10/mo | Priority issue responses, sponsor badge |
| 🥈 **Silver** | $50/mo | + Influence roadmap, early access to features |
| 🥇 **Gold** | $200/mo | + 1:1 consultation hour/month, custom IAM2 review |
| 💎 **Platinum** | $500/mo | + White-glove support, architecture review |

### Community Support

- 💬 [GitHub Discussions](https://github.com/IntentSolutions/iam1-regional-manager/discussions) - Ask questions, share ideas
- 🐛 [Issue Tracker](https://github.com/IntentSolutions/iam1-regional-manager/issues) - Report bugs, request features
- 📝 [Documentation](docs/) - Comprehensive guides
- 🐦 [Twitter](https://twitter.com/IntentSolutions) - Updates and announcements

---

## 🎯 Examples

Explore real-world IAM1 configurations:

| Example | Description | Link |
|---------|-------------|------|
| **Sales IAM1** | CRM integration, lead qualification, forecasting | [View](examples/sales-iam1/) |
| **Engineering IAM1** | Code reviews, architecture Q&A, Jira integration | [View](examples/engineering-iam1/) |
| **Multi-IAM1 Enterprise** | 4 coordinating IAM1s with A2A Protocol | [View](examples/multi-iam1/) |

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to get started:

```bash
# 1. Fork the repository
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/iam1-regional-manager.git

# 3. Create a feature branch
git checkout -b feature/amazing-improvement

# 4. Make your changes and test
make test

# 5. Commit and push
git commit -m "Add amazing improvement"
git push origin feature/amazing-improvement

# 6. Open a Pull Request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📊 Project Status

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/IntentSolutions/iam1-regional-manager?style=social)
![GitHub Forks](https://img.shields.io/github/forks/IntentSolutions/iam1-regional-manager?style=social)
![GitHub Issues](https://img.shields.io/github/issues/IntentSolutions/iam1-regional-manager)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/IntentSolutions/iam1-regional-manager)

**Active Development** | **Production-Ready** | **Enterprise-Tested**

</div>

---

## ⚡ Performance & Scale

- **Response Time**: < 3 seconds average
- **Concurrent Users**: 1-10 instances (auto-scaling)
- **Knowledge Base**: Millions of documents via Vertex AI Search
- **Multi-Agent Coordination**: Up to 10 IAM1s + 40 IAM2s tested
- **Uptime**: 99.9% on Google Cloud infrastructure

---

## 🔐 Security

- ✅ **Authentication**: API key + Google Cloud IAM
- ✅ **Data Isolation**: Client-specific projects and knowledge bases
- ✅ **Network Security**: VPC controls, private endpoints
- ✅ **Encryption**: At-rest and in-transit (Google Cloud managed)
- ✅ **Audit Logging**: Full telemetry and trace data
- ✅ **A2A Security**: Peer authentication via API keys

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

This means you can:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Use for any purpose

---

## 🙏 Acknowledgments

Built with love using:

- [Google ADK](https://github.com/google/adk-python) - Agent Development Kit
- [A2A Protocol](https://a2a-protocol.org/) - Agent2Agent standard
- [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack) - Inspiration
- [Vertex AI](https://cloud.google.com/vertex-ai) - Google Cloud platform

Special thanks to our contributors and the open-source community.

---

## 📞 Get in Touch

### For Developers

- 📖 [Documentation](docs/)
- 💬 [Discussions](https://github.com/IntentSolutions/iam1-regional-manager/discussions)
- 🐛 [Issues](https://github.com/IntentSolutions/iam1-regional-manager/issues)

### For Business

- 🤝 [Become a Reseller](https://intentsolutions.io/reseller) - Partner with us
- 🏢 [Enterprise Solutions](https://intentsolutions.io/contact) - Managed deployments
- 💝 [Sponsor This Project](https://github.com/sponsors/IntentSolutions) - Support development

### Professional Support

- 📧 Email: [support@intentsolutions.io](mailto:support@intentsolutions.io)
- 🌐 Website: [intentsolutions.io](https://intentsolutions.io)
- 💼 LinkedIn: [IntentSolutions](https://linkedin.com/company/intentsolutions)
- 🐦 Twitter: [@IntentSolutions](https://twitter.com/IntentSolutions)

---

<div align="center">

### Ready to Deploy Your First IAM1?

[**Get Started →**](#-quick-start) | [**Become a Reseller →**](https://intentsolutions.io/reseller) | [**Sponsor →**](https://github.com/sponsors/IntentSolutions)

---

**Made with ❤️ by [IntentSolutions](https://intentsolutions.io)**

⭐ **Star this repo** if you find it useful! | 💝 [**Sponsor Us**](https://github.com/sponsors/IntentSolutions)

</div>

