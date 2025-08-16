#!/usr/bin/env python3
"""
Simplified Graphiti Framework without AI Dependencies
Focuses on knowledge graph operations without LLM/embeddings
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from google.cloud import bigquery
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)


class SimpleGraphiti:
    """
    Graphiti-compatible framework without AI dependencies
    Manages knowledge graph in Neo4j and syncs with BigQuery
    """

    def __init__(self, uri: str, user: str, password: str, project_id: str = "bobs-house-ai"):
        """Initialize connection to Neo4j and BigQuery"""
        self.uri = uri
        self.user = user
        self.password = password
        self.project_id = project_id

        # Initialize Neo4j driver
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.driver.verify_connectivity()
            logger.info(f"✅ Connected to Neo4j at {uri}")
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            self.driver = None

        # Initialize BigQuery client
        try:
            self.bq_client = bigquery.Client(project=project_id)
            logger.info(f"✅ Connected to BigQuery project {project_id}")
        except Exception as e:
            logger.error(f"❌ BigQuery connection failed: {e}")
            self.bq_client = None

    def add_episode(self, content: str, user: str = "system", metadata: Dict = None):
        """
        Add an episode (conversation/event) to the knowledge graph
        This replaces the AI-powered entity extraction with simple pattern matching
        """
        if not self.driver:
            logger.warning("Neo4j not connected, skipping episode")
            return None

        episode_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()
        timestamp = datetime.now().isoformat()

        with self.driver.session() as session:
            # Create episode node
            episode_query = """
            CREATE (e:Episode {
                id: $episode_id,
                content: $content,
                user: $user,
                timestamp: $timestamp,
                metadata: $metadata
            })
            RETURN e
            """

            result = session.run(
                episode_query,
                episode_id=episode_id,
                content=content,
                user=user,
                timestamp=timestamp,
                metadata=json.dumps(metadata) if metadata else "{}",
            )

            # Extract simple entities (keywords) without AI
            entities = self._extract_entities_simple(content)

            # Create entity nodes and relationships
            for entity in entities:
                entity_query = """
                MERGE (ent:Entity {name: $name, type: $type})
                WITH ent
                MATCH (e:Episode {id: $episode_id})
                CREATE (e)-[:MENTIONS]->(ent)
                """
                session.run(entity_query, name=entity["name"], type=entity["type"], episode_id=episode_id)

            # Sync to BigQuery
            self._sync_to_bigquery(episode_id, content, user, entities, metadata)

            logger.info(f"✅ Added episode {episode_id} with {len(entities)} entities")
            return episode_id

    def search(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Search the knowledge graph for relevant episodes
        Uses simple text matching instead of vector similarity
        """
        if not self.driver:
            logger.warning("Neo4j not connected, returning empty results")
            return []

        results = []

        with self.driver.session() as session:
            # Simple text search query
            search_query = """
            MATCH (e:Episode)
            WHERE toLower(e.content) CONTAINS toLower($query)
            RETURN e.id as id, e.content as content, e.user as user,
                   e.timestamp as timestamp, e.metadata as metadata
            ORDER BY e.timestamp DESC
            LIMIT $limit
            """

            result = session.run(search_query, query=query, limit=num_results)

            for record in result:
                results.append(
                    {
                        "id": record["id"],
                        "content": record["content"],
                        "user": record["user"],
                        "timestamp": record["timestamp"],
                        "metadata": json.loads(record["metadata"]) if record["metadata"] else {},
                    }
                )

        return results

    def get_entities(self, entity_type: str = None) -> List[Dict]:
        """Get all entities of a specific type or all entities"""
        if not self.driver:
            return []

        with self.driver.session() as session:
            if entity_type:
                query = """
                MATCH (e:Entity {type: $type})
                RETURN e.name as name, e.type as type,
                       size((e)<-[:MENTIONS]-()) as mention_count
                ORDER BY mention_count DESC
                """
                result = session.run(query, type=entity_type)
            else:
                query = """
                MATCH (e:Entity)
                RETURN e.name as name, e.type as type,
                       size((e)<-[:MENTIONS]-()) as mention_count
                ORDER BY mention_count DESC
                """
                result = session.run(query)

            entities = []
            for record in result:
                entities.append(
                    {"name": record["name"], "type": record["type"], "mention_count": record["mention_count"]}
                )

            return entities

    def get_relationships(self, entity_name: str) -> List[Dict]:
        """Get all relationships for a specific entity"""
        if not self.driver:
            return []

        with self.driver.session() as session:
            query = """
            MATCH (e:Entity {name: $name})-[r]-(other)
            RETURN type(r) as relationship,
                   labels(other) as other_labels,
                   other.name as other_name,
                   other.id as other_id
            """
            result = session.run(query, name=entity_name)

            relationships = []
            for record in result:
                relationships.append(
                    {
                        "relationship": record["relationship"],
                        "other_type": record["other_labels"][0] if record["other_labels"] else "Unknown",
                        "other_name": record["other_name"],
                        "other_id": record["other_id"],
                    }
                )

            return relationships

    def _extract_entities_simple(self, content: str) -> List[Dict]:
        """
        Simple entity extraction without AI
        Extracts equipment types, error codes, and key terms
        """
        entities = []
        content_lower = content.lower()

        # Equipment types
        equipment_types = [
            "excavator",
            "skid steer",
            "loader",
            "dozer",
            "grader",
            "tractor",
            "mower",
            "generator",
            "compressor",
            "forklift",
            "bobcat",
            "caterpillar",
            "john deere",
            "kubota",
            "case",
        ]

        for equipment in equipment_types:
            if equipment in content_lower:
                entities.append({"name": equipment.title(), "type": "Equipment"})

        # Error codes (pattern: uppercase letters followed by numbers)
        import re

        error_pattern = r"\b[A-Z]{1,4}[-]?\d{3,5}\b"
        errors = re.findall(error_pattern, content)
        for error in errors:
            entities.append({"name": error, "type": "ErrorCode"})

        # Repair types
        repair_types = [
            "hydraulic",
            "engine",
            "transmission",
            "electrical",
            "fuel",
            "cooling",
            "brake",
            "steering",
            "pto",
        ]

        for repair in repair_types:
            if repair in content_lower:
                entities.append({"name": repair.title(), "type": "RepairType"})

        # Remove duplicates
        seen = set()
        unique_entities = []
        for entity in entities:
            key = f"{entity['name']}:{entity['type']}"
            if key not in seen:
                seen.add(key)
                unique_entities.append(entity)

        return unique_entities

    def _sync_to_bigquery(self, episode_id: str, content: str, user: str, entities: List[Dict], metadata: Dict):
        """Sync episode data to BigQuery for analytics"""
        if not self.bq_client:
            return

        try:
            # Ensure dataset and table exist
            dataset_id = f"{self.project_id}.graphiti_knowledge"
            table_id = f"{dataset_id}.episodes"

            # Create dataset if it doesn't exist
            try:
                dataset = bigquery.Dataset(dataset_id)
                dataset.location = "US"
                self.bq_client.create_dataset(dataset, exists_ok=True)
            except:
                pass

            # Create table if it doesn't exist
            schema = [
                bigquery.SchemaField("episode_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("content", "STRING"),
                bigquery.SchemaField("user", "STRING"),
                bigquery.SchemaField("entities", "JSON"),
                bigquery.SchemaField("metadata", "JSON"),
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
            ]

            table = bigquery.Table(table_id, schema=schema)
            try:
                self.bq_client.create_table(table, exists_ok=True)
            except:
                pass

            # Insert episode data
            rows = [
                {
                    "episode_id": episode_id,
                    "content": content[:10000],  # Limit content size
                    "user": user,
                    "entities": entities,
                    "metadata": metadata,
                    "timestamp": datetime.now(),
                }
            ]

            errors = self.bq_client.insert_rows_json(table_id, rows)
            if errors:
                logger.warning(f"BigQuery insert errors: {errors}")
            else:
                logger.info(f"✅ Synced episode to BigQuery")

        except Exception as e:
            logger.error(f"BigQuery sync failed: {e}")

    def analyze_patterns(self) -> Dict:
        """
        Analyze patterns in the knowledge graph
        This is used by Circle of Life for learning
        """
        if not self.driver:
            return {}

        patterns = {
            "most_mentioned_equipment": [],
            "common_error_codes": [],
            "frequent_repair_types": [],
            "user_activity": [],
        }

        with self.driver.session() as session:
            # Most mentioned equipment
            result = session.run(
                """
                MATCH (e:Entity {type: 'Equipment'})
                RETURN e.name as name, size((e)<-[:MENTIONS]-()) as count
                ORDER BY count DESC
                LIMIT 10
            """
            )
            patterns["most_mentioned_equipment"] = [{"name": r["name"], "count": r["count"]} for r in result]

            # Common error codes
            result = session.run(
                """
                MATCH (e:Entity {type: 'ErrorCode'})
                RETURN e.name as name, size((e)<-[:MENTIONS]-()) as count
                ORDER BY count DESC
                LIMIT 10
            """
            )
            patterns["common_error_codes"] = [{"code": r["name"], "count": r["count"]} for r in result]

            # Frequent repair types
            result = session.run(
                """
                MATCH (e:Entity {type: 'RepairType'})
                RETURN e.name as name, size((e)<-[:MENTIONS]-()) as count
                ORDER BY count DESC
                LIMIT 10
            """
            )
            patterns["frequent_repair_types"] = [{"type": r["name"], "count": r["count"]} for r in result]

            # User activity
            result = session.run(
                """
                MATCH (e:Episode)
                RETURN e.user as user, count(e) as episode_count
                ORDER BY episode_count DESC
            """
            )
            patterns["user_activity"] = [{"user": r["user"], "episodes": r["episode_count"]} for r in result]

        return patterns

    def close(self):
        """Close database connections"""
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")


# Integration with existing Graphiti interface
class GraphitiCompatible(SimpleGraphiti):
    """
    Wrapper to make SimpleGraphiti compatible with existing Graphiti calls
    """

    async def add_episode(self, *args, **kwargs):
        """Async wrapper for compatibility"""
        return super().add_episode(*args, **kwargs)

    async def search(self, *args, **kwargs):
        """Async wrapper for compatibility"""
        return super().search(*args, **kwargs)

    def build_context(self, query: str, num_results: int = 5) -> str:
        """Build context string from search results"""
        results = self.search(query, num_results)
        context_parts = []

        for result in results:
            context_parts.append(f"[{result['timestamp']}] {result['user']}: {result['content']}")

        return "\n\n".join(context_parts)


if __name__ == "__main__":
    # Test the simplified Graphiti
    import asyncio

    # Get Neo4j credentials
    neo4j_uri = os.environ.get("NEO4J_URI", "bolt://10.128.0.2:7687")
    neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
    neo4j_password = os.environ.get("NEO4J_PASSWORD", "BobBrain2025")

    # Create instance
    graphiti = SimpleGraphiti(neo4j_uri, neo4j_user, neo4j_password)

    # Test adding an episode
    episode_id = graphiti.add_episode(
        "The John Deere excavator is showing error code E2003 related to hydraulic pressure",
        user="test_user",
        metadata={"source": "test"},
    )

    print(f"Added episode: {episode_id}")

    # Test searching
    results = graphiti.search("excavator")
    print(f"Search results: {results}")

    # Test entity extraction
    entities = graphiti.get_entities("Equipment")
    print(f"Equipment entities: {entities}")

    # Test pattern analysis
    patterns = graphiti.analyze_patterns()
    print(f"Patterns: {json.dumps(patterns, indent=2)}")

    graphiti.close()
