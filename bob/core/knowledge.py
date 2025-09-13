"""
ChromaDB Knowledge Base Integration
"""

import chromadb
from pathlib import Path
from typing import List, Dict, Any, Optional
from .config import BobConfig


class KnowledgeBase:
    """ChromaDB knowledge base management"""
    
    def __init__(self, config: BobConfig):
        """Initialize knowledge base connection"""
        self.config = config
        self.chroma_client = chromadb.PersistentClient(
            path=config.chroma_persist_dir
        )
        self.knowledge_collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Get or create the bob_knowledge collection"""
        try:
            return self.chroma_client.get_collection('bob_knowledge')
        except Exception:
            return self.chroma_client.create_collection(
                name='bob_knowledge',
                metadata={"description": "Bob's knowledge base for DiagnosticPro.io"}
            )
    
    def query_knowledge(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query the knowledge base"""
        try:
            results = self.knowledge_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Knowledge query error: {e}")
            return []
    
    def add_knowledge(self, documents: List[str], metadata: List[Dict] = None, ids: List[str] = None):
        """Add knowledge to the database"""
        try:
            self.knowledge_collection.add(
                documents=documents,
                metadatas=metadata or [{}] * len(documents),
                ids=ids or [f"doc_{i}" for i in range(len(documents))]
            )
        except Exception as e:
            print(f"Knowledge addition error: {e}")
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get knowledge collection statistics"""
        try:
            count = self.knowledge_collection.count()
            return {"total_documents": count}
        except Exception:
            return {"total_documents": 0}