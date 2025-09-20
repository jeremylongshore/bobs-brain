#!/usr/bin/env python3
"""
Scraper Neo4j Router - Phase 4
Redirects all scraper data to Neo4j for Graphiti knowledge graph
Separates scraping from diagnostic data (which goes to BigQuery)
"""

import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScraperNeo4jRouter:
    """Routes all scraped data to Neo4j for Bob's knowledge graph"""

    def __init__(self):
        # Neo4j connection (via VPC for Cloud Run)
        if os.environ.get("K_SERVICE"):  # Running on Cloud Run
            self.neo4j_uri = "bolt://10.128.0.2:7687"  # Internal IP via VPC
        else:
            self.neo4j_uri = "bolt://34.46.31.224:7687"  # External IP for local

        self.neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
        self.neo4j_password = os.environ.get("NEO4J_PASSWORD", "bobshouse123")

        self.driver = None
        self._connect()

    def _connect(self):
        """Establish Neo4j connection"""
        try:
            self.driver = GraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_user, self.neo4j_password))
            # Test connection
            with self.driver.session() as session:
                result = session.run("RETURN 1")
                if result.single():
                    logger.info(f"✅ Connected to Neo4j at {self.neo4j_uri}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to Neo4j: {e}")
            self.driver = None

    def store_scraped_content(self, content: Dict[str, Any]) -> bool:
        """Store scraped content in Neo4j for Graphiti"""
        if not self.driver:
            logger.warning("⚠️ Neo4j not available, cannot store scraped content")
            return False

        try:
            with self.driver.session() as session:
                # Create content node
                content_id = self._generate_id(content.get("url", "") + content.get("title", ""))

                query = """
                MERGE (c:ScrapedContent {id: $id})
                SET c.url = $url,
                    c.title = $title,
                    c.content = $content,
                    c.source_type = $source_type,
                    c.category = $category,
                    c.scraped_at = $scraped_at,
                    c.metadata = $metadata

                // Create relationships to knowledge categories
                WITH c
                UNWIND $tags AS tag
                MERGE (t:Tag {name: tag})
                MERGE (c)-[:TAGGED_WITH]->(t)

                // Link to equipment if mentioned
                WITH c
                UNWIND $equipment AS equip
                MERGE (e:Equipment {type: equip})
                MERGE (c)-[:RELATES_TO]->(e)

                RETURN c.id as content_id
                """

                # Extract tags and equipment from content
                tags = self._extract_tags(content)
                equipment = self._extract_equipment(content)

                result = session.run(
                    query,
                    {
                        "id": content_id,
                        "url": content.get("url", ""),
                        "title": content.get("title", ""),
                        "content": content.get("content", "")[:5000],  # Limit content size
                        "source_type": content.get("source_type", "unknown"),
                        "category": content.get("category", "general"),
                        "scraped_at": datetime.utcnow().isoformat(),
                        "metadata": json.dumps(content.get("metadata", {})),
                        "tags": tags,
                        "equipment": equipment,
                    },
                )

                if result.single():
                    logger.info(f"✅ Stored scraped content in Neo4j: {content_id}")

                    # Also create knowledge relationships
                    self._create_knowledge_relationships(session, content_id, content)

                    return True

        except Exception as e:
            logger.error(f"❌ Failed to store in Neo4j: {e}")

        return False

    def _create_knowledge_relationships(self, session, content_id: str, content: Dict):
        """Create relationships in the knowledge graph"""
        try:
            # Link to problem patterns
            if "problem" in content.get("content", "").lower():
                query = """
                MATCH (c:ScrapedContent {id: $content_id})
                MERGE (p:ProblemPattern {type: 'diagnostic'})
                MERGE (c)-[:DESCRIBES_PROBLEM]->(p)
                """
                session.run(query, {"content_id": content_id})

            # Link to solution patterns
            if any(word in content.get("content", "").lower() for word in ["fix", "repair", "solution", "solve"]):
                query = """
                MATCH (c:ScrapedContent {id: $content_id})
                MERGE (s:SolutionPattern {type: 'repair'})
                MERGE (c)-[:PROVIDES_SOLUTION]->(s)
                """
                session.run(query, {"content_id": content_id})

            # Link to Bob's knowledge base
            query = """
            MATCH (c:ScrapedContent {id: $content_id})
            MERGE (kb:KnowledgeBase {name: 'BobBrain'})
            MERGE (c)-[:PART_OF]->(kb)
            """
            session.run(query, {"content_id": content_id})

        except Exception as e:
            logger.warning(f"⚠️ Failed to create relationships: {e}")

    def _extract_tags(self, content: Dict) -> List[str]:
        """Extract relevant tags from content"""
        tags = []

        # Add source type as tag
        if content.get("source_type"):
            tags.append(content["source_type"])

        # Extract equipment brands
        brands = ["Bobcat", "CAT", "Caterpillar", "John Deere", "Kubota", "Case", "Komatsu"]
        content_text = (content.get("title", "") + " " + content.get("content", "")).lower()

        for brand in brands:
            if brand.lower() in content_text:
                tags.append(brand)

        # Extract problem types
        problems = ["hydraulic", "engine", "electrical", "transmission", "steering"]
        for problem in problems:
            if problem in content_text:
                tags.append(problem)

        return list(set(tags))  # Remove duplicates

    def _extract_equipment(self, content: Dict) -> List[str]:
        """Extract equipment types from content"""
        equipment = []

        equipment_types = [
            "excavator",
            "loader",
            "bulldozer",
            "skid steer",
            "tractor",
            "backhoe",
            "forklift",
            "crane",
            "compactor",
            "grader",
        ]

        content_text = (content.get("title", "") + " " + content.get("content", "")).lower()

        for equip in equipment_types:
            if equip in content_text:
                equipment.append(equip)

        return list(set(equipment))

    def _generate_id(self, text: str) -> str:
        """Generate unique ID for content"""
        return hashlib.md5(text.encode()).hexdigest()

    def query_knowledge(self, query: str) -> List[Dict]:
        """Query the knowledge graph"""
        if not self.driver:
            return []

        try:
            with self.driver.session() as session:
                cypher_query = """
                MATCH (c:ScrapedContent)
                WHERE toLower(c.content) CONTAINS toLower($query)
                   OR toLower(c.title) CONTAINS toLower($query)
                RETURN c.title as title,
                       c.content as content,
                       c.url as url,
                       c.scraped_at as date
                ORDER BY c.scraped_at DESC
                LIMIT 10
                """

                result = session.run(cypher_query, {"query": query})

                knowledge = []
                for record in result:
                    knowledge.append(
                        {
                            "title": record["title"],
                            "content": record["content"][:500],
                            "url": record["url"],
                            "date": record["date"],
                        }
                    )

                return knowledge

        except Exception as e:
            logger.error(f"❌ Failed to query knowledge: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Get statistics about stored knowledge"""
        if not self.driver:
            return {}

        try:
            with self.driver.session() as session:
                query = """
                MATCH (c:ScrapedContent)
                RETURN COUNT(c) as total_content,
                       COUNT(DISTINCT c.source_type) as source_types,
                       MAX(c.scraped_at) as latest_scrape
                """

                result = session.run(query).single()

                if result:
                    return {
                        "total_content": result["total_content"],
                        "source_types": result["source_types"],
                        "latest_scrape": result["latest_scrape"],
                    }

        except Exception as e:
            logger.error(f"❌ Failed to get statistics: {e}")

        return {}

    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            logger.info("🔒 Neo4j connection closed")


# Integration with existing scrapers


class ScraperIntegration:
    """Integrate with existing scrapers to route data to Neo4j"""

    def __init__(self):
        self.router = ScraperNeo4jRouter()

    def process_scraped_data(self, data: Dict) -> bool:
        """Process data from any scraper and route to Neo4j"""
        # Standardize the data format
        content = {
            "url": data.get("url", ""),
            "title": data.get("title", ""),
            "content": data.get("content", data.get("text", "")),
            "source_type": data.get("type", "web"),
            "category": data.get("category", "general"),
            "metadata": {
                "source": data.get("source", "unknown"),
                "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
            },
        }

        # Route to Neo4j
        return self.router.store_scraped_content(content)

    def bulk_process(self, data_list: List[Dict]) -> Dict:
        """Process multiple scraped items"""
        results = {"total": len(data_list), "success": 0, "failed": 0}

        for data in data_list:
            if self.process_scraped_data(data):
                results["success"] += 1
            else:
                results["failed"] += 1

        logger.info(f"📊 Bulk processing complete: {results}")
        return results


def main():
    """Test the Neo4j router"""
    router = ScraperNeo4jRouter()

    # Test data
    test_content = {
        "url": "https://example.com/bobcat-repair",
        "title": "Bobcat T590 Hydraulic System Repair Guide",
        "content": (
            "Common hydraulic problems in Bobcat T590 include slow operation and leaking seals. "
            "To fix these issues..."
        ),
        "source_type": "forum",
        "category": "repair_guide",
    }

    # Store test content
    success = router.store_scraped_content(test_content)
    if success:
        logger.info("✅ Test content stored successfully")

    # Query knowledge
    results = router.query_knowledge("hydraulic")
    logger.info(f"📚 Found {len(results)} results for 'hydraulic'")

    # Get statistics
    stats = router.get_statistics()
    logger.info(f"📊 Knowledge graph statistics: {stats}")

    router.close()


if __name__ == "__main__":
    main()
