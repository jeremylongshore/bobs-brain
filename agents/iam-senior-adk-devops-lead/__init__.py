"""
iam-senior-adk-devops-lead - ADK Department Foreman Agent

This agent orchestrates the iam-* specialist team within the ADK/Agent Engineering Department.
It receives high-level requests from Bob and delegates to specialized worker agents.
"""

from .agent import get_agent, create_runner

__all__ = ["get_agent", "create_runner"]
__version__ = "0.1.0"