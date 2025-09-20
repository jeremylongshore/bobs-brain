#!/usr/bin/env python3
"""
Circle of Life Scraper Integration
Automatically runs overnight to gather repair knowledge
Feeds directly into Bob's Brain learning system
Focus: Bobcat S740 and compact equipment
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from google.cloud import bigquery
try:
    from google.cloud import scheduler_v1
except ImportError:
    scheduler_v1 = None
try:
    from google.cloud import run_v2
except ImportError:
    run_v2 = None
from google.cloud.exceptions import AlreadyExists

from circle_of_life import CircleOfLife
from skidsteer_scraper import SkidSteerKnowledgeScraper
from forum_scraper import ForumIntelligenceScraper

logger = logging.getLogger(__name__)

class CircleOfLifeScraperIntegration:
    """
    Integrates web scraping with Circle of Life learning system
    Runs automatically overnight to build knowledge base
    """

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.circle_of_life = CircleOfLife()
        self.skidsteer_scraper = SkidSteerKnowledgeScraper(project_id)
        self.forum_scraper = ForumIntelligenceScraper(project_id)
        self.bq_client = bigquery.Client(project=project_id)

        # Initialize tracking tables
        self._init_tracking_tables()

        logger.info("🔄 Circle of Life Scraper Integration initialized")

    def _init_tracking_tables(self):
        """Initialize tables for tracking scraping operations"""
        dataset_id = f"{self.project_id}.circle_of_life"

        # Create scraping history table
        table_id = f"{dataset_id}.scraping_history"
        schema = [
            bigquery.SchemaField("scrape_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("scrape_type", "STRING"),  # skidsteer, forum, comprehensive
            bigquery.SchemaField("start_time", "TIMESTAMP"),
            bigquery.SchemaField("end_time", "TIMESTAMP"),
            bigquery.SchemaField("status", "STRING"),  # running, completed, failed
            bigquery.SchemaField("forums_scraped", "INT64"),
            bigquery.SchemaField("threads_scraped", "INT64"),
            bigquery.SchemaField("solutions_found", "INT64"),
            bigquery.SchemaField("s740_issues_found", "INT64"),
            bigquery.SchemaField("errors", "STRING"),
            bigquery.SchemaField("metadata", "JSON"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info("✅ Scraping history table ready")
        except Exception as e:
            logger.debug(f"Table exists or error: {e}")

    async def run_overnight_scraping(self) -> Dict:
        """
        Main overnight scraping operation
        Runs comprehensive scraping focused on Bobcat S740
        """
        logger.info("🌙 Starting overnight Circle of Life scraping operation")

        scrape_id = f"overnight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()

        # Log scraping start
        await self._log_scraping_start(scrape_id, "comprehensive", start_time)

        results = {
            "scrape_id": scrape_id,
            "start_time": start_time.isoformat(),
            "phases_completed": [],
            "total_data_collected": 0,
            "errors": []
        }

        try:
            # Phase 1: Scrape Bobcat S740 specific content
            logger.info("🚜 Phase 1: Scraping Bobcat S740 and skid steer forums...")
            skidsteer_results = await self.skidsteer_scraper.scrape_skidsteer_forums()
            results["skidsteer_scraping"] = skidsteer_results
            results["phases_completed"].append("skidsteer")

            # Process S740 data into Circle of Life
            await self._process_s740_into_learning(skidsteer_results)

            # Phase 2: Scrape general repair forums
            logger.info("🔧 Phase 2: Scraping general repair forums...")
            forum_search_queries = [
                "Bobcat S740 problems",
                "skid steer repair forum",
                "compact equipment maintenance",
                "Bobcat error codes",
                "hydraulic troubleshooting skid steer",
                "DPF regeneration Bobcat",
                "loader attachment problems"
            ]

            forum_results = await self.forum_scraper.run_comprehensive_scrape(forum_search_queries)
            results["forum_scraping"] = forum_results
            results["phases_completed"].append("forums")

            # Phase 3: Extract patterns and learn
            logger.info("🧠 Phase 3: Extracting patterns and learning...")
            learning_results = await self._extract_and_learn_patterns()
            results["learning"] = learning_results
            results["phases_completed"].append("learning")

            # Phase 4: Update Bob's knowledge base
            logger.info("📚 Phase 4: Updating Bob's knowledge base...")
            await self._update_bobs_knowledge()
            results["phases_completed"].append("knowledge_update")

            # Phase 5: Generate daily insights report
            logger.info("📊 Phase 5: Generating insights report...")
            insights = await self._generate_daily_insights()
            results["daily_insights"] = insights
            results["phases_completed"].append("insights")

            # Calculate totals
            results["total_data_collected"] = (
                skidsteer_results.get("issues_found", 0) +
                skidsteer_results.get("hacks_found", 0) +
                forum_results.get("threads_scraped", 0)
            )

            results["status"] = "completed"
            results["end_time"] = datetime.now().isoformat()

            # Log successful completion
            await self._log_scraping_complete(scrape_id, results)

            logger.info(f"""
            ✅ Overnight Scraping Complete!
            ==============================
            Scrape ID: {scrape_id}
            Duration: {(datetime.now() - start_time).total_seconds() / 60:.1f} minutes
            Total Data Collected: {results['total_data_collected']}
            Phases Completed: {', '.join(results['phases_completed'])}

            Bobcat S740 Issues Found: {skidsteer_results.get('issues_found', 0)}
            Equipment Hacks Found: {skidsteer_results.get('hacks_found', 0)}
            Forums Scraped: {forum_results.get('forums_discovered', 0)}
            Threads Analyzed: {forum_results.get('threads_scraped', 0)}
            """)

        except Exception as e:
            logger.error(f"Overnight scraping failed: {e}")
            results["status"] = "failed"
            results["errors"].append(str(e))
            await self._log_scraping_error(scrape_id, str(e))

        return results

    async def _process_s740_into_learning(self, skidsteer_results: Dict):
        """Process Bobcat S740 data into Circle of Life learning system"""
        try:
            # Query newly scraped S740 issues
            query = f"""
            SELECT
                problem_type,
                problem_description,
                solution,
                parts_needed,
                error_codes,
                difficulty
            FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
            WHERE DATE(scraped_at) = CURRENT_DATE()
            """

            results = self.bq_client.query(query).result()

            for row in results:
                # Create learning insight
                insight = {
                    "insight_id": f"s740_{datetime.now().timestamp()}",
                    "problem_category": row.problem_type,
                    "problem_description": row.problem_description,
                    "equipment_type": "Bobcat S740",
                    "solution_provided": row.solution,
                    "confidence_score": 0.85,  # High confidence for specific model data
                    "timestamp": datetime.now(),
                    "source": "skidsteer_scraper"
                }

                # Store in Circle of Life diagnostic insights
                table_id = f"{self.project_id}.circle_of_life.diagnostic_insights"
                errors = self.bq_client.insert_rows_json(table_id, [insight])

                if not errors:
                    logger.debug(f"✅ Processed S740 issue into learning: {row.problem_type}")

                # Extract patterns
                if row.error_codes:
                    for code in row.error_codes:
                        await self._record_error_code_pattern(code, row.problem_type, row.solution)

                # Record parts patterns
                if row.parts_needed:
                    for part in row.parts_needed:
                        await self._record_parts_pattern(part, row.problem_type)

        except Exception as e:
            logger.error(f"Failed to process S740 data: {e}")

    async def _extract_and_learn_patterns(self) -> Dict:
        """Extract patterns from scraped data and learn"""
        patterns_found = {
            "problem_patterns": 0,
            "solution_patterns": 0,
            "equipment_patterns": 0,
            "seasonal_patterns": 0
        }

        try:
            # Analyze problem frequency patterns
            query = f"""
            WITH problem_frequency AS (
                SELECT
                    problem_category,
                    COUNT(*) as frequency,
                    AVG(confidence_score) as avg_confidence
                FROM `{self.project_id}.circle_of_life.diagnostic_insights`
                WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
                GROUP BY problem_category
                HAVING COUNT(*) > 5
            )
            SELECT * FROM problem_frequency
            ORDER BY frequency DESC
            """

            results = self.bq_client.query(query).result()

            for row in results:
                # Store pattern in learning_patterns table
                pattern = {
                    "pattern_id": f"prob_freq_{row.problem_category}_{datetime.now().timestamp()}",
                    "pattern_type": "problem_frequency",
                    "pattern_value": row.problem_category,
                    "frequency": row.frequency,
                    "effectiveness": float(row.avg_confidence),
                    "last_seen": datetime.now(),
                    "metadata": {"category": row.problem_category}
                }

                table_id = f"{self.project_id}.circle_of_life.learning_patterns"
                self.bq_client.insert_rows_json(table_id, [pattern])
                patterns_found["problem_patterns"] += 1

            # Analyze solution effectiveness patterns
            query = f"""
            SELECT
                solution,
                COUNT(*) as usage_count,
                AVG(CASE WHEN verified THEN 1 ELSE 0 END) as success_rate
            FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
            WHERE solution IS NOT NULL AND solution != ''
            GROUP BY solution
            HAVING COUNT(*) > 3
            """

            results = self.bq_client.query(query).result()

            for row in results:
                pattern = {
                    "pattern_id": f"sol_eff_{datetime.now().timestamp()}",
                    "pattern_type": "solution_effectiveness",
                    "pattern_value": row.solution[:500],  # Truncate long solutions
                    "frequency": row.usage_count,
                    "effectiveness": float(row.success_rate),
                    "last_seen": datetime.now(),
                    "metadata": {"usage_count": row.usage_count}
                }

                table_id = f"{self.project_id}.circle_of_life.learning_patterns"
                self.bq_client.insert_rows_json(table_id, [pattern])
                patterns_found["solution_patterns"] += 1

            logger.info(f"📊 Extracted patterns: {patterns_found}")

        except Exception as e:
            logger.error(f"Failed to extract patterns: {e}")

        return patterns_found

    async def _record_error_code_pattern(self, code: str, problem_type: str, solution: str):
        """Record error code pattern for learning"""
        try:
            pattern = {
                "pattern_id": f"error_{code}_{datetime.now().timestamp()}",
                "pattern_type": "error_code",
                "pattern_value": f"{code}: {problem_type}",
                "frequency": 1,
                "effectiveness": 0.7,
                "last_seen": datetime.now(),
                "metadata": {
                    "error_code": code,
                    "problem_type": problem_type,
                    "solution_preview": solution[:200] if solution else ""
                }
            }

            table_id = f"{self.project_id}.circle_of_life.learning_patterns"
            self.bq_client.insert_rows_json(table_id, [pattern])

        except Exception as e:
            logger.debug(f"Failed to record error code pattern: {e}")

    async def _record_parts_pattern(self, part: str, problem_type: str):
        """Record parts usage pattern"""
        try:
            pattern = {
                "pattern_id": f"part_{part}_{datetime.now().timestamp()}",
                "pattern_type": "parts_usage",
                "pattern_value": f"{part} for {problem_type}",
                "frequency": 1,
                "effectiveness": 0.6,
                "last_seen": datetime.now(),
                "metadata": {
                    "part": part,
                    "problem_type": problem_type
                }
            }

            table_id = f"{self.project_id}.circle_of_life.learning_patterns"
            self.bq_client.insert_rows_json(table_id, [pattern])

        except Exception as e:
            logger.debug(f"Failed to record parts pattern: {e}")

    async def _update_bobs_knowledge(self):
        """Update Bob's knowledge base with new scraped data"""
        try:
            # Create knowledge summary for Bob
            query = f"""
            WITH latest_knowledge AS (
                SELECT
                    'S740_ISSUE' as knowledge_type,
                    problem_type as category,
                    problem_description as content,
                    solution as answer,
                    ARRAY_TO_STRING(parts_needed, ', ') as parts,
                    difficulty,
                    source_url
                FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
                WHERE DATE(scraped_at) = CURRENT_DATE()

                UNION ALL

                SELECT
                    'EQUIPMENT_HACK' as knowledge_type,
                    hack_type as category,
                    description as content,
                    benefits as answer,
                    ARRAY_TO_STRING(tools_needed, ', ') as parts,
                    'moderate' as difficulty,
                    source_url
                FROM `{self.project_id}.skidsteer_knowledge.equipment_hacks`
                WHERE DATE(scraped_at) = CURRENT_DATE()
            )
            INSERT INTO `{self.project_id}.knowledge_base.bob_knowledge`
            (knowledge_id, knowledge_type, category, content, answer, metadata, created_at, source)
            SELECT
                GENERATE_UUID() as knowledge_id,
                knowledge_type,
                category,
                content,
                answer,
                TO_JSON_STRING(STRUCT(parts as parts, difficulty as difficulty)) as metadata,
                CURRENT_TIMESTAMP() as created_at,
                source_url as source
            FROM latest_knowledge
            """

            # First ensure the knowledge base table exists
            self._ensure_knowledge_base_table()

            # Execute the knowledge update
            job = self.bq_client.query(query)
            job.result()  # Wait for completion

            logger.info("✅ Updated Bob's knowledge base with new scraped data")

        except Exception as e:
            logger.error(f"Failed to update Bob's knowledge: {e}")

    def _ensure_knowledge_base_table(self):
        """Ensure Bob's knowledge base table exists"""
        dataset_id = f"{self.project_id}.knowledge_base"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except:
            pass

        table_id = f"{dataset_id}.bob_knowledge"
        schema = [
            bigquery.SchemaField("knowledge_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("knowledge_type", "STRING"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("answer", "STRING"),
            bigquery.SchemaField("metadata", "STRING"),  # JSON string
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("source", "STRING"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        try:
            self.bq_client.create_table(table, exists_ok=True)
        except:
            pass

    async def _generate_daily_insights(self) -> Dict:
        """Generate daily insights from scraping"""
        insights = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "top_problems": [],
            "new_solutions": 0,
            "equipment_focus": "Bobcat S740",
            "recommendations": []
        }

        try:
            # Get top problems found today
            query = f"""
            SELECT
                problem_type,
                COUNT(*) as count
            FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
            WHERE DATE(scraped_at) = CURRENT_DATE()
            GROUP BY problem_type
            ORDER BY count DESC
            LIMIT 5
            """

            results = self.bq_client.query(query).result()

            for row in results:
                insights["top_problems"].append({
                    "type": row.problem_type,
                    "occurrences": row.count
                })

            # Count new solutions
            query = f"""
            SELECT COUNT(DISTINCT solution) as new_solutions
            FROM `{self.project_id}.skidsteer_knowledge.bobcat_s740_issues`
            WHERE DATE(scraped_at) = CURRENT_DATE()
            AND solution IS NOT NULL AND solution != ''
            """

            result = list(self.bq_client.query(query).result())[0]
            insights["new_solutions"] = result.new_solutions

            # Generate recommendations
            if insights["top_problems"]:
                top_problem = insights["top_problems"][0]["type"]
                insights["recommendations"].append(
                    f"Focus on {top_problem} issues - high frequency detected"
                )

            insights["recommendations"].append(
                f"Added {insights['new_solutions']} new solutions to knowledge base"
            )

            logger.info(f"📊 Generated daily insights: {insights}")

        except Exception as e:
            logger.error(f"Failed to generate insights: {e}")

        return insights

    async def _log_scraping_start(self, scrape_id: str, scrape_type: str, start_time: datetime):
        """Log scraping operation start"""
        try:
            record = {
                "scrape_id": scrape_id,
                "scrape_type": scrape_type,
                "start_time": start_time,
                "status": "running",
                "metadata": {"initiated_by": "scheduled"}
            }

            table_id = f"{self.project_id}.circle_of_life.scraping_history"
            self.bq_client.insert_rows_json(table_id, [record])

        except Exception as e:
            logger.error(f"Failed to log scraping start: {e}")

    async def _log_scraping_complete(self, scrape_id: str, results: Dict):
        """Log scraping operation completion"""
        try:
            # Update the scraping history record
            query = f"""
            UPDATE `{self.project_id}.circle_of_life.scraping_history`
            SET
                end_time = CURRENT_TIMESTAMP(),
                status = 'completed',
                forums_scraped = {results.get('forum_scraping', {}).get('forums_discovered', 0)},
                threads_scraped = {results.get('forum_scraping', {}).get('threads_scraped', 0)},
                solutions_found = {results.get('skidsteer_scraping', {}).get('solutions_found', 0)},
                s740_issues_found = {results.get('skidsteer_scraping', {}).get('issues_found', 0)},
                metadata = PARSE_JSON('{json.dumps({"phases": results.get("phases_completed", [])})}')
            WHERE scrape_id = '{scrape_id}'
            """

            self.bq_client.query(query).result()

        except Exception as e:
            logger.error(f"Failed to log scraping completion: {e}")

    async def _log_scraping_error(self, scrape_id: str, error: str):
        """Log scraping operation error"""
        try:
            query = f"""
            UPDATE `{self.project_id}.circle_of_life.scraping_history`
            SET
                end_time = CURRENT_TIMESTAMP(),
                status = 'failed',
                errors = '{error}'
            WHERE scrape_id = '{scrape_id}'
            """

            self.bq_client.query(query).result()

        except Exception as e:
            logger.error(f"Failed to log scraping error: {e}")

    def setup_cloud_scheduler(self):
        """Set up Cloud Scheduler to run scraping overnight"""
        if not scheduler_v1:
            logger.warning("Cloud Scheduler module not available - skipping scheduler setup")
            return

        try:
            scheduler_client = scheduler_v1.CloudSchedulerClient()
            parent = f"projects/{self.project_id}/locations/us-central1"

            job = scheduler_v1.Job(
                name=f"{parent}/jobs/circle-of-life-scraper",
                description="Overnight scraping for Bobcat S740 and equipment knowledge",
                schedule="0 2 * * *",  # Run at 2 AM every day
                time_zone="America/Chicago",
                http_target=scheduler_v1.HttpTarget(
                    uri=f"https://circle-of-life-scraper-{self.project_id}.a.run.app/scrape",
                    http_method=scheduler_v1.HttpMethod.POST,
                    headers={"Content-Type": "application/json"},
                    body=json.dumps({"scrape_type": "overnight"}).encode(),
                    oidc_token=scheduler_v1.OidcToken(
                        service_account_email=f"circle-of-life@{self.project_id}.iam.gserviceaccount.com"
                    )
                )
            )

            try:
                response = scheduler_client.create_job(parent=parent, job=job)
                logger.info(f"✅ Cloud Scheduler job created: {response.name}")
            except AlreadyExists:
                logger.info("Cloud Scheduler job already exists")

        except Exception as e:
            logger.error(f"Failed to set up Cloud Scheduler: {e}")

async def main():
    """Main function for testing Circle of Life scraper"""
    integration = CircleOfLifeScraperIntegration()

    # Run overnight scraping
    results = await integration.run_overnight_scraping()

    print(json.dumps(results, indent=2, default=str))

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(main())