# iam-issue: Issue Author & GitHub Formatter Specialist

## Overview

**iam-issue** is a specialized ADK agent that transforms raw findings, audit reports, and structured data into high-quality, well-formatted GitHub issues. It's part of the **iam-* agent team** in the bobs-brain repository, working alongside iam-adk, iam-cleanup, and other specialists.

## Purpose

This agent solves a critical problem: converting unstructured findings into professional, actionable GitHub issues. It ensures that:

- Issues are clearly written and immediately understandable
- All issues are properly categorized and labeled
- Format and structure are consistent across the project
- Metadata is correctly embedded for automation
- Quality standards are maintained

## Architecture

### Core Pattern

```
iam-adk (audit findings)        iam-cleanup (cleanup tasks)
        |                              |
        └─────────────┬────────────────┘
                      |
                      v
              IssueSpec objects
                      |
                      v
              iam-issue formatter
                      |
                      v
        GitHub-ready issue body
                      |
                      v
      iam-senior-adk-devops-lead
        (posts to GitHub via API)
```

### Agent Composition

```
agents/iam_issue/
├── agent.py                 # LlmAgent with tools and memory
├── __init__.py             # Module exports
├── system-prompt.md        # Role and responsibilities
├── agent_card.yaml         # A2A protocol contract
├── README.md               # This file
└── tools/
    ├── __init__.py
    └── formatting_tools.py # Issue formatting utilities
```

## Key Features

### 1. Issue Validation
- Validates `IssueSpec` objects for completeness
- Checks required fields and constraints
- Provides quality scores and improvement suggestions
- Identifies missing or incomplete information

### 2. Markdown Formatting
- Converts structured data to GitHub-compatible markdown
- Organizes issues with consistent sections:
  - Summary
  - Component
  - Type & Severity
  - Reproduction steps (for bugs)
  - Acceptance criteria (for tasks)
  - References
  - Metadata

### 3. Label Generation
- Automatically creates appropriate GitHub labels
- Components: agents, service, infra, ci, docs
- Severity: priority-high, priority-critical
- Types: bug, tech_debt, improvement, task, violation
- Custom labels from user input

### 4. Metadata Management
- Embeds issue tracking information
- Creates HTML comments for metadata
- Enables downstream automation
- Tracks issue ID, component, type, severity

## How It Works

### Input: IssueSpec Contract

```python
@dataclass
class IssueSpec:
    # Required
    title: str                                  # 10-100 chars
    description: str                           # 20+ chars
    component: Literal["agents", "service", ...]
    severity: Literal["low", "medium", "high", "critical"]
    type: Literal["bug", "tech_debt", "improvement", "task", "violation"]

    # Optional but recommended
    repro_steps: List[str] = []
    acceptance_criteria: List[str] = []
    labels: List[str] = []
    links: List[str] = []
    assignees: List[str] = []
    milestone: Optional[str] = None
    notes: str = ""
```

### Output: GitHub Issue

```markdown
## Summary
[Detailed description]

## Component
`agents`

## Type
`bug`

## Severity
`critical`

## Reproduction Steps
1. Step one
2. Step two
3. Expected vs actual result

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## References
- Link to related code
- Link to documentation
```

## Tools

### validate_issue_spec(issue_data: str) -> str

Validates an IssueSpec for completeness and correctness.

**Input**: JSON string containing IssueSpec data
**Output**: Validation report with errors, warnings, quality score

```python
{
    "is_valid": true,
    "errors": [],
    "warnings": ["Missing acceptance_criteria"],
    "score": 0.95
}
```

### format_issue_markdown(issue_data: str) -> str

Converts IssueSpec to GitHub-compatible markdown.

**Input**: JSON string containing IssueSpec data
**Output**: Formatted markdown for GitHub issue

### generate_issue_labels(issue_data: str) -> str

Generates appropriate labels based on issue metadata.

**Input**: JSON string containing IssueSpec data
**Output**: Label list with component, type, severity labels

```python
{
    "labels": ["bug", "priority-critical", "agents", "needs-review"],
    "suggested": true,
    "count": 4
}
```

### create_github_issue_body(issue_data: str, include_metadata: bool = True) -> str

Creates complete GitHub issue body with formatting and metadata.

**Input**: JSON string containing IssueSpec data
**Output**: Full issue body ready for GitHub posting

## Integration Points

### With iam-adk
- Receives: `AuditReport` with violations
- Produces: GitHub issues for each violation
- Flow: `audit findings → violations → IssueSpecs → formatted issues`

### With iam-cleanup
- Receives: `CleanupTask` specifications
- Produces: GitHub issues for cleanup work
- Flow: `cleanup tasks → IssueSpecs → formatted issues`

### With iam-senior-adk-devops-lead
- Receives: Issue creation requests
- Produces: Complete, formatted GitHub issues
- Flow: `foreman → create_issue → iam-issue → formatted issue → foreman posts`

### With iam-fix-plan
- Receives: Optional context from fix plans
- Produces: Issues with linked fix plan references
- Flow: `issue + fix_plan_link → iam-issue → formatted with links`

## Usage Example

### Scenario: iam-adk finds an ADK pattern violation

```python
# 1. iam-adk produces audit finding
audit_report = AuditReport(
    summary="Found Runner usage in service/ code",
    violations=[{
        "rule": "R3",
        "severity": "HIGH",
        "message": "Runner imported in service/a2a_gateway/main.py (line 15)",
    }]
)

# 2. Convert to IssueSpec
issue_spec = {
    "title": "ADK Runner imported in service gateway",
    "description": "Violation of R3: Runner should not be used in service/ code...",
    "component": "service",
    "severity": "high",
    "type": "violation",
    "repro_steps": [
        "Open service/a2a_gateway/main.py",
        "Look at line 15",
        "See Runner import"
    ],
    "acceptance_criteria": [
        "[ ] Remove Runner import from service code",
        "[ ] Use REST API to call Agent Engine instead",
        "[ ] Verify tests pass"
    ],
    "links": [
        "https://google.github.io/adk-docs/hard-mode-rules/#r3"
    ]
}

# 3. iam-issue validates and formats
validity = validate_issue_spec(json.dumps(issue_spec))
# → is_valid: true, score: 0.95

markdown = format_issue_markdown(json.dumps(issue_spec))
# → Properly formatted markdown

labels = generate_issue_labels(json.dumps(issue_spec))
# → ["violation", "priority-high", "service"]

body = create_github_issue_body(json.dumps(issue_spec))
# → Complete issue body ready for posting

# 4. Foreman posts to GitHub
```

## Quality Standards

### Issue Clarity
- Clear, specific titles
- Complete descriptions
- Well-organized sections
- Professional language

### Issue Completeness
- All required fields present
- Optional fields included when relevant
- Sufficient context for actionability
- Related issues linked

### Issue Actionability
- Clear reproduction steps (for bugs)
- Well-defined acceptance criteria
- Realistic scope
- Specific, not vague

### Issue Organization
- Correct component
- Appropriate severity
- Proper type classification
- Consistent labels

## Compliance

### Hard Mode Rules (R1-R8)

- **R1**: Uses google-adk LlmAgent ✓
- **R2**: Designed for Vertex AI Agent Engine ✓
- **R5**: Dual memory wiring (Session + Memory Bank) ✓
- **R7**: SPIFFE ID propagation in logs ✓
- **R3**: No Runner imports (pure formatting agent) ✓
- **R6**: All docs in 000-docs/ ✓
- **R4**: CI-only deployment (no local credentials) ✓
- **R8**: No drift from formatting standards ✓

## Testing

### Unit Tests

```bash
# Test issue validation
pytest tests/unit/test_iam_issue_validation.py

# Test markdown formatting
pytest tests/unit/test_iam_issue_formatting.py

# Test label generation
pytest tests/unit/test_iam_issue_labels.py

# All iam-issue tests
pytest tests/unit/test_iam_issue*.py
```

### Integration Tests

```bash
# Test with sample IssueSpecs
pytest tests/integration/test_iam_issue_pipeline.py

# Test A2A communication
pytest tests/integration/test_iam_issue_a2a.py
```

### Smoke Tests (CI)

```bash
# Test agent creation
pytest tests/smoke/test_iam_issue_smoke.py
```

## Local Development

### Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config
cp .env.example .env
```

### Test Agent Creation

```bash
# Test that the agent can be created
python3 -c "
from agents.iam_issue import get_agent
agent = get_agent()
print(f'✅ Agent created: {agent.name}')
"
```

### Test Tools Directly

```python
import json
from agents.iam_issue.tools.formatting_tools import (
    validate_issue_spec,
    format_issue_markdown,
)

# Sample IssueSpec
issue = {
    "title": "Test issue",
    "description": "This is a test issue for validation",
    "component": "agents",
    "severity": "medium",
    "type": "improvement"
}

# Validate
result = validate_issue_spec(json.dumps(issue))
print(json.loads(result))

# Format
markdown = format_issue_markdown(json.dumps(issue))
print(markdown)
```

## Deployment

### Via ADK CLI

```bash
# Deploy to Vertex AI Agent Engine
adk deploy agents.iam_issue --trace_to_cloud

# Logs
gcloud logging read "resource.type=cloud_run_managed" \
  --filter="labels.agent=iam_issue" --limit=50
```

### Via GitHub Actions

Automatic deployment triggered on push to main branch.

```yaml
# .github/workflows/deploy-agent-engine.yml
- name: Deploy iam-issue
  run: adk deploy agents.iam_issue --trace_to_cloud
```

## Monitoring

### Metrics

- `iam_issue_issues_created` - Total issues created
- `iam_issue_issues_validated` - Total issues validated
- `iam_issue_quality_score` - Average quality score
- `iam_issue_formatting_latency_ms` - Formatting latency
- `iam_issue_labels_generated` - Total labels generated

### Logs

```bash
# View iam-issue logs
gcloud logging read "resource.type=cloud_run" \
  --filter='jsonPayload.spiffe_id=~"iam_issue"' \
  --limit=100 --format=json

# Follow real-time logs
gcloud logging read --follow \
  --filter='jsonPayload.spiffe_id=~"iam_issue"'
```

## Troubleshooting

### Issue Validation Fails

**Problem**: `validate_issue_spec` returns errors

**Solution**:
1. Check required fields (title, description, component, severity, type)
2. Verify enum values (component, severity, type)
3. Ensure title is 10-100 characters
4. Check field format and constraints

### Formatting Produces Blank Output

**Problem**: `format_issue_markdown` returns empty markdown

**Solution**:
1. Verify input is valid JSON
2. Check that required fields exist in IssueSpec
3. Verify description is present
4. Look for exceptions in logs

### Labels Not Generated

**Problem**: `generate_issue_labels` returns only default labels

**Solution**:
1. Check component field is valid
2. Verify severity is one of: low, medium, high, critical
3. Ensure type is one of: bug, tech_debt, improvement, task, violation
4. Check for exceptions in logs

## Related Documentation

- **System Prompt**: `system-prompt.md` - Complete role and responsibilities
- **Agent Card**: `agent_card.yaml` - A2A protocol contract
- **IssueSpec Contract**: `agents/iam_contracts.py` - Data model
- **Hard Mode Rules**: See CLAUDE.md (R1-R8)
- **Filing Standards**: `000-docs/` structure and NNN-CC-ABCD naming

## Future Enhancements

- [ ] GitHub API integration for direct issue posting
- [ ] Template-based issue creation
- [ ] Automated issue linking (related issues)
- [ ] Issue templating by type (bug, feature, etc.)
- [ ] Bulk issue creation from audit reports
- [ ] Issue update and modification support

## Support

For issues or questions:
- Check `system-prompt.md` for role details
- Review `agent_card.yaml` for A2A contract
- See troubleshooting section above
- Check `000-docs/` for architecture details

---

**Version**: 0.8.0
**Last Updated**: 2025-11-19
**Status**: Production Ready
