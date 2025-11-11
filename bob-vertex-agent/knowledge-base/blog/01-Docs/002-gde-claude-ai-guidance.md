# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site portfolio and blog using the hugo-bearblog theme. The site serves as a professional portfolio for Jeremy Longshore, an AI Engineer & Speed DevOps Specialist, featuring technical blog posts and project showcases. The site documents DiagnosticPro platform work with 254+ BigQuery tables, 226+ RSS feeds, and enterprise-scale data processing.

## Key Commands

### Local Development
```bash
# Start local development server with live reload
hugo server -D  # -D flag includes draft posts

# Start server without drafts
hugo server

# Start server accessible from external devices
hugo server -D --bind 0.0.0.0
```

### Building the Site
```bash
# Build static site to public/ directory
hugo

# Build including drafts
hugo -D
```

### Content Management
```bash
# Create a new blog post (primary location)
hugo new posts/my-new-post.md

# Create static pages
hugo new about.md
hugo new contact.md
```

### Content Synchronization
```bash
# Sync selected content from Start AI Tools blog (Python script)
python scripts/sync-startaitools.py

# Sync selected content from Start AI Tools blog (Bash script)
./scripts/sync-startaitools.sh
```

### Automated Content Sync
GitHub Actions automatically syncs Start AI Tools content daily at 06:17 UTC via `.github/workflows/sync-startaitools.yml`

## Project Structure

The site follows Hugo conventions with clean content structure and hugo-bearblog theme:

- **content/posts/** - Primary blog posts location (12+ published posts)
- **content/en/blogs/** - Legacy blog structure (maintained for compatibility)
- **content/** - Main static pages (_index.md, about.md, contact.md)
- **themes/hugo-bearblog/** - hugo-bearblog theme (Git submodule, clean minimal design)
- **themes/hermit-v2/** - Legacy Hermit v2 theme (available but not active)
- **static/** - Static assets (images, CSS, JS)
- **scripts/** - Content sync utilities (Python & Bash) for Start AI Tools integration
- **public/** - Generated static site (auto-generated, never edit directly)
- **hugo.toml** - Site configuration with simple 3-item menu (Posts, About, Contact)
- **netlify.toml** - Netlify deployment configuration (Hugo v0.149.1)
- **.github/workflows/** - Automated content sync from Start AI Tools

## Content Architecture

### Content Structure
The site uses a simplified content organization:
- **content/posts/** - Primary blog posts location (TOML front matter)
- **content/en/blogs/** - Legacy structure maintained for compatibility
- **content/posts/startai/** - Synced content from Start AI Tools

### Front Matter Format
Posts use TOML front matter format:
```toml
+++
title = 'Building a 254-Table BigQuery Schema in 72 Hours'
date = 2025-09-08T14:30:00-05:00
draft = false
tags = ["BigQuery", "Data Architecture", "Google Cloud Platform", "Python"]
categories = ["Technical Deep-Dive", "Architecture", "Cloud Computing"]
description = "Technical deep-dive into building enterprise data platform"
+++
```

### Content Sync Integration
Automated content synchronization from Start AI Tools:
- **Python script**: `scripts/sync-startaitools.py` (primary)
- **Bash script**: `scripts/sync-startaitools.sh` (legacy)
- **GitHub Actions**: Daily automated sync at 06:17 UTC
- **Target directory**: `content/posts/startai/`
- **Dependencies**: `requests`, `beautifulsoup4` for Python script

## Site Configuration

### Theme Setup (hugo-bearblog)
- **Active theme**: hugo-bearblog (minimal, fast, accessible)
- **Legacy theme**: hermit-v2 (available but not active)
- **Description**: "AI engineering, software, and startup notes."
- **Navigation**: 3-item menu (Posts, About, Contact)
- **Features**: Clean typography, fast loading, minimal design

### Content Features
- **Permalinks**: Posts use `/posts/:slug/` structure
- **Taxonomies**: Tags and categories enabled
- **Pagination**: 10 posts per page
- **Markup**: Goldmark with unsafe HTML enabled for rich content

### Technical Configuration
- **Base URL**: https://jeremylongshore.com/
- **Hugo version**: 0.149.1 (locked in netlify.toml)
- **Node version**: 18 (for build environment)
- **Timezone**: America/Chicago
- **Google Analytics**: Commented out (G-XXXXXXX placeholder)

## Deployment & Environment

### Netlify Configuration
- **Build command**: `hugo` (standard build)
- **Publish directory**: `public/`
- **Hugo version**: 0.149.1 (locked in netlify.toml)
- **Environment**: Production with HTTPS redirect
- **Domain**: jeremylongshore.com

### Development Workflow
1. Create content in `content/posts/` for new posts
2. Use `hugo server -D` for local preview with drafts
3. Commit changes triggers automatic Netlify deployment
4. Automated daily sync from Start AI Tools at 06:17 UTC

## Theme Architecture

### Current Theme (hugo-bearblog)
- **Theme location**: `themes/hugo-bearblog/` (Git submodule)
- **Design philosophy**: Minimal, fast, accessible
- **Customization**: Override layouts in `layouts/` directory if needed
- **Features**: Clean typography, fast loading, responsive design

### Legacy Theme (hermit-v2)
- **Status**: Available but not active in hugo.toml
- **Location**: `themes/hermit-v2/` (Git submodule)
- **Features**: Professional design with rich features

### Content Types
The site focuses on technical blog posts covering:
- **Data Engineering**: BigQuery, data pipelines, enterprise architecture
- **AI Engineering**: Machine learning, AI deployment, automation
- **Startup Tech**: Project case studies, development workflows
- **Personal Notes**: Development journey, technical exploration