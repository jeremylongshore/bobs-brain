# Bob's Smart Knowledge Strategy

**Created:** 2025-11-09
**Goal:** Get 50GB of /home/jeremy data into Bob's brain efficiently within 5GB Vertex AI free tier

---

## The Problem

- **Total data:** 67GB in /home/jeremy/
- **Vertex AI free tier:** 5GB
- **Archive data:** 8.9GB of old projects (backed up, rarely needed)
- **Need:** Most relevant data searchable ASAP

---

## The Smart Solution: 2-Tier Knowledge System (100% FREE!)

### Tier 1: Hot Knowledge (Vertex AI Search - 5GB max)
**What:** Most relevant, actively used data
**Why:** Fast semantic search, always available to Bob
**Cost:** FREE (within 5GB tier)

**Includes:**
- All active project documentation (*.md, README, CLAUDE.md)
- Code from active projects (*.py, *.js, *.ts, *.go, *.sh)
- Configuration files (package.json, pyproject.toml, Makefile, docker-compose.yml)
- Recent analytics and research (last 90 days)
- Command bible and standards

**Excludes:**
- Archive (067-archive/) - Move to Tier 2
- Old analytics (> 90 days) - Move to Tier 2
- Binary files, node_modules, .venv, build artifacts
- Secrets (004-security/)

**Estimated size:** ~4-5GB after filtering

---

### Tier 2: Complete Archive (Local SQLite - Unlimited)
**What:** EVERYTHING searchable on local disk (your backup + Bob's archive)
**Why:** Offline access, no cloud costs, full-text search, disaster recovery
**Cost:** FREE (local disk)

**Includes:**
- EVERYTHING from Tier 1 (duplicate for offline access)
- Archive directory (067-archive/)
- Old analytics (> 90 days)
- Full project history
- All markdown, code, configs (no binaries)
- RAW file backup paths (so Bob knows where binaries are)

**Storage:** `/home/jeremy/bobs-brain-archive.db`
**Size:** ~8-12GB SQLite database
**Query speed:** < 100ms for full-text search

**Bob can query this when:**
- "Search my archive for..."
- "Find old projects related to..."
- "When did I work on X?" (historical queries)

**Your backup strategy:**
- Local SQLite: Immediate backup
- External drive: Weekly rsync (your existing practice)
- No cloud costs!

---

## Implementation Plan

### Phase 1: Optimize for 5GB Free Tier (Tonight - 30 min)

**1. Filter smart (keep Tier 1 under 5GB):**
```bash
# Update collect-all-project-docs.sh to be smarter
INCLUDE:
  *.md, *.txt, README*, CLAUDE.md
  *.py, *.js, *.ts, *.go, *.rs, *.sh, *.yaml
  package.json, pyproject.toml, Makefile, Dockerfile
  Recent analytics (< 90 days)
  Command bible

EXCLUDE:
  067-archive/           → Move to SQLite
  001-analytics/old/     → Move to SQLite (> 90 days)
  node_modules/, .venv/, __pycache__
  *.log, *.db, *.sqlite (except important ones)
  Binary files (*.jpg, *.png, *.pdf, *.zip)
  Build artifacts (dist/, build/, target/)
```

**2. Run filtered collection:**
```bash
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent
./collect-smart-knowledge.sh  # New script (creates this)
```

**3. Ingest to Vertex AI:**
```bash
make data-ingestion
```

**Expected result:** 4-5GB in Vertex AI (within free tier)

---

### Phase 2: Build Local SQLite Archive (Tomorrow - 1 hour)

**1. Create SQLite database:**
```bash
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent
python3 build-sqlite-archive.py
```

**2. Index EVERYTHING (including archive):**
- Full-text search on all markdown/code
- Metadata (file path, size, modified date)
- Content embeddings (optional - can use sentence-transformers)

**3. Bob gets new tool: `search_archive(query)`**
- Queries local SQLite
- Returns results with file paths
- < 100ms response time

---

### Phase 3: Automate Daily Updates (Day 3 - 30 min)

**Nightly sync (2 AM cron job):**

1. **Scan for changes** (rsync-style)
2. **Hot knowledge (Tier 1):** Upload changed files to Vertex AI
3. **Warm archive (Tier 2):** Update SQLite with changes
4. **Cold backup (Tier 3):** rsync all to GCS, weekly to Wasabi

**Total time:** ~15 minutes/night (only changed files)

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│              /home/jeremy/ (67GB)                            │
│  ├── 000-projects/    (31GB) ← Active                       │
│  ├── 067-archive/     (8.9GB) ← Old                         │
│  ├── 001-analytics/   (8.1GB) ← Mixed                       │
│  └── ... (other dirs)                                       │
└─────────────┬───────────────────────────────────────────────┘
              │
              │ Smart Filtering
              ▼
┌─────────────────────────────────────────────────────────────┐
│         TIER 1: HOT KNOWLEDGE (Vertex AI - 5GB)             │
│         ✅ FREE TIER                                        │
├─────────────────────────────────────────────────────────────┤
│  • Active project docs (*.md, README, CLAUDE.md)            │
│  • Active code (*.py, *.js, *.ts, *.go, *.sh)              │
│  • Configs (package.json, Makefile, docker-compose.yml)     │
│  • Recent analytics (< 90 days)                             │
│  • Command bible & standards                                │
│  • Size: ~4-5GB                                             │
│  • Query speed: < 2 seconds                                 │
│  • Cost: FREE                                               │
└─────────────────────────────────────────────────────────────┘
              │
              │ Archive moves here
              ▼
┌─────────────────────────────────────────────────────────────┐
│      TIER 2: WARM ARCHIVE (Local SQLite - 8-12GB)          │
│      ✅ FREE (local disk)                                   │
├─────────────────────────────────────────────────────────────┤
│  • Everything from Tier 1 (offline copy)                    │
│  • Archive (067-archive/)                                   │
│  • Old analytics (> 90 days)                                │
│  • Full project history                                     │
│  • Full-text search                                         │
│  • Size: ~8-12GB                                            │
│  • Query speed: < 100ms                                     │
│  • Cost: FREE                                               │
└─────────────────────────────────────────────────────────────┘
              │
              │ Full backup
              ▼
┌─────────────────────────────────────────────────────────────┐
│       TIER 3: COLD BACKUP (GCS + Wasabi - 67GB)            │
│       💰 ~$20/month                                         │
├─────────────────────────────────────────────────────────────┤
│  • RAW everything (no filtering)                            │
│  • All binaries, node_modules, builds                       │
│  • Version history (30 days on GCS)                         │
│  • Offsite disaster recovery (Wasabi)                       │
│  • Bob NEVER queries this (pure backup)                     │
│  • Cost: $15 (GCS) + $4 (Wasabi) = $19/month               │
└─────────────────────────────────────────────────────────────┘
```

---

## What Bob Can Answer (After Phase 1)

**Immediately (Tier 1 - Vertex AI):**
- "What's the architecture of the hustle project?"
- "Show me all CLAUDE.md files"
- "Find code related to authentication"
- "What's in the command bible about deployments?"
- "Explain the iams project structure"

**After Phase 2 (Tier 2 - SQLite):**
- "Search my archive for old projects about X"
- "When did I last work on Y?"
- "Find analytics from 6 months ago"
- "Show me all projects I've ever worked on"

---

## Storage Optimization Rules

### Keep in Tier 1 (Hot - Vertex AI 5GB):
✅ Documentation that changes frequently
✅ Code from active projects
✅ Recent research/analytics (< 90 days)
✅ Standards and command references

### Move to Tier 2 (Warm - SQLite):
📦 Archive projects (067-archive/)
📦 Old analytics (> 90 days)
📦 Historical project versions
📦 Completed/deprecated code

### Keep in Tier 3 ONLY (Cold - GCS/Wasabi):
❄️ Binaries (images, PDFs, videos)
❄️ Dependencies (node_modules, .venv)
❄️ Build artifacts (dist/, build/)
❄️ Log files (*.log)

---

## Cost Breakdown

| Tier | Storage | Service | Monthly Cost |
|------|---------|---------|--------------|
| Tier 1 | 5GB | Vertex AI Search | **FREE** |
| Tier 2 | 8-12GB | Local SQLite | **FREE** |
| **Total** | **~15GB usable** | | **$0/month** |

**Queries (1000/month):**
- Vertex AI Search: **FREE** (within free tier)
- Gemini inference: **FREE** (1,500 req/day free tier)
- SQLite: **FREE** (local)

**Grand Total: $0/month** 🎉

---

## Quick Start Commands

### Tonight (Phase 1):

```bash
cd /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent

# 1. Create smart collection script
cat > collect-smart-knowledge.sh << 'EOF'
#!/bin/bash
# Smart knowledge collection - optimized for 5GB Vertex AI free tier
# Excludes: archive, old analytics, binaries, build artifacts

KNOWLEDGE_BASE_DIR="./knowledge-base"
mkdir -p "$KNOWLEDGE_BASE_DIR"
rm -rf "$KNOWLEDGE_BASE_DIR"/*

echo "Collecting HOT knowledge (active projects only)..."

# Active projects (exclude archive)
find /home/jeremy/000-projects -type f \
  \( -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.ts" \
     -o -name "*.go" -o -name "*.sh" -o -name "*.yaml" \
     -o -name "package.json" -o -name "pyproject.toml" -o -name "Makefile" \) \
  ! -path "*/067-archive/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/.venv/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  -exec cp --parents {} "$KNOWLEDGE_BASE_DIR/" \;

# Command bible
find /home/jeremy/002-command-bible -name "*.md" -exec cp --parents {} "$KNOWLEDGE_BASE_DIR/" \;

# Recent analytics (last 90 days)
find /home/jeremy/001-analytics -name "*.md" -mtime -90 -exec cp --parents {} "$KNOWLEDGE_BASE_DIR/" \;

echo "Collection complete!"
du -sh "$KNOWLEDGE_BASE_DIR"
EOF

chmod +x collect-smart-knowledge.sh

# 2. Run collection
./collect-smart-knowledge.sh

# 3. Upload to Vertex AI
make data-ingestion

# 4. Test Bob in Slack!
```

---

## Database Audit Results

**Your jeremy user:**
- ✅ No PostgreSQL databases (good!)
- ✅ 1 cron job: Weekly analytics auto-ingest (Saturdays 3 AM)

**admincostplus user (separate):**
- ✅ PostgreSQL 16 running (production CostPlus databases)
- ✅ 13 cron jobs for monitoring/security (all working)
- ⚠️ pgbackrest archiver error (their monitoring script `check-wal-archiving.sh` runs every 5 min to catch this)

**No action needed on your part** - the admincostplus user's monitoring is handling the archiver error.

---

## Next Steps

**Tonight:**
1. ✅ Slack webhook fixed (deployed)
2. Run Phase 1 (collect smart knowledge, ingest to Vertex AI)
3. Test Bob in Slack with real queries
4. Verify 5GB limit not exceeded

**Tomorrow:**
1. Build SQLite archive (Phase 2)
2. Give Bob `search_archive()` tool
3. Test historical queries

**Day 3:**
1. Set up daily automation
2. Configure GCS + Wasabi backup
3. Bob fully operational + backed up

---

**Let's roll! Ready to run Phase 1?**

