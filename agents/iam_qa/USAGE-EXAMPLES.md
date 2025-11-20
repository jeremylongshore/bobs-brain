# iam-qa Usage Examples

This document provides practical examples of how iam-qa evaluates fixes and produces QAVerdict verdicts.

## Example 1: High-Risk Fix - Agent Architecture Change

### Scenario
A developer has implemented a major change to agent memory wiring following a FixPlan from iam-fix-plan.

**FixPlan Input:**
```json
{
  "summary": "Refactor dual-memory wiring to use new VertexAiMemoryBankService",
  "impacted_areas": ["agents/bob/agent.py", "agents/iam_fix_plan/agent.py", "agents/iam_adk/agent.py"],
  "steps": [
    "1. Update VertexAiMemoryBankService initialization",
    "2. Add auto_save callback to all agents",
    "3. Test session persistence across agent restarts",
    "4. Verify memory lookups work correctly"
  ],
  "risk_level": "high",
  "testing_strategy": ["unit", "integration", "e2e"]
}
```

**Implementation Results:**
```json
{
  "files_changed": ["agents/bob/agent.py", "agents/iam_fix_plan/agent.py", "agents/iam_adk/agent.py"],
  "test_results": {
    "passed": 48,
    "failed": 0,
    "skipped": 0
  },
  "coverage_percent": 94.5,
  "smoke_tests_passed": true,
  "completeness_percent": 100.0,
  "performance_impact": "acceptable",
  "todo_comments": 0,
  "commented_code": 0,
  "debug_logging": 0,
  "tests_written": true,
  "docs_updated": true
}
```

### iam-qa Evaluation Process

**Step 1: Generate Test Suite**
```
Input: FixPlan with risk_level="high"
Process:
  - Generate 3+ unit tests per impacted file (9+ total)
  - Generate 2+ integration tests for service interactions
  - Generate 1+ E2E test for full memory lifecycle
  - Identify edge cases (concurrent access, session timeout, memory failures)
Output:
  - 16 total tests planned
  - Estimated coverage: 90-95%
```

**Step 2: Validate Test Coverage**
```
Input: Coverage report 94.5%
Process:
  - Check minimum 85%: ✅ PASS (94.5% > 85%)
  - Check critical paths 95%+: ✅ PASS (agent memory is critical)
  - Check no gaps in memory code: ✅ PASS
Output:
  - Coverage Valid: TRUE
  - Meets Standard: TRUE
  - Critical Coverage: TRUE
  - Issues: NONE
```

**Step 3: Run Smoke Tests**
```
Input: Implementation details (3 files changed, key functions listed)
Process:
  - Import all 3 modified files: ✅ OK
  - Call agent initialization: ✅ OK
  - Verify callback wiring: ✅ OK
  - Test memory service availability: ✅ OK
Output:
  - 6 smoke tests run
  - 6 smoke tests passed
  - No errors or warnings
```

**Step 4: Assess Completeness**
```
Input: Implementation details
Process:
  - Step 1 (Update VertexAiMemoryBankService): ✅ DONE
  - Step 2 (Add auto_save callback): ✅ DONE
  - Step 3 (Test persistence): ✅ DONE (tests passing)
  - Step 4 (Verify lookups): ✅ DONE
  - TODOs/FIXMEs: 0 found
  - Debug code: 0 found
  - Documentation: ✅ UPDATED
Output:
  - Complete: TRUE
  - Completion: 100%
  - Blockers: NONE
```

**Step 5: Produce QAVerdict**
```
Input: All assessment data
Process:
  - Status determination:
    * Tests passing: ✅ (48 passed, 0 failed)
    * Coverage sufficient: ✅ (94.5% >= 85%)
    * Smoke tests: ✅ PASSED
    * Completeness: ✅ 100%
    * Blockers: ❌ NONE
    → Status = "pass"

  - Evidence synthesis:
    * "48 tests passed, 0 failed"
    * "Coverage: 94.5% (exceeds 85% minimum)"
    * "All implementation steps complete"
    * "Smoke tests: PASSED"
    * "No blockers or issues found"

  - Recommendations:
    * "Ready for production deployment"
    * "Excellent test coverage"
    * "All quality standards exceeded"

Output: QAVerdict
```

### iam-qa Verdict Output

```json
{
  "status": "pass",
  "notes": "QA PASSED: All tests passing (48 tests), coverage 94.5% (exceeds minimum). Implementation complete with zero TODOs. Ready for deployment.",
  "test_evidence": [
    "48 tests passed, 0 failed",
    "Coverage: 94.5% (exceeds 85% minimum)",
    "Smoke tests: PASSED",
    "All implementation steps complete",
    "Documentation updated",
    "No debug code or TODOs found"
  ],
  "test_types": ["unit", "integration", "e2e"],
  "coverage_report": {
    "coverage_percent": 94.5,
    "meets_minimum": true,
    "minimum_required": 85.0,
    "critical_paths_covered": true
  },
  "performance_impact": "acceptable",
  "security_review": "safe",
  "recommendations": [
    "Ready for production deployment",
    "Excellent test coverage and implementation quality"
  ],
  "blocking_issues": [],
  "timestamp": "2025-11-19T10:30:00Z"
}
```

**Result:** ✅ **APPROVED FOR DEPLOYMENT**

---

## Example 2: Medium-Risk Fix - Coverage Below Standard

### Scenario
A developer fixed a bug in agent configuration handling but didn't write comprehensive tests.

**FixPlan Input:**
```json
{
  "summary": "Fix agent configuration validation to handle edge cases",
  "impacted_areas": ["agents/config.py", "agents/validation.py"],
  "steps": [
    "1. Fix null check in configuration parser",
    "2. Add validation for empty config files",
    "3. Write tests for edge cases"
  ],
  "risk_level": "medium",
  "testing_strategy": ["unit", "integration"]
}
```

**Implementation Results:**
```json
{
  "files_changed": ["agents/config.py", "agents/validation.py"],
  "test_results": {
    "passed": 12,
    "failed": 0,
    "skipped": 0
  },
  "coverage_percent": 78.5,
  "smoke_tests_passed": true,
  "completeness_percent": 90.0,
  "todo_comments": 2,
  "commented_code": 1,
  "debug_logging": 0,
  "tests_written": true,
  "docs_updated": false
}
```

### iam-qa Evaluation

**Step 1-4: Testing Process**
- Generated test suite: 8 unit tests + 2 integration tests
- Coverage validation: 78.5% < 85% minimum ❌
- Smoke tests: PASSED ✅
- Completeness: 90% (2 TODOs remaining, docs not updated) ⚠️

**Step 5: Produce Verdict**
```
Status Determination:
  - Tests passing: ✅ (12/12)
  - Coverage sufficient: ❌ (78.5% < 85%)
  - Blockers: ⚠️ (2 TODOs, missing docs)
  → Status = "partial"

Issues Found:
  - Coverage 78.5% below 85% minimum
  - 2 TODO comments blocking review
  - Documentation not updated

Recommendations:
  - "Add unit tests for edge cases in config validation (need ~7 more covered lines)"
  - "Remove or complete TODO comments before merging"
  - "Update README or implementation docs"
```

### iam-qa Verdict Output

```json
{
  "status": "partial",
  "notes": "QA PARTIAL: Tests passing but coverage (78.5%) below minimum 85%. Two TODO comments found. Documentation not updated.",
  "test_evidence": [
    "12 tests passed, 0 failed",
    "Coverage: 78.5% (below 85% minimum)",
    "Smoke tests: PASSED",
    "2 TODO comments found",
    "Documentation: NOT UPDATED"
  ],
  "test_types": ["unit", "integration"],
  "coverage_report": {
    "coverage_percent": 78.5,
    "meets_minimum": false,
    "minimum_required": 85.0,
    "critical_paths_covered": true
  },
  "performance_impact": "acceptable",
  "security_review": "safe",
  "recommendations": [
    "Add ~7-10 more covered lines to reach 85% coverage",
    "Focus on edge case testing in config.py",
    "Complete or remove 2 TODO comments",
    "Update documentation for configuration validation changes"
  ],
  "blocking_issues": [
    "Coverage 78.5% below 85% minimum"
  ],
  "timestamp": "2025-11-19T10:35:00Z"
}
```

**Result:** ⚠️ **REQUIRES FIXES** - Can proceed once:
1. Coverage brought to 85%+
2. TODO comments completed or removed
3. Documentation updated

---

## Example 3: Critical Failure - Blocking Issues

### Scenario
A developer made significant changes but they broke existing tests during the merge.

**Implementation Results:**
```json
{
  "files_changed": ["agents/bob/agent.py", "agents/bob/tools/adk_tools.py"],
  "test_results": {
    "passed": 28,
    "failed": 5,
    "skipped": 2
  },
  "coverage_percent": 82.0,
  "smoke_tests_passed": false,
  "completeness_percent": 85.0,
  "todo_comments": 3,
  "commented_code": 2,
  "debug_logging": 3,
  "tests_written": true,
  "docs_updated": false,
  "smoke_test_errors": [
    "ImportError: Agent initialization failed",
    "AttributeError: 'NoneType' object has no attribute 'tools'"
  ]
}
```

### iam-qa Evaluation

**Status Determination:**
```
- Tests passing: ❌ (5 failures out of 35 tests)
- Coverage sufficient: ❌ (82% < 85%)
- Smoke tests: ❌ FAILED (2 errors)
- Debug code: ❌ (3 instances)
- TODOs: ❌ (3 comments)
→ Status = "blocked"
```

### iam-qa Verdict Output

```json
{
  "status": "blocked",
  "notes": "QA BLOCKED: 5 test failures, smoke tests failed, debug code present, and coverage below standard. Cannot proceed to deployment.",
  "test_evidence": [
    "28 tests passed, 5 FAILED, 2 skipped",
    "Coverage: 82% (below 85% minimum)",
    "Smoke tests: FAILED",
    "Errors: ImportError in agent init, NoneType in tools",
    "3 debug logging statements found",
    "3 TODO comments found"
  ],
  "test_types": ["unit", "integration"],
  "coverage_report": {
    "coverage_percent": 82.0,
    "meets_minimum": false,
    "minimum_required": 85.0
  },
  "performance_impact": "unknown",
  "security_review": "needs_review",
  "recommendations": [
    "FIX BLOCKING: Address 5 failing tests (see log details)",
    "FIX BLOCKING: Fix ImportError in agent initialization",
    "FIX BLOCKING: Fix NoneType error in tools initialization",
    "REMOVE: 3 debug logging statements",
    "COMPLETE: 3 TODO comments",
    "IMPROVE: Bring coverage from 82% to 85%+"
  ],
  "blocking_issues": [
    "5 test failures preventing deployment",
    "Smoke test failures - agent initialization broken",
    "Debug code must be removed before merge",
    "Coverage below 85% minimum"
  ],
  "timestamp": "2025-11-19T10:40:00Z"
}
```

**Result:** 🔴 **CANNOT DEPLOY** - Blocking issues must be resolved:

1. **CRITICAL:** Fix 5 failing tests
   - Error details in test output
   - Expected behavior must be restored

2. **CRITICAL:** Fix smoke test failures
   - Agent initialization broken
   - Import error in agent.py
   - NoneType in tools

3. **CRITICAL:** Remove debug code
   - 3 logging statements in production code
   - Not acceptable in main branch

4. **HIGH:** Remove TODO comments
   - 3 unfinished TODOs blocking review

5. **MEDIUM:** Improve coverage
   - Bring from 82% to 85%+ minimum

**Send back for fixes** → Once fixed, resubmit for QA evaluation

---

## Example 4: Low-Risk Fix - Quick Approval

### Scenario
A developer made a simple documentation fix with minimal code changes.

**FixPlan Input:**
```json
{
  "summary": "Fix typos in docstrings and update old API references",
  "impacted_areas": ["agents/bob/agent.py", "agents/iam_fix_plan/agent.py"],
  "steps": [
    "1. Fix docstring typos",
    "2. Update API references",
    "3. Verify documentation renders correctly"
  ],
  "risk_level": "low",
  "testing_strategy": ["smoke"]
}
```

**Implementation Results:**
```json
{
  "files_changed": ["agents/bob/agent.py", "agents/iam_fix_plan/agent.py"],
  "test_results": {
    "passed": 3,
    "failed": 0
  },
  "coverage_percent": 89.2,
  "smoke_tests_passed": true,
  "completeness_percent": 100.0,
  "todo_comments": 0,
  "commented_code": 0,
  "debug_logging": 0,
  "tests_written": false,
  "docs_updated": true
}
```

### iam-qa Evaluation

**Quick Assessment:**
- Risk level: LOW → Smoke tests sufficient ✅
- Coverage: 89.2% (excellent for doc-only change) ✅
- Smoke tests: PASSED ✅
- Completeness: 100% ✅
- Issues: NONE ✅

### iam-qa Verdict Output

```json
{
  "status": "pass",
  "notes": "QA PASSED: Low-risk documentation update. Smoke tests passing, coverage maintained at 89.2%. Ready for deployment.",
  "test_evidence": [
    "Smoke tests: PASSED",
    "Coverage maintained at 89.2%",
    "No regressions detected",
    "Documentation updated"
  ],
  "test_types": ["smoke"],
  "coverage_report": {
    "coverage_percent": 89.2,
    "meets_minimum": true,
    "minimum_required": 85.0
  },
  "recommendations": [
    "Ready for immediate deployment",
    "Documentation quality improved"
  ],
  "blocking_issues": [],
  "timestamp": "2025-11-19T10:45:00Z"
}
```

**Result:** ✅ **APPROVED FOR IMMEDIATE DEPLOYMENT**

---

## Common Scenarios Reference

| Scenario | Risk | Coverage | Tests | Verdict | Action |
|----------|------|----------|-------|---------|--------|
| Doc fix | LOW | >85% | Smoke only | ✅ PASS | Deploy |
| Config bug | MED | <85% | Unit+Int | ⚠️ PARTIAL | Fix coverage |
| Agent arch | HIGH | >90% | Unit+Int+E2E | ✅ PASS | Deploy |
| Broken tests | ANY | <80% | Failing | 🔴 BLOCKED | Fix tests |
| Security fix | MED | >85% | Full suite | ✅ PASS | Deploy |
| Performance | HIGH | >90% | Full suite | ✅ PASS | Deploy |

---

## How to Respond to iam-qa Verdicts

### If Status = "pass"
- ✅ Your implementation meets all quality standards
- Proceed with deployment confidence
- Celebrate a job well done!

### If Status = "partial"
- ⚠️ Your implementation is mostly good but needs work
- Focus on iam-qa's recommendations
- Most common: "Add more test coverage"
- Resubmit after addressing issues

### If Status = "blocked"
- 🔴 Critical issues must be fixed before deployment
- Read iam-qa's blocking_issues list carefully
- Fix each issue and resubmit
- Do not try to deploy or merge while blocked

### If Status = "fail"
- ❌ Tests are failing and deployment cannot proceed
- Fix the test failures or revert the changes
- Work with the implementation team to resolve

---

**Last Updated:** 2025-11-19
**Version:** 0.8.0
