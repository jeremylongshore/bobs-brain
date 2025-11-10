# Hybrid AI Stack - Quick Reference

## 🚀 Quick Start

```bash
# Install everything
./install.sh

# Configure API key
nano .env  # Add ANTHROPIC_API_KEY

# Deploy
./deploy-all.sh docker
```

## 📡 API Endpoints

```bash
# Chat (auto-routing)
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your question"}'

# Estimate complexity
curl -X POST http://localhost:8080/api/v1/complexity \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your question"}'

# Get stats
curl http://localhost:8080/api/v1/stats

# Health check
curl http://localhost:8080/health
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose --profile cpu up -d

# View logs
docker-compose logs -f [service]

# Restart service
docker-compose restart [service]

# Stop all
docker-compose down

# Pull Ollama models
docker exec ollama ollama pull tinyllama
docker exec ollama ollama pull phi
```

## 📊 Service URLs

- **API Gateway**: http://localhost:8080
- **n8n**: http://localhost:5678
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🎯 Complexity Routing

| Complexity | Model | Cost | Use Case |
|------------|-------|------|----------|
| < 0.3 | TinyLlama | $0 | Simple Q&A, lists |
| 0.3-0.6 | Phi-2 | $0 | Explanations, summaries |
| > 0.6 | Claude | $0.003-0.015 | Code, analysis |

## ⚙️ Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-your-key
OLLAMA_URL=http://localhost:11434
USE_LOCAL_FOR_SIMPLE=true
COMPLEXITY_THRESHOLD=0.5
```

## 🔧 Taskwarrior

```bash
# Source helper functions
source scripts/tw-helper.sh

# Quick task
tw_quick_add "Deploy to AWS"

# Start/complete
tw_start 42
tw_complete 42 "Deployment successful"

# View routing stats
tw_routing_stats

# Cost tracking
tw_track_cost 0.015 claude-sonnet "Complex analysis"
tw_cost_report
```

## ☁️ Cloud Deployment

### AWS
```bash
# Set credentials
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret

# Deploy Tier 2
./deploy-all.sh aws 2
```

### Terraform
```bash
cd terraform/aws

# Initialize
terraform init

# Plan
terraform plan -var="tier=2" -var="key_name=your-key"

# Apply
terraform apply -var="tier=2" -var="key_name=your-key"
```

## 🧪 Testing

```bash
# Run tests
source venv/bin/activate
pytest tests/

# Test router
python tests/test_router.py

# Run example scripts
python scripts/moderation_pipeline.py
python scripts/support_router.py
```

## 📈 Monitoring

```bash
# Prometheus metrics
curl http://localhost:8080/metrics

# Check model health
docker exec ollama ollama list

# View Gateway logs
docker-compose logs -f api-gateway
```

## 💰 Cost Optimization

**Rule of Thumb:**
- Use local for: Facts, lists, simple questions
- Use cloud for: Code generation, complex analysis, creative writing

**Expected Savings:**
- Tier 2 (Standard): 60-70% reduction
- Tier 3 (Performance): 75-85% reduction

## 🔍 Troubleshooting

```bash
# Ollama not responding
docker exec ollama ollama list
docker-compose restart ollama-cpu

# API Gateway 500 error
docker-compose logs -f api-gateway
cat .env | grep ANTHROPIC_API_KEY

# Services not starting
docker-compose down
docker-compose up -d

# Reset everything
docker-compose down -v
./install.sh
./deploy-all.sh docker
```

## 📚 Documentation

- [Full README](README.md)
- [Quick Start](docs/QUICKSTART.md)
- [VPS Tiers](docs/VPS-TIERS.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

**💡 Pro Tips:**
- Keep `USE_LOCAL_FOR_SIMPLE=true` for maximum savings
- Monitor costs with Taskwarrior integration
- Use Grafana dashboards for visual monitoring
- Test routing with `curl` before production
