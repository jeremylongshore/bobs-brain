"""
A2A Protocol AgentCard for iam-senior-adk-devops-lead.

This module provides the AgentCard configuration for agent-to-agent
communication, enabling Bob to discover and invoke the foreman.
"""

from a2a.types import AgentCard
import os

APP_NAME = os.getenv("APP_NAME", "iam-senior-adk-devops-lead")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
PUBLIC_URL = os.getenv(
    "FOREMAN_A2A_URL",
    "https://iam-senior-adk-devops-lead.run.app"
)
AGENT_SPIFFE_ID = os.getenv(
    "AGENT_SPIFFE_ID",
    "spiffe://intent.solutions/agent/iam-senior-adk-devops-lead/dev/us-central1/0.1.0"
)


def get_agent_card() -> AgentCard:
    """
    Get the AgentCard for the foreman agent.

    Returns the A2A protocol AgentCard that describes this agent's
    capabilities for discovery and invocation by other agents.

    Returns:
        AgentCard with foreman's metadata and skills
    """
    return AgentCard(
        name=APP_NAME,
        description=f"ADK Department Foreman - Orchestrates iam-* specialist agents for the ADK/Agent Engineering team. (SPIFFE: {AGENT_SPIFFE_ID})",
        url=PUBLIC_URL,
        version=APP_VERSION,
        skills=[
            # Core orchestration skills
            "task_planning",
            "specialist_delegation",
            "workflow_coordination",
            "result_aggregation",

            # Analysis skills
            "repository_analysis",
            "compliance_checking",
            "pattern_validation",

            # Management skills
            "quality_control",
            "progress_tracking",
            "issue_escalation"
        ]
    )