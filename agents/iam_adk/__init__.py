"""
iam-adk - ADK/Vertex Design & Static Analysis Specialist

This agent specializes in ADK pattern analysis, A2A compliance checking,
and producing structured audit reports and issue specifications.

Enforces R1 (ADK only), R2 (Agent Engine runtime), R5 (dual memory).
"""

from .agent import get_agent, create_runner, auto_save_session_to_memory, root_agent

__all__ = [
    "get_agent",
    "create_runner",
    "auto_save_session_to_memory",
    "root_agent",  # Required by ADK CLI for Agent Engine deployment
]
