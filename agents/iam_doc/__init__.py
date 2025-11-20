"""
iam-doc - Documentation Specialist Agent

This module exports the iam-doc agent and its runner.
"""

from .agent import get_agent, create_runner, root_agent

__all__ = ["get_agent", "create_runner", "root_agent"]
