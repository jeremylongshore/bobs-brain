# Bob Enhancement Directory Structure & Git Strategy

## 📁 Directory Structure

```
bobs-brain/                          # Root directory (existing)
│
├── src/                             # Existing Bob source code
│   ├── bob_cloud_run.py            # Current Bob (Cloud Run version) - BASE
│   ├── bob_firestore.py            # Socket mode version
│   ├── bob_ultimate.py             # Legacy version
│   └── knowledge_loader.py         # Knowledge loading utilities
│
├── src/enhanced_bob/                # NEW: Enhanced Bob components
│   ├── __init__.py                 # Package init
│   ├── bob_base.py                 # Enhanced Bob base class
│   ├── bob_memory.py               # Graphiti memory integration
│   ├── bob_model_router.py         # Model Garden router
│   └── bob_manager.py              # API for managing multiple Bobs
│
├── src/bobs/                        # NEW: Specialized Bob versions
│   ├── __init__.py                 
│   ├── research_bob.py             # Research specialization
│   ├── assistant_bob.py            # Assistant specialization (future)
│   └── diagnostic_bob.py           # Diagnostic specialization (future)
│
├── src/tools/                       # NEW: Pluggable tools for Bobs
│   ├── __init__.py
│   ├── web_scraper.py              # Web scraping tools
│   ├── pdf_processor.py            # PDF processing
│   ├── calendar_connector.py       # Calendar integration
│   └── task_manager.py             # Task management
│
├── src/memory/                      # NEW: Memory components
│   ├── __init__.py
│   ├── graphiti_connector.py       # Graphiti integration
│   ├── firestore_connector.py      # Firestore wrapper
│   └── vector_search.py            # Vector search utilities
│
├── tests/                           # NEW: Test suite
│   ├── test_bob_base.py            # Base Bob tests
│   ├── test_memory.py              # Memory system tests
│   ├── test_model_router.py        # Model routing tests
│   └── test_research_bob.py        # Research Bob tests
│
├── configs/                         # NEW: Configuration files
│   ├── model_configs.yaml          # Model Garden configurations
│   ├── bob_configs.yaml            # Bob-specific settings
│   └── specializations.yaml        # Specialization definitions
│
├── deployments/                     # Deployment configurations
│   ├── cloud_run/
│   │   ├── Dockerfile              # Cloud Run container
│   │   └── deploy.sh               # Deployment script
│   └── docker-compose.yml          # Local development
│
├── docs/                            # Documentation
│   ├── CLAUDE.md                   # Existing: Current Bob docs
│   ├── AGENT_FRAMEWORK.md          # New: Overall architecture
│   ├── BOB_BASE_MODEL_PLAN.md      # New: Implementation plan
│   ├── BASE_FRAMEWORK_IMPLEMENTATION.md # New: Technical details
│   └── DIRECTORY_STRUCTURE.md      # This file
│
├── requirements.txt                 # Python dependencies (existing)
├── requirements-enhanced.txt        # NEW: Enhanced Bob dependencies
├── .env                            # Environment variables (existing)
├── .gitignore                      # Git ignore rules (existing)
└── README.md                       # Project readme (existing)
```

## 🌳 Git Branch Strategy

### Current State
- **Branch:** `bobs-brain-birthed` (active, up to date)
- **Remote:** https://github.com/jeremylongshore/bobs-brain

### Branching Strategy for Enhancement

```
main
 └── bobs-brain-birthed (current working branch)
      └── enhance-bob-graphiti (Phase 1: Memory)
           └── enhance-bob-models (Phase 2: Model Router)
                └── enhance-bob-modular (Phase 3: Specializations)
                     └── deploy-enhanced-bob (Phase 4: Production)
```

### Git Workflow

1. **Create feature branch for Phase 1:**
```bash
git checkout -b enhance-bob-graphiti
```

2. **Regular commits during development:**
```bash
git add src/enhanced_bob/bob_memory.py
git commit -m "Add Graphiti memory integration to Bob"
```

3. **Push to GitHub regularly:**
```bash
git push origin enhance-bob-graphiti
```

4. **Merge back when phase complete:**
```bash
git checkout bobs-brain-birthed
git merge enhance-bob-graphiti
git push origin bobs-brain-birthed
```

## 📝 File Naming Conventions

### Python Files
- **Base classes:** `bob_base.py`, `bob_memory.py`
- **Specialized Bobs:** `research_bob.py`, `assistant_bob.py`
- **Tools:** `web_scraper.py`, `pdf_processor.py`
- **Tests:** `test_[module_name].py`

### Configuration Files
- **YAML format:** `model_configs.yaml`, `bob_configs.yaml`
- **Environment:** `.env` (never commit secrets)

### Documentation
- **Markdown:** `UPPERCASE_TITLE.md` for major docs
- **README:** One per major directory if needed

## 🔒 What NOT to Commit

Already in `.gitignore`:
- `.env` files with secrets
- `__pycache__/` directories
- `*.pyc` files
- `logs/` directory
- Neo4j data directories
- Test outputs

## 🚀 Initial Setup Commands

```bash
# 1. Ensure we're on the right branch
cd ~/bobs-brain
git checkout bobs-brain-birthed
git pull origin bobs-brain-birthed

# 2. Create enhancement branch
git checkout -b enhance-bob-graphiti

# 3. Create __init__.py files
touch src/enhanced_bob/__init__.py
touch src/bobs/__init__.py
touch src/tools/__init__.py
touch src/memory/__init__.py

# 4. Create requirements-enhanced.txt
cat > requirements-enhanced.txt << EOF
# Enhanced Bob Dependencies
graphiti==0.3.0
neo4j==5.14.0
google-cloud-aiplatform==1.71.1
langchain==0.1.0
playwright==1.40.0
beautifulsoup4==4.12.2
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.2
EOF

# 5. Initial commit
git add -A
git commit -m "Set up directory structure for Bob enhancement

- Created enhanced_bob directory for new components
- Added bobs directory for specializations
- Added tools and memory directories
- Set up test structure
- Added enhanced requirements file"

# 6. Push to GitHub
git push origin enhance-bob-graphiti
```

## 📊 Development Phases by Directory

### Phase 1: Memory Enhancement
**Focus:** `src/enhanced_bob/` and `src/memory/`
- Create `bob_memory.py`
- Create `graphiti_connector.py`
- Test in `tests/test_memory.py`

### Phase 2: Model Router
**Focus:** `src/enhanced_bob/`
- Create `bob_model_router.py`
- Update `bob_base.py`
- Test in `tests/test_model_router.py`

### Phase 3: Specializations
**Focus:** `src/bobs/` and `src/tools/`
- Create `research_bob.py`
- Create `web_scraper.py`
- Test in `tests/test_research_bob.py`

### Phase 4: Deployment
**Focus:** `deployments/`
- Update `Dockerfile`
- Create `deploy.sh`
- Test deployment

## ✅ Ready to Start

Directory structure is set up and ready for Bob enhancement. The separation of concerns is clear:
- Original Bob code remains untouched in `src/`
- Enhanced components go in `src/enhanced_bob/`
- Specializations go in `src/bobs/`
- Tools are modular in `src/tools/`

This structure allows us to:
1. Keep existing Bob working
2. Develop enhancements in isolation
3. Test each component independently
4. Deploy progressively