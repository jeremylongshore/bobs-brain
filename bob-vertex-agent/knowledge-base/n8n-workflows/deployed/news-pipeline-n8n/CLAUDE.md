# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**News Pipeline N8N** - Enterprise-grade automated news intelligence workflow with AI-powered analysis for tech/AI content monitoring.

A production N8N workflow that collects news from 12 premium tech/AI sources, uses GPT-4o-mini to analyze and categorize content, then delivers structured intelligence to Airtable for business intelligence and competitive analysis.

## Repository Structure

```
news-pipeline-n8n/
├── workflows/
│   └── tech-news-tracker.json    # Main N8N workflow (15 nodes, 35KB)
├── rss-feeds/
│   ├── tech-ai-feeds.json        # Curated tech/AI RSS sources (12 premium feeds)
│   └── comprehensive-news-feeds.json  # Extended feed collection (45+ feeds)
├── docs/
│   ├── index.html                # GitHub Pages documentation site
│   └── workflow-analysis.html    # Technical workflow analysis
├── README.md                     # Comprehensive user documentation
├── CHANGELOG.md                  # Version history and releases
└── ANALYSIS_SUMMARY.md           # Technical performance analysis
```

## Core Workflow Architecture

### N8N Workflow Components
- **Schedule Trigger**: Daily execution at 8:01 AM
- **Airtable Integration**:
  - Base ID: `app42MWoBdW4bj8Ba` ("News Pipeline Base")
  - Topics Table: `tbl0UGDeOm5zulwqA` ("Topics to Monitor")
  - Articles Table: `tblil2WC8McQ9MPmQ` ("Articles Table")
- **RSS Collection**: 12 parallel HTTP Request nodes for tech/AI sources
- **AI Processing**: LangChain LLM node with GPT-4o-mini (10KB+ prompts)
- **Data Storage**: Structured Airtable output with 25+ metadata fields

### RSS Sources Configuration
The workflow focuses on 12 premium tech/AI news sources from `rss-feeds/tech-ai-feeds.json`:
- **Core Tech**: TechCrunch, The Verge, Ars Technica, VentureBeat
- **AI Research**: OpenAI Blog, Google AI Blog, Anthropic Blog, Hugging Face Blog
- **Developer/Business**: Hacker News, MIT Technology Review, Bloomberg Technology

### AI Analysis Pipeline
- **Model**: OpenRouter GPT-4o-mini
- **Temperature**: 0.2 (consistent output)
- **Processing**: 10,160-character prompts for structured analysis
- **Output**: JSON with topic tags, significance scores, entity extraction
- **Categories**: 35 tech-specific topic categories

## Common Development Commands

### N8N Workflow Management
```bash
# Import workflow into N8N
n8n import:workflow --input="workflows/tech-news-tracker.json"

# Export updated workflow
n8n export:workflow --id=[workflow-id] --output="workflows/tech-news-tracker.json"

# Validate JSON structure
jq . "workflows/tech-news-tracker.json" > /dev/null && echo "Valid JSON"
```

### RSS Feed Testing
```bash
# Test RSS feed availability
curl -s "https://techcrunch.com/feed/" | head -20

# Validate RSS feed JSON configuration
jq . "rss-feeds/tech-ai-feeds.json" > /dev/null && echo "Valid JSON"
```

### Documentation Deployment
The project uses GitHub Pages for documentation:
- **Site**: https://jeremylongshore.github.io/news-pipeline-n8n/
- **Source**: `docs/index.html` (automatically deployed on push to main)

## Workflow Configuration

### Required API Credentials
Set up these credentials in N8N:
- **Airtable Personal Access Token**: For base/table access
- **OpenRouter API Key**: For GPT-4o-mini processing
- **NewsAPI Key**: For additional news source coverage (optional)

### Critical Configuration Points
1. **Airtable Base/Table IDs**: Hard-coded in workflow nodes
2. **Schedule Timing**: 8:01 AM daily execution
3. **RSS Source URLs**: Defined in individual HTTP Request nodes
4. **AI Prompt**: 10KB+ prompt in LangChain LLM node
5. **Topic Keywords**: Managed dynamically in Airtable "Topics to Monitor" table

### Performance Specifications
- **Processing Time**: 2-3 minutes for 100-300 articles
- **Success Rate**: 99.2% workflow reliability
- **Match Accuracy**: 70-85% topic relevance (improved from 30% in v1.0)
- **Daily Volume**: 100-300 tech articles processed
- **Resource Usage**: ~50MB memory, 100-200 execution credits per run

## Development Workflow

### Making Changes to the Workflow
1. **Export current workflow** from N8N as backup
2. **Modify nodes** in N8N editor interface
3. **Test execution** with "Execute Workflow" button
4. **Verify Airtable output** for data quality
5. **Export updated workflow** to `workflows/tech-news-tracker.json`
6. **Commit changes** with descriptive message

### Adding New RSS Sources
1. **Add source** to `rss-feeds/tech-ai-feeds.json`
2. **Create new HTTP Request node** in N8N workflow
3. **Connect to "Merge Articles" node**
4. **Test execution** to verify data flow
5. **Update documentation** if needed

### Modifying AI Analysis
The AI prompt can be customized in the "Basic LLM Chain" node:
- **Topic tags**: Adjust for specific industry needs
- **Significance criteria**: Modify 1-5 rating system
- **Status categories**: Change development status types
- **Entity extraction**: Add custom entity types

### Topic Management
Topics are managed dynamically through Airtable:
- **Add topics**: Insert comma-separated keywords in "Topics to Monitor" table
- **Remove topics**: Delete rows from Airtable
- **Workflow pickup**: Changes detected on next scheduled run
- **Broad terms recommended**: Use general keywords for maximum coverage

## Troubleshooting

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| No articles collected | API credentials or RSS URLs | Check N8N credentials, verify RSS feed URLs |
| AI processing fails | OpenRouter credits/prompt format | Verify API credits, check prompt structure |
| Airtable errors | Base/table IDs or permissions | Verify IDs match, check token permissions |
| Workflow timeouts | Large article batches | Add delays, reduce batch sizes |
| Rate limiting | Too many API calls | Increase wait times between requests |

### Validation Commands
```bash
# Validate workflow JSON
jq . workflows/tech-news-tracker.json

# Check RSS feed status
curl -I https://techcrunch.com/feed/

# Verify Airtable base access (with token)
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://api.airtable.com/v0/app42MWoBdW4bj8Ba/tbl0UGDeOm5zulwqA"
```

### Debug Mode
Enable console logging in N8N Code nodes:
```javascript
console.log('Articles processed:', articles.length);
console.log('Topics matched:', matchedTopics);
console.log('AI response:', aiResponse);
```
View output in N8N execution history panel.

## Data Flow Architecture

### Processing Pipeline
1. **Schedule Trigger** → Daily execution at 8:01 AM
2. **Airtable Topics Fetch** → Retrieve monitoring keywords
3. **RSS Collection** → Parallel gathering from 12 sources
4. **Content Merging** → Combine all articles with 10-second delay
5. **JavaScript Processing** → Filter and match topics
6. **AI Analysis** → GPT-4o-mini structured analysis
7. **Data Enrichment** → Add metadata (25+ fields)
8. **Airtable Storage** → Structured output for team access

### Article Metadata Structure
Each processed article includes:
- **Core Data**: title, description, URL, source, author, publication date
- **AI Analysis**: summary, topic tags, significance score, development status
- **Processing Info**: workflow ID, execution ID, quality score, manual review flag
- **Business Intelligence**: key entities, competitive analysis, trend indicators

## Version Control

### Current Version: 2.1.1
- **Focus**: Tech/AI news sources (improved from general news)
- **Performance**: 70-85% relevance accuracy (up from 30%)
- **Documentation**: Comprehensive README and GitHub Pages site
- **Integration**: X/Twitter posting via Waygate MCP OAuth 2.0

### Release Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Changelog**: Detailed in CHANGELOG.md
- **GitHub Releases**: Tagged releases with comprehensive notes
- **Documentation**: Updated with each version

## Integration Points

### External Services
- **N8N Platform**: Workflow execution environment (v1.110.1+)
- **Airtable**: Data storage and team collaboration
- **OpenRouter**: AI processing (GPT-4o-mini)
- **RSS Feeds**: 12 premium tech/AI news sources
- **GitHub Pages**: Documentation hosting

### API Rate Limits
- **RSS Feeds**: No limits, 10-second delays for respectful polling
- **OpenRouter**: Per-token billing, ~300 tokens per article
- **Airtable**: 5 requests/second, handled by N8N wait nodes
- **NewsAPI**: 1,000 requests/day (optional source)

---

**Last Updated**: 2025-09-30
**Status**: Production ready with enterprise-grade documentation and social media integration