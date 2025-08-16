# Neo4j Aura Setup Instructions

## Your Credentials
- **Password**: `q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE`
- **Username**: `neo4j` (default)
- **Service**: `prod.n4gcp.neo4j.io` (needs verification)

## Getting the Correct Connection URI

### Option 1: Through GCP Marketplace
1. Go to GCP Console: https://console.cloud.google.com
2. Navigate to Marketplace → My Solutions
3. Find Neo4j Aura
4. Click "MANAGE VIA NEO4J, INC."
5. This will take you to the Neo4j Console
6. Find your database instance
7. Copy the connection URI (format: `neo4j+s://xxxxx.databases.neo4j.io`)

### Option 2: Direct Neo4j Console
1. Go to: https://console.neo4j.io
2. Sign in with your Google account (same as GCP)
3. You should see your database instance
4. Click on the instance
5. Copy the connection URI

## Expected URI Format
The connection URI should look like one of these:
- `neo4j+s://[instance-id].databases.neo4j.io`
- `neo4j+s://[instance-id].aura.neo4j.io`

## Once You Have the Correct URI

Run this command to update Bob:
```bash
export NEO4J_AURA_URI="neo4j+s://[your-instance-id].databases.neo4j.io"
export NEO4J_AURA_PASSWORD="q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE"

# Deploy Bob with new credentials
gcloud run deploy bobs-brain \
  --source . \
  --region us-central1 \
  --set-env-vars "NEO4J_URI=${NEO4J_AURA_URI},NEO4J_PASSWORD=${NEO4J_AURA_PASSWORD}"
```
