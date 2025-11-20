# Repository Relationships

**Date:** 2025-11-11
**Category:** 062-DR-REPO (Documentation Reference - Repository)
**Status:** Documentation

---

## Repository Structure

### Template Repository (iam1-intent-agent-model-vertex-ai)

**URL:** https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai

**Purpose:** Template for building ADK + Agent Engine agents with Hard Mode architecture

**Contains:**
- Hard Mode architecture (R1-R8 rules)
- ADK + Agent Engine foundation
- Terraform infrastructure boilerplate
- CI/CD workflows with drift detection
- Complete documentation structure
- Best practices and patterns

**Use Case:** Clone this template to create NEW agent projects

**Visibility:** Public (so others can use it)

---

### Implementation Repository (bobs-brain)

**URL:** https://github.com/jeremylongshore/bobs-brain

**Purpose:** Specific implementation of the IAM1 template for Slack AI assistant

**Contains:**
- All template code (customized for Bob's Brain)
- Slack integration (webhook + events)
- Production deployment configuration
- Environment-specific settings (dev/staging/prod)
- Bob-specific tools and customizations

**Use Case:** This is the ACTUAL Bob's Brain production system

**Visibility:** Public

**Relationship to Template:**
- Built FROM the iam1-intent-agent-model-vertex-ai template
- Implements the Hard Mode rules (R1-R8)
- Adds Slack-specific functionality
- Production-ready configuration

---

## How to Use

### Creating a New Agent (Use Template)

```bash
# Clone the template
git clone https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai.git my-new-agent

cd my-new-agent

# Customize for your use case
# - Update agent name in variables
# - Implement your tools in my_agent/tools/
# - Configure your integrations (not Slack, something else)
# - Update documentation

# Deploy your agent
cd infra/terraform
terraform apply -var-file="envs/prod.tfvars"
```

### Working on Bob's Brain (Use Implementation)

```bash
# Clone Bob's Brain
git clone https://github.com/jeremylongshore/bobs-brain.git

cd bobs-brain

# Make changes
# - Update agent logic
# - Add new Slack features
# - Improve existing tools

# Deploy
cd infra/terraform
terraform apply -var-file="envs/prod.tfvars"
```

---

## Repository Comparison

| Aspect | Template (IAM1) | Implementation (Bob's Brain) |
|--------|----------------|------------------------------|
| **Purpose** | Generic agent template | Slack AI assistant |
| **Use Case** | Clone for new projects | Production Bob's Brain |
| **Integration** | None (you add yours) | Slack webhook + events |
| **Deployment** | Example configs | Production configs |
| **Customization** | High (starting point) | Specific (Slack-focused) |
| **Visibility** | Public (template) | Public (implementation) |
| **Updates** | Template improvements | Bob-specific features |

---

## Update Strategy

### Template Updates (iam1-intent-agent-model-vertex-ai)

When improving the template:
1. Update core architecture patterns
2. Improve Terraform configurations
3. Enhance documentation
4. Add new Hard Mode enforcement
5. Update CI/CD workflows

**DO NOT** add Bob-specific code to the template.

### Implementation Updates (bobs-brain)

When improving Bob's Brain:
1. Add Slack-specific features
2. Improve conversation handling
3. Add Bob-specific tools
4. Update production configurations

**CAN** pull template improvements into Bob's Brain.

---

## Syncing Template Improvements

If the template gets updated, you can pull improvements into Bob's Brain:

```bash
# In Bob's Brain repo
cd /home/jeremy/000-projects/iams/bobs-brain

# Add template as remote
git remote add template https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai.git

# Fetch template updates
git fetch template

# Review changes
git diff main template/main

# Merge specific improvements (carefully)
git cherry-pick <commit-hash>

# Or merge entire template branch (risky)
git merge template/main
```

---

## Directory Locations

**Local Development:**
- Template: `/home/jeremy/000-projects/iams/bobs-brain/` (this is Bob's Brain, based on template)
- Implementation: Same location

**GitHub:**
- Template: https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai
- Implementation: https://github.com/jeremylongshore/bobs-brain

---

## Key Differences

### What's in BOTH

- Hard Mode architecture (R1-R8)
- ADK + Agent Engine setup
- Terraform infrastructure
- CI/CD workflows
- Drift detection
- Documentation structure

### What's ONLY in Bob's Brain

- Slack integration code
- `service/slack_webhook/` implementation
- Slack-specific environment variables
- Production Slack credentials (in tfvars)
- Bob's personality/prompt customizations
- Deployed to `bobs-brain` GCP project

### What's ONLY in Template

- Generic gateway examples
- Placeholder configurations
- More comments/documentation for learning
- Example tool implementations
- Starter documentation

---

## Decision Tree

**Question:** "Should I update the template or Bob's Brain?"

```
Is this change...
├─ Generic architecture improvement? → Update TEMPLATE
├─ Slack-specific feature? → Update BOB'S BRAIN
├─ Hard Mode rule enhancement? → Update TEMPLATE
├─ Bob's personality/behavior? → Update BOB'S BRAIN
├─ Terraform best practice? → Update TEMPLATE
├─ Production config tweak? → Update BOB'S BRAIN
└─ CI/CD improvement? → Update TEMPLATE (then pull into Bob)
```

---

## Visibility

Both repositories are **PUBLIC**:

**Template (iam1-intent-agent-model-vertex-ai):**
- Public so others can use it
- No secrets (only example configs)
- General-purpose agent template

**Implementation (bobs-brain):**
- Public (decided by user)
- Production secrets in GCP Secret Manager (not in repo)
- Actual working Slack assistant

**Security Note:** All secrets managed via:
- Secret Manager (production)
- `.env` files (local, .gitignored)
- GitHub Secrets (CI/CD)

NO SECRETS IN EITHER REPOSITORY ✅

---

## Summary

**Template:** https://github.com/jeremylongshore/iam1-intent-agent-model-vertex-ai
- Generic agent template with Hard Mode
- Use to create NEW agents
- Public for community

**Bob's Brain:** https://github.com/jeremylongshore/bobs-brain
- Specific Slack AI assistant implementation
- Built FROM the template
- Production system
- Public

**Relationship:** Bob's Brain is a specific implementation of the IAM1 template.

---

**Last Updated:** 2025-11-11
**Category:** Repository Relationships
**Status:** Active (both repos public)
