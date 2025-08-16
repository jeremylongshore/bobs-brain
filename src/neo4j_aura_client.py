#!/usr/bin/env python3
"""
Neo4j Aura Client for Google Cloud
Provides API integration between Bob Brain and Neo4j Aura
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from neo4j import AsyncGraphDatabase, GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Neo4jAuraClient:
    """Neo4j Aura client optimized for Google Cloud"""

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """Initialize Neo4j Aura connection"""

        # Get credentials from environment or parameters
        self.uri = (
            uri or os.getenv("NEO4J_URI") or os.getenv("NEO4J_AURA_URI") or "neo4j+s://d3653283.databases.neo4j.io"
        )
        self.user = user or os.getenv("NEO4J_USER") or os.getenv("NEO4J_USERNAME") or "neo4j"
        self.password = (
            password
            or os.getenv("NEO4J_PASSWORD")
            or os.getenv("NEO4J_AURA_PASSWORD")
            or "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"
        )

        # Connection settings optimized for cloud
        self.driver = None
        self.async_driver = None
        self._connected = False

        logger.info(f"Neo4j Aura client configured for: {self.uri}")

    def connect(self) -> bool:
        """Establish connection to Neo4j Aura"""
        try:
            self.driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                connection_timeout=30,  # Longer timeout for cloud
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                fetch_size=1000,
                encrypted=True,  # Always encrypted for Aura
            )

            # Verify connection
            with self.driver.session() as session:
                result = session.run("RETURN 1 as test")
                if result.single()["test"] == 1:
                    self._connected = True
                    logger.info("✅ Connected to Neo4j Aura")
                    return True

        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self._connected = False
            return False

    async def connect_async(self) -> bool:
        """Establish async connection for high-performance operations"""
        try:
            self.async_driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                connection_timeout=30,
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
            )

            # Verify connection
            async with self.async_driver.session() as session:
                result = await session.run("RETURN 1 as test")
                record = await result.single()
                if record["test"] == 1:
                    logger.info("✅ Async connection to Neo4j Aura established")
                    return True

        except Exception as e:
            logger.error(f"❌ Async connection failed: {e}")
            return False

    def close(self):
        """Close connections"""
        if self.driver:
            self.driver.close()
        if self.async_driver:
            asyncio.run(self.async_driver.close())

    # Knowledge Graph APIs

    def store_conversation(self, user_message: str, bob_response: str, metadata: Dict = None) -> str:
        """Store conversation in knowledge graph"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                query = """
                CREATE (c:Conversation {
                    id: randomUUID(),
                    timestamp: datetime(),
                    user_message: $user_message,
                    bob_response: $bob_response,
                    metadata: $metadata
                })
                RETURN c.id as conversation_id
                """

                result = session.run(
                    query, user_message=user_message, bob_response=bob_response, metadata=json.dumps(metadata or {})
                )

                conversation_id = result.single()["conversation_id"]
                logger.info(f"Stored conversation: {conversation_id}")
                return conversation_id

        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")
            return None

    def extract_entities(self, text: str) -> List[Dict]:
        """Extract and store entities from text"""
        if not self._connected:
            self.connect()

        entities = []

        try:
            with self.driver.session() as session:
                # Extract equipment mentions
                equipment_query = """
                WITH $text as text
                UNWIND [
                    'excavator', 'skid steer', 'loader', 'dozer', 'grader',
                    'tractor', 'mower', 'bobcat', 'caterpillar', 'john deere',
                    'kubota', 'case', 'volvo', 'komatsu', 'hitachi'
                ] as equipment
                WHERE toLower(text) CONTAINS toLower(equipment)
                MERGE (e:Equipment {name: equipment})
                SET e.last_mentioned = datetime()
                RETURN e.name as entity, 'Equipment' as type
                """

                result = session.run(equipment_query, text=text)
                for record in result:
                    entities.append({"entity": record["entity"], "type": record["type"]})

                # Extract error codes
                error_code_query = """
                WITH $text as text
                WITH text,
                     [x IN split(text, ' ') WHERE x =~ '[A-Z]{1,4}[-]?[0-9]{3,5}'] as codes
                UNWIND codes as code
                MERGE (e:ErrorCode {code: code})
                SET e.last_seen = datetime()
                RETURN e.code as entity, 'ErrorCode' as type
                """

                result = session.run(error_code_query, text=text)
                for record in result:
                    entities.append({"entity": record["entity"], "type": record["type"]})

                logger.info(f"Extracted {len(entities)} entities")
                return entities

        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []

    def create_knowledge_relationship(self, entity1: str, relationship: str, entity2: str) -> bool:
        """Create relationship between entities in knowledge graph"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                query = """
                MERGE (e1:Entity {name: $entity1})
                MERGE (e2:Entity {name: $entity2})
                MERGE (e1)-[r:RELATES_TO {type: $relationship}]->(e2)
                SET r.created = datetime()
                RETURN r
                """

                session.run(query, entity1=entity1, relationship=relationship, entity2=entity2)

                logger.info(f"Created relationship: {entity1} --[{relationship}]--> {entity2}")
                return True

        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            return False

    def query_knowledge(self, query: str, limit: int = 10) -> List[Dict]:
        """Query knowledge graph with natural language"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                # Search for relevant nodes
                cypher_query = """
                CALL db.index.fulltext.queryNodes('entity_search', $query)
                YIELD node, score
                RETURN node, score
                ORDER BY score DESC
                LIMIT $limit
                """

                result = session.run(cypher_query, query=query, limit=limit)

                results = []
                for record in result:
                    node = dict(record["node"])
                    results.append({"data": node, "score": record["score"]})

                return results

        except Exception as e:
            logger.error(f"Knowledge query failed: {e}")
            # Fallback to simple search
            return self._simple_search(query, limit)

    def _simple_search(self, query: str, limit: int = 10) -> List[Dict]:
        """Simple fallback search"""
        try:
            with self.driver.session() as session:
                cypher_query = """
                MATCH (n)
                WHERE toLower(n.name) CONTAINS toLower($query)
                   OR toLower(n.code) CONTAINS toLower($query)
                   OR toLower(n.user_message) CONTAINS toLower($query)
                   OR toLower(n.bob_response) CONTAINS toLower($query)
                RETURN n
                LIMIT $limit
                """

                result = session.run(cypher_query, query=query, limit=limit)

                results = []
                for record in result:
                    results.append({"data": dict(record["n"])})

                return results

        except Exception as e:
            logger.error(f"Simple search failed: {e}")
            return []

    def get_learning_patterns(self) -> List[Dict]:
        """Extract learning patterns for Circle of Life"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                query = """
                MATCH (c:Conversation)
                WITH c.user_message as question, c.bob_response as answer, count(*) as frequency
                WHERE frequency > 1
                RETURN question, answer, frequency
                ORDER BY frequency DESC
                LIMIT 100
                """

                result = session.run(query)

                patterns = []
                for record in result:
                    patterns.append(
                        {"question": record["question"], "answer": record["answer"], "frequency": record["frequency"]}
                    )

                return patterns

        except Exception as e:
            logger.error(f"Failed to get learning patterns: {e}")
            return []

    def store_diagnostic_data(self, diagnostic: Dict) -> bool:
        """Store diagnostic data from MVP3"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                query = """
                CREATE (d:Diagnostic {
                    id: randomUUID(),
                    timestamp: datetime(),
                    equipment: $equipment,
                    error_code: $error_code,
                    description: $description,
                    solution: $solution,
                    metadata: $metadata
                })

                WITH d
                MERGE (e:Equipment {name: $equipment})
                MERGE (d)-[:DIAGNOSED]->(e)

                WITH d
                WHERE $error_code IS NOT NULL
                MERGE (ec:ErrorCode {code: $error_code})
                MERGE (d)-[:HAS_ERROR]->(ec)

                RETURN d.id as diagnostic_id
                """

                result = session.run(
                    query,
                    equipment=diagnostic.get("equipment", "Unknown"),
                    error_code=diagnostic.get("error_code"),
                    description=diagnostic.get("description", ""),
                    solution=diagnostic.get("solution", ""),
                    metadata=json.dumps(diagnostic.get("metadata", {})),
                )

                diagnostic_id = result.single()["diagnostic_id"]
                logger.info(f"Stored diagnostic: {diagnostic_id}")
                return True

        except Exception as e:
            logger.error(f"Failed to store diagnostic: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get database statistics"""
        if not self._connected:
            self.connect()

        try:
            with self.driver.session() as session:
                stats_query = """
                MATCH (n)
                WITH labels(n) as label
                UNWIND label as l
                WITH l, count(*) as count
                RETURN l as label, count
                ORDER BY count DESC
                """

                result = session.run(stats_query)

                stats = {}
                for record in result:
                    stats[record["label"]] = record["count"]

                # Get total relationships
                rel_query = "MATCH ()-[r]->() RETURN count(r) as total"
                result = session.run(rel_query)
                stats["total_relationships"] = result.single()["total"]

                return stats

        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}


class Neo4jAuraAPI:
    """REST API wrapper for Neo4j Aura operations"""

    def __init__(self):
        self.client = Neo4jAuraClient()
        self.client.connect()

    def health_check(self) -> Dict:
        """API health check endpoint"""
        try:
            stats = self.client.get_stats()
            return {"status": "healthy", "connected": self.client._connected, "database": "Neo4j Aura", "stats": stats}
        except:
            return {"status": "unhealthy", "connected": False, "error": "Connection failed"}

    def process_message(self, message: str, response: str = None) -> Dict:
        """Process message through Neo4j APIs"""

        # Extract entities
        entities = self.client.extract_entities(message)

        # Store conversation if response provided
        conversation_id = None
        if response:
            conversation_id = self.client.store_conversation(message, response)

        # Query for relevant knowledge
        knowledge = self.client.query_knowledge(message, limit=5)

        return {"conversation_id": conversation_id, "entities": entities, "knowledge": knowledge}

    def learn(self, feedback: Dict) -> Dict:
        """Process learning feedback"""

        # Extract patterns
        patterns = self.client.get_learning_patterns()

        # Store diagnostic if provided
        if "diagnostic" in feedback:
            self.client.store_diagnostic_data(feedback["diagnostic"])

        return {"patterns_found": len(patterns), "learning_complete": True}

    def close(self):
        """Cleanup connections"""
        self.client.close()


# Export for use in Bob Brain
__all__ = ["Neo4jAuraClient", "Neo4jAuraAPI"]
