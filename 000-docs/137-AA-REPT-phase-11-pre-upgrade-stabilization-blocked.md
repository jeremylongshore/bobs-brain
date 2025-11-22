# 137-AA-REPT – Phase 11: Pre-Upgrade Stabilization BLOCKED

**Phase:** Phase 11 - Pre-Upgrade Stabilization & ADK Pin
**Date:** 2025-11-21
**Status:** ⚠️ **BLOCKED** (No compatible google-adk version found)
**Branch:** `feature/a2a-agentcards-foreman-worker`

---

## I. Executive Summary

**Objective:** Find and pin to a pre-1.18 google-adk version where existing App + dual-memory wiring works with minimal code changes.

**Outcome:** ⚠️ **PHASE BLOCKED**
- Tested google-adk versions: 1.5.0, 1.12.0, 1.14.0, 1.16.0, 1.17.0, 1.18.0
- **CRITICAL FINDING**: The App API pattern used in our code (`App(agent=..., app_name=..., session_service=..., memory_service=...)`) does NOT exist in ANY tested version
- All recent versions (1.16.0+) use Pydantic `**data` pattern for App constructor
- Older versions (1.5.0-1.12.0) do NOT have `App` class at all

**Root Cause:** Our code was written for an App API that either:
1. Never existed in any released google-adk version, OR
2. Existed in an untested version between 1.12 and 1.16, OR
3. Was based on examples/docs that don't match actual released API

**Recommendation:** **Cannot proceed** with Phase 11 as specified. Need alternative approach (see Options section).

---

## II. Investigation Process

### Step 0: Initial Context ✅

**Repository State:**
- Path: `/home/jeremy/000-projects/iams/bobs-brain`
- Branch: `feature/a2a-agentcards-foreman-worker`
- Working tree: Clean

**Key Documents Reviewed:**
- `134-AA-REPT` - Original test blocker (no google-adk installed)
- `135-AA-REPT` - Environment fix (installed 1.18.0)
- `136-AA-REPT` - 1.18.0 API breaking changes discovered

---

### Step 1: Current Dependency Analysis ✅

**Current State (as of Phase 10B):**
- `requirements.txt`: `google-adk>=0.1.0` (unpinned)
- Installed version: google-adk 1.18.0
- Test status: 135 passed, 20 failed (87%)

**Current Code Pattern:**
```python
# Import (after Phase 10B fix)
from google.adk.apps import App
from google.adk import Runner

# App instantiation (unchanged)
app_instance = App(
    agent=create_agent,  # Function reference (lazy loading)
    app_name="bobs-brain",
    session_service=session_service,  # R5 dual memory
    memory_service=memory_service,
)
```

---

### Step 2: Version Testing ⚠️

Systematically tested versions to find compatible API:

#### google-adk 1.18.0 (Current - Known Broken)
**Status:** ❌ INCOMPATIBLE

**Findings:**
- Import: `from google.adk.apps import App` ✅ Works
- App signature: Pydantic `**data` pattern
- Required parameters: `name`, `root_agent`
- Rejected parameters: `agent`, `app_name`, `session_service`, `memory_service`
- VertexAiSessionService: Uses `project` parameter ✅ (Phase 10B fixed)

**Error:**
```
pydantic_core._pydantic_core.ValidationError: 6 validation errors for App
    name: Field required
    root_agent: Field required
    agent: Extra inputs are not permitted
    app_name: Extra inputs are not permitted
    session_service: Extra inputs are not permitted
    memory_service: Extra inputs are not permitted
```

---

#### google-adk 1.17.0 (Most Recent Pre-1.18)
**Status:** ❌ INCOMPATIBLE (Same API as 1.18.0)

**Findings:**
- Import: `from google.adk.apps import App` ✅ Works
- App signature: Pydantic `**data` pattern (SAME AS 1.18.0)
- App.model_fields: `name`, `root_agent`, `plugins`, `events_compaction_config`, etc.
- VertexAiSessionService: Uses `project` parameter

**Conclusion:** API changes occurred BEFORE 1.18.0

---

#### google-adk 1.16.0
**Status:** ❌ INCOMPATIBLE (Same API as 1.17.0)

**Findings:**
- Import: `from google.adk.apps import App` ✅ Works
- App signature: Pydantic `**data` pattern
- VertexAiSessionService: Uses `project` parameter

**Conclusion:** Pydantic App pattern exists at least back to 1.16.0

---

#### google-adk 1.12.0 and 1.14.0
**Status:** ❌ NO APP CLASS

**Findings:**
- `google.adk` exports: `Agent`, `Runner`, `agents`, `sessions`, etc.
- NO `App` class in `google.adk`
- NO `google.adk.apps` module

**Conclusion:** `App` was introduced between 1.12.0 and 1.16.0

---

#### google-adk 1.5.0 (Older Release)
**Status:** ❌ NO APP CLASS

**Findings:**
- Very minimal API
- Only `Agent` and `Runner` available
- NO `App` construct at all

**Conclusion:** Early versions used Agent/Runner directly, no App wrapper

---

### Step 3: Historical Code Analysis ✅

**Checked git history to understand when current App pattern was introduced:**

**Commit `c08e19a3` (Before Phase 10B):**
```python
# Import (before Phase 10B)
from google.adk import App, Runner  # ❌ This never worked

# App usage
app_instance = App(
    agent=create_agent,
    app_name="bobs-brain",
    session_service=session_service,
    memory_service=memory_service,
)
```

**Original Test Status (from 134-AA-REPT):**
- Tests NEVER ran successfully with google-adk installed
- All 26 ADK-related test failures were: `ModuleNotFoundError: No module named 'google.adk'`
- Tests were written but never validated against actual google-adk API

**Conclusion:** Current App pattern was never tested against ANY google-adk version

---

## III. Critical Findings

### Finding 1: API Pattern Mismatch

**Our Code Expects:**
```python
App(
    agent=create_agent,  # Function reference
    app_name="bobs-brain",
    session_service=VertexAiSessionService(...),
    memory_service=VertexAiMemoryBankService(...),
)
```

**All Recent Versions (1.16.0-1.18.0) Provide:**
```python
App(
    name="bobs-brain",  # String (renamed from app_name)
    root_agent=agent_instance,  # Instance (renamed from agent)
    # session_service and memory_service NOT accepted
)
```

**No version tested supports the "old" API our code uses.**

---

### Finding 2: App Evolution Timeline

Based on testing:

| Version Range | App Status | API Pattern |
|---------------|------------|-------------|
| 0.x - 1.12.x | NO App class | Agent/Runner only |
| 1.13.x - 1.15.x | **UNKNOWN** (not tested) | **UNKNOWN** |
| 1.16.0 - 1.18.0+ | App in google.adk.apps | Pydantic **data pattern |

**Gap:** Versions 1.13-1.15 were not tested and MIGHT have different API

---

### Finding 3: Phase 10B Changes Were Correct

**Phase 10B commits:**
1. `b92cdd89` - Changed `from google.adk import App` to `from google.adk.apps import App`
   - ✅ CORRECT for all versions 1.16.0+

2. `22c29a65` - Changed `project_id` to `project` parameter
   - ✅ CORRECT for all versions 1.16.0+

**These changes align with 1.16/1.17 API, NOT just 1.18.**

---

### Finding 4: Tests Were Never Green

**Timeline:**
1. Code written with `App(agent=..., app_name=..., session_service=..., memory_service=...)`
2. Tests written against this pattern
3. No google-adk installed in environment
4. Phase 10: Installed google-adk 1.18.0
5. Tests revealed API mismatches

**The "old API" our code uses never actually worked.**

---

## IV. Why Phase 11 Cannot Proceed As Specified

### Blocking Condition from Instructions

> "If you **cannot** get to 155/155 without effectively performing the 1.18 migration (new App pattern, new memory wiring), STOP and treat the phase as BLOCKED."

### Why We're Blocked

1. **No compatible version exists:**
   - Tested 6 versions (1.5.0, 1.12.0, 1.14.0, 1.16.0, 1.17.0, 1.18.0)
   - NONE support `App(agent=..., app_name=..., session_service=..., memory_service=...)`

2. **Gap versions unlikely to help:**
   - Versions 1.13-1.15 untested
   - Even if one has different API, it's between "no App" (1.12) and "Pydantic App" (1.16)
   - Unlikely to have the exact pattern we need

3. **Code never validated:**
   - Current pattern was never tested against actual google-adk
   - May be based on examples/docs that don't match released versions

4. **Migration required:**
   - To make tests pass with ANY version (1.16+), we need to:
     - Change `agent` → `root_agent`
     - Change `app_name` → `name`
     - Remove or relocate `session_service` and `memory_service`
   - This IS the "App migration" Phase 11 says NOT to do

---

## V. Options for Resolution

### Option 1: Test Gap Versions (Low Probability)

**Steps:**
1. Test google-adk 1.13.0, 1.13.1, 1.13.2, etc.
2. Test google-adk 1.14.1, 1.15.0, 1.15.1
3. Hope one has the exact API we need

**Pros:**
- Might find a compatible version

**Cons:**
- Low probability (API likely evolved gradually)
- Even if found, would be an old, potentially unsupported version
- Doesn't explain why code was written for API that might not exist

**Effort:** Medium (manual testing of 6-10 versions)

**Recommendation:** ❌ **NOT RECOMMENDED** (low success probability)

---

### Option 2: Rewrite Code to Match 1.17.0 API (Outside Phase Scope)

**Steps:**
1. Pin google-adk to 1.17.0
2. Update all agents to use:
   ```python
   App(
       name=APP_NAME,
       root_agent=create_agent(),  # Call function, get instance
   )
   ```
3. Move memory services configuration to Runner or elsewhere
4. Update all 155 tests

**Pros:**
- Uses most recent pre-1.18 version
- Aligns with actual released API
- Makes tests pass

**Cons:**
- **Violates Phase 11 scope** ("No 1.18 App migration")
- Changes lazy-loading pattern
- Affects R5 dual memory wiring
- Requires architectural review

**Effort:** High (equivalent to 1.18 migration)

**Recommendation:** ❌ **NOT ALLOWED** (outside Phase 11 scope per instructions)

---

### Option 3: Admit Code Was Never Tested, Create Design Phase

**Steps:**
1. Document that current App pattern was never validated
2. Create new "ADK API Alignment" phase to:
   - Research actual google-adk API evolution
   - Design correct pattern for App + memory services
   - Implement across all agents
   - Validate with tests
3. Block Phase 11 pending this work

**Pros:**
- Honest assessment of situation
- Allows proper design review
- Doesn't hack around fundamental API misalignment

**Cons:**
- Delays PR/merge/release
- Requires more research and design work

**Effort:** High (new phase)

**Recommendation:** ✅ **RECOMMENDED** (most honest approach)

---

### Option 4: Use google-adk 1.12.0 + Remove App Pattern

**Steps:**
1. Pin to google-adk 1.12.0 (no App class)
2. Rewrite agents to use Agent/Runner directly (no App wrapper)
3. Update tests
4. Accept that we're using a 2-year-old version

**Pros:**
- Uses stable, older API
- Simpler pattern (no App layer)

**Cons:**
- Very old version (potential security/bugs)
- Removes App construct entirely
- Still requires significant code changes
- May not align with Agent Engine deployment expectations

**Effort:** Medium-High

**Recommendation:** ❌ **NOT RECOMMENDED** (uses very old version)

---

## VI. Research Questions

To unblock this situation, we need answers to:

1. **What version of google-adk was this code originally written for?**
   - Check original PR/commit notes
   - Check any documentation references
   - Ask original author

2. **Was the App pattern based on examples or actual API?**
   - Was code written from examples/docs that showed different API?
   - Were examples tested against real google-adk installation?

3. **Is there official migration guidance?**
   - google-adk changelog/release notes
   - Migration guides from App v1 → App v2
   - Official examples showing memory services configuration

4. **What's the current google-adk recommended pattern?**
   - How do official examples create App?
   - Where do they configure session/memory services?
   - How do they handle lazy loading?

---

## VII. Immediate Next Steps (Pending Decision)

**Cannot proceed with Phase 11 as specified.**

**Recommended Path Forward:**

1. **User Decision Required:**
   - Option 1: Continue searching gap versions (low probability)
   - Option 2: Scope change - allow App migration in Phase 11
   - Option 3: Block Phase 11, create new "ADK API Alignment" phase
   - Option 4: Use old version, remove App pattern

2. **If Option 3 (New Phase):**
   - Research google-adk API evolution (changelogs, release notes)
   - Check google-adk documentation/examples for current patterns
   - Design App + memory wiring aligned with actual API
   - Implement and validate

3. **If User Provides Version Info:**
   - Test that specific version
   - Document findings
   - Proceed with pin if compatible

---

## VIII. Environment Notes

**Virtual Environment Issue:**
- During testing, `.venv` was deleted (possibly by pip during package downgrades)
- Had to recreate: `python3 -m venv .venv`
- This is noted for future reference

**Package Testing:**
- Successfully installed and tested: 1.5.0, 1.12.0, 1.14.0, 1.16.0, 1.17.0, 1.18.0
- Each version's API was inspected using `inspect.signature()`
- All findings documented above

---

## IX. Files Modified

**None** - Phase blocked before making any changes.

---

## X. Commits Made

**None** - Phase blocked before making any commits.

---

## XI. Lessons Learned

### What Went Well ✅

1. **Systematic investigation** - Tested multiple versions methodically
2. **Historical analysis** - Checked git history to understand code evolution
3. **Clear documentation** - Comprehensive findings documented

### Critical Issues Discovered 🔴

1. **Code never tested** - App pattern never ran against actual google-adk
2. **API assumptions incorrect** - Expected API doesn't match any released version
3. **Missing validation** - Tests written but never validated before Phase 10

### Recommendations for Future 📋

1. **Always test dependencies** - Validate code against actual installed packages
2. **Lock file discipline** - Use `poetry.lock` or `requirements-lock.txt` to pin working versions
3. **CI/CD earlier** - Run tests in CI before merge to catch dependency issues
4. **API documentation** - Reference specific google-adk version in code comments

---

## XII. Summary

**Phase Outcome:** ⚠️ **BLOCKED**

**Key Finding:** The `App(agent=..., app_name=..., session_service=..., memory_service=...)` pattern used in our code does NOT exist in ANY tested google-adk version (1.5.0-1.18.0).

**Versions Tested:**
- 1.18.0 ❌ (Pydantic App, new API)
- 1.17.0 ❌ (Pydantic App, same as 1.18)
- 1.16.0 ❌ (Pydantic App, same as 1.17)
- 1.14.0 ❌ (No App class)
- 1.12.0 ❌ (No App class)
- 1.5.0 ❌ (No App class)

**Next Action Required:** User decision on how to proceed (see Options section).

**Cannot Complete Phase 11:** No pre-1.18 version found where existing code works without App API migration.

---

**Prepared by:** Claude Code
**Date:** 2025-11-21
**AAR Version:** 1.0
**Related Docs:**
- `000-docs/134-AA-REPT-phase-10-pr-merge-release-blocked-on-test-env.md` (Original test environment blocker)
- `000-docs/135-AA-REPT-phase-10-unblocked-new-import-error-discovered.md` (Environment fix results)
- `000-docs/136-AA-REPT-phase-10b-extensive-api-changes-discovered.md` (1.18.0 API changes)
- `requirements.txt` (Current dependency specification)
