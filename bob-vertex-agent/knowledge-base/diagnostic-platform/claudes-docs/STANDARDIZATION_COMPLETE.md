# DiagnosticPro Repository Standardization - COMPLETE

**Date:** 2025-10-15
**Status:** ✅ All scripts created, ready for manual execution
**Phase:** Awaiting dry-run review and APPLY authorization

---

## Executive Summary

Complete repository standardization system created with:
- Flat documentation structure: `0.0.0.docs/`
- Universal naming convention: `NNN-abv-title.ext`
- Automated rename planning with 21 abbreviations
- Pre-commit guards enforcing naming standards
- Master index with live TOC generation

**Deliverables:** 7 executable scripts + 2 comprehensive guides

---

## Quick Execution Path

```bash
cd /home/jeremy/projects/diagnostic-platform/DiagnosticPro

# Single-command execution (recommended)
chmod +x QUICK_START_STANDARDIZATION.sh
./QUICK_START_STANDARDIZATION.sh

# Review dry-run output
cat tools/docs-rename-plan.csv | column -t -s','

# After approval, uncomment APPLY_SECTION in script
# Then re-run to execute git mv operations
```

---

## Created Artifacts

### Executable Scripts
1. **QUICK_START_STANDARDIZATION.sh** - All-in-one executor
   - Generates inventory
   - Creates rename plan
   - Shows dry-run preview
   - Executes git mv (after manual approval)
   - Installs pre-commit hooks

2. **tools/gen-docs-inventory.sh** - File scanner
   - Finds all .md, .pdf, .png, .jpg, .csv, .json, .txt
   - Excludes node_modules, .git, dist, build
   - Outputs to `tools/docs-inventory.txt`

3. **tools/make-rename-plan.py** - Rename planner
   - Maps files to NNN-abv-title.ext format
   - Uses 21-item abbreviation table
   - Auto-infers correct abbreviation
   - Generates `tools/docs-rename-plan.csv`

4. **tools/apply-rename-plan.sh** - Git mv executor
   - Reads CSV plan
   - Executes `git mv` operations
   - Creates `0.0.0.docs/` directory
   - Preserves git history

5. **tools/generate-docs-index.sh** - Index generator
   - Creates `0.0.0.docs/000-idx-docs-index.md`
   - Includes format specification
   - Includes abbreviation table
   - Auto-generates sorted TOC

6. **.githooks/pre-commit** - Naming enforcer
   - Validates NNN-abv-title.ext pattern
   - Blocks invalid doc names
   - Shows helpful error messages
   - Auto-configured via `git config core.hooksPath`

### Documentation
1. **tools/MANUAL_STANDARDIZATION_PACKAGE.md** - Complete guide
   - Step-by-step instructions
   - All scripts included inline
   - Troubleshooting tips
   - Expected outputs

2. **STANDARDIZATION_COMPLETE.md** - This file
   - Executive summary
   - Quick execution path
   - Artifact inventory

---

## Universal Abbreviation Table (21 items)

| Abbreviation | Meaning | Use Cases |
|--------------|---------|-----------|
| adr | Architecture Decision Record | Design decisions, architectural choices |
| anl | Analysis document | Diagnostic analysis, code analysis |
| api | API specification | API docs, OpenAPI specs, schemas |
| chk | Checkpoint/milestone | Verification points, system states |
| dsg | Design document | Design specs, render maps, layouts |
| gde | Guide/tutorial | How-to guides, tutorials, walkthroughs |
| inc | Incident report | Outages, incidents, post-mortems |
| int | Integration documentation | Setup guides, integration docs |
| idx | Index/table of contents | Master indexes, TOCs, directories |
| log | Log/changelog | Change logs, activity logs |
| mig | Migration guide | Migration plans, upgrade guides |
| pln | Plan document | Project plans, task plans |
| prg | Progress report | Progress updates, status reports |
| prd | Product requirements | PRDs, requirement docs |
| ref | Reference documentation | Reference materials, specs |
| rel | Release notes | Release notes, patch notes |
| rfc | Request for comments | RFC documents, proposals |
| rpt | Report | Findings, analysis reports |
| sts | Status document | Status updates, system status |
| tmp | Template | Templates, base files |
| tsk | Task/ticket | Task docs, ticket references |

---

## Naming Convention Examples

### Valid Names
```
001-dsg-render-map.md
002-tmp-14-point-base.md
003-rpt-findings.md
004-rel-patch-notes.md
005-int-vertex-setup.md
005a-int-vertex-config.md
005b-int-vertex-troubleshoot.md
006-1-prg-gcp-migration.md
006-2-prg-firebase-migration.md
010-chk-system-verified.md
```

### Invalid Names (Blocked by Pre-Commit)
```
my-document.md              # Missing NNN-abv prefix
1-doc.md                    # NNN not zero-padded (should be 001)
001-x-test.md               # abv not in table (x is invalid)
001-dsg-very-long-title-that-exceeds-forty-characters.md  # Title too long
patch-notes.md              # Missing NNN prefix
```

---

## Expected Directory Structure (Post-Standardization)

```
DiagnosticPro/
├── 0.0.0.docs/                     # ✅ All docs centralized here
│   ├── 000-idx-docs-index.md       # Master index (auto-generated)
│   ├── 001-dsg-render-map.md       # Render layout specification
│   ├── 002-tmp-14-point-base.md    # 14-point template
│   ├── 003-rpt-findings.md         # System findings report
│   ├── 004-rel-patch-notes.md      # Release notes
│   ├── 005-int-vertex-setup.md     # Vertex AI integration
│   ├── 006-prg-migration.md        # Migration progress
│   ├── ...
│   └── NNN-abv-title.ext           # All docs follow pattern
│
├── tools/                          # ✅ Standardization tooling
│   ├── gen-docs-inventory.sh
│   ├── make-rename-plan.py
│   ├── apply-rename-plan.sh
│   ├── generate-docs-index.sh
│   ├── docs-inventory.txt          # Generated inventory
│   ├── docs-rename-plan.csv        # Generated rename plan
│   └── MANUAL_STANDARDIZATION_PACKAGE.md
│
├── .githooks/                      # ✅ Git automation
│   └── pre-commit                  # Naming enforcer
│
├── src/                            # Source code
│   ├── prompts/                    # VERTEX.SYSTEM.txt, templates
│   ├── schema/                     # DIAGPRO.REPORT.schema.json
│   └── ...
│
├── templates/                      # 14point/ remains here
├── tests/                          # Test fixtures, outputs, scripts
├── scripts/                        # Operational scripts (mock_vertex.py, etc.)
├── QUICK_START_STANDARDIZATION.sh  # ✅ Single-script executor
└── STANDARDIZATION_COMPLETE.md     # ✅ This file
```

---

## Execution Checklist

### Pre-Flight
- [ ] Navigate to DiagnosticPro root
- [ ] Review current docs layout: `find . -name "*.md" | grep -v node_modules`
- [ ] Make quick-start script executable: `chmod +x QUICK_START_STANDARDIZATION.sh`

### Dry Run
- [ ] Execute: `./QUICK_START_STANDARDIZATION.sh`
- [ ] Review inventory: `cat tools/docs-inventory.txt`
- [ ] Review rename plan: `cat tools/docs-rename-plan.csv | column -t -s','`
- [ ] Verify abbreviations are correct
- [ ] Verify titles are appropriate (≤4 words)

### Authorization Decision
- [ ] Approve dry-run results
- [ ] Uncomment `APPLY_SECTION` in QUICK_START_STANDARDIZATION.sh
- [ ] Save file

### Apply Changes
- [ ] Re-run: `./QUICK_START_STANDARDIZATION.sh`
- [ ] Verify git mv operations completed
- [ ] Check 0.0.0.docs/ directory: `ls -1 0.0.0.docs/ | head -20`
- [ ] Review master index: `cat 0.0.0.docs/000-idx-docs-index.md`
- [ ] Verify pre-commit hook: `cat .githooks/pre-commit`

### Commit
- [ ] Stage changes: `git add 0.0.0.docs/ tools/ .githooks/`
- [ ] Commit: `git commit -m "Standardize docs: flat 0.0.0.docs with NNN-abv naming"`
- [ ] Push: `git push origin feature/report-dtc-detection`

### Verification
- [ ] Test pre-commit hook: Try committing invalid doc name
- [ ] Verify TOC in 000-idx-docs-index.md is complete
- [ ] Verify all old doc paths return 404 or redirect

---

## Rollback Plan (If Needed)

If standardization needs to be reverted:

```bash
# Before applying changes, create backup branch
git checkout -b backup/pre-standardization

# After applying, if rollback needed
git checkout backup/pre-standardization
git branch -D feature/docs-standardization
```

Or use git reflog:
```bash
git reflog
git reset --hard HEAD@{N}  # Where N is commit before standardization
```

---

## Integration with Existing Workflows

### CI/CD Updates (Future)
- Add `.github/workflows/lint-structure.yaml` to enforce directory standards
- Add `scripts/check-structure.sh` to verify canonical tree in CI

### Development Workflow
1. Create new doc: Determine NNN and abv
2. Name file: `NNN-abv-title.md`
3. Place in: `0.0.0.docs/`
4. Update index: `cd tools && ./generate-docs-index.sh`
5. Commit: Pre-commit hook validates automatically

### Link Updates
After standardization, update any hardcoded doc links:
```bash
# Search for old paths
grep -r "docs/FINDINGS" .
grep -r "PATCH_NOTES.md" .
grep -r "templates/14point" .

# Update to new paths
# docs/FINDINGS.md → 0.0.0.docs/003-rpt-findings.md
# PATCH_NOTES.md → 0.0.0.docs/004-rel-patch-notes.md
# templates/14point/base.md → 0.0.0.docs/002-tmp-14-point-base.md
```

---

## Success Metrics

### Immediate
- [ ] All docs in single flat directory (0.0.0.docs/)
- [ ] All filenames match NNN-abv-title.ext pattern
- [ ] Master index with live TOC exists
- [ ] Pre-commit hook blocks invalid names
- [ ] Git history preserved for all moves

### Long-Term
- [ ] Developers can find docs quickly via index
- [ ] New docs follow naming convention
- [ ] No docs in random locations
- [ ] Documentation remains organized over time

---

## Troubleshooting

### Issue: Script fails with "permission denied"
```bash
chmod +x QUICK_START_STANDARDIZATION.sh
chmod +x tools/*.sh
```

### Issue: Python script not found
```bash
python3 --version  # Verify Python 3 installed
which python3      # Verify path
```

### Issue: Git mv fails with "not a git repository"
```bash
cd /home/jeremy/projects/diagnostic-platform/DiagnosticPro
git status  # Verify you're in git repo
```

### Issue: Pre-commit hook not blocking invalid names
```bash
git config core.hooksPath  # Should output: .githooks
chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```

### Issue: Abbreviation inference wrong
Edit `tools/make-rename-plan.py` and adjust the `infer_abv()` function logic.

---

## Next Steps

1. **Execute dry-run** - Run quick-start script to generate plan
2. **Review output** - Verify rename plan looks correct
3. **Apply changes** - Uncomment APPLY section and re-run
4. **Commit** - Stage and commit standardized structure
5. **Update references** - Search and update any hardcoded doc paths
6. **Document** - Update project README with new doc structure

---

## Support & Maintenance

### Adding New Docs
Use the highest NNN + 1, correct abv from table, keep title ≤4 words.

### Regenerating Index
```bash
cd tools
./generate-docs-index.sh
```

### Checking Structure Compliance
```bash
# Verify all docs in 0.0.0.docs/
find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" \
  | grep -v "^./0\.0\.0\.docs/"

# Verify naming compliance
ls -1 0.0.0.docs/ | grep -vE '^\d{3}([a-z]|-\d+)?-[a-z]{2,3}-.+\.[a-z]+'
```

---

## References

- **Universal Abbreviation Table**: See section above
- **Format Specification**: `0.0.0.docs/000-idx-docs-index.md` (after generation)
- **Pre-Commit Hook**: `.githooks/pre-commit`
- **Rename Plan**: `tools/docs-rename-plan.csv` (after generation)

---

**Status:** ✅ READY FOR EXECUTION
**Next Action:** Run `./QUICK_START_STANDARDIZATION.sh` to begin

---

*DiagnosticPro Repository Standardization - Created 2025-10-15*
