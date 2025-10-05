# Integrate Ternary Quantization (BitNet 1.58-bit) into Bob's Brain

**Date**: 2025-10-05
**Purpose**: Add 6x faster Slack responses with ternary quantization support

---

## Overview

Integrate Microsoft BitNet 1.58-bit ternary quantization into Bob's Brain Slack bot for:
- **6x faster inference** on CPU
- **82% energy reduction**
- **16x less RAM** (run 7B models on 8GB)
- **Handle 85% of Slack queries locally** (vs 70% before)

---

## Source Material

All implementation code and documentation is in:
- **Implementation**: `/home/jeremy/projects/hybrid-ai-stack/scripts/`
- **Documentation**: `/home/jeremy/projects/hybrid-ai-stack/docs/TERNARY.md`
- **Smart router**: `/home/jeremy/projects/hybrid-ai-stack/scripts/smart_router.py`

---

## Step-by-Step Integration

### 1. Copy Ternary Infrastructure

```bash
cd /home/jeremy/projects/bobs-brain

# Copy installation scripts
cp /home/jeremy/projects/hybrid-ai-stack/scripts/install_ternary.sh .
cp /home/jeremy/projects/hybrid-ai-stack/scripts/download_ternary_models.sh .
cp /home/jeremy/projects/hybrid-ai-stack/scripts/ternary_server.py .
cp /home/jeremy/projects/hybrid-ai-stack/scripts/setup_ternary_service.sh .
cp /home/jeremy/projects/hybrid-ai-stack/scripts/benchmark_ternary.py .

# Make executable
chmod +x install_ternary.sh download_ternary_models.sh setup_ternary_service.sh
```

### 2. Install BitNet.cpp Runtime

```bash
# Install BitNet.cpp (installs to ~/ai_stack/bitnet.cpp)
./install_ternary.sh

# Download models (choose option 1: Microsoft BitNet 2B - RECOMMENDED)
./download_ternary_models.sh

# Setup as systemd service (runs ternary server on port 8003)
./setup_ternary_service.sh

# Verify installation
curl http://localhost:8003/health

# Expected response:
# {
#   "status": "healthy",
#   "ternary": true,
#   "framework": "BitNet.cpp",
#   "models_available": ["bitnet-2b", "falcon3-7b"]
# }
```

### 3. Update Bob's Brain Smart Router

**File to modify**: `bob_brain/routers/smart_router.py`

Add these changes:

#### 3.1 Add Ternary Model Configurations

```python
# In SmartRouter class, update MODELS dict:

MODELS = {
    'tinyllama': {
        'backend': 'local',
        'max_complexity': 0.3,
        'cost_per_token': 0.0,
        'endpoint': 'http://localhost:11434/api/generate'
    },
    'phi2': {
        'backend': 'local',
        'max_complexity': 0.6,
        'cost_per_token': 0.0,
        'endpoint': 'http://localhost:11434/api/generate'
    },
    # NEW: Ternary models (BitNet 1.58-bit)
    'bitnet-2b': {
        'backend': 'ternary',
        'max_complexity': 0.5,
        'cost_per_token': 0.0,
        'endpoint': 'http://localhost:8003/generate',
        'speed_multiplier': 6.0,  # 6x faster
        'energy_savings': 0.82    # 82% reduction
    },
    'mistral-7b-ternary': {
        'backend': 'ternary',
        'max_complexity': 0.8,
        'cost_per_token': 0.0,
        'endpoint': 'http://localhost:8003/generate',
        'speed_multiplier': 6.0,
        'energy_savings': 0.82
    },
    'gemini-flash': {
        'backend': 'cloud',
        'max_complexity': 1.0,
        'cost_per_1m_tokens': 0.075,
        'cost_per_token': 0.000000075
    }
}
```

#### 3.2 Add Ternary Availability Check

```python
def __init__(self, use_local: bool = True, use_ternary: bool = True):
    """Initialize router with ternary support"""
    self.use_local = use_local
    self.use_ternary = use_ternary
    self.ternary_available = False

    # Check if ternary runtime is available
    if self.use_ternary:
        self.ternary_available = self._check_ternary_available()
        if self.ternary_available:
            logger.info("✅ Ternary runtime detected and available")
        else:
            logger.info("ℹ️  Ternary runtime not available, using standard models")

    # ... rest of initialization

def _check_ternary_available(self) -> bool:
    """Check if ternary runtime is running"""
    try:
        ternary_url = os.getenv('TERNARY_URL', 'http://localhost:8003')
        response = requests.get(f"{ternary_url}/health", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get('ternary', False)
        return False
    except:
        return False
```

#### 3.3 Update Model Selection Logic

```python
def select_model(self, complexity: float) -> str:
    """Select optimal model with ternary support"""
    # Ternary-optimized routing (if available)
    if self.ternary_available:
        if complexity < 0.5:
            return 'bitnet-2b'  # Fast 2B model
        elif complexity < 0.8:
            return 'mistral-7b-ternary'  # 7B quality, 2.5GB RAM
        else:
            return 'gemini-flash'  # Ultra-complex only
    # Standard routing (fallback)
    elif not self.use_local or complexity > 0.6:
        return 'gemini-flash'
    elif complexity < 0.3:
        return 'tinyllama'
    else:
        return 'phi2'
```

#### 3.4 Add Ternary Request Execution

```python
def execute_ternary_request(self, model: str, prompt: str) -> Dict:
    """Execute request on ternary model server"""
    ternary_url = os.getenv('TERNARY_URL', 'http://localhost:8003')
    endpoint = f"{ternary_url}/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": 512
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        return {
            'model': model,
            'backend': 'ternary',
            'response': result.get('text', ''),
            'inference_time_ms': result.get('inference_time_ms', 0),
            'tokens_per_second': result.get('tokens_per_second', 0),
            'cost': 0.0,
            'quantization': '1.58-bit'
        }
    except Exception as e:
        logger.error(f"Ternary request failed: {e}, falling back to cloud")
        return self.execute_gemini_request(prompt)

def process_request(self, prompt: str) -> Dict:
    """Main request processing with ternary support"""
    decision = self.route_request(prompt)

    # Execute based on backend
    if decision.backend == 'ternary':
        result = self.execute_ternary_request(decision.model, prompt)
    elif decision.backend == 'local':
        result = self.execute_ollama_request(decision.model, prompt)
    else:
        result = self.execute_gemini_request(prompt)

    # Add routing metadata
    result['routing'] = {
        'complexity': decision.complexity,
        'reasoning': decision.reasoning,
        'estimated_cost': decision.estimated_cost
    }

    return result
```

### 4. Update Environment Variables

**File**: `.env`

Add these variables:

```bash
# Ternary Configuration
USE_TERNARY=true
TERNARY_URL=http://localhost:8003
```

### 5. Update Slack Integration

Ensure Slack message handler uses the enhanced smart router:

**File**: `bob_brain/slack/handlers.py` (or wherever Slack messages are processed)

```python
from bob_brain.routers.smart_router import SmartRouter

# Initialize router with ternary support
router = SmartRouter(use_ternary=True)

async def handle_slack_message(event):
    """Process Slack message with ternary routing"""
    message_text = event.get('text', '')

    # Route and execute
    result = router.process_request(message_text)

    # Send response to Slack
    response_text = result['response']

    # Optional: Add metadata for debugging
    metadata = f"\n_Model: {result['model']} | " \
               f"Backend: {result['backend']} | " \
               f"Cost: ${result['cost']:.6f}_"

    return {
        'text': response_text,
        'metadata': metadata  # Only show in debug mode
    }
```

### 6. Testing

#### Test Ternary Server Directly

```bash
# Simple query (should use BitNet 2B)
curl -X POST http://localhost:8003/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Python?", "model": "bitnet-2b"}'

# Complex query (should use Mistral-7B ternary)
curl -X POST http://localhost:8003/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing", "model": "mistral-7b-ternary"}'
```

#### Test Smart Router Integration

```python
# Test in Python
from bob_brain.routers.smart_router import SmartRouter

router = SmartRouter(use_ternary=True)

# Simple query
result = router.process_request("What is 2+2?")
print(f"Model: {result['model']}")  # Should be 'bitnet-2b'
print(f"Response: {result['response']}")

# Complex query
result = router.process_request("Write a Python function for binary search")
print(f"Model: {result['model']}")  # Should be 'mistral-7b-ternary'
```

#### Test Slack Integration

Send test messages to Bob in Slack:
1. **Simple**: "What is the capital of France?" → Should use BitNet 2B
2. **Medium**: "Explain machine learning" → Should use Mistral-7B ternary
3. **Complex**: "Design a microservices architecture" → Should use Gemini Flash

### 7. Performance Benchmarking

```bash
# Run comprehensive benchmark
python benchmark_ternary.py

# Expected output:
# BitNet 2B vs Phi-2: 2-6x faster
# Mistral-7B ternary: Runs on same hardware, better quality
# Energy savings: 82% reduction
```

### 8. Monitoring

**Check ternary server status:**
```bash
# Health check
curl http://localhost:8003/health

# View logs
sudo journalctl -u ternary-server -f

# Restart if needed
sudo systemctl restart ternary-server
```

**Check Bob's Brain logs:**
```bash
# Look for ternary routing messages
tail -f /var/log/bobs-brain/app.log | grep -i ternary
```

### 9. Documentation Updates

**File**: `CLAUDE.md`

Add section:

```markdown
## Ternary Quantization (BitNet 1.58-bit)

Bob's Brain now supports ternary quantization for 6x faster responses:

### Configuration
- **Environment**: `USE_TERNARY=true` in `.env`
- **Endpoint**: `http://localhost:8003` (ternary server)
- **Models**: BitNet 2B, Mistral-7B ternary

### Routing Logic
- Complexity < 0.5: BitNet 2B (local, 0.4GB RAM)
- Complexity 0.5-0.8: Mistral-7B ternary (local, 2.5GB RAM)
- Complexity > 0.8: Gemini Flash (cloud, paid)

### Performance
- 6x faster inference vs standard models
- 82% energy reduction
- Handles 85% of Slack queries locally

### Maintenance
- **Restart**: `sudo systemctl restart ternary-server`
- **Health**: `curl http://localhost:8003/health`
- **Logs**: `sudo journalctl -u ternary-server -f`
```

---

## Expected Results

After integration:

### Performance Improvements
- **Inference Speed**: 6x faster (0.5-1s vs 3-5s)
- **Energy Consumption**: 82% reduction
- **Memory Usage**: 16x smaller (2.5GB vs 40GB for 7B model)
- **Local Handling**: 85% of requests (vs 70% before)

### Cost Savings
- **Before**: 70% local, 30% cloud → $90/mo API costs (10K requests)
- **After**: 85% local, 15% cloud → $45/mo API costs
- **Savings**: $45/mo (50% reduction)

### Quality Trade-offs
- **Accuracy**: 2-3% lower than FP16 models
- **Context**: Limited to 4096 tokens (vs 128K for Gemini)
- **Models**: Fewer variants available

---

## Troubleshooting

### Ternary Server Won't Start

```bash
# Check if BitNet.cpp is installed
ls ~/ai_stack/bitnet.cpp

# Check if models are downloaded
ls ~/ai_stack/models/ternary

# Check service status
sudo systemctl status ternary-server

# View error logs
sudo journalctl -u ternary-server -n 50
```

### Smart Router Not Using Ternary

```python
# Test ternary availability check
from bob_brain.routers.smart_router import SmartRouter

router = SmartRouter(use_ternary=True)
print(f"Ternary available: {router.ternary_available}")

# If False, check:
# 1. Is ternary-server running? sudo systemctl status ternary-server
# 2. Is port 8003 accessible? curl http://localhost:8003/health
# 3. Environment variable set? echo $USE_TERNARY
```

### Model Not Found Error

```bash
# Re-download models
cd /home/jeremy/projects/bobs-brain
./download_ternary_models.sh

# Verify model files exist
ls ~/ai_stack/models/ternary/bitnet-2b/
```

---

## Reference Documentation

- **Full Technical Guide**: `/home/jeremy/projects/hybrid-ai-stack/docs/TERNARY.md`
- **VPS Tier 2.5**: `/home/jeremy/projects/hybrid-ai-stack/docs/VPS-TIERS.md`
- **Smart Router Source**: `/home/jeremy/projects/hybrid-ai-stack/scripts/smart_router.py`
- **BitNet GitHub**: https://github.com/microsoft/BitNet
- **BitNet Paper**: https://arxiv.org/abs/2402.17764

---

## Next Steps After Integration

1. **Monitor performance** for 1 week
2. **Compare costs** before/after
3. **Adjust complexity thresholds** if needed
4. **Consider upgrading to Mistral-7B ternary** as default
5. **Deploy to production** if successful

---

**Status**: Ready for implementation
**Estimated Time**: 1-2 hours
**Risk Level**: Low (fallback to cloud if ternary fails)

---

**Created**: 2025-10-05
**Last Updated**: 2025-10-05
