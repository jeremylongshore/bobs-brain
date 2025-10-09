# Bob's Avatar Training Data Architecture

**Date:** 2025-10-05
**Question:** Where to train Bob with your avatars/personal data?
**Key Issue:** If data is local, how does cloud Bob access it?

---

## Understanding "Avatar Training"

**What is avatar training?**
- Building knowledge base with YOUR expertise
- Teaching Bob YOUR communication style
- Loading YOUR documents, preferences, context
- Creating a "digital twin" that thinks like you

**Bob's learning systems:**
1. **Knowledge Orchestrator** - 77,264 documents (research, docs)
2. **Circle of Life** - Learns from conversations, corrections
3. **Vector Store (Chroma)** - Semantic search on documents
4. **SQLite DB** - Structured knowledge, FTS search
5. **Neo4j Graph** (optional) - Relationship mapping

---

## The Core Challenge

### Problem: Data Privacy vs Cloud Access

```
Your Personal Data (Local)
- Resume, work history
- Personal docs, notes
- Private conversations
- Preferences, habits
- Proprietary knowledge

         ↓

    WHERE SHOULD THIS LIVE?

         ↓

Cloud Bob (Production)        Local Bob (Development)
- Needs access to respond     - Has direct access
- Running 24/7 in cloud       - Only when PC on
- Serving Slack requests      - Fast local access
```

**Dilemma:**
- **Option A:** Upload personal data to cloud → Privacy risk
- **Option B:** Keep data local → Cloud Bob can't access it
- **Option C:** Hybrid architecture → Complexity

---

## Architecture Options

### Option 1: Everything in Cloud ☁️

**Architecture:**
```
Your Personal Data
    ↓ Upload once
Google Cloud Storage (private bucket)
    ↓
Cloud Run (Bob)
    ├── Reads from Cloud Storage
    ├── Vector DB (Chroma in memory)
    ├── Knowledge DB (SQLite ephemeral)
    └── Learns from Slack conversations
    ↓
Persistent Storage:
    ├── Cloud SQL (structured data)
    ├── Cloud Storage (documents)
    └── Vertex AI Vector Search (embeddings)
```

**How it works:**
1. **One-time upload:** Upload your training docs to Cloud Storage
2. **Bob reads on startup:** Loads knowledge into memory
3. **Persistent learning:** Circle of Life stores in Cloud SQL
4. **Always available:** Cloud Bob has everything

**Privacy controls:**
- Private bucket (only Bob's service account can read)
- Encryption at rest (Google default)
- Encryption in transit (HTTPS)
- VPC networking (isolated network)
- Audit logs (who accessed what)

✅ **PROS:**
- Cloud Bob has full access 24/7
- Fast access (in same data center)
- Persistent storage (survives restarts)
- Scales automatically
- Professional setup

❌ **CONS:**
- Personal data in Google's cloud
- Must trust Google's security
- Data subject to subpoenas
- Costs more ($10-30/month extra)

**Cost breakdown:**
| Component | Monthly Cost |
|-----------|--------------|
| Cloud Run (base) | $5-15 |
| Cloud Storage | $1-5 (per GB) |
| Cloud SQL (small) | $10-20 |
| Vertex AI Vector | $10-30 |
| **Total** | **$26-70/month** |

**Setup:**
```bash
# 1. Create Cloud Storage bucket
gsutil mb -p bobs-house-ai gs://bobs-brain-knowledge

# 2. Upload training data
gsutil -m cp -r ~/Documents/training-data/* gs://bobs-brain-knowledge/

# 3. Set permissions (private)
gsutil iam ch serviceAccount:bob@bobs-house-ai.iam.gserviceaccount.com:objectViewer \
  gs://bobs-brain-knowledge

# 4. Deploy Bob with access
gcloud run deploy bobs-brain \
  --set-env-vars "KNOWLEDGE_BUCKET=bobs-brain-knowledge"
```

---

### Option 2: Everything Local 💻

**Architecture:**
```
Your Personal Data (Local)
    ↓
Local Bob (Flask on your PC)
    ├── Direct file access
    ├── SQLite (77,264 docs)
    ├── Chroma vector store
    ├── Circle of Life learning
    └── No cloud, no upload
    ↓
Slack (via ngrok tunnel)
```

**How it works:**
1. **Training data local:** Everything in `~/Documents/`, `~/research/`
2. **Bob reads locally:** Direct filesystem access
3. **Learning persists:** SQLite/Chroma on your disk
4. **Slack via ngrok:** Tunnel for webhooks

✅ **PROS:**
- **Maximum privacy** - data never leaves your machine
- **Full control** - you own everything
- **No cloud costs** - just electricity
- **Direct access** - fastest possible
- **Easy updates** - just edit local files

❌ **CONS:**
- **No 24/7** - offline when PC off
- **ngrok hassle** - URL changes, Slack config pain
- **Single machine** - no redundancy
- **Limited scale** - your PC only

**Cost:** $2-10/month (electricity + ngrok)

**Setup:**
```bash
# 1. Organize training data locally
mkdir -p ~/bobs-training-data
cp -r ~/Documents/work ~/bobs-training-data/
cp -r ~/Documents/personal ~/bobs-training-data/

# 2. Configure Bob to read local data
cat >> .env <<EOF
KNOWLEDGE_DIR=/home/jeremy/bobs-training-data
TRAINING_DATA_PATH=/home/jeremy/Documents
EOF

# 3. Ingest into knowledge DB
cd ~/projects/bobs-brain
python scripts/ingest_knowledge.py ~/bobs-training-data

# 4. Start Bob locally
python -m flask --app src.app run --port 8080

# 5. Expose with ngrok
ngrok http 8080
```

---

### Option 3: Hybrid - General in Cloud, Personal Local 🔀

**Architecture:**
```
Cloud Bob (Production)
    ├── General knowledge (public docs)
    ├── Slack integration
    ├── 24/7 availability
    └── API: /api/query (X-API-Key required)

         +

Local Bob (Personal Knowledge)
    ├── Your personal data
    ├── Private documents
    ├── Development/testing
    └── API: localhost:8080/api/query

Strategy:
    ├── Team queries → Cloud Bob
    ├── Personal queries → Local Bob (when PC on)
    └── Fallback: Cloud Bob says "ask local Bob for personal stuff"
```

**How it works:**
1. **Cloud Bob:** General knowledge, handles most Slack requests
2. **Local Bob:** Personal data, you query directly when needed
3. **Clear separation:** Public vs private knowledge
4. **Best of both:** 24/7 availability + privacy

✅ **PROS:**
- Privacy preserved (personal data stays local)
- 24/7 Slack for general queries
- Fast local access for personal stuff
- Reasonable cost ($5-15/month)

❌ **CONS:**
- Two separate Bobs (some confusion)
- Personal queries only work when PC on
- Must remember which Bob to ask

**Cost:** $5-15/month (cloud only, local is free)

---

### Option 4: Local Primary + Cloud Sync 🔄

**Architecture:**
```
Local Bob (Primary)
    ├── All training data
    ├── Full knowledge base
    ├── Learning from corrections
    └── Exports knowledge snapshots
         ↓
    [Sync Script - Daily/Weekly]
         ↓
Cloud Bob (Replica)
    ├── Receives knowledge exports
    ├── Loads into memory
    ├── Serves Slack 24/7
    └── Slightly stale (1 day behind)
```

**How it works:**
1. **Train locally:** All avatar data on your machine
2. **Bob learns:** Circle of Life updates knowledge
3. **Export daily:** Script exports knowledge base
4. **Upload to cloud:** Encrypted upload to Cloud Storage
5. **Cloud loads on startup:** Reads latest snapshot

**Sync script:**
```bash
#!/bin/bash
# sync-knowledge-to-cloud.sh
# Run daily via cron

set -e

echo "Exporting local knowledge..."
cd ~/projects/bobs-brain

# Export SQLite knowledge DB
sqlite3 bb.db ".backup /tmp/bb_snapshot.db"

# Export Chroma embeddings
tar czf /tmp/chroma_snapshot.tar.gz .chroma/

# Encrypt before upload (for extra security)
gpg --encrypt --recipient bob@bobs-house-ai \
  /tmp/bb_snapshot.db \
  /tmp/chroma_snapshot.tar.gz

# Upload to cloud
gsutil cp /tmp/bb_snapshot.db.gpg gs://bobs-brain-knowledge/
gsutil cp /tmp/chroma_snapshot.tar.gz.gpg gs://bobs-brain-knowledge/

# Trigger cloud restart to load new data
gcloud run services update bobs-brain \
  --region us-central1 \
  --update-env-vars KNOWLEDGE_VERSION=$(date +%Y%m%d)

echo "✅ Knowledge synced to cloud"
```

**Cron setup:**
```bash
# Edit crontab
crontab -e

# Add daily sync at 3am
0 3 * * * /home/jeremy/projects/bobs-brain/scripts/sync-knowledge-to-cloud.sh
```

✅ **PROS:**
- Best of both worlds
- Privacy maintained (data local first)
- Cloud Bob stays updated
- Can audit what goes to cloud
- Encrypted uploads

❌ **CONS:**
- Cloud data slightly stale (1 day behind)
- Sync complexity
- Must manage encryption keys
- Cloud storage costs ($5-15/month)

**Cost:** $10-25/month (cloud + storage)

---

### Option 5: Cloud Bob Calls Local API 🌐 ← 💻

**Architecture:**
```
Cloud Bob (Slack Handler)
    ├── Receives Slack message
    ├── Determines if needs personal knowledge
    └── Calls: https://jeremy-home.dyndns.org/bob-api
         ↓
    [Internet / VPN]
         ↓
Local Bob API (Your PC)
    ├── Secure API endpoint
    ├── Requires API key
    ├── Has full personal knowledge
    └── Returns answer
         ↓
Cloud Bob
    └── Sends answer to Slack
```

**How it works:**
1. **Cloud Bob:** Lightweight, handles Slack
2. **Personal queries:** Forwards to your local Bob API
3. **Local Bob:** Responds with personal knowledge
4. **Cloud relays:** Sends answer back to Slack

**Requirements:**
- **Static IP or DynamicDNS** - Cloud needs to reach your PC
- **Port forward** - Router must allow incoming
- **API key auth** - Secure the endpoint
- **Your PC must be on** - Falls back if offline

✅ **PROS:**
- Personal data never uploaded
- Cloud handles Slack 24/7
- Local only accessed when needed
- Clear separation

❌ **CONS:**
- Network complexity (port forward, DNS)
- Your PC must be on for personal queries
- Latency (cloud → internet → your home → back)
- Security concerns (exposed endpoint)

**Setup:**
```bash
# 1. Local Bob exposes API
# Edit .env
echo "API_MODE=server" >> .env
echo "API_KEY=$(openssl rand -hex 32)" >> .env

# Start Bob API
python -m flask --app src.app run --host 0.0.0.0 --port 8080

# 2. Configure router port forwarding
# Forward external port 8443 → your PC 8080

# 3. Set up DynamicDNS (e.g., noip.com)
# jeremy-home.ddns.net → your dynamic IP

# 4. Cloud Bob configured to call you
# Cloud Run env var:
# PERSONAL_KNOWLEDGE_API=https://jeremy-home.ddns.net:8443
# PERSONAL_API_KEY=<your-api-key>
```

---

## Recommendation Matrix

| Your Priority | Best Option | Cost/Month | Complexity |
|---------------|-------------|------------|------------|
| **Maximum privacy** | Local only (Option 2) | $2-10 | Low |
| **24/7 Slack** | Hybrid (Option 3) | $5-15 | Medium |
| **Best of both** | Local + Sync (Option 4) | $10-25 | High |
| **Professional** | Everything Cloud (Option 1) | $26-70 | Medium |
| **Advanced** | Cloud calls Local (Option 5) | $5-15 | Very High |

---

## Recommended: Option 4 (Local + Cloud Sync)

**For you specifically, Jeremy:**

✅ **Train locally** - All personal data on your PC
✅ **Export daily** - Sync knowledge to cloud automatically
✅ **Cloud serves Slack** - 24/7 availability
✅ **Privacy preserved** - You control what syncs
✅ **Development speed** - Fast local iteration

### Implementation Plan

**Phase 1: Set Up Local Training (Week 1)**
```bash
# 1. Organize training data
mkdir -p ~/bobs-training-data/{documents,code,personal,work}

# 2. Copy your avatar data
cp -r ~/Documents/resume ~/bobs-training-data/personal/
cp -r ~/Documents/projects ~/bobs-training-data/work/
cp -r ~/Documents/notes ~/bobs-training-data/personal/

# 3. Ingest into Bob's knowledge DB
cd ~/projects/bobs-brain
python scripts/ingest_knowledge.py ~/bobs-training-data

# 4. Verify ingestion
sqlite3 bb.db "SELECT COUNT(*) FROM knowledge"
# Should show 77,264+ documents
```

**Phase 2: Train Circle of Life (Week 2)**
```bash
# Start local Bob
python -m flask --app src.app run --port 8080

# Test and correct Bob
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query":"Tell me about my work experience"}'

# Submit corrections
curl -X POST http://localhost:8080/learn \
  -H "Content-Type: application/json" \
  -d '{
    "correction": "When discussing work, mention 15 years in tech",
    "context": "User bio and experience"
  }'
```

**Phase 3: Set Up Cloud Sync (Week 3)**
```bash
# 1. Create sync script
nano scripts/sync-knowledge-to-cloud.sh
# (Use script from Option 4 above)

# 2. Make executable
chmod +x scripts/sync-knowledge-to-cloud.sh

# 3. Test manual sync
./scripts/sync-knowledge-to-cloud.sh

# 4. Set up daily cron
crontab -e
# Add: 0 3 * * * /home/jeremy/projects/bobs-brain/scripts/sync-knowledge-to-cloud.sh
```

**Phase 4: Deploy Cloud Bob (Week 4)**
```bash
# Deploy with knowledge loading
./05-Scripts/deploy/deploy-to-cloudrun.sh

# Cloud Bob downloads knowledge on startup from Cloud Storage
# Loads into memory, serves Slack
```

---

## Security Best Practices

### Encrypting Personal Data

**Option A: GPG Encryption**
```bash
# Encrypt before upload
gpg --encrypt --recipient bob@bobs-house-ai knowledge.db

# Cloud decrypts on load (requires private key)
```

**Option B: Google KMS**
```bash
# Encrypt with Cloud KMS
gcloud kms encrypt \
  --key bob-knowledge-key \
  --keyring bob-keyring \
  --location us-central1 \
  --plaintext-file knowledge.db \
  --ciphertext-file knowledge.db.enc

# Upload encrypted
gsutil cp knowledge.db.enc gs://bobs-brain-knowledge/

# Cloud Bob decrypts automatically (has KMS permissions)
```

### Access Controls

**Minimal permissions:**
```yaml
Cloud Storage Bucket:
  - Bob's service account: Read only
  - Your account: Read/Write
  - Everyone else: No access

Secret Manager:
  - Bob's service account: Access secrets
  - Audit logs: Enabled

Cloud Run:
  - Service account: bob-brain@bobs-house-ai.iam.gserviceaccount.com
  - VPC: private network (optional)
  - Ingress: Slack webhook only
```

### Audit What Gets Synced

**Pre-sync filter:**
```python
# scripts/filter_knowledge.py
"""
Filter personal data before cloud sync
"""

EXCLUDE_PATTERNS = [
    "**/private/**",
    "**/secret/**",
    "**/*_personal.md",
    "**/passwords/**",
]

def should_sync(filepath):
    """Return False if file should stay local"""
    for pattern in EXCLUDE_PATTERNS:
        if filepath.match(pattern):
            return False
    return True

# Use in sync script
for file in knowledge_files:
    if should_sync(file):
        upload_to_cloud(file)
    else:
        print(f"Skipping private file: {file}")
```

---

## Data Access Patterns

### Where Cloud Bob Gets Data

```
Cloud Bob Memory (Runtime):
├── Startup: Load from Cloud Storage
│   ├── knowledge.db (SQLite)
│   ├── chroma/ (vector embeddings)
│   └── config.json
├── During conversation:
│   ├── Query knowledge DB (in memory)
│   ├── Search Chroma vectors
│   └── Call Gemini API
└── Learning:
    └── Store in Cloud SQL (persistent)

Cloud Bob doesn't:
❌ Access your local filesystem
❌ Connect to your PC
❌ Read from ~/Documents
❌ Access local SQLite directly
```

### Where Local Bob Gets Data

```
Local Bob (Your PC):
├── Direct filesystem access:
│   ├── ~/bobs-training-data/
│   ├── ~/Documents/
│   ├── ~/projects/
│   └── ~/research/
├── Local databases:
│   ├── ./bb.db (SQLite)
│   ├── ./.chroma/ (vectors)
│   └── ./artifacts/
└── Learning:
    └── Persists to local SQLite

Local Bob can:
✅ Read any file on your PC
✅ Access local databases
✅ Run scripts to gather data
✅ Monitor filesystem changes
```

---

## Next Steps

**Immediate (Today):**
1. Decide which option fits your needs
2. Organize training data locally
3. Test ingestion into local Bob

**This Week:**
1. Train local Bob with your avatar data
2. Submit corrections to Circle of Life
3. Verify knowledge base is accurate

**Next Week:**
1. Set up sync script (if using Option 4)
2. Deploy cloud Bob
3. Configure Slack

**Ongoing:**
1. Train Bob with new documents
2. Submit corrections as needed
3. Monitor cloud sync logs

---

## FAQ

**Q: How much personal data can Bob handle?**
A: Current setup: 77,264 documents. Can scale to millions with proper indexing.

**Q: Will cloud Bob have real-time access to my data?**
A: Option 1 (yes), Option 4 (1-day lag), Option 5 (yes but requires PC on)

**Q: Can I delete data from cloud later?**
A: Yes, delete from Cloud Storage bucket. Bob loads on startup.

**Q: What if I don't want ANY data in cloud?**
A: Use Option 2 (local only) or Option 3 (hybrid, cloud gets general knowledge only)

**Q: How do I update cloud Bob's knowledge?**
A: Re-run sync script, or manually upload to Cloud Storage and restart service

**Q: Can cloud Bob learn from Slack conversations?**
A: Yes, Circle of Life can store learnings in Cloud SQL (persistent)

---

## Cost Summary

| Option | Monthly Cost | Setup Time | Privacy | 24/7 Access |
|--------|--------------|------------|---------|-------------|
| **1. Everything Cloud** | $26-70 | 1 hour | Low | ✅ |
| **2. Everything Local** | $2-10 | 30 min | ✅ High | ❌ |
| **3. Hybrid** | $5-15 | 1 hour | ✅ High | Partial |
| **4. Local + Sync** | $10-25 | 2 hours | Medium | ✅ |
| **5. Cloud Calls Local** | $5-15 | 3 hours | ✅ High | Partial |

**Recommended: Option 4** - $10-25/month, best balance

---

**Created:** 2025-10-05
**Status:** ✅ Complete analysis
**Recommendation:** Local training + daily sync to cloud
**Next:** Organize training data, start local ingestion

