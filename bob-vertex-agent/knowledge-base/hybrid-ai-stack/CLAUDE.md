# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Hybrid AI Stack** is a production-ready AI orchestration system that intelligently routes requests between local CPU-based models and cloud APIs to achieve 60-80% cost reduction. The system uses multi-factor complexity estimation to automatically select the optimal model for each request.

**Repository**: https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions

## Directory Standards

Follow `.directory-standards.md` for structure and file naming.
- Store all docs in `01-Docs/`
- Use `NNN-abv-description.ext` format with approved abbreviations
- Maintain strict chronological order

## Project Purpose

Reduce AI API costs through intelligent routing:
- **Simple queries** (complexity < 0.3) → TinyLlama (local, free)
- **Medium queries** (0.3 - 0.6) → Phi-2 (local, free)
- **Complex queries** (> 0.6) → Claude Sonnet (cloud, paid)

This achieves **60-80% cost reduction** vs. cloud-only approaches while maintaining quality.

## System Architecture

### Core Components

```
User Request
     ↓
API Gateway (Flask + Gunicorn) :8080
     ↓
Smart Router (scripts/smart_router.py)
     ↓
├── TinyLlama (Ollama, local, free)
├── Phi-2 (Ollama, local, free)
└── Claude Sonnet (Anthropic API, paid)
```

### Request Flow (Detailed)

```
1. Client → POST /api/v1/chat {"prompt": "..."}
                ↓
2. gateway/app.py:107-170 (chat endpoint)
   - Validates request
   - Extracts prompt and optional model override
                ↓
3. scripts/smart_router.py:route_request()
   - Calls estimate_complexity() → Returns (0.0-1.0, reasoning)
   - Calls select_model(complexity) → Returns 'tinyllama'|'phi2'|'claude-sonnet'
   - Calls estimate_cost() → Returns $0.00 or $0.003-0.015
                ↓
4. Execute request on selected backend:
   ├─ Local (TinyLlama/Phi-2):
   │  └─ scripts/smart_router.py:execute_ollama_request()
   │     └─ HTTP POST to http://ollama:11434/api/generate
   │
   └─ Cloud (Claude):
      └─ scripts/smart_router.py:execute_claude_request()
         └─ Anthropic SDK → Claude API
                ↓
5. Response processing:
   - Logs to Python logging (gateway/app.py:25-28)
   - Records to Prometheus metrics (gateway/app.py:54-68)
   - Optional: Logs to Taskwarrior (if ENABLE_TASKWARRIOR_LOGGING=true)
   - Optional: Caches in Redis (if redis_client available)
                ↓
6. Return JSON response to client
   {
     "response": "...",
     "model": "tinyllama",
     "backend": "local",
     "cost": 0.0,
     "routing": {"complexity": 0.2, "reasoning": "...", "estimated_cost": 0.0}
   }
```

### Technology Stack

**Backend**:
- Python 3.11+
- Flask 3.1 (API Gateway)
- Anthropic SDK (Claude API)
- Ollama (local model serving)

**Infrastructure**:
- Docker Compose (8 services)
- Terraform (AWS/GCP deployment)
- Prometheus + Grafana (monitoring)
- n8n (workflow automation)
- Taskwarrior (task tracking)

**Models**:
- TinyLlama 1.1B (700MB RAM, simple queries)
- Phi-2 2.7B (1.6GB RAM, medium queries)
- Mistral-7B (4GB RAM, optional, high-quality)
- Claude Sonnet 4 (cloud API, complex queries)

## Directory Structure

```
hybrid-ai-stack/
├── scripts/
│   ├── smart_router.py           # Core routing logic (CRITICAL)
│   ├── moderation_pipeline.py    # Example: content moderation
│   ├── support_router.py         # Example: customer support
│   └── tw-helper.sh              # Taskwarrior helper functions
├── gateway/
│   ├── app.py                    # Flask API Gateway
│   ├── Dockerfile                # Gateway container
│   └── requirements.txt          # Gateway dependencies
├── terraform/
│   ├── aws/                      # AWS Terraform configs
│   │   ├── main.tf               # EC2 instances, security groups
│   │   ├── variables.tf          # Tier configurations
│   │   └── outputs.tf            # SSH commands, IPs
│   └── gcp/                      # GCP Terraform configs
├── workflows/                     # n8n workflow definitions
│   ├── smart_routing.json        # Automated routing workflow
│   ├── cost_monitor.json         # Cost alerting
│   ├── performance_monitor.json  # Performance reports
│   └── orchestrator_pipeline.json # Multi-stage orchestration
├── docs/                          # GitHub Pages documentation
│   ├── QUICKSTART.md
│   ├── ARCHITECTURE.md
│   ├── VPS-TIERS.md
│   ├── DEPLOYMENT.md
│   ├── SMART-ROUTER.md
│   ├── COST-OPTIMIZATION.md
│   ├── MONITORING.md
│   ├── TROUBLESHOOTING.md
│   ├── EXAMPLES.md
│   ├── N8N-WORKFLOWS.md
│   └── TASKWARRIOR.md
├── configs/                       # Service configurations
│   ├── prometheus.yml
│   └── grafana-datasources.yml
├── tests/
│   └── test_router.py            # Pytest test suite
├── docker-compose.yml            # Complete stack definition
├── install.sh                    # One-command installation
├── deploy-all.sh                 # One-command deployment
├── .env.example                  # Environment template
└── requirements.txt              # Python dependencies
```

## Key Files & Their Purposes

### Critical Files (DO NOT MODIFY WITHOUT UNDERSTANDING)

**`scripts/smart_router.py`** (375 lines)
- Core intelligent routing logic
- Multi-factor complexity estimation (see algorithm below)
- Model selection algorithm
- Ollama integration for local models
- Claude API integration
- Taskwarrior logging
- Cost tracking

**Complexity Estimation Algorithm (scripts/smart_router.py:87-149):**

The router uses a weighted scoring system:

1. **Length Factor** (contributes to final score):
   - < 100 chars: +0.1 (short)
   - 100-500 chars: +0.3 (medium)
   - > 500 chars: +0.5 (long)

2. **Keyword Factor**:
   - Complex keywords (analyze, design, implement, etc.): +0.1 per keyword (max 0.3)
   - Simple keywords (list, what is, define, etc.): -0.1
   - Neutral: +0.1

3. **Code Detection** (regex patterns):
   - Detects: code blocks (```), function defs, imports, syntax characters
   - 2+ matches: +0.3

4. **Task Type**:
   - Simple questions (single `?`): -0.1
   - Creative tasks (create, build): +0.2
   - Neutral: 0.0

**Final score normalized to 0.0-1.0 range**

**Model Selection Thresholds (scripts/smart_router.py:151-158):**
- `complexity < 0.3` → TinyLlama (local, free)
- `0.3 ≤ complexity < 0.6` → Phi-2 (local, free)
- `complexity ≥ 0.6` → Claude Sonnet (cloud, paid)

**`gateway/app.py`** (230 lines)
- Flask API Gateway with 6 REST endpoints
- Prometheus metrics export
- Redis caching (optional)
- Error handling and logging

**API Endpoints:**

1. **`GET /`** - Service info
   ```bash
   curl http://localhost:8080/
   # Returns: {"service": "Hybrid AI Stack", "status": "healthy", "version": "1.0.0"}
   ```

2. **`GET /health`** - Detailed health check
   ```bash
   curl http://localhost:8080/health
   # Returns: {api_gateway, redis, ollama, claude_api} status
   ```

3. **`POST /api/v1/chat`** - Main chat endpoint with auto-routing
   ```bash
   # Auto-routing (recommended)
   curl -X POST http://localhost:8080/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is Python?"}'

   # Manual model selection
   curl -X POST http://localhost:8080/api/v1/chat \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Explain recursion", "model": "phi2"}'

   # Response format:
   {
     "response": "Model's answer here",
     "model": "tinyllama",
     "backend": "local",
     "cost": 0.0,
     "routing": {
       "complexity": 0.2,
       "reasoning": "Complexity 0.20: short prompt, simple task keywords",
       "estimated_cost": 0.0
     }
   }
   ```

4. **`POST /api/v1/complexity`** - Complexity estimation only (no LLM call)
   ```bash
   curl -X POST http://localhost:8080/api/v1/complexity \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Design a microservices architecture"}'

   # Returns: {"complexity": 0.8, "reasoning": "...", "recommended_model": "claude-sonnet"}
   ```

5. **`GET /api/v1/stats`** - Routing statistics
   ```bash
   curl http://localhost:8080/api/v1/stats
   # Returns: {total_requests, local_requests, cloud_requests, total_cost, avg_complexity}
   ```

6. **`GET /metrics`** - Prometheus metrics
   ```bash
   curl http://localhost:8080/metrics
   # Returns: Prometheus exposition format metrics
   ```

**`docker-compose.yml`** (Complete stack)
- 8 services: api-gateway, ollama-cpu, n8n, prometheus, grafana, redis, qdrant, postgres
- CPU and GPU profiles
- Volume mounts and networks
- Auto-pulls TinyLlama and Phi models on startup

### Deployment Scripts

**`install.sh`** (314 lines)
- NEVER runs as root (explicit check)
- Sudo keep-alive for long operations
- Idempotent package installation
- Docker, Ollama, Python setup
- Creates virtual environment
- Initializes Taskwarrior
- Creates .env from .env.example

**`deploy-all.sh`** (392 lines)
- One-command deployment for docker/aws/gcp
- Tier validation (1-4)
- Taskwarrior task creation
- Health checks
- Cost warnings for cloud deployments

### Configuration Files

**`.env.example`**
- Required: `ANTHROPIC_API_KEY`
- Optional: `OPENAI_API_KEY`
- Ollama URL, complexity thresholds
- Deployment tier and cloud provider

**`configs/prometheus.yml`**
- Scrapes API Gateway metrics every 15s
- Monitors Ollama health every 30s
- Alert rules for high costs, errors, slow responses

## Development Workflow

### Local Development

```bash
# 1. Install
./install.sh

# 2. Configure
nano .env  # Add ANTHROPIC_API_KEY

# 3. Deploy locally (CPU profile is default)
./deploy-all.sh docker

# Alternative: Use GPU profile (if NVIDIA GPU available)
docker-compose --profile gpu-nvidia up -d

# Alternative: AMD GPU
docker-compose --profile gpu-amd up -d

# 4. Test
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?"}'

# 5. View logs
docker-compose logs -f api-gateway

# 6. Run tests
source venv/bin/activate
pytest tests/ -v
```

### Cloud Deployment

```bash
# AWS Tier 2 (Standard: 4GB RAM, 2 CPU, $52/mo)
./deploy-all.sh aws 2

# GCP Tier 3 (Performance: 8GB RAM, 4 CPU, $120/mo)
./deploy-all.sh gcp 3
```

### Docker Profile System

The system uses Docker Compose profiles for hardware optimization:

- **`cpu`** (default) - CPU-only Ollama, works everywhere
- **`gpu-nvidia`** - NVIDIA GPU acceleration with CUDA
- **`gpu-amd`** - AMD GPU acceleration with ROCm

**When to switch profiles:**
- Staying on CPU? No action needed (default)
- Have NVIDIA GPU? Use `--profile gpu-nvidia`
- Have AMD GPU? Use `--profile gpu-amd`

## Common Development Tasks

### Modify Routing Logic

Edit `scripts/smart_router.py`:

```python
# Change complexity thresholds
COMPLEXITY_THRESHOLD_TINY = 0.3  # Default
COMPLEXITY_THRESHOLD_PHI = 0.6   # Default

# Adjust factor weights
complexity = (
    factors['length'] * 0.3 +      # 30%
    factors['keywords'] * 0.3 +    # 30%
    factors['code'] * 0.25 +       # 25%
    factors['task_type'] * 0.15    # 15%
)
```

### Add New Endpoint

Edit `gateway/app.py`:

```python
@app.route('/api/v1/your-endpoint', methods=['POST'])
def your_endpoint():
    # Your logic here
    return jsonify({'result': 'success'}), 200
```

### Add Custom Workflow

Create JSON file in `workflows/`:
- Use n8n UI to design workflow
- Export as JSON
- Place in `workflows/` directory
- Import via n8n UI at http://localhost:5678

### Modify Terraform Deployment

Edit `terraform/aws/main.tf` or `terraform/gcp/main.tf`:
- Instance types defined in `variables.tf`
- User data scripts install system on boot
- Security groups configured for required ports

## Testing

### Run Test Suite

```bash
source venv/bin/activate
pytest tests/ -v

# With coverage
pytest --cov=scripts tests/

# Test routing logic directly
python tests/test_router.py

# Single test class
pytest tests/test_router.py::TestComplexityEstimation -v

# Single test method
pytest tests/test_router.py::TestComplexityEstimation::test_simple_question -v
```

### Test Specific Components

```bash
# Test complexity estimation
python -c "
from scripts.smart_router import SmartRouter
router = SmartRouter()
complexity, reasoning = router.estimate_complexity('What is Python?')
print(f'Complexity: {complexity}, Reasoning: {reasoning}')
"

# Test Ollama connection
curl http://localhost:11434/api/generate \
  -d '{"model": "tinyllama", "prompt": "test", "stream": false}'

# Test Claude routing
curl -X POST http://localhost:8080/api/v1/chat \
  -d '{"prompt": "Write a complex algorithm"}' -H "Content-Type: application/json"

# Test with manual model override
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?", "model": "phi2"}'
```

### Benchmark Routing Accuracy

The `prompts/prompt_templates.py` module provides categorized test prompts:

```bash
# View prompt library statistics
python prompts/prompt_templates.py

# Test routing accuracy with benchmark suite
python -c "
from prompts.prompt_templates import PromptLibrary
from scripts.smart_router import SmartRouter

router = SmartRouter()
suite = PromptLibrary.get_benchmark_suite()

for prompt_template in suite:
    complexity, _ = router.estimate_complexity(prompt_template.prompt)
    selected_model = router.select_model(complexity)
    match = '✓' if selected_model == prompt_template.expected_model else '✗'
    print(f'{match} Expected: {prompt_template.expected_model}, Got: {selected_model}')
"
```

## Monitoring & Observability

### Prometheus Metrics

Key metrics exported by API Gateway:
- `api_gateway_requests_total{model, backend, status}` - Total requests
- `api_gateway_request_duration_seconds{model, backend}` - Latency
- `api_gateway_cost_total{model}` - Cumulative costs

Access: http://localhost:9090

### Grafana Dashboards

Pre-configured dashboards:
- Request distribution (local vs cloud)
- Cost tracking and trends
- Latency heatmaps
- Model performance

Access: http://localhost:3000 (admin/admin)

### Taskwarrior Tracking

Every AI request creates a task:
```bash
# View routing tasks
task project:vps_ai.router list

# Cost report
source scripts/tw-helper.sh
tw_cost_report

# Routing statistics
tw_routing_stats
```

## Cost Optimization

### Current Strategy

- **Simple queries** (40-50% of traffic) → TinyLlama → $0
- **Medium queries** (20-30% of traffic) → Phi-2 → $0
- **Complex queries** (20-30% of traffic) → Claude → $0.003-0.015 each

**Result**: 60-80% cost reduction vs. cloud-only

### Optimization Opportunities

1. **Adjust thresholds** - Make routing more aggressive (more local, less cloud)
2. **Cache responses** - Redis caching for common queries
3. **Batch processing** - Group similar requests
4. **Model cascading** - Try local first, fallback to cloud if quality poor
5. **Time-based routing** - Use local during peak hours, cloud during off-peak

## VPS Tier Recommendations

| Tier | RAM | CPU | Cost/mo | Models | Local % | Savings |
|------|-----|-----|---------|--------|---------|---------|
| 1 | 2GB | 1 | $26 | TinyLlama | 30% | 30% |
| 2 | 4GB | 2 | $52 | TinyLlama + Phi-2 | 70% | 60-70% |
| 3 | 8GB | 4 | $120 | + Mistral-7B | 85% | 75-85% |
| 4 | 16GB+GPU | 8 | $310 | All + GPU | 95% | 85-95% |

**Recommended**: Tier 2 for most production use cases

## Potential Modifications

### Switch to Vertex AI (Instead of Claude)

If user has GCP access with startup credits:

1. Modify `scripts/smart_router.py`:
```python
def execute_vertex_ai_request(self, prompt):
    """Execute request on Vertex AI Gemini"""
    from google.cloud import aiplatform
    # Implementation here
```

2. Update `.env`:
```bash
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
VERTEX_AI_MODEL=gemini-1.5-flash  # or gemini-1.5-pro
```

3. Benefits:
- Free during startup program
- Gemini 1.5 Flash is fast
- Gemini 1.5 Pro rivals Claude
- Better GCP ecosystem integration

### Add GPT-4 Support

Modify `scripts/smart_router.py`:
```python
def execute_openai_request(self, prompt):
    """Execute request on OpenAI GPT-4"""
    import openai
    # Implementation here
```

## Important Conventions

### Error Handling

All functions should:
- Return dict with `success`, `error`, `data` keys
- Log errors with context
- Never expose API keys in logs
- Gracefully degrade (use fallback model if primary fails)

**Example pattern from `smart_router.py`:**
```python
def execute_ollama_request(self, model: str, prompt: str) -> Dict:
    """Execute request on local Ollama server"""
    try:
        response = requests.post(endpoint, json=payload, timeout=60)
        response.raise_for_status()
        return {
            'model': model,
            'backend': 'local',
            'response': result.get('response', ''),
            'cost': 0.0
        }
    except Exception as e:
        logger.error(f"Ollama request failed: {e}")
        raise  # Or fallback to cloud model
```

### Logging

- Use Python `logging` module
- Log levels: DEBUG, INFO, WARNING, ERROR
- Include request ID for tracing
- Log costs and model selections

**Current log format (gateway/app.py:25-28):**
```python
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Code Style

- Follow PEP 8
- Type hints where appropriate
- Docstrings for all functions
- Comments for complex logic
- 80-character line limit (flexible)

**Type hints example:**
```python
def estimate_complexity(self, prompt: str) -> Tuple[float, str]:
    """Estimate prompt complexity on 0-1 scale"""
    # Implementation...
    return final_score, reasoning
```

## Security Considerations

1. **API Keys**: Never commit to git, use `.env`
2. **Docker**: Containers run as non-root user
3. **Network**: Security groups limit access to required ports
4. **Secrets**: Use cloud provider secrets managers in production
5. **CORS**: Configure appropriately for your use case

## Deployment Checklist

Before deploying to production:

- [ ] API keys configured in `.env`
- [ ] Health checks passing: `curl http://localhost:8080/health`
- [ ] Models pulled: `docker exec ollama ollama list`
- [ ] Tests passing: `pytest tests/`
- [ ] Monitoring configured (Prometheus, Grafana)
- [ ] Backup strategy defined
- [ ] Scaling plan documented
- [ ] Cost alerts configured

## Support Resources

- **Documentation**: See `docs/` directory (12 comprehensive guides)
- **Examples**:
  - `scripts/moderation_pipeline.py` - Content moderation (95% cost savings example)
  - `scripts/support_router.py` - Customer support routing
  - `prompts/prompt_templates.py` - Benchmark prompts library (20+ categorized prompts)
- **Tests**: See `tests/test_router.py` for testing patterns
- **Workflows**: See `workflows/` for n8n automation examples

## Example Use Cases (With Code)

### Content Moderation Pipeline

The `scripts/moderation_pipeline.py` demonstrates a two-stage approach:

1. **Stage 1**: TinyLlama classifies content as SAFE/FLAGGED (free)
2. **Stage 2**: Claude reviews only flagged content (paid)

**Cost Savings**: 95% reduction vs. cloud-only
- Cloud Only: 1,000 posts × $0.015 = $15.00
- Hybrid: 950 safe (local) + 50 flagged (cloud) = $0.75

**Usage:**
```bash
python scripts/moderation_pipeline.py
```

### Customer Support Routing

The `scripts/support_router.py` routes based on query complexity:
- FAQs → TinyLlama (instant, free)
- Technical questions → Phi-2 (fast, free)
- Complex issues → Claude (accurate, paid)

**Cost Savings**: 70% reduction

### Prompt Benchmarking

Use `prompts/prompt_templates.py` to test routing accuracy:

```python
from prompts.prompt_templates import PromptLibrary

# Get all simple prompts (should route to TinyLlama)
simple = PromptLibrary.get_by_complexity('low')

# Get all complex prompts (should route to Claude)
complex = PromptLibrary.get_by_complexity('high')

# Get benchmark suite (balanced)
suite = PromptLibrary.get_benchmark_suite()
```

## Troubleshooting Common Issues

### Ollama Models Not Pulled

**Symptom**: API Gateway returns "model not found"

**Solution**:
```bash
# Check which models are available
docker exec ollama ollama list

# Pull missing models manually
docker exec ollama ollama pull tinyllama
docker exec ollama ollama pull phi

# Verify models work
docker exec ollama ollama run tinyllama "Hello"
```

### API Gateway Returns 500 Error

**Symptom**: Chat endpoint fails with 500 Internal Server Error

**Check list**:
```bash
# 1. Verify ANTHROPIC_API_KEY is set
cat .env | grep ANTHROPIC_API_KEY

# 2. Check API Gateway logs
docker-compose logs -f api-gateway

# 3. Verify Ollama is running
curl http://localhost:11434/api/tags

# 4. Test health endpoint
curl http://localhost:8080/health
```

### Docker Compose Fails to Start

**Symptom**: Services crash on startup

**Common causes**:
```bash
# Port conflicts (8080, 11434, 5678 already in use)
sudo lsof -i :8080
sudo lsof -i :11434

# Insufficient memory (need 4GB+ for Tier 2)
free -h

# Fix: Stop conflicting services or change ports in .env
```

### Routing Always Uses Claude (Not Local Models)

**Symptom**: All requests go to Claude, costs are high

**Check**:
```bash
# Verify USE_LOCAL_FOR_SIMPLE is true
cat .env | grep USE_LOCAL_FOR_SIMPLE

# Test complexity estimation
python -c "
from scripts.smart_router import SmartRouter
router = SmartRouter()
complexity, reasoning = router.estimate_complexity('What is Python?')
print(f'Complexity: {complexity} (should be < 0.3)')
print(f'Reasoning: {reasoning}')
"

# Verify Ollama is reachable from gateway container
docker exec api-gateway curl http://ollama:11434/api/tags
```

### High Memory Usage

**Symptom**: System runs out of RAM

**Models' memory requirements:**
- TinyLlama: ~700MB
- Phi-2: ~1.6GB
- Mistral-7B: ~4GB
- All services: ~1GB overhead

**Solutions**:
```bash
# Check current memory usage
docker stats

# Remove unused models
docker exec ollama ollama rm mistral

# Use smaller tier (remove Phi-2, keep only TinyLlama)
# Or upgrade to Tier 3 (8GB RAM)
```

### Slow Local Model Responses

**Symptom**: TinyLlama/Phi-2 take 5+ seconds

**This is normal on CPU-only systems**. Options:

1. **Use GPU profile** (if GPU available):
   ```bash
   docker-compose --profile gpu-nvidia up -d
   ```

2. **Adjust complexity thresholds** (use local less):
   ```bash
   # In .env
   COMPLEXITY_THRESHOLD=0.4  # More aggressive routing to Claude
   ```

3. **Accept latency trade-off** (saves money, but slower)

## Known Limitations

1. **Ollama CPU**: Slower than GPU (1-5s per request) - expected behavior
2. **Complexity Estimation**: Heuristic-based, not ML-based (requires manual tuning)
3. **Model Quality**: Local models (1-3B params) inferior to Claude (175B+) for complex tasks
4. **Scaling**: Single-server setup (can be load-balanced but needs custom setup)
5. **Context**: Local models have smaller context windows (2-4K vs Claude's 200K)
6. **No Streaming**: Current implementation doesn't stream responses (future enhancement)

## Future Enhancements

Potential improvements:
- [ ] Multi-model ensembles
- [ ] Active learning from user feedback
- [ ] A/B testing framework
- [ ] Cost prediction ML model
- [ ] Automatic threshold tuning
- [ ] Multi-language support
- [ ] Streaming responses
- [ ] WebSocket support

## Contact & Contribution

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Pull Requests**: Always welcome with tests

---

## Quick Reference: Common Commands

```bash
# Installation and setup
./install.sh                              # One-time setup
nano .env                                 # Configure API keys
./deploy-all.sh docker                    # Deploy locally

# Development
source venv/bin/activate                  # Activate Python environment
pytest tests/ -v                          # Run tests
python scripts/smart_router.py            # Test router directly
python prompts/prompt_templates.py        # View prompt library

# Docker management
docker-compose up -d                      # Start all services
docker-compose down                       # Stop all services
docker-compose logs -f api-gateway        # View logs
docker-compose restart ollama-cpu         # Restart Ollama
docker exec ollama ollama list            # List models
docker exec ollama ollama pull tinyllama  # Pull model

# Testing
curl http://localhost:8080/health         # Health check
curl -X POST http://localhost:8080/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "test"}'                 # Test routing

# Monitoring
curl http://localhost:8080/api/v1/stats   # Routing statistics
curl http://localhost:8080/metrics        # Prometheus metrics
task project:vps_ai.router list           # Taskwarrior tasks

# Troubleshooting
docker-compose logs -f api-gateway        # Debug API issues
docker exec ollama ollama list            # Check models
cat .env | grep ANTHROPIC_API_KEY         # Verify config
```

---

**Last Updated**: January 2025
**Version**: 1.0.0
**Status**: Production-ready
**Maintainer**: Jeremy Longshore
