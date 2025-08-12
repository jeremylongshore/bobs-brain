-- MVP3 BigQuery Schema - Form-Matched Database Architecture with Massive Expansion Design
-- Phase 4: Enterprise-grade schema for unlimited data collection and ecosystem unleashing

-- Create dataset if not exists (run manually if needed)
-- CREATE SCHEMA IF NOT EXISTS `bobs-house-ai.mvp3_diagnostic` 
-- OPTIONS(
--   description="MVP3 Diagnostic Ecosystem - Massive Expansion Ready",
--   location="US"
-- );

-- Main diagnostic submissions table matching MVP3 form structure
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_diagnostic_submissions` (
    -- Core identifiers
    submission_id STRING NOT NULL,
    schema_version STRING NOT NULL,
    
    -- Customer information (from form)
    full_name STRING NOT NULL,
    email STRING NOT NULL,
    phone STRING,
    
    -- Service selection (from form)
    selected_service STRING NOT NULL, -- diagnosis|verification|emergency
    service_price FLOAT64,
    promo_code STRING,
    applied_discount FLOAT64,
    
    -- Equipment details (exactly matching form fields)
    equipment_type STRING NOT NULL,
    equipment_category STRING,
    year INT64,
    make STRING,
    model STRING,
    vin STRING,
    serial_number STRING,
    mileage INT64,
    hours INT64,
    
    -- Problem details (from form)
    error_codes ARRAY<STRING>,
    problem_description STRING NOT NULL,
    symptoms ARRAY<STRING>,
    when_started STRING,
    frequency STRING,
    shop_quote FLOAT64,
    shop_name STRING,
    
    -- Media attachments
    uploaded_files JSON,
    audio_recording_url STRING,
    captured_images JSON,
    
    -- AI Analysis results
    ai_analysis JSON,
    ai_confidence_score FLOAT64,
    ai_model_used STRING,
    ai_processing_time_ms INT64,
    
    -- Payment information
    payment_status STRING,
    stripe_payment_id STRING,
    payment_amount FLOAT64,
    payment_completed_at TIMESTAMP,
    
    -- Email tracking
    email_sent BOOLEAN,
    email_sent_at TIMESTAMP,
    email_opened BOOLEAN,
    email_opened_at TIMESTAMP,
    
    -- MASSIVE EXPANSION FIELDS
    custom_fields JSON,
    metadata JSON,
    tags ARRAY<STRING>,
    data_source STRING,
    integration_source STRING,
    raw_form_data JSON,
    
    -- Versioning and audit
    form_version STRING,
    api_version STRING,
    client_info JSON,
    
    -- Timestamps
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    processed_at TIMESTAMP,
    archived_at TIMESTAMP,
    
    -- Relationships
    parent_submission_id STRING,
    related_submissions ARRAY<STRING>,
    customer_id STRING,
    session_id STRING,
    
    -- Analytics fields
    utm_source STRING,
    utm_medium STRING,
    utm_campaign STRING,
    referrer STRING,
    landing_page STRING
)
PARTITION BY DATE(created_at)
CLUSTER BY equipment_category, selected_service, payment_status;

-- Dynamic form fields table for unlimited expansion
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_dynamic_form_fields` (
    field_id STRING NOT NULL,
    form_version STRING NOT NULL,
    field_name STRING NOT NULL,
    field_type STRING,
    field_label STRING,
    field_options JSON,
    validation_rules JSON,
    is_required BOOLEAN,
    display_order INT64,
    category STRING,
    active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Customer profiles for repeat business
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_customer_profiles` (
    customer_id STRING NOT NULL,
    email STRING NOT NULL,
    full_name STRING,
    phone STRING,
    company STRING,
    equipment_owned JSON,
    submission_count INT64,
    total_spent FLOAT64,
    preferred_contact STRING,
    tags ARRAY<STRING>,
    notes STRING,
    metadata JSON,
    first_submission TIMESTAMP,
    last_submission TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- AI learning and feedback tracking
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_ai_feedback` (
    feedback_id STRING NOT NULL,
    submission_id STRING NOT NULL,
    feedback_type STRING,
    accuracy_rating INT64,
    usefulness_rating INT64,
    customer_feedback STRING,
    technician_validation JSON,
    actual_problem STRING,
    actual_solution STRING,
    repair_cost FLOAT64,
    repair_time_hours FLOAT64,
    created_at TIMESTAMP
);

-- Equipment knowledge base for pattern recognition
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_equipment_knowledge` (
    knowledge_id STRING NOT NULL,
    equipment_type STRING,
    make STRING,
    model STRING,
    year_range STRING,
    common_problems JSON,
    error_code_meanings JSON,
    repair_procedures JSON,
    parts_catalog JSON,
    service_bulletins JSON,
    recall_info JSON,
    source STRING,
    confidence_score FLOAT64,
    verified BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Comprehensive audit logging
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_audit_log` (
    audit_id STRING NOT NULL,
    entity_type STRING,
    entity_id STRING,
    action STRING,
    user_id STRING,
    user_email STRING,
    ip_address STRING,
    user_agent STRING,
    changes JSON,
    metadata JSON,
    timestamp TIMESTAMP NOT NULL
)
PARTITION BY DATE(timestamp);

-- Real-time metrics and analytics
CREATE TABLE IF NOT EXISTS `bobs-house-ai.circle_of_life.mvp3_metrics` (
    metric_id STRING NOT NULL,
    metric_type STRING,
    metric_name STRING,
    metric_value FLOAT64,
    dimensions JSON,
    tags ARRAY<STRING>,
    timestamp TIMESTAMP NOT NULL
)
PARTITION BY TIMESTAMP_TRUNC(timestamp, HOUR);

-- Create view for daily analytics
CREATE OR REPLACE VIEW `bobs-house-ai.circle_of_life.mvp3_daily_summary` AS
SELECT
    DATE(created_at) as date,
    COUNT(*) as total_submissions,
    COUNT(DISTINCT email) as unique_customers,
    SUM(payment_amount) as revenue,
    AVG(ai_confidence_score) as avg_confidence,
    COUNTIF(payment_status = 'completed') as paid_submissions,
    COUNTIF(email_sent) as emails_sent,
    ARRAY_AGG(DISTINCT equipment_category IGNORE NULLS) as categories
FROM `bobs-house-ai.circle_of_life.mvp3_diagnostic_submissions`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY date
ORDER BY date DESC;

-- Create view for customer lifetime value
CREATE OR REPLACE VIEW `bobs-house-ai.circle_of_life.mvp3_customer_ltv` AS
SELECT
    email,
    MIN(full_name) as customer_name,
    COUNT(*) as total_submissions,
    SUM(payment_amount) as lifetime_value,
    AVG(ai_confidence_score) as avg_confidence,
    MIN(created_at) as first_submission,
    MAX(created_at) as last_submission,
    DATE_DIFF(CURRENT_DATE(), DATE(MIN(created_at)), DAY) as customer_age_days
FROM `bobs-house-ai.circle_of_life.mvp3_diagnostic_submissions`
WHERE payment_status = 'completed'
GROUP BY email
ORDER BY lifetime_value DESC;