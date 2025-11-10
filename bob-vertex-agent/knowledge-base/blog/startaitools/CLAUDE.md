# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Start AI Tools** is a Hugo-based business blog and educational platform documenting AI development projects, technical deep-dives, and real-world implementation guides. The site showcases Intent Solutions' work and serves as a knowledge center for AI engineering, data platform architecture, and DevOps automation.

- **Live Site**: https://startaitools.com
- **Theme**: Archie (professional business theme)
- **Deployment**: Netlify (auto-deploy on push to master)
- **Content**: 37+ technical blog posts, curriculum, project documentation

## Essential Commands

### Local Development
```bash
# Start development server (includes drafts)
hugo server -D

# Production preview (no drafts)
hugo server

# Accessible from external devices
hugo server -D --bind 0.0.0.0
```

### Building & Deployment
```bash
# Production build (used by Netlify)
hugo --gc --minify --cleanDestinationDir

# Standard build
hugo
```

### Content Creation
```bash
# Create new blog post
hugo new posts/my-new-post.md

# Create project page
hugo new projects/my-project.md
```

## Content Architecture

### Front Matter Format

**CRITICAL**: This site uses **TOML front matter** (not YAML):

```toml
+++
title = 'Your Post Title'
date = 2025-10-09T10:00:00-06:00
draft = false
tags = ["ai", "programming", "deployment"]
categories = ["Technical Deep-Dive"]
description = "Brief description for SEO and social media"
+++
```

**Note**: Delimiters are `+++` (TOML), NOT `---` (YAML).

### Content Structure
```
content/
├── posts/                          # Main blog posts (37+ published)
│   ├── *.md                        # Individual posts (TOML front matter)
│   └── startai/                    # Reserved for synced content
├── _index.md                       # Homepage
├── about.md                        # About page
├── contact.md                      # Contact page
├── projects.md                     # Projects showcase
├── research.md                     # Research & curriculum hub
├── agentic-design-patterns/        # Design pattern docs
├── mcp-for-beginners/              # MCP tutorial series
└── tiny-recursive-models/          # ML model documentation
```

### Permalink Structure
- Blog posts: `/posts/:slug/`
- Clean URLs without dates or categories

## Navigation Menu

6-item menu structure (defined in `config/_default/config.toml`):
1. **Home** - Landing page (/)
2. **Posts** - Blog archive (/posts/)
3. **About** - About Intent Solutions (/about/)
4. **Research & Curriculum** - Educational resources (/research/)
5. **Projects** - Active projects showcase (/projects/)
6. **Contact** - Contact information (/contact/)

## Theme & Customization

### Archie Theme
- **Location**: `themes/archie/` (Git submodule)
- **Design**: Professional business blog
- **Features**: Clean typography, syntax highlighting, responsive

### Hugo Book Theme
- **Location**: `themes/book/` (Git submodule)
- **Status**: Available for specific content sections (e.g., MCP tutorials)
- **Features**: Collapsible navigation, documentation-focused

### Customization Approach
- **DO NOT** modify theme files directly
- Override layouts in `layouts/` directory
- Custom CSS via `static/css/custom.css`
- Theme parameters in `config/_default/config.toml`

## Deployment Configuration

### Netlify Settings (netlify.toml)
```toml
[build]
  command = "hugo --gc --minify --cleanDestinationDir"
  publish = "public"

[build.environment]
  HUGO_VERSION = "0.150.0"
  NODE_VERSION = "18"
  TZ = "America/Chicago"
```

### Cache Control Strategy
Aggressive cache-busting for dynamic content:
- HTML pages: `no-cache, no-store, must-revalidate`
- Dynamic routes: `public, max-age=0, must-revalidate`
- Forces fresh content on every visit

### HTTPS Redirect
HTTP to HTTPS 301 redirect configured for all traffic.

## Critical Development Rules

1. **Never edit `public/`** - Auto-generated, will be overwritten
2. **Test locally first** - Always run `hugo server -D` before committing
3. **Use TOML front matter** - Not YAML (this is critical!)
4. **Respect theme structure** - Override in `layouts/`, don't modify themes
5. **Auto-deploy on push** - Commits to master trigger Netlify deployment
6. **Hugo version locked** - v0.150.0 in netlify.toml

## Content Categories & Tags

### Primary Content Topics
1. **Data Engineering** - BigQuery schemas, data pipelines, RSS validation
2. **AI Platforms** - DiagnosticPro, AI integration, deployment patterns
3. **DevOps Automation** - N8N workflows, GitHub Actions, CI/CD
4. **Documentation Systems** - Claude.md, directory standards, AI-assisted writing
5. **Real-World Debugging** - Technical deep-dives, problem-solving

### Tag Guidelines
Use specific, searchable tags:
- Technology: "BigQuery", "Hugo", "Python", "N8N"
- Concepts: "Data Architecture", "AI Engineering", "DevOps"
- Platforms: "Google Cloud Platform", "Netlify", "GitHub"

## Site Configuration

### Key Parameters (config/_default/config.toml)
```toml
baseURL = "https://startaitools.com/"
title = "Start AI Tools - Presented by Intent Solutions"
theme = "archie"

[params]
description = "Deploy AI solutions in days, not months"
```

### Markup Configuration
- **Renderer**: Goldmark with unsafe HTML enabled
- **Syntax Highlighting**: 'friendly' style, no line numbers
- **Code Fences**: Enabled with language support

## Testing Workflow

1. Navigate to project: `cd /home/jeremy/projects/blog/startaitools`
2. Start local server: `hugo server -D`
3. Verify content at `http://localhost:1313`
4. Test navigation, links, formatting
5. Build production: `hugo --gc --minify --cleanDestinationDir`
6. Verify `public/` directory generated correctly
7. Commit changes (triggers auto-deploy)

## Common Issues & Solutions

### Front Matter Errors
- **Problem**: "failed to unmarshal YAML"
- **Solution**: Ensure using TOML format (`+++`) not YAML (`---`)

### Theme Not Loading
- **Problem**: Theme files missing
- **Solution**: Initialize submodules: `git submodule update --init --recursive`

### Cache Issues
- **Problem**: Changes not visible on live site
- **Solution**: Cache headers force no-cache; clear browser cache or hard refresh

### Build Failures
- **Problem**: Hugo build fails on Netlify
- **Solution**: Check Hugo version compatibility (locked at 0.150.0)

## Performance Targets

- **Lighthouse Score**: 95+/100
- **Page Load**: < 2s
- **First Contentful Paint**: < 800ms
- **Time to Interactive**: < 1.5s

## Hugo Version & Dependencies

- **Hugo**: v0.150.0 (extended version)
- **Node.js**: v18 (build environment)
- **Themes**: Archie (primary), Book (documentation sections)
- **Timezone**: America/Chicago

## Related Projects

This site documents work from several interconnected projects:
- **DiagnosticPro** - AI diagnostic platform (diagnosticpro.io)
- **Intent Solutions** - AI consulting (intentsolutions.io)
- **Bob's Brain** - Slack AI assistant
- **Waygate MCP** - Security-hardened MCP server

## Contact & Support

- **Website**: https://startaitools.com
- **Email**: jeremy@intentsolutions.io
- **GitHub**: @jeremylongshore
- **LinkedIn**: Jeremy Longshore

---

**Last Updated**: 2025-10-09
**Hugo Version**: 0.150.0
**Theme**: Archie (professional business blog)
