"""
Cleanup Tools Module

Exports cleanup detection and analysis tools for iam-cleanup agent.
"""

from .cleanup_tools import (
    detect_dead_code,
    detect_unused_dependencies,
    identify_naming_issues,
    find_code_duplication,
    analyze_structure,
    propose_cleanup_task,
)

__all__ = [
    "detect_dead_code",
    "detect_unused_dependencies",
    "identify_naming_issues",
    "find_code_duplication",
    "analyze_structure",
    "propose_cleanup_task",
]
