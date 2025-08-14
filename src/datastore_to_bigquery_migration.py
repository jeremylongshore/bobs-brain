#!/usr/bin/env python3
"""
Datastore to BigQuery Migration with Enhanced Schema
Migrates MVP3 diagnostic data from Datastore to BigQuery with room for growth
"""

import hashlib
import json
import logging
from datetime import datetime
from typing import Any, Dict, List

from google.cloud import bigquery, datastore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatastoreToBigQueryMigration:
    """Migrate Datastore to BigQuery with enhanced schema for future growth"""

    def __init__(self, source_project="diagnostic-pro-mvp", target_project="bobs-house-ai"):
        self.source_project = source_project
        self.target_project = target_project

        # Initialize clients
        self.datastore_client = datastore.Client(project=source_project)
        self.bq_client = bigquery.Client(project=target_project)

        logger.info(f"Migration configured: {source_project} -> {target_project}")

    def create_enhanced_schema(self):
        """Create BigQuery schema with room for growth including customer web intake"""

        # Enhanced diagnostic schema with customer website data fields
        diagnostic_schema = [
            # Core fields from Datastore
            bigquery.SchemaField("diagnostic_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
            # Equipment information (expanded)
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("equipment_brand", "STRING"),
            bigquery.SchemaField("equipment_model", "STRING"),
            bigquery.SchemaField("equipment_year", "INTEGER"),
            bigquery.SchemaField("equipment_serial", "STRING"),
            bigquery.SchemaField("equipment_hours", "INTEGER"),
            bigquery.SchemaField("equipment_location", "STRING"),
            bigquery.SchemaField("equipment_condition", "STRING"),
            bigquery.SchemaField("equipment_value", "FLOAT64"),
            bigquery.SchemaField("equipment_images", "STRING", mode="REPEATED"),
            bigquery.SchemaField("equipment_videos", "STRING", mode="REPEATED"),
            # Problem details (expanded)
            bigquery.SchemaField("problem_category", "STRING"),
            bigquery.SchemaField("problem_subcategory", "STRING"),
            bigquery.SchemaField("problem_description", "STRING"),
            bigquery.SchemaField("problem_severity", "STRING"),
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("symptoms", "STRING", mode="REPEATED"),
            bigquery.SchemaField("problem_started_date", "DATE"),
            bigquery.SchemaField("problem_frequency", "STRING"),
            bigquery.SchemaField("previous_repairs", "JSON"),
            # Solution information (expanded)
            bigquery.SchemaField("solution_provided", "STRING"),
            bigquery.SchemaField("solution_steps", "JSON"),
            bigquery.SchemaField("parts_required", "JSON"),
            bigquery.SchemaField("tools_required", "STRING", mode="REPEATED"),
            bigquery.SchemaField("estimated_time", "FLOAT64"),
            bigquery.SchemaField("estimated_cost", "FLOAT64"),
            bigquery.SchemaField("actual_time", "FLOAT64"),
            bigquery.SchemaField("actual_cost", "FLOAT64"),
            bigquery.SchemaField("warranty_coverage", "BOOLEAN"),
            # Customer information (website intake)
            bigquery.SchemaField("customer_id", "STRING"),
            bigquery.SchemaField("customer_email", "STRING"),
            bigquery.SchemaField("customer_phone", "STRING"),
            bigquery.SchemaField("customer_name", "STRING"),
            bigquery.SchemaField("customer_company", "STRING"),
            bigquery.SchemaField("customer_type", "STRING"),  # individual, business, fleet
            bigquery.SchemaField("customer_location_city", "STRING"),
            bigquery.SchemaField("customer_location_state", "STRING"),
            bigquery.SchemaField("customer_location_country", "STRING"),
            bigquery.SchemaField("customer_location_zip", "STRING"),
            bigquery.SchemaField("customer_preferred_contact", "STRING"),
            bigquery.SchemaField("customer_language", "STRING"),
            bigquery.SchemaField("customer_timezone", "STRING"),
            # Business/Fleet customer fields
            bigquery.SchemaField("fleet_size", "INTEGER"),
            bigquery.SchemaField("industry_type", "STRING"),
            bigquery.SchemaField("annual_revenue", "STRING"),
            bigquery.SchemaField("employee_count", "STRING"),
            bigquery.SchemaField("service_contract", "BOOLEAN"),
            bigquery.SchemaField("account_manager", "STRING"),
            # Website interaction data
            bigquery.SchemaField("session_id", "STRING"),
            bigquery.SchemaField("ip_address", "STRING"),
            bigquery.SchemaField("user_agent", "STRING"),
            bigquery.SchemaField("referrer_source", "STRING"),
            bigquery.SchemaField("landing_page", "STRING"),
            bigquery.SchemaField("pages_visited", "STRING", mode="REPEATED"),
            bigquery.SchemaField("time_on_site", "INTEGER"),
            bigquery.SchemaField("form_completion_time", "INTEGER"),
            bigquery.SchemaField("abandoned_form", "BOOLEAN"),
            bigquery.SchemaField("utm_source", "STRING"),
            bigquery.SchemaField("utm_medium", "STRING"),
            bigquery.SchemaField("utm_campaign", "STRING"),
            # Communication preferences
            bigquery.SchemaField("opt_in_email", "BOOLEAN"),
            bigquery.SchemaField("opt_in_sms", "BOOLEAN"),
            bigquery.SchemaField("opt_in_phone", "BOOLEAN"),
            bigquery.SchemaField("opt_in_marketing", "BOOLEAN"),
            bigquery.SchemaField("communication_frequency", "STRING"),
            # Service request details
            bigquery.SchemaField("service_type", "STRING"),  # repair, maintenance, consultation
            bigquery.SchemaField("urgency_level", "STRING"),  # emergency, urgent, scheduled
            bigquery.SchemaField("preferred_date", "DATE"),
            bigquery.SchemaField("preferred_time", "STRING"),
            bigquery.SchemaField("budget_range", "STRING"),
            bigquery.SchemaField("payment_method", "STRING"),
            # Attachments and documentation
            bigquery.SchemaField("uploaded_files", "JSON"),
            bigquery.SchemaField("document_links", "STRING", mode="REPEATED"),
            bigquery.SchemaField("voice_notes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("chat_transcript", "STRING"),
            # AI/ML fields
            bigquery.SchemaField("confidence_score", "FLOAT64"),
            bigquery.SchemaField("ml_predictions", "JSON"),
            bigquery.SchemaField("pattern_matches", "STRING", mode="REPEATED"),
            bigquery.SchemaField("similar_cases", "STRING", mode="REPEATED"),
            bigquery.SchemaField("sentiment_score", "FLOAT64"),
            bigquery.SchemaField("priority_score", "FLOAT64"),
            bigquery.SchemaField("churn_risk_score", "FLOAT64"),
            # Feedback and outcomes
            bigquery.SchemaField("solution_successful", "BOOLEAN"),
            bigquery.SchemaField("customer_feedback", "STRING"),
            bigquery.SchemaField("feedback_rating", "INTEGER"),
            bigquery.SchemaField("nps_score", "INTEGER"),
            bigquery.SchemaField("follow_up_notes", "STRING"),
            bigquery.SchemaField("resolution_time", "INTEGER"),
            bigquery.SchemaField("first_contact_resolution", "BOOLEAN"),
            # Support ticket integration
            bigquery.SchemaField("ticket_id", "STRING"),
            bigquery.SchemaField("ticket_status", "STRING"),
            bigquery.SchemaField("assigned_technician", "STRING"),
            bigquery.SchemaField("escalation_level", "INTEGER"),
            bigquery.SchemaField("sla_met", "BOOLEAN"),
            # Revenue and conversion tracking
            bigquery.SchemaField("lead_score", "FLOAT64"),
            bigquery.SchemaField("conversion_value", "FLOAT64"),
            bigquery.SchemaField("lifetime_value", "FLOAT64"),
            bigquery.SchemaField("referral_source", "STRING"),
            bigquery.SchemaField("affiliate_id", "STRING"),
            # Neo4j integration fields
            bigquery.SchemaField("neo4j_node_id", "STRING"),
            bigquery.SchemaField("neo4j_relationships", "JSON"),
            # System and metadata
            bigquery.SchemaField("submission_source", "STRING"),  # web, mobile, api, slack
            bigquery.SchemaField("api_version", "STRING"),
            bigquery.SchemaField("metadata", "JSON"),
            bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("version", "STRING"),
            bigquery.SchemaField("data_consent", "BOOLEAN"),
            bigquery.SchemaField("gdpr_compliant", "BOOLEAN"),
        ]

        # Create dataset
        dataset_id = f"{self.target_project}.mvp3_migrated"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "MVP3 diagnostic data migrated from Datastore with enhanced schema"
        dataset.location = "US"

        self.bq_client.create_dataset(dataset, exists_ok=True)
        logger.info(f"✅ Created dataset: {dataset_id}")

        # Create main table
        table_id = f"{dataset_id}.diagnostics"
        table = bigquery.Table(table_id, schema=diagnostic_schema)
        table.description = "Diagnostic submissions with enhanced schema for growth"

        # Add clustering for performance
        table.clustering_fields = ["equipment_type", "problem_category", "created_at"]

        # Add partitioning for cost optimization
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="created_at")

        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Created table: {table_id}")

        return table_id

    def migrate_datastore_entities(self, kind="Diagnostic", batch_size=500):
        """Migrate entities from Datastore to BigQuery"""

        table_id = self.create_enhanced_schema()

        try:
            # Query all entities from Datastore
            query = self.datastore_client.query(kind=kind)

            migrated_count = 0
            batch = []

            for entity in query:
                # Transform Datastore entity to BigQuery row
                row = self.transform_entity_to_row(entity)
                batch.append(row)

                # Insert in batches
                if len(batch) >= batch_size:
                    errors = self.bq_client.insert_rows_json(table_id, batch)
                    if errors:
                        logger.error(f"Insert errors: {errors}")
                    else:
                        migrated_count += len(batch)
                        logger.info(f"Migrated {migrated_count} records...")
                    batch = []

            # Insert remaining records
            if batch:
                errors = self.bq_client.insert_rows_json(table_id, batch)
                if not errors:
                    migrated_count += len(batch)

            logger.info(f"✅ Migration complete: {migrated_count} records migrated")
            return migrated_count

        except Exception as e:
            logger.error(f"Migration failed: {e}")
            return 0

    def transform_entity_to_row(self, entity) -> Dict:
        """Transform Datastore entity to BigQuery row with enhanced fields"""

        # Generate unique ID if not present
        diagnostic_id = entity.get("id") or hashlib.md5(f"{entity.key.name or entity.key.id}".encode()).hexdigest()

        # Build row with all available data and defaults for new fields
        row = {
            "diagnostic_id": diagnostic_id,
            "created_at": entity.get("created_at") or datetime.now().isoformat(),
            "updated_at": entity.get("updated_at") or datetime.now().isoformat(),
            # Equipment fields
            "equipment_type": entity.get("equipment_type", "Unknown"),
            "equipment_brand": entity.get("equipment_brand", ""),
            "equipment_model": entity.get("equipment_model", ""),
            "equipment_year": entity.get("equipment_year"),
            "equipment_serial": entity.get("serial_number", ""),
            "equipment_hours": entity.get("hours"),
            "equipment_location": entity.get("location", ""),
            # Problem fields
            "problem_category": entity.get("problem_category", "General"),
            "problem_subcategory": entity.get("problem_subcategory", ""),
            "problem_description": entity.get("problem_description", ""),
            "problem_severity": entity.get("severity", "Medium"),
            "error_codes": entity.get("error_codes", []),
            "symptoms": entity.get("symptoms", []),
            # Solution fields
            "solution_provided": entity.get("solution", ""),
            "solution_steps": json.dumps(entity.get("solution_steps", [])),
            "parts_required": json.dumps(entity.get("parts", {})),
            "tools_required": entity.get("tools", []),
            "estimated_time": entity.get("time_estimate"),
            "estimated_cost": entity.get("cost_estimate"),
            # User fields
            "user_id": entity.get("user_id", ""),
            "user_email": entity.get("user_email", ""),
            "user_role": entity.get("user_role", "technician"),
            "company_name": entity.get("company", "DiagnosticPro"),
            "submission_source": entity.get("source", "MVP3"),
            # ML fields (to be populated by ML pipeline)
            "confidence_score": entity.get("confidence", 0.5),
            "ml_predictions": json.dumps({}),
            "pattern_matches": [],
            "similar_cases": [],
            # Feedback fields
            "solution_successful": entity.get("successful"),
            "user_feedback": entity.get("feedback", ""),
            "feedback_rating": entity.get("rating"),
            "follow_up_notes": entity.get("notes", ""),
            # Neo4j fields (to be populated after Neo4j integration)
            "neo4j_node_id": "",
            "neo4j_relationships": json.dumps({}),
            # Metadata
            "metadata": json.dumps(entity.get("metadata", {})),
            "tags": entity.get("tags", []),
            "version": "1.0",
        }

        # Clean None values
        return {k: v for k, v in row.items() if v is not None}

    def create_views_for_compatibility(self):
        """Create views that maintain compatibility with existing queries"""

        # Create a view that matches the old Circle of Life schema
        view_sql = """
        CREATE OR REPLACE VIEW `{project}.circle_of_life.diagnostic_insights` AS
        SELECT
            diagnostic_id as insight_id,
            problem_category,
            problem_description,
            equipment_type,
            solution_provided,
            confidence_score,
            created_at as ingested_at,
            submission_source as source,
            metadata
        FROM `{project}.mvp3_migrated.diagnostics`
        """.format(
            project=self.target_project
        )

        self.bq_client.query(view_sql).result()
        logger.info("✅ Created compatibility view for Circle of Life")

        # Create aggregated views for analytics
        patterns_view = """
        CREATE OR REPLACE VIEW `{project}.diagnostic_patterns.common_problems` AS
        SELECT
            equipment_type,
            problem_category,
            COUNT(*) as occurrence_count,
            AVG(confidence_score) as avg_confidence,
            ARRAY_AGG(DISTINCT error_codes IGNORE NULLS) as common_error_codes,
            ARRAY_AGG(DISTINCT solution_provided IGNORE NULLS LIMIT 5) as top_solutions
        FROM `{project}.mvp3_migrated.diagnostics`
        GROUP BY equipment_type, problem_category
        HAVING occurrence_count > 5
        ORDER BY occurrence_count DESC
        """.format(
            project=self.target_project
        )

        self.bq_client.query(patterns_view).result()
        logger.info("✅ Created patterns analysis view")

    def verify_migration(self):
        """Verify migration success"""

        # Count records in source
        query = self.datastore_client.query(kind="Diagnostic")
        source_count = len(list(query.fetch(limit=1000)))

        # Count records in target
        query_sql = f"""
        SELECT COUNT(*) as count
        FROM `{self.target_project}.mvp3_migrated.diagnostics`
        """
        target_count = list(self.bq_client.query(query_sql))[0]["count"]

        logger.info(f"Source records: {source_count}")
        logger.info(f"Target records: {target_count}")

        if source_count == target_count:
            logger.info("✅ Migration verified successfully!")
            return True
        else:
            logger.warning(f"⚠️ Record count mismatch: {source_count} vs {target_count}")
            return False

    def run_migration(self):
        """Execute complete migration process"""

        logger.info("=" * 60)
        logger.info("🚀 STARTING DATASTORE TO BIGQUERY MIGRATION")
        logger.info("=" * 60)

        # 1. Migrate data
        count = self.migrate_datastore_entities()

        if count > 0:
            # 2. Create compatibility views
            self.create_views_for_compatibility()

            # 3. Verify migration
            self.verify_migration()

            logger.info("=" * 60)
            logger.info("✅ MIGRATION COMPLETE")
            logger.info(f"Migrated {count} records to BigQuery")
            logger.info("=" * 60)

            print(
                """
Next Steps:
===========
1. Update Circle of Life to read from BigQuery instead of Datastore:
   - Change source to: {}.mvp3_migrated.diagnostics

2. Connect Neo4j to sync with BigQuery:
   - Run: python3 src/neo4j_bigquery_sync.py

3. Update Bob Brain to use migrated data:
   - Already compatible via views

4. Optional: Stop reading from Datastore to save API calls
            """.format(
                    self.target_project
                )
            )
        else:
            logger.error("❌ No data migrated")

        return count > 0


if __name__ == "__main__":
    migration = DatastoreToBigQueryMigration()
    migration.run_migration()
