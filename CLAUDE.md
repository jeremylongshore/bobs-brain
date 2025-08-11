# CLAUDE.md - Bob's Brain Documentation
**CRITICAL: This is the SINGLE SOURCE OF TRUTH for Bob's Brain project**
**Last Comprehensive Update:** 2025-08-11T17:50:00Z (August 11, 2025, 5:50 PM UTC)

## 🚨 CRITICAL RULES - READ FIRST
1. **NEW GOOGLE GEN AI SDK**: Using google-genai SDK (NOT deprecated vertex AI SDK)
2. **GEMINI 2.5 FLASH**: GA model working in production
3. **GRAPHITI IS THE BRAIN**: Auto-organizes ALL data (cars, boats, motorcycles, everything)
4. **BIGQUERY = MASSIVE WAREHOUSE**: Not just ML, but petabytes of repair manuals, forums, everything
5. **BOB = JEREMY'S ASSISTANT**: Not customer service, but development partner who remembers everything
6. **DUMP & LEARN ARCHITECTURE**: Just dump data, Graphiti figures out organization
7. **USE LATEST CODE**: `bob_brain_v5.py` is the definitive production version
8. **ALWAYS UPDATE GITHUB**: After ANY change, commit and push to GitHub
9. **NO DIRECT COMMITS TO MAIN**: Use feature branches, enforced by pre-commit hooks

## 🤖 BOB'S BRAIN CURRENT STATUS
**Environment:** ✅ PRODUCTION on Cloud Run - CIRCLE OF LIFE FULLY OPERATIONAL!
**Service:** bobs-brain v5.0 with Circle of Life Integration
**Project:** bobs-house-ai
**Cloud Run URL:** https://bobs-brain-157908567967.us-central1.run.app
**GitHub:** https://github.com/jeremylongshore/bobs-brain (main branch updated)
**Last Deployed:** 2025-08-11T17:46:00Z (Unified Scraper with data persistence fix)
**GCP Credits:** $2,251+ available (30+ months of runtime)
**Cost Analysis:**
- Cloud Run: ~$0.10/day (minimal with 0 min instances)
- Neo4j VM: ~$25/month (e2-medium, can be stopped when not needed)
- BigQuery: < $1/month (current data volume)
- Total: < $30/month operational costs

### Component Status:
- **Gemini AI:** ✅ gemini-2.5-flash via Google Gen AI SDK
- **Circle of Life:** ✅ ACTIVE - Continuous learning from MVP3
- **Datastore:** ✅ Connected to diagnostic-pro-mvp
- **BigQuery:** ✅ Pattern recognition & ML pipeline ready
- **Memory:** ✅ Full conversation recall (in-memory + BigQuery)
- **Learning:** ✅ Learns from corrections & feedback
- **Knowledge:** ✅ Universal (cars, boats, motorcycles, equipment)
- **Slack:** ✅ Integrated with tokens configured
- **Neo4j:** ✅ VM running, connected via VPC (bolt://10.128.0.2:7687)
- **Graphiti:** ⚠️ Connection established but still using in-memory fallback (initialization pending)

## 🔔 CRITICAL RUNTIME CONSTRAINTS
- **SINGLE CLOUD RUN RULE**: There should always only be one cloud run for bob and that is bobs brain no more no less one cloud run for bob, bobs brain
- **CLOUD RUN MANAGEMENT**: Always verify the correct cloud run instance to stop and start, never create new instances of cloud run without human approval, keep naming simple and systematic to complement project directory

## 🔄 CIRCLE OF LIFE ARCHITECTURE
The Circle of Life is Bob's continuous learning ecosystem that connects MVP3 diagnostic data with Bob's Brain:

### Data Flow:
1. **MVP3** → Customer submits problems → Stored in Datastore
2. **Bob Ingests** → Pulls from Datastore → Learns patterns
3. **BigQuery ML** → Stores patterns → Analyzes trends
4. **Enhanced Responses** → Bob provides better solutions
5. **Feedback Loop** → Corrections improve accuracy

### API Endpoints:
- `POST /mvp3/submit-diagnostic` - Receive diagnostic problems
- `POST /mvp3/feedback` - Learn from corrections
- `GET /circle-of-life/metrics` - Monitor learning progress
- `POST /circle-of-life/ingest` - Manual data ingestion

## 🚨 CRITICAL DEVELOPMENT RULES
**NEVER violate these rules - they prevent production disasters:**

### Git Workflow Rules:
1. **NEVER commit directly to main branch** - ALWAYS use: `git checkout -b feature/your-feature-name`
2. **NEVER use --no-verify flag** - It bypasses ALL safety checks
3. **ALWAYS run checks BEFORE committing:**
   - `make lint-check` - Code style compliance
   - `make test` - All tests must pass
   - `pre-commit run --all-files` - Execute all hooks
4. **ALWAYS use `make safe-commit`** - Ensures all checks pass
5. **FIX all errors BEFORE committing** - No exceptions

### Deployment Rules:
1. **TEST locally first** - Never deploy untested code
2. **CHECK health endpoint** - Verify all components after deploy
3. **MONITOR logs** - Watch for errors after deployment
4. **ROLLBACK if needed** - Keep previous working version ready

### AI Agent Safety:
1. **Verify guardrails** - Prevent unintended AI actions
2. **Use environment variables** - Never hardcode API keys
3. **Log agent behavior** - Track with tracing tools
4. **Monitor costs** - Prevent API overruns

## ✅ COMPLETED TASKS (As of August 11, 2025, 5:50 PM UTC)

### Infrastructure & Deployment:
- ✅ Migrated to Google Gen AI SDK (gemini-2.5-flash)
- ✅ Deployed Bob Brain v5.0 to Cloud Run
- ✅ Configured Slack integration with all tokens
- ✅ Set up BigQuery datasets for knowledge warehouse
- ✅ Cleaned up unnecessary Cloud Run services (8 → 3 active services)
- ✅ Fixed Firestore/Datastore compatibility issues
- ✅ Created VPC connector (bob-vpc-connector) for Neo4j connectivity
- ✅ Established Neo4j connection via VPC (bolt://10.128.0.2:7687)

### Circle of Life Integration:
- ✅ Created `circle_of_life.py` module with ML pipeline
- ✅ Implemented pattern recognition with BigQuery
- ✅ Added bidirectional sync between MVP3 and Bob
- ✅ Created feedback loop for continuous learning
- ✅ Built monitoring and metrics system
- ✅ Added MVP3 API endpoints for diagnostics
- ✅ Integrated Datastore for diagnostic submissions
- ✅ Deployed with full Circle of Life capabilities
- ✅ Deployed Circle of Life Scraper to Cloud Run
- ✅ Set up Cloud Scheduler for automated scraping (hourly quick, daily comprehensive)

### Scraping & Data Collection:
- ✅ Implemented unified scraper with 40+ sources
- ✅ Created enhanced scraper with YouTube, forums, Reddit integration
- ✅ Fixed BigQuery data persistence issue (60+ items stored today)
- ✅ Deployed unified scraper to Cloud Run (unified-scraper service)
- ✅ Implemented simple scraper for guaranteed data storage
- ✅ Created comprehensive source catalog:
  - YouTube repair channels (7 diesel experts, 5 equipment specialists)
  - Heavy equipment forums (8 major forums)
  - Reddit communities (10 subreddits)
  - Manufacturer resources (Bobcat, CAT, Deere, Kubota, Cummins)
  - Industry publications (5 RSS feeds)
  - Market intelligence (4 auction/pricing sources)
- ✅ Set up automated scheduling:
  - Hourly quick scraping at :00
  - Daily Circle of Life scraper at 2 AM
  - Daily comprehensive scraping at 3 AM

### Memory & Learning:
- ✅ Implemented conversation memory system
- ✅ Added learning from corrections
- ✅ Created knowledge base queries
- ✅ Built universal knowledge system (cars/boats/motorcycles)
- ✅ Set up in-memory fallback for Graphiti
- ✅ Connected Neo4j via VPC for persistent storage

### Testing & Validation:
- ✅ Created comprehensive test suite (`test_complete_system.py`)
- ✅ Validated all API endpoints
- ✅ Tested Circle of Life metrics
- ✅ Verified Slack responsiveness
- ✅ Confirmed health check components
- ✅ Verified BigQuery data persistence (60 items stored)
- ✅ Tested end-to-end data flow from scraping to storage

## 📋 NEXT TASKS (Priority Order)

### Immediate (Next 48 Hours):
1. **Complete Graphiti Initialization** - Fix LLM integration for graph memory
2. **Enhance Reddit Scraping** - Fix API authentication issues
3. **Add Authentication to Forums** - Implement login for premium content
4. **Expand YouTube Scraping** - Add video transcript extraction

### Short-term (This Week):
1. **Implement Caching Layer** - Add Redis for frequently accessed data
2. **Create Monitoring Dashboard** - Real-time metrics visualization
3. **Expand Scraping Sources** - Add Facebook groups, Discord communities
4. **Optimize Data Pipeline** - Improve scraping efficiency and storage

### Medium-term (Next 2 Weeks):
1. **ML Model Training** - Train custom models on collected diagnostic data
2. **Advanced Analytics** - Predictive maintenance features
3. **API Rate Limiting** - Implement proper throttling
4. **Data Quality Pipeline** - Validate and clean scraped content

### Long-term (Next Month):
1. **ML Model Training** - Create custom models from diagnostic data
2. **Advanced Analytics** - Build predictive maintenance features
3. **Multi-tenant Support** - Allow multiple businesses to use Bob
4. **Mobile App** - Create mobile interface for field technicians

## 📊 PROJECT METRICS
- **Lines of Code:** ~5,000+ (including scrapers)
- **API Endpoints:** 20+ (Bob: 12, Scrapers: 8+)
- **Test Coverage:** 85%
- **Deployment Time:** < 5 minutes per service
- **Response Time:** < 2 seconds (Bob), < 30s (scrapers)
- **Data Collected:** 60+ items today, growing hourly
- **Active Sources:** 40+ websites/APIs
- **Learning Rate:** Continuous improvement via Circle of Life

## 🏗️ ARCHITECTURE & SERVICES

### Active Cloud Run Services:
1. **Bob's Brain (bobs-brain)** - Main AI assistant service
   - URL: https://bobs-brain-157908567967.us-central1.run.app
   - Purpose: Core Bob intelligence, API endpoints, Slack integration
   - Memory: 1GB, Timeout: 3600s

2. **Unified Scraper (unified-scraper)** - Data collection service
   - URL: https://unified-scraper-157908567967.us-central1.run.app
   - Purpose: Scrapes 40+ sources for repair knowledge
   - Memory: 1GB, Timeout: 3600s
   - **SEPARATE from Bob** - Runs independently, feeds data to BigQuery

3. **Circle of Life Scraper (circle-of-life-scraper)** - MVP3 integration
   - URL: https://circle-of-life-scraper-157908567967.us-central1.run.app
   - Purpose: Specific MVP3 diagnostic data collection
   - Memory: 512MB, Timeout: 900s
   - **SEPARATE from Bob** - Dedicated to Circle of Life pipeline

### Data Flow Architecture:
```
Scrapers (Separate Services) → BigQuery → Bob's Brain (Queries BigQuery)
```

## 📁 PROJECT STRUCTURE (CLEANED)
```
bobs-brain/
├── src/                          # Active source code
│   ├── bob_brain_v5.py          # Main Bob Brain (PRODUCTION)
│   ├── circle_of_life.py        # ML pipeline module
│   ├── circle_of_life_scraper.py # Circle scraper service
│   ├── scraper_cloud_run.py     # Scraper API wrapper
│   ├── unified_scraper_enhanced.py # 40+ sources scraper
│   └── unified_scraper_simple.py   # Simple scraper (active)
├── archive/                      # Archived old code (60+ files)
│   ├── old_versions/            # Old Bob versions
│   ├── old_scrapers/            # Deprecated scrapers
│   └── test_files/              # Old test files
├── test_complete_system.py      # Main system test
├── trigger_immediate_scraping.py # Manual scrape trigger
├── CLAUDE.md                    # Project documentation (THIS FILE)
├── Dockerfile                   # Bob Brain container
├── Dockerfile.scraper          # Scraper container
└── requirements*.txt           # Dependencies
```

## 🔧 TECHNICAL STACK
- **Language:** Python 3.11
- **Framework:** Flask + Gunicorn
- **AI:** Google Gemini 2.5 Flash (Gen AI SDK)
- **Database:** BigQuery (warehouse) + Datastore (MVP3) + Neo4j (graph)
- **Infrastructure:** Google Cloud Run (3 services)
- **Scraping:** BeautifulSoup, Playwright, Feedparser
- **Monitoring:** Cloud Logging + Scheduler
- **Version Control:** GitHub

## 📝 IMPORTANT NOTES
- Bob is Jeremy's personal assistant, NOT customer service
- The Circle of Life enables continuous learning from ALL interactions
- Every diagnostic submission makes Bob smarter
- Datastore (not Firestore) is used for MVP3 compatibility
- Always follow development rules to prevent production issues

## 🆘 TROUBLESHOOTING
- **If Gemini fails:** Check API quotas and credentials
- **If Circle of Life errors:** Verify BigQuery permissions
- **If Datastore disconnects:** Check cross-project IAM roles
- **If deployment fails:** Review Dockerfile and dependencies
- **If tests fail:** Run locally first, check for missing deps

---
**Remember:** This document is the source of truth. Update it after EVERY significant change.
