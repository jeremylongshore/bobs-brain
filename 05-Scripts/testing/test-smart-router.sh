#!/bin/bash
#
# Test Smart Router Integration
#

set -e

echo "════════════════════════════════════════════════════════════"
echo "Testing Bob's Smart Router (Groq + Ollama + Knowledge)"
echo "════════════════════════════════════════════════════════════"
echo ""

BASE_URL="${1:-http://localhost:8080}"
API_KEY="${BB_API_KEY:-change-me-to-something-secure}"

echo "Base URL: $BASE_URL"
echo "API Key: ${API_KEY:0:10}..."
echo ""

# Test 1: Router Status
echo "📊 Test 1: Check Router Status"
echo "--------------------------------"
curl -s "$BASE_URL/api/router/status" | python3 -m json.tool
echo ""
echo ""

# Test 2: Simple Question (should route to Ollama or Groq)
echo "⚡ Test 2: Simple Question"
echo "--------------------------------"
echo "Query: 'What is Python?'"
curl -s -X POST "$BASE_URL/api/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"What is Python?"}' | python3 -m json.tool
echo ""
echo ""

# Test 3: Medium Complexity (should route to Groq)
echo "🔄 Test 3: Medium Complexity"
echo "--------------------------------"
echo "Query: 'Explain how Docker containers work'"
curl -s -X POST "$BASE_URL/api/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"Explain how Docker containers work"}' | python3 -m json.tool
echo ""
echo ""

# Test 4: Complex Question (should route to Gemini/Claude)
echo "🧠 Test 4: Complex Question"
echo "--------------------------------"
echo "Query: 'Design a microservices architecture for an e-commerce platform'"
curl -s -X POST "$BASE_URL/api/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"Design a microservices architecture for an e-commerce platform with payment processing, inventory management, and user authentication"}' | python3 -m json.tool
echo ""
echo ""

# Test 5: Force Provider (Groq)
echo "🎯 Test 5: Force Provider (Groq)"
echo "--------------------------------"
echo "Query: 'Hello' (forced to Groq)"
curl -s -X POST "$BASE_URL/api/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"Hello", "force_provider":"groq"}' | python3 -m json.tool
echo ""
echo ""

# Test 6: Knowledge Integration
echo "📚 Test 6: Knowledge + Router"
echo "--------------------------------"
echo "Query: 'What are LLM gateway best practices?'"
curl -s -X POST "$BASE_URL/api/query" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"query":"What are LLM gateway best practices?"}' | python3 -m json.tool
echo ""
echo ""

echo "✅ All tests complete!"
echo ""
echo "Check the 'routing' field in each response to see which provider was used."
echo "Expected routing:"
echo "  - Simple questions → Ollama (if available) or Groq"
echo "  - Medium complexity → Groq"
echo "  - High complexity → Gemini or Claude"
echo ""
