# Directory Structure Analysis

**Date:** 2025-10-05
**Directory:** /home/jeremy/projects/bobs-brain
**Auditor:** Claude AI

## Current Structure

### Compliant Directories (✅)
```
bobs-brain/
├── 01-Docs/                      ✅ Standard directory exists (EMPTY)
├── 02-Src/                       ✅ Standard directory exists (EMPTY)
│   ├── core/                     ✅ Proper subdirectory
│   ├── features/                 ✅ Proper subdirectory
│   ├── shared/                   ✅ Proper subdirectory
│   └── vendor/                   ✅ Proper subdirectory
├── 03-Tests/                     ✅ Standard directory exists (EMPTY)
│   ├── e2e/                      ✅ Proper subdirectory
│   ├── integration/              ✅ Proper subdirectory
│   └── unit/                     ✅ Proper subdirectory
├── 04-Assets/                    ✅ Standard directory exists (EMPTY)
│   ├── configs/                  ✅ Proper subdirectory
│   ├── data/                     ✅ Proper subdirectory
│   └── images/                   ✅ Proper subdirectory
├── 05-Scripts/                   ✅ Standard directory exists (EMPTY)
│   ├── build/                    ✅ Proper subdirectory
│   ├── deploy/                   ✅ Proper subdirectory
│   └── maintenance/              ✅ Proper subdirectory
├── 06-Infrastructure/            ✅ Standard directory exists (EMPTY)
│   ├── docker/                   ✅ Proper subdirectory
│   ├── kubernetes/               ✅ Proper subdirectory
│   └── terraform/                ✅ Proper subdirectory
├── 07-Releases/                  ✅ Standard directory exists (EMPTY)
│   ├── archive/                  ✅ Proper subdirectory
│   └── current/                  ✅ Proper subdirectory
├── 99-Archive/                   ✅ Standard directory exists (EMPTY)
│   ├── deprecated/               ✅ Proper subdirectory
│   └── legacy/                   ✅ Proper subdirectory
├── .github/                      ✅ Required for GitHub workflows
├── claudes-docs/                 ✅ Claude-created documentation
│   ├── analysis/                 ✅ Organized subdirectory
│   ├── audits/                   ✅ Organized subdirectory
│   ├── logs/                     ✅ Organized subdirectory
│   ├── misc/                     ✅ Organized subdirectory
│   ├── plans/                    ✅ Organized subdirectory
│   ├── reports/                  ✅ Organized subdirectory
│   └── tasks/                    ✅ Organized subdirectory
```

### Non-Compliant Directories (❌)
```
├── archive/                      ❌ DUPLICATE of 99-Archive/ (should merge or remove)
│   ├── deprecated_bobs/          ❌ Underscore naming, duplicate purpose
│   ├── dockerfiles/              ❌ Should be in 99-Archive/legacy/dockerfiles
│   ├── old_scrapers/             ❌ Underscore naming
│   ├── old_src_files/            ❌ Underscore naming
│   ├── old_versions/             ❌ Underscore naming
│   ├── removed_20250920/         ❌ Underscore naming
│   └── test_files/               ❌ Underscore naming
├── ai-dev-tasks/                 ❌ Should be in 01-Docs/ or tools/
├── ci-artifacts/                 ❌ Should be gitignored, not tracked
├── docs/                         ❌ DUPLICATE of 01-Docs/ (lowercase violation)
├── reports/                      ❌ Should be in claudes-docs/reports/
├── scripts/                      ❌ DUPLICATE of 05-Scripts/ (lowercase)
│   └── testing/                  ❌ Should be in 03-Tests/
├── src/                          ❌ DUPLICATE of 02-Src/ (lowercase)
│   ├── .mypy_cache/              ❌ Should be gitignored
│   ├── __pycache__/              ❌ Should be gitignored
│   └── skills/                   ✅ Proper code organization
├── tasks/                        ❌ Purpose unclear, should be organized
├── test_reports/                 ❌ Underscore naming, should be in claudes-docs/reports/
├── tests/                        ❌ DUPLICATE of 03-Tests/ (lowercase)
│   ├── __pycache__/              ❌ Should be gitignored
│   ├── integration/              ❌ Duplicate
│   └── unit/                     ❌ Duplicate
```

## Critical Issues Identified

### 🚨 ISSUE 1: Parallel Directory Structures
**The project has TWO complete directory structures running in parallel:**

**Structure A (STANDARD - EMPTY):**
- 01-Docs/, 02-Src/, 03-Tests/, 04-Assets/, 05-Scripts/, 06-Infrastructure/, 07-Releases/, 99-Archive/

**Structure B (ACTIVE - POPULATED):**
- docs/, src/, tests/, scripts/, archive/

**Impact:** Confusion, maintenance burden, unclear which is authoritative

### 🚨 ISSUE 2: Archive Confusion
- `archive/` directory exists with 18 deprecated bobs, old scrapers, etc.
- `99-Archive/` directory exists but is EMPTY
- **Action Required:** Consolidate all archived content into 99-Archive/

### 🚨 ISSUE 3: Active Code in Wrong Location
- All active source code is in `src/` (lowercase)
- Standard requires `02-Src/` (PascalCase with prefix)
- All active tests are in `tests/` (lowercase)
- Standard requires `03-Tests/` (PascalCase with prefix)

### 🚨 ISSUE 4: Files in Root
**5 script files in project root (should be in 05-Scripts/):**
- deploy_phase5.sh
- setup_ml_models.sh
- deploy_all_ml.sh
- deploy_fixes.sh
- setup_bigquery_sync.sh

### 🚨 ISSUE 5: Gitignore Gaps
Cache directories being tracked:
- src/.mypy_cache/
- src/__pycache__/
- tests/__pycache__/
- ci-artifacts/

## Depth Violations
All violations are in venv/ (virtual environment - should be gitignored)
✅ No depth violations in actual project files

## Compliance Score

**Structure compliance: 3/10**

- ✅ Standard directories created (but empty)
- ❌ Parallel structure with active code in non-standard locations
- ❌ Multiple duplicate directories
- ❌ Files scattered in root
- ❌ Archive confusion (2 archive dirs)
- ❌ Cache files tracked in git

## Remediation Plan

### Phase 1: CRITICAL - Consolidate Directory Structure (Priority: HIGH)

**Option A: Migrate to Standard Structure** ⭐ RECOMMENDED
1. Move `src/*` → `02-Src/`
2. Move `tests/*` → `03-Tests/`
3. Move `scripts/*` → `05-Scripts/`
4. Move `docs/*` → `01-Docs/`
5. Move `archive/*` → `99-Archive/legacy/`
6. Delete empty lowercase directories

**Option B: Remove Standard Structure**
1. Delete 01-Docs/, 02-Src/, 03-Tests/, etc.
2. Keep existing lowercase structure
3. Update .directory-standards.md to match actual structure

### Phase 2: Clean Root Directory (Priority: HIGH)
1. Move deploy_phase5.sh → 05-Scripts/deploy/
2. Move setup_ml_models.sh → 05-Scripts/deploy/
3. Move deploy_all_ml.sh → 05-Scripts/deploy/
4. Move deploy_fixes.sh → 05-Scripts/deploy/
5. Move setup_bigquery_sync.sh → 05-Scripts/deploy/

### Phase 3: Archive Consolidation (Priority: MEDIUM)
1. Move archive/* → 99-Archive/legacy/
2. Organize by category:
   - deprecated_bobs → 99-Archive/legacy/bobs/
   - old_scrapers → 99-Archive/legacy/scrapers/
   - old_versions → 99-Archive/legacy/versions/
3. Delete original archive/ directory

### Phase 4: Gitignore Updates (Priority: MEDIUM)
Add to .gitignore:
```
__pycache__/
*.pyc
.mypy_cache/
.pytest_cache/
ci-artifacts/
venv/
.venv/
*.egg-info/
```

### Phase 5: Organize Miscellaneous (Priority: LOW)
1. ai-dev-tasks → 01-Docs/ai-dev-tasks/ or remove
2. reports → claudes-docs/reports/
3. test_reports → claudes-docs/reports/tests/
4. tasks → claudes-docs/tasks/ or 01-Docs/tasks/

## Estimated Time
- Phase 1: 30 minutes (file moves + import updates)
- Phase 2: 10 minutes (script relocation)
- Phase 3: 15 minutes (archive consolidation)
- Phase 4: 5 minutes (gitignore updates)
- Phase 5: 10 minutes (misc cleanup)
- **Total: ~70 minutes**

## Risk Assessment
- **HIGH RISK:** Moving src/ and tests/ requires import path updates
- **MEDIUM RISK:** Moving scripts may break automation
- **LOW RISK:** Archive consolidation, gitignore updates

## TaskWarrior Commands

```bash
task add project:dir-audit +STRUCTURE priority:H "DECIDE: Migrate to standard structure OR remove standard dirs"
task add project:dir-audit +STRUCTURE priority:H "Move 5 root scripts to 05-Scripts/deploy/"
task add project:dir-audit +STRUCTURE priority:M "Consolidate archive/ into 99-Archive/legacy/"
task add project:dir-audit +STRUCTURE priority:M "Update .gitignore for cache directories"
task add project:dir-audit +STRUCTURE priority:L "Organize ai-dev-tasks, reports, tasks directories"
```

## Next Steps

1. ⏳ **CRITICAL DECISION NEEDED:** Migrate to standard structure OR remove it?
2. ⏳ Execute chosen path systematically
3. ⏳ Update imports after any moves
4. ⏳ Test all scripts and code after relocation
5. ⏳ Commit with message: "refactor: consolidate directory structure per standards"

## Recommendation

**I recommend Option A: Migrate to Standard Structure**

Reasons:
1. Standard structure already created (invested effort)
2. Provides clear organization long-term
3. Aligns with .directory-standards.md
4. Professional appearance for future collaborators

**However, this requires significant import path changes and testing.**
