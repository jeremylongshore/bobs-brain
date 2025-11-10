# 🚀 Quick Start Guide

> **Navigation**: [← Back to Docs Hub](./README.md) | [Next: VPS Tiers →](./VPS-TIERS.md)

<details>
<summary><b>📋 TL;DR</b> - Click to expand</summary>

**Get running in 3 commands:**
1. `./install.sh` - Install everything
2. Edit `.env` with your API key
3. `./deploy-all.sh docker` - Start services

**Test it:** `curl -X POST http://localhost:8080/api/v1/chat -H "Content-Type: application/json" -d '{"prompt": "What is Python?"}'`

</details>

---

## Prerequisites

Before you begin, ensure you have:

- **Ubuntu 22.04+** (or compatible Linux distribution)
- **4GB+ RAM** (minimum for local models)
- **Sudo access** (for installing dependencies)
- **Internet connection** (to download models and images)

**Optional but recommended:**
- Anthropic API key (for Claude access)
- SSH key pair (for cloud deployments)

## Step 1: Clone the Repository

```bash
git clone https://github.com/jeremylongshore/hybrid-ai-stack.git
cd hybrid-ai-stack
```

## Step 2: Run One-Command Installation

The installation script will:
- ✅ Check for sudo access
- ✅ Install Docker, Docker Compose, Python, Ollama
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Initialize Taskwarrior
- ✅ Create `.env` from template

```bash
./install.sh
```

**Expected output:**
```
[INFO] Starting Hybrid AI Stack installation...
[✓] Sudo access verified
[✓] Docker already installed
[✓] Ollama installed successfully
[✓] Python dependencies installed
[✓] Taskwarrior initialized

═══════════════════════════════════════════════════════════
  Hybrid AI Stack Installation Complete!
═══════════════════════════════════════════════════════════
```

## Step 3: Configure Environment

Edit `.env` and add your API keys:

```bash
nano .env
```

**Required:**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Optional:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

> **💡 Tip:** Get your Anthropic API key from https://console.anthropic.com/

## Step 4: Deploy the Stack

```bash
./deploy-all.sh docker
```

This will:
1. ✅ Start Ollama service
2. ✅ Pull TinyLlama and Phi-2 models (~2GB download)
3. ✅ Start all Docker services
4. ✅ Run health checks
5. ✅ Display access URLs

**Expected output:**
```
╔════════════════════════════════════════════════════════════════╗
║                  Hybrid AI Stack Deployment                   ║
║            Intelligent AI Request Routing System              ║
╚════════════════════════════════════════════════════════════════╝

[INFO] Starting Docker deployment...
[⟳] Pulling TinyLlama and Phi-2...
[✓] Models pulled successfully
[✓] All services started
[✓] API Gateway is healthy (http://localhost:8080)
[✓] n8n is healthy (http://localhost:5678)

═══════════════════════════════════════════════════════════
  Deployment Complete!
═══════════════════════════════════════════════════════════

🎉 Your Hybrid AI Stack is now running!

📊 Access URLs:
   • API Gateway:  http://localhost:8080
   • n8n:         http://localhost:5678
   • Grafana:     http://localhost:3000 (admin/admin)
   • Prometheus:  http://localhost:9090
```

## Step 5: Test the System

### Simple Test (Routes to TinyLlama)

```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?"}'
```

**Expected response:**
```json
{
  "model": "tinyllama",
  "backend": "local",
  "response": "Python is a high-level programming language...",
  "cost": 0.0,
  "routing": {
    "complexity": 0.2,
    "reasoning": "Complexity 0.20: short prompt, simple task keywords",
    "estimated_cost": 0.0
  },
  "latency_seconds": 1.23
}
```

### Complex Test (Routes to Claude)

```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to implement a binary search tree with insert, delete, and search methods."
  }'
```

**Expected response:**
```json
{
  "model": "claude-sonnet",
  "backend": "cloud",
  "response": "Here's a complete implementation...",
  "cost": 0.012,
  "routing": {
    "complexity": 0.8,
    "reasoning": "Complexity 0.80: long prompt, contains code, complex keywords",
    "estimated_cost": 0.012
  },
  "latency_seconds": 3.45
}
```

### Check Routing Statistics

```bash
curl http://localhost:8080/api/v1/stats
```

**Response:**
```json
{
  "total_requests": 2,
  "local_requests": 1,
  "cloud_requests": 1,
  "local_percentage": 50.0
}
```

## Step 6: Explore the Services

### n8n Workflow Automation

1. Open http://localhost:5678
2. Create account (first-time setup)
3. Explore pre-loaded workflows

### Grafana Dashboards

1. Open http://localhost:3000
2. Login: `admin` / `admin`
3. View AI Stack dashboard

### Prometheus Metrics

1. Open http://localhost:9090
2. Query: `api_gateway_requests_total`

## Quick Validation Checklist

- [ ] `curl http://localhost:8080/health` returns `{"api_gateway": "healthy"}`
- [ ] `docker-compose ps` shows all services running
- [ ] `docker exec ollama ollama list` shows tinyllama and phi
- [ ] Simple request routes to local model (cost = $0)
- [ ] Complex request routes to Claude (cost > $0)

## Common Post-Install Tasks

### Pull Additional Models

```bash
# Mistral 7B (for Tier 3+)
docker exec ollama ollama pull mistral

# Llama 3.2
docker exec ollama ollama pull llama3.2
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api-gateway
docker-compose logs -f ollama-cpu
```

### Restart Services

```bash
# Restart specific service
docker-compose restart api-gateway

# Restart everything
docker-compose down
docker-compose --profile cpu up -d
```

## Next Steps

Now that your system is running:

1. **Understand the Architecture** → [Architecture Guide](./ARCHITECTURE.md)
2. **Optimize for Your Use Case** → [Cost Optimization](./COST-OPTIMIZATION.md)
3. **Try Example Scripts**:
   ```bash
   source venv/bin/activate
   python scripts/moderation_pipeline.py
   python scripts/support_router.py
   ```
4. **Set Up Monitoring** → [Monitoring Guide](./MONITORING.md)
5. **Deploy to Cloud** → [Deployment Guide](./DEPLOYMENT.md)

## Troubleshooting

### Services Not Starting

```bash
# Check Docker is running
docker info

# View detailed logs
docker-compose logs -f

# Reset and try again
docker-compose down -v
./deploy-all.sh docker
```

### Ollama Models Not Pulling

```bash
# Check Ollama service
docker-compose logs ollama-cpu

# Manually pull models
docker exec ollama ollama pull tinyllama
docker exec ollama ollama pull phi
```

### API Gateway Returns 500

```bash
# Check if API key is set
cat .env | grep ANTHROPIC_API_KEY

# View API Gateway logs
docker-compose logs -f api-gateway

# Restart gateway
docker-compose restart api-gateway
```

**→ Full troubleshooting guide:** [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)

---

**Related Documentation:**
- [Architecture Overview](./ARCHITECTURE.md)
- [VPS Tier Selection](./VPS-TIERS.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Troubleshooting](./TROUBLESHOOTING.md)

[⬆ Back to Top](#-quick-start-guide)
