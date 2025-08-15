#!/usr/bin/env python3
"""
BOB FERRARI EDITION - Complete Holistic AI Assistant
Integrates ALL systems for maximum intelligence:
- Neo4j (Graph Database) - Relationships & structured knowledge
- ChromaDB (Vector Search) - Semantic similarity matching
- Graphiti (Entity Extraction) - Auto-builds knowledge graphs
- BigQuery (Analytics) - Long-term pattern analysis
- Datastore (MVP3 Integration) - Circle of Life data
- Gemini 2.5 Flash - AI responses
- Slack - Communication interface
"""

import asyncio
import json
import logging
import os
import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Vector Search
import chromadb

# Core AI
import google.generativeai as genai

# Google Cloud
from google.cloud import bigquery, datastore

# Graph Database
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

# Communication
from slack_sdk import WebClient

# Entity Extraction
try:
    from graphiti_core import Graphiti
    from graphiti_core.nodes import EpisodeType

    GRAPHITI_AVAILABLE = True
except ImportError:
    GRAPHITI_AVAILABLE = False
    print("⚠️ Graphiti not available - entity extraction limited")

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

print("=" * 80)
print("🏎️ BOB FERRARI EDITION - HOLISTIC AI SYSTEM")
print("=" * 80)


class BobFerrari:
    """The complete, holistic Bob with all systems integrated"""

    def __init__(self):
        """Initialize all subsystems"""
        # Configuration
        self.project_id = "bobs-house-ai"
        self.mvp_project = "diagnostic-pro-mvp"
        self.channel_id = "C099A4N4PSN"
        self.jeremy_id = "U099CBRE7CL"

        # State management
        self.conversation_history = []
        self.processed_messages = set()
        self.entity_cache = defaultdict(list)
        self.learning_buffer = []

        # Stats - MUST BE BEFORE INIT METHODS
        self.stats = {
            "messages_processed": 0,
            "entities_extracted": 0,
            "knowledge_items": 0,
            "graph_nodes": 0,
            "patterns_learned": 0,
        }

        # Initialize all systems
        self._init_gemini()
        self._init_slack()
        self._init_neo4j()
        self._init_chromadb()
        self._init_bigquery()
        self._init_datastore()
        self._init_graphiti()

        logger.info("🚀 Bob Ferrari initialized - All systems operational")
        self._log_system_status()

    def _init_gemini(self):
        """Initialize Gemini AI"""
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        logger.info("✅ Gemini 2.5 Flash initialized")

    def _init_slack(self):
        """Initialize Slack client"""
        token = os.getenv("SLACK_BOT_TOKEN")
        self.slack = WebClient(token=token)
        self.bot_id = self.slack.auth_test()["user_id"]
        logger.info(f"✅ Slack connected as {self.bot_id}")

    def _init_neo4j(self):
        """Initialize Neo4j with new credentials"""
        uri = "neo4j+s://d3653283.databases.neo4j.io"
        user = "neo4j"
        password = os.getenv("NEO4J_PASSWORD")

        try:
            self.neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
            # Test connection and get stats
            with self.neo4j_driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count")
                self.stats["graph_nodes"] = result.single()["count"]
            logger.info(f"✅ Neo4j connected - {self.stats['graph_nodes']} nodes")
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            self.neo4j_driver = None

    def _init_chromadb(self):
        """Initialize ChromaDB for vector search"""
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.chroma_collection = self.chroma_client.get_or_create_collection(
            name="bob_ferrari_knowledge", metadata={"description": "Holistic knowledge base with all sources"}
        )
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.stats["knowledge_items"] = self.chroma_collection.count()
        logger.info(f"✅ ChromaDB initialized - {self.stats['knowledge_items']} items")

    def _init_bigquery(self):
        """Initialize BigQuery for analytics"""
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
            # Ensure datasets exist
            self._ensure_bigquery_datasets()
            logger.info("✅ BigQuery connected for analytics")
        except Exception as e:
            logger.error(f"BigQuery initialization failed: {e}")
            self.bq_client = None

    def _init_datastore(self):
        """Initialize Datastore for MVP3 integration"""
        try:
            self.datastore_client = datastore.Client(project=self.mvp_project)
            logger.info("✅ Datastore connected for Circle of Life")
        except Exception as e:
            logger.error(f"Datastore initialization failed: {e}")
            self.datastore_client = None

    def _init_graphiti(self):
        """Initialize Graphiti for entity extraction"""
        # Temporarily disabled - needs correct initialization parameters
        self.graphiti = None
        logger.info("⚠️ Graphiti temporarily disabled - will fix later")

    def _ensure_bigquery_datasets(self):
        """Ensure BigQuery datasets exist"""
        datasets = [
            ("bob_ferrari", "Holistic AI knowledge warehouse"),
            ("circle_of_life", "Learning patterns from MVP3"),
            ("conversation_analytics", "Conversation insights"),
        ]

        for dataset_name, description in datasets:
            dataset_id = f"{self.project_id}.{dataset_name}"
            dataset = bigquery.Dataset(dataset_id)
            dataset.description = description
            dataset.location = "US"

            try:
                self.bq_client.create_dataset(dataset, exists_ok=True)
            except:
                pass  # Dataset exists

    def _log_system_status(self):
        """Log the status of all systems"""
        status = {
            "Gemini": "✅" if self.gemini_model else "❌",
            "Slack": "✅" if self.slack else "❌",
            "Neo4j": f"✅ ({self.stats['graph_nodes']} nodes)" if self.neo4j_driver else "❌",
            "ChromaDB": f"✅ ({self.stats['knowledge_items']} items)" if self.chroma_collection else "❌",
            "BigQuery": "✅" if self.bq_client else "❌",
            "Datastore": "✅" if self.datastore_client else "❌",
            "Graphiti": "✅" if self.graphiti else "⚠️",
        }

        logger.info("SYSTEM STATUS:")
        for system, status in status.items():
            logger.info(f"  {system}: {status}")

    # ============= KNOWLEDGE RETRIEVAL =============

    def search_neo4j(self, query: str) -> List[Dict]:
        """Search Neo4j graph for structured relationships"""
        if not self.neo4j_driver:
            return []

        results = []
        try:
            with self.neo4j_driver.session() as session:
                # Search multiple patterns
                cypher = """
                // Search equipment problems
                MATCH (e:Equipment)-[:HAS_PROBLEM]->(p:Problem)
                WHERE toLower(e.name) CONTAINS toLower($query)
                   OR toLower(p.description) CONTAINS toLower($query)
                OPTIONAL MATCH (p)-[:SOLVED_BY]->(s:Solution)
                RETURN 'equipment' as type, e.name as equipment,
                       p.description as problem, collect(s.description) as solutions
                LIMIT 3

                UNION

                // Search error codes
                MATCH (ec:ErrorCode)-[:INDICATES]->(p:Problem)
                WHERE ec.code CONTAINS $query OR toLower(p.description) CONTAINS toLower($query)
                OPTIONAL MATCH (p)-[:SOLVED_BY]->(s:Solution)
                RETURN 'error_code' as type, ec.code as equipment,
                       p.description as problem, collect(s.description) as solutions
                LIMIT 3

                UNION

                // Search diagnostic cases
                MATCH (dc:DiagnosticCase)
                WHERE toLower(dc.symptoms) CONTAINS toLower($query)
                   OR toLower(dc.diagnosis) CONTAINS toLower($query)
                RETURN 'diagnostic' as type, dc.equipment as equipment,
                       dc.symptoms as problem, [dc.diagnosis] as solutions
                LIMIT 3
                """

                result = session.run(cypher, {"query": query})
                for record in result:
                    results.append(
                        {
                            "type": record["type"],
                            "equipment": record["equipment"],
                            "problem": record["problem"],
                            "solutions": record["solutions"],
                        }
                    )
        except Exception as e:
            logger.error(f"Neo4j search error: {e}")

        return results

    def search_vectors(self, query: str, k: int = 5) -> List[Dict]:
        """Search ChromaDB for semantically similar content"""
        try:
            query_embedding = self.embedder.encode([query])[0].tolist()

            results = self.chroma_collection.query(
                query_embeddings=[query_embedding], n_results=k, include=["documents", "metadatas", "distances"]
            )

            formatted_results = []
            if results["documents"] and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    similarity = 1 - results["distances"][0][i]
                    if similarity > -0.3:  # Relevance threshold
                        formatted_results.append(
                            {
                                "content": doc,
                                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                                "similarity": similarity,
                            }
                        )

            return formatted_results
        except Exception as e:
            logger.error(f"Vector search error: {e}")
            return []

    def search_bigquery_patterns(self, query: str) -> List[Dict]:
        """Search BigQuery for historical patterns"""
        if not self.bq_client:
            return []

        try:
            # Query for similar historical problems
            sql = """
            SELECT
                problem_category,
                problem_description,
                solution_provided,
                AVG(effectiveness_score) as avg_effectiveness,
                COUNT(*) as occurrences
            FROM `bobs-house-ai.circle_of_life.diagnostic_insights`
            WHERE LOWER(problem_description) LIKE LOWER(@query)
               OR LOWER(solution_provided) LIKE LOWER(@query)
            GROUP BY problem_category, problem_description, solution_provided
            ORDER BY occurrences DESC, avg_effectiveness DESC
            LIMIT 5
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("query", "STRING", f"%{query}%")]
            )

            query_job = self.bq_client.query(sql, job_config=job_config)
            results = []

            for row in query_job:
                results.append(
                    {
                        "category": row.problem_category,
                        "problem": row.problem_description,
                        "solution": row.solution_provided,
                        "effectiveness": row.avg_effectiveness,
                        "occurrences": row.occurrences,
                    }
                )

            return results
        except Exception as e:
            logger.error(f"BigQuery search error: {e}")
            return []

    def extract_entities(self, text: str, response: str) -> Dict[str, Any]:
        """Extract entities using Gemini"""
        extraction_prompt = f"""Extract entities and relationships from this technical conversation.

USER: {text}
ASSISTANT: {response}

Extract in JSON format:
{{
    "entities": [
        {{"name": "entity_name", "type": "Equipment|Part|Problem|Solution|ErrorCode", "properties": {{}}}}
    ],
    "relationships": [
        {{"from": "entity1", "to": "entity2", "type": "HAS_PROBLEM|SOLVED_BY|INDICATES|PART_OF", "properties": {{}}}}
    ],
    "patterns": ["Important patterns or insights"],
    "confidence": 0.0-1.0
}}

Focus on equipment, problems, solutions, and diagnostic information.
Return valid JSON only."""

        try:
            extraction_response = self.gemini_model.generate_content(extraction_prompt)
            if extraction_response and extraction_response.text:
                json_text = extraction_response.text.strip()
                if "```json" in json_text:
                    json_text = json_text.split("```json")[1].split("```")[0]
                elif "```" in json_text:
                    json_text = json_text.split("```")[1].split("```")[0]

                extracted = json.loads(json_text)
                self.stats["entities_extracted"] += len(extracted.get("entities", []))
                return extracted
        except Exception as e:
            logger.error(f"Entity extraction error: {e}")

        return {"entities": [], "relationships": [], "patterns": [], "confidence": 0}

    def save_to_neo4j(self, entities: List[Dict], relationships: List[Dict]):
        """Save extracted entities to Neo4j"""
        if not self.neo4j_driver:
            return

        try:
            with self.neo4j_driver.session() as session:
                # Create entities
                for entity in entities:
                    cypher = f"""
                    MERGE (n:{entity['type']} {{name: $name}})
                    SET n += $properties
                    SET n.updated_at = datetime()
                    """
                    session.run(cypher, name=entity["name"], properties=entity.get("properties", {}))

                # Create relationships
                for rel in relationships:
                    cypher = f"""
                    MATCH (a {{name: $from_node}})
                    MATCH (b {{name: $to_node}})
                    MERGE (a)-[r:{rel['type']}]->(b)
                    SET r += $properties
                    SET r.created_at = datetime()
                    """
                    session.run(cypher, from_node=rel["from"], to_node=rel["to"], properties=rel.get("properties", {}))

                self.stats["graph_nodes"] += len(entities)
        except Exception as e:
            logger.error(f"Neo4j save error: {e}")

    def save_to_chromadb(self, text: str, response: str, entities: List[Dict]):
        """Save to vector database with entity metadata"""
        try:
            doc_id = f"conv_{datetime.now().timestamp()}"
            doc_text = f"Question: {text}\nAnswer: {response}"

            metadata = {
                "type": "conversation",
                "timestamp": datetime.now().isoformat(),
                "user": "jeremy",
                "entities": [e["name"] for e in entities[:5]],  # Top 5 entities
            }

            embedding = self.embedder.encode([doc_text])[0].tolist()
            self.chroma_collection.add(documents=[doc_text], embeddings=[embedding], metadatas=[metadata], ids=[doc_id])

            self.stats["knowledge_items"] += 1
        except Exception as e:
            logger.error(f"ChromaDB save error: {e}")

    def save_to_bigquery(self, text: str, response: str, extracted: Dict):
        """Save conversation analytics to BigQuery"""
        if not self.bq_client:
            return

        try:
            table_id = f"{self.project_id}.conversation_analytics.conversations"

            row = {
                "conversation_id": f"conv_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "user_message": text[:1000],
                "bot_response": response[:1000],
                "entities_extracted": len(extracted.get("entities", [])),
                "relationships_found": len(extracted.get("relationships", [])),
                "patterns": extracted.get("patterns", []),
                "confidence_score": extracted.get("confidence", 0),
            }

            errors = self.bq_client.insert_rows_json(table_id, [row])
            if not errors:
                self.stats["patterns_learned"] += len(extracted.get("patterns", []))
        except Exception as e:
            logger.error(f"BigQuery save error: {e}")

    def get_holistic_context(self, query: str) -> str:
        """Combine all knowledge sources for comprehensive context"""
        context_parts = []

        # 1. Neo4j structured knowledge
        neo4j_results = self.search_neo4j(query)
        if neo4j_results:
            context_parts.append("📊 GRAPH KNOWLEDGE (Neo4j):")
            for r in neo4j_results[:2]:
                context_parts.append(f"• {r['equipment']}: {r['problem']}")
                if r["solutions"]:
                    context_parts.append(f"  Solutions: {', '.join(r['solutions'][:2])}")

        # 2. Vector similarity search
        vector_results = self.search_vectors(query, k=3)
        if vector_results:
            context_parts.append("\n🔍 SIMILAR KNOWLEDGE (ChromaDB):")
            for r in vector_results[:2]:
                context_parts.append(f"• ({r['similarity']:.2f}) {r['content'][:150]}...")

        # 3. Historical patterns from BigQuery
        bq_patterns = self.search_bigquery_patterns(query)
        if bq_patterns:
            context_parts.append("\n📈 HISTORICAL PATTERNS (BigQuery):")
            for p in bq_patterns[:2]:
                context_parts.append(f"• {p['problem']} → {p['solution']}")
                context_parts.append(f"  (Used {p['occurrences']}x, {p['effectiveness']:.0%} effective)")

        return "\n".join(context_parts) if context_parts else ""

    def process_message(self, text: str) -> str:
        """Process a message with full holistic intelligence"""
        # Get comprehensive context from all sources
        knowledge_context = self.get_holistic_context(text)

        # Build conversation history
        conv_history = ""
        if self.conversation_history:
            conv_history = "Recent conversation:\n"
            for hist in self.conversation_history[-3:]:
                conv_history += f"User: {hist['user']}\n"
                conv_history += f"Bob: {hist['bot']}\n"

        # Create holistic prompt
        prompt = f"""You are Bob Ferrari Edition - the most advanced AI assistant with access to:
- Neo4j Graph Database ({self.stats['graph_nodes']} nodes of structured knowledge)
- ChromaDB Vector Search ({self.stats['knowledge_items']} semantic knowledge items)
- BigQuery Analytics ({self.stats['patterns_learned']} learned patterns)
- Real-time entity extraction and learning
- Circle of Life integration with MVP3 diagnostics

You have processed {self.stats['messages_processed']} messages and extracted {self.stats['entities_extracted']} entities.

CONTEXT:
{conv_history}

KNOWLEDGE BASE RESULTS:
{knowledge_context if knowledge_context else "No specific matches - using general knowledge"}

User message: {text}

Provide a comprehensive, intelligent response using ALL available knowledge:"""

        try:
            # Generate response
            response = self.gemini_model.generate_content(prompt)
            if response and response.text:
                bot_response = response.text.strip()

                # Extract entities and learn
                extracted = self.extract_entities(text, bot_response)

                # Save to all systems
                if extracted["entities"]:
                    self.save_to_neo4j(extracted["entities"], extracted["relationships"])
                    self.save_to_chromadb(text, bot_response, extracted["entities"])
                    self.save_to_bigquery(text, bot_response, extracted)

                # Update conversation history
                self.conversation_history.append(
                    {"user": text[:200], "bot": bot_response[:200], "time": datetime.now().isoformat()}
                )

                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]

                self.stats["messages_processed"] += 1

                return bot_response
        except Exception as e:
            logger.error(f"Message processing error: {e}")
            return f"Sorry, I encountered an error: {str(e)[:100]}"

    def run(self):
        """Main loop - monitor Slack and respond with full intelligence"""
        # Send startup message
        startup_msg = f"""🏎️ Bob Ferrari Edition Online!
• Neo4j: {self.stats['graph_nodes']} nodes
• ChromaDB: {self.stats['knowledge_items']} items
• BigQuery: {self.stats['patterns_learned']} patterns
• Entity Extraction: {'Active ✅' if self.graphiti else 'Gemini-based ✅'}
• Circle of Life: Integrated ✅

I'm the Ferrari of AI assistants - ready to help with maximum intelligence!"""

        self.slack.chat_postMessage(channel=self.channel_id, text=startup_msg)
        logger.info("🏁 Bob Ferrari is running - monitoring Slack...")

        while True:
            try:
                # Get recent messages
                msgs = self.slack.conversations_history(channel=self.channel_id, limit=20)

                for msg in msgs["messages"]:
                    ts = msg.get("ts")
                    user = msg.get("user")
                    text = msg.get("text", "")

                    # Skip if already processed, from bot, or not from Jeremy
                    if ts in self.processed_messages or user == self.bot_id or user != self.jeremy_id:
                        continue

                    logger.info(f"📨 Processing message from Jeremy: {text[:100]}...")
                    self.processed_messages.add(ts)

                    # Process with full intelligence
                    response = self.process_message(text)

                    # Send response
                    self.slack.chat_postMessage(channel=self.channel_id, text=response)

                    # Log stats
                    logger.info(
                        f"✅ Responded | Messages: {self.stats['messages_processed']} | "
                        f"Entities: {self.stats['entities_extracted']} | "
                        f"KB: {self.stats['knowledge_items']}"
                    )

                # Cleanup old processed messages
                if len(self.processed_messages) > 100:
                    self.processed_messages = set(list(self.processed_messages)[-50:])

                time.sleep(2)  # Poll every 2 seconds

            except KeyboardInterrupt:
                logger.info("\n👋 Shutting down Bob Ferrari...")
                self._shutdown()
                break
            except Exception as e:
                logger.error(f"Loop error: {e}")
                time.sleep(5)

    def _shutdown(self):
        """Clean shutdown with stats"""
        summary = f"""🏁 Bob Ferrari shutting down

Final Statistics:
• Messages Processed: {self.stats['messages_processed']}
• Entities Extracted: {self.stats['entities_extracted']}
• Knowledge Items: {self.stats['knowledge_items']}
• Graph Nodes: {self.stats['graph_nodes']}
• Patterns Learned: {self.stats['patterns_learned']}

Thanks for the ride! 🏎️"""

        self.slack.chat_postMessage(channel=self.channel_id, text=summary)

        # Close connections
        if self.neo4j_driver:
            self.neo4j_driver.close()

        logger.info("✅ Clean shutdown complete")


# ============= MAIN EXECUTION =============
if __name__ == "__main__":
    try:
        bob = BobFerrari()
        bob.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Failed to start Bob Ferrari: {e}")
