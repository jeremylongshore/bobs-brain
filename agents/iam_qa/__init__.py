"""
iam-qa Testing & Quality Assurance Specialist Agent

This module exports the iam-qa agent and its public interface.

The iam-qa agent is responsible for:
- Designing comprehensive test suites
- Validating test coverage against quality standards
- Running smoke tests and assessments
- Producing QAVerdict verdicts for deployment decisions
- Blocking deployment when quality standards are not met
"""

from .agent import get_agent, create_runner, root_agent

__all__ = [
    "get_agent",
    "create_runner",
    "root_agent",
]

__version__ = "0.8.0"
__name__ = "iam_qa"
