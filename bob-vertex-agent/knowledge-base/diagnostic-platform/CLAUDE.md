# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

The DiagnosticPro Platform is a comprehensive diagnostic and repair data platform with **3-PROJECT GOOGLE CLOUD ARCHITECTURE** and clean separation of concerns across data collection, database management, and customer-facing services.

## Project Architecture

```
diagnostic-platform/
├── DiagnosticPro/              # Customer-facing React app (Firebase/Cloud Run)
├── bigq and scrapers/
│   ├── schema/                 # BigQuery schemas (266 tables → diagnostic-pro-start-up)
│   ├── scraper/                # Data collection → diagnostic-pro-start-up
│   └── marketing-intelligence/ # Analytics and insights
├── 01-Docs/                    # Flat documentation directory (NNN-abv-description.ext)
├── 02-Src/                     # Additional source code
├── 05-Scripts/                 # Automation scripts
├── 06-Infrastructure/          # Infrastructure as Code (Terraform)
└── claudes-docs/               # AI-generated documentation
```

### Google Cloud Projects (3-Project Separation)

1. **`diagnostic-pro-start-up`** - BigQuery Data & Analytics (266 production tables)
2. **`diagnostic-pro-prod`** - Production Cloud Run Services, Vertex AI, Firestore
3. **`diagnostic-pro-creatives`** - Third project for creative assets

**Data Flow:** Scrapers → diagnostic-pro-start-up (BigQuery) → API queries from diagnostic-pro-prod → Customer reports

## Quick Commands

### DiagnosticPro Customer Platform (diagnostic-pro-prod)

```bash
cd DiagnosticPro

# Frontend development (React + TypeScript + Vite)
cd 02-src/frontend
npm install                       # Install dependencies
npm run dev                       # Vite dev server (http://localhost:5173)
npm run build                     # Production build
npm run preview                   # Preview production build
npm test                          # Run Jest tests

# Backend API (Cloud Run)
cd 02-src/backend/services/backend
npm start                         # Production mode
npm run dev                       # Development with nodemon
npm test                          # Run tests

# Deploy backend to Cloud Run
gcloud run deploy diagnosticpro-vertex-ai-backend \
  --source . \
  --region us-central1 \
  --project diagnostic-pro-prod

# Firebase deployment
firebase deploy --only hosting    # Deploy frontend to diagnosticpro.io
firebase deploy --only functions  # Deploy Cloud Functions
firebase deploy --only firestore  # Deploy security rules
firebase emulators:start          # Local development with emulators
```

### BigQuery Data Operations (diagnostic-pro-start-up)

```bash
cd "bigq and scrapers/schema"

# Deploy BigQuery tables (266 tables)
PROJECT="diagnostic-pro-start-up" ./deploy_bigquery_tables.sh

# Import data pipeline
./bigquery_import_pipeline.sh

# Query production data
bq query --project diagnostic-pro-start-up \
  --use_legacy_sql=false \
  "SELECT COUNT(*) FROM \`diagnostic-pro-start-up.diagnosticpro_prod.users\`"

# List datasets and tables
bq ls diagnostic-pro-start-up                          # Datasets
bq ls diagnostic-pro-start-up:diagnosticpro_prod       # Production tables
bq ls diagnostic-pro-start-up:diagnosticpro_analytics  # Analytics
```

### Data Collection & Scraping (diagnostic-pro-start-up)

```bash
cd "bigq and scrapers/scraper"

# Run individual data collectors
python3 youtube_scraper/data_extractor.py       # YouTube videos
python3 praw/massive_500k_collector.py          # Reddit posts
python3 github_miner/enhanced_github_miner.py   # GitHub repos
./scripts/run_all_collectors.sh                 # All in parallel

# Data processing pipeline
python3 scripts/validate_export_data.py         # Validate against schema
python3 scripts/prepare_cloud_export.py         # Prepare for upload
cd export_gateway/cloud_ready && ./upload_to_gcp.sh

# Monitor pipeline status
ls -la export_gateway/raw/ | wc -l              # Pending items
ls -la export_gateway/cloud_ready/ | wc -l      # Ready for upload
ls -la export_gateway/failed/                   # Failed exports
tail -f logs/*.log                              # Live logs
```

### Project Management

```bash
# AI-dev pipeline status
make status

# Create document from template
make create T=template-name.md N=document-name.md

# List available templates
make list-templates
```

## Technology Stack

### DiagnosticPro Customer Service (diagnostic-pro-prod)
- **Frontend**: React 18 + TypeScript + Vite → Firebase Hosting (diagnosticpro.io)
- **Backend**: Node.js 18 Express API → Cloud Run (`diagnosticpro-vertex-ai-backend`)
- **Database**: Firestore (diagnosticSubmissions, orders, emailLogs)
- **AI**: Vertex AI Gemini 2.5 Flash (proprietary 15-section analysis)
- **Payments**: Stripe ($4.99 per diagnostic)
- **Storage**: Cloud Storage with signed URLs
- **UI**: shadcn/ui + Tailwind CSS

### BigQuery Data Platform (diagnostic-pro-start-up)
- **Database**: Google BigQuery (266 production tables)
- **Languages**: Python 3.12+, SQL, Bash
- **Scraping**: Selenium, Playwright, BeautifulSoup, PRAW
- **Data Sources**: YouTube, Reddit, GitHub
- **Datasets**: diagnosticpro_prod, diagnosticpro_analytics, repair_diagnostics

## Critical Architecture Rules

### Data Flow Pipeline
1. **Separation of Concerns**: Scrapers NEVER access databases directly
2. **Single Exit Point**: All scraped data exits through `scraper/export_gateway/cloud_ready/`
3. **Single Entry Point**: Schema project receives data through `datapipeline_import/pending/`
4. **Schema Validation**: All data validated against `scraper/configs/schema_rules.json`
5. **Cross-Project Access**: Production services query BigQuery via IAM (diagnostic-pro-prod → diagnostic-pro-start-up)
6. **Universal Equipment Registry**: Mandatory field mapping compliance for all equipment types

### Production Workflow (v2.0.0)
```
Customer Form → Firestore (diagnosticSubmissions)
     ↓
Stripe Payment ($4.99) → Firestore (orders)
     ↓
Webhook → 15-Section AI Analysis → Vertex AI Gemini 2.5 Flash
     ↓
PDF Generation (production-grade) → Cloud Storage → Signed URL
     ↓
Email Delivery → Customer Download
```

### Proprietary AI Analysis Framework (v2.0)
15-section diagnostic analysis:
1. Primary Diagnosis
2. Differential Diagnosis
3. Diagnostic Verification
4. Shop Interrogation
5. Conversation Scripting
6. Cost Breakdown
7. Ripoff Detection
8. Authorization Guide
9. Technical Education
10. OEM Parts Strategy
11. Negotiation Tactics
12. Likely Causes
13. Recommendations
14. Source Verification
15. Root Cause Analysis (v2.0 addition)

## Directory Standards

This project follows `.directory-standards.md`:
- All docs stored in flat `01-Docs/` directory (no subdirectories)
- Naming format: `NNN-abv-description.ext`
- Approved abbreviations: adr, prd, tsk, mtg, aar, log, etc.
- Strict chronological order enforced

## Git Workflow (ENFORCED)

1. **NEVER commit directly to main branch**
2. **ALWAYS create feature branches**: `git checkout -b feature/description`
3. **Pre-commit validation**: All changes must pass linting and type checking
4. **Clean commit messages**: Follow conventional commits format

## Environment Variables

### Production Backend (Cloud Run)
```bash
GOOGLE_CLOUD_PROJECT=diagnostic-pro-prod
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
FIRESTORE_PROJECT_ID=diagnostic-pro-prod
VERTEX_AI_PROJECT=diagnostic-pro-prod
VERTEX_AI_REGION=us-central1
```

### Data Scraping (diagnostic-pro-start-up)
```bash
GOOGLE_CLOUD_PROJECT=diagnostic-pro-start-up
BIGQUERY_DATASET=diagnosticpro_prod
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=RepairDataExtractor/1.0
```

### Frontend (Firebase)
```bash
VITE_FIREBASE_PROJECT_ID=diagnostic-pro-prod
VITE_FIREBASE_API_KEY=AIzaSyBmuntVKosh_EGz5yxQLlIoNXlxwYE6tMg
VITE_FIREBASE_AUTH_DOMAIN=diagnostic-pro-prod.firebaseapp.com
VITE_FIREBASE_STORAGE_BUCKET=diagnostic-pro-prod.firebasestorage.app
```

## Monitoring & Debugging

### Production Service Logs
```bash
# Cloud Run backend logs
gcloud logging read "resource.type=\"cloud_run_revision\" \
  AND resource.labels.service_name=\"diagnosticpro-vertex-ai-backend\"" \
  --project diagnostic-pro-prod --limit 50

# Firebase Functions logs
firebase functions:log

# Health checks
curl https://simple-diagnosticpro-298932670545.us-central1.run.app/healthz
```

### Data Pipeline Health
```bash
# Check export pipeline
ls -la "bigq and scrapers/scraper/export_gateway/raw/" | wc -l      # Pending
ls -la "bigq and scrapers/scraper/export_gateway/failed/"           # Failed

# BigQuery status
bq ls diagnostic-pro-start-up:diagnosticpro_prod                    # Tables
tail -f "bigq and scrapers/scraper/logs/"*.log                      # Logs
```

## Performance Targets

### Customer Service
- End-to-end success rate: >95%
- Email delivery rate: >98%
- Response time: <10 minutes
- Firestore queries: <100ms
- Vertex AI analysis: <30s
- PDF generation: <5s

### Data Collection
- YouTube scraping: 1,000 videos/hour
- Reddit collection: 10,000 posts/hour
- BigQuery upload: 100MB/minute
- Data validation: <100ms per batch

## Key Integration Points

| Component | Location | Purpose |
|-----------|----------|---------|
| Schema Rules | `scraper/configs/schema_rules.json` | Shared validation (READ-ONLY) |
| Export Gateway | `scraper/export_gateway/cloud_ready/` | Prepared data for import |
| Import Pipeline | `schema/datapipeline_import/pending/` | Awaiting validation |
| BigQuery Production | `diagnostic-pro-start-up:diagnosticpro_prod` | 266 production tables |
| Customer Frontend | `DiagnosticPro/02-src/frontend/` | React app |
| Backend API | `DiagnosticPro/02-src/backend/services/backend/` | Cloud Run service |

## Project Context

Part of Jeremy's diagnostic platform ecosystem expanding from $4.99 automotive diagnostics to universal equipment diagnostics ($4.99-$49.99). Market expansion from $100B automotive to $500B+ universal equipment market.

**Related Projects:**
- Parent workspace: `/home/jeremy/000-projects/`
- Blog: `blog/startaitools/` (Hugo)
- Infrastructure: `waygate-mcp/` (security-hardened MCP)
- AI workflows: `ai-dev-tasks-master/` (templates)

## Project-Specific Documentation

Each major component has its own detailed CLAUDE.md:
- `DiagnosticPro/CLAUDE.md` - Customer service app (v2.0.0 with 15-section AI)
- `bigq and scrapers/schema/CLAUDE.md` - Database schema project (266 tables)
- `bigq and scrapers/scraper/CLAUDE.md` - Data collection system (YouTube, Reddit, GitHub)

Refer to component-specific CLAUDE.md files for detailed commands, workflows, and architectural details.
