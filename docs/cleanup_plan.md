# Bob's Brain Cleanup Plan
## Current State: 119 items in root (MESSY)

### Proposed Directory Structure:
```
bobs-brain/
├── src/                    # Core application code
│   ├── bob_brain_v5.py    # Production Bob Brain
│   └── scrapers/           # All scraper implementations
├── scripts/                # Utility and automation scripts
│   ├── testing/            # Test scripts
│   ├── migration/          # Data migration scripts
│   └── deployment/         # Deployment scripts
├── docs/                   # Documentation
│   ├── CLAUDE.md          # Main project documentation
│   └── archived/           # Old documentation
├── archive/                # Old/deprecated code
│   └── old_versions/       # Previous Bob versions
├── config/                 # Configuration files
└── tests/                  # Test files
```

### Files to Move:
1. **Testing Scripts** (24 .py files) → scripts/testing/
   - debug_bob.py, quick_debug.py, verify_bob_complete.py, etc.

2. **Scrapers** → src/scrapers/
   - ytdlp_scraper.py, reddit_equipment_scraper.py, diesel_truck_scraper.py

3. **Old Documentation** → docs/archived/
   - Old .md files that aren't current

4. **Email Scripts** → scripts/email/ (already exists)

5. **Migration Scripts** → scripts/migration/ (already exists)

### Files to Keep in Root:
- CLAUDE.md (main documentation)
- README.md (if exists)
- Dockerfile* (deployment configs)
- requirements*.txt (dependencies)
- Makefile (build automation)
- .gitignore, .pre-commit-config.yaml (git configs)

### Files to Consider Deleting (with permission):
- Test output files (.json results)
- Duplicate/old versions
- Temporary test scripts