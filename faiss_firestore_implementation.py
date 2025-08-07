#!/usr/bin/env python3
"""
FAISS + Firestore Hybrid Implementation for Bob's Brain
High-performance vector search with cloud persistence
"""

import faiss
import numpy as np
import pickle
import json
import os
from datetime import datetime
from google.cloud import firestore
from typing import List, Dict, Tuple, Optional
import hashlib

class FaissFirestoreBrain:
    """Hybrid vector search: FAISS for speed + Firestore for persistence"""

    def __init__(self, firestore_project: str = "bobs-house-ai"):
        self.firestore_client = firestore.Client(project=firestore_project)
        self.index = None
        self.id_mapping = {}  # FAISS index -> Firestore doc_id
        self.reverse_mapping = {}  # doc_id -> FAISS index
        self.index_cache_path = "/tmp/bob_faiss_index.pkl"
        self.metadata_cache_path = "/tmp/bob_metadata.json"

        # Performance metrics
        self.index_build_time = 0
        self.last_sync_time = None

    def initialize_index(self, force_rebuild: bool = False):
        """Initialize FAISS index with caching mechanism"""
        print("🧠 Initializing Bob's FAISS+Firestore Brain...")

        if not force_rebuild and self._load_cached_index():
            print("✅ Loaded cached FAISS index")
            return

        print("🔄 Building FAISS index from Firestore...")
        start_time = datetime.now()

        # Fetch all knowledge items from Firestore
        knowledge_docs = self.firestore_client.collection('bob_knowledge').get()

        if not knowledge_docs:
            print("⚠️  No knowledge items in Firestore - creating empty index")
            self.index = faiss.IndexFlatIP(384)  # Inner product for similarity
            return

        # Extract embeddings and build mapping
        embeddings = []
        doc_ids = []

        for i, doc in enumerate(knowledge_docs):
            doc_data = doc.to_dict()
            if 'embedding' in doc_data:
                embeddings.append(doc_data['embedding'])
                doc_ids.append(doc.id)
                self.id_mapping[i] = doc.id
                self.reverse_mapping[doc.id] = i

        if not embeddings:
            print("⚠️  No embeddings found - check data migration")
            self.index = faiss.IndexFlatIP(384)
            return

        # Build FAISS index
        embeddings_array = np.array(embeddings, dtype=np.float32)
        self.index = faiss.IndexFlatIP(embeddings_array.shape[1])
        self.index.add(embeddings_array)

        self.index_build_time = (datetime.now() - start_time).total_seconds()
        self.last_sync_time = datetime.now()

        print(f"✅ FAISS index built: {len(embeddings)} vectors in {self.index_build_time:.2f}s")

        # Cache for next startup
        self._cache_index()

    def _load_cached_index(self) -> bool:
        """Load FAISS index from cache if available and valid"""
        try:
            if not os.path.exists(self.index_cache_path) or not os.path.exists(self.metadata_cache_path):
                return False

            # Check cache freshness (rebuild if older than 1 hour)
            cache_age = datetime.now().timestamp() - os.path.getmtime(self.index_cache_path)
            if cache_age > 3600:  # 1 hour
                print("⏰ FAISS cache expired, rebuilding...")
                return False

            # Load index
            self.index = faiss.read_index(self.index_cache_path)

            # Load metadata
            with open(self.metadata_cache_path, 'r') as f:
                metadata = json.load(f)
                self.id_mapping = metadata['id_mapping']
                self.reverse_mapping = metadata['reverse_mapping']
                self.last_sync_time = datetime.fromisoformat(metadata['last_sync_time'])

            return True

        except Exception as e:
            print(f"❌ Failed to load FAISS cache: {e}")
            return False

    def _cache_index(self):
        """Cache FAISS index and metadata for next startup"""
        try:
            # Save FAISS index
            faiss.write_index(self.index, self.index_cache_path)

            # Save metadata
            metadata = {
                'id_mapping': {str(k): v for k, v in self.id_mapping.items()},
                'reverse_mapping': self.reverse_mapping,
                'last_sync_time': self.last_sync_time.isoformat(),
                'index_size': self.index.ntotal
            }

            with open(self.metadata_cache_path, 'w') as f:
                json.dump(metadata, f)

            print(f"💾 FAISS index cached ({self.index.ntotal} vectors)")

        except Exception as e:
            print(f"⚠️  Failed to cache FAISS index: {e}")

    def search_knowledge(self, query_vector: List[float], k: int = 5) -> List[Dict]:
        """Perform hybrid search: FAISS + Firestore retrieval"""
        if not self.index or self.index.ntotal == 0:
            print("⚠️  FAISS index empty")
            return []

        # FAISS similarity search
        query_array = np.array([query_vector], dtype=np.float32)
        scores, indices = self.index.search(query_array, k)

        # Retrieve full documents from Firestore
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for insufficient results
                continue

            doc_id = self.id_mapping.get(idx)
            if doc_id:
                doc_ref = self.firestore_client.collection('bob_knowledge').document(doc_id)
                doc = doc_ref.get()
                if doc.exists:
                    data = doc.to_dict()
                    data['similarity_score'] = float(score)
                    data['doc_id'] = doc_id
                    results.append(data)

        return results

    def add_knowledge_item(self, content: str, embedding: List[float],
                          metadata: Dict = None) -> str:
        """Add new knowledge item to both FAISS and Firestore"""

        # Add to Firestore
        doc_data = {
            'content': content,
            'embedding': embedding,
            'metadata': metadata or {},
            'created_at': firestore.SERVER_TIMESTAMP,
            'source': 'bob_agent'
        }

        doc_ref = self.firestore_client.collection('bob_knowledge').add(doc_data)[1]
        doc_id = doc_ref.id

        # Add to FAISS index
        if self.index:
            embedding_array = np.array([embedding], dtype=np.float32)
            new_index = self.index.ntotal
            self.index.add(embedding_array)

            # Update mappings
            self.id_mapping[new_index] = doc_id
            self.reverse_mapping[doc_id] = new_index

            # Update cache
            self._cache_index()

        print(f"✅ Added knowledge item: {doc_id}")
        return doc_id

    def sync_with_firestore(self):
        """Incremental sync with Firestore (check for new items)"""
        if not self.last_sync_time:
            return self.initialize_index(force_rebuild=True)

        # Query for items added since last sync
        new_docs = (self.firestore_client.collection('bob_knowledge')
                   .where('created_at', '>', self.last_sync_time)
                   .get())

        if not new_docs:
            print("🔄 No new knowledge items to sync")
            return

        print(f"🔄 Syncing {len(new_docs)} new knowledge items...")

        # Add new items to FAISS
        for doc in new_docs:
            doc_data = doc.to_dict()
            if 'embedding' in doc_data:
                embedding_array = np.array([doc_data['embedding']], dtype=np.float32)
                new_index = self.index.ntotal
                self.index.add(embedding_array)

                self.id_mapping[new_index] = doc.id
                self.reverse_mapping[doc.id] = new_index

        self.last_sync_time = datetime.now()
        self._cache_index()
        print(f"✅ Synced {len(new_docs)} items")

    def get_index_stats(self) -> Dict:
        """Get performance and size statistics"""
        return {
            'total_vectors': self.index.ntotal if self.index else 0,
            'index_build_time': self.index_build_time,
            'last_sync_time': self.last_sync_time.isoformat() if self.last_sync_time else None,
            'cache_exists': os.path.exists(self.index_cache_path),
            'memory_usage_mb': self.index.ntotal * 384 * 4 / (1024*1024) if self.index else 0
        }


class BobAliceCommunication:
    """Structured communication between Bob and Alice via Firestore"""

    def __init__(self, firestore_project: str = "bobs-house-ai"):
        self.firestore_client = firestore.Client(project=firestore_project)

    def create_task_for_alice(self, task_type: str, description: str,
                             priority: str = "medium", metadata: Dict = None) -> str:
        """Bob creates task for Alice"""

        task_doc = {
            'agent_from': 'bob',
            'agent_to': 'alice',
            'task_type': task_type,  # 'gcp_operation', 'cloud_deployment', 'monitoring'
            'description': description,
            'priority': priority,  # 'low', 'medium', 'high', 'urgent'
            'status': 'pending',  # 'pending', 'in_progress', 'completed', 'failed'
            'metadata': metadata or {},
            'created_at': firestore.SERVER_TIMESTAMP,
            'updated_at': firestore.SERVER_TIMESTAMP,
            'attempts': 0,
            'max_attempts': 3
        }

        doc_ref = self.firestore_client.collection('shared_context').add(task_doc)[1]
        print(f"📤 Bob created task for Alice: {doc_ref.id}")
        return doc_ref.id

    def alice_claim_task(self, task_id: str) -> bool:
        """Alice claims pending task"""
        doc_ref = self.firestore_client.collection('shared_context').document(task_id)

        try:
            doc_ref.update({
                'status': 'in_progress',
                'alice_claimed_at': firestore.SERVER_TIMESTAMP,
                'attempts': firestore.Increment(1)
            })
            print(f"🤝 Alice claimed task: {task_id}")
            return True
        except Exception as e:
            print(f"❌ Alice failed to claim task {task_id}: {e}")
            return False

    def complete_task(self, task_id: str, result: Dict, success: bool = True):
        """Mark task as completed with results"""
        doc_ref = self.firestore_client.collection('shared_context').document(task_id)

        update_data = {
            'status': 'completed' if success else 'failed',
            'completed_at': firestore.SERVER_TIMESTAMP,
            'result': result,
            'updated_at': firestore.SERVER_TIMESTAMP
        }

        doc_ref.update(update_data)
        print(f"✅ Task completed: {task_id}")

    def get_pending_tasks_for_alice(self, limit: int = 10) -> List[Dict]:
        """Alice gets pending tasks"""
        docs = (self.firestore_client.collection('shared_context')
               .where('agent_to', '==', 'alice')
               .where('status', '==', 'pending')
               .order_by('priority')
               .order_by('created_at')
               .limit(limit)
               .get())

        return [{'id': doc.id, **doc.to_dict()} for doc in docs]


# Usage Example
if __name__ == "__main__":
    # Initialize Bob's hybrid brain
    brain = FaissFirestoreBrain()
    brain.initialize_index()

    # Example search (would use actual embedding from query)
    sample_query_vector = [0.1] * 384  # Replace with actual embedding
    results = brain.search_knowledge(sample_query_vector, k=3)

    print(f"🔍 Search results: {len(results)} items")
    for result in results:
        print(f"  - {result['content'][:80]}... (score: {result['similarity_score']:.3f})")

    # Bob-Alice communication example
    comm = BobAliceCommunication()
    task_id = comm.create_task_for_alice(
        task_type="gcp_monitoring",
        description="Check Cloud Run service health for bob-extended-brain",
        priority="medium",
        metadata={"service": "bob-extended-brain", "region": "us-central1"}
    )

    print(f"📊 FAISS Index Stats: {brain.get_index_stats()}")
