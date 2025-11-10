# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**iamNews** - Reusable TEMPLATE for building news agent platforms. This is NOT a specific implementation.

**Location:** `/home/jeremy/000-projects/iams/iamnews/`
**Status:** Template extraction in progress
**Type:** TEMPLATE (generic, reusable)

---

## 🎯 Critical Understanding: TEMPLATE vs INSTANCE

### This Directory (iamnews/) is a TEMPLATE

**What this means:**
- Contains GENERIC patterns for ANY news platform
- NOT specific to BrightStream, TechStream, or any implementation
- Provides reusable infrastructure, agent configs, tools, and prompts
- Used to BUILD specific implementations (instances)

**What belongs here:**
```
iamnews/
├── main.tf                 # Generic GCP infrastructure
├── variables.tf            # Customization points
├── outputs.tf              # Generic outputs
├── README.md               # How to use this template
│
├── 000-docs/               # Generic news agent documentation
│   ├── 001-PP-ARCH-iamnews-base-architecture.md
│   └── 002-AT-FLOW-agent-interaction-patterns.md
│
├── templates/              # Reusable templates (TO BE CREATED)
│   ├── agent-configs/      # Generic agent YAML templates
│   ├── agent-tools/        # Generic tool templates
│   ├── prompts/            # Generic prompt templates
│   └── infrastructure/     # Generic Docker/Makefile templates
│
└── brightstream/           # INSTANCE (specific implementation)
    └── (BrightStream-specific files only)
```

---

## Architecture Hierarchy

### Three Tiers

```
iams/                           # Tier 1: ALL agent systems
├── 000-docs/                    # General agent research
│
├── iamnews/                     # Tier 2: NEWS AGENT TEMPLATE ← YOU ARE HERE
│   ├── templates/               # Reusable templates
│   ├── 000-docs/               # Generic news agent docs
│   └── brightstream/            # Tier 3: BrightStream INSTANCE
│       ├── terraform.tfvars    # BrightStream config
│       └── customizations/     # BrightStream-specific
```

**Navigation:**
- **Parent (Tier 1):** `/home/jeremy/000-projects/iams/` - All agent systems
- **This Level (Tier 2):** `/home/jeremy/000-projects/iams/iamnews/` - News template
- **Child (Tier 3):** `/home/jeremy/000-projects/iams/iamnews/brightstream/` - BrightStream instance

---

## What Goes in THIS Directory?

### ✅ KEEP HERE (Generic, Reusable)
- **Infrastructure:** `main.tf`, `variables.tf`, `outputs.tf` (with placeholders)
- **Templates:** Agent configs, tools, prompts (with {{PLACEHOLDERS}})
- **Documentation:** How news agents work, how to create implementations
- **Examples:** Reference implementations showing different patterns

### ❌ MOVE to brightstream/ (Specific)
- BrightStream GCP project configuration
- Positive news RSS feeds
- BrightStream product specifications
- Positivity-focused customizations

---

## Current Status

### ⚠️ Template Extraction Needed

**Problem:** Most "generic" files currently in `brightstream/` directory
**Solution:** Extract to `templates/` directory with placeholders

**See:**
- `TEMPLATE-SEPARATION-STRATEGY.md` - Detailed migration plan
- `ULTRATHINK-SUMMARY.md` - Quick overview
- `brightstream/ARCHITECTURE-CLARITY.md` - Complete explanation

---

## Common Commands

### Infrastructure Management
```bash
# Initialize Terraform (from this directory)
terraform init

# Validate generic infrastructure
terraform validate

# Plan deployment with implementation config
terraform plan -var-file="brightstream/terraform.tfvars"

# Apply to specific implementation
terraform apply -var-file="brightstream/terraform.tfvars"
```

### Template Building (Future)
```bash
# Build implementation from templates
./build-implementation.sh brightstream
./build-implementation.sh techstream

# Validate templates
./validate-templates.sh
```

---

## Creating a New Implementation

### Quick Start (After Template Extraction)

```bash
# 1. Create implementation folder
mkdir mystream
mkdir mystream/{000-docs,customizations}

# 2. Copy template config
cp terraform.tfvars.template mystream/terraform.tfvars

# 3. Customize configuration
vim mystream/terraform.tfvars
# Set: project_id, platform_name, rss_feeds, etc.

# 4. Build from templates
./build-implementation.sh mystream

# 5. Deploy
terraform apply -var-file="mystream/terraform.tfvars"
```

**Time:** 30 minutes after template extraction complete

---

## Documentation Structure

### iamnews/000-docs/ (Generic)
- `001-PP-ARCH-iamnews-base-architecture.md` - News agent architecture
- `002-AT-FLOW-agent-interaction-patterns.md` - Agent workflows

### brightstream/000-docs/ (Specific)
- BrightStream product specifications
- Target audience definitions
- RSS feed lists
- Deployment status

**Rule:** If it applies to ALL news platforms → iamnews/000-docs/
**Rule:** If it's BrightStream-specific → brightstream/000-docs/

---

## Key Files in This Directory

### Infrastructure (Terraform)
- **main.tf** (16KB) - Complete GCP infrastructure for news platforms
- **variables.tf** (15KB) - All customization points
- **outputs.tf** (12KB) - Infrastructure outputs
- **terraform.tfvars.example** (9KB) - Template configuration

### Documentation
- **README.md** - Template usage guide
- **TEMPLATE-SEPARATION-STRATEGY.md** - Migration plan
- **ULTRATHINK-SUMMARY.md** - Architecture overview

### Implementations
- **brightstream/** - Positive news platform (first implementation)
- *(future)* **techstream/** - Tech news platform
- *(future)* **bizstream/** - Business news platform

---

## Technology Stack

**Infrastructure:** Google Cloud Platform (Vertex AI, Firestore, Cloud Storage, Cloud Run)
**Framework:** Google ADK (Agent Development Kit)
**Models:** Gemini 2.5 Flash (primary), Lyria (audio), Imagen 3 (images)
**IaC:** Terraform 1.5+
**Language:** Python 3.12+

---

## Design Principles

### Template Design
1. **Generic by default** - No implementation-specific code in templates
2. **Customizable** - Use {{PLACEHOLDERS}} for all variable parts
3. **Well-documented** - Every template has usage examples
4. **Validated** - Templates tested with multiple implementations

### Implementation Pattern
1. **Minimal override** - Only customize what's different
2. **Clear ownership** - Template vs customization separation
3. **Version tracking** - Track which template version used
4. **Easy upgrade** - Rebuild from newer template versions

---

## Migration Status

### Completed ✅
- Base Terraform infrastructure
- Generic architecture documentation
- BrightStream initial build (mixed template + specific)

### In Progress 🟡
- Template extraction from BrightStream
- Template placeholder system
- Build system creation

### Planned 🔴
- Template validation
- Second implementation (TechStream) for validation
- CI/CD for template + implementations

---

## Support & Resources

**Related Documentation:**
- `brightstream/CLAUDE.md` - BrightStream-specific guidance
- `brightstream/ARCHITECTURE-CLARITY.md` - Complete tier explanation
- `../000-docs/` - General IAMS documentation

**External Resources:**
- Google ADK: https://github.com/google/adk-python
- Vertex AI Agent Engine: https://cloud.google.com/vertex-ai/docs/agents
- Terraform Google Provider: https://registry.terraform.io/providers/hashicorp/google/latest

---

## Quick Decision Guide

### "Should this go in iamnews/ or brightstream/?"

**Ask yourself:**
- ✅ "Would TechStream need this?" → iamnews/templates/
- ✅ "Would BizStream need this?" → iamnews/templates/
- ✅ "Is this about news agents in general?" → iamnews/000-docs/
- ❌ "Is this specific to positive news?" → brightstream/
- ❌ "Is this BrightStream's RSS feed list?" → brightstream/
- ❌ "Is this BrightStream's branding?" → brightstream/

**When in doubt:** Put it in iamnews/ with placeholders, let implementations customize.

---

**Last Updated:** 2025-10-29
**Status:** Template directory (extraction in progress)
**Next Action:** Complete template extraction from BrightStream
