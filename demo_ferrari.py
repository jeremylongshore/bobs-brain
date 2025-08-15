#!/usr/bin/env python3
"""
Demo Bob Ferrari's Holistic Intelligence
Shows how all systems work together
"""

import json
from datetime import datetime

import chromadb
import google.generativeai as genai
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

print("=" * 80)
print("🏎️ BOB FERRARI DEMO - HOLISTIC INTELLIGENCE")
print("=" * 80)

# Initialize components
genai.configure(api_key="os.getenv("GEMINI_API_KEY")")
model = genai.GenerativeModel("gemini-1.5-flash")

neo4j_driver = GraphDatabase.driver(
    "neo4j+s://d3653283.databases.neo4j.io", auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
)

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("bob_ferrari_knowledge")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Test query
test_query = "My Bobcat T770 won't start and shows error P0340"

print(f"\n📝 USER QUERY: '{test_query}'")
print("-" * 80)

# 1. Search Neo4j for structured knowledge
print("\n1️⃣ SEARCHING NEO4J GRAPH DATABASE...")
neo4j_results = []
with neo4j_driver.session() as session:
    # First, let's add some test data if not exists
    session.run(
        """
        MERGE (e:Equipment {name: 'Bobcat T770'})
        MERGE (ec:ErrorCode {code: 'P0340', description: 'Camshaft Position Sensor Circuit Malfunction'})
        MERGE (p:Problem {description: 'Engine won\\'t start'})
        MERGE (s:Solution {description: 'Replace camshaft position sensor'})
        MERGE (s2:Solution {description: 'Check wiring harness for damage'})
        MERGE (s3:Solution {description: 'Verify timing belt alignment'})
        MERGE (e)-[:HAS_PROBLEM]->(p)
        MERGE (ec)-[:INDICATES]->(p)
        MERGE (p)-[:SOLVED_BY]->(s)
        MERGE (p)-[:SOLVED_BY]->(s2)
        MERGE (p)-[:SOLVED_BY]->(s3)
    """
    )

    # Now search
    result = session.run(
        """
        MATCH (e:Equipment {name: 'Bobcat T770'})-[:HAS_PROBLEM]->(p:Problem)
        OPTIONAL MATCH (ec:ErrorCode {code: 'P0340'})-[:INDICATES]->(p)
        OPTIONAL MATCH (p)-[:SOLVED_BY]->(s:Solution)
        RETURN e.name as equipment, p.description as problem,
               ec.code as error_code, ec.description as error_desc,
               collect(s.description) as solutions
    """
    )

    for record in result:
        print(f"   📊 Found: {record['equipment']} - {record['problem']}")
        if record["error_code"]:
            print(f"      Error: {record['error_code']} ({record['error_desc']})")
        if record["solutions"]:
            print(f"      Solutions:")
            for solution in record["solutions"]:
                print(f"         • {solution}")
        neo4j_results.append(record.data())

# 2. Search ChromaDB for similar problems
print("\n2️⃣ SEARCHING CHROMADB VECTOR DATABASE...")
query_embedding = embedder.encode([test_query])[0].tolist()

# Add some test knowledge if collection is empty
if collection.count() < 10:
    test_knowledge = [
        "Bobcat T770 engine cranks but won't start - Check fuel supply, glow plugs, and starter motor",
        "Error P0340 indicates camshaft sensor issues - Replace sensor and check timing",
        "No-start conditions often caused by sensor failures or fuel system problems",
        "Bobcat equipment requires regular sensor maintenance to prevent starting issues",
    ]
    for i, knowledge in enumerate(test_knowledge):
        embedding = embedder.encode([knowledge])[0].tolist()
        collection.add(documents=[knowledge], embeddings=[embedding], ids=[f"demo_{i}"])

results = collection.query(query_embeddings=[query_embedding], n_results=3, include=["documents", "distances"])

vector_results = []
if results["documents"] and results["documents"][0]:
    for i, doc in enumerate(results["documents"][0]):
        similarity = 1 - results["distances"][0][i]
        print(f"   🔍 Similar ({similarity:.2f}): {doc[:100]}...")
        vector_results.append({"content": doc, "similarity": similarity})

# 3. Extract entities from the query
print("\n3️⃣ EXTRACTING ENTITIES...")
extraction_prompt = f"""Extract entities from: {test_query}

Return JSON with:
{{"entities": [{{"name": "...", "type": "Equipment|ErrorCode|Problem"}}],
  "relationships": [{{"from": "...", "to": "...", "type": "..."}}]}}"""

extraction_response = model.generate_content(extraction_prompt)
entities = {"entities": [], "relationships": []}
if extraction_response and extraction_response.text:
    try:
        json_text = extraction_response.text
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0]
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0]
        entities = json.loads(json_text.strip())

        print("   🏷️ Entities found:")
        for entity in entities.get("entities", []):
            print(f"      • {entity['name']} ({entity['type']})")

        if entities.get("relationships"):
            print("   🔗 Relationships:")
            for rel in entities["relationships"]:
                print(f"      • {rel['from']} → {rel['to']} ({rel['type']})")
    except:
        pass

# 4. Generate holistic response
print("\n4️⃣ GENERATING HOLISTIC RESPONSE...")
print("-" * 80)

# Build comprehensive context
context = "KNOWLEDGE FROM NEO4J GRAPH:\n"
if neo4j_results:
    for r in neo4j_results:
        context += f"• Equipment: {r['equipment']}, Problem: {r['problem']}\n"
        if r["solutions"]:
            context += f"  Solutions: {', '.join(r['solutions'])}\n"

context += "\nSIMILAR PROBLEMS FROM VECTOR SEARCH:\n"
if vector_results:
    for v in vector_results[:2]:
        context += f"• ({v['similarity']:.2f}) {v['content'][:150]}\n"

context += f"\nEXTRACTED ENTITIES: {len(entities.get('entities', []))} entities found\n"

# Generate response with all knowledge
prompt = f"""You are Bob Ferrari - the most advanced AI assistant with holistic knowledge.

AVAILABLE KNOWLEDGE:
{context}

User Query: {test_query}

Provide a comprehensive response using ALL available knowledge. Be specific and helpful."""

response = model.generate_content(prompt)
if response and response.text:
    print("\n🏎️ BOB FERRARI RESPONSE:")
    print("=" * 80)
    print(response.text.strip())

# 5. Show learning capability
print("\n" + "=" * 80)
print("5️⃣ CONTINUOUS LEARNING:")
print("-" * 80)

# Save this interaction to Neo4j
with neo4j_driver.session() as session:
    session.run(
        """
        CREATE (dc:DiagnosticCase {
            case_id: $case_id,
            timestamp: datetime(),
            equipment: 'Bobcat T770',
            symptoms: $symptoms,
            diagnosis: 'P0340 Camshaft sensor failure',
            solution: 'Replace sensor and check wiring'
        })
    """,
        case_id=f"demo_{datetime.now().timestamp()}",
        symptoms=test_query,
    )

    # Count total diagnostic cases
    result = session.run("MATCH (dc:DiagnosticCase) RETURN count(dc) as count")
    count = result.single()["count"]
    print(f"   ✅ Saved to Neo4j - Now have {count} diagnostic cases")

# Save to ChromaDB
doc_id = f"learning_{datetime.now().timestamp()}"
doc_text = f"Query: {test_query}\nLearned: P0340 is camshaft sensor issue on Bobcat T770"
embedding = embedder.encode([doc_text])[0].tolist()
collection.add(documents=[doc_text], embeddings=[embedding], ids=[doc_id])
print(f"   ✅ Saved to ChromaDB - Now have {collection.count()} knowledge items")

print("\n" + "=" * 80)
print("🏁 DEMO COMPLETE - Bob Ferrari learns from every interaction!")
print("=" * 80)

# Cleanup
neo4j_driver.close()
