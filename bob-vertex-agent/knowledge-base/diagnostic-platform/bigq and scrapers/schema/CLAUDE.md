# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🏗️ Project Overview

This is a **DATABASE SCHEMA PROJECT** for managing DiagnosticPro's repair platform database infrastructure. The project handles database schemas, data validation, import pipelines, and BigQuery/MySQL operations.

**Critical:** This project NEVER handles web scraping, data collection, or external API calls. It only receives and validates clean data.

## 📁 Project Structure

```
schema/
├── datapipeline_import/        # Data import pipeline
│   ├── pending/               # Awaiting validation
│   ├── validated/             # Passed validation
│   ├── failed/                # Failed validation
│   └── imported/              # Successfully imported
├── ARCHIVE_OLD_SYSTEM/        # PostgreSQL schemas (17 SQL files)
│   └── core_code/            # Original schema definitions
└── ARCHIVE_2025_08_29/       # Previous MySQL migration attempts
```

## 🛠️ Key Commands

### Database Connection
```bash
# Connect to Google Cloud SQL MySQL via proxy
cloud_sql_proxy -instances=diagnostic-pro-start-up:us-central1:repair-master-db=tcp:3307
mysql -h 127.0.0.1 -P 3307 -u root -p'DiagnosticPro2025' repair_platform

# Connect via Jump VM
gcloud compute ssh repair-db-access --zone=us-west1-b
mysql -h 10.103.0.5 -u root -p repair_platform
```

### BigQuery Operations
```bash
# Deploy tables to BigQuery
./deploy_bigquery_tables.sh

# Check BigQuery tables
bq ls --format=json diagnostic-pro-start-up:repair_diagnostics
```

### Data Pipeline
```bash
# Place data for import
cp data.json datapipeline_import/pending/

# Check pipeline status
ls -la datapipeline_import/*/
```

## 🗄️ Database Architecture

The schema includes 254 tables organized into these core systems:

1. **Authentication & Users** - User management, sessions, API keys
2. **Communication** - Messages, notifications, conversations  
3. **File Storage** - Documents, media, audit trails
4. **Billing & Scheduling** - Appointments, invoices, payments
5. **Vehicle Management** - Makes, models, diagnostic data
6. **Universal Equipment Registry** - All equipment types (vehicles, electronics, machinery)
7. **Diagnostic Protocols** - OBD-II, J1939, proprietary protocols
8. **ML Infrastructure** - Predictions, features, training data
9. **Multimedia Storage** - Images, videos, waveforms
10. **Operational Tracking** - Metrics, analytics, telemetry

## ⚠️ Critical Rules

1. **NO SCRAPING CODE** - This project receives data, never collects it
2. **SINGLE ENTRY POINT** - All data enters through `datapipeline_import/`
3. **VALIDATION FIRST** - Never import unvalidated data
4. **SCHEMA OWNERSHIP** - This project owns all schema definitions

## 🔄 Common Workflows

### Data Import
1. External system sends data to `datapipeline_import/pending/`
2. Validation process checks against schema rules
3. Valid data moves to `validated/` then to database
4. Failed data goes to `failed/` with error logs

### Schema Modification
1. Update SQL schema files
2. Test changes locally first
3. Deploy to Cloud SQL/BigQuery
4. Update validation rules

## 🚫 Do NOT:
- Add scraping or crawling logic
- Make direct external API calls
- Create files without explicit permission
- Mix database logic with data collection
- Deploy untested schema changes

## 📊 Performance Targets
- Validation: < 100ms per batch
- Bulk import: 10,000 records/second  
- API response: < 200ms
- Queue processing: Every 30 seconds

## 🔧 Maintenance Tasks

**Daily:**
- Check `datapipeline_import/failed/` for errors
- Monitor `datapipeline_import/pending/` queue

**Weekly:**
- Archive processed data from `imported/`
- Review error patterns in failed imports
- Optimize slow queries

**Monthly:**
- Update schema documentation
- Backup schema definitions
- Review and optimize indexes