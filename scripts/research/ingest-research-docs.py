#!/usr/bin/env python3
"""
Ingest Jeremy's research documents into ChromaDB for semantic search.

This script:
1. Reads all markdown files from ~/research/
2. Creates vector embeddings using LlamaIndex
3. Stores in ChromaDB collection 'jeremy_research'
4. Enables semantic search via knowledge orchestrator

Usage:
    python scripts/research/ingest-research-docs.py
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def ingest_research_docs():
    """Ingest all research markdown files into ChromaDB"""

    try:
        import chromadb
        from llama_index.core import Document, StorageContext, VectorStoreIndex
        from llama_index.vector_stores.chroma import ChromaVectorStore
    except ImportError as e:
        logger.error(
            f"Missing dependencies: {e}\n"
            "Install with: pip install llama-index chromadb"
        )
        return False

    # Research directory
    research_dir = Path.home() / "research"
    if not research_dir.exists():
        logger.error(f"Research directory not found: {research_dir}")
        return False

    # Find all markdown files
    md_files = list(research_dir.glob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]  # Skip README

    if not md_files:
        logger.warning("No markdown files found in ~/research/")
        return False

    logger.info(f"Found {len(md_files)} research documents")

    # Initialize ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(path=".chroma")

        # Delete existing collection if it exists (for fresh start)
        try:
            chroma_client.delete_collection("jeremy_research")
            logger.info("Deleted existing jeremy_research collection")
        except Exception:
            pass  # Collection doesn't exist, that's fine

        # Create new collection
        chroma_collection = chroma_client.create_collection(
            name="jeremy_research",
            metadata={"description": "Jeremy's AI research papers and strategic analysis"},
        )
        logger.info("✅ Created jeremy_research collection")

    except Exception as e:
        logger.error(f"ChromaDB initialization failed: {e}")
        return False

    # Convert markdown files to LlamaIndex Documents
    documents = []
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")

            # Extract title (first line if starts with #)
            lines = content.split("\n")
            title = md_file.stem  # Default to filename
            if lines and lines[0].startswith("#"):
                title = lines[0].lstrip("#").strip()

            # Create LlamaIndex Document
            doc = Document(
                text=content,
                metadata={
                    "title": title,
                    "file_name": md_file.name,
                    "file_path": str(md_file),
                    "size_kb": md_file.stat().st_size / 1024,
                },
                doc_id=md_file.stem,  # Use filename as ID
            )

            documents.append(doc)
            logger.info(f"  ✓ {md_file.name} ({doc.metadata['size_kb']:.1f} KB)")

        except Exception as e:
            logger.warning(f"  ✗ Failed to process {md_file.name}: {e}")

    if not documents:
        logger.error("No documents successfully processed")
        return False

    logger.info(f"\n📄 Processing {len(documents)} documents...")

    # Create vector store and index
    try:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # Create index (this generates embeddings and stores them)
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True,  # Show progress bar
        )

        logger.info("✅ Vector embeddings generated and stored")

    except Exception as e:
        logger.error(f"Indexing failed: {e}")
        return False

    # Verify collection
    try:
        count = chroma_collection.count()
        logger.info(f"\n✅ SUCCESS! Indexed {count} documents in ChromaDB")
        logger.info(f"📊 Collection: jeremy_research")
        logger.info(f"📁 Location: .chroma/")
        logger.info(f"\n🔍 Test semantic search:")
        logger.info(f"   from src.knowledge_orchestrator import get_knowledge_orchestrator")
        logger.info(f"   ko = get_knowledge_orchestrator()")
        logger.info(f'   result = ko.query("LLM gateway patterns", mode="research")')
        logger.info(f"   print(result['answer'])")

        return True

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        return False


if __name__ == "__main__":
    success = ingest_research_docs()
    sys.exit(0 if success else 1)
