# Analytics & Knowledge Base Integration with Bob's Brain

**Date:** 2025-10-05
**Purpose:** Document Jeremy's analytics infrastructure and integration opportunities with Bob's Brain

---

## Executive Summary

Jeremy has a comprehensive analytics and knowledge management system at `~/analytics/` that tracks API usage, content performance, and maintains a **653MB knowledge database**. This analysis explores integration opportunities with Bob's Brain.

---

## Analytics Infrastructure Overview

### Location: `/home/jeremy/analytics/`

**Created:** 2025-09-27
**Size:** 653MB+ (primarily knowledge.db)
**Purpose:** Centralized analytics and data tracking for all projects

---

## Database Architecture

### 1. API Usage Tracking Database ✅

**File:** `~/analytics/databases/api_usage_tracking.db` (48KB)

**Purpose:** Track all API usage, quotas, rate limits, and costs

**Schema:**
```sql
-- api_usage table
CREATE TABLE api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_provider TEXT NOT NULL,
    api_endpoint TEXT NOT NULL,
    request_timestamp DATETIME NOT NULL,
    response_status INTEGER,
    response_time_ms REAL,
    request_size_bytes INTEGER,
    response_size_bytes INTEGER,
    cost_usd REAL DEFAULT 0.0,
    quota_used INTEGER DEFAULT 1,
    rate_limit_remaining INTEGER,
    error_message TEXT,
    request_context TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Additional tables
api_quotas       -- Monthly/daily quotas and budgets
api_rate_limits  -- Rate limiting tracking
api_billing      -- Cost aggregation and billing
```

**Providers Tracked:**
- X API (Twitter) - 1,500/month, $0 (free)
- Claude API (Anthropic) - 100k/month, $50 budget
- Google Cloud - 10k/month, $100 budget
- GitHub API - 5k/hour, $0 (free)
- Turso Database - 100k ops/month, $0 (free)

**Current Metrics (as of 2025-09-27):**
- Total Monthly Budget: $150
- Current Spend: $0.01 (0.007% of budget)
- Free APIs: X, GitHub, Turso - $0 cost

### 2. Content Analytics Database

**File:** `~/analytics/databases/content_analytics_clean.db` (24KB)

**Purpose:** Track content performance across all platforms

**Tables:**
- `blog_posts` - Blog content metrics
- `social_posts` - X, LinkedIn, etc. posts
- `content_performance` - Engagement and performance data

**Content Tracked:**
- 📝 Blog Posts: 33 total (startaitools.com + jeremylongshore.com)
- 🐦 X Posts: Social media engagement
- 📊 Performance: Engagement metrics

### 3. Knowledge Base Database 🚀

**File:** `~/analytics/knowledge-base/knowledge.db` (653MB!)

**Purpose:** Large-scale knowledge storage and retrieval

**Schema:**
```sql
-- Main tables
conversations          -- Conversation history
documents              -- Document storage
documents_fts          -- Full-text search index
documents_fts_config   -- FTS configuration
documents_fts_data     -- FTS data
documents_fts_docsize  -- FTS document sizes
documents_fts_idx      -- FTS indexes
search_queries         -- Search query tracking
```

**Key Features:**
- ✅ **Full-text search** (FTS) enabled
- ✅ **Conversations** tracked
- ✅ **Documents** indexed
- ✅ **Search queries** logged
- ✅ **653MB of knowledge** (substantial corpus)

**Supporting Infrastructure:**
- `chunks/` - Document chunking
- `exports/` - Export functionality
- `scripts/` - Processing scripts
- `.config/` - Configuration

**Cloud Backup:**
- Service: Turso Database (`waygate-mcp`)
- Sync logs: `turso_upload.log` (377KB)
- Location: AWS us-east-1

---

## Integration Opportunities with Bob's Brain

### Option 1: API Usage Analytics Integration 📊

**Benefit:** Track Bob's API calls, costs, and quotas

**Implementation:**
```python
# In src/app.py - add API usage tracking
from analytics_helpers import log_api_usage

@app.post("/api/query")
def api_query():
    start_time = time.time()
    body = request.get_json(force=True) or {}

    # Process query
    result = process_query(body)

    # Log API usage
    log_api_usage(
        api_provider="bob-brain",
        api_endpoint="/api/query",
        request_timestamp=datetime.now(),
        response_time_ms=(time.time() - start_time) * 1000,
        cost_usd=calculate_cost(result),
        quota_used=1
    )

    return jsonify(result)
```

**Analytics Tracked:**
- Bob's LLM provider costs (Anthropic, Google, OpenRouter, Ollama)
- Circle of Life insight generation costs
- Neo4j query performance
- Slack integration API usage
- Response time metrics

**Benefits:**
- ✅ Cost optimization insights
- ✅ Performance bottleneck detection
- ✅ Budget tracking and alerts
- ✅ Provider comparison analytics

### Option 2: Knowledge Base Integration 🧠

**Current Knowledge DB:** 653MB with FTS

**Bob's Brain Enhancement:**
- Ingest knowledge.db documents into Bob's ChromaDB
- Use existing FTS for fast keyword search
- Leverage conversations for context
- Apply Circle of Life learning to knowledge usage

**Hybrid Approach:**
```python
# Use both databases
knowledge_db = sqlite3.connect("~/analytics/knowledge-base/knowledge.db")
chroma_db = vector_store()  # Bob's ChromaDB

# Keyword search via FTS (fast)
fts_results = knowledge_db.execute(
    "SELECT * FROM documents_fts WHERE documents_fts MATCH ?",
    (query,)
)

# Semantic search via ChromaDB (contextual)
semantic_results = chroma_db.query(query_texts=[query], n_results=5)

# Combine results for best coverage
combined_results = merge_results(fts_results, semantic_results)
```

**Benefits:**
- ✅ Leverage 653MB existing knowledge
- ✅ FTS for exact keyword matching
- ✅ ChromaDB for semantic understanding
- ✅ No duplicate storage needed

### Option 3: Analytics Dashboard for Bob 📈

**Create Bob's Brain Analytics:**
```python
# New endpoint: /analytics
@app.get("/analytics")
def bob_analytics():
    return jsonify({
        "api_usage": get_api_metrics(),
        "circle_of_life": get_col_metrics(),
        "knowledge_queries": get_knowledge_metrics(),
        "costs": get_cost_summary()
    })
```

**Metrics Tracked:**
- Total API calls by provider
- Average response times
- Circle of Life insights generated
- Knowledge base queries
- Cost per query
- Monthly spend vs budget

**Visualization:**
- Grafana dashboard (optional)
- JSON API for programmatic access
- Slack notifications for budget alerts

---

## Proposed Integration Architecture

### Unified Analytics + Knowledge System

```
┌─────────────────────────────────────────────────────────────┐
│                    Bob's Brain v5                            │
│  (Flask API + Circle of Life + Pluggable Providers)          │
└────────────┬────────────────────────────────┬───────────────┘
             │                                │
    ┌────────▼─────────┐          ┌──────────▼──────────┐
    │  Analytics DB    │          │   Knowledge DB      │
    │  (48KB SQLite)   │          │   (653MB SQLite)    │
    ├──────────────────┤          ├─────────────────────┤
    │ • api_usage      │          │ • documents (FTS)   │
    │ • api_quotas     │          │ • conversations     │
    │ • api_billing    │          │ • search_queries    │
    │ • rate_limits    │          │                     │
    └──────────────────┘          └─────────────────────┘
             │                                │
             └────────────┬───────────────────┘
                          │
                 ┌────────▼─────────┐
                 │   ChromaDB       │
                 │  (Research Docs) │
                 ├──────────────────┤
                 │ • jeremy_research│
                 │ • bob_knowledge  │
                 └──────────────────┘
                          │
                 ┌────────▼─────────┐
                 │   Circle of Life │
                 │  Learning Loop   │
                 ├──────────────────┤
                 │ • Track usage    │
                 │ • Learn patterns │
                 │ • Optimize costs │
                 │ • Suggest docs   │
                 └──────────────────┘
```

---

## Implementation Plan

### Phase 1: API Usage Tracking (Week 1)

**Goal:** Track Bob's API calls and costs

**Tasks:**
1. Copy `~/analytics/analytics_helpers.py` to Bob's Brain
2. Add logging to all API endpoints
3. Track LLM provider costs
4. Create `/analytics` endpoint
5. Set up budget alerts

**Expected Results:**
- Track all Bob API calls
- Real-time cost monitoring
- Budget alerts at 80%, 90%, 100%

### Phase 2: Knowledge DB Integration (Week 2)

**Goal:** Leverage 653MB knowledge database

**Tasks:**
1. Create read-only connection to knowledge.db
2. Add FTS search endpoint
3. Combine FTS + ChromaDB results
4. Track which documents are most useful
5. Circle of Life learning on knowledge usage

**Expected Results:**
- Access 653MB knowledge corpus
- Fast keyword search (FTS)
- Semantic search (ChromaDB)
- Learn valuable documents

### Phase 3: Analytics Dashboard (Week 3)

**Goal:** Comprehensive Bob analytics

**Tasks:**
1. Create analytics aggregation queries
2. Build JSON API endpoints
3. (Optional) Grafana dashboard
4. Slack notifications for key metrics
5. Monthly cost reports

**Expected Results:**
- Real-time Bob metrics
- Cost optimization insights
- Performance monitoring
- Usage pattern analysis

---

## Database Details

### Analytics Database Schema

**api_usage table:**
- Tracks: Provider, endpoint, timestamp, status, timing, cost
- Indexes: provider+timestamp, endpoint, cost
- Usage: Log every API call with performance metrics

**api_quotas table:**
- Tracks: Monthly/daily quotas per provider
- Alerts: Warn at 80%, 90%, critical at 100%
- Providers: Claude, Google, OpenRouter, Ollama

**api_billing table:**
- Tracks: Aggregated costs by provider
- Reporting: Daily, weekly, monthly summaries
- Budget: Compare actual vs allocated spend

### Knowledge Database Schema

**documents table:**
- Stores: Full document content
- FTS: Full-text search enabled
- Size: 653MB corpus
- Types: Research papers, blog posts, notes

**conversations table:**
- Stores: Historical conversations
- Context: Previous interactions
- Learning: Pattern recognition

**search_queries table:**
- Tracks: What users search for
- Analytics: Popular queries
- Optimization: Pre-cache frequent searches

---

## Cost Optimization Opportunities

### Current Spend Analysis (from analytics DB)

**Total Budget:** $150/month
- Claude API: $50 allocated
- Google Cloud: $100 allocated

**Current Spend:** $0.01 (0.007% of budget)

**Free Tier Usage:**
- X API: 1,500/month limit
- GitHub API: 5k/hour limit
- Turso DB: 100k ops/month limit

### Bob's Brain Cost Optimization

**With Analytics Integration:**
1. **Track per-provider costs**
   - Compare Anthropic vs Google vs OpenRouter
   - Identify most expensive queries
   - Optimize model selection

2. **Circle of Life cost learning**
   - Learn which queries are expensive
   - Route simple queries to cheaper models
   - Use local Ollama for low-stakes queries

3. **Budget alerts**
   - Warn at 80% of budget ($120)
   - Critical at 90% ($135)
   - Auto-throttle at 100% ($150)

4. **Cost per query metrics**
   - Average cost per Slack message
   - Cost per Circle of Life insight
   - ROI on knowledge queries

**Expected Savings:**
- 20-30% reduction in API costs
- Better provider utilization
- Predictive budget management

---

## Files to Copy to Bob's Brain

### From ~/analytics/

**Core Files:**
1. `analytics_helpers.py` (13KB)
   - API usage logging functions
   - Cost calculation utilities
   - Database connection helpers

2. `databases/api_usage_tracking.db` (48KB)
   - Reference for schema
   - Or create new Bob-specific tracking

3. `knowledge-base/knowledge.db` (653MB)
   - Read-only connection (don't copy)
   - Query from original location
   - Backup to Bob's ChromaDB over time

**Documentation:**
4. `README.md` → `claudes-docs/analysis/analytics-overview.md`
5. `STRUCTURE.md` → `claudes-docs/analysis/analytics-structure.md`
6. `DATABASE_ARCHITECTURE.md` → `claudes-docs/analysis/analytics-db-architecture.md`

---

## Success Metrics

### Phase 1 Success
- ✅ All Bob API calls logged
- ✅ Real-time cost tracking
- ✅ Budget alerts functional
- ✅ <5ms logging overhead

### Phase 2 Success
- ✅ Knowledge DB accessible via API
- ✅ FTS + ChromaDB hybrid search
- ✅ <200ms query response time
- ✅ Circle of Life learning knowledge usage

### Phase 3 Success
- ✅ Analytics dashboard live
- ✅ Monthly cost reports automated
- ✅ Performance bottlenecks identified
- ✅ 20%+ cost reduction achieved

---

## Next Steps

### Immediate (Do First)

1. **Copy analytics helpers to Bob**
   ```bash
   cp ~/analytics/analytics_helpers.py \
      ~/projects/bobs-brain/src/analytics.py
   ```

2. **Create API usage tracking**
   ```bash
   # Add to src/app.py
   from src.analytics import log_api_usage
   ```

3. **Test logging**
   ```bash
   # Send test query
   curl -X POST http://localhost:8080/api/query \
     -H "X-API-Key: test" \
     -d '{"query":"test"}'

   # Check analytics
   sqlite3 ~/analytics/databases/api_usage_tracking.db \
     "SELECT * FROM api_usage WHERE api_provider='bob-brain'"
   ```

### Short-term (This Week)

4. **Knowledge DB read-only connection**
5. **Create /api/knowledge endpoint**
6. **Hybrid FTS + ChromaDB search**
7. **Circle of Life knowledge tracking**

### Medium-term (Next Sprint)

8. **Analytics dashboard API**
9. **Cost optimization analysis**
10. **Budget alert system**
11. **Monthly reporting automation**

---

## Conclusion

Jeremy's analytics infrastructure provides **production-grade API tracking, cost monitoring, and a 653MB knowledge database**. Integration with Bob's Brain enables:

1. **Cost Optimization:** Track and reduce API costs by 20-30%
2. **Performance Monitoring:** Identify bottlenecks and optimize
3. **Knowledge Leverage:** Access 653MB knowledge corpus
4. **Learning Enhancement:** Circle of Life learns from analytics

**Status:** Ready for Phase 1 implementation
**Priority:** High - Cost savings and performance insights
**Risk:** Low - Read-only analytics integration

---

**Document Created:** 2025-10-05
**Related:**
- `~/analytics/README.md`
- `~/analytics/knowledge-base/knowledge.db` (653MB)
- `~/analytics/databases/api_usage_tracking.db`
- `claudes-docs/analysis/2025-10-05_circle-of-life-knowledge-integration.md`
