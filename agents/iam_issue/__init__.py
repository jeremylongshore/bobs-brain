"""
iam-issue - Issue Author & Formatter Specialist

This agent specializes in formatting and creating high-quality GitHub issues
from findings, audit reports, and other structured inputs.

Enforces R1 (ADK only), R2 (Agent Engine runtime), R5 (dual memory).
"""

from .agent import get_agent, create_runner, auto_save_session_to_memory, root_agent

__all__ = [
    "get_agent",
    "create_runner",
    "auto_save_session_to_memory",
    "root_agent",  # Required by ADK CLI for Agent Engine deployment
]
