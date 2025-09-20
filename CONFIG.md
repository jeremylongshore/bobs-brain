# Configuration

## Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `BB_API_KEY` | **Yes** | - | API authentication key for protected endpoints |
| `GCP_PROJECT` | **Yes** | `bobs-house-ai` | Google Cloud project ID for Vertex AI |
| `GCP_LOCATION` | **Yes** | `us-central1` | Google Cloud region for Vertex AI |
| `NEO4J_URI` | Optional | - | Neo4j bolt URI for graph database |
| `NEO4J_USER` | Optional | `neo4j` | Neo4j username |
| `NEO4J_PASSWORD` | Optional | - | Neo4j password |
| `SLACK_BOT_TOKEN` | Optional | - | Slack bot OAuth token |
| `BB_CONFIDENCE_MIN` | Optional | `0.6` | Minimum confidence threshold for insights |
| `BB_COL_BATCH` | Optional | `50` | Circle of Life batch size |
| `BB_COL_COOLDOWN` | Optional | `60` | Minimum seconds between Circle of Life runs |
| `RUNNING_IN_CLOUD_RUN` | Optional | `false` | Enables Google Cloud logging |
| `PORT` | Optional | `8080` | HTTP server port |

## Authentication

The API uses a simple API key authentication system. All endpoints except `/health`, `/metrics`, `/slack/events`, and `/` require an `X-API-Key` header.

Example:
```bash
curl -H "X-API-Key: your-api-key" \
     -H "Content-Type: application/json" \
     -d '{"query": "Hello Bob"}' \
     http://localhost:8080/api/query
```

## Rate Limiting

Default rate limits:
- General endpoints: 60 requests/minute
- `/api/query`: 10 requests/minute
- `/learn`: 5 requests/minute
- `/slack/events`: 30 requests/minute

## Circle of Life

The learning system processes events in batches with the following flow:
1. **Ingest**: Deduplicate and batch events
2. **Analyze**: Group events by type and user
3. **Generate Insights**: Use LLM to extract patterns
4. **Persist**: Store high-confidence insights to Neo4j/BigQuery
5. **Apply**: Update system behavior based on learnings

Configuration:
- `BB_CONFIDENCE_MIN`: Only insights above this threshold are persisted
- `BB_COL_BATCH`: Maximum events processed per cycle
- `BB_COL_COOLDOWN`: Minimum seconds between learning cycles