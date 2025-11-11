# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Intent Solutions landing page - Professional website showcasing customizable Intent Agent Models (IAM), private AI infrastructure, automation services, and education resources.

**Active Project**: `/astro-site` (Astro 5.14 + React 19 islands)
**Deployed at**: https://intentsolutions.io
**Deployment**: Netlify (auto-deploy on push to main)

## Core Positioning

### Intent Agent Models (IAM)
- **IAM** = Intent Agent Models - fully customizable AI agent building blocks
- **IAE** = Intent Agent Engine - the framework powering IAM
- **M1/M2/M3** = Pre-configured IAE packages (starters for common use cases)
- **Key Message**: "We customize any IAM for any workflow"

### PipelinePilot MVP
- **What**: Live production SDR automation platform
- **How**: Built with 4 customized IAM agents
- **Purpose**: Proof of IAM customizability
- **URL**: https://pipelinepilot-prod.web.app
- **4 Agents**: Orchestrator, Data Captain, Content Analyst, Readiness Auditor

### Site Principles
- Model-agnostic (Claude, OpenAI, Gemini, Llama, Mistral, Qwen, fine-tunes, local)
- Transparent pricing (flat fee + usage pass-through)
- Vertex-first security for production (with n8n for orchestration)
- No vendor lock-in messaging

## Site Structure

```
/
├── /                          # Homepage with hero, products, services, contact
├── /agents                    # IAM packages (M1/M2/M3) + PipelinePilot example
├── /private-ai                # Model-agnostic private AI infrastructure
├── /automation                # n8n automation + Vertex comparison
├── /cloud                     # Google Cloud services
├── /about                     # About page
├── /resellers                 # White-label reseller program
├── /learn                     # Education hub
│   ├── /learn/pricing         # Transparent pricing explanation
│   ├── /learn/security        # Vertex vs self-hosted comparison
│   └── /learn/models          # Model-agnostic delivery (9 model families)
└── /survey                    # HUSTLE survey flow (15 sections, 76 questions)
```

## Key Components

### New Components (2025-01-03 refactor)
- **MvpShowcase.tsx** - Modal showcasing PipelinePilot's 4 custom IAM agents
- **PricingBlocks.tsx** - Reusable transparent pricing component

### Core Components
- **Hero.tsx** - Main hero with Framer Motion animations
- **Products.tsx** - 9 product showcase items
- **Services.tsx** - Service offerings grid
- **Contact.tsx** - React Hook Form + Zod validation + Netlify Forms
- **Footer.tsx** - Footer with learn/resellers links
- **SiteNav.astro** - Navigation with learn/resellers links

## Recent Major Updates (2025-01-03)

### Complete Site Refactor
1. **IAM Positioning**: Emphasized customizability of Intent Agent Models
2. **Education Hub**: Created `/learn` with pricing/security/models pages
3. **Resellers Program**: Added `/resellers` white-label program page
4. **PipelinePilot Integration**: Linked live MVP showing 4 custom IAM agents
5. **Model-Agnostic Messaging**: Emphasized flexibility across all pages
6. **Transparent Pricing**: Clear engagement ladder (discovery → MVP → managed → enterprise)

### Key Messaging Updates
- IAM are "fully customizable" for any workflow
- PipelinePilot shows "customized IAM for SDR automation"
- M1/M2/M3 are "pre-configured starters"
- Vertex recommended for production, n8n for orchestration glue
- 9 model families supported (Claude, OpenAI, Gemini, Llama, Mistral, Qwen, fine-tunes, local, others)

## Development Workflow

### Installation
```bash
cd astro-site
bun install
```

### Development
```bash
bun run dev  # http://localhost:4321
```

### Build & Preview
```bash
bun run build
bun run preview
```

### Deployment
**Automatic**: Push to `main` branch triggers Netlify deployment

```bash
git add .
git commit -m "feat: description"
git push origin main
```

Netlify auto-detects settings from `netlify.toml`:
- Build command: `bun run build`
- Publish directory: `dist`

## Tech Stack

- **Framework**: Astro 5.14 (SSG)
- **UI**: React 19 islands (partial hydration)
- **Styling**: Tailwind CSS 4
- **Animations**: Framer Motion
- **Forms**: React Hook Form + Zod
- **Deployment**: Netlify
- **Domain**: intentsolutions.io

## Design System

### Charcoal Slate Theme
- **Colors**: Zinc palette (900-50)
- **Typography**: Inter font family
- **Style**: Minimal professional gray monochrome
- **Animations**: Framer Motion page load + scroll triggers

### Key Classes
- `card-slate` - Standard content card
- `btn-primary` - Primary CTA button
- `text-h1` - Hero heading size
- `transition-smooth` - Consistent transitions

## Important Files

### Configuration
- `astro-site/astro.config.mjs` - Astro configuration
- `astro-site/tailwind.config.mjs` - Tailwind theme
- `astro-site/netlify.toml` - Netlify build settings
- `astro-site/src/styles/global.css` - Theme variables

### Documentation
- `claudes-docs/INTENT-SOLUTIONS-WEB-DESIGN-DOCUMENTATION.md` - Complete site documentation
- `claudes-docs/REFACTOR-IMPLEMENTATION-GUIDE.md` - Refactor implementation notes

## Content Guidelines

### Messaging Do's
✅ Emphasize IAM customizability
✅ Position PipelinePilot as proof of customization
✅ Show model-agnostic flexibility
✅ Be transparent about pricing
✅ Recommend Vertex for production with clear reasoning
✅ Link to PipelinePilot MVP: https://pipelinepilot-prod.web.app

### Messaging Don'ts
❌ Don't imply vendor lock-in
❌ Don't say "3 agents" as a product cap
❌ Don't link IAM to specific platforms (LinkedIn, etc.)
❌ Don't hide pricing or make it opaque
❌ Don't imply Vertex is the only option

## SEO

### Meta Descriptions
- Default: "Model-agnostic AI agents, private AI infrastructure, and n8n automation. Transparent pricing, Vertex-first security, no vendor lock-in."
- Each page has custom title/description

### Key Pages for SEO
- Homepage: Core positioning and offerings
- /agents: IAM packages and PipelinePilot example
- /learn: Education hub with pricing/security/models
- /resellers: White-label program for agencies

## Support & Contact

- **Email**: jeremy@intentsolutions.io
- **Location**: Gulf Shores, Alabama
- **Blog**: https://startaitools.com
- **GitHub**: https://github.com/jeremylongshore

## Quick Reference

### View Site Locally
```bash
cd astro-site && bun run dev
```

### Deploy Changes
```bash
git add . && git commit -m "your message" && git push origin main
```

### Test Production Build
```bash
bun run build && bun run preview
```

---

**Last Updated**: 2025-01-03
**Version**: 2.1.1
**Status**: ✅ Production site with complete refactor deployed
