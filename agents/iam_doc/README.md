# iam-doc - Documentation Specialist Agent

**Agent Type:** LlmAgent (ADK)
**Model:** gemini-2.0-flash-exp
**Status:** Active Development
**Version:** 0.8.0+

## Purpose

The iam-doc agent is a specialized documentation agent responsible for creating, maintaining, and organizing technical documentation across the bobs-brain agent factory. It ensures all phases, changes, and decisions are properly documented following Document Filing System v2.0 standards.

## Responsibilities

### 1. After-Action Reports (AARs)
- Generate AARs for completed phases
- Document objectives, outcomes, lessons learned
- Create actionable next steps
- Link to related issues and commits
- Follow NNN-AA-REPT-description.md naming

### 2. README Maintenance
- Update agent documentation
- Maintain quick start guides
- Document new features and tools
- Keep architecture diagrams current
- Update troubleshooting sections

### 3. Design Documentation
- Create Architecture Decision Records (ADRs)
- Document key design decisions
- Record alternatives considered
- Explain trade-offs and rationale
- Follow NNN-AT-ARCH-description.md naming

### 4. Documentation Structure
- Maintain 000-docs/ organization
- Enforce Document Filing System v2.0
- Ensure consistent formatting
- Cross-reference related docs
- Track documentation coverage

## Tools

### generate_aar
Generate After-Action Reports for completed phases.

**Parameters:**
- `phase_name`: Phase name (e.g., "Phase 1 - Agent Creation")
- `objectives`: List of original objectives
- `outcomes`: List of actual outcomes
- `lessons_learned`: Key insights and learnings
- `next_steps`: Recommended future actions
- `related_issues`: Optional GitHub issue IDs

**Returns:** Dict with `file_name`, `content`, and `metadata`

### update_readme
Update sections in README files.

**Parameters:**
- `readme_path`: Path to README.md file
- `section_name`: Section header (e.g., "## Agents")
- `new_content`: New content for section
- `append`: If True, append instead of replace

**Returns:** Dict with `success`, `updated_path`, `changes_made`

### create_design_doc
Create design documentation for architectural decisions.

**Parameters:**
- `title`: Document title
- `purpose`: Purpose and context
- `architecture`: Architecture description
- `decisions`: List of decisions with rationale
- `alternatives`: Optional alternatives considered

**Returns:** Dict with `file_name`, `content`, `metadata`

### list_documentation
List all documentation in 000-docs/ directory.

**Parameters:**
- `docs_dir`: Path to 000-docs directory
- `category_filter`: Optional category code filter

**Returns:** Dict with `total_docs`, `docs`, `categories`

## Outputs

### DocumentationUpdate
Structured output from iam-doc following the contract:

```python
from agents.iam_contracts import DocumentationUpdate

doc_update = DocumentationUpdate(
    type="aar",  # or "readme", "api_doc", "design_doc"
    title="Phase 1 Implementation AAR",
    content="# After-Action Report...",
    file_path="000-docs/6767-042-AA-REPT-phase-1-implementation.md",
    related_issues=["#123", "#124"],
    sections_updated=["Objectives", "Outcomes"],
    review_status="draft",
    metadata={"phase": "1", "timestamp": "2025-11-19T21:00:00Z"}
)
```

## Hard Mode Compliance

### R1: ADK-Only Implementation
- Uses `google.adk.agents.LlmAgent`
- No alternative frameworks (LangChain, CrewAI, etc.)
- Pure ADK FunctionTool pattern for all tools

### R2: Vertex AI Agent Engine Runtime
- Designed for Agent Engine deployment
- Runner created only in Agent Engine container
- No local execution in production (R4)

### R5: Dual Memory Wiring
- `VertexAiSessionService` for short-term cache
- `VertexAiMemoryBankService` for long-term persistence
- `auto_save_session_to_memory` callback configured

### R7: SPIFFE ID Propagation
- All logs include `spiffe_id` field
- Agent identity tracked throughout execution
- Metadata includes SPIFFE ID reference

## Integration

### With iam-senior-adk-devops-lead (Foreman)
The foreman delegates documentation tasks to iam-doc:
- Phase completion → Request AAR generation
- Architecture changes → Request design doc update
- Feature additions → Request README update

### With Other iam-* Agents
- **iam-adk**: Receives AuditReports → Generates compliance AARs
- **iam-qa**: Receives QAVerdicts → Documents test results
- **iam-fix-impl**: Receives code changes → Updates technical docs
- **iam-issue**: Receives IssueSpecs → Links in AARs

## Usage Examples

### Generate AAR for Phase
```python
from agents.iam_doc import get_agent

agent = get_agent()

# Request AAR generation
result = agent.run(
    "Generate an AAR for Phase 1 - iam-doc Agent Creation. "
    "Objectives: Create agent, implement tools. "
    "Outcomes: Agent created successfully, tools working. "
    "Lessons: ADK patterns work well for specialized agents."
)
```

### Update README
```python
# Request README update
result = agent.run(
    "Update the README.md Agents section to add information about iam-doc. "
    "It's a documentation specialist agent with AAR generation capabilities."
)
```

### Create Design Doc
```python
# Request design documentation
result = agent.run(
    "Create a design document for the iam-doc agent architecture. "
    "Key decision: Use FunctionTool for all documentation operations. "
    "Rationale: Simple, testable, follows ADK patterns."
)
```

## Testing

### Smoke Test
```bash
# Test agent creation
cd /home/jeremy/000-projects/iams/bobs-brain
python3 -c "from agents.iam_doc import get_agent; a = get_agent(); print('✅ iam-doc agent created')"
```

### Tool Testing
```bash
# Test AAR generation
python3 -c "
from agents.iam_doc.tools import generate_aar
result = generate_aar(
    phase_name='Test Phase',
    objectives=['Test objective'],
    outcomes=['Test outcome'],
    lessons_learned=['Test lesson'],
    next_steps=['Test next step']
)
print(f'AAR generated: {result[\"file_name\"]}')"
```

## Document Filing System v2.0

All documentation follows the standard:

**Format:** `NNN-CC-ABCD-description.ext`

**Categories:**
- **AA** - After-Action Reports
- **AT** - Architecture & Technical
- **PP** - Product & Planning
- **DR** - Documentation & Reference
- **OD** - Operations & Deployment

**Examples:**
- `042-AA-REPT-phase-1-implementation.md` (AAR)
- `043-AT-ARCH-iam-doc-agent-design.md` (Design doc)
- `044-PP-PLAN-phase-2-deployment.md` (Plan)

## Future Enhancements

1. **Automated AAR Triggers**: Generate AARs automatically on phase completion
2. **Doc Health Checks**: Scan for outdated or missing documentation
3. **Cross-Reference Validation**: Ensure all links and references are valid
4. **Template Library**: Reusable templates for common doc types
5. **Changelog Generation**: Auto-generate changelogs from commits

## Related Documentation

- **Agent Contracts:** `/home/jeremy/000-projects/iams/bobs-brain/agents/iam_contracts.py`
- **Document Filing Standard:** Referenced in CLAUDE.md files
- **ADK Documentation:** Uses standard ADK LlmAgent patterns
- **000-docs/:** All generated documentation stored here

---

**Last Updated:** 2025-11-19
**Status:** Active
**Owner:** Bob's Brain Agent Factory
