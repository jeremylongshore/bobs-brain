#!/usr/bin/env python3
"""
Complete FAISS + Firestore Implementation for Bob's Brain
Includes embedding generation, vector search, and cloud sync
"""

import faiss
import numpy as np
import pickle
import json
import os
import hashlib
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from google.cloud import firestore
from sentence_transformers import SentenceTransformer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingGenerator:
    """Handles text embedding generation using SentenceTransformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        Model options:
        - all-MiniLM-L6-v2: 384 dimensions, fast, good quality
        - all-mpnet-base-v2: 768 dimensions, slower, best quality
        - paraphrase-MiniLM-L3-v2: 384 dimensions, fastest
        """
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        logger.info(f"Embedding dimension: {self.embedding_dim}")

    def encode_text(self, text: str) -> List[float]:
        """Generate embedding for single text"""
        embedding = self.model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts (more efficient)"""
        embeddings = self.model.encode(texts, convert_to_tensor=False, batch_size=32)
        return embeddings.tolist()

    def get_dimension(self) -> int:
        """Get embedding dimension"""
        return self.embedding_dim


class CompleteFaissFirestoreBrain:
    """Complete hybrid vector search: FAISS for speed + Firestore for persistence"""

    def __init__(self, firestore_project: str = "bobs-house-ai",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        # Initialize components
        self.firestore_client = firestore.Client(project=firestore_project)
        self.embedding_generator = EmbeddingGenerator(embedding_model)

        # FAISS index and mappings
        self.index = None
        self.id_mapping = {}  # FAISS index -> Firestore doc_id
        self.reverse_mapping = {}  # doc_id -> FAISS index

        # Cache paths
        self.cache_dir = "/home/jeremylongshore/bobs_brain/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        self.index_cache_path = f"{self.cache_dir}/faiss_index.bin"
        self.metadata_cache_path = f"{self.cache_dir}/metadata.json"

        # Performance metrics
        self.stats = {
            'index_build_time': 0,
            'last_sync_time': None,
            'total_vectors': 0,
            'search_count': 0,
            'cache_hits': 0
        }

    def initialize_index(self, force_rebuild: bool = False) -> bool:
        """Initialize FAISS index with smart caching"""
        logger.info("🧠 Initializing Bob's FAISS+Firestore Brain...")

        if not force_rebuild and self._load_cached_index():
            logger.info("✅ Loaded cached FAISS index")
            return True

        logger.info("🔄 Building FAISS index from Firestore...")
        start_time = datetime.now()

        try:
            # Fetch all knowledge items from Firestore
            knowledge_docs = self.firestore_client.collection('bob_knowledge').stream()

            embeddings = []
            doc_ids = []
            doc_count = 0

            for doc in knowledge_docs:
                doc_data = doc.to_dict()
                if 'embedding' in doc_data and doc_data['embedding']:
                    embeddings.append(doc_data['embedding'])
                    doc_ids.append(doc.id)
                    self.id_mapping[doc_count] = doc.id
                    self.reverse_mapping[doc.id] = doc_count
                    doc_count += 1

            if not embeddings:
                logger.warning("⚠️  No embeddings found - creating empty index")
                self.index = faiss.IndexFlatIP(self.embedding_generator.get_dimension())
                return True

            # Build FAISS index
            embeddings_array = np.array(embeddings, dtype=np.float32)

            # Use IndexFlatIP for inner product similarity (cosine similarity for normalized vectors)
            self.index = faiss.IndexFlatIP(embeddings_array.shape[1])

            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings_array)
            self.index.add(embeddings_array)

            self.stats['index_build_time'] = (datetime.now() - start_time).total_seconds()
            self.stats['last_sync_time'] = datetime.now()
            self.stats['total_vectors'] = len(embeddings)

            logger.info(f"✅ FAISS index built: {len(embeddings)} vectors in {self.stats['index_build_time']:.2f}s")

            # Cache for next startup
            self._cache_index()
            return True

        except Exception as e:
            logger.error(f"❌ Failed to initialize FAISS index: {e}")
            return False

    def _load_cached_index(self) -> bool:
        """Load FAISS index from cache if available and valid"""
        try:
            if not os.path.exists(self.index_cache_path) or not os.path.exists(self.metadata_cache_path):
                return False

            # Check cache freshness (rebuild if older than 4 hours)
            cache_age = datetime.now().timestamp() - os.path.getmtime(self.index_cache_path)
            if cache_age > 14400:  # 4 hours
                logger.info("⏰ FAISS cache expired, rebuilding...")
                return False

            # Load index
            self.index = faiss.read_index(self.index_cache_path)

            # Load metadata
            with open(self.metadata_cache_path, 'r') as f:
                metadata = json.load(f)
                # Convert string keys back to integers
                self.id_mapping = {int(k): v for k, v in metadata['id_mapping'].items()}
                self.reverse_mapping = metadata['reverse_mapping']
                self.stats.update(metadata['stats'])
                if self.stats['last_sync_time']:
                    self.stats['last_sync_time'] = datetime.fromisoformat(self.stats['last_sync_time'])

            self.stats['cache_hits'] += 1
            return True

        except Exception as e:
            logger.error(f"❌ Failed to load FAISS cache: {e}")
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
                'stats': {
                    **self.stats,
                    'last_sync_time': self.stats['last_sync_time'].isoformat() if self.stats['last_sync_time'] else None
                },
                'cache_created': datetime.now().isoformat(),
                'embedding_model': self.embedding_generator.model.get_model_name()
            }

            with open(self.metadata_cache_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"💾 FAISS index cached ({self.index.ntotal} vectors)")

        except Exception as e:
            logger.warning(f"⚠️  Failed to cache FAISS index: {e}")

    def search_knowledge(self, query: str, k: int = 5, similarity_threshold: float = 0.1) -> List[Dict]:
        """
        Perform hybrid search: Generate embedding -> FAISS search -> Firestore retrieval

        Args:
            query: Text query
            k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)
        """
        if not self.index or self.index.ntotal == 0:
            logger.warning("⚠️  FAISS index empty")
            return []

        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.encode_text(query)
            query_array = np.array([query_embedding], dtype=np.float32)
            faiss.normalize_L2(query_array)  # Normalize for cosine similarity

            # FAISS similarity search
            scores, indices = self.index.search(query_array, k)

            # Filter by similarity threshold
            results = []
            batch_doc_ids = []

            for score, idx in zip(scores[0], indices[0]):
                if idx == -1 or score < similarity_threshold:  # FAISS returns -1 for insufficient results
                    continue

                doc_id = self.id_mapping.get(idx)
                if doc_id:
                    batch_doc_ids.append((doc_id, float(score)))

            # Batch retrieve from Firestore for efficiency
            if batch_doc_ids:
                for doc_id, score in batch_doc_ids:
                    try:
                        doc_ref = self.firestore_client.collection('bob_knowledge').document(doc_id)
                        doc = doc_ref.get()
                        if doc.exists:
                            data = doc.to_dict()
                            # Remove embedding from response to save bandwidth
                            if 'embedding' in data:
                                del data['embedding']
                            data.update({
                                'similarity_score': score,
                                'doc_id': doc_id,
                                'search_query': query
                            })
                            results.append(data)
                    except Exception as e:
                        logger.error(f"Error retrieving doc {doc_id}: {e}")

            self.stats['search_count'] += 1
            logger.info(f"🔍 Found {len(results)} results for: {query[:50]}...")
            return results

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            return []

    def add_knowledge_item(self, content: str, metadata: Dict = None,
                          category: str = "general", source: str = "user") -> Optional[str]:
        """Add new knowledge item to both FAISS and Firestore"""

        try:
            # Generate embedding
            embedding = self.embedding_generator.encode_text(content)

            # Prepare document
            doc_data = {
                'content': content,
                'embedding': embedding,
                'metadata': metadata or {},
                'category': category,
                'source': source,
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }

            # Add to Firestore
            doc_ref = self.firestore_client.collection('bob_knowledge').add(doc_data)[1]
            doc_id = doc_ref.id

            # Add to FAISS index
            if self.index:
                embedding_array = np.array([embedding], dtype=np.float32)
                faiss.normalize_L2(embedding_array)

                new_index = self.index.ntotal
                self.index.add(embedding_array)

                # Update mappings
                self.id_mapping[new_index] = doc_id
                self.reverse_mapping[doc_id] = new_index
                self.stats['total_vectors'] += 1

                # Update cache
                self._cache_index()

            logger.info(f"✅ Added knowledge item: {doc_id}")
            return doc_id

        except Exception as e:
            logger.error(f"❌ Failed to add knowledge item: {e}")
            return None

    def sync_with_firestore(self) -> bool:
        """Incremental sync with Firestore (check for new items)"""
        try:
            if not self.stats['last_sync_time']:
                return self.initialize_index(force_rebuild=True)

            # Query for items added since last sync
            new_docs = (self.firestore_client.collection('bob_knowledge')
                       .where('created_at', '>', self.stats['last_sync_time'])
                       .stream())

            new_items = list(new_docs)
            if not new_items:
                logger.info("🔄 No new knowledge items to sync")
                return True

            logger.info(f"🔄 Syncing {len(new_items)} new knowledge items...")

            # Add new items to FAISS
            new_embeddings = []
            for doc in new_items:
                doc_data = doc.to_dict()
                if 'embedding' in doc_data and doc_data['embedding']:
                    new_embeddings.append(doc_data['embedding'])
                    new_index = self.index.ntotal + len(new_embeddings) - 1
                    self.id_mapping[new_index] = doc.id
                    self.reverse_mapping[doc.id] = new_index

            if new_embeddings:
                embeddings_array = np.array(new_embeddings, dtype=np.float32)
                faiss.normalize_L2(embeddings_array)
                self.index.add(embeddings_array)
                self.stats['total_vectors'] += len(new_embeddings)

            self.stats['last_sync_time'] = datetime.now()
            self._cache_index()

            logger.info(f"✅ Synced {len(new_items)} items")
            return True

        except Exception as e:
            logger.error(f"❌ Sync failed: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        memory_usage_mb = 0
        if self.index and self.index.ntotal > 0:
            memory_usage_mb = self.index.ntotal * self.embedding_generator.get_dimension() * 4 / (1024*1024)

        return {
            'total_vectors': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.embedding_generator.get_dimension(),
            'embedding_model': self.embedding_generator.model.get_model_name(),
            'index_build_time_seconds': self.stats['index_build_time'],
            'last_sync_time': self.stats['last_sync_time'].isoformat() if self.stats['last_sync_time'] else None,
            'search_count': self.stats['search_count'],
            'cache_hits': self.stats['cache_hits'],
            'cache_exists': os.path.exists(self.index_cache_path),
            'memory_usage_mb': round(memory_usage_mb, 2),
            'firestore_collections': self._get_firestore_stats()
        }

    def _get_firestore_stats(self) -> Dict:
        """Get Firestore collection statistics"""
        try:
            collections = ['bob_knowledge', 'bob_conversations', 'shared_context']
            stats = {}

            for collection in collections:
                docs = list(self.firestore_client.collection(collection).limit(1).stream())
                # Rough count (Firestore doesn't support efficient counting)
                stats[collection] = "exists" if docs else "empty"

            return stats
        except Exception as e:
            return {"error": str(e)}


# Setup Instructions
"""
SETUP INSTRUCTIONS:

1. Install Dependencies:
   pip install sentence-transformers faiss-cpu google-cloud-firestore numpy

2. For GPU acceleration (optional):
   pip install faiss-gpu

3. Set up Google Cloud credentials:
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"

4. Initialize Firestore database:
   - Enable Firestore in Native mode in Google Cloud Console
   - Create collections: bob_knowledge, bob_conversations, shared_context

5. Usage:
   brain = CompleteFaissFirestoreBrain()
   brain.initialize_index()
   results = brain.search_knowledge("tell me about DiagnosticPro")
"""

# Example usage
if __name__ == "__main__":
    # Initialize Bob's complete brain
    brain = CompleteFaissFirestoreBrain()

    if brain.initialize_index():
        # Example search
        results = brain.search_knowledge("DiagnosticPro project status", k=3)

        print(f"🔍 Search Results ({len(results)} found):")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Score: {result['similarity_score']:.3f}")
            print(f"   Content: {result['content'][:100]}...")
            print(f"   Category: {result.get('category', 'unknown')}")

        # Show statistics
        stats = brain.get_stats()
        print(f"\n📊 Brain Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
    else:
        print("❌ Failed to initialize brain")
