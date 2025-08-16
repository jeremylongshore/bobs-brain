#!/usr/bin/env python3
"""
Neo4j Aura and BigQuery Bidirectional Sync
Integrates all datasets between Neo4j knowledge graph and BigQuery warehouse
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

from google.cloud import bigquery
from neo4j import GraphDatabase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Neo4jBigQuerySync:
    """Synchronize data between Neo4j Aura and BigQuery"""

    def __init__(self):
        # Neo4j Aura connection
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE")

        # BigQuery connection
        self.project_id = os.getenv("PROJECT_ID", "bobs-house-ai")
        self.bq_client = bigquery.Client(project=self.project_id)

        # Initialize drivers
        self.neo4j_driver = None
        self._connect_neo4j()

        logger.info("Neo4j-BigQuery sync initialized")

    def _connect_neo4j(self):
        """Connect to Neo4j Aura"""
        try:
            self.neo4j_driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password),
                connection_timeout=30,
                max_connection_lifetime=3600,
            )

            # Verify connection
            with self.neo4j_driver.session() as session:
                result = session.run("RETURN 1 as test")
                if result.single()["test"] == 1:
                    logger.info("✅ Connected to Neo4j Aura")

        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            raise

    def sync_customer_submissions_to_neo4j(self):
        """Sync customer submissions from BigQuery to Neo4j"""

        logger.info("Starting customer submissions sync to Neo4j...")

        # Query BigQuery for recent submissions
        query = f"""
        SELECT
            submission_id,
            customer_email,
            customer_name,
            customer_company,
            equipment_type,
            equipment_brand,
            equipment_model,
            problem_description,
            problem_category,
            ai_analysis,
            confidence_score,
            created_at
        FROM `{self.project_id}.customer_submissions.diagnostics`
        WHERE DATE(created_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        ORDER BY created_at DESC
        LIMIT 1000
        """

        results = self.bq_client.query(query)

        with self.neo4j_driver.session() as session:
            for row in results:
                # Create customer node
                session.run(
                    """
                    MERGE (c:Customer {email: $email})
                    SET c.name = $name,
                        c.company = $company,
                        c.last_submission = datetime($created_at)
                """,
                    email=row.customer_email,
                    name=row.customer_name,
                    company=row.customer_company,
                    created_at=str(row.created_at),
                )

                # Create equipment node
                session.run(
                    """
                    MERGE (e:Equipment {
                        type: $type,
                        brand: $brand,
                        model: $model
                    })
                    SET e.last_reported = datetime($created_at)
                """,
                    type=row.equipment_type,
                    brand=row.equipment_brand,
                    model=row.equipment_model,
                    created_at=str(row.created_at),
                )

                # Create diagnostic submission node
                session.run(
                    """
                    CREATE (d:Diagnostic {
                        id: $submission_id,
                        description: $description,
                        category: $category,
                        ai_analysis: $ai_analysis,
                        confidence: $confidence,
                        created_at: datetime($created_at)
                    })
                """,
                    submission_id=row.submission_id,
                    description=row.problem_description,
                    category=row.problem_category,
                    ai_analysis=row.ai_analysis,
                    confidence=row.confidence_score,
                    created_at=str(row.created_at),
                )

                # Create relationships
                session.run(
                    """
                    MATCH (c:Customer {email: $email})
                    MATCH (d:Diagnostic {id: $submission_id})
                    MATCH (e:Equipment {type: $equipment_type})
                    CREATE (c)-[:SUBMITTED]->(d)
                    CREATE (d)-[:ABOUT]->(e)
                """,
                    email=row.customer_email,
                    submission_id=row.submission_id,
                    equipment_type=row.equipment_type,
                )

                # Update BigQuery with Neo4j node ID
                self._update_neo4j_reference(row.submission_id, f"diagnostic:{row.submission_id}")

        logger.info("✅ Customer submissions synced to Neo4j")

    def sync_scraped_data_to_neo4j(self):
        """Sync scraped knowledge to Neo4j"""

        logger.info("Starting scraped data sync to Neo4j...")

        # Query BigQuery for scraped content
        query = f"""
        SELECT
            source,
            title,
            content,
            url,
            scraped_at,
            metadata
        FROM `{self.project_id}.scraped_data.unified_content`
        WHERE DATE(scraped_at) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
        LIMIT 500
        """

        results = self.bq_client.query(query)

        with self.neo4j_driver.session() as session:
            for row in results:
                # Create knowledge node
                session.run(
                    """
                    MERGE (k:Knowledge {url: $url})
                    SET k.title = $title,
                        k.content = $content,
                        k.source = $source,
                        k.scraped_at = datetime($scraped_at),
                        k.metadata = $metadata
                """,
                    url=row.url,
                    title=row.title,
                    content=row.content[:1000],  # Truncate for performance
                    source=row.source,
                    scraped_at=str(row.scraped_at),
                    metadata=json.dumps(dict(row.metadata)) if row.metadata else "{}",
                )

                # Extract and link equipment mentions
                if row.content:
                    equipment_types = self._extract_equipment_mentions(row.content)
                    for equipment in equipment_types:
                        session.run(
                            """
                            MATCH (k:Knowledge {url: $url})
                            MERGE (e:Equipment {type: $equipment})
                            MERGE (k)-[:MENTIONS]->(e)
                        """,
                            url=row.url,
                            equipment=equipment,
                        )

        logger.info("✅ Scraped data synced to Neo4j")

    def sync_conversations_to_neo4j(self):
        """Sync Bob's conversations to Neo4j"""

        logger.info("Starting conversations sync to Neo4j...")

        query = f"""
        SELECT
            conversation_id,
            user_message,
            bob_response,
            user_name,
            channel,
            timestamp
        FROM `{self.project_id}.conversations.history`
        WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY)
        ORDER BY timestamp DESC
        LIMIT 500
        """

        results = self.bq_client.query(query)

        with self.neo4j_driver.session() as session:
            for row in results:
                # Create conversation node
                session.run(
                    """
                    CREATE (c:Conversation {
                        id: $conversation_id,
                        user_message: $user_message,
                        bob_response: $bob_response,
                        user: $user_name,
                        channel: $channel,
                        timestamp: datetime($timestamp)
                    })
                """,
                    conversation_id=row.conversation_id,
                    user_message=row.user_message,
                    bob_response=row.bob_response,
                    user_name=row.user_name,
                    channel=row.channel,
                    timestamp=str(row.timestamp),
                )

                # Extract entities and create relationships
                entities = self._extract_entities(row.user_message)
                for entity_type, entity_value in entities:
                    session.run(
                        """
                        MATCH (c:Conversation {id: $conversation_id})
                        MERGE (e:Entity {value: $value, type: $type})
                        MERGE (c)-[:CONTAINS]->(e)
                    """,
                        conversation_id=row.conversation_id,
                        value=entity_value,
                        type=entity_type,
                    )

        logger.info("✅ Conversations synced to Neo4j")

    def sync_neo4j_patterns_to_bigquery(self):
        """Extract patterns from Neo4j and store in BigQuery"""

        logger.info("Extracting patterns from Neo4j...")

        patterns = []

        with self.neo4j_driver.session() as session:
            # Find common problem patterns
            result = session.run(
                """
                MATCH (d:Diagnostic)-[:ABOUT]->(e:Equipment)
                WITH e.type as equipment, d.category as problem, COUNT(*) as frequency
                WHERE frequency > 2
                RETURN equipment, problem, frequency
                ORDER BY frequency DESC
                LIMIT 100
            """
            )

            for record in result:
                patterns.append(
                    {
                        "pattern_type": "equipment_problem",
                        "equipment": record["equipment"],
                        "problem": record["problem"],
                        "frequency": record["frequency"],
                        "extracted_at": datetime.now().isoformat(),
                    }
                )

            # Find customer patterns
            result = session.run(
                """
                MATCH (c:Customer)-[:SUBMITTED]->(d:Diagnostic)
                WITH c.company as company, COUNT(DISTINCT d) as submission_count
                WHERE submission_count > 5
                RETURN company, submission_count
                ORDER BY submission_count DESC
                LIMIT 50
            """
            )

            for record in result:
                patterns.append(
                    {
                        "pattern_type": "frequent_customer",
                        "company": record["company"],
                        "submission_count": record["submission_count"],
                        "extracted_at": datetime.now().isoformat(),
                    }
                )

            # Find solution effectiveness patterns
            result = session.run(
                """
                MATCH (d:Diagnostic)
                WHERE d.confidence > 0.8
                WITH d.category as category, AVG(d.confidence) as avg_confidence, COUNT(*) as count
                RETURN category, avg_confidence, count
                ORDER BY avg_confidence DESC
            """
            )

            for record in result:
                patterns.append(
                    {
                        "pattern_type": "high_confidence_category",
                        "category": record["category"],
                        "avg_confidence": record["avg_confidence"],
                        "count": record["count"],
                        "extracted_at": datetime.now().isoformat(),
                    }
                )

        # Store patterns in BigQuery
        if patterns:
            table_id = f"{self.project_id}.diagnostic_patterns.neo4j_patterns"
            errors = self.bq_client.insert_rows_json(table_id, patterns)

            if errors:
                logger.error(f"BigQuery insert errors: {errors}")
            else:
                logger.info(f"✅ Stored {len(patterns)} patterns in BigQuery")

        return patterns

    def create_knowledge_graph_views(self):
        """Create BigQuery views of Neo4j knowledge graph"""

        logger.info("Creating knowledge graph views...")

        # Equipment relationships view
        equipment_view = f"""
        CREATE OR REPLACE VIEW `{self.project_id}.knowledge_graph.equipment_relationships` AS
        WITH equipment_data AS (
            SELECT DISTINCT
                equipment_type,
                equipment_brand,
                equipment_model,
                problem_category,
                COUNT(*) as problem_count
            FROM `{self.project_id}.customer_submissions.diagnostics`
            GROUP BY equipment_type, equipment_brand, equipment_model, problem_category
        )
        SELECT
            equipment_type,
            equipment_brand,
            equipment_model,
            ARRAY_AGG(
                STRUCT(problem_category, problem_count)
                ORDER BY problem_count DESC
            ) as common_problems
        FROM equipment_data
        GROUP BY equipment_type, equipment_brand, equipment_model
        """

        self.bq_client.query(equipment_view).result()

        # Customer journey view
        customer_view = f"""
        CREATE OR REPLACE VIEW `{self.project_id}.knowledge_graph.customer_journey` AS
        SELECT
            customer_email,
            customer_company,
            COUNT(DISTINCT submission_id) as total_submissions,
            ARRAY_AGG(DISTINCT equipment_type IGNORE NULLS) as equipment_types,
            ARRAY_AGG(DISTINCT problem_category IGNORE NULLS) as problem_categories,
            AVG(confidence_score) as avg_confidence,
            MIN(created_at) as first_submission,
            MAX(created_at) as last_submission
        FROM `{self.project_id}.customer_submissions.diagnostics`
        GROUP BY customer_email, customer_company
        """

        self.bq_client.query(customer_view).result()

        logger.info("✅ Knowledge graph views created")

    def _extract_equipment_mentions(self, text: str) -> List[str]:
        """Extract equipment mentions from text"""

        equipment_keywords = [
            "excavator",
            "loader",
            "dozer",
            "grader",
            "skid steer",
            "bobcat",
            "caterpillar",
            "john deere",
            "kubota",
            "case",
            "volvo",
            "komatsu",
            "hitachi",
            "jcb",
            "new holland",
        ]

        text_lower = text.lower()
        mentions = []

        for keyword in equipment_keywords:
            if keyword in text_lower:
                mentions.append(keyword.title())

        return mentions

    def _extract_entities(self, text: str) -> List[tuple]:
        """Extract entities from text"""

        entities = []

        # Extract error codes (pattern: letter(s)-numbers)
        import re

        error_pattern = r"\b[A-Z]{1,4}[-]?\d{3,5}\b"
        errors = re.findall(error_pattern, text.upper())
        for error in errors:
            entities.append(("ErrorCode", error))

        # Extract equipment mentions
        equipment = self._extract_equipment_mentions(text)
        for equip in equipment:
            entities.append(("Equipment", equip))

        return entities

    def _update_neo4j_reference(self, submission_id: str, neo4j_node_id: str):
        """Update BigQuery with Neo4j node reference"""

        query = f"""
        UPDATE `{self.project_id}.customer_submissions.diagnostics`
        SET neo4j_node_id = @neo4j_node_id
        WHERE submission_id = @submission_id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("neo4j_node_id", "STRING", neo4j_node_id),
                bigquery.ScalarQueryParameter("submission_id", "STRING", submission_id),
            ]
        )

        self.bq_client.query(query, job_config=job_config).result()

    def run_full_sync(self):
        """Run complete bidirectional sync"""

        logger.info("=" * 60)
        logger.info("🔄 STARTING NEO4J-BIGQUERY FULL SYNC")
        logger.info("=" * 60)

        try:
            # BigQuery → Neo4j
            self.sync_customer_submissions_to_neo4j()
            self.sync_scraped_data_to_neo4j()
            self.sync_conversations_to_neo4j()

            # Neo4j → BigQuery
            patterns = self.sync_neo4j_patterns_to_bigquery()

            # Create views
            self.create_knowledge_graph_views()

            # Get statistics
            with self.neo4j_driver.session() as session:
                result = session.run(
                    """
                    MATCH (n)
                    RETURN
                        COUNT(DISTINCT CASE WHEN 'Customer' IN labels(n) THEN n END) as customers,
                        COUNT(DISTINCT CASE WHEN 'Equipment' IN labels(n) THEN n END) as equipment,
                        COUNT(DISTINCT CASE WHEN 'Diagnostic' IN labels(n) THEN n END) as diagnostics,
                        COUNT(DISTINCT CASE WHEN 'Knowledge' IN labels(n) THEN n END) as knowledge,
                        COUNT(DISTINCT CASE WHEN 'Conversation' IN labels(n) THEN n END) as conversations
                """
                )

                stats = result.single()

                logger.info("=" * 60)
                logger.info("✅ SYNC COMPLETE")
                logger.info("=" * 60)
                logger.info(f"Neo4j Statistics:")
                logger.info(f"  Customers: {stats['customers']}")
                logger.info(f"  Equipment: {stats['equipment']}")
                logger.info(f"  Diagnostics: {stats['diagnostics']}")
                logger.info(f"  Knowledge: {stats['knowledge']}")
                logger.info(f"  Conversations: {stats['conversations']}")
                logger.info(f"  Patterns extracted: {len(patterns)}")

        except Exception as e:
            logger.error(f"Sync failed: {e}")
            raise

        finally:
            if self.neo4j_driver:
                self.neo4j_driver.close()

    def setup_scheduled_sync(self):
        """Setup Cloud Scheduler for automated sync"""

        print(
            """
To setup automated sync, run:

gcloud scheduler jobs create http neo4j-bigquery-sync \\
    --location us-central1 \\
    --schedule "0 */4 * * *" \\
    --uri "https://bobs-brain-sytrh5wz5q-uc.a.run.app/sync/neo4j-bigquery" \\
    --http-method POST \\
    --oidc-service-account-email bobs-brain@bobs-house-ai.iam.gserviceaccount.com
        """
        )


if __name__ == "__main__":
    sync = Neo4jBigQuerySync()
    sync.run_full_sync()
