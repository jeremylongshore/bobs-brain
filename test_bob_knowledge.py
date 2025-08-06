#!/usr/bin/env python3
"""
Test Bob's ReAct system and knowledge retrieval about DiagnosticPro
"""

import chromadb


def test_bob_knowledge():
    """Test Bob's knowledge about today's achievements"""

    print("🧠 Testing Bob's knowledge about DiagnosticPro breakthrough...")

    # Connect to Bob's brain
    client = chromadb.PersistentClient(path='/home/jeremylongshore/.bob_brain/chroma')
    collection = client.get_collection('bob_knowledge')

    # Test knowledge retrieval
    test_queries = [
        "DiagnosticPro breakthrough session",
        "OpenRouter GPT-4o Mini API",
        "tomorrow's priority DNS migration",
        "revenue ready business model"
    ]

    for query in test_queries:
        print(f"\n🔍 Testing query: '{query}'")

        try:
            results = collection.query(
                query_texts=[query],
                n_results=2
            )

            if results['documents'] and results['documents'][0]:
                doc = results['documents'][0][0]
                metadata = results['metadatas'][0][0] if results['metadatas'][0] else {}

                print(f"✅ Found knowledge (type: {metadata.get('type', 'unknown')})")
                print(f"📝 Content preview: {doc[:100]}...")

            else:
                print("❌ No knowledge found for this query")

        except Exception as e:
            print(f"⚠️ Error querying Bob's brain: {e}")

    # Check Bob's total knowledge
    total = collection.count()
    print(f"\n🧠 Bob's total knowledge items: {total}")

    return True


if __name__ == "__main__":
    test_bob_knowledge()
    print("\n✅ Bob's knowledge test complete!")
