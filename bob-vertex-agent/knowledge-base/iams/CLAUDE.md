# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**IAMS** - Intent Agent Manager & Engine System - Master directory for ALL intelligent agent systems.

**Location:** `/home/jeremy/000-projects/iams/`
**Status:** Active development across multiple agent systems
**Type:** MASTER (contains all agent system templates and implementations)

---

## 🎯 Critical Understanding: The Three-Tier Architecture

###Tier 1: iams/ (YOU ARE HERE)

**What this is:**
- Master directory for ALL agent systems (news, SDR, customer service, etc.)
- Contains general agent research, patterns, and cross-cutting templates
- NOT specific to any domain (news, sales, etc.)

**What belongs here:**
```
iams/
├── 000-docs/                    # General agent system documentation
│   ├── REASONING-TECHNIQUES-REFERENCE.md
│   ├── agent-communication-patterns.md
│   └── ... (cross-cutting patterns)
│
├── iamnews/                     # Tier 2: NEWS AGENT TEMPLATE
│   ├── templates/               # Generic news agent patterns
│   └── brightstream/            # Tier 3: BrightStream INSTANCE
│
├── iamsdr/                      # Tier 2: SDR AGENT TEMPLATE (future)
│   └── enterprise-sdr/          # Tier 3: Enterprise SDR INSTANCE (future)
│
└── ... (other agent system templates)
```

---

## Sub-Projects

### Active Projects

#### iamnews/ - News Agent Template
**Purpose:** Reusable template for building news platforms
**Status:** Template extraction in progress
**Implementations:**
- `iamnews/brightstream/` - Positive news platform (first implementation)
- *(future)* `iamnews/techstream/` - Tech news platform
- *(future)* `iamnews/bizstream/` - Business news platform

**See:** `iamnews/README.md` for template details

#### Other Agent Systems (Future)
- **iamsdr/** - SDR automation template
- **iamcustomer/** - Customer service template
- **iamanalytics/** - Analytics agent template

---

## Documentation Structure

### Tier 1: iams/ (Master)
- **Purpose:** General agent system patterns
- **Audience:** All agent systems
- **Content:** Cross-cutting research, architecture patterns, reasoning techniques

### Tier 2: Templates (e.g., iamnews/)
- **Purpose:** Domain-specific templates (news, SDR, etc.)
- **Audience:** Implementations within that domain
- **Content:** Reusable configs, tools, prompts for that domain

### Tier 3: Instances (e.g., brightstream/)
- **Purpose:** Specific implementations
- **Audience:** End users, deployment teams
- **Content:** Configuration, customizations, product docs

**Example Navigation:**
```
iams/000-docs/                          # General patterns (all domains)
└── iamnews/000-docs/                    # News patterns (all news platforms)
    └── brightstream/000-docs/           # BrightStream product docs (specific)
```

---

## File Organization Rules

### What Goes in iams/ (Tier 1)

✅ **KEEP HERE:**
- General agent architecture patterns
- Cross-domain research (applies to news, SDR, customer service, etc.)
- Reasoning techniques applicable to all agent systems
- Agent-to-Agent communication patterns
- General templates that work for ANY domain

❌ **MOVE TO SUB-PROJECTS:**
- News-specific patterns → `iamnews/`
- SDR-specific patterns → `iamsdr/`
- Implementation-specific configs → `iamnews/brightstream/`

---

## Quick Decision Guide

### "Where does this documentation go?"

**Ask:**
1. "Does this apply to ALL agent systems?" → `iams/000-docs/`
2. "Does this apply to all NEWS platforms?" → `iamnews/000-docs/`
3. "Does this apply to BrightStream only?" → `brightstream/000-docs/`

**Examples:**
- "How to implement ReACT pattern" → `iams/000-docs/` (all systems)
- "How news agents work" → `iamnews/000-docs/` (all news platforms)
- "BrightStream RSS feeds" → `brightstream/000-docs/` (specific)

---

## Navigation Map

### From iams/ (Root)
```
iams/ (YOU ARE HERE)
├── 000-docs/                    # Read for general patterns
│   └── REASONING-TECHNIQUES-REFERENCE.md
│
├── iamnews/                     # News agent systems
│   ├── CLAUDE.md               # News template guidance
│   ├── README.md               # How to use news template
│   ├── 000-docs/               # Generic news agent docs
│   │   ├── 001-PP-ARCH-iamnews-base-architecture.md
│   │   └── 002-AT-FLOW-agent-interaction-patterns.md
│   │
│   └── brightstream/            # BrightStream implementation
│       ├── CLAUDE.md           # BrightStream-specific guidance
│       ├── README.md           # BrightStream overview
│       └── 000-docs/           # BrightStream product docs
│
└── (future agent systems)
```

### Key Files by Tier

**Tier 1 (iams/):**
- `iams/CLAUDE.md` - This file (master guidance)
- `iams/000-docs/REASONING-TECHNIQUES-REFERENCE.md` - General reasoning

**Tier 2 (iamnews/):**
- `iamnews/CLAUDE.md` - News template guidance
- `iamnews/README.md` - How to use news template
- `iamnews/TEMPLATE-SEPARATION-STRATEGY.md` - Migration plan
- `iamnews/ULTRATHINK-SUMMARY.md` - Quick architecture overview

**Tier 3 (brightstream/):**
- `brightstream/CLAUDE.md` - BrightStream guidance
- `brightstream/README.md` - BrightStream overview
- `brightstream/ARCHITECTURE-CLARITY.md` - Tier explanation
- `brightstream/PROJECT-STRUCTURE-SCAFFOLD.md` - Directory structure

---

## Common Operations

### Working on BrightStream
```bash
# Navigate to BrightStream
cd /home/jeremy/000-projects/iams/iamnews/brightstream/

# Read BrightStream guidance
cat CLAUDE.md
cat README.md

# Deploy BrightStream
cd ..
terraform apply -var-file="brightstream/terraform.tfvars"
```

### Working on iamNews Template
```bash
# Navigate to template
cd /home/jeremy/000-projects/iams/iamnews/

# Read template guidance
cat CLAUDE.md
cat README.md
cat TEMPLATE-SEPARATION-STRATEGY.md

# Extract templates from BrightStream
# (follow migration plan in TEMPLATE-SEPARATION-STRATEGY.md)
```

### Working on General Agent Patterns
```bash
# Navigate to master
cd /home/jeremy/000-projects/iams/

# Read general patterns
cat 000-docs/REASONING-TECHNIQUES-REFERENCE.md

# Create new agent system template
mkdir iamsdr
cd iamsdr
# Create template structure
```

---

## Technology Stack

### Infrastructure
- **Google Cloud Platform** (primary deployment)
- **Terraform** (Infrastructure as Code)
- **Docker** (containerization)
- **GitHub Actions** (CI/CD)

### Agent Frameworks
- **Google ADK** (Agent Development Kit - primary)
- **Vertex AI Agent Engine** (managed agent hosting)
- **Genkit** (full-stack AI framework)

### AI Models
- **Gemini 2.5 Flash** (primary LLM - all projects)
- **Gemini 1.5 Pro** (complex reasoning - all projects)

**Media Generation Models** (project-specific):
- **Lyria** (audio generation - iamNews only)
- **Imagen 3** (image generation - iamNews only)
- **Veo** (video generation - iamNews only, optional)

**Note:** PipelinePilot (B2B sales automation) uses Gemini for orchestration only, not media generation.

### Languages
- **Python 3.12+** (agent implementations)
- **TypeScript/JavaScript** (Genkit backends)
- **HCL** (Terraform)
- **YAML** (agent configs)

---

## Documentation Standards

All projects follow **Document Filing System v2.0**:

**Format:** `NNN-CC-ABCD-description.ext`
- **NNN** = Sequential number (001-999)
- **CC** = Category code (PP, AT, DC, TQ, OD, LS, RA, MC, PM, DR, UC, BL, RL, AA, WA, DD, MS)
- **ABCD** = Document type (4-letter abbreviation)
- **description** = 1-4 words, kebab-case

**Category Codes:**
- **PP** = Product & Planning
- **AT** = Architecture & Technical
- **TQ** = Testing & Quality
- **OD** = Operations & Deployment
- **LS** = Logs & Status
- **RA** = Reports & Analysis
- **DR** = Documentation & Reference
- **MC** = Meetings & Communication
- **PM** = Project Management

**Example:** `001-PP-ARCH-iamnews-base-architecture.md`

---

## Design Principles

### 1. Separation of Concerns
- **Tier 1 (iams/)** - General patterns for all domains
- **Tier 2 (iamnews/)** - Domain-specific templates
- **Tier 3 (brightstream/)** - Specific implementations

### 2. Reusability
- Templates use {{PLACEHOLDERS}} for customization
- Implementations override only what's different
- Generic patterns benefit all projects

### 3. Clear Ownership
- Each tier has clear responsibility
- Documentation at appropriate level
- Easy to find what you need

### 4. Scalability
- Add new domains (iamsdr, iamcustomer) easily
- Add new implementations (techstream, bizstream) in minutes
- Patterns extracted and reused

---

## Current Status

### Completed ✅
- IAMS master directory structure
- iamNews template infrastructure (Terraform)
- BrightStream initial implementation
- Documentation standards defined

### In Progress 🟡
- Template extraction from BrightStream → iamNews
- ADK compliance fixes
- Agent tool implementations

### Planned 🔴
- iamSDR template (SDR automation)
- iamCustomer template (customer service)
- Multi-domain template patterns

---

## Support & Resources

**Location:** `/home/jeremy/000-projects/iams/`

**Related Projects:**
- iamNews Template: `iamnews/`
- BrightStream: `iamnews/brightstream/`

**External Resources:**
- Google ADK: https://github.com/google/adk-python
- Vertex AI: https://cloud.google.com/vertex-ai/docs
- Terraform: https://www.terraform.io/docs

---

**Last Updated:** 2025-10-29
**Status:** Active development (multi-project)
**Next Action:** Complete iamNews template extraction
