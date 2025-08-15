# PROJECT ORGANIZATION - BOB'S BRAIN
**CRITICAL: This prevents confusion and maintains clean architecture**

## 📍 CURRENT STATUS
- **Branch:** enhance-bob-graphiti (ACTIVE)
- **Location:** /home/jeremylongshore/bobs-brain/
- **Uncommitted Files:** 7 new files need committing

## 🎯 WHICH CODE WE'RE USING (NO CONFUSION!)

### ✅ ACTIVE CODE (WHAT WE USE)
```
src/
├── bob_firestore.py      # PRIMARY - Socket Mode Bob (CURRENTLY RUNNING)
├── bob_memory.py         # NEW - Graphiti/Firestore memory system
├── bob_base.py           # NEW - Base model with specializations
└── knowledge_loader.py   # ACTIVE - Loads knowledge base

tests/
├── test_memory_only.py   # ACTIVE - Tests memory without Slack
├── test_bob_base.py      # ACTIVE - Full test suite
└── run_all_tests.py      # ACTIVE - Master test runner
```

### ⚠️ TRANSITION CODE (BEING DEVELOPED)
```
src/
├── bob_cloud_run.py      # NEEDS CONVERSION from Socket to HTTP
└── bob_hybrid.py         # EXPERIMENTAL - Not fully tested
```

### ❌ DEPRECATED CODE (DO NOT USE)
```
src/
├── bob_ultimate.py       # OLD - Pre-Firestore version
├── bob_legacy_v2.py      # OLD - Backup from recovery
└── bob_test_harness.py   # OLD - Testing framework
```

## 📊 FILE PURPOSE MATRIX

| File | Purpose | Status | When to Use |
|------|---------|--------|-------------|
| **bob_firestore.py** | Main Bob with Socket Mode | ✅ ACTIVE | Current production code |
| **bob_memory.py** | Graphiti knowledge graph | 🔧 FIXING | After Graphiti params fixed |
| **bob_base.py** | Specialized Bobs | ✅ READY | With memory system |
| **bob_cloud_run.py** | HTTP mode for Cloud Run | ⚠️ CONVERT | After Socket→HTTP conversion |
| **bob_hybrid.py** | Socket+HTTP experiment | 🧪 TEST | Not for production |
| **bob_ultimate.py** | Old ChromaDB version | ❌ DEPRECATED | Never |
| **bob_legacy_v2.py** | Recovery backup | ❌ DEPRECATED | Never |

## 🗂️ DATA LOCATIONS

### Databases
- **Firestore:** `diagnostic-pro-mvp/bob-brain` (5 docs, ACTIVE)
- **ChromaDB:** `/home/jeremylongshore/bobs-brain/chroma_data/` (MIGRATED)
- **Neo4j:** Not installed yet (PENDING)

### Configuration
- **Slack Tokens:** In `.env` file (NOT in Git)
- **GCP Project:** bobs-house-ai
- **Service Account:** Uses default credentials

## 🔄 GITHUB BRANCHES

| Branch | Purpose | Status |
|--------|---------|--------|
| **enhance-bob-graphiti** | Current work - Graphiti integration | 🔴 ACTIVE |
| **bobs-brain-birthed** | Last stable deployment | ✅ STABLE |
| **main** | Original branch | ⚠️ OUTDATED |

## 📝 DOCUMENTATION HIERARCHY

1. **CLAUDE.md** - Single source of truth (THIS IS LAW)
2. **PROJECT_ORGANIZATION.md** - This file (PREVENTS CONFUSION)
3. **STEP_BY_STEP_PLAN.md** - Migration roadmap (CURRENT FOCUS)
4. **GRAPHITI_MIGRATION_PLAN.md** - Detailed technical plan
5. **SLACK_SETUP.md** - Slack configuration reference

## 🚨 CRITICAL RULES TO PREVENT CHAOS

1. **NEVER** use deprecated files (bob_ultimate.py, bob_legacy_v2.py)
2. **ALWAYS** check this file before using any code
3. **COMMIT** changes regularly to GitHub
4. **TEST** each component before integration
5. **UPDATE** CLAUDE.md after major changes

## 🎯 CURRENT WORKING FILES

For the Graphiti migration, we are ONLY working with:

```bash
# Primary files
src/bob_firestore.py     # Main Bot (Socket Mode)
src/bob_memory.py        # Memory system (needs Graphiti fix)
src/bob_base.py          # Base model with specializations

# Test files
tests/test_memory_only.py   # Memory tests (no Slack needed)
tests/test_bob_base.py      # Full test suite
run_all_tests.py            # Master test runner

# Documentation
CLAUDE.md                   # Source of truth
PROJECT_ORGANIZATION.md     # This file
STEP_BY_STEP_PLAN.md       # Current roadmap
```

## 📋 NEXT ACTIONS TO STAY ORGANIZED

1. ✅ Created PROJECT_ORGANIZATION.md
2. 🔄 Commit new files to GitHub
3. 🔄 Fix Graphiti parameters in bob_memory.py
4. 🔄 Follow STEP_BY_STEP_PLAN.md

## 🗑️ FILES TO POTENTIALLY REMOVE (CLEANUP)

After confirming everything works:
- bob_ultimate.py (deprecated)
- bob_legacy_v2.py (deprecated)
- bob_test_harness.py (deprecated)
- Any duplicate test files

---

**Remember:** When in doubt, check this file and CLAUDE.md to know exactly what code to use!
