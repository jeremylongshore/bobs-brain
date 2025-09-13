"""
Bob's Brain - Unified AI Business Partner

Professional AI agent for DiagnosticPro.io and business operations.
"""

__version__ = "2.0.0"
__author__ = "Jeremy Longshore"
__description__ = "Unified AI business partner for DiagnosticPro.io"

from .agents.unified_v2 import BobUnifiedV2
from .agents.basic import BobBasic

__all__ = ['BobUnifiedV2', 'BobBasic']