# GitHub Template Setup for IAM1 Regional Manager

**Created:** 2025-11-09
**Purpose:** Convert bob-vertex-agent into a public GitHub template repository for IAM1 deployments

---

## Overview

Transform bob-vertex-agent into **iam1-regional-manager** - a GitHub template repository that enables:

1. **Open Source Community**: Public template for developers to build multi-agent systems
2. **Client Deployments**: Use template to create client-specific IAM1 instances
3. **Base Model Sync**: Clients can pull updates from template when IAM1 improves
4. **Marketing**: "Open source IAM1 Regional Manager with A2A Protocol support"

---

## Business Model

### Open Core Strategy

**Free (Open Source):**
- IAM1 base template on GitHub
- Full source code with MIT/Apache 2.0 license
- Community contributions welcome
- Documentation and examples

**Paid (IntentSolutions Services):**
- Managed deployments for clients
- Client-specific knowledge grounding (Vertex AI Search)
- Custom IAM2 specialist development
- Multi-IAM1 enterprise coordination setup
- Support and maintenance ($500/month per IAM1)

**Revenue Model:**
- Template is free → Builds brand awareness
- Deployments are paid → Recurring revenue
- Community improvements → Enhanced product
- Contributors → Potential hires/partners

---

## Repository Structure

### Current (bob-vertex-agent)

```
bob-vertex-agent/
├── app/                    # IAM1 source code
├── deployment/             # Terraform infrastructure
├── data_ingestion/         # Knowledge base pipeline
├── slack-webhook/          # Slack integration
├── tests/                  # Test suites
├── pyproject.toml          # Dependencies
├── Makefile                # Deployment commands
└── README.md               # Documentation
```

### Proposed (iam1-regional-manager)

```
iam1-regional-manager/
├── app/                    # IAM1 source code
│   ├── agent.py            # Main orchestrator
│   ├── sub_agents.py       # IAM2 specialists
│   ├── a2a_tools.py        # Peer coordination
│   ├── agent_card.json     # A2A discovery
│   └── retrievers.py       # RAG knowledge
├── deployment/             # Terraform infrastructure
│   └── terraform/
│       ├── dev/            # Dev environment
│       ├── staging/        # Staging environment
│       └── prod/           # Production environment
├── data_ingestion/         # Knowledge pipeline
├── integrations/           # Optional integrations
│   └── slack/              # Slack webhook
├── tests/                  # Test suites
├── docs/                   # Documentation
│   ├── DEPLOYMENT.md       # Deployment guide
│   ├── A2A-SETUP.md        # A2A configuration
│   ├── CLIENT-SETUP.md     # Client deployment guide
│   └── UPGRADE-SYNC.md     # Syncing template updates
├── examples/               # Example configurations
│   ├── sales-iam1/         # Sales domain example
│   ├── engineering-iam1/   # Engineering example
│   └── multi-iam1/         # Enterprise multi-IAM1
├── .github/
│   ├── workflows/          # GitHub Actions CI/CD
│   └── ISSUE_TEMPLATE/     # Issue templates
├── pyproject.toml          # Dependencies
├── Makefile                # Deployment commands
├── LICENSE                 # MIT or Apache 2.0
├── CONTRIBUTING.md         # Contribution guidelines
├── CODE_OF_CONDUCT.md      # Community standards
└── README.md               # Main documentation
```

---

## Rebranding Checklist

### 1. Repository Name

**Change:**
- FROM: `bob-vertex-agent`
- TO: `iam1-regional-manager`

**Git command:**
```bash
# GitHub Settings → Repository → Settings → Repository name
# Or create new repo and migrate
```

### 2. Display Names

**Update all references:**
- `pyproject.toml`: `name = "iam1-regional-manager"`
- README title: "IAM1 Regional Manager"
- Agent card: `"name": "IntentSolutions IAM1 - Regional Manager Agent"`
- Documentation headers

### 3. Internal Code Names

**Keep "Bob" internally, rename user-facing:**
- ✅ KEEP: Internal variable names (e.g., `bob_orchestrator`)
- ✅ CHANGE: User-facing strings (e.g., error messages, logs)
- ✅ CHANGE: Display names in console/UI
- ✅ CHANGE: Agent card metadata

### 4. GitHub Template Settings

**Enable Template Repository:**
1. Go to GitHub repo settings
2. Check "Template repository" checkbox
3. Add topics: `ai-agent`, `multi-agent-system`, `vertex-ai`, `a2a-protocol`, `google-adk`

---

## README.md Template

```markdown
# IAM1 Regional Manager

![Version](https://img.shields.io/badge/version-2.0.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![A2A Protocol](https://img.shields.io/badge/A2A-0.3.0-purple)

> Production-ready hierarchical multi-agent system with A2A Protocol support on Google Cloud Vertex AI

## Overview

**IAM1 Regional Manager** is an open-source template for building sovereign AI agents that can:

- 🤖 **Orchestrate IAM2 Specialists** - Command subordinate agents (Research, Code, Data, Slack)
- 🤝 **Coordinate with Peer IAM1s** - Cross-domain collaboration via A2A Protocol
- 📚 **Ground in Knowledge** - RAG-powered retrieval from Vertex AI Search
- 🚀 **Deploy to Production** - Terraform infrastructure + CI/CD included
- 💼 **Client Isolation** - Deploy per-client with isolated knowledge bases

## Quick Start

### 1. Use This Template

Click "Use this template" on GitHub to create your own IAM1 repository.

### 2. Deploy to Google Cloud

```bash
# Clone your new repository
git clone https://github.com/YOUR-USERNAME/your-iam1-instance.git
cd your-iam1-instance

# Set your GCP project
export PROJECT_ID=your-gcp-project

# Install dependencies
uv sync

# Deploy to Vertex AI Agent Engine
make deploy
```

### 3. Configure Domain (Optional)

```bash
# Set IAM1 domain (sales, engineering, operations, etc.)
export DOMAIN=sales

# Deploy domain-specific IAM1
make deploy
```

## Architecture

```
┌─────────────────────────────────────────┐
│  IAM1 (Regional Manager)                │
│  - Sovereign in domain                  │
│  - Coordinates with peer IAM1s (A2A)    │
│  - Commands IAM2 subordinates           │
└─────────────────────────────────────────┘
         │                      │
         │ Commands             │ Coordinates (A2A)
         ▼                      ▼
┌─────────────────────┐   ┌─────────────────┐
│  IAM2 Specialists   │   │  Peer IAM1s     │
│  - Research         │   │  - Engineering  │
│  - Code             │   │  - Sales        │
│  - Data             │   │  - Operations   │
│  - Slack            │   │  - Marketing    │
└─────────────────────┘   └─────────────────┘
```

## Features

### Core Capabilities

- ✅ **Multi-Agent Orchestration** - Hierarchical IAM1 → IAM2 delegation
- ✅ **A2A Protocol Support** - Peer-to-peer agent coordination
- ✅ **RAG Knowledge Grounding** - Vertex AI Search integration
- ✅ **Production Infrastructure** - Terraform, CI/CD, monitoring
- ✅ **Client Isolation** - Per-client deployments with isolated data

### IAM2 Specialists

| Specialist | Purpose | Use Cases |
|------------|---------|-----------|
| **Research** | Deep research, knowledge synthesis | Multi-source research, comparative analysis |
| **Code** | Code generation, debugging | Writing code, fixing bugs, refactoring |
| **Data** | BigQuery queries, data analysis | SQL queries, analytics, insights |
| **Slack** | Slack interactions, formatting | Channel management, user operations |

### A2A Peer Coordination

Coordinate with other IAM1 agents across domains:

- **Engineering IAM1** - Product roadmap, technical architecture
- **Sales IAM1** - Sales metrics, customer data, forecasts
- **Operations IAM1** - Infrastructure, support tickets
- **Marketing IAM1** - Campaign performance, brand metrics
- **Finance IAM1** - Budget, financial forecasts
- **HR IAM1** - Headcount, hiring, org structure

## Documentation

- [Deployment Guide](docs/DEPLOYMENT.md) - Deploy IAM1 to Google Cloud
- [A2A Setup](docs/A2A-SETUP.md) - Configure peer coordination
- [Client Setup](docs/CLIENT-SETUP.md) - Deploy for specific clients
- [Upgrade Sync](docs/UPGRADE-SYNC.md) - Pull updates from template

## Examples

### Single IAM1 Deployment

Deploy a standalone IAM1 for a single domain:

```bash
export PROJECT_ID=client-a-project
export DOMAIN=sales
make deploy
```

### Multi-IAM1 Enterprise

Deploy multiple IAM1s with A2A coordination:

```bash
# Deploy Engineering IAM1
cd deployments/engineering-iam1
export PROJECT_ID=enterprise-engineering
make deploy

# Deploy Sales IAM1 (with Engineering peer URL)
cd ../sales-iam1
export PROJECT_ID=enterprise-sales
export IAM1_ENGINEERING_URL=https://engineering-iam1.example.com
make deploy
```

See [examples/](examples/) for complete configurations.

## Technology Stack

- **Runtime**: Python 3.10+
- **AI Platform**: Google Vertex AI Agent Engine
- **LLM**: Gemini 2.0 Flash (orchestrator), Gemini 2.5 Flash (specialists)
- **Framework**: Google ADK (Agent Development Kit)
- **Knowledge**: Vertex AI Search (RAG grounding)
- **Protocol**: A2A (Agent-to-Agent) 0.3.0
- **Infrastructure**: Terraform
- **CI/CD**: GitHub Actions

## Requirements

- Python 3.10+
- Google Cloud SDK (`gcloud`)
- Terraform 1.0+
- `uv` package manager

## Known Issues

### Deprecation Warnings

**google-cloud-storage < 3.0.0:**
- Warning: Will be removed in future version
- Status: Works until updated
- Action: Monitor for google-cloud-aiplatform updates

**vertexai model_garden:**
- Deprecated: June 24, 2025
- Removed: June 24, 2026
- Status: Works until mid-2026
- Action: Google will release migration path

These are non-blocking warnings. Everything works correctly.

## Business Model

### Open Source Template (Free)

- Full source code (MIT License)
- Community contributions welcome
- Documentation and examples
- Deploy yourself on Google Cloud

### Professional Services (Paid)

IntentSolutions offers managed IAM1 deployments:

- **Basic**: $500/month per IAM1
- **Team**: +$200/IAM2 specialist
- **Enterprise**: Custom pricing for multi-IAM1 coordination

Services include:
- Managed deployment and infrastructure
- Client-specific knowledge grounding
- Custom IAM2 specialist development
- A2A multi-agent setup
- Support and maintenance

Contact: support@intentsolutions.io

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/IntentSolutions/iam1-regional-manager.git
cd iam1-regional-manager

# Install dependencies
uv sync

# Run tests
make test

# Deploy to dev environment
export PROJECT_ID=your-dev-project
make deploy
```

## Community

- [GitHub Discussions](https://github.com/IntentSolutions/iam1-regional-manager/discussions) - Questions and ideas
- [Issue Tracker](https://github.com/IntentSolutions/iam1-regional-manager/issues) - Bug reports and feature requests
- [Contributing Guide](CONTRIBUTING.md) - How to contribute

## License

MIT License - See [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [Google ADK](https://github.com/google/adk-python)
- Uses [A2A Protocol](https://a2a-protocol.org/)
- Inspired by [Agent Starter Pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)

---

**Created by IntentSolutions** | [Website](https://intentsolutions.io) | [LinkedIn](https://linkedin.com/company/intentsolutions)
```

---

## Upgrade Sync Mechanism

### Problem

When you improve the base IAM1 template, how do deployed instances get updates?

### Solution: Git Remote Upstream

**Strategy:**
1. Template repo: `IntentSolutions/iam1-regional-manager` (upstream)
2. Client repo: `client-a/sales-iam1` (forked/templated from upstream)
3. Client adds upstream remote and merges updates selectively

### Workflow

**Initial Deployment (Client):**
```bash
# Use GitHub template to create new repo
# https://github.com/IntentSolutions/iam1-regional-manager/generate

# Clone client-specific repo
git clone https://github.com/client-a/sales-iam1.git
cd sales-iam1

# Add upstream template as remote
git remote add upstream https://github.com/IntentSolutions/iam1-regional-manager.git

# Customize for client
# ... client-specific changes ...

# Deploy
export PROJECT_ID=client-a-sales
make deploy
```

**Pulling Updates (Client):**
```bash
# Fetch latest from template
git fetch upstream

# Review changes
git log HEAD..upstream/main

# Merge updates (selectively)
git merge upstream/main

# Or cherry-pick specific commits
git cherry-pick <commit-hash>

# Test updates
make test

# Deploy updated IAM1
make deploy
```

**Automated Update Checks:**

Create `.github/workflows/check-upstream.yml`:

```yaml
name: Check for Template Updates

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  check-upstream:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Add upstream remote
        run: |
          git remote add upstream https://github.com/IntentSolutions/iam1-regional-manager.git
          git fetch upstream

      - name: Check for updates
        id: check
        run: |
          BEHIND=$(git rev-list HEAD..upstream/main --count)
          echo "behind=$BEHIND" >> $GITHUB_OUTPUT

      - name: Create issue if updates available
        if: steps.check.outputs.behind > 0
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: 'Template updates available from upstream',
              body: `There are ${{ steps.check.outputs.behind }} new commits in the template repository.\\n\\nTo update:\\n\`\`\`bash\\ngit fetch upstream\\ngit log HEAD..upstream/main\\ngit merge upstream/main\\n\`\`\``,
              labels: ['upstream-update']
            })
```

### Documentation: `docs/UPGRADE-SYNC.md`

```markdown
# Syncing Updates from IAM1 Template

## Overview

Your IAM1 instance is based on the **IntentSolutions/iam1-regional-manager** template. When the template improves, you can pull updates into your deployment.

## Setup (One-time)

Add the template as an upstream remote:

```bash
cd your-iam1-repo
git remote add upstream https://github.com/IntentSolutions/iam1-regional-manager.git
git fetch upstream
```

## Checking for Updates

```bash
# Fetch latest from template
git fetch upstream

# See what's changed
git log HEAD..upstream/main --oneline

# View detailed changes
git log HEAD..upstream/main
```

## Pulling Updates

### Option 1: Merge All Updates

```bash
# Merge all template updates
git merge upstream/main

# Resolve conflicts if any
# ... fix conflicts ...

# Test
make test

# Deploy
make deploy
```

### Option 2: Cherry-pick Specific Updates

```bash
# Pick specific commits
git cherry-pick <commit-hash>

# Or range of commits
git cherry-pick <start-hash>..<end-hash>
```

### Option 3: Review Changes First

```bash
# Create review branch
git checkout -b review-upstream-updates
git merge upstream/main

# Test in review branch
make test

# If good, merge to main
git checkout main
git merge review-upstream-updates
```

## What to Update

### Safe to Update (Low Risk)

- Bug fixes in IAM1 orchestrator
- New IAM2 specialist capabilities
- Documentation improvements
- Test suite enhancements

### Review Carefully (Medium Risk)

- Changes to routing logic
- A2A protocol updates
- Dependency upgrades
- Infrastructure changes (Terraform)

### Client-Specific (Don't Overwrite)

- Knowledge base configuration
- Client-specific IAM2 customizations
- Environment-specific Terraform vars
- Custom integrations

## Automated Update Notifications

Enable GitHub Action to check for updates weekly:

1. Copy `.github/workflows/check-upstream.yml` from template
2. Push to your repo
3. Get weekly notifications when updates are available

## Best Practices

1. **Test Before Production**: Always test updates in dev/staging first
2. **Review Changelogs**: Read what changed before merging
3. **Backup Before Update**: Ensure you can rollback if needed
4. **Incremental Updates**: Don't let updates pile up - sync regularly
5. **Document Custom Changes**: Track what you've customized vs template

## Rollback

If an update breaks something:

```bash
# Rollback to previous commit
git reset --hard HEAD~1

# Or specific commit
git reset --hard <good-commit-hash>

# Force push if already deployed
git push origin main --force

# Redeploy previous version
make deploy
```

## Support

Issues with template updates? Contact IntentSolutions support:
- Email: support@intentsolutions.io
- GitHub Issues: https://github.com/IntentSolutions/iam1-regional-manager/issues
```

---

## Next Steps

### 1. Repository Rebranding (This Week)

- [ ] Create new GitHub repository: `iam1-regional-manager`
- [ ] Migrate code from `bob-vertex-agent`
- [ ] Update all branding references
- [ ] Enable template repository setting
- [ ] Add topics and description

### 2. Documentation (This Week)

- [ ] Write comprehensive README.md
- [ ] Create DEPLOYMENT.md guide
- [ ] Write A2A-SETUP.md for peer coordination
- [ ] Create CLIENT-SETUP.md for client deployments
- [ ] Write UPGRADE-SYNC.md for template updates
- [ ] Add CONTRIBUTING.md and CODE_OF_CONDUCT.md

### 3. Examples (Week 2)

- [ ] Create `examples/sales-iam1/` with full config
- [ ] Create `examples/engineering-iam1/` with full config
- [ ] Create `examples/multi-iam1/` enterprise setup
- [ ] Add README to each example

### 4. GitHub Features (Week 2)

- [ ] Set up GitHub Actions CI/CD
- [ ] Create issue templates
- [ ] Configure GitHub Discussions
- [ ] Add labels for community management

### 5. Marketing Launch (Week 3)

- [ ] Announce on social media (LinkedIn, Twitter)
- [ ] Post to relevant communities (Reddit r/MachineLearning, Hacker News)
- [ ] Write blog post: "Open Source IAM1 Regional Manager"
- [ ] Create demo video
- [ ] Submit to awesome-lists (awesome-ai-agents, awesome-multi-agent-systems)

---

## License Recommendation

**MIT License** (Recommended)

Pros:
- Most permissive
- Encourages adoption
- Allows commercial use
- Simple and well-understood

Alternative: **Apache 2.0**

Pros:
- Patent grant protection
- More formal contributor agreements
- Better for enterprise adoption

---

## Success Metrics

### Community Growth

- GitHub stars: Target 100 in first month
- Forks: Target 20 client deployments
- Contributors: Target 5 external contributors
- GitHub Discussions: Active community Q&A

### Business Impact

- Leads generated: Track "Contact Us" from GitHub
- Professional service inquiries
- Brand awareness (blog views, social engagement)
- Enterprise demos scheduled

### Technical Adoption

- PyPI downloads (if published)
- Deployment success rate
- Template usage statistics
- Community PRs merged

---

**Document Version:** 1.0
**Last Updated:** 2025-11-09
**Next Review:** After template launch
