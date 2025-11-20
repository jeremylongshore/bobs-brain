# iam-qa Testing & Quality Assurance Specialist

**Agent Name:** `iam_qa`
**Version:** 0.8.0
**Model:** Gemini 2.0 Flash Exp
**Status:** Active

## Overview

`iam-qa` is a specialized testing and quality assurance agent that ensures quality and correctness of implemented fixes before they are deployed. It operates as part of the ADK Agent Department, working between `iam-fix-impl` and `iam-doc`.

## Role & Responsibilities

iam-qa specializes in:

1. **Test Suite Design** - Creating comprehensive unit, integration, and E2E test plans
2. **Coverage Validation** - Ensuring test coverage meets minimum standards (85%)
3. **Smoke Testing** - Running basic functionality checks on implementations
4. **Completeness Assessment** - Verifying all fix plan steps are implemented
5. **QAVerdict Production** - Synthesizing findings into deployment verdicts
6. **Blocking Authority** - Can prevent deployment if quality issues are found

## Workflow

```
iam-fix-impl
    ↓
    (produces implementation with tests)
    ↓
iam-qa  ← YOU ARE HERE
    ↓
    (produces QAVerdict)
    ↓
iam-doc
    ↓
    (documents results)
```

## Key Expertise Areas

### Test Types

- **Unit Tests:** Isolated component testing with clear assertions
- **Integration Tests:** Component interaction validation
- **End-to-End Tests:** Full workflow validation
- **Smoke Tests:** Basic functionality verification
- **Regression Tests:** Ensure no existing functionality broken
- **Performance Tests:** Impact and baseline analysis

### Quality Standards

- **Minimum Coverage:** 85% for all code
- **Critical Paths:** 95%+ coverage required
- **Edge Cases:** All major branches and error paths tested
- **Performance:** No unacceptable degradation
- **Security:** No vulnerabilities in critical areas

### Verdict Status

- **"pass"** → Ready for production deployment
- **"fail"** → Tests failing, critical issues, cannot proceed
- **"partial"** → Tests mostly passing but coverage gaps or incomplete work
- **"blocked"** → Explicit blocking issues that must be resolved
- **"skipped"** → Testing deferred (only when explicitly approved)

## Inputs

iam-qa consumes:

1. **FixPlan** from iam-fix-plan
   - Implementation steps and strategy
   - Risk level assessment
   - Testing strategy outline
   - Success metrics

2. **Implementation Details**
   - Files changed
   - Test results and coverage metrics
   - Smoke test outcomes
   - Documentation updates

3. **Assessment Data**
   - All QA activity results
   - Coverage reports
   - Performance metrics
   - Security review findings

## Outputs

iam-qa produces:

1. **QAVerdict**
   ```python
   status: "pass" | "fail" | "partial" | "blocked" | "skipped"
   notes: str                          # Verdict summary
   test_evidence: List[str]            # Test results
   test_types: List[str]               # ["unit", "integration", "e2e"]
   coverage_report: Dict               # Coverage metrics
   performance_impact: str             # "acceptable"|"degraded"|"improved"
   security_review: str                # "safe"|"needs_review"|"issues_found"
   recommendations: List[str]          # Action items
   blocking_issues: List[str]          # Issues preventing deployment
   ```

2. **Test Specifications**
   - Unit test specs with assertions
   - Integration test scenarios
   - E2E test workflows
   - Coverage targets and gaps

3. **Assessment Reports**
   - Completeness status
   - Coverage analysis
   - Risk assessment
   - Mitigation recommendations

## Available Tools

### generate_test_suite(fix_data: str) → str

Design a comprehensive test plan from a FixPlan.

```python
input = {
    "summary": "Fix description",
    "impacted_areas": ["file1.py", "file2.py"],
    "risk_level": "high",
    "testing_strategy": ["unit", "integration"]
}

output = {
    "unit_tests": [...],
    "integration_tests": [...],
    "e2e_tests": [...],
    "total_test_count": 15,
    "estimated_coverage": "85%"
}
```

### validate_test_coverage(test_results: str) → str

Validate test coverage meets quality standards.

```python
input = {
    "coverage_percent": 85.0,
    "uncovered_areas": ["file.py:10-20"],
    "critical_paths": ["auth.py"]
}

output = {
    "valid": True,
    "meets_standard": True,
    "critical_paths_covered": True,
    "issues": [],
    "recommendations": []
}
```

### run_smoke_tests(implementation_data: str) → str

Run basic functionality smoke tests.

```python
input = {
    "files_changed": ["file1.py"],
    "key_functions": ["func1"],
    "entry_points": ["app.py"]
}

output = {
    "passed": True,
    "tests_run": 10,
    "tests_passed": 10,
    "tests_failed": 0,
    "duration_seconds": 2.5
}
```

### assess_fix_completeness(implementation_data: str) → str

Assess whether implementation fully addresses fix plan.

```python
input = {
    "fix_plan_steps": ["step1", "step2"],
    "completed_steps": ["step1", "step2"],
    "todo_comments": 0,
    "tests_written": True,
    "docs_updated": True
}

output = {
    "complete": True,
    "completion_percent": 100.0,
    "issues": [],
    "blockers": []
}
```

### produce_qa_verdict(assessment_data: str) → str

Generate final QAVerdict from all assessment results.

```python
input = {
    "test_results": {"passed": 45, "failed": 0},
    "coverage_percent": 88.5,
    "smoke_tests_passed": True,
    "completeness_percent": 95.0,
    "blocking_issues": []
}

output = {
    "status": "pass",
    "notes": "All tests passing...",
    "test_evidence": ["45 tests passed", "Coverage 88.5%"],
    "recommendations": ["Ready for deployment"],
    "blocking_issues": []
}
```

## Usage Examples

### Example 1: High-Risk Fix Evaluation

```
Input: FixPlan for agent architecture refactor
Risk Level: HIGH

Process:
1. Generate comprehensive test suite (unit + integration + E2E)
2. Validate coverage targets 95%+ for critical code
3. Run smoke tests on agent startup and communication
4. Assess all implementation steps completed
5. Produce QAVerdict

Output: QAVerdict(status="pass", coverage=96%, recommendations=["Ready for production"])
```

### Example 2: Blocked Due to Coverage

```
Input: FixPlan for bug fix with tests
Risk Level: MEDIUM

Process:
1. Generate test suite
2. Validate coverage → Found 72% (below 85% minimum)
3. Assess completeness → Found 3 TODO comments
4. Run smoke tests → PASSED
5. Produce QAVerdict with blockers

Output: QAVerdict(
    status="blocked",
    blocking_issues=["Coverage 72% below 85%", "3 TODO comments"],
    recommendations=["Add coverage for uncovered paths", "Remove TODOs"]
)
```

### Example 3: Partial Pass - Needs Work

```
Input: Implementation with partial testing
Risk Level: LOW

Process:
1. Generate test specs
2. Validate coverage → 81% (below 85%)
3. Run smoke tests → PASSED
4. Assess completeness → COMPLETE
5. Produce verdict with recommendations

Output: QAVerdict(
    status="partial",
    coverage_report={"coverage_percent": 81, "meets_standard": False},
    recommendations=["Add unit tests to reach 85% coverage"]
)
```

## Integration Points

### From iam-fix-impl

Receives:
- Complete implementation with code changes
- Test suite and test results
- Coverage metrics (pytest --cov output)
- Smoke test results

### To iam-doc

Sends:
- QAVerdict for documentation
- Test evidence for archival
- Coverage reports for tracking
- Recommendations for future work

### To iam-senior-adk-devops-lead

Sends:
- QAVerdict for deployment decision
- Blocking issues that prevent deployment
- Risk assessment and mitigation
- Recommendations for rollout strategy

## Blocking Authority

iam-qa has authority to **BLOCK** deployment when:

1. **Test Failures** - Unexplained test failures exist
2. **Coverage Gaps** - Coverage below 85% without explicit risk acceptance
3. **Incomplete Implementation** - Fix plan steps not implemented
4. **Security Issues** - Vulnerabilities found and unaddressed
5. **Performance Regression** - Unacceptable degradation detected
6. **Blocking Issues** - Explicit blockers identified

When blocking, iam-qa provides:
- Clear explanation of why it's blocked
- Specific steps to unblock
- Risk assessment if override considered
- Expected effort to resolve

## Quality Standards

### Code Coverage

- **Minimum:** 85% for all code
- **Critical Paths:** 95%+ required
- **Target:** 90%+ across codebase

### Test Types

Each fix should include appropriate test types:
- **Low Risk:** Smoke tests + unit tests (70%+ coverage acceptable)
- **Medium Risk:** Unit + integration tests (85% coverage required)
- **High Risk:** Unit + integration + E2E tests (90%+ coverage required)

### Documentation

- Test specifications documented
- Test evidence archived
- Failure root causes documented
- Recommendations actionable and specific

## Verdict Reasoning

When iam-qa produces a verdict, it considers:

1. **Test Results**
   - Number of tests passing/failing
   - Test execution time
   - Flakiness or inconsistency

2. **Coverage Metrics**
   - Overall code coverage percentage
   - Critical path coverage
   - Coverage trends over time

3. **Implementation Completeness**
   - All fix plan steps implemented
   - No debug code or TODOs
   - Documentation updated

4. **Functional Validation**
   - Smoke tests passing
   - Integration tests passing
   - No regressions detected

5. **Non-Functional Validation**
   - Performance acceptable
   - Security review passed
   - Error handling correct

6. **Risk Assessment**
   - Risk level of changes
   - Blast radius if something fails
   - Rollback feasibility

## Communication Style

iam-qa communicates with:

- **Developers:** Constructive feedback, actionable recommendations
- **Foreman:** Clear verdicts with blocking issues and mitigation
- **Metrics/Monitoring:** Structured QAVerdict for tracking

Key principles:
- Be decisive (clear go/no-go)
- Be evidence-based (backed by metrics)
- Be constructive (help fix issues)
- Be realistic (acknowledge constraints)
- Be thorough (comprehensive assessment)

## Environment Variables

Required:
- `PROJECT_ID` - GCP project ID
- `LOCATION` - Cloud region (default: us-central1)
- `AGENT_ENGINE_ID` - Vertex AI Agent Engine ID
- `APP_NAME` - Application name (default: bobs-brain)

Optional:
- `AGENT_SPIFFE_ID` - SPIFFE identity (auto-set in Agent Engine)

## Deployment

iam-qa is deployed to Vertex AI Agent Engine:

```bash
# Deploy via CI/CD (recommended)
git push origin main
# → GitHub Actions triggers deploy

# Manual deployment (use CI/CD instead)
adk deploy agents.iam_qa
```

## Testing iam-qa

Test the agent locally (CI smoke test only):

```bash
# Load and verify agent
python3 -c "from agents.iam_qa import get_agent; a = get_agent(); print('✅ Agent loaded')"

# Run tests
pytest tests/agents/test_iam_qa.py -v

# With coverage
pytest --cov=agents.iam_qa tests/agents/test_iam_qa.py
```

## Troubleshooting

### "BLOCKED: Coverage below 85%"

**Cause:** Test coverage insufficient for quality standards
**Solution:** Add more unit tests for uncovered code paths

```bash
# Check coverage details
pytest --cov=src --cov-report=html
# Open htmlcov/index.html and add tests for red lines
```

### "BLOCKED: X failing tests"

**Cause:** Tests are failing on the implementation
**Solution:** Fix the test failures in implementation

```bash
pytest -v --tb=short
# Read failure details and fix code
```

### "BLOCKED: Incomplete implementation"

**Cause:** Not all fix plan steps are implemented
**Solution:** Complete remaining implementation steps

### "PARTIAL: Recommendations provided"

**Cause:** Implementation acceptable but could be improved
**Solution:** Address recommendations for future improvement

## Further Reading

- [QA Decision Playbook](../../000-docs/QA-DECISION-PLAYBOOK.md)
- [Run QA Evaluation](../../000-docs/RUN-QA-EVALUATION.md)
- [Testing Standards](../../000-docs/TESTING-STANDARDS.md)
- [System Prompt](system-prompt.md)
- [Agent Card](agent_card.yaml)

---

**Created:** 2025-11-19
**Version:** 0.8.0
**Status:** Active
**Last Updated:** 2025-11-19
