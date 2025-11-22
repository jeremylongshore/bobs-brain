"""
iam-adk - ADK/Vertex Design & Static Analysis Specialist

This agent specializes in ADK pattern analysis, A2A compliance checking,
and producing structured audit reports and issue specifications.

Enforces R1 (ADK only), R2 (Agent Engine runtime), R5 (dual memory).

Phase 12 Update: Migrated to google-adk 1.18+ API (App pattern)
"""

from .agent import create_agent, create_runner, auto_save_session_to_memory, app

__all__ = [
    "create_agent",  # Phase 12: renamed from get_agent
    "create_runner",
    "auto_save_session_to_memory",
    "app",  # Phase 12: App pattern for Agent Engine (was root_agent)
]
