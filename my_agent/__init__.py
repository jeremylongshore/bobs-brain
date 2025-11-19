"""
Bob's Brain - ADK Agent Implementation

This module contains the core agent implementation using Google ADK
with dual memory wiring (Session + Memory Bank).

Enforces R1 (ADK only), R2 (Agent Engine runtime), R5 (dual memory).
"""

from .agent import get_agent, create_runner, auto_save_session_to_memory, root_agent

# NOTE: a2a_card import removed for Agent Engine deployment compatibility
# AgentCard is only needed by service/a2a_gateway/, not by the agent itself
# from .a2a_card import get_agent_card

__all__ = [
    "get_agent",
    "create_runner",
    "auto_save_session_to_memory",
    "root_agent",  # Required by ADK CLI for Agent Engine deployment
    # "get_agent_card",  # Only needed for gateway service
]
