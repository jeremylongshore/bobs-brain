# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Multi-blog project workspace containing **two Hugo static sites** plus social media content repositories.

### Hugo Static Sites
1. **jeremylongshore/** - Personal portfolio (jeremylongshore.com) - hugo-bearblog theme
2. **startaitools/** - Business blog (startaitools.com) - Archie theme

### Social Media Content
3. **linkedin-posts/** - LinkedIn content for Intent Solutions
4. **x-threads/** - X/Twitter threads and promotional posts

**⚠️ CRITICAL**: Always verify which site directory you're working in before making changes.

## Directory Structure

This project follows the master directory standards:

```
blog/
├── .directory-standards.md    # Master standards (local copy)
├── 01-Docs/                   # All project documentation (9 files)
├── 02-Src/                    # Source code (reserved for future use)
├── 03-Tests/                  # Test files (reserved for future use)
├── 04-Assets/                 # Shared assets (reserved for future use)
├── 05-Scripts/                # Automation scripts (reserved for future use)
├── 06-Infrastructure/         # Deployment configs (reserved for future use)
├── 07-Releases/               # Release artifacts (reserved for future use)
├── 99-Archive/                # Archived content (reserved for future use)
├── jeremylongshore/           # Hugo site #1 (DO NOT MODIFY STRUCTURE)
├── startaitools/              # Hugo site #2 (DO NOT MODIFY STRUCTURE)
├── linkedin-posts/            # Social media content (LEAVE IN PLACE)
└── x-threads/                 # Social media content (LEAVE IN PLACE)
```

## Documentation Organization

All documentation is centralized in `01-Docs/` with standardized naming:

1. **001-gde-blog-project-overview.md** - Original project README
2. **002-gde-claude-ai-guidance.md** - AI assistant guidance for Hugo sites
3. **003-gde-contributing-guidelines.md** - Contributing guidelines
4. **004-gde-gemini-ai-guidance.md** - Gemini AI guidance
5. **005-gde-github-setup-instructions.md** - GitHub setup instructions
6. **006-ref-release-history.md** - Release history and changelog
7. **007-rep-forensic-after-action-report.md** - Forensic after-action report
8. **008-rep-slash-command-fix-audit.md** - Slash command fix audit
9. **009-tpl-pull-request-template.md** - Pull request template

## Hugo Sites Configuration

### jeremylongshore/ - Personal Portfolio
- **URL**: https://jeremylongshore.com
- **Theme**: hugo-bearblog (minimal, accessible, no JavaScript)
- **Front Matter**: TOML format (`+++...+++`)
- **Content**: content/posts/ (69+ published posts)
- **Sync**: Automated daily sync from startaitools.com at 06:17 UTC → content/posts/startai/
- **Git**: Separate repo (github.com/jeremylongshore/My-Hugo-blog)

### startaitools/ - Business Blog
- **URL**: https://startaitools.com
- **Theme**: Archie (professional business theme)
- **Front Matter**: YAML format (`---...---`)
- **Content**: content/posts/ (37+ published posts), mcp-for-beginners/, research/
- **Features**: Pagefind search, custom CSS, cache-busting headers
- **Git**: Separate repo (github.com/jeremylongshore/startaitools.com)

**⚠️ KEY DIFFERENCE**: jeremylongshore uses TOML (`+++`), startaitools uses YAML (`---`)

## Common Development Commands

### Development Server
```bash
# jeremylongshore site
cd jeremylongshore/
hugo server -D                    # Include drafts
hugo server                       # Production-like preview
hugo server -D --bind 0.0.0.0     # Accessible from external devices

# startaitools site
cd startaitools/
hugo server -D                    # Include drafts
hugo server                       # Production-like preview
hugo server -D --bind 0.0.0.0     # Accessible from external devices
```

### Building Sites
```bash
# jeremylongshore
cd jeremylongshore/
hugo              # Standard build to public/

# startaitools
cd startaitools/
hugo --gc --minify --cleanDestinationDir  # Optimized production build
```

### Creating Content
```bash
# jeremylongshore - blog posts
cd jeremylongshore/
hugo new posts/my-post.md

# startaitools - blog posts
cd startaitools/
hugo new posts/my-article.md
hugo new tools/new-tool.md
```

## Critical Development Rules

1. **Verify Site Context**: Always confirm which site directory you're working in
2. **Never Edit public/**: These directories are auto-generated and will be overwritten
3. **Test Locally**: Always run `hugo server -D` to preview changes before committing
4. **Respect Themes**: Don't modify theme files directly; use layout overrides in layouts/
5. **Keep Sites Separate**: Don't mix content, configurations, or assets between sites
6. **Use Correct Front Matter**: jeremylongshore uses TOML (+++), startaitools uses YAML (---)
7. **Preserve Blog Content**: Blog content stays in Hugo site directories, only docs move to 01-Docs/

## Front Matter Formats (Critical)

### jeremylongshore - TOML (`+++`)
```toml
+++
title = 'Post Title'
date = 2025-10-25T10:00:00-05:00
draft = false
tags = ["ai", "programming"]
categories = ["Technical Deep-Dive"]
+++
```

### startaitools - YAML (`---`)
```yaml
---
title: "Post Title"
date: 2025-10-25T10:00:00-06:00
draft: false
tags: ["ai", "tools"]
categories: ["Technical Deep-Dive"]
description: "SEO description"
---
```

**Common mistake**: Using YAML format in jeremylongshore or TOML in startaitools will cause build failures.

## Deployment (Netlify)

Both sites auto-deploy on push to main:

| Setting | jeremylongshore | startaitools |
|---------|----------------|--------------|
| **Hugo Version** | 0.150.0 | 0.150.0 |
| **Build Command** | `git submodule update --init --recursive && hugo --gc --minify --cleanDestinationDir` | `hugo --gc --minify --cleanDestinationDir` |
| **Publish Dir** | public/ | public/ |
| **Node Version** | 18 | 18 |
| **Timezone** | America/Chicago | America/Chicago |
| **HTTPS Redirect** | ✅ (301) | ✅ (301) |
| **Cache Headers** | Default | Aggressive no-cache for HTML |

**Key difference**: jeremylongshore initializes Git submodules (for hugo-bearblog theme)

## Content Sync Automation

**jeremylongshore** automatically syncs content from **startaitools**:

### Automated Sync Process
- **Frequency**: Daily at 06:17 UTC via GitHub Actions
- **Source**: https://startaitools.com/index.xml (RSS feed)
- **Destination**: `jeremylongshore/content/posts/startai/`
- **Script**: `jeremylongshore/scripts/sync-startaitools.py`
- **Dependencies**: `requests`, `beautifulsoup4`
- **Image handling**: Downloads images to `static/images/startai/`

### Manual Sync
```bash
cd jeremylongshore/
pip install requests beautifulsoup4
python scripts/sync-startaitools.py
```

### GitHub Actions Workflow
- File: `.github/workflows/sync-startaitools.yml`
- Triggers: Daily scheduled + manual workflow_dispatch
- Auto-commits: Yes, if new content detected

## Social Media Content Workflow

### LinkedIn Posts (`linkedin-posts/`)
- **Purpose**: Formatted posts for Intent Solutions company LinkedIn page
- **Format**: Plain text with structured sections (content, hashtags, engagement strategy)
- **Naming**: `YYYY-MM-DD-topic-description-linkedin.txt`
- **Sections**: Post content, suggested hashtags, engagement strategy, metrics tracking

### X/Twitter Threads (`x-threads/`)
- **Purpose**: Tweet threads and promotional content for X/Twitter
- **Format**: Plain text (.txt) or markdown (.md)
- **Naming**: `YYYY-MM-DD-topic-description-x[N].txt` (N = thread number)
- **Content**: Multi-tweet threads with character count tracking for each tweet

## File Management Rules

1. **Documentation**: All documentation goes to `01-Docs/` with NNN-XXX-description.md naming
2. **Blog Content**: Stays in Hugo site directories (jeremylongshore/, startaitools/)
3. **Social Content**: Stays in original directories (linkedin-posts/, x-threads/)
4. **New Files**: Get explicit permission before creating any new files
5. **Existing Files**: Prefer editing over creating new files

## Testing Workflow

1. Navigate to the correct site directory
2. Run `hugo server -D` for local development
3. Test all functionality (navigation, links, content rendering)
4. Build with `hugo` to verify production output
5. Check public/ directory is generated correctly
6. Commit changes (auto-deploys to Netlify)

## Master Standards Reference

This project complies with master directory standards located at:
- `.directory-standards.md` (local copy)
- `/home/jeremy/projects/prompts-intent-solutions/000-master-systems/directory/MASTER-DIRECTORY-STANDARDS.md` (master)

## Project-Specific Documentation

For detailed Hugo site documentation, see:
- `01-Docs/002-gde-claude-ai-guidance.md` - Original Claude guidance for Hugo sites
- `01-Docs/001-gde-blog-project-overview.md` - Original project README

## Theme Management

Both sites use **Hugo v0.150.0** with Git submodule themes:

| Theme | jeremylongshore | startaitools |
|-------|----------------|--------------|
| **Name** | hugo-bearblog | Archie (+ Book for docs) |
| **Design** | Minimal, no JS | Professional business |
| **Navigation** | 4 items | 6 items |
| **Location** | themes/hugo-bearblog/ | themes/archie/, themes/book/ |
| **Customization** | Override in layouts/ | Custom CSS via config |

### Theme Best Practices
- **Never edit theme files directly** - they're Git submodules
- Override theme layouts by creating files in `layouts/` directory
- Update themes: `git submodule update --remote --merge`
- Both use Goldmark renderer with unsafe HTML enabled (for embedded content)
- Permalinks: `/posts/:slug/` (clean URLs without dates)

## Additional Resources

- **Individual site CLAUDE.md files**:
  - `jeremylongshore/CLAUDE.md` - Detailed jeremylongshore.com documentation
  - `startaitools/CLAUDE.md` - Detailed startaitools.com documentation
- **Centralized docs**: `01-Docs/` directory (10 documentation files)
- **Master directory standards**: `.directory-standards.md`
- **Deployment**: Both sites use Netlify with automatic deploys on push to main

---

**Last Updated**: 2025-10-25
**Hugo Version**: 0.150.0
**Status**: Active development, compliant with master directory standards
