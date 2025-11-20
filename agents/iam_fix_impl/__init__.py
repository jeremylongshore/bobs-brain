"""
iam-fix-impl - Implementation Specialist Agent

This module exports the iam-fix-impl agent interface.
"""

from .agent import get_agent, create_runner, root_agent

__all__ = ["get_agent", "create_runner", "root_agent"]
