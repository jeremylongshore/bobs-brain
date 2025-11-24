"""
A2A (Agent-to-Agent) Protocol Implementation

This package provides infrastructure for agent-to-agent communication
following the AgentCard contract specifications.

Modules:
- types: Core data models (A2ATask, A2AResult)
- dispatcher: Agent invocation and skill orchestration

Follows:
- 6767-LAZY: No import-time validation or heavy work
- R7: SPIFFE ID propagation
- AgentCard contracts for skill validation
"""

from .types import A2ATask, A2AResult, A2AError
from .dispatcher import call_specialist, discover_specialists

__all__ = [
    "A2ATask",
    "A2AResult",
    "A2AError",
    "call_specialist",
    "discover_specialists",
]
