# Archived Databases

This directory contains old database files that have been migrated to new systems.

## Contents

### ChromaDB (Migrated to BigQuery)
- **Location:** `chroma_data/`
- **Contents:** 5 knowledge documents
- **Migration Date:** 2025-08-13
- **New Location:** BigQuery `knowledge_base.chromadb_migrated`

### Backup Files (Migrated to BigQuery)
- **File:** `bob_data_backup_20250810_185731.json`
- **Contents:** 5 documents (same as ChromaDB)
- **Migration Date:** 2025-08-13
- **New Location:** BigQuery `knowledge_base.backup_migrated`

## Migration Status
✅ All data from these old databases has been migrated to:
1. BigQuery (primary data warehouse)
2. Neo4j Aura (knowledge graph)

## Note
These files are kept for historical reference only. The active data is now in:
- **BigQuery:** `bobs-house-ai` project
- **Neo4j Aura:** Instance d3653283

The old Neo4j VM can be deleted to save $50/month.
