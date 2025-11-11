# Naming Convention Violations Audit

**Date:** 2025-10-05
**Directory:** /home/jeremy/projects/bobs-brain
**Auditor:** Claude AI

## Summary

Total violations found: **13 files**

## Violations by Type

### Files with Spaces (0 files)
✅ No files with spaces found

### Files with Underscores (12 files)

**Root-level scripts:**
- `deploy_phase5.sh` → should be `deploy-phase5.sh`
- `setup_ml_models.sh` → should be `setup-ml-models.sh`
- `deploy_all_ml.sh` → should be `deploy-all-ml.sh`
- `deploy_fixes.sh` → should be `deploy-fixes.sh`
- `setup_bigquery_sync.sh` → should be `setup-bigquery-sync.sh`

**Source code:**
- `src/circle_of_life.py` → should be `src/circle-of-life.py`

**Scripts:**
- `scripts/start_bob.sh` → should be `scripts/start-bob.sh`

**Test files:**
- `tests/test_smoke.py` → **ACCEPTABLE** (Python test convention)
- `tests/test_config.py` → **ACCEPTABLE** (Python test convention)
- `tests/test_basic.py` → **ACCEPTABLE** (Python test convention)
- `tests/test_circle.py` → **ACCEPTABLE** (Python test convention)

**Test reports:**
- `test_reports/test_results_20250810_165359.json` → should be `test-reports/test-results-2025-08-10.json`

### Files with Mixed Case (1 file)
- `docs/Gemfile` → **ACCEPTABLE** (Ruby/Jekyll convention)

## Remediation Plan

### Priority 1: Root Scripts (5 files)
Rename deployment and setup scripts to kebab-case:
1. `deploy_phase5.sh` → `deploy-phase5.sh`
2. `setup_ml_models.sh` → `setup-ml-models.sh`
3. `deploy_all_ml.sh` → `deploy-all-ml.sh`
4. `deploy_fixes.sh` → `deploy-fixes.sh`
5. `setup_bigquery_sync.sh` → `setup-bigquery-sync.sh`

### Priority 2: Source Code (1 file)
1. `src/circle_of_life.py` → `src/circle-of-life.py`
   - **Risk:** HIGH - This is a core module imported in other files
   - Update imports in: `src/app.py`

### Priority 3: Support Scripts (1 file)
1. `scripts/start_bob.sh` → `scripts/start-bob.sh`

### Priority 4: Test Reports Directory (1 directory + files)
1. Rename `test_reports/` → `test-reports/`
2. Standardize file naming with dates

### Estimated Time
- **Low risk renames:** 10 minutes (scripts)
- **Medium risk renames:** 15 minutes (source code with import updates)
- **Total:** ~25 minutes

## Impact Assessment

**Low Risk (7 files):**
- Shell scripts (not imported by code)

**Medium Risk (1 file):**
- `circle_of_life.py` - Core module, requires import updates

**No Action Needed (5 files):**
- Test files with `test_` prefix (Python convention)
- Gemfile (Ruby convention)

## TaskWarrior Commands

```bash
task add project:dir-audit +NAMING priority:M "Rename 5 root-level scripts to kebab-case"
task add project:dir-audit +NAMING priority:H "Rename circle_of_life.py and update imports"
task add project:dir-audit +NAMING priority:L "Rename scripts/start_bob.sh to kebab-case"
task add project:dir-audit +NAMING priority:L "Rename test_reports directory and files"
```

## Next Steps

1. ✅ Review this audit
2. ⏳ Execute renames starting with low-risk files
3. ⏳ Test imports after renaming circle_of_life.py
4. ⏳ Update any documentation referencing old names
5. ⏳ Commit changes with clear message: "refactor: standardize file naming to kebab-case"
