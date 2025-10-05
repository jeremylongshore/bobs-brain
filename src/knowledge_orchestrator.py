"""
LlamaIndex-powered Knowledge Orchestrator for Bob's Brain

Integrates multiple knowledge sources:
1. Research docs (ChromaDB vector store)
2. Knowledge DB (653MB SQLite with FTS)
3. Analytics DB (cost tracking)
4. Circle of Life learnings (Neo4j - optional)

GitHub: https://github.com/run-llama/llama_index
Docs: https://docs.llamaindex.ai/
"""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class BobKnowledgeOrchestrator:
    """
    Multi-source knowledge orchestration using LlamaIndex.

    Automatically routes queries to optimal knowledge source(s):
    - Simple keyword queries → Knowledge DB (FTS)
    - Conceptual queries → Research docs (semantic search)
    - Cost/performance queries → Analytics DB
    """

    def __init__(self):
        """Initialize all knowledge sources and create composable graph"""
        self.initialized = False
        self.research_index = None
        self.knowledge_index = None
        self.analytics_index = None
        self.graph = None

        try:
            self._init_llamaindex()
        except ImportError as e:
            logger.warning(
                f"LlamaIndex not installed: {e}. "
                "Install with: pip install llama-index chromadb sqlalchemy"
            )
        except Exception as e:
            logger.error(f"Failed to initialize knowledge orchestrator: {e}")

    def _init_llamaindex(self):
        """Initialize LlamaIndex components"""
        from llama_index.core import (
            ServiceContext,
            StorageContext,
            VectorStoreIndex,
            set_global_service_context,
        )
        from llama_index.core.indices.struct_store import SQLStructStoreIndex
        from llama_index.core.schema import TextNode
        from llama_index.llms.openai import OpenAI
        from llama_index.vector_stores.chroma import ChromaVectorStore

        try:
            import chromadb
        except ImportError:
            logger.warning("ChromaDB not installed. Vector search unavailable.")
            return

        # 1. Setup service context (LLM for query understanding)
        llm = OpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512)
        set_global_service_context(service_context)

        # 2. Research docs (ChromaDB vector store)
        self._init_research_index()

        # 3. Knowledge DB (653MB SQLite with FTS)
        self._init_knowledge_db()

        # 4. Analytics DB (cost tracking)
        self._init_analytics_db()

        # 5. Create composable graph (optional - combines all sources)
        # Uncomment when ready to use multi-source querying
        # self._init_graph()

        self.initialized = True
        logger.info("✅ Knowledge orchestrator initialized successfully")

    def _init_research_index(self):
        """Initialize research docs vector index"""
        try:
            import chromadb
            from llama_index.core import StorageContext, VectorStoreIndex
            from llama_index.vector_stores.chroma import ChromaVectorStore

            # Connect to existing ChromaDB
            chroma_client = chromadb.PersistentClient(path=".chroma")

            try:
                chroma_collection = chroma_client.get_collection("jeremy_research")
                logger.info("✅ Connected to existing jeremy_research collection")
            except Exception:
                # Collection doesn't exist yet - create it
                chroma_collection = chroma_client.create_collection("jeremy_research")
                logger.info("📝 Created new jeremy_research collection")
                # Need to run ingestion script to populate it
                logger.warning(
                    "Run scripts/research/ingest-research-docs.py to populate collection"
                )

            # Create vector store index
            vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)

            self.research_index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )

            logger.info("✅ Research index initialized")

        except Exception as e:
            logger.warning(f"Research index initialization failed: {e}")
            self.research_index = None

    def _init_knowledge_db(self):
        """Initialize knowledge DB (653MB SQLite)"""
        try:
            from llama_index.core import SQLDatabase
            from llama_index.core.indices.struct_store import SQLStructStoreIndex

            knowledge_db_path = Path.home() / "analytics" / "knowledge-base" / "knowledge.db"

            if not knowledge_db_path.exists():
                logger.warning(f"Knowledge DB not found at {knowledge_db_path}")
                self.knowledge_index = None
                return

            # Connect to existing database
            sql_database = SQLDatabase.from_uri(f"sqlite:///{knowledge_db_path}")

            # Create index (doesn't duplicate data, just creates query interface)
            self.knowledge_index = SQLStructStoreIndex.from_documents(
                [], sql_database=sql_database  # Empty list - DB already populated
            )

            logger.info(f"✅ Knowledge DB initialized ({knowledge_db_path})")

        except Exception as e:
            logger.warning(f"Knowledge DB initialization failed: {e}")
            self.knowledge_index = None

    def _init_analytics_db(self):
        """Initialize analytics DB (API usage tracking)"""
        try:
            from llama_index.core import SQLDatabase
            from llama_index.core.indices.struct_store import SQLStructStoreIndex

            analytics_db_path = Path.home() / "analytics" / "databases" / "api_usage_tracking.db"

            if not analytics_db_path.exists():
                logger.warning(f"Analytics DB not found at {analytics_db_path}")
                self.analytics_index = None
                return

            sql_database = SQLDatabase.from_uri(f"sqlite:///{analytics_db_path}")

            self.analytics_index = SQLStructStoreIndex.from_documents(
                [], sql_database=sql_database
            )

            logger.info(f"✅ Analytics DB initialized ({analytics_db_path})")

        except Exception as e:
            logger.warning(f"Analytics DB initialization failed: {e}")
            self.analytics_index = None

    def _init_graph(self):
        """Initialize composable graph (combines all sources)"""
        try:
            from llama_index.core import ComposableGraph

            # Only create graph if we have at least one index
            available_indices = [
                idx for idx in [self.research_index, self.knowledge_index, self.analytics_index] if idx
            ]

            if not available_indices:
                logger.warning("No indices available for graph creation")
                return

            # Create index summaries for routing
            summaries = []
            if self.research_index:
                summaries.append("Jeremy's strategic research papers on AI, LLMs, architecture")
            if self.knowledge_index:
                summaries.append("Large document corpus (653MB) with technical knowledge and FTS")
            if self.analytics_index:
                summaries.append("API usage, cost tracking, and performance analytics")

            # Composable graph routes queries to best source(s)
            self.graph = ComposableGraph.from_indices(
                root_index=available_indices[0],
                children_indices=available_indices[1:] if len(available_indices) > 1 else [],
                index_summaries=summaries,
            )

            logger.info("✅ Composable graph initialized (multi-source routing enabled)")

        except Exception as e:
            logger.warning(f"Graph initialization failed: {e}")
            self.graph = None

    def query(self, question: str, mode: str = "auto") -> Dict[str, Any]:
        """
        Query all knowledge sources intelligently.

        Args:
            question: User's question
            mode: Query mode
                - "auto": Automatic routing to best source(s)
                - "research": Only research docs
                - "knowledge": Only knowledge DB
                - "analytics": Only analytics DB
                - "all": Query all sources and combine

        Returns:
            Dict with answer, sources used, metadata
        """
        if not self.initialized:
            return {
                "answer": "Knowledge orchestrator not initialized. Install llama-index.",
                "sources": [],
                "error": "not_initialized",
            }

        try:
            if mode == "research" and self.research_index:
                return self._query_research(question)
            elif mode == "knowledge" and self.knowledge_index:
                return self._query_knowledge_db(question)
            elif mode == "analytics" and self.analytics_index:
                return self._query_analytics_db(question)
            elif mode == "all":
                return self._query_all(question)
            else:  # auto mode
                return self._query_auto(question)

        except Exception as e:
            logger.error(f"Query failed: {e}")
            return {"answer": f"Query error: {e}", "sources": [], "error": str(e)}

    def _query_research(self, question: str) -> Dict[str, Any]:
        """Query research docs only"""
        query_engine = self.research_index.as_query_engine(similarity_top_k=5)
        response = query_engine.query(question)

        return {
            "answer": response.response,
            "sources": [
                {"source": "research", "score": node.score, "text": node.node.text[:200]}
                for node in response.source_nodes
            ],
            "mode": "research",
        }

    def _query_knowledge_db(self, question: str) -> Dict[str, Any]:
        """Query 653MB knowledge DB"""
        query_engine = self.knowledge_index.as_query_engine()
        response = query_engine.query(question)

        return {
            "answer": response.response,
            "sources": [{"source": "knowledge_db", "text": response.response[:200]}],
            "mode": "knowledge",
        }

    def _query_analytics_db(self, question: str) -> Dict[str, Any]:
        """Query analytics/cost tracking DB"""
        query_engine = self.analytics_index.as_query_engine()
        response = query_engine.query(question)

        return {
            "answer": response.response,
            "sources": [{"source": "analytics", "text": response.response[:200]}],
            "mode": "analytics",
        }

    def _query_auto(self, question: str) -> Dict[str, Any]:
        """Automatic routing to best source"""
        # Simple heuristic routing (can be replaced with LLM-based routing)
        q_lower = question.lower()

        # Analytics-related keywords
        if any(word in q_lower for word in ["cost", "price", "api", "usage", "expensive"]):
            if self.analytics_index:
                return self._query_analytics_db(question)

        # Research-related keywords
        if any(
            word in q_lower
            for word in [
                "research",
                "paper",
                "architecture",
                "strategy",
                "gateway",
                "multi-agent",
            ]
        ):
            if self.research_index:
                return self._query_research(question)

        # Default: knowledge DB (largest corpus)
        if self.knowledge_index:
            return self._query_knowledge_db(question)

        # Fallback: research if available
        if self.research_index:
            return self._query_research(question)

        return {
            "answer": "No knowledge sources available",
            "sources": [],
            "error": "no_sources",
        }

    def _query_all(self, question: str) -> Dict[str, Any]:
        """Query all available sources and combine results"""
        results = []

        if self.research_index:
            results.append(self._query_research(question))

        if self.knowledge_index:
            results.append(self._query_knowledge_db(question))

        if self.analytics_index:
            results.append(self._query_analytics_db(question))

        # Combine all answers
        combined_answer = "\n\n".join(
            [f"**From {r['mode']}:** {r['answer']}" for r in results if r.get("answer")]
        )

        all_sources = []
        for r in results:
            all_sources.extend(r.get("sources", []))

        return {"answer": combined_answer, "sources": all_sources, "mode": "all", "count": len(results)}

    def get_status(self) -> Dict[str, Any]:
        """Get status of all knowledge sources"""
        return {
            "initialized": self.initialized,
            "research_index": self.research_index is not None,
            "knowledge_index": self.knowledge_index is not None,
            "analytics_index": self.analytics_index is not None,
            "graph": self.graph is not None,
        }


# Global instance (singleton)
_orchestrator = None


def get_knowledge_orchestrator() -> BobKnowledgeOrchestrator:
    """Get or create global knowledge orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = BobKnowledgeOrchestrator()
    return _orchestrator
