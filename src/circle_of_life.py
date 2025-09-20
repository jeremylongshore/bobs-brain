#!/usr/bin/env python3
"""
Circle of Life - Holistic ML Learning System
Integrates MVP3 diagnostic data with Bob's Brain for continuous learning
Uses Google Cloud's native frameworks for scalability and efficiency
"""

import asyncio
import hashlib
import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from google.api_core import retry
# Google Cloud imports
from google.cloud import bigquery, datastore

logger = logging.getLogger(__name__)


class CircleOfLife:
    """
    Implements the Circle of Life learning system:
    1. Ingest: Pull diagnostic data from MVP3's Datastore
    2. Learn: Extract patterns and insights
    3. Store: Warehouse knowledge in BigQuery
    4. Apply: Use learnings to enhance Bob's responses
    5. Feedback: Continuous improvement loop
    """

    def __init__(self, mvp_project="diagnostic-pro-mvp", bob_project="bobs-house-ai", batch_size=100):
        """
        Initialize Circle of Life with optimal settings for scalability
        """
        self.mvp_project = mvp_project
        self.bob_project = bob_project
        self.batch_size = batch_size

        # Initialize clients with retry policies for reliability
        self._init_clients()

        # Learning state
        self.patterns = defaultdict(int)
        self.solutions = defaultdict(list)
        self.effectiveness = {}

        logger.info("🔄 Circle of Life initialized - Ready for continuous learning")

    def _init_clients(self):
        """Initialize Google Cloud clients with optimal configurations"""
        try:
            # Datastore client for MVP3 data
            self.datastore_client = datastore.Client(project=self.mvp_project)
            logger.info(f"✅ Connected to Datastore in {self.mvp_project}")

            # BigQuery client for Bob's knowledge warehouse
            self.bq_client = bigquery.Client(project=self.bob_project)
            self._ensure_bigquery_tables()
            logger.info(f"✅ Connected to BigQuery in {self.bob_project}")

        except Exception as e:
            logger.error(f"Failed to initialize clients: {e}")
            raise

    def _ensure_bigquery_tables(self):
        """Ensure BigQuery tables exist for the Circle of Life"""
        datasets = {
            "circle_of_life": "Core learning system data",
            "diagnostic_patterns": "Learned diagnostic patterns",
            "solution_effectiveness": "Solution success metrics",
        }

        for dataset_name, description in datasets.items():
            dataset_id = f"{self.bob_project}.{dataset_name}"
            dataset = bigquery.Dataset(dataset_id)
            dataset.description = description
            dataset.location = "US"

            try:
                self.bq_client.create_dataset(dataset, exists_ok=True)
                logger.info(f"📊 BigQuery dataset ready: {dataset_name}")
            except Exception as e:
                logger.warning(f"Dataset {dataset_name} already exists or error: {e}")

        # Create tables with schemas optimized for ML
        self._create_learning_tables()

    def _create_learning_tables(self):
        """Create optimized tables for machine learning"""
        tables = {
            "diagnostic_insights": [
                bigquery.SchemaField("insight_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("problem_category", "STRING"),
                bigquery.SchemaField("problem_description", "STRING"),
                bigquery.SchemaField("equipment_type", "STRING"),
                bigquery.SchemaField("solution_provided", "STRING"),
                bigquery.SchemaField("confidence_score", "FLOAT64"),
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
                bigquery.SchemaField("source", "STRING"),
            ],
            "learning_patterns": [
                bigquery.SchemaField("pattern_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("pattern_type", "STRING"),
                bigquery.SchemaField("pattern_value", "STRING"),
                bigquery.SchemaField("frequency", "INT64"),
                bigquery.SchemaField("effectiveness", "FLOAT64"),
                bigquery.SchemaField("last_seen", "TIMESTAMP"),
                bigquery.SchemaField("metadata", "JSON"),
            ],
            "feedback_loop": [
                bigquery.SchemaField("feedback_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("original_problem", "STRING"),
                bigquery.SchemaField("suggested_solution", "STRING"),
                bigquery.SchemaField("actual_solution", "STRING"),
                bigquery.SchemaField("success", "BOOL"),
                bigquery.SchemaField("user_rating", "INT64"),
                bigquery.SchemaField("timestamp", "TIMESTAMP"),
            ],
        }

        for table_name, schema in tables.items():
            table_id = f"{self.bob_project}.circle_of_life.{table_name}"
            table = bigquery.Table(table_id, schema=schema)

            try:
                table = self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")

    @retry.Retry(deadline=30.0)
    async def ingest_diagnostic_data(self, limit=100) -> List[Dict]:
        """
        Ingest diagnostic submissions from MVP3's Datastore
        Uses efficient batch processing for scalability
        """
        insights = []

        try:
            # Query Datastore for diagnostic submissions
            query = self.datastore_client.query(kind="diagnostic_submissions")
            query.order = ["-created_at"]

            # Use cursor for efficient pagination
            results = query.fetch(limit=limit)

            for entity in results:
                # Transform Datastore entity to insight
                insight = self._transform_to_insight(entity)
                if insight:
                    insights.append(insight)

            logger.info(f"📥 Ingested {len(insights)} diagnostic insights")

            # Store in BigQuery for ML processing
            if insights:
                await self._store_insights(insights)

            return insights

        except Exception as e:
            logger.error(f"Failed to ingest diagnostic data: {e}")
            return []

    def _transform_to_insight(self, entity) -> Optional[Dict]:
        """Transform Datastore entity to learning insight"""
        try:
            # Extract key information while preserving privacy
            insight = {
                "insight_id": hashlib.md5(str(entity.key).encode()).hexdigest(),
                "problem_category": self._categorize_problem(entity.get("problem_description", "")),
                "problem_description": entity.get("problem_description", ""),
                "equipment_type": entity.get("equipment_type", "unknown"),
                "solution_provided": entity.get("ai_solution", ""),
                "confidence_score": entity.get("confidence", 0.5),
                "timestamp": entity.get("created_at", datetime.now()),
                "source": "mvp3_diagnostic",
            }
            return insight
        except Exception as e:
            logger.error(f"Failed to transform entity: {e}")
            return None

    def _categorize_problem(self, description: str) -> str:
        """Intelligent problem categorization using keywords"""
        description_lower = description.lower()

        categories = {
            "electrical": ["electrical", "battery", "alternator", "starter", "lights", "wiring"],
            "engine": ["engine", "motor", "cylinder", "piston", "valve", "timing"],
            "transmission": ["transmission", "gear", "clutch", "shifting", "automatic", "manual"],
            "brake": ["brake", "pad", "rotor", "caliper", "abs", "stopping"],
            "suspension": ["suspension", "shock", "strut", "spring", "alignment"],
            "cooling": ["cooling", "radiator", "coolant", "overheating", "thermostat"],
            "fuel": ["fuel", "gas", "pump", "injector", "tank", "filter"],
            "exhaust": ["exhaust", "muffler", "catalytic", "emission", "smoke"],
            "hvac": ["ac", "air conditioning", "heater", "climate", "defrost"],
            "body": ["body", "dent", "paint", "rust", "collision", "windshield"],
        }

        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category

        return "general"

    async def _store_insights(self, insights: List[Dict]):
        """Store insights in BigQuery with batch optimization"""
        table_id = f"{self.bob_project}.circle_of_life.diagnostic_insights"

        try:
            errors = self.bq_client.insert_rows_json(table_id, insights)
            if errors:
                logger.error(f"Failed to insert insights: {errors}")
            else:
                logger.info(f"💾 Stored {len(insights)} insights in BigQuery")
        except Exception as e:
            logger.error(f"BigQuery insert failed: {e}")

    async def learn_patterns(self) -> Dict[str, Any]:
        """
        Extract patterns from diagnostic data using BigQuery ML capabilities
        Returns learned patterns for Bob to use
        """
        patterns = {"common_problems": {}, "effective_solutions": {}, "problem_correlations": {}, "seasonal_trends": {}}

        try:
            # Query for most common problems
            common_problems_query = f"""
            SELECT
                problem_category,
                COUNT(*) as frequency,
                AVG(confidence_score) as avg_confidence
            FROM `{self.bob_project}.circle_of_life.diagnostic_insights`
            WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
            GROUP BY problem_category
            ORDER BY frequency DESC
            LIMIT 20
            """

            results = self.bq_client.query(common_problems_query).result()
            for row in results:
                patterns["common_problems"][row.problem_category] = {
                    "frequency": row.frequency,
                    "confidence": row.avg_confidence,
                }

            # Query for effective solutions
            solutions_query = f"""
            SELECT
                problem_category,
                solution_provided,
                AVG(confidence_score) as effectiveness
            FROM `{self.bob_project}.circle_of_life.diagnostic_insights`
            WHERE solution_provided IS NOT NULL
            GROUP BY problem_category, solution_provided
            HAVING effectiveness > 0.7
            ORDER BY effectiveness DESC
            """

            results = self.bq_client.query(solutions_query).result()
            for row in results:
                if row.problem_category not in patterns["effective_solutions"]:
                    patterns["effective_solutions"][row.problem_category] = []
                patterns["effective_solutions"][row.problem_category].append(
                    {
                        "solution": row.solution_provided[:200],  # Truncate for efficiency
                        "effectiveness": row.effectiveness,
                    }
                )

            # Store learned patterns
            await self._store_patterns(patterns)

            logger.info(f"🧠 Learned {len(patterns['common_problems'])} problem patterns")
            return patterns

        except Exception as e:
            logger.error(f"Pattern learning failed: {e}")
            return patterns

    async def _store_patterns(self, patterns: Dict):
        """Store learned patterns in BigQuery for persistence"""
        table_id = f"{self.bob_project}.circle_of_life.learning_patterns"

        rows = []
        for pattern_type, pattern_data in patterns.items():
            if isinstance(pattern_data, dict):
                for key, value in pattern_data.items():
                    rows.append(
                        {
                            "pattern_id": hashlib.md5(f"{pattern_type}_{key}".encode()).hexdigest(),
                            "pattern_type": pattern_type,
                            "pattern_value": key,
                            "frequency": value.get("frequency", 1) if isinstance(value, dict) else 1,
                            "effectiveness": value.get("confidence", 0.5) if isinstance(value, dict) else 0.5,
                            "last_seen": datetime.now(),
                            "metadata": (
                                json.dumps(value)
                                if isinstance(value, (dict, list))
                                else json.dumps({"value": str(value)})
                            ),
                        }
                    )

        if rows:
            errors = self.bq_client.insert_rows_json(table_id, rows)
            if not errors:
                logger.info(f"📊 Stored {len(rows)} learned patterns")

    async def apply_learning(self, problem: str) -> Dict[str, Any]:
        """
        Apply learned patterns to provide intelligent solutions
        This is where Bob gets smarter from the Circle of Life
        """
        category = self._categorize_problem(problem)

        response = {
            "category": category,
            "confidence": 0.0,
            "suggested_solutions": [],
            "similar_cases": [],
            "learning_context": {},
        }

        try:
            # Query for similar problems and their solutions
            similar_query = f"""
            SELECT
                problem_description,
                solution_provided,
                confidence_score
            FROM `{self.bob_project}.circle_of_life.diagnostic_insights`
            WHERE problem_category = @category
            AND confidence_score > 0.6
            ORDER BY confidence_score DESC
            LIMIT 5
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[bigquery.ScalarQueryParameter("category", "STRING", category)]
            )

            results = self.bq_client.query(similar_query, job_config=job_config).result()

            for row in results:
                response["similar_cases"].append(
                    {
                        "problem": row.problem_description[:100],
                        "solution": row.solution_provided[:200],
                        "confidence": row.confidence_score,
                    }
                )

                if row.solution_provided and row.solution_provided not in response["suggested_solutions"]:
                    response["suggested_solutions"].append(row.solution_provided)

            # Calculate average confidence
            if response["similar_cases"]:
                response["confidence"] = sum(case["confidence"] for case in response["similar_cases"]) / len(
                    response["similar_cases"]
                )

            # Add learning context
            response["learning_context"] = {
                "total_similar_cases": len(response["similar_cases"]),
                "category_confidence": response["confidence"],
                "data_source": "circle_of_life_ml",
            }

            logger.info(f"🎯 Applied learning: Found {len(response['similar_cases'])} similar cases")
            return response

        except Exception as e:
            logger.error(f"Failed to apply learning: {e}")
            return response

    async def feedback_loop(
        self, problem: str, suggested_solution: str, actual_solution: str, success: bool, rating: int = 0
    ):
        """
        Complete the Circle of Life with feedback
        This is how Bob learns from corrections and improves
        """
        feedback = {
            "feedback_id": hashlib.md5(f"{problem}{datetime.now()}".encode()).hexdigest(),
            "original_problem": problem[:500],
            "suggested_solution": suggested_solution[:500],
            "actual_solution": actual_solution[:500],
            "success": success,
            "user_rating": rating,
            "timestamp": datetime.now(),
        }

        try:
            table_id = f"{self.bob_project}.circle_of_life.feedback_loop"
            errors = self.bq_client.insert_rows_json(table_id, [feedback])

            if not errors:
                logger.info(f"✅ Feedback recorded: {'Success' if success else 'Learning opportunity'}")

                # If unsuccessful, trigger immediate pattern re-learning
                if not success:
                    await self.learn_patterns()
            else:
                logger.error(f"Failed to record feedback: {errors}")

        except Exception as e:
            logger.error(f"Feedback loop error: {e}")

    async def get_system_metrics(self) -> Dict[str, Any]:
        """Get Circle of Life system metrics for monitoring"""
        metrics = {
            "total_insights": 0,
            "patterns_learned": 0,
            "feedback_received": 0,
            "learning_rate": 0.0,
            "categories": {},
            "health": "healthy",
        }

        try:
            # Count total insights
            count_query = f"""
            SELECT
                COUNT(*) as total,
                COUNT(DISTINCT problem_category) as categories
            FROM `{self.bob_project}.circle_of_life.diagnostic_insights`
            """

            result = list(self.bq_client.query(count_query).result())
            if result:
                metrics["total_insights"] = result[0].total
                metrics["total_categories"] = result[0].categories

            # Count patterns
            patterns_query = f"""
            SELECT COUNT(DISTINCT pattern_id) as patterns
            FROM `{self.bob_project}.circle_of_life.learning_patterns`
            """

            result = list(self.bq_client.query(patterns_query).result())
            if result:
                metrics["patterns_learned"] = result[0].patterns

            # Calculate learning rate from feedback
            feedback_query = f"""
            SELECT
                COUNT(*) as total_feedback,
                COUNTIF(success = true) as successful
            FROM `{self.bob_project}.circle_of_life.feedback_loop`
            WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
            """

            result = list(self.bq_client.query(feedback_query).result())
            if result and result[0].total_feedback > 0:
                metrics["feedback_received"] = result[0].total_feedback
                metrics["learning_rate"] = result[0].successful / result[0].total_feedback

            logger.info(
                f"📊 System metrics: {metrics['total_insights']} insights, {metrics['patterns_learned']} patterns"
            )
            return metrics

        except Exception as e:
            logger.error(f"Failed to get metrics: {e}")
            metrics["health"] = "degraded"
            return metrics

    async def run_circle_of_life(self):
        """
        Main Circle of Life execution loop
        Runs continuously to keep Bob learning and improving
        """
        logger.info("🔄 Starting Circle of Life continuous learning loop")

        while True:
            try:
                # Step 1: Ingest new diagnostic data
                insights = await self.ingest_diagnostic_data(limit=self.batch_size)

                # Step 2: Learn patterns every 100 insights
                if len(insights) >= 10:
                    patterns = await self.learn_patterns()
                    logger.info(f"📈 Updated patterns: {len(patterns.get('common_problems', {}))} categories")

                # Step 3: Get system metrics for monitoring
                metrics = await self.get_system_metrics()

                # Log health status
                logger.info(
                    f"💚 Circle of Life Health: {metrics['health']} | "
                    f"Insights: {metrics['total_insights']} | "
                    f"Learning Rate: {metrics['learning_rate']:.2%}"
                )

                # Wait before next cycle (adjust for your needs)
                await asyncio.sleep(300)  # 5 minutes

            except Exception as e:
                logger.error(f"Circle of Life error: {e}")
                await asyncio.sleep(60)  # Wait 1 minute on error


# Singleton instance for easy import
circle_of_life = None


def get_circle_of_life() -> CircleOfLife:
    """Get or create Circle of Life instance"""
    global circle_of_life
    if circle_of_life is None:
        circle_of_life = CircleOfLife()
    return circle_of_life


if __name__ == "__main__":
    # Test the Circle of Life
    logging.basicConfig(level=logging.INFO)

    async def test():
        col = CircleOfLife()

        # Test ingestion
        insights = await col.ingest_diagnostic_data(limit=10)
        print(f"Ingested {len(insights)} insights")

        # Test learning
        patterns = await col.learn_patterns()
        print(f"Learned patterns: {patterns}")

        # Test application
        solution = await col.apply_learning("My engine is making a knocking sound")
        print(f"Suggested solution: {solution}")

        # Test metrics
        metrics = await col.get_system_metrics()
        print(f"System metrics: {metrics}")

    asyncio.run(test())
