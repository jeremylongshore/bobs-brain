#!/usr/bin/env python3
"""
MVP3 BigQuery Schema - Form-Matched Database Architecture with Massive Expansion Design
Phase 4: Enterprise-grade schema for unlimited data collection and ecosystem unleashing
"""

import logging

from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MVP3BigQuerySchema:
    """
    Massive expansion-ready BigQuery schema matching MVP3 forms
    Designed for ecosystem unleashing and unlimited data collection
    """

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        # Use existing circle_of_life dataset for MVP3 data
        self.dataset_id = f"{project_id}.circle_of_life"

        # Schema version for future migrations
        self.schema_version = "2.0.0"

        logger.info(f"🚀 Initializing MVP3 BigQuery Schema v{self.schema_version}")

    def create_dataset(self):
        """Verify dataset exists (using existing circle_of_life dataset)"""
        try:
            dataset = self.bq_client.get_dataset(self.dataset_id)
            logger.info(f"✅ Using existing dataset: {self.dataset_id}")
        except Exception as e:
            logger.warning(f"Dataset check: {e}")
            # Try to create if doesn't exist
            try:
                dataset = bigquery.Dataset(self.dataset_id)
                dataset.location = "US"
                dataset.description = "MVP3 Diagnostic Ecosystem - Massive Expansion Ready"
                self.bq_client.create_dataset(dataset, exists_ok=True)
                logger.info(f"✅ Dataset created: {self.dataset_id}")
            except Exception as create_error:
                logger.info(f"Using dataset as-is: {create_error}")

    def create_diagnostic_submissions_table(self):
        """
        Create main diagnostic submissions table matching MVP3 form structure
        With massive expansion capabilities
        """
        table_id = f"{self.dataset_id}.diagnostic_submissions"

        schema = [
            # Core identifiers
            bigquery.SchemaField("submission_id", "STRING", mode="REQUIRED", description="Unique submission ID"),
            bigquery.SchemaField(
                "schema_version", "STRING", mode="REQUIRED", description="Schema version for migration tracking"
            ),
            # Customer information
            bigquery.SchemaField("full_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("phone", "STRING"),
            # Service selection
            bigquery.SchemaField(
                "selected_service", "STRING", mode="REQUIRED", description="diagnosis|verification|emergency"
            ),
            bigquery.SchemaField("service_price", "FLOAT64"),
            bigquery.SchemaField("promo_code", "STRING"),
            bigquery.SchemaField("applied_discount", "FLOAT64"),
            # Equipment details (matching form exactly)
            bigquery.SchemaField("equipment_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField(
                "equipment_category",
                "STRING",
                description="Consumer|Commercial|Industrial|Heavy|Medical|Agricultural|Marine|Transportation",
            ),
            bigquery.SchemaField("year", "INTEGER"),
            bigquery.SchemaField("make", "STRING"),
            bigquery.SchemaField("model", "STRING"),
            bigquery.SchemaField("vin", "STRING"),
            bigquery.SchemaField("serial_number", "STRING"),
            bigquery.SchemaField("mileage", "INTEGER"),
            bigquery.SchemaField("hours", "INTEGER", description="Operating hours for equipment"),
            # Problem details
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED", description="Array of error codes"),
            bigquery.SchemaField("problem_description", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("symptoms", "STRING", mode="REPEATED", description="Array of symptoms"),
            bigquery.SchemaField("when_started", "STRING"),
            bigquery.SchemaField("frequency", "STRING"),
            bigquery.SchemaField("shop_quote", "FLOAT64"),
            bigquery.SchemaField("shop_name", "STRING"),
            # Media attachments
            bigquery.SchemaField("uploaded_files", "JSON", description="JSON array of file metadata"),
            bigquery.SchemaField("audio_recording_url", "STRING"),
            bigquery.SchemaField("captured_images", "JSON", description="JSON array of image URLs"),
            # AI Analysis results
            bigquery.SchemaField("ai_analysis", "JSON", description="Complete AI analysis response"),
            bigquery.SchemaField("ai_confidence_score", "FLOAT64"),
            bigquery.SchemaField("ai_model_used", "STRING"),
            bigquery.SchemaField("ai_processing_time_ms", "INTEGER"),
            # Payment information
            bigquery.SchemaField("payment_status", "STRING", description="pending|completed|failed|refunded"),
            bigquery.SchemaField("stripe_payment_id", "STRING"),
            bigquery.SchemaField("payment_amount", "FLOAT64"),
            bigquery.SchemaField("payment_completed_at", "TIMESTAMP"),
            # Email tracking
            bigquery.SchemaField("email_sent", "BOOLEAN"),
            bigquery.SchemaField("email_sent_at", "TIMESTAMP"),
            bigquery.SchemaField("email_opened", "BOOLEAN"),
            bigquery.SchemaField("email_opened_at", "TIMESTAMP"),
            # MASSIVE EXPANSION FIELDS
            bigquery.SchemaField("custom_fields", "JSON", description="Unlimited custom form fields as JSON"),
            bigquery.SchemaField("metadata", "JSON", description="Flexible metadata for any additional data"),
            bigquery.SchemaField("tags", "STRING", mode="REPEATED", description="Searchable tags array"),
            bigquery.SchemaField("data_source", "STRING", description="web_form|api|mobile|voice|chat|email"),
            bigquery.SchemaField("integration_source", "STRING", description="Source system identifier"),
            bigquery.SchemaField("raw_form_data", "JSON", description="Complete raw form submission"),
            # Versioning and audit
            bigquery.SchemaField("form_version", "STRING"),
            bigquery.SchemaField("api_version", "STRING"),
            bigquery.SchemaField("client_info", "JSON", description="Browser, IP, user agent, etc"),
            # Timestamps
            bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
            bigquery.SchemaField("processed_at", "TIMESTAMP"),
            bigquery.SchemaField("archived_at", "TIMESTAMP"),
            # Relationships
            bigquery.SchemaField("parent_submission_id", "STRING", description="For follow-up submissions"),
            bigquery.SchemaField("related_submissions", "STRING", mode="REPEATED"),
            bigquery.SchemaField("customer_id", "STRING", description="For repeat customers"),
            bigquery.SchemaField("session_id", "STRING"),
            # Analytics fields
            bigquery.SchemaField("utm_source", "STRING"),
            bigquery.SchemaField("utm_medium", "STRING"),
            bigquery.SchemaField("utm_campaign", "STRING"),
            bigquery.SchemaField("referrer", "STRING"),
            bigquery.SchemaField("landing_page", "STRING"),
        ]

        # Configure table with partitioning for massive scale
        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="created_at")
        table.clustering_fields = ["equipment_category", "selected_service", "payment_status"]
        table.description = "MVP3 diagnostic form submissions with massive expansion capabilities"

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table created/verified: {table_id}")
        except Exception as e:
            logger.error(f"Error creating table: {e}")

    def create_expansion_tables(self):
        """Create additional tables for massive expansion"""

        # Dynamic form fields table for unlimited expansion
        self._create_dynamic_fields_table()

        # Customer profiles for repeat business
        self._create_customer_profiles_table()

        # AI learning feedback table
        self._create_ai_feedback_table()

        # Equipment knowledge base
        self._create_equipment_knowledge_table()

        # Audit log for compliance
        self._create_audit_log_table()

        # Real-time metrics table
        self._create_metrics_table()

    def _create_dynamic_fields_table(self):
        """Table for managing dynamic form fields"""
        table_id = f"{self.dataset_id}.dynamic_form_fields"

        schema = [
            bigquery.SchemaField("field_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("form_version", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("field_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("field_type", "STRING"),
            bigquery.SchemaField("field_label", "STRING"),
            bigquery.SchemaField("field_options", "JSON"),
            bigquery.SchemaField("validation_rules", "JSON"),
            bigquery.SchemaField("is_required", "BOOLEAN"),
            bigquery.SchemaField("display_order", "INTEGER"),
            bigquery.SchemaField("category", "STRING"),
            bigquery.SchemaField("active", "BOOLEAN"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Dynamic fields table created: {table_id}")

    def _create_customer_profiles_table(self):
        """Customer profiles for enhanced service"""
        table_id = f"{self.dataset_id}.customer_profiles"

        schema = [
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("email", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("full_name", "STRING"),
            bigquery.SchemaField("phone", "STRING"),
            bigquery.SchemaField("company", "STRING"),
            bigquery.SchemaField("equipment_owned", "JSON"),
            bigquery.SchemaField("submission_count", "INTEGER"),
            bigquery.SchemaField("total_spent", "FLOAT64"),
            bigquery.SchemaField("preferred_contact", "STRING"),
            bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("notes", "STRING"),
            bigquery.SchemaField("metadata", "JSON"),
            bigquery.SchemaField("first_submission", "TIMESTAMP"),
            bigquery.SchemaField("last_submission", "TIMESTAMP"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Customer profiles table created: {table_id}")

    def _create_ai_feedback_table(self):
        """AI learning and feedback tracking"""
        table_id = f"{self.dataset_id}.ai_feedback"

        schema = [
            bigquery.SchemaField("feedback_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("submission_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("feedback_type", "STRING"),
            bigquery.SchemaField("accuracy_rating", "INTEGER"),
            bigquery.SchemaField("usefulness_rating", "INTEGER"),
            bigquery.SchemaField("customer_feedback", "STRING"),
            bigquery.SchemaField("technician_validation", "JSON"),
            bigquery.SchemaField("actual_problem", "STRING"),
            bigquery.SchemaField("actual_solution", "STRING"),
            bigquery.SchemaField("repair_cost", "FLOAT64"),
            bigquery.SchemaField("repair_time_hours", "FLOAT64"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ AI feedback table created: {table_id}")

    def _create_equipment_knowledge_table(self):
        """Equipment knowledge base for pattern recognition"""
        table_id = f"{self.dataset_id}.equipment_knowledge"

        schema = [
            bigquery.SchemaField("knowledge_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("make", "STRING"),
            bigquery.SchemaField("model", "STRING"),
            bigquery.SchemaField("year_range", "STRING"),
            bigquery.SchemaField("common_problems", "JSON"),
            bigquery.SchemaField("error_code_meanings", "JSON"),
            bigquery.SchemaField("repair_procedures", "JSON"),
            bigquery.SchemaField("parts_catalog", "JSON"),
            bigquery.SchemaField("service_bulletins", "JSON"),
            bigquery.SchemaField("recall_info", "JSON"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("confidence_score", "FLOAT64"),
            bigquery.SchemaField("verified", "BOOLEAN"),
            bigquery.SchemaField("created_at", "TIMESTAMP"),
            bigquery.SchemaField("updated_at", "TIMESTAMP"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Equipment knowledge table created: {table_id}")

    def _create_audit_log_table(self):
        """Comprehensive audit logging"""
        table_id = f"{self.dataset_id}.audit_log"

        schema = [
            bigquery.SchemaField("audit_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("entity_type", "STRING"),
            bigquery.SchemaField("entity_id", "STRING"),
            bigquery.SchemaField("action", "STRING"),
            bigquery.SchemaField("user_id", "STRING"),
            bigquery.SchemaField("user_email", "STRING"),
            bigquery.SchemaField("ip_address", "STRING"),
            bigquery.SchemaField("user_agent", "STRING"),
            bigquery.SchemaField("changes", "JSON"),
            bigquery.SchemaField("metadata", "JSON"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.DAY, field="timestamp")
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Audit log table created: {table_id}")

    def _create_metrics_table(self):
        """Real-time metrics and analytics"""
        table_id = f"{self.dataset_id}.metrics"

        schema = [
            bigquery.SchemaField("metric_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("metric_type", "STRING"),
            bigquery.SchemaField("metric_name", "STRING"),
            bigquery.SchemaField("metric_value", "FLOAT64"),
            bigquery.SchemaField("dimensions", "JSON"),
            bigquery.SchemaField("tags", "STRING", mode="REPEATED"),
            bigquery.SchemaField("timestamp", "TIMESTAMP", mode="REQUIRED"),
        ]

        table = bigquery.Table(table_id, schema=schema)
        table.time_partitioning = bigquery.TimePartitioning(type_=bigquery.TimePartitioningType.HOUR, field="timestamp")
        self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"✅ Metrics table created: {table_id}")

    def create_views(self):
        """Create useful views for analytics"""

        # Daily summary view
        view_id = f"{self.dataset_id}.daily_summary"
        view_query = f"""
        SELECT
            DATE(created_at) as date,
            COUNT(*) as total_submissions,
            COUNT(DISTINCT email) as unique_customers,
            SUM(payment_amount) as revenue,
            AVG(ai_confidence_score) as avg_confidence,
            COUNTIF(payment_status = 'completed') as paid_submissions,
            COUNTIF(email_sent) as emails_sent,
            ARRAY_AGG(DISTINCT equipment_category IGNORE NULLS) as categories
        FROM `{self.dataset_id}.diagnostic_submissions`
        WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
        GROUP BY date
        ORDER BY date DESC
        """

        view = bigquery.Table(view_id)
        view.view_query = view_query
        self.bq_client.create_table(view, exists_ok=True)
        logger.info(f"✅ Daily summary view created: {view_id}")

    def setup_complete_schema(self):
        """Set up the complete schema with all tables"""
        logger.info("🚀 Setting up complete MVP3 BigQuery schema...")

        # Create main dataset
        self.create_dataset()

        # Create primary table
        self.create_diagnostic_submissions_table()

        # Create expansion tables
        self.create_expansion_tables()

        # Create analytics views
        self.create_views()

        logger.info("✅ Complete MVP3 BigQuery schema created successfully!")
        logger.info(f"📊 Dataset: {self.dataset_id}")
        logger.info("🎯 Ready for massive data collection and ecosystem unleashing!")

        return {
            "dataset": self.dataset_id,
            "tables": [
                "diagnostic_submissions",
                "dynamic_form_fields",
                "customer_profiles",
                "ai_feedback",
                "equipment_knowledge",
                "audit_log",
                "metrics",
            ],
            "views": ["daily_summary"],
            "schema_version": self.schema_version,
        }


def main():
    """Create the MVP3 BigQuery schema"""
    schema_manager = MVP3BigQuerySchema()
    result = schema_manager.setup_complete_schema()

    print("\n" + "=" * 60)
    print("✅ MVP3 BIGQUERY SCHEMA CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Dataset: {result['dataset']}")
    print(f"Tables created: {', '.join(result['tables'])}")
    print(f"Schema version: {result['schema_version']}")
    print("\n🚀 Ready for massive expansion and ecosystem unleashing!")
    print("=" * 60)


if __name__ == "__main__":
    main()
