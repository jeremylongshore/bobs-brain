# 📋 BOB'S BRAIN PROJECT TODO LIST
**Last Updated:** 2025-01-12 (January 12, 2025)
**Project Owner:** Jeremy Longshore
**Current Phase:** Testing & Data Pipeline Fix

---

## 🔴 PRIORITY 0: TEST ENVIRONMENT & WORKSPACE SETUP

### 1. **Set Up Test Environment for Google Workspace Service Account** ⏰ URGENT
- [ ] Create test project in GCP for safe testing
- [ ] Verify Google Workspace service account permissions
- [ ] Test service account can access:
  - [ ] Gmail API
  - [ ] Drive API
  - [ ] Calendar API
  - [ ] Workspace Admin SDK (if needed)
- [ ] Create test script to verify all permissions
- [ ] Document working configuration
- [ ] Test Bob can read/write to Workspace resources

### 2. **Create Local Test Environment**
- [ ] Set up local Docker environment matching Cloud Run
- [ ] Create test data pipeline
- [ ] Verify all API keys work locally
- [ ] Test scraper without affecting production

---

## 🟡 PRIORITY 1: FIX DATA COLLECTION (TODAY)

### 3. **Deploy Working Scraper**
- [ ] Deploy safe_scraper.py to unified-scraper
- [ ] Test Reddit API with new credentials
- [ ] Verify RSS feeds are collecting
- [ ] Check manufacturer sites scraping
- [ ] Monitor BigQuery for new data

### 4. **Fix Scraping Issues**
- [ ] Remove sites that require login
- [ ] Add error handling for timeouts
- [ ] Implement retry logic
- [ ] Add health monitoring for scrapers

---

## 🟢 PRIORITY 2: CORE IMPROVEMENTS (THIS WEEK)

### 5. **Initialize Graphiti Knowledge Graph**
- [ ] Fix LLM integration for Graphiti
- [ ] Test entity extraction
- [ ] Verify Neo4j storing relationships
- [ ] Create knowledge query endpoints

### 6. **YouTube Scraper Enhancement**
- [ ] Get real equipment repair video IDs
- [ ] Set up YouTube Data API (optional)
- [ ] Extract transcripts from popular channels:
  - [ ] Messick's Equipment
  - [ ] Diesel Creek
  - [ ] Andrew Camarata
- [ ] Store transcripts in BigQuery

### 7. **Data Quality Pipeline**
- [ ] Implement deduplication
- [ ] Add data validation
- [ ] Create quality scoring
- [ ] Set up monitoring alerts

---

## 🔵 PRIORITY 3: MONITORING & OPTIMIZATION (NEXT WEEK)

### 8. **Create Monitoring Dashboard**
- [ ] Set up Grafana or similar
- [ ] Track scraping success rates
- [ ] Monitor API usage & costs
- [ ] Create alerts for failures
- [ ] Track data growth over time

### 9. **Implement Caching Layer**
- [ ] Set up Redis for frequently accessed data
- [ ] Cache common queries
- [ ] Reduce BigQuery costs
- [ ] Improve response times

### 10. **Performance Optimization**
- [ ] Optimize BigQuery queries
- [ ] Implement connection pooling
- [ ] Add async processing where needed
- [ ] Profile and fix bottlenecks

---

## ⚪ PRIORITY 4: ADVANCED FEATURES (NEXT MONTH)

### 11. **ML Model Training**
- [ ] Collect sufficient training data
- [ ] Train custom diagnostic models
- [ ] Implement predictive maintenance
- [ ] Create failure pattern recognition

### 12. **Expand Data Sources**
- [ ] Add Facebook groups (if possible)
- [ ] Integrate Discord communities
- [ ] Connect manufacturer APIs
- [ ] Add parts catalog data

### 13. **Mobile & Voice Interface**
- [ ] Design mobile app architecture
- [ ] Implement offline mode
- [ ] Add voice commands
- [ ] Create field technician features

---

## 📊 SUCCESS METRICS

### Weekly Goals:
- [ ] 1000+ items scraped per day
- [ ] < 2 second response time
- [ ] 0 service downtime
- [ ] < $1/day operational cost

### Monthly Goals:
- [ ] 30,000+ knowledge items stored
- [ ] 95% query accuracy
- [ ] 10+ equipment types covered
- [ ] Complete diagnostic coverage

---

## 🛠️ QUICK COMMANDS

### Test Service Account:
```bash
# Test Workspace API access
python3 test_workspace_access.py

# Check service account permissions
gcloud iam service-accounts get-iam-policy YOUR-SA@PROJECT.iam.gserviceaccount.com
```

### Deploy Scraper Fix:
```bash
# Update scraper code
cp src/safe_scraper.py src/unified_scraper_simple.py

# Deploy to Cloud Run
gcloud run deploy unified-scraper --source . --region us-central1
```

### Monitor Data Collection:
```bash
# Check recent scrapes
gcloud logging read "resource.type=cloud_run_revision AND textPayload:'items stored'" --limit 10

# Query BigQuery
bq query --use_legacy_sql=false "SELECT COUNT(*) FROM \`bobs-house-ai.DATASET.TABLE\`"
```

### Test Reddit API:
```bash
curl -X POST https://unified-scraper-157908567967.us-central1.run.app/scrape/quick \
  -H "Content-Type: application/json" \
  -d '{}' --max-time 30
```

---

## 📝 NOTES

- **Google Workspace Integration:** Critical for reading company emails/docs for knowledge
- **Test Environment:** Prevents breaking production while developing
- **Data Collection:** Current #1 issue - Bob needs data to be useful
- **Reddit API:** Now configured but needs scraper deployment to use it

---

**Remember:** Test in development first, deploy to production second!
