"""
Bob's Brain - ADK Agent Implementation

This module contains the core agent implementation using Google ADK
with dual memory wiring (Session + Memory Bank).

Enforces R1 (ADK only), R2 (Agent Engine runtime), R5 (dual memory).
"""

from my_agent.agent import get_agent, create_runner, auto_save_session_to_memory
from my_agent.a2a_card import get_agent_card

__all__ = [
    "get_agent",
    "create_runner",
    "auto_save_session_to_memory",
    "get_agent_card",
]
