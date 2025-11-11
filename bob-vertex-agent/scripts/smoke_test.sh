#!/bin/bash
# Quick health check after deployment

set -e

BASE_URL="${1:-http://localhost:8080}"

echo "Running smoke tests against $BASE_URL..."

echo "✓ Testing health endpoint..."
curl -f "$BASE_URL/_health" || { echo "✗ Health check failed"; exit 1; }

echo "✓ Testing A2A AgentCard..."
curl -f "$BASE_URL/.well-known/agent-card" || { echo "✗ AgentCard failed"; exit 1; }

echo "✓ Testing root endpoint..."
curl -f "$BASE_URL/" || { echo "✗ Root endpoint failed"; exit 1; }

echo ""
echo "✅ All smoke tests passed!"
