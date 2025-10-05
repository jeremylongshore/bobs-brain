# Content Organization Audit

**Date:** 2025-10-05
**Directory:** /home/jeremy/projects/bobs-brain
**Auditor:** Claude AI

## Documentation Files

**Total found: 10 files**

### Documentation Locations

| Location | Count | Files |
|----------|-------|-------|
| `.` (root) | 4 | README.md, CLAUDE.md, CHANGELOG.md, .directory-standards.md |
| `claudes-docs/audits/` | 2 | 2025-10-05_naming-violations-audit.md, 2025-10-05_structure-analysis-audit.md |
| `ai-dev-tasks/ai-dev-tasks-template-masters/` | 3 | README.md, templates/*.md, master/*.md |
| `.pytest_cache/` | 1 | README.md (cache file, should be gitignored) |

### Analysis

**✅ GOOD:**
- Core documentation in root (README.md, CLAUDE.md, CHANGELOG.md)
- Claude-created audits properly organized in `claudes-docs/audits/`
- .directory-standards.md in root for reference

**❌ ISSUES:**
- `01-Docs/` directory exists but is EMPTY
- AI dev task templates scattered in `ai-dev-tasks/` (should be in 01-Docs/)
- pytest cache README tracked (should be gitignored)

## Duplicate Files

**Found: Multiple duplicate filenames**

Most duplicates are in venv/ (Python packages - acceptable).

**Project-level duplicates:**
- `.gitignore` - Found in multiple locations (1 in root, others in subdirs - check if needed)
- `README.md` - Found in root, ai-dev-tasks, .pytest_cache

**Action:** Root .gitignore is authoritative, remove others if redundant

## Large Files

**✅ No files over 10MB found**

Project is lean with no bloat.

## Temporary Files

**✅ No .tmp, .cache, .bak, or ~ files found**

Clean - no temporary files being tracked.

## Script Files in Root

**5 deployment/setup scripts in root (should be organized):**

| File | Size | Purpose (from name) | Destination |
|------|------|---------------------|-------------|
| deploy_phase5.sh | 3.1K | Phase 5 deployment | 05-Scripts/deploy/ |
| deploy_fixes.sh | 3.0K | Deploy bug fixes | 05-Scripts/deploy/ |
| deploy_all_ml.sh | 1.2K | Deploy ML models | 05-Scripts/deploy/ |
| setup_ml_models.sh | 3.3K | Setup ML infrastructure | 05-Scripts/deploy/ |
| setup_bigquery_sync.sh | 2.4K | Setup BigQuery sync | 05-Scripts/deploy/ |

## Content Distribution Issues

### Issue 1: Empty Standard Directories
**All standard directories created but EMPTY:**
- 01-Docs/ (0 files)
- 02-Src/core/ (0 files)
- 02-Src/features/ (0 files)
- 02-Src/shared/ (0 files)
- 03-Tests/unit/ (0 files)
- 03-Tests/integration/ (0 files)
- 03-Tests/e2e/ (0 files)
- 04-Assets/* (0 files in all subdirs)
- 05-Scripts/* (0 files in all subdirs)
- 06-Infrastructure/* (0 files in all subdirs)
- 07-Releases/* (0 files in all subdirs)
- 99-Archive/deprecated/ (0 files)
- 99-Archive/legacy/ (0 files)

### Issue 2: Active Content in Non-Standard Locations
**All active content is in lowercase parallel structure:**
- `src/` (8 Python files) - should be in 02-Src/
- `tests/` (4 test files) - should be in 03-Tests/
- `scripts/` (3 scripts) - should be in 05-Scripts/
- `docs/` (Jekyll/GitHub Pages) - should be in 01-Docs/
- `archive/` (18 deprecated bobs + old code) - should be in 99-Archive/

### Issue 3: Scattered AI/Development Tasks
- `ai-dev-tasks/` directory with templates and TODOs
- Should be consolidated into 01-Docs/ai-dev/ or similar

### Issue 4: Reports Not Consolidated
- `reports/` directory exists (junit.xml)
- `test_reports/` directory exists (test results)
- `ci-artifacts/coverage/` exists (coverage.xml)
- Should all be in `claudes-docs/reports/` or gitignored

## Remediation Plan

### Phase 1: CRITICAL DECISION - Directory Strategy

**Option A: Migrate to Standard Structure** (RECOMMENDED)
1. Move all active content to standard directories
2. Delete empty parallel lowercase directories
3. Consolidate scattered content

**Option B: Remove Standard Structure**
1. Delete 01-Docs/ through 99-Archive/
2. Keep existing structure
3. Update standards to match reality

### Phase 2: Consolidate Documentation (if Option A)
1. Move ai-dev-tasks → 01-Docs/ai-development/
2. Keep root docs (README, CLAUDE, CHANGELOG, .directory-standards)
3. Keep claudes-docs/ organized structure

### Phase 3: Organize Scripts
1. Move 5 root scripts → 05-Scripts/deploy/
2. Move scripts/testing → 05-Scripts/testing/ or 03-Tests/scripts/
3. Delete empty scripts/ directory

### Phase 4: Archive Consolidation
1. Move archive/* → 99-Archive/legacy/
   - deprecated_bobs → 99-Archive/legacy/bobs/
   - old_scrapers → 99-Archive/legacy/scrapers/
   - old_versions → 99-Archive/legacy/versions/
   - dockerfiles → 99-Archive/legacy/dockerfiles/
   - old_src_files → 99-Archive/legacy/src-files/
   - test_files → 99-Archive/legacy/test-files/
2. Delete original archive/ directory

### Phase 5: Reports and Artifacts
1. Consolidate reports:
   - reports/junit.xml → claudes-docs/reports/ci/
   - test_reports/* → claudes-docs/reports/tests/
   - ci-artifacts/coverage → claudes-docs/reports/coverage/
2. Update .gitignore to prevent future tracking
3. Delete original directories

## Performance Impact

**Current State:**
- 10 documentation files (manageable)
- No large files (good)
- No temp files (clean)
- Duplicates mostly in venv (acceptable)

**After Reorganization:**
- Faster file location (clear structure)
- Easier navigation
- Better discoverability

## Estimated Time

- Phase 1 Decision: 5 minutes
- Phase 2 Documentation: 15 minutes
- Phase 3 Scripts: 10 minutes
- Phase 4 Archive: 20 minutes
- Phase 5 Reports: 10 minutes
- **Total: ~60 minutes**

## Risk Assessment

- **LOW RISK:** Moving documentation files
- **MEDIUM RISK:** Moving scripts (may break automation if hardcoded paths)
- **LOW RISK:** Archive consolidation (no active usage)
- **LOW RISK:** Report consolidation (test artifacts, regenerated)

## TaskWarrior Commands

```bash
task add project:dir-audit +CONTENT priority:H "DECIDE: Migrate content to standard structure OR remove standards"
task add project:dir-audit +CONTENT priority:M "Consolidate ai-dev-tasks to 01-Docs/"
task add project:dir-audit +CONTENT priority:M "Move 5 root scripts to 05-Scripts/deploy/"
task add project:dir-audit +CONTENT priority:M "Consolidate archive/ into 99-Archive/legacy/"
task add project:dir-audit +CONTENT priority:L "Consolidate reports to claudes-docs/reports/"
```

## Recommendations

1. **Choose Option A:** Migrate to standard structure
   - Provides long-term clarity
   - Aligns with .directory-standards.md
   - Professional organization

2. **Consolidate scattered content systematically:**
   - Documentation → 01-Docs/
   - Active code → 02-Src/
   - Tests → 03-Tests/
   - Scripts → 05-Scripts/
   - Archives → 99-Archive/

3. **Update imports after moves:**
   - Test all scripts
   - Update any hardcoded paths
   - Verify CI/CD pipelines

4. **Gitignore cleanup:**
   - Add reports/, test_reports/, ci-artifacts/
   - Add __pycache__/, .mypy_cache/, .pytest_cache/

## Next Steps

1. ⏳ Get approval for migration strategy
2. ⏳ Execute Phase 1 (directory decision)
3. ⏳ Execute Phases 2-5 systematically
4. ⏳ Test all functionality after moves
5. ⏳ Commit with: "refactor: reorganize content per directory standards"
