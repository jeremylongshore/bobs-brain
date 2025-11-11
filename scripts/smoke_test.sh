#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8000"

echo "Starting ADK API server in background..."
# Start server in background if not already running
adk api_server > /tmp/adk_api_server.log 2>&1 &
PID=$!
echo "Server PID: $PID"

# Give server time to start
sleep 3

# Cleanup function
cleanup() {
    echo "Stopping server (PID: $PID)..."
    kill $PID 2>/dev/null || true
    wait $PID 2>/dev/null || true
}
trap cleanup EXIT

echo "Testing /list-apps endpoint..."
# 1) List apps
curl -sf "$BASE/list-apps" | jq .

echo "Testing /run endpoint..."
# 2) Run once (single response)
APP="bobs-brain"   # if this 404s, set to "my_agent" and retry
USER="u_local"
SESS="s_local"

curl -sf -X POST "$BASE/run" -H 'content-type: application/json' -d @- <<JSON | jq .
{
  "app_name": "$APP",
  "user_id": "$USER",
  "session_id": "$SESS",
  "new_message": { "role": "user", "parts": [ { "text": "what time is it?" } ] }
}
JSON

echo ""
echo "✅ Smoke tests passed!"
