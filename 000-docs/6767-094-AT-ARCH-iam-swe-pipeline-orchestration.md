# 6767-094-AT-ARCH-iam-swe-pipeline-orchestration.md

**Date Created:** 2025-11-20
**Category:** AT - Architecture & Technical
**Type:** ARCH - Architecture Document
**Status:** IMPLEMENTATION READY ✅

---

## Executive Summary

This document defines the **IAM Department SWE Pipeline** orchestrated by iam-senior-adk-devops-lead (foreman). The pipeline coordinates eight specialist iam-* agents to analyze, fix, test, and document improvements to target repositories in a structured, repeatable workflow.

---

## Pipeline Architecture

### Overview
```
Input: Repository + Task Description
           ↓
    [iam-senior-adk-devops-lead]
           ↓
    ┌──────────────┐
    │ Orchestrator │
    └──────┬───────┘
           ↓
    ┌──────────────────────────────────┐
    │  Step 1: iam-adk (Analysis)       │
    │  Step 2: iam-issue (Issues)       │
    │  Step 3: iam-fix-plan (Planning)   │
    │  Step 4: iam-fix-impl (Implement)  │
    │  Step 5: iam-qa (Verification)     │
    │  Step 6: iam-doc (Documentation)   │
    │  Step 7: iam-cleanup (Optional)    │
    │  Step 8: iam-index (Knowledge)     │
    └──────────────────────────────────┘
           ↓
Output: PipelineResult (Issues + Fixes + Docs)
```

### Pipeline Steps

| Step | Agent | Input | Output | Purpose |
|------|-------|-------|--------|---------|
| 1 | **iam-adk** | Repo path, task | AnalysisReport | Analyze ADK compliance |
| 2 | **iam-issue** | AnalysisReport | List[IssueSpec] | Create structured issues |
| 3 | **iam-fix-plan** | IssueSpecs | List[FixPlan] | Plan fixes for issues |
| 4 | **iam-fix-impl** | FixPlans | List[CodeChange] | Implement code changes |
| 5 | **iam-qa** | CodeChanges | List[QAVerdict] | Verify fixes are safe |
| 6 | **iam-doc** | Issues, Plans | List[DocumentationUpdate] | Update documentation |
| 7 | **iam-cleanup** | Issues | List[CleanupTask] | Identify tech debt |
| 8 | **iam-index** | PipelineResult | List[IndexEntry] | Update knowledge base |

---

## Contract Objects

### Input Contract
```python
@dataclass
class PipelineRequest:
    repo_hint: str                # Target repository
    task_description: str          # What to do
    env: Literal["dev", "staging", "prod"]
    max_issues_to_fix: int = 2
    include_cleanup: bool = False
    include_indexing: bool = True
```

### Output Contract
```python
@dataclass
class PipelineResult:
    request: PipelineRequest
    issues: List[IssueSpec]
    plans: List[FixPlan]
    implementations: List[CodeChange]
    qa_report: List[QAVerdict]
    docs: List[DocumentationUpdate]
    cleanup: List[CleanupTask]
    index_updates: List[IndexEntry]

    # Metrics
    total_issues_found: int
    issues_fixed: int
    issues_documented: int
    pipeline_duration_seconds: float
```

### Inter-Agent Contracts

Each agent consumes and produces specific contract objects:

| Contract | Purpose | Fields |
|----------|---------|--------|
| **IssueSpec** | Structured issue | id, type, severity, title, file_path |
| **FixPlan** | How to fix issue | issue_id, steps, risk_level |
| **CodeChange** | Actual code diff | file_path, diff_text, confidence |
| **QAVerdict** | Test results | status, tests_run, safe_to_apply |
| **DocumentationUpdate** | Doc changes | doc_type, file_path, updated_text |
| **CleanupTask** | Tech debt | category, priority, safe_to_automate |
| **IndexEntry** | Knowledge update | knowledge_type, tags, storage_path |

---

## Implementation Details

### Current State: Local Stubs
```python
# agents/iam-senior-adk-devops-lead/orchestrator.py

def run_swe_pipeline(request: PipelineRequest) -> PipelineResult:
    # Step 1-8: Call stub functions
    analysis = iam_adk_analyze(...)
    issues = iam_issue_create(...)
    plans = iam_fix_plan_create(...)
    # ... etc
```

Each stub function:
- Simulates agent behavior
- Returns well-formed contract objects
- Prints progress to console
- No network calls or LLM usage

### Future State: A2A Integration
```python
# Future implementation with real A2A calls

async def run_swe_pipeline_a2a(request: PipelineRequest) -> PipelineResult:
    # Step 1: A2A call to iam-adk agent
    analysis = await a2a_client.call_agent(
        agent_id="iam-adk",
        method="analyze",
        params={"repo": request.repo_hint}
    )
    # ... etc
```

---

## Testing Strategy

### Synthetic Test Fixtures
Location: `tests/data/synthetic_repo/`
```
synthetic_repo/
├── README.md           # Fake readme
├── agents/
│   └── example.py     # Code with violations
└── agent.yaml         # ADK config (fake)
```

### Test Coverage
```python
# tests/test_swe_pipeline.py

def test_pipeline_end_to_end():
    """Test complete pipeline flow."""
    request = PipelineRequest(...)
    result = run_swe_pipeline(request)

    assert result.total_issues_found > 0
    assert len(result.plans) > 0
    assert result.pipeline_duration_seconds > 0

def test_pipeline_no_issues():
    """Test when no issues found."""
    # ...

def test_pipeline_with_cleanup():
    """Test optional cleanup phase."""
    # ...
```

### Running Tests
```bash
# Run pipeline tests
make test-swe-pipeline

# Run with coverage
pytest tests/test_swe_pipeline.py --cov=agents.iam-senior-adk-devops-lead

# Run demo
make run-swe-pipeline-demo
```

---

## Usage Examples

### Programmatic Usage
```python
from agents.iam_senior_adk_devops_lead.orchestrator import (
    run_swe_pipeline, PipelineRequest
)

# Quick audit
request = PipelineRequest(
    repo_hint="/path/to/repo",
    task_description="Audit ADK compliance",
    env="dev"
)
result = run_swe_pipeline(request)

print(f"Found {result.total_issues_found} issues")
print(f"Fixed {result.issues_fixed} issues")
```

### CLI Usage
```bash
# Run pipeline via script
python scripts/run_swe_pipeline_once.py \
    --repo-path /path/to/repo \
    --task "Find and fix ADK violations"

# Run demo with synthetic repo
make run-swe-pipeline-demo
```

---

## Pipeline Configuration

### Environment-Specific Settings

| Environment | Max Issues | Cleanup | Indexing | Review Required |
|------------|------------|---------|----------|-----------------|
| **dev** | 2 | No | Yes | No |
| **staging** | 5 | Yes | Yes | Yes |
| **prod** | 10 | Yes | Yes | Yes |

### Risk Thresholds

| Risk Level | Auto-Apply | Manual Review | Block |
|------------|------------|---------------|-------|
| **Low** | ✅ | | |
| **Medium** | | ✅ | |
| **High** | | | ✅ |

---

## Future A2A Integration

### Deployment Architecture
```
Bob (Orchestrator)
    ↓ A2A
iam-senior-adk-devops-lead (Foreman)
    ↓ A2A
┌────────────────────────┐
│ iam-adk    (Agent Engine) │
│ iam-issue  (Agent Engine) │
│ iam-fix-*  (Agent Engine) │
│ iam-qa     (Agent Engine) │
│ iam-doc    (Agent Engine) │
│ iam-cleanup(Agent Engine) │
│ iam-index  (Agent Engine) │
└────────────────────────┘
```

### A2A Protocol Flow
1. Bob receives user request via Slack
2. Bob calls foreman via A2A
3. Foreman orchestrates pipeline:
   - Parallel calls where possible
   - Sequential where dependencies exist
4. Results aggregated and returned to Bob
5. Bob formats response for user

### AgentCard Requirements
Each iam-* agent needs:
- Unique agent_id
- Input/output schemas matching contracts
- A2A endpoint configuration
- Proper SPIFFE ID

---

## Monitoring & Metrics

### Pipeline Metrics
- **Throughput**: Pipelines/hour
- **Latency**: Average duration
- **Success Rate**: Successful completions
- **Fix Rate**: Issues fixed / issues found

### Agent Metrics
- **Response Time**: Per agent latency
- **Error Rate**: Failures per agent
- **Confidence**: Average fix confidence

### Quality Metrics
- **Test Pass Rate**: QA verdicts passed
- **Coverage Delta**: Code coverage change
- **Complexity Delta**: Cyclomatic complexity change

---

## Error Handling

### Failure Modes

| Failure | Handling | Recovery |
|---------|----------|----------|
| Agent timeout | Skip step, log warning | Continue pipeline |
| Invalid contract | Validate, reject | Stop pipeline |
| QA failure | Mark unsafe | Skip implementation |
| Network error | Retry 3x | Fallback to cache |

### Rollback Strategy
1. Keep original code in memory
2. If QA fails, don't apply changes
3. Document attempted fixes
4. Index failures for learning

---

## Security Considerations

1. **Read-Only Analysis**: Pipeline only reads code in current implementation
2. **Sandboxed Execution**: Future A2A agents run in isolated environments
3. **Change Validation**: All changes require QA verification
4. **Audit Trail**: Complete log of all pipeline actions

---

## Performance Targets

| Metric | Target | Current (Stub) |
|--------|--------|----------------|
| Pipeline duration | < 60s | ~1s |
| Issues per second | > 10 | N/A |
| Fix success rate | > 80% | 100% (fake) |
| Memory usage | < 1GB | < 100MB |

---

## Summary

The IAM SWE Pipeline provides:
- ✅ Structured, repeatable workflow
- ✅ Clear contracts between agents
- ✅ Testable with synthetic fixtures
- ✅ Ready for A2A integration
- ✅ Comprehensive error handling
- ✅ Performance monitoring

This architecture ensures the IAM department can systematically improve code quality across any repository while maintaining safety and auditability.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-20
**Status:** Implementation Ready
**Owner:** iam-senior-adk-devops-lead

---