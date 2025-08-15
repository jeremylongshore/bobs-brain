# 📁 Bob's Brain Project Structure

## Directory Organization (Industry Standard)

```
bobs-brain/
├── src/                              # Source code (production)
│   └── (future modularization)
├── scripts/                          # Utility scripts
│   ├── deployment/                   # Deployment automation
│   │   ├── bob-ferrari.service      # Systemd service file
│   │   ├── install-bob-service.sh   # Service installer
│   │   └── start-bob-ferrari.sh     # Quick start script
│   └── email/                        # Email utilities
│       ├── email_bob_explanation.py # Email formatter
│       └── send_email_now.py        # Email sender
├── tests/                            # Test files
│   ├── clean_agent_template.py      # Agent template
│   └── demo_ferrari.py              # Ferrari demo
├── docs/                             # Documentation
│   └── bob_ferrari_explanation.md   # System explanation
├── config/                           # Configuration files
│   └── (future configs)
├── logs/                             # Application logs
├── chroma_db/                        # Vector database (local)
├── bob_ferrari.py                    # MAIN APPLICATION
├── CLAUDE.md                         # PROJECT DOCUMENTATION
├── README.md                         # Public documentation
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Container definition
├── Makefile                          # Build automation
├── .env                              # Environment variables (SECRET)
├── .gitignore                        # Git exclusions
└── PROJECT_STRUCTURE.md             # THIS FILE

## Quick Access Guide

### 🚀 To Run Bob Ferrari:
```bash
python3 bob_ferrari.py
# OR
./scripts/deployment/start-bob-ferrari.sh
```

### 📍 Key File Locations:
- **Main Application**: `bob_ferrari.py` (root)
- **Project Documentation**: `CLAUDE.md` (root)
- **Deployment Scripts**: `scripts/deployment/`
- **Test Files**: `tests/`
- **Email Utilities**: `scripts/email/`
- **System Explanation**: `docs/bob_ferrari_explanation.md`

### ☁️ Cloud Services:
- **bobs-brain**: Main AI assistant (Cloud Run)
- **unified-scraper**: Data collection (Cloud Run)
- **circle-of-life-scraper**: MVP3 integration (Cloud Run)

### 💾 Data Storage:
- **Neo4j**: Cloud (Aura) - Equipment knowledge graph
- **ChromaDB**: Local (`chroma_db/`) - Vector search
- **BigQuery**: Cloud - Analytics warehouse
- **Datastore**: Cloud - MVP3 integration

## Professional Standards Applied:
1. ✅ Separation of concerns (src, scripts, tests, docs)
2. ✅ Clear deployment pipeline (scripts/deployment)
3. ✅ Test isolation (tests/)
4. ✅ Documentation centralization (docs/)
5. ✅ Configuration management (config/, .env)
6. ✅ Build automation (Makefile, Dockerfile)
7. ✅ Version control best practices (.gitignore)

Last Updated: August 14, 2025