"""
Delegation tool for invoking iam-* specialist agents.

This tool allows the foreman to delegate tasks to specialist agents
via Agent-to-Agent (A2A) protocol or direct invocation.
"""

import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum

logger = logging.getLogger(__name__)


class SpecialistAgent(Enum):
    """Available iam-* specialist agents."""

    IAM_ADK = "iam-adk"
    IAM_ISSUE = "iam-issue"
    IAM_FIX_PLAN = "iam-fix-plan"
    IAM_FIX_IMPL = "iam-fix-impl"
    IAM_QA = "iam-qa"
    IAM_DOC = "iam-doc"
    IAM_CLEANUP = "iam-cleanup"
    IAM_INDEX = "iam-index"


def delegate_to_specialist(
    specialist: str,
    task_description: str,
    context: Optional[Dict[str, Any]] = None,
    timeout_seconds: int = 300
) -> Dict[str, Any]:
    """
    Delegate a task to a specialist agent.

    This is a mock implementation for Phase 1. In Phase 3, this will
    use actual A2A protocol to invoke agents via Agent Engine.

    Args:
        specialist: Name of the specialist agent (e.g., "iam-adk")
        task_description: Detailed description of the task to perform
        context: Optional context dictionary with additional information
        timeout_seconds: Maximum time to wait for specialist response

    Returns:
        Dict containing:
        - specialist: Name of the agent that handled the task
        - status: "success", "failure", or "timeout"
        - result: The specialist's output
        - metadata: Execution metadata (timing, logs, etc.)

    Example:
        >>> result = delegate_to_specialist(
        ...     specialist="iam-adk",
        ...     task_description="Analyze agent.py for ADK compliance",
        ...     context={"file_path": "agents/bob/agent.py"}
        ... )
    """
    logger.info(f"Delegating to {specialist}: {task_description[:100]}...")

    # Validate specialist exists
    try:
        specialist_enum = SpecialistAgent(specialist)
    except ValueError:
        return {
            "specialist": specialist,
            "status": "failure",
            "result": f"Unknown specialist: {specialist}",
            "metadata": {"error": "InvalidSpecialist"}
        }

    # Mock implementation for Phase 1
    # In Phase 3, this will make actual A2A calls
    mock_responses = {
        SpecialistAgent.IAM_ADK: {
            "status": "success",
            "result": {
                "compliance_score": 95,
                "findings": [
                    "✅ Uses ADK LlmAgent pattern",
                    "✅ Dual memory properly wired",
                    "✅ SPIFFE ID propagated",
                    "⚠️ Consider adding more comprehensive error handling"
                ],
                "recommendations": [
                    "Add retry logic for memory operations",
                    "Implement circuit breaker pattern"
                ]
            }
        },
        SpecialistAgent.IAM_ISSUE: {
            "status": "success",
            "result": {
                "issue_spec": {
                    "title": "Implement comprehensive error handling",
                    "body": "Add retry logic and circuit breaker patterns",
                    "labels": ["enhancement", "adk", "reliability"],
                    "assignees": [],
                    "milestone": "Phase 2"
                },
                "issue_url": "https://github.com/org/repo/issues/123"
            }
        },
        SpecialistAgent.IAM_FIX_PLAN: {
            "status": "success",
            "result": {
                "plan": {
                    "approach": "Add exponential backoff retry",
                    "steps": [
                        "Import retry utilities",
                        "Wrap memory operations",
                        "Add circuit breaker class",
                        "Update tests"
                    ],
                    "estimated_effort": "2 hours",
                    "risks": ["Increased complexity"]
                }
            }
        },
        SpecialistAgent.IAM_FIX_IMPL: {
            "status": "success",
            "result": {
                "files_modified": ["agent.py", "tools/delegation.py"],
                "lines_added": 45,
                "lines_removed": 10,
                "tests_added": 3,
                "commit_sha": "abc123def456"
            }
        },
        SpecialistAgent.IAM_QA: {
            "status": "success",
            "result": {
                "tests_passed": 25,
                "tests_failed": 0,
                "coverage": 92.5,
                "ci_status": "green",
                "quality_gate": "passed"
            }
        },
        SpecialistAgent.IAM_DOC: {
            "status": "success",
            "result": {
                "documents_created": [
                    "000-docs/081-AA-REPT-error-handling.md"
                ],
                "documents_updated": [
                    "README.md",
                    "CLAUDE.md"
                ],
                "word_count": 1250
            }
        },
        SpecialistAgent.IAM_CLEANUP: {
            "status": "success",
            "result": {
                "files_cleaned": 5,
                "unused_imports_removed": 12,
                "formatting_fixed": 8,
                "type_hints_added": 15
            }
        },
        SpecialistAgent.IAM_INDEX: {
            "status": "success",
            "result": {
                "documents_indexed": 34,
                "knowledge_entries": 156,
                "search_index_updated": True,
                "last_index_time": "2025-11-19T10:30:00Z"
            }
        }
    }

    # Get mock response for the specialist
    response = mock_responses.get(specialist_enum, {
        "status": "failure",
        "result": "Specialist not yet implemented"
    })

    return {
        "specialist": specialist,
        "status": response["status"],
        "result": response["result"],
        "metadata": {
            "mock_response": True,
            "phase": "Phase 1 - Mock Implementation",
            "context_provided": context is not None,
            "timeout_seconds": timeout_seconds
        }
    }


def delegate_to_multiple(
    delegations: List[Dict[str, Any]],
    execution_mode: str = "sequential"
) -> List[Dict[str, Any]]:
    """
    Delegate tasks to multiple specialists.

    Args:
        delegations: List of delegation configurations, each containing:
            - specialist: Name of the specialist
            - task_description: Task to perform
            - context: Optional context
        execution_mode: "sequential" or "parallel" (mock in Phase 1)

    Returns:
        List of results from each specialist

    Example:
        >>> results = delegate_to_multiple([
        ...     {
        ...         "specialist": "iam-adk",
        ...         "task_description": "Analyze code"
        ...     },
        ...     {
        ...         "specialist": "iam-doc",
        ...         "task_description": "Update documentation"
        ...     }
        ... ])
    """
    results = []

    for delegation in delegations:
        result = delegate_to_specialist(
            specialist=delegation["specialist"],
            task_description=delegation["task_description"],
            context=delegation.get("context")
        )
        results.append(result)

    return results


def check_specialist_availability(specialist: str) -> bool:
    """
    Check if a specialist agent is available.

    In Phase 1, this returns True for known specialists.
    In Phase 3, this will check actual Agent Engine status.

    Args:
        specialist: Name of the specialist agent

    Returns:
        True if specialist is available, False otherwise
    """
    try:
        SpecialistAgent(specialist)
        return True
    except ValueError:
        return False


def get_specialist_capabilities(specialist: str) -> Dict[str, Any]:
    """
    Get the capabilities of a specialist agent.

    Args:
        specialist: Name of the specialist agent

    Returns:
        Dictionary describing the specialist's capabilities
    """
    capabilities = {
        "iam-adk": {
            "description": "ADK/Vertex design and static analysis specialist",
            "capabilities": [
                "Analyze code for ADK compliance",
                "Detect pattern violations",
                "Suggest ADK best practices",
                "Validate Agent Engine compatibility"
            ],
            "input_types": ["code_files", "agent_configs", "terraform_configs"],
            "output_types": ["compliance_report", "findings", "recommendations"]
        },
        "iam-issue": {
            "description": "GitHub issue specification and creation specialist",
            "capabilities": [
                "Create well-structured issue specs",
                "Write comprehensive issue descriptions",
                "Set appropriate labels and metadata",
                "Link related issues and PRs"
            ],
            "input_types": ["problem_description", "context", "requirements"],
            "output_types": ["issue_spec", "issue_url"]
        },
        "iam-fix-plan": {
            "description": "Fix planning and design specialist",
            "capabilities": [
                "Analyze problems and design solutions",
                "Create step-by-step fix plans",
                "Estimate effort and complexity",
                "Identify risks and dependencies"
            ],
            "input_types": ["issue_spec", "codebase_context", "constraints"],
            "output_types": ["fix_plan", "approach", "estimates"]
        },
        "iam-fix-impl": {
            "description": "Implementation and coding specialist",
            "capabilities": [
                "Implement fixes according to plan",
                "Write production-quality code",
                "Follow ADK patterns",
                "Create appropriate tests"
            ],
            "input_types": ["fix_plan", "code_context", "test_requirements"],
            "output_types": ["code_changes", "test_files", "commit_info"]
        },
        "iam-qa": {
            "description": "Testing and CI/CD verification specialist",
            "capabilities": [
                "Run comprehensive tests",
                "Verify CI/CD pipeline status",
                "Check code coverage",
                "Validate quality gates"
            ],
            "input_types": ["code_changes", "test_files", "ci_config"],
            "output_types": ["test_results", "coverage_report", "ci_status"]
        },
        "iam-doc": {
            "description": "Documentation and AAR creation specialist",
            "capabilities": [
                "Write technical documentation",
                "Create After-Action Reports",
                "Update existing docs",
                "Follow 000-docs conventions"
            ],
            "input_types": ["work_performed", "decisions_made", "outcomes"],
            "output_types": ["documents", "aars", "updates"]
        },
        "iam-cleanup": {
            "description": "Repository hygiene specialist",
            "capabilities": [
                "Remove unused code",
                "Fix formatting issues",
                "Add type hints",
                "Organize imports"
            ],
            "input_types": ["code_files", "cleanup_scope", "standards"],
            "output_types": ["cleanup_report", "files_modified"]
        },
        "iam-index": {
            "description": "Knowledge management specialist",
            "capabilities": [
                "Index documentation",
                "Update search indices",
                "Manage knowledge base",
                "Track document relationships"
            ],
            "input_types": ["documents", "code_files", "metadata"],
            "output_types": ["index_updates", "knowledge_graph"]
        }
    }

    return capabilities.get(specialist, {
        "description": "Unknown specialist",
        "capabilities": [],
        "input_types": [],
        "output_types": []
    })