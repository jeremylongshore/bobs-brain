# CLAUDE.md - Bob's Brain Documentation
**CRITICAL: This is the SINGLE SOURCE OF TRUTH for Bob's Brain project**

## 🚨 CRITICAL RULES - READ FIRST
1. **ONLY ONE CLOUD RUN INSTANCE**: There should only be ONE `bobs-brain` service on Cloud Run
2. **GITHUB IS ALWAYS TRUTH**: Always pull latest from GitHub before making changes
3. **USE LATEST CODE**: We use `bob_cloud_run.py` for Cloud Run (NOT bob_firestore.py or bob_ultimate.py)
4. **NO DUPLICATE SERVICES**: Delete any duplicate Cloud Run services immediately
5. **ALWAYS UPDATE GITHUB**: After ANY change, commit and push to GitHub

## 🤖 BOB'S BRAIN CURRENT STATUS
**Service:** bobs-brain (ONLY ONE - DELETE ANY DUPLICATES)
**Project:** bobs-house-ai  
**Cloud Run URL:** https://bobs-brain-157908567967.us-central1.run.app
**GitHub:** https://github.com/jeremylongshore/bobs-brain (branch: bobs-brain-birthed)
**Last Updated:** 2025-08-10T20:25:00Z
**Current Revision:** bobs-brain-00007-fb7

## ✅ DEPLOYMENT STATUS - LIVE ON CLOUD RUN!
- **Cloud Run:** ✅ DEPLOYED & RUNNING (Single instance only!)
- **Slack Tokens:** ✅ CONFIGURED in Cloud Run environment
- **Vertex AI:** ✅ Working (but DEPRECATED - dies June 2026)
- **Database:** ✅ Using FIRESTORE (projects/diagnostic-pro-mvp/databases/bob-brain)
- **Health Check:** https://bobs-brain-157908567967.us-central1.run.app/health
- **Slack Events:** https://bobs-brain-157908567967.us-central1.run.app/slack/events

## 📁 PROJECT STRUCTURE
```
/home/jeremylongshore/bobs-brain/
├── src/
│   ├── bob_cloud_run.py       # ✅ ACTIVE - Cloud Run HTTP server version
│   ├── bob_firestore.py       # ❌ NOT USED - Socket Mode version
│   ├── bob_ultimate.py        # ❌ NOT USED - Legacy version
│   ├── bob_legacy_v2.py       # ❌ NOT USED - Old backup
│   ├── knowledge_loader.py    # Shared knowledge base loader
│   └── migrate_to_firestore.py # One-time migration tool
├── requirements-cloudrun.txt  # ✅ MINIMAL deps for fast builds
├── requirements.txt           # ❌ HEAVY deps - DO NOT USE for Cloud Run
├── Dockerfile                 # ✅ Optimized for Cloud Run
├── SLACK_SETUP.md            # Slack configuration instructions
├── CLAUDE.md                 # THIS FILE - SINGLE SOURCE OF TRUTH
└── .gitignore                # Protects secrets from GitHub
```

## 🚀 HOW TO DEPLOY (CORRECT WAY)

### Prerequisites Check
```bash
# 1. ALWAYS check current status first
gcloud run services list --region us-central1 | grep bob

# 2. If you see multiple bob services, DELETE extras:
# gcloud run services delete [duplicate-service-name] --region us-central1

# 3. Pull latest from GitHub
cd ~/bobs-brain
git pull origin bobs-brain-birthed
```

### Deploy to Cloud Run
```bash
cd ~/bobs-brain

# Deploy using optimized Dockerfile and requirements-cloudrun.txt
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --project bobs-house-ai \
  --port 3000 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300 \
  --set-env-vars "SLACK_BOT_TOKEN=xoxb-[token],SLACK_APP_TOKEN=xapp-[token],SLACK_SIGNING_SECRET=[secret],GCP_PROJECT=bobs-house-ai"
```

## 🔧 SLACK CONFIGURATION

### Current Tokens (Store in Cloud Run env vars ONLY)
- **Bot Token:** xoxb-9318399480516-9316254671362-[rest]
- **App Token:** xapp-1-A099YKLCM1N-9312940498067-[rest]
- **Signing Secret:** d00942f9329d902a0af65f31f968f355

### Slack App Settings
1. Go to https://api.slack.com/apps
2. Event Subscriptions URL: `https://bobs-brain-157908567967.us-central1.run.app/slack/events`
3. Required OAuth Scopes:
   - chat:write
   - channels:history
   - im:history
   - groups:history
   - app_mentions:read

## 🧪 TESTING

### Test Health Check
```bash
curl https://bobs-brain-157908567967.us-central1.run.app/health
```

### Test Slack Integration
```bash
python3 test_slack_verification.py
```

### Check Logs
```bash
gcloud run services logs read bobs-brain --region us-central1 --limit 50
```

## ⚠️ COMMON PROBLEMS & SOLUTIONS

### Problem: Build takes forever
**Solution:** Use `requirements-cloudrun.txt` NOT `requirements.txt`

### Problem: Multiple Bob services running
**Solution:** Delete duplicates, keep only `bobs-brain`
```bash
gcloud run services delete [duplicate-name] --region us-central1
```

### Problem: Bob not responding in Slack
**Solution:** Check Event Subscriptions URL in Slack app settings

### Problem: Signature verification failing
**Solution:** URL verification is bypassed in bob_cloud_run.py (fixed on 2025-08-10)

### Problem: Code confusion/wrong version
**Solution:** ALWAYS use bob_cloud_run.py for Cloud Run, pull latest from GitHub

## 📝 DEVELOPMENT WORKFLOW

1. **ALWAYS START WITH:**
   ```bash
   cd ~/bobs-brain
   git pull origin bobs-brain-birthed
   ```

2. **Make changes locally**

3. **Test locally if needed:**
   ```bash
   PORT=5000 python3 src/bob_cloud_run.py
   ```

4. **Commit and push to GitHub:**
   ```bash
   git add [files]
   git commit -m "Clear description"
   git push origin bobs-brain-birthed
   ```

5. **Deploy to Cloud Run** (see deployment section above)

## 🔴 WHAT NOT TO DO
- ❌ DO NOT create multiple Cloud Run services
- ❌ DO NOT use requirements.txt for Cloud Run (too heavy)
- ❌ DO NOT use bob_firestore.py for Cloud Run (wrong mode)
- ❌ DO NOT commit secrets to GitHub (.env files)
- ❌ DO NOT deploy without pulling latest from GitHub first
- ❌ DO NOT use bob_ultimate.py or bob_legacy_v2.py (outdated)

## 📊 PROJECT HISTORY
- **2025-08-10:** Fixed Cloud Run deployment with optimized dependencies
- **2025-08-10:** Fixed Slack URL verification issue
- **2025-08-10:** Migrated to Firestore from ChromaDB
- **2025-08-09:** Bob's Brain birthed and initial recovery
- **Past 3 days:** Bob has been working successfully when properly configured

## 🎯 NEXT SESSION CHECKLIST
When starting a new session, ALWAYS:
1. Read this CLAUDE.md file first
2. Check Cloud Run status: `gcloud run services list --region us-central1 | grep bob`
3. Pull latest from GitHub: `git pull origin bobs-brain-birthed`
4. Verify single instance: Delete any duplicate services
5. Test health: `curl https://bobs-brain-157908567967.us-central1.run.app/health`

## 🆘 EMERGENCY RECOVERY
If Bob is completely broken:
1. The working code is in GitHub: https://github.com/jeremylongshore/bobs-brain
2. Branch: `bobs-brain-birthed`
3. Use `bob_cloud_run.py` with `requirements-cloudrun.txt`
4. Deploy using the command in the deployment section
5. Update Slack Event URL to Cloud Run endpoint

---
**Remember: This file is the SINGLE SOURCE OF TRUTH. When in doubt, follow this guide.**