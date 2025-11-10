# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Last Updated**: 2025-09-14

## Project Overview

Multi-source data collection system for DiagnosticPro platform. Collects automotive repair and diagnostic data from YouTube, Reddit, and GitHub through a strict export gateway architecture.

## High-Level Architecture

### Data Flow Pipeline
```
Scrapers (YouTube/Reddit/GitHub)
    ↓
Export Gateway (validation & transformation)
    ↓
Schema Project (../schema/)
    ↓
BigQuery (diagnostic-pro-start-up)
```

### Key Architectural Principles
1. **Separation of Concerns**: Scrapers NEVER access databases directly
2. **Single Exit Point**: All data flows through export_gateway/
3. **Schema Compliance**: configs/schema_rules.json is READ-ONLY from ../schema/
4. **Universal Equipment Registry**: All equipment data must comply with standardized identification

## Core Commands

### Data Collection
```bash
# YouTube - Extract repair videos from channels
python3 youtube_scraper/data_extractor.py
python3 youtube_scraper/massive_extractor.py  # Bulk processing

# Reddit - Two approaches available
# Option 1: Browser-based (Playwright)
python3 reddit_scrapers/reddit_url_collector.py      # Phase 1: Collect URLs
python3 reddit_scrapers/reddit_json_processor.py     # Phase 2: Extract data

# Option 2: API-based (PRAW - requires credentials)
python3 praw/massive_500k_collector.py
./praw/start_massive_collection.sh

# GitHub - Mine automotive repositories
python3 github_miner/enhanced_github_miner.py

# Run all collectors in parallel
./scripts/run_all_collectors.sh
```

### Data Processing & Export
```bash
# Prepare data for BigQuery
python3 scripts/prepare_cloud_export.py

# Validate data before export
python3 scripts/validate_export_data.py

# Clean up straggling data
python3 scripts/cleanup_straggling_data.py
python3 scripts/data_cleaner.py

# Upload to BigQuery
cd export_gateway/cloud_ready && ./upload_to_gcp.sh
```

### Testing
```bash
# Test Reddit collection
python3 praw/test_reddit.py
python3 praw/test_comprehensive_collector.py

# Run 10-minute collection test
python3 ten_minute_test.py
```

### Monitoring & Maintenance
```bash
# Check pipeline status
ls -la export_gateway/raw/ | wc -l           # Pending items
ls -la export_gateway/cloud_ready/ | wc -l   # Ready for upload
ls -la export_gateway/failed/                # Failed exports

# Monitor running collectors
tail -f logs/*.log

# Stop all collectors
pkill -f collector.py
```

## Project Structure & Responsibilities

### Scrapers
- **youtube_scraper/**: Video metadata, repair procedures, part numbers
  - `data_extractor.py`: Main YouTube scraper
  - `massive_extractor.py`: Bulk video processing
  - `expert_channels_extractor.py`: Specific channel targeting
- **praw/**: Reddit posts, DTC discussions (has own CLAUDE.md with file creation rules)
  - `massive_500k_collector.py`: Large-scale Reddit collection
  - `comprehensive_repair_collector.py`: Detailed repair discussions
  - `dtc_focused_collector.py`: DTC code specific collection
- **github_miner/**: Code repositories, technical documentation
  - `enhanced_github_miner.py`: Main GitHub mining tool

### Export Gateway (`export_gateway/`)
```
raw/           → Incoming scraped data
transformed/   → Schema-mapped data
cloud_ready/   → NDJSON for BigQuery
sent/          → Successfully exported
failed/        → Export failures
```

### Scripts (`scripts/`)
- `validate_export_data.py`: Validates NDJSON files before BigQuery upload
- `prepare_cloud_export.py`: Transforms data to NDJSON format
- `cleanup_straggling_data.py`: Removes processed data
- `data_cleaner.py`: Data cleaning utilities
- `run_all_collectors.sh`: Runs all collectors in parallel

### Configuration (`configs/`)
- **schema_rules.json**: Database schema (READ-ONLY from ../schema/)
  - Contains Universal Equipment Registry definitions
  - Equipment categories and identification types
  - Validation rules for VIN, HIN, IMEI, Serial numbers

## Critical Integration Rules

### Field Mappings (Universal Equipment Registry)
```
Source Field → Database Field
vin         → identification_number
error_code  → dtc_code
car_make    → equipment.make
make        → manufacturer
```

### BigQuery Configuration
- **Project**: diagnostic-pro-start-up
- **Production Dataset**: diagnosticpro_prod (266 tables)
- **Scraped Data Dataset**: scraped_data
- **Storage Bucket**: diagnostic-scraper-processed

### DTC Code Validation
- Format: `^[PBCU]\d{4}$` (e.g., P0301, B1342, C0035, U0100)
- P = Powertrain, B = Body, C = Chassis, U = Network

## Development Workflow

### Adding New Scraper
1. Create scraper in appropriate directory
2. Output to `export_gateway/raw/` as JSON
3. Implement schema mapping per `configs/schema_rules.json`
4. Validate with `scripts/validate_export_data.py`
5. Test small batch before bulk collection

### Data Export Requirements
- Format: Newline-delimited JSON (NDJSON)
- Required fields: `import_timestamp`, `source`
- Max file size: 100MB for BigQuery
- Include manifest file with counts

### Debugging Failed Exports
1. Check `export_gateway/failed/` for error files
2. Review validation logs
3. Verify schema compliance against `configs/schema_rules.json`
4. Re-process through pipeline

## Performance Targets
- YouTube: 1,000 videos/hour
- Reddit: 10,000 posts/hour
- GitHub: 100 repos/hour
- BigQuery upload: 100MB/minute
- Batch processing: 10,000 records max
- Collection test: 5,000+ items in 10 minutes

## Environment Requirements
- Python 3.7+
- gcloud CLI configured
- Chrome/Chromium with ChromeDriver (for Selenium scrapers)
- Brave browser (optional, for enhanced scraping)
- Reddit API credentials in `praw/.env`:
  ```
  REDDIT_CLIENT_ID=your_client_id
  REDDIT_CLIENT_SECRET=your_secret
  REDDIT_USER_AGENT=RepairDataExtractor/1.0
  ```

## Important Notes
- Archive directory (`archive/ARCHIVE_COMPLETE/`) contains old system - DO NOT USE
- Follow file creation rules in `praw/CLAUDE.md` - NO unauthorized file creation
- All scrapers must validate against `configs/schema_rules.json`
- Never create direct database connections in scraper code
- Always use export gateway for data flow