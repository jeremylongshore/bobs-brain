# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal portfolio and technical blog for Jeremy Longshore, AI Automation Specialist based in Gulf Shores, Alabama. Built with Hugo and the hugo-bearblog theme, featuring production engineering case studies, cloud infrastructure work, and AI automation projects.

**Live site:** https://jeremylongshore.com
**GitHub:** https://github.com/jeremylongshore
**Company:** intentsolutions.io
**Contact:** jeremy@intentsolutions.io

**Active Projects Referenced:**
- [DiagnosticPro](https://diagnosticpro.io) - AI diagnostic platform (Google Vertex AI Gemini, 266 BigQuery tables, 226+ RSS feeds)
- [Claude Code Plugins Plus](https://github.com/jeremylongshore/claude-code-plugins-plus) - 227 plugins hub with Skills Powerkit
- [Start AI Tools](https://startaitools.com) - AI tools directory and implementation guides
- [Bob's Brain](https://github.com/jeremylongshore/bobs-brain) - Sovereign AI agent for Slack
- [Waygate MCP](https://github.com/jeremylongshore/waygate-mcp) - Enterprise MCP server framework
- Hustle - Youth sports stats app (private repo, Next.js 15 + PostgreSQL)

## Key Commands

### Local Development
```bash
# Start local development server with live reload
hugo server -D  # -D flag includes draft posts

# Start server without drafts (production-like preview)
hugo server

# Start server accessible from external devices
hugo server -D --bind 0.0.0.0
```

### Building the Site
```bash
# Production build (used by Netlify)
hugo --gc --minify --cleanDestinationDir

# Standard build to public/ directory
hugo
```

### Content Management
```bash
# Create a new blog post (primary location)
hugo new posts/my-new-post.md

# Create static pages
hugo new about.md
hugo new contact.md
```

### Content Synchronization from Start AI Tools
```bash
# Run Python sync script (primary method)
python scripts/sync-startaitools.py

# Automated: GitHub Actions runs daily at 06:17 UTC
# Manual trigger: workflow_dispatch via GitHub Actions UI
```

## Project Structure

```
jeremylongshore/
├── config/_default/
│   └── config.toml              # Main Hugo configuration (TOML format)
├── content/
│   ├── posts/                   # Primary blog posts (69+ published posts)
│   │   └── startai/            # Synced content from Start AI Tools (38 posts)
│   ├── en/blogs/               # Legacy blog structure (1 post for compatibility)
│   ├── _index.md               # Homepage content
│   ├── about.md                # About page (20+ years ops → AI specialist)
│   ├── contact.md              # Contact page
│   └── projects.md             # Projects showcase (DiagnosticPro, Hybrid AI Stack, etc.)
├── themes/
│   └── hugo-bearblog/          # Active theme (Git submodule, minimal design)
├── static/
│   └── images/                 # Static assets (images, CSS, JS)
│       └── startai/            # Downloaded images from synced content
├── scripts/
│   ├── sync-startaitools.py    # Python sync script (primary, requests + beautifulsoup4)
│   └── sync-startaitools.sh    # Bash sync script (legacy)
├── public/                     # Generated site (DO NOT EDIT - auto-generated)
├── netlify.toml                # Netlify deployment config (Hugo v0.150.0)
├── README.md                   # Project documentation (⚠️ OUTDATED - being updated)
└── .github/workflows/
    ├── sync-startaitools.yml   # Daily automated content sync (06:17 UTC)
    └── release.yml             # Release workflow
```

**Note:** README.md contains outdated information (mentions Hermit v2 theme, wrong Hugo version). This CLAUDE.md is the source of truth.

## Hugo Architecture & Configuration

### Front Matter Format
All posts use TOML front matter (delimited by `+++`):
```toml
+++
title = 'Your Post Title'
date = 2025-09-08T14:30:00-05:00
draft = false
tags = ["BigQuery", "Data Architecture", "GCP"]
categories = ["Technical Deep-Dive", "Architecture"]
description = "Brief description for SEO and social sharing"
+++

Your markdown content here...
```

**IMPORTANT:** This site uses TOML format (+++), NOT YAML (---).

### Site Configuration (config/_default/config.toml)
```toml
baseURL = "https://jeremylongshore.com/"
theme = "hugo-bearblog"
title = "Jeremy Longshore"
languageCode = "en-US"

[params]
  description = "AI engineering, software, and startup notes."

[menu]
  [[menu.main]]
    name = "Posts"      # weight = 10
  [[menu.main]]
    name = "About"      # weight = 20
  [[menu.main]]
    name = "Projects"   # weight = 25
  [[menu.main]]
    name = "Contact"    # weight = 30

[permalinks]
  posts = "/posts/:slug/"

[markup.goldmark.renderer]
  unsafe = true  # Allow raw HTML in markdown
```

### Content Sync from Start AI Tools
Automated RSS feed synchronization pulls content from startaitools.com:

**Python script** (`scripts/sync-startaitools.py`):
- Fetches RSS feed from https://startaitools.com/index.xml
- Downloads and localizes images to `static/images/startai/`
- Converts HTML to markdown while preserving code blocks
- Writes posts to `content/posts/startai/` with TOML front matter
- **Dependencies:** `requests`, `beautifulsoup4`

**GitHub Actions** (`.github/workflows/sync-startaitools.yml`):
- Runs daily at 06:17 UTC
- Can be manually triggered via workflow_dispatch
- Auto-commits changes if new content detected

## Deployment & Netlify Configuration

**Hosting:** Netlify with automatic deployments on push to main branch

**Build Configuration** (netlify.toml):
```toml
[build]
  command = "hugo --gc --minify --cleanDestinationDir"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.150.0"
  HUGO_ENABLEGITINFO = "true"
  HUGO_ENV = "production"
  NODE_VERSION = "18"
  TZ = "America/Chicago"

[[redirects]]
  from = "http://jeremylongshore.com/*"
  to = "https://jeremylongshore.com/:splat"
  status = 301
  force = true  # HTTP → HTTPS redirect
```

**Deployment workflow:**
1. Edit/create content in `content/posts/`
2. Test locally with `hugo server -D`
3. Commit and push to main branch
4. Netlify auto-builds and deploys (typically < 2 minutes)
5. Daily automated sync from Start AI Tools at 06:17 UTC

## Theme: hugo-bearblog

**Active theme:** hugo-bearblog (Git submodule at `themes/hugo-bearblog/`)

**Design philosophy:**
- Minimal, fast, accessible
- Clean typography with no JavaScript dependencies
- Focused on content readability
- Responsive design

**Customization approach:**
- Override layouts by creating files in `layouts/` directory
- Hugo will use local layouts over theme layouts
- Never edit theme files directly (Git submodule)

**Navigation menu:** 4-item menu configured in config.toml:
- Posts (weight 10)
- About (weight 20)
- Projects (weight 25)
- Contact (weight 30)

## Content Topics & Categories

**Recent focus (Oct 2025):**
- **Production Engineering:** CI/CD pipelines, debugging case studies, testing infrastructure (Playwright)
- **Claude Code Development:** Plugin marketplace, Skills Powerkit, automation workflows
- **Cloud Infrastructure:** Google Cloud Platform (Vertex AI, BigQuery, Firestore, Cloud Functions)
- **Enterprise Systems:** Marketplace schema validation, legal compliance, production deployments

**Ongoing technical coverage:**
- **Data Engineering:** BigQuery schemas (266 tables), data pipelines, RSS feed validation (226+ feeds)
- **AI Automation:** N8N workflows, Google Vertex AI Gemini, multi-agent systems
- **Developer Productivity:** Custom AI commands, workflow automation, rapid deployment (days not months)
- **Project Case Studies:** DiagnosticPro ($500K+ revenue), Claude Code Plugins (227 plugins), Waygate MCP

**Personal background (reflected in About page):**
- 20+ years restaurant operations → self-taught developer → AI automation specialist
- Marine Corps Reservist, The Citadel graduate
- Based in Gulf Shores, Alabama
- Company: Intent Solutions (intentsolutions.io)

## Critical Development Rules

1. **Never edit `public/` directory** - It's auto-generated and will be overwritten on every build
2. **Use TOML front matter** - This site uses `+++` delimiters, NOT `---` (YAML)
3. **Test locally before committing** - Run `hugo server -D` to preview changes
4. **Theme is Git submodule** - Never modify files in `themes/hugo-bearblog/` directly
5. **Images for synced content** - Automatically downloaded to `static/images/startai/` by sync script
6. **Hugo version locked** - Site uses Hugo v0.150.0 (defined in netlify.toml)

## Common Development Tasks

### Creating a New Blog Post
```bash
# Generate new post with proper front matter
hugo new posts/my-new-post.md

# Edit the file (opens in default editor)
# Set draft = false when ready to publish
# Commit and push to deploy
```

### Testing Content Sync
```bash
# Install Python dependencies
pip install requests beautifulsoup4

# Run sync script manually
python scripts/sync-startaitools.py

# Check for new content in content/posts/startai/
# Check for new images in static/images/startai/
```

### Previewing Production Build
```bash
# Build exactly as Netlify does
hugo --gc --minify --cleanDestinationDir

# Serve the built site
cd public && python -m http.server 8000
# Visit http://localhost:8000
```

### Updating Theme
```bash
# Update hugo-bearblog submodule to latest
cd themes/hugo-bearblog
git pull origin main
cd ../..
git add themes/hugo-bearblog
git commit -m "chore: update hugo-bearblog theme"
```

## Active GitHub Repositories (Oct 2025)

**Public Repositories (15 total):**
- `claude-code-plugins-plus` - 227 plugins hub, most actively developed (updated Oct 19)
- `startaitools.com` - AI tools directory with tutorials (Hugo + Jupyter notebooks)
- `jeremylongshore.com` - This blog (Python sync scripts, Hugo)
- `bobs-brain` - Slack AI assistant with sovereign deployment
- `waygate-mcp` - Enterprise MCP server framework (Python 3.12, FastAPI, Docker)
- `local-rag-agent-intent-solutions` - Local RAG system with zero-cost deployment
- `ai-devops-intent-solutions` - AI-powered documentation generator (5-minute PRDs)
- `lead-followup-system-n8n` - B2B lead capture with AI scoring
- `gmail-drive-organizer-n8n` - Gmail attachment automation
- `disposable-marketplace-n8n` - Instant marketplace for quote collection
- `ai-blog-journalist-n8n` - Automated content using Perplexity + Claude
- `news-pipeline-n8n` - Daily news monitoring with AI analysis
- `n8n-workflow-template` - Professional N8N repo template
- `diagnosticpro-schema-sql` - SQL schemas (public subset)
- `Hybrid-ai-stack-intent-solutions` - 60-80% AI cost reduction

**Private Repositories:**
- `hustle` - Youth sports stats app (Next.js 15 + TypeScript + PostgreSQL)
- `DiagnosticPro` - Main diagnostic platform (TypeScript, Firebase, Vertex AI)
- `intent-solutions-landing` - Company landing page (TypeScript, React/Vite, Bun)
- `diagnostic-platform` - Data platform components (Python)
- `cost-plus-db` - Database work (HTML)
- Others: `plugins-Claude-code`, `claude-code-marketplace`, `prompts-intent-solutions`, `brainstorm-intent-solutions`, `daily-energizer-workflow-n8n`, `fix-it-detective-ai`, `diagnostic-pro-mvp3-legacy`

**Recent Activity Indicators:**
- Most active: `claude-code-plugins-plus` (daily commits)
- Regular updates: `startaitools.com`, `hustle`, `jeremylongshore.com`
- Stable/mature: `waygate-mcp`, `bobs-brain`, N8N workflow repos

## Technology Stack (Based on Active Projects)

**Primary Languages:**
- Python (AI agents, automation, data pipelines, MCP servers)
- TypeScript/JavaScript (React, Next.js 15, web applications)
- SQL (PostgreSQL, BigQuery)
- Shell scripting (automation, DevOps)

**Frontend Frameworks:**
- Next.js 15 (App Router, React 19)
- SvelteKit (DiagnosticPro)
- React 18/19 + Vite
- Hugo (static sites)

**Backend & Infrastructure:**
- Google Cloud Platform (Vertex AI Gemini, BigQuery, Firestore, Cloud Functions, Cloud Run)
- Firebase (Hosting, Functions, Firestore)
- Docker (containerization, MCP servers)
- FastAPI (Python APIs)
- PostgreSQL (Hustle, other apps)

**AI & Automation:**
- Google Vertex AI Gemini 2.5 Flash (primary)
- Claude API (Anthropic)
- N8N (workflow automation - 10+ production workflows)
- Ollama (local models)
- LangChain, RAG systems

**DevOps & Deployment:**
- Netlify (static sites, auto-deploy)
- Google Cloud Run (containerized services)
- GitHub Actions (CI/CD)
- Terraform (IaC for AWS/GCP)
- Nginx (reverse proxy)

## Important Context for AI Assistants

**Development Philosophy:**
- "Deploy in days, not months" - Rapid prototyping and iteration
- Practical solutions over theoretical perfection
- Working code over comprehensive documentation
- Business value over technical complexity

**Common Workflow:**
1. Build MVP in 24-72 hours
2. Deploy to production early
3. Iterate based on real usage
4. Document what actually works

**Writing Style in Blog Posts:**
- Direct, no-BS tone
- Focus on real numbers and outcomes
- Technical depth with practical application
- Case studies from actual projects

**Avoid When Writing Content:**
- Corporate buzzwords and fluff
- Theoretical concepts without implementation
- Over-promising or marketing speak
- Generic advice without specifics