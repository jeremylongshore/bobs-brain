"""
iam-cleanup Repository Hygiene and Cleanup Specialist Agent

This module exports the iam-cleanup agent and its public interface.

The iam-cleanup agent is responsible for:
- Detecting dead code, unused dependencies, and orphaned files
- Identifying naming inconsistencies and structural issues
- Finding code duplication and optimization opportunities
- Proposing cleanup tasks with thorough safety assessments
- Blocking deployment-blocking cleanup work
"""

from .agent import get_agent, create_runner, root_agent

__all__ = [
    "get_agent",
    "create_runner",
    "root_agent",
]

__version__ = "0.8.0"
__name__ = "iam_cleanup"
