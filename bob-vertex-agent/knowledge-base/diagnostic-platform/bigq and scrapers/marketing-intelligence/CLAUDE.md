# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a marketing intelligence extraction system designed for DiagnosticPro's $4.99 equipment diagnostic service. The system mines marketing strategies, customer discovery frameworks, and automation workflows from multiple data sources to support customer acquisition and retention.

## Project Architecture

The system follows a multi-agent architecture with specialized agents for different marketing intelligence tasks:

```
marketing-intelligence/
├── system/                    # Core system components
│   ├── agents/               # Specialized processing agents
│   │   ├── customer-discovery-agent.py      # Customer research & validation
│   │   ├── technical-marketing-agent.py     # B2B technical service marketing
│   │   ├── automation-agent.py              # N8N workflow automation
│   │   ├── x-twitter-agent.py              # Twitter/X social intelligence
│   │   └── x_token_refresh.py              # OAuth2 token management
│   ├── scripts/              # Data extraction engines
│   │   ├── marketing_miner.py              # GitHub repository mining
│   │   └── quality_filter.py               # Constitutional AI compliance
│   └── configs/              # Configuration standards
│       └── n8n_repo_standards.json        # N8N evaluation criteria
├── reports/                  # Generated intelligence reports
│   ├── final/               # Primary deliverables for review
│   ├── extraction_data/     # Raw API extraction results
│   └── agent_outputs/       # Processed agent results
└── marketing-intelligence/  # Nested project structure (legacy)
```

## Core Commands

### Data Extraction Pipeline
```bash
# Extract marketing intelligence from GitHub
cd system/scripts/
python3 marketing_miner.py

# Process with specialized agents
cd system/agents/
python3 customer-discovery-agent.py     # Customer research focus
python3 automation-agent.py             # N8N automation workflows
python3 technical-marketing-agent.py    # B2B technical strategies

# Refresh social media access tokens
python3 x_token_refresh.py              # OAuth2 token refresh
```

### Review Generated Intelligence
```bash
# Primary deliverable - start here
cat reports/final/FINAL_MARKETING_INTELLIGENCE_REPORT.json

# Actionable implementation strategies
cat reports/final/marketing_intelligence_actionable_report.json

# Raw extraction data
ls reports/extraction_data/marketing_intelligence_*.json
```

### Quality Assurance
```bash
# Apply constitutional AI filtering
cd system/scripts/
python3 quality_filter.py < input_data.json > filtered_output.json
```

## Agent Specializations

### Customer Discovery Agent
- **Purpose**: Validates target customer segments for DiagnosticPro
- **Focus**: Vehicle owners suspicious of repair quotes, equipment operators
- **Output**: Interview frameworks, customer validation scripts
- **Price Point**: $4.99 value proposition validation

### Technical Marketing Agent
- **Purpose**: B2B/SaaS marketing strategies for technical services
- **Focus**: Professional credibility, industry positioning
- **Output**: Content marketing, SEO optimization, authority building

### Automation Agent
- **Purpose**: N8N workflow automation for customer onboarding
- **Focus**: Payment processing, diagnostic delivery, email sequences
- **Output**: Complete automation pipelines, conversion optimization

### X/Twitter Agent
- **Purpose**: Social media intelligence extraction
- **Focus**: Viral marketing patterns, customer discovery discussions
- **Output**: Trending strategies, engagement patterns

## Data Sources & Rate Limits

### GitHub API
- **Status**: ✅ Operational
- **Rate Limit**: 5,000 requests/hour
- **Categories**: Customer discovery, automation, pricing strategies
- **Repository Standards**: Defined in `system/configs/n8n_repo_standards.json`

### Reddit PRAW
- **Status**: ✅ Configured
- **Rate Limit**: 60 requests/minute
- **Target Subreddits**: marketing, entrepreneur, smallbusiness, startups
- **Background Collection**: Continuous monitoring

### X/Twitter API v2
- **Status**: 🔄 Requires OAuth2 refresh
- **Rate Limit**: 300 requests/15min (search), 900 requests/15min (lookup)
- **Token Management**: `system/agents/x_token_refresh.py`

## Target Market Context

### Primary Customers
- Vehicle owners suspicious of mechanic quotes
- Fleet managers verifying repair recommendations
- Equipment operators (diesel skid steers, boats, RVs)
- Repair shop owners seeking second opinions

### Key Pain Points
- Mechanic trust issues and overcharging fears
- Technical knowledge gaps in equipment diagnosis
- Need for independent validation of expensive repairs

### Value Proposition
$4.99 professional diagnostic validation vs potential $100s-$1000s savings

## Implementation Priorities

### Ready-to-Implement Strategies (from reports/final/)

1. **Customer Discovery Framework** (2-4 hours)
   - Interview scripts for equipment owners
   - $4.99 value proposition validation
   - Customer segment refinement

2. **N8N Customer Onboarding Automation** (4-6 hours)
   - $4.99 payment → diagnostic → delivery workflow
   - 50% reduction in manual tasks
   - Scalable customer processing

3. **Lead Nurturing Email Sequence** (6-8 hours)
   - 5-email sequence over 30 days
   - Target repair quote anxiety
   - 15-25% conversion increase

## Configuration Files

### N8N Repository Standards
File: `system/configs/n8n_repo_standards.json`
- Evaluation criteria for N8N automation repositories
- Quality scoring (excellent: 90-100, good: 70-89, acceptable: 50-69)
- DiagnosticPro-specific requirements (Stripe integration, email automation)
- Implementation roadmap with phases and timeframes

### Environment Variables
Required for API access:
- `GITHUB_TOKEN`: GitHub API authentication
- `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`: Reddit PRAW credentials
- `X_BEARER_TOKEN`, `X_CLIENT_ID`, `X_CLIENT_SECRET`: Twitter/X API v2

## Quality Standards

### Constitutional AI Compliance
- All content filtered through `system/scripts/quality_filter.py`
- Anthropic prompt guidelines adherence
- Business-appropriate content validation
- No promotional or spam content

### Repository Evaluation
- Minimum 10 stars for consideration
- Active maintenance (updated within 12 months)
- Clear documentation and setup instructions
- Production-ready workflow examples

## Monitoring & Success Metrics

### Customer Discovery
- Interview completion rate: >80%
- Price sensitivity validation for $4.99
- Customer segment validation accuracy

### Automation Workflow
- Payment completion rate: >95%
- Email delivery rate: >98%
- Customer satisfaction: >4.5/5

### Lead Nurturing
- Email open rates: >25%
- Click-through rates: >5%
- Conversion improvement: 15-25%

## Development Notes

### Agent Architecture
Each agent inherits from a base class with DiagnosticPro context:
- Service: $4.99 equipment diagnostic validation
- Target customers: Predefined segments
- Pain points: Mechanic trust, technical gaps, validation needs
- Value proposition: Professional analysis to prevent repair scams

### Data Flow
1. **Extraction**: Scripts mine data from APIs (GitHub, Reddit, X/Twitter)
2. **Processing**: Specialized agents filter and categorize by marketing function
3. **Quality Assurance**: Constitutional AI filtering removes inappropriate content
4. **Output**: Actionable strategies in `reports/final/` for immediate implementation

### OAuth2 Token Management
X/Twitter integration requires periodic token refresh:
```bash
cd system/agents/
python3 x_token_refresh.py
```
Check token status in extraction reports before running X/Twitter agent.