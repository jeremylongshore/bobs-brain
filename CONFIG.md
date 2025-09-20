# CONFIG.md

| Var | Required | Purpose |
|-----|----------|---------|
| BB_API_KEY | yes | Header auth for /api/* |
| PROVIDER, MODEL | yes | LLM selection (Claude, etc.) |
| STATE_BACKEND, DATABASE_URL | no | SQLite/Postgres |
| VECTOR_BACKEND, CHROMA_DIR | no | Chroma by default |
| GRAPH_BACKEND, NEO4J_* | no | Neo4j optional |
| CACHE_BACKEND, REDIS_URL | no | Redis optional |
| ARTIFACT_BACKEND,* | no | Local or S3 |
| BB_CONFIDENCE_MIN, BB_COL_* | no | CoL tuning |
| COL_SCHEDULE | no | CRON for CoL |