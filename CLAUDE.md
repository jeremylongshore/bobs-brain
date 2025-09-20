# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bob's Brain is an AI-powered assistant ecosystem built with Google Gemini 2.5 Flash, Neo4j graph database, and enterprise-grade cloud infrastructure. It provides intelligent responses via Slack integration, persistent memory, and continuous learning capabilities.

## Architecture

### Core Components
- **Main Service**: `src/bob_brain_v5.py` - Flask app with Slack integration and AI processing
- **Data Collection**: `src/unified_scraper_*.py` - Web scrapers for knowledge aggregation
- **Learning System**: `src/circle_of_life.py` - ML pipeline for continuous improvement
- **Memory Layer**: Neo4j graph database + BigQuery analytics + Graphiti memory system

### Technology Stack
- **Runtime**: Python 3.11, Flask + Gunicorn
- **AI**: Google Gemini 2.5 Flash via Gen AI SDK
- **Databases**: Neo4j (graph), BigQuery (analytics), Datastore (MVP3 compatibility)
- **Deployment**: Google Cloud Run with VPC networking
- **Integration**: Slack SDK for messaging interface

## Development Commands

### Essential Commands
```bash
# Development workflow
make safe-commit    # Run all checks before committing (REQUIRED)
make test          # Run test suite
make lint-check    # Code style compliance
make type-check    # Type checking with mypy
make security-check # Security scanning

# Deployment
make deploy        # Deploy to Cloud Run
make test-health   # Test health endpoints

# Monitoring
make logs          # View application logs
make metrics       # Display system metrics
```

### Testing
```bash
# Integration testing
python scripts/testing/verify_fixes.py
python scripts/testing/test_complete_flow.py

# Manual testing
python scripts/testing/trigger_immediate_scraping.py
```

## Critical Development Rules

### Git Workflow (MANDATORY)
1. **NEVER commit directly to main** - Always use feature branches
2. **ALWAYS run `make safe-commit`** before committing
3. **NEVER use `--no-verify` flag** - It bypasses safety checks
4. **Create feature branches**: `git checkout -b feature/description`

### Code Quality Standards
- **Line length**: 120 characters (enforced by Black)
- **Type hints**: Required for all function parameters and returns
- **Pre-commit hooks**: Automatically run linting, formatting, security checks
- **Test coverage**: All new functionality must have tests

### Production Environment Rules
1. **Single Cloud Run Rule**: Only ONE instance named `bobs-brain`
2. **VPC Connectivity**: All services use `bob-vpc-connector` for Neo4j access
3. **VPC Egress**: Use `private-ranges-only` for Slack integration
4. **Cost Control**: Keep min instances at 0 when not actively used

## Key File Locations

### Production Code
- `src/bob_brain_v5.py` - Main AI assistant service (PRODUCTION)
- `src/circle_of_life.py` - Learning pipeline and ML system
- `src/unified_scraper_*.py` - Data collection services

### Configuration
- `Dockerfile` - Main Bob Brain container
- `Dockerfile.unified-scraper` - Scraper service container
- `requirements.txt` - Python dependencies
- `.pre-commit-config.yaml` - Code quality hooks

### Scripts
- `scripts/testing/` - Integration and system tests
- `scripts/deployment/` - Deployment automation
- `Makefile` - Build and development commands

### Archive Structure
- `archive/deprecated_bobs/` - Old Bob versions (18 files)
- `archive/old_scrapers/` - Previous scraper implementations
- `archive/old_versions/` - Legacy code and migrations

## Deployment Process

### Cloud Run Deployment
```bash
# Primary service deployment
gcloud run deploy bobs-brain \
  --source . \
  --platform managed \
  --region us-central1 \
  --memory 1Gi \
  --vpc-connector bob-vpc-connector \
  --vpc-egress private-ranges-only

# Scraper service deployment
docker build -f Dockerfile.unified-scraper -t gcr.io/bobs-house-ai/unified-scraper:latest .
docker push gcr.io/bobs-house-ai/unified-scraper:latest
gcloud run deploy unified-scraper --image gcr.io/bobs-house-ai/unified-scraper:latest
```

### Required Environment Variables
- `PROJECT_ID`: GCP project identifier (`bobs-house-ai`)
- `SLACK_BOT_TOKEN`: Slack bot OAuth token (Secret Manager)
- `SLACK_SIGNING_SECRET`: Request validation (Secret Manager)
- `NEO4J_URI`: Database connection string
- `NEO4J_AUTH`: Database credentials (Secret Manager)

## API Endpoints

### Bob's Brain Service (`bobs-brain`)
- `GET /health` - Health check with component status
- `POST /slack/events` - Slack event webhook handler
- `POST /test` - Test Bob's response capabilities
- `POST /learn` - Submit learning data for corrections
- `GET /circle-of-life/metrics` - Learning system metrics

### Unified Scraper Service
- `GET /health` - Service health status
- `POST /scrape` - General scraping with type parameter
- `POST /scrape/youtube` - YouTube transcript extraction
- `POST /scrape/tsb` - Technical bulletin scraping

## Common Issues & Solutions

### Slack Integration Issues
```bash
# Check VPC egress configuration
gcloud run services describe bobs-brain --region us-central1 \
  --format="value(spec.template.metadata.annotations.run.googleapis.com/vpc-access-egress)"

# Should return: private-ranges-only
```

### Neo4j Connectivity Issues
```bash
# Check VM status
gcloud compute instances list | grep neo4j

# Start if stopped
gcloud compute instances start neo4j-vm --zone=us-central1-a
```

### Service Health Monitoring
```bash
# Check all service endpoints
for service in bobs-brain unified-scraper circle-of-life-scraper; do
  curl https://$service-157908567967.us-central1.run.app/health
done
```

## Project Organization Principles

### File Creation Rules
- **NEVER create files without explicit permission**
- **ALWAYS prefer editing existing files over creating new ones**
- **Use proper directory structure** - src/ for code, scripts/ for utilities
- **Archive old code** in organized subdirectories, don't delete

### Memory & Learning System
- Conversations stored locally in your GCP project (`bobs-house-ai`)
- Used for Bob's context awareness and learning from corrections
- Data flows: Slack → Bob → Gemini → Neo4j/BigQuery storage
- Circle of Life system provides continuous model improvement

### Performance Targets
- Response time: < 2s (current: 1.8s)
- Uptime: 99.9% (current: 99.95%)
- Monthly cost: < $30 (current: $28)
- Data collection: 100+ sources daily

## Security Considerations

- All secrets stored in Google Secret Manager
- VPC networking for internal service communication
- Pre-commit hooks prevent secret commits
- Regular security scanning with Bandit
- Rate limiting on all public endpoints