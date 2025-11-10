# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Content Nuke is a **command-based content automation platform** that transforms single development sessions into published multi-platform content. Unlike traditional applications, this is an intelligent slash command system for Claude Code that generates platform-optimized content across blogs and social media with comprehensive analytics tracking.

## Architecture Overview

This is a **command-driven automation ecosystem** built around Claude Code slash commands. The system employs a content multiplication pattern where one development session generates four platform-optimized outputs:

### Core Components

**Command System (`content-nuke-claude/commands/`)**
- 14 specialized slash command definitions (.md files)
- Multi-platform content blast commands (`/content-nuke`)
- Single-platform commands (`/blog-single-startai`, `/blog-single-jeremy`)
- Platform templates (Hugo, Jekyll, Gatsby, Next.js, WordPress)
- Intelligence commands (`/intel-commands`, analytics dashboard)

**Automation Scripts (`content-nuke-claude/scripts/` + `scripts/`)**
- OAuth 1.0a and OAuth 2.0 authentication handlers
- X (Twitter) thread posting with auto-refresh tokens (`post_x_thread.py`)
- LinkedIn content generation and posting (`post_linkedin.py`)
- Token refresh automation (`refresh_tokens.py`)
- Waygate MCP integration for secure credential storage

**Documentation System (`content-nuke-claude/docs/`)**
- Platform setup guides for 5 supported blog platforms
- Complete X API OAuth 2.0 setup walkthrough
- LinkedIn API integration documentation
- Command customization guides

**Content Generation Architecture**
- Session analysis engine (git history + conversation context)
- Content adaptation engine (technical vs personal angles)
- **X-Gen-System**: Advanced X content optimization with MCP integration
- Intelligent link selection for cross-platform optimization
- Multi-platform deployment coordination

**X-Gen-System Integration (NEW)**
- **Character Budgeting**: 280-char limit with URL=23, emoji buffer calculations
- **Proven Hook Patterns**: Counter-intuitive, mini-case, list-promise, myth-bust templates
- **MCP Compliance**: 100% schema validation for direct API consumption
- **Accessibility Standards**: CamelCase hashtags, alt text requirements, ASCII-only
- **A/B Variant Generation**: Engagement optimization with hook/CTA variants
- **Error Handling**: Graceful fallback, auto-split algorithm, content recovery

### Command Categories

**Multi-Platform Commands**
- `/content-nuke` - Deploy content across ALL platforms (StartAITools + JeremyLongshore blogs + X thread + LinkedIn post)
- `/intel-commands` - Generate comprehensive command documentation with analytics

**Single-Platform Commands**
- `/blog-single-startai` - StartAITools technical blog + X thread
- `/blog-single-jeremy` - JeremyLongshore portfolio blog + X thread

**Platform Templates**
- Hugo, Jekyll, Gatsby, Next.js, WordPress automation templates
- Fully customizable for different blog platforms and deployment strategies

## Development Commands

### Command Installation & Setup

```bash
# Install all commands from this repository
cp content-nuke-claude/commands/*.md ~/.claude/commands/

# Verify installation - should show 14 command files
ls -la ~/.claude/commands/ | grep -E "(content-nuke|blog-|post-|intel)"

# Test command discovery
cd ~/projects/any-project
/content-nuke  # This should be recognized by Claude Code
```

### Available Commands

| Command | Purpose | Generates | Analytics |
|---------|---------|-----------|-----------|
| `/content-nuke` | **Multi-platform blast** | 4 pieces: StartAI blog + Jeremy blog + X thread + LinkedIn | ✅ Full |
| `/blog-single-startai` | Technical blog + X thread | StartAITools post + X thread | ✅ Tracked |
| `/blog-single-jeremy` | Personal blog + X thread | JeremyLongshore post + X thread | ✅ Tracked |
| `/intel-commands` | Command documentation | Analytics dashboard + usage stats | ✅ Meta |
| `/post-x` | X thread only | Standalone X thread | ✅ Social |

### Core Command Usage

```bash
# Multi-platform content deployment
/content-nuke
# Claude analyzes session → generates 4 content pieces → deploys to all platforms

# Command intelligence and documentation
/intel-commands
# Generates complete command bible with usage analytics

# Single platform deployments
/blog-single-startai    # Technical blog + X thread
/blog-single-jeremy     # Portfolio blog + X thread
```

### Social Media API Setup

**X (Twitter) API - OAuth 1.0a Authentication:**
```bash
# Environment variables for OAuth 1.0a (preferred)
export X_API_KEY="your_api_key_here"
export X_API_SECRET="your_api_secret_here"
export X_ACCESS_TOKEN="your_access_token_here"
export X_ACCESS_SECRET="your_access_secret_here"
```

**X (Twitter) API - OAuth 2.0 via Waygate MCP:**
```bash
# Uses credentials from waygate-mcp/.env automatically
# X_CLIENT_ID, X_CLIENT_SECRET, X_OAUTH2_ACCESS_TOKEN

# Test X API posting
python3 scripts/post_x_thread.py "Test tweet content"

# Post X thread from file
python3 scripts/post_x_thread.py x-threads/2025-09-28-example-nuclear-x3.txt
```

**LinkedIn API Setup:**
```bash
export LINKEDIN_CLIENT_ID="your_client_id"
export LINKEDIN_CLIENT_SECRET="your_client_secret"
export LINKEDIN_ACCESS_TOKEN="your_access_token"

# Test LinkedIn posting
python3 scripts/post_linkedin.py "Professional update content"
```

### Testing & Debugging

```bash
# Test individual automation scripts
python3 scripts/post_x_thread.py "Test tweet"
python3 scripts/post_linkedin.py "Test LinkedIn post"
python3 scripts/refresh_tokens.py x  # Refresh X tokens

# Validate command installation
ls ~/.claude/commands/ | wc -l  # Should show 14+ commands

# Test blog deployment paths
ls /home/jeremy/projects/blog/startaitools/content/posts/
ls /home/jeremy/projects/blog/jeremylongshore/content/posts/

# Verify output directories exist
mkdir -p x-threads x-posts  # Create if missing
```

## Key Content Generation Workflow

### The Content Nuke Process

1. **Session Analysis Engine**
   - Git history: Analyzes commits since last blog post dates
   - Conversation context: Reviews complete Claude Code session
   - Project files: Examines changes, TODOs, CLAUDE.md files
   - Cross-linking: Identifies related existing content for linking

2. **Content Adaptation Engine**
   - **Business Lead Generation Angle** (StartAITools + LinkedIn): Technical capabilities, architectural solutions
   - **Hiring Evaluation Angle** (JeremyLongshore + X): Problem-solving approach, professional competence
   - **Intelligent Link Selection**: Auto-selects most contextually relevant links based on session focus

3. **Multi-Platform Generation**
   - **StartAITools Blog**: Technical deep-dive (2000+ words, architecture focus)
   - **JeremyLongshore Blog**: Personal journey (1000+ words, learning focus)
   - **X Thread**: TL;DR format with personal insights (1-7 tweets, user-specified size)
   - **LinkedIn Post**: Professional achievement showcase (1200-1500 chars)

4. **Automated Deployment**
   - Blog platforms: Hugo build → Git commit → Push → Deploy
   - Social platforms: API posting with auto-refresh authentication
   - Analytics tracking: Performance monitoring across all platforms

### Content Output Structure

```
Content Nuke Deployment:
├── StartAITools Blog Post (Technical deep-dive)
├── JeremyLongshore Blog Post (Personal journey)
├── X Thread (Quick insights with TL;DR)
└── LinkedIn Post (Professional achievements)

Generated Files:
├── /home/jeremy/projects/blog/startaitools/content/posts/[slug].md
├── /home/jeremy/projects/blog/jeremylongshore/content/posts/[slug].md
├── /home/jeremy/projects/content-nuke/x-threads/YYYY-MM-DD-slug-nuclear-x[size].txt
└── /home/jeremy/projects/content-nuke/x-posts/YYYY-MM-DD-slug-linkedin.txt
```

## Platform Integrations

### Blog Platforms Supported
- **Hugo** - Static site generator with YAML/TOML front matter
- **Jekyll** - GitHub Pages compatible with Ruby-based builds
- **Gatsby** - React-based framework with GraphQL integration
- **Next.js** - App/Pages Router with MDX support
- **WordPress** - WP-CLI or REST API publishing

### Social Platforms
- **X (Twitter)** - Automated thread posting via OAuth 1.0a API
- **LinkedIn** - Manual posting with generated optimized content

### Analytics Integration
- **SQLite Database** - Local command execution and performance tracking
- **Cross-Platform Metrics** - Content performance across all platforms
- **Command Intelligence** - Usage patterns and optimization insights

## File Structure & Conventions

```
content-nuke/
├── TODO.md                    # Project task tracking
├── content-nuke-claude/       # Main command system
│   ├── README.md             # Complete documentation
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   ├── commands/             # Slash command definitions
│   │   ├── content-nuke.md   # Multi-platform deployment
│   │   ├── intel-commands.md # Command intelligence
│   │   ├── blog-*.md         # Platform-specific commands
│   │   └── post-x.md         # X thread commands
│   ├── docs/                 # Setup and API documentation
│   │   ├── X_API_SETUP.md    # Complete X API setup guide
│   │   ├── PLATFORM_SETUP.md # Blog platform setup
│   │   └── X_OAUTH_API_REFERENCE.md # X API reference
│   ├── scripts/              # Automation utilities
│   │   ├── post_x_thread.py  # X thread posting script
│   │   └── oauth2_pkce_setup.py # OAuth setup utility
│   └── examples/             # Usage examples and templates
├── x-threads/                # Generated X thread content
└── x-posts/                  # Generated X post content
```

## Command Customization

### Adapting Commands for Your Blog

1. **Copy template command:**
   ```bash
   cp ~/.claude/commands/blog-hugo-technical.md ~/.claude/commands/blog-myblog.md
   ```

2. **Update paths and configuration:**
   - Blog content directory paths
   - Build commands for your platform
   - Front matter format
   - Deployment process

3. **Platform-specific requirements:**
   - **Hugo:** Update config.toml/hugo.toml paths and build flags
   - **Jekyll:** Adjust _posts/ directory and bundle exec commands
   - **Gatsby:** Configure content/ directory and GraphQL schema
   - **Next.js:** Set App/Pages Router paths and MDX configuration
   - **WordPress:** Configure WP-CLI or REST API authentication

## Security & Authentication

### X API Security
- Never commit API credentials to git
- Use environment variables only
- Regenerate tokens if accidentally exposed
- Monitor usage in X Developer Portal

### Blog Authentication
- SSH keys for git repository access
- Platform-specific authentication (GitHub, Netlify, etc.)
- WordPress application passwords for REST API

## Analytics & Intelligence

### Command Tracking
- Every command execution automatically tracked in SQLite database
- Success rates, execution times, parameter usage
- Content analytics: word counts, character counts, engagement metrics
- Monthly usage trends and effectiveness rankings

### Content Performance
- Cross-platform content performance tracking
- Blog post metrics and social media engagement
- Content ROI analysis and optimization insights

## Command Architecture & Customization

### Command Structure Patterns

All commands follow a consistent structure:
1. **Phase 1**: Session Analysis (git history + conversation context)
2. **Phase 2**: Content Strategy (audience-specific angles)
3. **Phase 3**: User Input (thread size, link preferences)
4. **Phase 4**: Content Generation (platform-optimized outputs)
5. **Phase 5**: Review & Approval (show complete package)
6. **Phase 6**: Deployment (automated publishing + analytics)

### Platform-Specific Customization

**Hugo Commands** (`blog-*-technical.md` templates):
- Front matter: YAML format with tags, categories, date
- Build command: `hugo --gc --minify --cleanDestinationDir`
- Deploy: Git commit → push → auto-deploy (Netlify/Vercel)

**Jekyll Commands**:
- Front matter: YAML with Jekyll-specific fields
- Build: `bundle exec jekyll build`
- Deploy: Git push to GitHub Pages

**WordPress Commands**:
- WP-CLI integration: `wp post create --post_status=publish`
- REST API fallback for hosted WordPress
- Category and tag management

### Authentication Patterns

**Dual OAuth Support** (X/Twitter):
- OAuth 1.0a: Full environment variables (X_API_KEY, X_API_SECRET, etc.)
- OAuth 2.0: Waygate MCP integration with auto-refresh tokens
- Fallback hierarchy: OAuth 1.0a → OAuth 2.0 → Error

**Credential Storage**:
- Environment variables (development)
- Waygate MCP `.env` integration (production)
- Never commit credentials to git

## Best Practices

### Content Strategy
- Use `/content-nuke` for major development sessions with substantial content potential
- Use `/blog-single-*` commands for quick updates or platform-specific content
- Always review generated content before deployment
- Maintain consistent voice across different platforms
- Cross-link related content for SEO and user engagement

### Operational Security
- Test commands in non-production projects first
- Verify blog build processes before deploying
- Monitor API rate limits for social platforms
- Use token refresh automation for long-running sessions
- Keep credentials in secure environment variables only

### Command Development
- Follow existing 6-phase command structure
- Include platform-specific customization instructions
- Test with Claude Code in development environment
- Document authentication requirements clearly
- Implement graceful error handling and retry logic

## Support & Documentation

- **Main Documentation:** [content-nuke-claude/README.md](content-nuke-claude/README.md)
- **X API Setup:** [docs/X_API_SETUP.md](content-nuke-claude/docs/X_API_SETUP.md)
- **Platform Setup:** [docs/PLATFORM_SETUP.md](content-nuke-claude/docs/PLATFORM_SETUP.md)
- **Contributing:** [CONTRIBUTING.md](content-nuke-claude/CONTRIBUTING.md)

---

# 📝 End-of-Day Report
**Date:** 2025-09-28
**Repo:** content-nuke
**Branch:** chore/eod-2025-09-28

---

## ✅ Status Summary
- Current branch: chore/eod-2025-09-28
- CI status: N/A (no CI configured yet)
- Tests: ⚠️ No tests detected (Python syntax validation passed)
- Version: 1.0.0 → 1.0.1 (PATCH bump)

---

## 📊 Work Completed
- ✅ Performed comprehensive end-of-day repository sweep
- ✅ Executed automated project type detection (Python project identified)
- ✅ Validated Python syntax across all .py files
- ✅ Performed repository hygiene cleanup (already clean)
- ✅ Analyzed version management and bumped 1.0.0 → 1.0.1
- ✅ Created CHANGELOG.md with full project history
- ✅ Updated end-of-day documentation

---

## 🧩 Issues Found
- ⚠️ No automated test suite detected
- 📝 TODO: Add unit tests for Python scripts
- 📝 TODO: Set up CI/CD pipeline for automated testing

---

## 🚀 Next Steps (Tomorrow)
1. Create comprehensive test suite for automation scripts
2. Set up GitHub Actions CI/CD pipeline
3. Test all 14 slash commands in production environment
4. Add error handling and retry logic to posting scripts
5. Create command usage analytics dashboard

---

## 🔗 PR / Commit Reference
- Branch: chore/eod-2025-09-28
- Version bump: 1.0.0 → 1.0.1 (documentation update)
- CHANGELOG.md: Created with full project history

---

**Project Status:** Production-ready content automation system
**Repository Status:** ✅ Clean and version-bumped
**Last Updated:** September 28, 2025
**Version:** v1.0.1