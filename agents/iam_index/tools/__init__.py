"""
Indexing and Knowledge Management Tools for iam-index agent.
"""

from .indexing_tools import (
    index_adk_docs,
    index_project_docs,
    query_knowledge_base,
    sync_vertex_search,
    generate_index_entry,
    analyze_knowledge_gaps
)

__all__ = [
    "index_adk_docs",
    "index_project_docs",
    "query_knowledge_base",
    "sync_vertex_search",
    "generate_index_entry",
    "analyze_knowledge_gaps"
]