# Bob's Complete Knowledge + Backup Architecture

**Created:** 2025-11-09
**Purpose:** Bob as complete knowledge extension + backup system

---

## Overview

Bob becomes:
1. **Knowledge AI** - Answers questions about all your work
2. **Version Tracker** - Tracks changes over time
3. **Backup System** - 3-tier backup of all life work
4. **Analytics Engine** - Analyzes progress, patterns, trends

---

## Current State

- **Total Data:** 67GB in /home/jeremy/
- **Projects:** 31GB in 000-projects/
- **Current Bob Knowledge:** 302 files (3.8MB) - way too small!

---

## Proposed Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                                │
├─────────────────────────────────────────────────────────────────┤
│  /home/jeremy/                                                   │
│  ├── 000-projects/ (31GB) ← All active projects                │
│  ├── 001-analytics/        ← Analytics data                     │
│  ├── 002-command-bible/    ← Commands & standards              │
│  ├── 003-research/         ← Research & knowledge base          │
│  ├── 004-security/         ← Credentials (EXCLUDE from Bob!)    │
│  ├── 067-archive/          ← Old projects (include for history) │
│  └── ... (all other dirs)                                       │
│                                                                  │
│  Google Drive (via rclone)                                      │
│  ├── Documents/                                                 │
│  ├── Projects/                                                  │
│  └── Archive/                                                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Daily Ingestion
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FILTERING & PROCESSING                         │
├─────────────────────────────────────────────────────────────────┤
│  • Extract documentation (*.md, *.txt, README*, CLAUDE.md)      │
│  • Include code (*.py, *.js, *.ts, *.go, *.rs, *.java)         │
│  • Exclude: node_modules/, .venv/, __pycache__/, .git/objects  │
│  • Exclude: Credentials, .env files, API keys                   │
│  • Track changes (git diff style)                               │
│  • Generate metadata (timestamps, file sizes, hashes)           │
│  • Estimated filtered size: 5-10GB                              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TIER 1: BOB'S KNOWLEDGE BASE                   │
│                  (Vertex AI Search)                             │
├─────────────────────────────────────────────────────────────────┤
│  • Purpose: Fast semantic search for AI queries                 │
│  • Storage: ~5-10GB after filtering                             │
│  • Embeddings: text-embedding-005                               │
│  • Query speed: < 2 seconds                                     │
│  • Cost: ~$50-100/month                                         │
│  • Daily updates: Incremental only (changed files)              │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Backup
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              TIER 2: PRIMARY BACKUP (GCS)                       │
│              gs://bobs-brain-life-work-backup/                  │
├─────────────────────────────────────────────────────────────────┤
│  • Purpose: Full backup of ALL data (unfiltered)                │
│  • Storage: Full 67GB + Google Drive                            │
│  • Versioning: Keep 30 days of versions                         │
│  • Lifecycle: Archive to Coldline after 90 days                 │
│  • Cost: ~$15/month (Standard) + $5/month (Coldline)            │
│  • Daily snapshots with rsync                                   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Replicate
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│          TIER 3: OFFSITE BACKUP (Wasabi)                       │
│          s3://jeremy-life-work-backup/                          │
├─────────────────────────────────────────────────────────────────┤
│  • Purpose: Disaster recovery (offsite, different provider)     │
│  • Storage: Full 67GB                                           │
│  • Versioning: Keep 90 days                                     │
│  • Cost: ~$4/month (Wasabi flat rate, no egress fees)           │
│  • Weekly sync from GCS                                         │
│  • Immutable: Cannot be deleted for 90 days                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ Local Copy
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│          TIER 4: LOCAL BACKUP (SQLite + Embeddings)            │
│          /home/jeremy/bob-local-knowledge.db                    │
├─────────────────────────────────────────────────────────────────┤
│  • Purpose: Offline access, bare metal restore                  │
│  • Storage: SQLite database with full-text search               │
│  • Embeddings: Stored as vectors in SQLite                      │
│  • Size: ~8-12GB (includes embeddings)                          │
│  • Cost: FREE (local disk)                                      │
│  • Daily update from filtered files                             │
│  • Queryable with SQL                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow - Daily Automation

**Every Night at 2 AM:**

1. **Collection** (10 minutes)
   - Scan /home/jeremy/ for changes
   - Mount Google Drive (rclone)
   - Identify new/modified files
   - Apply exclusion filters

2. **Tier 1 - Bob's Knowledge** (30 minutes)
   - Upload changed files to GCS staging
   - Run Vertex AI data ingestion pipeline
   - Update embeddings for changed docs
   - Delete embeddings for removed files

3. **Tier 2 - GCS Backup** (20 minutes)
   - rsync ALL files to gs://bobs-brain-life-work-backup/
   - Create daily snapshot
   - Apply lifecycle rules

4. **Tier 3 - Wasabi Backup** (Once/week - 60 minutes)
   - Sync from GCS to Wasabi
   - Verify checksums
   - Update manifest

5. **Tier 4 - Local SQLite** (15 minutes)
   - Generate embeddings locally (sentence-transformers)
   - Update SQLite database
   - Vacuum and optimize

**Total Daily Time:** ~75 minutes
**Weekly Time:** +60 minutes (Wasabi sync)

---

## File Filtering Strategy

### INCLUDE (for Bob's Knowledge)

**Documentation:**
- `*.md` (Markdown)
- `*.txt` (Text files)
- `README*`, `CLAUDE.md`, `CHANGELOG*`
- `01-Docs/`, `docs/`, `claudes-docs/`

**Code:**
- `*.py` (Python)
- `*.js`, `*.ts`, `*.jsx`, `*.tsx` (JavaScript/TypeScript)
- `*.go` (Go)
- `*.rs` (Rust)
- `*.java` (Java)
- `*.sh`, `*.bash` (Shell scripts)
- `*.yaml`, `*.yml` (Config files)
- `Makefile`, `Dockerfile`

**Configuration:**
- `package.json`, `pyproject.toml`, `Cargo.toml`
- `.gitignore`, `.env.example`
- Terraform files (`*.tf`)

### EXCLUDE (Security/Size)

**Security (NEVER ingest):**
- `004-security/` (entire directory)
- `*.key`, `*.pem`, `*.crt`
- `.env` (actual secrets)
- `credentials.json`, `serviceAccount.json`
- SSH keys (`id_rsa`, `id_ed25519`)

**Size/Noise:**
- `node_modules/`
- `.venv/`, `venv/`, `adk-venv/`
- `__pycache__/`, `*.pyc`
- `.git/objects/` (keep .git/config)
- `*.log` (keep last 100 lines only)
- Binary files: `*.jpg`, `*.png`, `*.pdf`, `*.zip`, `*.tar.gz`
- Build artifacts: `dist/`, `build/`, `target/`

---

## Change Tracking & Analytics

Bob tracks:
- **File changes:** Daily diffs
- **Code evolution:** Lines added/removed per project
- **Documentation updates:** Which docs changed
- **Project activity:** Which projects are active
- **Knowledge gaps:** What's missing documentation

**Example Queries Bob Can Answer:**
- "What changed in the hustle project this week?"
- "Show me all projects that haven't been updated in 30 days"
- "What are my most active projects this month?"
- "Compare the claude-code-plugins architecture from last month vs now"
- "What documentation is missing from my projects?"
- "Show my coding patterns over the last year"

---

## Cost Breakdown

### Monthly Recurring Costs

| Tier | Service | Storage | Cost/Month |
|------|---------|---------|------------|
| Tier 1 | Vertex AI Search | 5-10GB | $50-100 |
| Tier 2 | GCS Standard | 67GB | $15 |
| Tier 2 | GCS Coldline (archive) | 67GB | $5 |
| Tier 3 | Wasabi | 67GB | $4 |
| Tier 4 | Local SQLite | 8-12GB | FREE |
| **TOTAL** | | **~200GB** | **$74-124/month** |

### Query Costs (Per 1000 Queries)

| Operation | Cost |
|-----------|------|
| Vertex AI Search queries | $1.50 |
| Gemini 2.5 Flash inference | $0.20 |
| Embeddings (text-embedding-005) | $0.05 |
| **Total per 1000 queries** | **$1.75** |

### Ingestion Costs (Daily)

| Operation | Cost/Day | Cost/Month |
|-----------|----------|------------|
| Data ingestion pipeline | $0.10 | $3 |
| Embeddings (changed files) | $0.05 | $1.50 |
| GCS operations | $0.01 | $0.30 |
| **Total daily operations** | **$0.16** | **$4.80** |

**Grand Total: ~$80-130/month** (depending on usage)

---

## Implementation Plan

### Phase 1: Expand Bob's Knowledge (Week 1)

**Day 1-2:**
- [x] Collect from selected projects (DONE - 302 files)
- [ ] Expand to ALL /home/jeremy/ directories
- [ ] Set up filtering rules
- [ ] Test with 1GB subset

**Day 3-4:**
- [ ] Full ingestion of filtered data (~5-10GB)
- [ ] Verify Vertex AI Search performance
- [ ] Test Bob's answers on expanded knowledge

**Day 5-7:**
- [ ] Tune filtering rules based on results
- [ ] Optimize cost vs coverage
- [ ] Document what's included/excluded

### Phase 2: Backup System (Week 2)

**Tier 2 - GCS Backup:**
- [ ] Create gs://bobs-brain-life-work-backup/
- [ ] Set up daily rsync script
- [ ] Configure lifecycle policies
- [ ] Test restore procedure

**Tier 3 - Wasabi Backup:**
- [ ] Sign up for Wasabi account
- [ ] Create S3 bucket
- [ ] Configure rclone for Wasabi
- [ ] Set up weekly sync

**Tier 4 - Local SQLite:**
- [ ] Install sentence-transformers
- [ ] Create SQLite schema
- [ ] Generate embeddings locally
- [ ] Build query interface

### Phase 3: Automation (Week 3)

**Daily Automation:**
- [ ] Create master sync script
- [ ] Set up cron job (2 AM daily)
- [ ] Configure GitHub Actions (backup)
- [ ] Add monitoring/alerting

**Google Drive Integration:**
- [ ] Install rclone
- [ ] Configure Google Drive mount
- [ ] Add Drive to daily sync
- [ ] Test bidirectional sync

### Phase 4: Analytics & Tracking (Week 4)

**Change Tracking:**
- [ ] Build diff tracking system
- [ ] Store diffs in BigQuery
- [ ] Create dashboards (Looker Studio)
- [ ] Set up weekly reports

**Bob Enhancements:**
- [ ] Add "show changes" tool
- [ ] Add "compare versions" tool
- [ ] Add "project analytics" tool
- [ ] Train on your coding patterns

---

## Automation Scripts

### Daily Sync Master Script

Location: `/home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent/daily-sync.sh`

Run via cron: `0 2 * * * /home/jeremy/000-projects/iams/bobs-brain/bob-vertex-agent/daily-sync.sh`

### Google Drive Setup

```bash
# Install rclone
curl https://rclone.org/install.sh | sudo bash

# Configure Google Drive
rclone config

# Mount Google Drive
mkdir -p /home/jeremy/gdrive
rclone mount gdrive: /home/jeremy/gdrive --daemon

# Add to daily sync
rsync -av /home/jeremy/gdrive/ gs://bobs-brain-life-work-backup/gdrive/
```

---

## Disaster Recovery

**Scenario 1: Bare Metal Restore**
1. Install fresh OS
2. Clone bob-vertex-agent repo
3. Restore from Tier 4 (local SQLite backup on external drive)
4. Bob can guide you through restoring from GCS/Wasabi

**Scenario 2: Bob Goes Down**
1. Local SQLite backup still works (offline)
2. Query with SQL directly
3. Restore Bob from GCS backup
4. Redeploy to Vertex AI

**Scenario 3: GCP Account Issues**
1. Tier 3 (Wasabi) has complete backup
2. Tier 4 (local) has knowledge base
3. Can migrate to AWS/Azure
4. Restore from Wasabi

---

## Privacy & Security

**What Bob NEVER Sees:**
- `/home/jeremy/004-security/` (entire directory)
- `.env` files with actual secrets
- Private keys, certificates
- Personal financial data
- Passwords, API keys

**What Bob Sees (Safe):**
- Documentation, code, architecture
- CLAUDE.md, README files
- Public configs (`.env.example`)
- Git history (commits, not objects)
- Command references

**Access Control:**
- Bob (Vertex AI) - Read-only to knowledge base
- You - Full control over all tiers
- Backups encrypted at rest
- Wasabi bucket has object lock (immutable)

---

## Benefits

**For You:**
1. **Ask Bob anything** about your 10 years of work
2. **Never lose data** - 3-tier backup strategy
3. **Track progress** - See how projects evolve
4. **Find patterns** - Bob analyzes your work style
5. **Quick context** - Bob knows all project details
6. **Historical analysis** - Compare any time period
7. **Disaster recovery** - Multiple restore options

**For Projects:**
1. **Instant onboarding** - Bob explains any project
2. **Code archaeology** - Find why decisions were made
3. **Best practices** - Bob learns from your patterns
4. **Consistency** - Bob ensures standards across projects
5. **Documentation** - Bob generates missing docs
6. **Refactoring** - Bob understands full context

---

## Next Steps

1. **Approve this architecture**
2. **Set budget** (~$100/month reasonable?)
3. **Choose what to include/exclude**
4. **Start Phase 1** (expand knowledge base)
5. **Set up backup tiers**
6. **Automate everything**

---

**Questions:**
1. Budget approval for ~$100/month?
2. Any specific directories to EXCLUDE?
3. Google Drive - do you want it included?
4. Analytics - what metrics matter most?
5. When should we start?
