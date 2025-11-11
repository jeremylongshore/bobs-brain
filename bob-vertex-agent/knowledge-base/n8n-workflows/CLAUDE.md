# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Multi-project N8N workflow repository containing production-ready automation workflows for content generation, news intelligence, marketplace creation, and lead management. Each workflow operates independently with its own documentation and deployment requirements.

## Repository Structure

```
n8n-workflows/
├── deployed/                           # Production workflows
│   ├── daily-energizer-workflow/      # Daily inspirational article generator
│   ├── news-pipeline-n8n/             # Tech/AI news intelligence pipeline
│   └── n8n-vm-starter-repo/           # N8N VM setup and invoice extraction
├── disposable-marketplace-n8n/         # Instant marketplace creation workflow
├── raw/                                # Raw/unorganized workflow exports
├── n8n/                                # N8N setup guides and templates
└── *.json                              # Individual workflow files (root level)
```

## Main Workflows

### 1. Daily Energizer (Production)
**Location**: `deployed/daily-energizer-workflow/`
**Status**: V4 in production
**Purpose**: Generate daily inspirational articles from positive news RSS feeds

**Key Features**:
- 4-layer anti-hallucination system
- 10 curated positive news RSS feeds
- AI story scoring and selection (GPT-4o-mini, temperature 0)
- Automated image generation and Google Sheets integration
- 48-hour freshness filtering

**Files**:
- `The Daily Energizer Article and Image Generator V4.json` (Current)
- `The Daily Energizer Article and Image Generator V3.json` (Stable fallback)

**See**: `deployed/daily-energizer-workflow/CLAUDE.md` for complete details

### 2. News Pipeline (Production)
**Location**: `deployed/news-pipeline-n8n/`
**Status**: v2.1.1 in production
**Purpose**: Enterprise news intelligence with AI analysis

**Key Features**:
- 12 premium tech/AI RSS sources
- Airtable integration for team collaboration
- GPT-4o-mini structured analysis (10KB+ prompts)
- Daily automated execution (8:01 AM)
- 70-85% topic relevance accuracy

**Files**:
- `workflows/tech-news-tracker.json` (15 nodes, 35KB)
- `rss-feeds/tech-ai-feeds.json` (12 sources)
- `rss-feeds/comprehensive-news-feeds.json` (45+ sources)

**See**: `deployed/news-pipeline-n8n/CLAUDE.md` for complete details

### 3. Disposable Marketplace (Production)
**Location**: `disposable-marketplace-n8n/`
**Status**: Production ready
**Purpose**: Instant marketplace creation for quote collection

**Key Features**:
- CSV-based reseller management
- Dual outreach (email + API)
- Automated ranking system
- Webhook endpoints for offer collection
- Google Sheets tracking

**Files**:
- `workflow.json` (15KB workflow)
- `example-resellers.csv` (Sample data structure)
- `test-requests.sh` (API testing script)

**See**: `disposable-marketplace-n8n/CLAUDE.md` for complete details

### 4. Root-Level Workflows
**Location**: Repository root
**Status**: Various (development/testing)

**Files**:
- `AI Lead Follow-Up System - updated.json` (86KB)
- `AI_Blog_Post_Journalist.json` (13.7KB)
- `Day4_Organize_Email_Attachments_from_Gmail_to_Structured_Google_Drive_Folders.json` (6KB)

## Common N8N Commands

### Workflow Management
```bash
# Import workflow into N8N instance
n8n import:workflow --input="path/to/workflow.json"

# Execute workflow manually (requires workflow ID)
n8n execute --id=[workflow-id]

# Export workflow (for version control)
n8n export:workflow --id=[workflow-id] --output="path/to/workflow.json"

# Export all workflows
docker exec -ti n8n n8n export:workflow --output=/home/node/.n8n/exported

# Import from JSON (in container)
docker exec -ti n8n n8n import:workflow --input=/home/node/.n8n/myworkflow.json
```

### Validation & Testing
```bash
# Validate JSON structure
jq . "workflow.json" > /dev/null && echo "Valid JSON"

# Test RSS feed availability
curl -s "https://example.com/feed/" | head -20

# Create backup before changes
cp "workflow.json" "backup-$(date +%Y%m%d).json"
```

### REST API Management
```bash
# List all workflows
curl -H "Authorization: Bearer $N8N_API_KEY" \
     https://n8n.yourdomain.com/rest/workflows

# Update workflow via API
curl -X PUT -H "Authorization: Bearer $N8N_API_KEY" \
     -H "Content-Type: application/json" \
     -d @workflow.json \
     https://n8n.yourdomain.com/rest/workflows/12
```

## N8N Development Patterns

### Node Variable Syntax (Critical)
```javascript
// CORRECT - Always use N8N built-in helpers
const stories = $input.first().json.stories;
const allItems = $input.all();
const currentData = $json;

// INCORRECT - Will cause undefined variable errors
const stories = items[0].json.stories;  // DO NOT USE
const data = items.json;                 // DO NOT USE
```

### Version Control Workflow
1. **Design in N8N UI** - Use visual editor for complex workflows
2. **Export to Git** - Save workflow JSON to repository
3. **Review & Edit** - Team review via pull requests
4. **Import via CLI/API** - Deploy to production N8N instance

### Best Practices
- Use **temperature: 0** for LLM nodes requiring deterministic output
- Implement **error handling** with N8N's error workflows
- Add **wait nodes** between API calls to respect rate limits
- Use **environment variables** for credentials (never hardcode)
- Test workflows in **development environment** before production deployment

## Working with Workflows

### Navigating Projects
Each major workflow has its own subdirectory with complete documentation:

```bash
# Daily Energizer (production content generation)
cd deployed/daily-energizer-workflow/
cat CLAUDE.md  # Full technical specs

# News Pipeline (production intelligence)
cd deployed/news-pipeline-n8n/
cat CLAUDE.md  # Integration details

# Disposable Marketplace (production marketplace)
cd disposable-marketplace-n8n/
cat CLAUDE.md  # API documentation
```

### Making Changes to Workflows
1. **Identify the workflow** - Check which subdirectory or root file
2. **Read project-specific CLAUDE.md** - Each has its own requirements
3. **Backup before editing** - `cp workflow.json backup-$(date +%Y%m%d).json`
4. **Validate after changes** - `jq . workflow.json > /dev/null`
5. **Test in N8N dev environment** - Never edit production directly
6. **Document changes** - Update relevant markdown files

### Common Validation Tasks
```bash
# Validate all JSON workflows in repository
find . -name "*.json" -type f -exec sh -c 'echo "Checking: $1" && jq . "$1" > /dev/null' _ {} \;

# Check for large workflow files (> 10KB indicates complex workflow)
find . -name "*.json" -size +10k -exec ls -lh {} \;

# Find all CLAUDE.md files (project-specific documentation)
find . -name "CLAUDE.md" -type f
```

## Setup & Configuration

### N8N Platform Requirements
- **N8N Version**: 1.110.1+ (Cloud or self-hosted)
- **Node.js**: 20+ (for Cloud Functions in some workflows)
- **Docker**: Optional (for containerized N8N instances)

### API Credentials Needed
Different workflows require different credentials:

**Daily Energizer**:
- OpenAI API key (GPT-4o-mini)
- Google Sheets API
- Google Drive API (image processing)

**News Pipeline**:
- Airtable Personal Access Token
- OpenRouter API key (GPT-4o-mini)
- NewsAPI key (optional)

**Disposable Marketplace**:
- SMTP credentials (email outreach)
- Google Sheets API
- N8N webhook access

### Environment Setup
```bash
# Set N8N API credentials (for CLI operations)
export N8N_API_KEY="your-api-key-here"
export N8N_BASE_URL="https://n8n.yourdomain.com"

# Validate connectivity
curl -H "Authorization: Bearer $N8N_API_KEY" \
     $N8N_BASE_URL/rest/workflows
```

## N8N Guides & Templates

The `n8n/` directory contains setup guides and best practices:

- **`cli-workflow-management-guide.md`** - CLI commands and REST API usage
- **`setup-guide-best-practices.md`** - Production setup recommendations
- **`self-host-setup-prompt.md`** - Self-hosting deployment guide
- **`n8n-repo-factory-template.md`** - Repository structure template
- **`enterprise-governance-guardrails.md`** - Enterprise compliance patterns

## Troubleshooting

### Common Issues Across Workflows

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "Referenced node doesn't exist" | Node connections broken | Use `$input.first()` syntax, verify connections |
| JSON parsing errors | Invalid workflow JSON | Run `jq . workflow.json` to validate |
| API authentication failures | Expired/invalid credentials | Verify API keys in N8N credentials manager |
| Workflow timeouts | Long processing times | Add wait nodes, increase timeout settings |
| Rate limit errors | Too many API calls | Implement delays between requests |

### Project-Specific Issues
- **Daily Energizer**: See `deployed/daily-energizer-workflow/CLAUDE.md` - Anti-hallucination system issues
- **News Pipeline**: See `deployed/news-pipeline-n8n/CLAUDE.md` - Airtable integration issues
- **Disposable Marketplace**: See `disposable-marketplace-n8n/CLAUDE.md` - Webhook configuration issues

## Project-Specific Documentation

Each workflow maintains its own comprehensive documentation:

| Workflow | Location | Key Docs |
|----------|----------|----------|
| Daily Energizer | `deployed/daily-energizer-workflow/` | CLAUDE.md, IMPLEMENTATION-GUIDE.md, FEATURE-UPDATES-SUMMARY.md |
| News Pipeline | `deployed/news-pipeline-n8n/` | CLAUDE.md, README.md, CHANGELOG.md |
| Disposable Marketplace | `disposable-marketplace-n8n/` | CLAUDE.md, README.md, SECURITY.md |

Always check project-specific CLAUDE.md files for detailed architecture, critical rules, and workflow-specific requirements.