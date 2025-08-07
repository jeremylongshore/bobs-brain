#!/usr/bin/env python3
"""
Enhanced Bob's Firestore tools with proper search and duplicate detection
"""

from google.cloud import firestore
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import hashlib
import time

class EnhancedBobTools:
    """Bob's enhanced tools with duplicate detection and better search"""

    def __init__(self):
        self.firestore_client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def search_knowledge(self, query: str, limit: int = 5) -> str:
        """Enhanced search with better text matching"""
        try:
            print(f"🔍 Searching for: '{query}'")
            docs = list(self.firestore_client.collection("knowledge").stream())
            print(f"📚 Scanning {len(docs)} documents...")

            results = []
            for doc in docs:
                data = doc.to_dict()
                content = data.get("content", "")
                metadata = data.get("metadata", {})

                # Enhanced search: check content and metadata
                search_targets = [
                    content.lower(),
                    str(metadata.get("title", "")).lower(),
                    str(metadata.get("category", "")).lower()
                ]

                query_lower = query.lower()
                match_found = False

                for target in search_targets:
                    if query_lower in target:
                        match_found = True
                        break

                if match_found:
                    title = metadata.get("title", "Untitled")
                    source = metadata.get("source", "unknown")
                    snippet = content[:200] + "..." if len(content) > 200 else content

                    result = f"**{title}** ({source})\n{snippet}"
                    results.append(result)

                    if len(results) >= limit:
                        break

            if results:
                return f"Found {len(results)} results for '{query}':\n\n" + "\n\n---\n\n".join(results)
            else:
                return f"No results found for '{query}'"

        except Exception as e:
            return f"Error searching knowledge: {str(e)}"

    def check_duplicate(self, content: str) -> dict:
        """Check if content already exists in knowledge base"""
        try:
            # Generate content hash
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()

            # Check all existing documents
            docs = list(self.firestore_client.collection("knowledge").stream())

            for doc in docs:
                data = doc.to_dict()
                existing_content = data.get("content", "")
                existing_hash = hashlib.sha256(existing_content.encode('utf-8')).hexdigest()

                # Exact hash match
                if content_hash == existing_hash:
                    return {
                        "is_duplicate": True,
                        "match_type": "exact",
                        "existing_doc_id": doc.id,
                        "confidence": 1.0
                    }

                # High similarity check (90%+ same content)
                similarity = self._calculate_similarity(content, existing_content)
                if similarity > 0.9:
                    return {
                        "is_duplicate": True,
                        "match_type": "high_similarity",
                        "existing_doc_id": doc.id,
                        "confidence": similarity
                    }

            return {"is_duplicate": False}

        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return {"is_duplicate": False, "error": str(e)}

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        try:
            # Simple word-based similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())

            if not words1 and not words2:
                return 1.0
            if not words1 or not words2:
                return 0.0

            intersection = words1.intersection(words2)
            union = words1.union(words2)

            return len(intersection) / len(union)

        except Exception:
            return 0.0

    def add_knowledge_with_duplicate_check(self, content: str, metadata: dict = None) -> dict:
        """Add knowledge item with automatic duplicate detection"""
        try:
            # Check for duplicates
            duplicate_check = self.check_duplicate(content)

            if duplicate_check["is_duplicate"]:
                return {
                    "success": False,
                    "reason": "duplicate_detected",
                    "details": duplicate_check
                }

            # Generate embedding
            embedding = self.embedding_model.encode(content).tolist()

            # Prepare document
            doc_data = {
                'content': content,
                'embedding': embedding,
                'metadata': metadata or {},
                'timestamp': firestore.SERVER_TIMESTAMP,
                'added_at': time.time(),
                'content_hash': hashlib.sha256(content.encode('utf-8')).hexdigest()
            }

            # Add to Firestore
            doc_ref = self.firestore_client.collection('knowledge').document()
            doc_ref.set(doc_data)

            return {
                "success": True,
                "doc_id": doc_ref.id,
                "content_length": len(content)
            }

        except Exception as e:
            return {
                "success": False,
                "reason": "error",
                "details": str(e)
            }

def test_enhanced_search():
    """Test the enhanced search capabilities"""
    print("🧪 TESTING ENHANCED BOB SEARCH")
    print("=" * 40)

    tools = EnhancedBobTools()

    test_queries = [
        "Firestore",
        "970 knowledge items",
        "migration project",
        "Alice integration",
        "data correction"
    ]

    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        result = tools.search_knowledge(query, limit=2)
        if "Found" in result:
            print("✅ SUCCESS")
        else:
            print("❌ NO RESULTS")
        print("-" * 30)

if __name__ == "__main__":
    test_enhanced_search()
