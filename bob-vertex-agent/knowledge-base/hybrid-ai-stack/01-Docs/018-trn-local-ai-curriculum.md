# VPS AI Orchestrator Stack - Practical Implementation Guide

> **For normal people using affordable VPS servers** - Real hardware, real models, real costs

## Table of Contents

1. [VPS Tier Recommendations & Model Selection](#vps-tier-recommendations--model-selection)
2. [Initial VPS Setup](#initial-vps-setup)
3. [Taskwarrior Installation](#taskwarrior-installation)
4. [Model Deployment by VPS Tier](#model-deployment-by-vps-tier)
5. [Cloud Orchestrator Setup](#cloud-orchestrator-setup)
6. [n8n Workflow Automation](#n8n-workflow-automation)
7. [Hybrid Architecture Examples](#hybrid-architecture-examples)
8. [Cost Optimization](#cost-optimization)

---

## VPS Tier Recommendations & Model Selection

### Tier 1: Budget VPS (Cloud-Only Orchestrator)
**Hardware:**
- 2GB RAM, 1 CPU
- 25GB SSD
- ~$6-12/month (Hetzner, Vultr)

**Model Strategy:**
- ❌ No local models (insufficient RAM)
- ✅ 100% cloud APIs (Claude, OpenAI, Groq)
- ✅ n8n for workflow automation
- ✅ Taskwarrior for tracking

**Use Case:** Pure orchestrator, no local inference

```bash
# Tier 1 setup tasks
task add "Setup Tier 1 VPS (cloud-only)" project:vps_ai.tier1 +budget
task add "Install n8n orchestrator" project:vps_ai.tier1.services depends:1
task add "Configure cloud API routing" project:vps_ai.tier1.config depends:2
```

**Monthly Cost Breakdown:**
- VPS: $6-12
- Claude API: $20-50 (moderate use)
- **Total: $26-62/month**

---

### Tier 2: Standard VPS (Tiny Models + Cloud)
**Hardware:**
- 4-8GB RAM, 2-4 CPUs
- 50GB SSD
- ~$20-40/month (DigitalOcean, Linode, Vultr)

**Recommended Models (CPU-Only):**

| Model | RAM Usage | Speed | Use Case |
|-------|-----------|-------|----------|
| **TinyLlama-1.1B-Chat** | ~2GB | Fast | Simple Q&A, classification |
| **Phi-2 (2.7B)** | ~4GB | Medium | Reasoning, coding assistance |
| **Qwen2-1.5B-Instruct** | ~2.5GB | Fast | General chat, summarization |
| **Gemma-2B-it** | ~3GB | Fast | Google's lightweight model |

**Architecture:**
- 🔹 Tiny local models for simple tasks (classification, routing, caching)
- 🔹 Cloud APIs for complex reasoning, code generation
- 🔹 Local models act as "gatekeepers" to reduce API costs

```bash
# Tier 2 setup tasks
task add "Setup Tier 2 VPS (hybrid)" project:vps_ai.tier2 +standard
task add "Install llama.cpp for CPU inference" project:vps_ai.tier2.local depends:1
task add "Download TinyLlama 1.1B GGUF" project:vps_ai.tier2.models depends:2
task add "Setup cloud API fallback" project:vps_ai.tier2.cloud depends:3
```

**Monthly Cost Breakdown:**
- VPS: $20-40
- Claude API: $10-30 (local models handle 60% of requests)
- **Total: $30-70/month**

---

### Tier 3: Performance VPS (Small Models + Cloud)
**Hardware:**
- 16GB RAM, 4-8 CPUs
- 100GB SSD
- ~$60-100/month (DigitalOcean CPU-Optimized, Hetzner CPX)

**Recommended Models (CPU-Only):**

| Model | RAM Usage | Speed | Use Case |
|-------|-----------|-------|----------|
| **Llama-3.2-3B-Instruct** | ~5GB | Medium | General purpose, good reasoning |
| **Mistral-7B-Instruct (Q4)** | ~6GB | Medium | Code, analysis, complex tasks |
| **Qwen2.5-7B-Instruct (Q4)** | ~7GB | Medium | Multilingual, strong performance |
| **Phi-3-Mini-4K (3.8B)** | ~5GB | Fast | Microsoft's efficient model |

**Architecture:**
- 🟢 Local models handle 80% of requests
- 🟢 Cloud APIs only for specialized tasks (image gen, advanced reasoning)
- 🟢 Model routing based on task complexity

```bash
# Tier 3 setup tasks
task add "Setup Tier 3 VPS (performance)" project:vps_ai.tier3 +performance
task add "Install Ollama for easy model management" project:vps_ai.tier3.local depends:1
task add "Download Mistral-7B-Instruct Q4_K_M" project:vps_ai.tier3.models depends:2
task add "Deploy model router service" project:vps_ai.tier3.router depends:3
```

**Monthly Cost Breakdown:**
- VPS: $60-100
- Claude API: $5-15 (local handles most work)
- **Total: $65-115/month**

---

### Tier 4: GPU VPS (Local First)
**Hardware:**
- 16GB+ RAM, GPU (RTX 3060 or better)
- 100GB+ SSD
- ~$150-300/month (RunPod, Vast.ai, Lambda Labs)

**Recommended Models (GPU):**

| Model | VRAM | Speed | Use Case |
|-------|------|-------|----------|
| **Mistral-7B-Instruct (FP16)** | ~14GB | Very Fast | Production inference |
| **Llama-3.1-8B-Instruct** | ~16GB | Very Fast | Meta's latest, excellent quality |
| **CodeLlama-13B** | ~24GB | Fast | Code generation specialist |
| **Mixtral-8x7B (Q4)** | ~24GB | Fast | Mixture of experts, high quality |

**Architecture:**
- 🟢 95% local GPU inference
- 🟢 Cloud only for vision, embeddings, or specialized tasks
- 🟢 Multiple models for different specializations

```bash
# Tier 4 setup tasks
task add "Setup GPU VPS" project:vps_ai.tier4 +gpu priority:H
task add "Install CUDA drivers" project:vps_ai.tier4.gpu depends:1 +critical
task add "Install vLLM for GPU inference" project:vps_ai.tier4.local depends:2
task add "Download Mistral-7B-Instruct FP16" project:vps_ai.tier4.models depends:3
```

**Monthly Cost Breakdown:**
- GPU VPS: $150-300
- Claude API: $0-10 (rare usage)
- **Total: $150-310/month**

---

## Initial VPS Setup

### Choose Your Tier

```bash
# First, decide your tier based on budget
task add "Determine VPS tier based on budget" project:vps_ai.planning +decision

# Tier selection guide:
# - Budget < $30/mo → Tier 1 (cloud-only)
# - Budget $30-70/mo → Tier 2 (tiny models + cloud)
# - Budget $70-120/mo → Tier 3 (small models + cloud)
# - Budget $120+/mo → Tier 4 (GPU)

# For this guide, we'll focus on Tier 2 (most practical for normal users)
```

### VPS Provider Setup (Tier 2 Example)

```bash
# Create VPS (DigitalOcean, Linode, Vultr)
# - Choose: Ubuntu 22.04 LTS
# - Size: 4GB RAM / 2 CPUs ($24/mo on DigitalOcean)
# - Region: Closest to you

# SSH into your VPS
ssh root@your-vps-ip

# Update system
task add "Update VPS system packages" project:vps_ai.tier2.setup +setup
task start 1

apt update && apt upgrade -y
apt install -y curl wget git vim htop python3.11 python3.11-venv python3-pip

task 1 annotate "System updated on $(date)"
task 1 done
```

### Create Application Directory

```bash
task add "Create application structure" project:vps_ai.tier2.setup +filesystem
task start 2

# Create app user
adduser aistack
usermod -aG sudo aistack
su - aistack

# Create directories
mkdir -p ~/ai_stack/{models,configs,scripts,workflows,prompts,logs}

task 2 annotate "Directory structure created at ~/ai_stack"
task 2 done
```

### Install Python Environment

```bash
task add "Setup Python environment" project:vps_ai.tier2.setup +python
task start 3

cd ~/ai_stack
python3.11 -m venv venv
source venv/bin/activate

# Install core dependencies
pip install --upgrade pip
pip install anthropic openai requests flask python-dotenv

task 3 annotate "Python 3.11 venv created with core packages"
task 3 done
```

### Install Docker for n8n

```bash
task add "Install Docker and Docker Compose" project:vps_ai.tier2.setup +docker
task start 4

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker aistack

# Log out and back in
exit
su - aistack

docker --version

task 4 annotate "Docker installed successfully"
task 4 done
```

---

## Taskwarrior Installation

```bash
task add "Install Taskwarrior" project:vps_ai.tools.taskwarrior +setup
task start 5

sudo apt install -y taskwarrior

# Configure
task config default.project vps_ai
task config urgency.user.tag.critical.coefficient 10.0

# Create project structure
cat > ~/ai_stack/taskwarrior_projects.txt << 'EOF'
# VPS AI Stack Projects

vps_ai.tier2                  # Tier 2 VPS setup
vps_ai.tier2.setup            # Initial setup
vps_ai.tier2.local            # Local model setup
vps_ai.tier2.cloud            # Cloud API config
vps_ai.tier2.router           # Request routing

vps_ai.tools.taskwarrior      # Taskwarrior setup
vps_ai.tools.n8n              # n8n automation

vps_ai.models                 # Model management
vps_ai.prompts                # Prompt engineering

vps_ai.production             # Production deployment
EOF

task 5 annotate "Taskwarrior configured with project structure"
task 5 done
```

---

## Model Deployment by VPS Tier

### Tier 2: TinyLlama + Phi-2 Setup (4-8GB RAM)

#### Install llama.cpp (CPU Inference)

```bash
task add "Install llama.cpp for CPU inference" project:vps_ai.tier2.local +setup
task start 6

cd ~/ai_stack
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
make -j

# Verify build
./main --version

task 6 annotate "llama.cpp built successfully (CPU only)"
task 6 done
```

#### Download Optimized Models

```bash
task add "Download TinyLlama 1.1B GGUF" project:vps_ai.tier2.models +download
task start 7

# Install Hugging Face CLI
pip install huggingface-hub

# Download TinyLlama (1.1B - very fast on CPU)
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF \
    tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
    --local-dir ~/ai_stack/models/tinyllama \
    --local-dir-use-symlinks False

task 7 annotate "TinyLlama 1.1B downloaded (~700MB)"
task 7 done

# Download Phi-2 (2.7B - better quality, slower)
task add "Download Phi-2 2.7B GGUF" project:vps_ai.tier2.models +download
task start 8

huggingface-cli download TheBloke/phi-2-GGUF \
    phi-2.Q4_K_M.gguf \
    --local-dir ~/ai_stack/models/phi2 \
    --local-dir-use-symlinks False

task 8 annotate "Phi-2 2.7B downloaded (~1.6GB)"
task 8 done
```

#### Start Local Model Servers

```bash
task add "Start TinyLlama server" project:vps_ai.tier2.local +service
task start 9

# Create systemd service for TinyLlama
sudo tee /etc/systemd/system/tinyllama.service > /dev/null << 'EOF'
[Unit]
Description=TinyLlama 1.1B Server
After=network.target

[Service]
Type=simple
User=aistack
WorkingDirectory=/home/aistack/ai_stack/llama.cpp
ExecStart=/home/aistack/ai_stack/llama.cpp/server \
    -m /home/aistack/ai_stack/models/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf \
    -c 2048 \
    --threads 2 \
    --host 0.0.0.0 \
    --port 8001
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable tinyllama.service
sudo systemctl start tinyllama.service

# Verify
curl http://localhost:8001/health

task 9 annotate "TinyLlama server running on port 8001"
task 9 done
```

```bash
# Start Phi-2 server
task add "Start Phi-2 server" project:vps_ai.tier2.local +service
task start 10

sudo tee /etc/systemd/system/phi2.service > /dev/null << 'EOF'
[Unit]
Description=Phi-2 2.7B Server
After=network.target

[Service]
Type=simple
User=aistack
WorkingDirectory=/home/aistack/ai_stack/llama.cpp
ExecStart=/home/aistack/ai_stack/llama.cpp/server \
    -m /home/aistack/ai_stack/models/phi2/phi-2.Q4_K_M.gguf \
    -c 2048 \
    --threads 3 \
    --host 0.0.0.0 \
    --port 8002
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable phi2.service
sudo systemctl start phi2.service

# Verify
curl http://localhost:8002/health

task 10 annotate "Phi-2 server running on port 8002"
task 10 done
```

#### Alternative: Ollama (Easier Management)

```bash
# Ollama is easier for beginners
task add "Install Ollama (alternative)" project:vps_ai.tier2.local +alternative
task start 11

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models (Ollama handles everything)
ollama pull tinyllama      # 637MB
ollama pull phi            # 1.6GB
ollama pull qwen2:1.5b     # 934MB

# Ollama auto-starts on port 11434
curl http://localhost:11434/api/tags

task 11 annotate "Ollama installed with 3 models"
task 11 done
```

**Ollama Model Recommendations by RAM:**

| RAM | Recommended Models | Command |
|-----|-------------------|---------|
| 2GB | tinyllama | `ollama pull tinyllama` |
| 4GB | phi, qwen2:1.5b | `ollama pull phi` |
| 8GB | llama3.2:3b, phi3 | `ollama pull llama3.2:3b` |
| 16GB | mistral, qwen2.5:7b | `ollama pull mistral` |

### Tier 3: Mistral-7B Setup (16GB RAM)

```bash
task add "Setup Tier 3 with Mistral-7B" project:vps_ai.tier3 +performance
task start 12

# Using Ollama for easier management
ollama pull mistral           # 4.1GB (Q4 quantized)
ollama pull qwen2.5:7b        # 4.7GB

# Or using llama.cpp for more control
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF \
    mistral-7b-instruct-v0.2.Q4_K_M.gguf \
    --local-dir ~/ai_stack/models/mistral \
    --local-dir-use-symlinks False

task 12 annotate "Mistral-7B deployed (4.1GB Q4 quantized)"
task 12 done
```

### Performance Benchmarks (Real World)

| Model | VPS Tier | RAM Used | Speed (tokens/sec) | Quality | Cost/1M tokens |
|-------|----------|----------|-------------------|---------|----------------|
| TinyLlama 1.1B | Tier 2 | ~2GB | 30-50 | Basic | $0 (local) |
| Phi-2 2.7B | Tier 2 | ~4GB | 15-25 | Good | $0 (local) |
| Llama 3.2 3B | Tier 3 | ~5GB | 20-35 | Very Good | $0 (local) |
| Mistral 7B Q4 | Tier 3 | ~6GB | 10-20 | Excellent | $0 (local) |
| Claude Sonnet | Any | 0 | N/A | Best | $3 |
| GPT-4o-mini | Any | 0 | N/A | Excellent | $0.15 |

---

## Cloud Orchestrator Setup

### API Configuration

```bash
task add "Configure cloud API keys" project:vps_ai.tier2.cloud +setup
task start 13

# Create .env file
cat > ~/ai_stack/.env << 'EOF'
# Cloud API Keys
ANTHROPIC_API_KEY=your_claude_key_here
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here  # Free tier: 30 req/min

# Local endpoints
TINYLLAMA_URL=http://localhost:8001
PHI2_URL=http://localhost:8002
OLLAMA_URL=http://localhost:11434

# Routing config
USE_LOCAL_FOR_SIMPLE=true
COMPLEXITY_THRESHOLD=0.5
EOF

chmod 600 ~/ai_stack/.env

task 13 annotate "API keys configured in .env"
task 13 done
```

### Smart Router Implementation

```bash
task add "Build intelligent request router" project:vps_ai.tier2.router +critical
task start 14

cat > ~/ai_stack/scripts/smart_router.py << 'EOF'
#!/usr/bin/env python3
"""
Smart Router - Routes requests to local or cloud based on complexity
"""

import os
from anthropic import Anthropic
import requests
from dotenv import load_dotenv
import re

load_dotenv('/home/aistack/ai_stack/.env')

class SmartRouter:
    def __init__(self):
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.local_endpoints = {
            'tinyllama': os.getenv('TINYLLAMA_URL'),
            'phi2': os.getenv('PHI2_URL'),
            'ollama': os.getenv('OLLAMA_URL')
        }
    
    def estimate_complexity(self, prompt: str) -> float:
        """Estimate prompt complexity (0-1)"""
        complexity_score = 0.0
        
        # Length factor
        if len(prompt) > 500:
            complexity_score += 0.3
        elif len(prompt) > 200:
            complexity_score += 0.2
        else:
            complexity_score += 0.1
        
        # Keyword analysis
        complex_keywords = [
            'analyze', 'explain', 'write code', 'debug', 'optimize',
            'design', 'architect', 'compare', 'evaluate', 'research'
        ]
        
        simple_keywords = [
            'summarize', 'list', 'what is', 'define', 'yes or no'
        ]
        
        prompt_lower = prompt.lower()
        
        if any(kw in prompt_lower for kw in complex_keywords):
            complexity_score += 0.4
        elif any(kw in prompt_lower for kw in simple_keywords):
            complexity_score += 0.1
        else:
            complexity_score += 0.2
        
        # Code detection
        if re.search(r'```|def |class |function|import ', prompt):
            complexity_score += 0.3
        
        return min(complexity_score, 1.0)
    
    def route_request(self, prompt: str, max_tokens: int = 512):
        """Route to appropriate model"""
        
        complexity = self.estimate_complexity(prompt)
        
        print(f"📊 Complexity Score: {complexity:.2f}")
        
        # Simple requests → TinyLlama (fastest, cheapest)
        if complexity < 0.3:
            print("🚀 Routing to: TinyLlama (local)")
            return self.call_local_ollama(prompt, 'tinyllama', max_tokens)
        
        # Medium requests → Phi-2 (good balance)
        elif complexity < 0.6:
            print("🔵 Routing to: Phi-2 (local)")
            return self.call_local_ollama(prompt, 'phi', max_tokens)
        
        # Complex requests → Claude (best quality)
        else:
            print("☁️  Routing to: Claude Sonnet (cloud)")
            return self.call_claude(prompt, max_tokens)
    
    def call_local_ollama(self, prompt: str, model: str, max_tokens: int):
        """Call Ollama API"""
        try:
            response = requests.post(
                f"{self.local_endpoints['ollama']}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "response": result['response'],
                    "model": f"ollama:{model}",
                    "cost": 0.0
                }
            else:
                print(f"❌ Local model error, falling back to cloud")
                return self.call_claude(prompt, max_tokens)
                
        except Exception as e:
            print(f"❌ Error calling local: {e}, using cloud")
            return self.call_claude(prompt, max_tokens)
    
    def call_claude(self, prompt: str, max_tokens: int):
        """Call Claude API"""
        message = self.anthropic.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Estimate cost (Claude Sonnet 4.5: $3 per 1M input tokens)
        input_tokens = len(prompt.split()) * 1.3  # rough estimate
        output_tokens = len(message.content[0].text.split()) * 1.3
        cost = (input_tokens * 3 / 1_000_000) + (output_tokens * 15 / 1_000_000)
        
        return {
            "response": message.content[0].text,
            "model": "claude-sonnet-4-5",
            "cost": cost
        }

def main():
    router = SmartRouter()
    
    # Test cases
    test_prompts = [
        "What is the capital of France?",  # Simple → TinyLlama
        "Explain quantum computing in simple terms",  # Medium → Phi-2
        "Write a Python script to scrape a website, handle errors, and save to database"  # Complex → Claude
    ]
    
    total_cost = 0.0
    
    for prompt in test_prompts:
        print(f"\n{'='*60}")
        print(f"Prompt: {prompt}")
        print(f"{'='*60}")
        
        result = router.route_request(prompt)
        
        print(f"\n📝 Response ({result['model']}):")
        print(result['response'][:200] + "..." if len(result['response']) > 200 else result['response'])
        print(f"\n💰 Cost: ${result['cost']:.6f}")
        
        total_cost += result['cost']
    
    print(f"\n{'='*60}")
    print(f"Total Cost: ${total_cost:.6f}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
EOF

chmod +x ~/ai_stack/scripts/smart_router.py

task 14 annotate "Smart router created - routes by complexity"
task 14 done
```

### Test the Router

```bash
task add "Test smart router" project:vps_ai.tier2.router +testing
task start 15

source ~/ai_stack/venv/bin/activate
python ~/ai_stack/scripts/smart_router.py

task 15 annotate "Router tested successfully - local models handling 60-70% of requests"
task 15 done
```

---

## n8n Workflow Automation

### Install n8n

```bash
task add "Install n8n via Docker" project:vps_ai.tools.n8n +setup
task start 16

docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=AIstack2024! \
  -e N8N_HOST=0.0.0.0 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Wait for startup
sleep 10

# Verify
curl -u admin:AIstack2024! http://localhost:5678/healthz

task 16 annotate "n8n running on port 5678 (user: admin)"
task 16 done
```

### Workflow 1: Smart Routing Workflow

```bash
task add "Create smart routing n8n workflow" project:vps_ai.tools.n8n.workflows +automation
task start 17

mkdir -p ~/.n8n/workflows

cat > ~/.n8n/workflows/smart_routing.json << 'EOF'
{
  "name": "Smart AI Router",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "ai-request",
        "responseMode": "responseNode"
      },
      "name": "Incoming Request",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "parameters": {
        "command": "python3 /home/aistack/ai_stack/scripts/smart_router.py '{{ $json.body.prompt }}'"
      },
      "name": "Smart Router",
      "type": "n8n-nodes-base.executeCommand",
      "position": [450, 300]
    },
    {
      "parameters": {
        "command": "task add 'Routed: {{ $json.model }}' project:vps_ai.router +automated"
      },
      "name": "Log to Taskwarrior",
      "type": "n8n-nodes-base.executeCommand",
      "position": [650, 300]
    },
    {
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ $json }}"
      },
      "name": "Return Response",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [850, 300]
    }
  ],
  "connections": {
    "Incoming Request": {
      "main": [[{"node": "Smart Router", "type": "main", "index": 0}]]
    },
    "Smart Router": {
      "main": [[{"node": "Log to Taskwarrior", "type": "main", "index": 0}]]
    },
    "Log to Taskwarrior": {
      "main": [[{"node": "Return Response", "type": "main", "index": 0}]]
    }
  }
}
EOF

task 17 annotate "Smart routing workflow created"
task 17 done
```

### Workflow 2: Cost Monitoring

```bash
task add "Create cost monitoring workflow" project:vps_ai.tools.n8n.workflows +monitoring
task start 18

cat > ~/.n8n/workflows/cost_monitor.json << 'EOF'
{
  "name": "API Cost Monitor",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 24}]
        }
      },
      "name": "Daily Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300]
    },
    {
      "parameters": {
        "command": "grep 'Cost:' /home/aistack/ai_stack/logs/router.log | awk '{sum += $2} END {print sum}'"
      },
      "name": "Calculate Daily Cost",
      "type": "n8n-nodes-base.executeCommand",
      "position": [450, 300]
    },
    {
      "parameters": {
        "command": "task add 'Daily API cost: ${{ $json.output }}' project:vps_ai.monitoring +cost"
      },
      "name": "Log Cost to Taskwarrior",
      "type": "n8n-nodes-base.executeCommand",
      "position": [650, 300]
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            {
              "value1": "={{ parseFloat($json.output) }}",
              "operation": "larger",
              "value2": 5.0
            }
          ]
        }
      },
      "name": "Check Alert Threshold",
      "type": "n8n-nodes-base.if",
      "position": [850, 300]
    },
    {
      "parameters": {
        "command": "task add 'ALERT: Daily cost exceeded $5 ({{ $json.output }})' project:vps_ai.monitoring +alert priority:H"
      },
      "name": "Create Cost Alert",
      "type": "n8n-nodes-base.executeCommand",
      "position": [1050, 200]
    }
  ],
  "connections": {
    "Daily Trigger": {
      "main": [[{"node": "Calculate Daily Cost", "type": "main", "index": 0}]]
    },
    "Calculate Daily Cost": {
      "main": [[{"node": "Log Cost to Taskwarrior", "type": "main", "index": 0}]]
    },
    "Log Cost to Taskwarrior": {
      "main": [[{"node": "Check Alert Threshold", "type": "main", "index": 0}]]
    },
    "Check Alert Threshold": {
      "main": [[{"node": "Create Cost Alert", "type": "main", "index": 0}], []]
    }
  }
}
EOF

task 18 annotate "Cost monitoring workflow created (daily checks)"
task 18 done
```

---

## Google Cloud Platform (GCP) Deployment

### GCP Instance Recommendations

#### Tier 2: e2-standard-2 (Budget-Friendly)
**Specs:**
- 2 vCPUs, 8GB RAM
- ~$50/month (us-central1)
- Good for: TinyLlama, Phi-2

```bash
# Create GCP setup tasks
task add "Setup GCP Compute Engine instance" project:vps_ai.gcp.setup +cloud priority:H
task add "Configure GCP firewall rules" project:vps_ai.gcp.network depends:1
task add "Install AI stack on GCP" project:vps_ai.gcp.install depends:2
```

#### Tier 3: e2-standard-4 (Performance)
**Specs:**
- 4 vCPUs, 16GB RAM
- ~$100/month
- Good for: Mistral-7B, Llama-3.2-3B

#### Tier 4: g2-standard-4 (GPU)
**Specs:**
- 4 vCPUs, 16GB RAM, 1x NVIDIA L4 GPU (24GB)
- ~$450/month
- Good for: Any model up to 13B

### GCP Setup Instructions

```bash
# 1. Create GCP project and enable APIs
task start 1

# Install gcloud CLI (on your local machine)
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init

# Create new project
gcloud projects create ai-orchestrator-stack --name="AI Orchestrator"
gcloud config set project ai-orchestrator-stack

# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com

task 1 annotate "GCP project created: ai-orchestrator-stack"
task 1 done

# 2. Create Compute Engine instance (Tier 2 example)
task start 2

gcloud compute instances create ai-stack-tier2 \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB \
  --boot-disk-type=pd-ssd \
  --tags=ai-stack,http-server,https-server

task 2 annotate "GCP instance created: ai-stack-tier2 (e2-standard-2)"
task 2 done

# 3. Configure firewall
task start 3

# Allow n8n, API gateway
gcloud compute firewall-rules create ai-stack-allow-services \
  --allow=tcp:5678,tcp:8080,tcp:8001,tcp:8002 \
  --target-tags=ai-stack \
  --description="Allow AI stack services"

# Allow SSH
gcloud compute firewall-rules create ai-stack-allow-ssh \
  --allow=tcp:22 \
  --target-tags=ai-stack

task 3 annotate "GCP firewall rules configured"
task 3 done

# 4. SSH into instance
gcloud compute ssh ai-stack-tier2 --zone=us-central1-a

# Now follow the standard installation steps from earlier sections
```

### GCP-Specific Optimizations

```bash
# Use Google Cloud Storage for model storage
task add "Setup GCS for model storage" project:vps_ai.gcp.storage +optimization
task start 4

# Install gsutil (already included with gcloud)
# Create storage bucket
gsutil mb -l us-central1 gs://ai-stack-models

# Download models to GCS first (cheaper egress)
gsutil cp gs://public-model-repo/tinyllama.gguf ~/ai_stack/models/

# Mount GCS bucket as filesystem (optional)
gcsfuse ai-stack-models ~/ai_stack/models

task 4 annotate "GCS bucket created for model storage"
task 4 done
```

### GCP GPU Instance Setup (Tier 4)

```bash
task add "Create GCP GPU instance" project:vps_ai.gcp.gpu +gpu priority:H
task start 5

# Create GPU instance with L4 GPU
gcloud compute instances create ai-stack-gpu \
  --zone=us-central1-a \
  --machine-type=g2-standard-4 \
  --accelerator=type=nvidia-l4,count=1 \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=100GB \
  --boot-disk-type=pd-ssd \
  --maintenance-policy=TERMINATE \
  --tags=ai-stack-gpu

# SSH into GPU instance
gcloud compute ssh ai-stack-gpu --zone=us-central1-a

# Install NVIDIA drivers
curl https://raw.githubusercontent.com/GoogleCloudPlatform/compute-gpu-installation/main/linux/install_gpu_driver.py --output install_gpu_driver.py
sudo python3 install_gpu_driver.py

# Verify GPU
nvidia-smi

task 5 annotate "GCP GPU instance ready with L4 GPU"
task 5 done
```

### GCP Cost Optimization

```bash
# Use preemptible instances (up to 80% cheaper)
task add "Setup GCP preemptible instance" project:vps_ai.gcp.cost +optimization

gcloud compute instances create ai-stack-preemptible \
  --zone=us-central1-a \
  --machine-type=e2-standard-2 \
  --preemptible \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=50GB

# Note: Preemptible instances can be terminated anytime
# Good for: Development, testing, batch processing
# Bad for: Production APIs
```

---

## AWS Deployment

### AWS Instance Recommendations

#### Tier 2: t3.large (Budget-Friendly)
**Specs:**
- 2 vCPUs, 8GB RAM
- ~$60/month (us-east-1)
- Good for: TinyLlama, Phi-2

```bash
# Create AWS setup tasks
task add "Setup AWS EC2 instance" project:vps_ai.aws.setup +cloud priority:H
task add "Configure AWS security groups" project:vps_ai.aws.network depends:1
task add "Install AI stack on AWS" project:vps_ai.aws.install depends:2
```

#### Tier 3: t3.xlarge (Performance)
**Specs:**
- 4 vCPUs, 16GB RAM
- ~$120/month
- Good for: Mistral-7B, Llama-3.2-3B

#### Tier 4: g5.xlarge (GPU)
**Specs:**
- 4 vCPUs, 16GB RAM, 1x NVIDIA A10G GPU (24GB)
- ~$1.00/hour (~$730/month spot ~$250/month)
- Good for: Any model up to 13B

### AWS Setup Instructions

```bash
# 1. Install AWS CLI and configure
task start 1

# Install AWS CLI v2
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (us-east-1), Output format (json)

task 1 annotate "AWS CLI configured"
task 1 done

# 2. Create key pair for SSH
task start 2

aws ec2 create-key-pair \
  --key-name ai-stack-key \
  --query 'KeyMaterial' \
  --output text > ~/.ssh/ai-stack-key.pem

chmod 400 ~/.ssh/ai-stack-key.pem

task 2 annotate "AWS key pair created: ai-stack-key"
task 2 done

# 3. Create security group
task start 3

# Create security group
aws ec2 create-security-group \
  --group-name ai-stack-sg \
  --description "Security group for AI stack"

# Get security group ID
SG_ID=$(aws ec2 describe-security-groups \
  --group-names ai-stack-sg \
  --query 'SecurityGroups[0].GroupId' \
  --output text)

# Allow SSH
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Allow n8n
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 5678 \
  --cidr 0.0.0.0/0

# Allow API services
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp \
  --port 8001-8002 \
  --cidr 0.0.0.0/0

task 3 annotate "AWS security group configured: $SG_ID"
task 3 done

# 4. Launch EC2 instance (Tier 2 example)
task start 4

# Get latest Ubuntu 22.04 AMI ID
AMI_ID=$(aws ec2 describe-images \
  --owners 099720109477 \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text)

# Launch instance
aws ec2 run-instances \
  --image-id $AMI_ID \
  --instance-type t3.large \
  --key-name ai-stack-key \
  --security-group-ids $SG_ID \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":50,"VolumeType":"gp3"}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ai-stack-tier2}]'

# Get instance ID
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=ai-stack-tier2" "Name=instance-state-name,Values=running" \
  --query 'Reservations[0].Instances[0].InstanceId' \
  --output text)

# Get public IP
PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids $INSTANCE_ID \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "Instance IP: $PUBLIC_IP"

task 4 annotate "AWS EC2 instance launched: $INSTANCE_ID at $PUBLIC_IP"
task 4 done

# 5. SSH into instance
ssh -i ~/.ssh/ai-stack-key.pem ubuntu@$PUBLIC_IP

# Now follow the standard installation steps
```

### AWS GPU Instance Setup (Tier 4)

```bash
task add "Create AWS GPU instance" project:vps_ai.aws.gpu +gpu priority:H
task start 5

# Get Deep Learning AMI (includes NVIDIA drivers)
DL_AMI=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=Deep Learning AMI GPU PyTorch * (Ubuntu 22.04)*" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --output text)

# Launch g5.xlarge with A10G GPU
aws ec2 run-instances \
  --image-id $DL_AMI \
  --instance-type g5.xlarge \
  --key-name ai-stack-key \
  --security-group-ids $SG_ID \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":100,"VolumeType":"gp3"}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ai-stack-gpu}]'

# Get GPU instance IP
GPU_IP=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=ai-stack-gpu" "Name=instance-state-name,Values=running" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

# SSH into GPU instance
ssh -i ~/.ssh/ai-stack-key.pem ubuntu@$GPU_IP

# Verify GPU
nvidia-smi

task 5 annotate "AWS GPU instance ready with A10G GPU at $GPU_IP"
task 5 done
```

### AWS Spot Instances (80% Cost Savings)

```bash
task add "Setup AWS Spot instance" project:vps_ai.aws.cost +optimization
task start 6

# Create launch template for spot instances
aws ec2 create-launch-template \
  --launch-template-name ai-stack-spot-template \
  --version-description "AI Stack Spot Instance" \
  --launch-template-data '{
    "ImageId": "'$AMI_ID'",
    "InstanceType": "t3.large",
    "KeyName": "ai-stack-key",
    "SecurityGroupIds": ["'$SG_ID'"],
    "BlockDeviceMappings": [{
      "DeviceName": "/dev/sda1",
      "Ebs": {
        "VolumeSize": 50,
        "VolumeType": "gp3"
      }
    }]
  }'

# Request spot instance
aws ec2 request-spot-instances \
  --spot-price "0.05" \
  --instance-count 1 \
  --type "one-time" \
  --launch-specification '{
    "ImageId": "'$AMI_ID'",
    "InstanceType": "t3.large",
    "KeyName": "ai-stack-key",
    "SecurityGroupIds": ["'$SG_ID'"]
  }'

task 6 annotate "AWS Spot instance requested (up to 80% cheaper)"
task 6 done

# Note: Spot instances can be terminated with 2-minute warning
# Good for: Development, batch processing
# Bad for: Production APIs without auto-scaling
```

### AWS-Specific Optimizations

#### S3 for Model Storage

```bash
task add "Setup S3 for model storage" project:vps_ai.aws.storage +optimization
task start 7

# Create S3 bucket
aws s3 mb s3://ai-stack-models-$(date +%s) --region us-east-1

# Upload models to S3
aws s3 cp ~/ai_stack/models/ s3://ai-stack-models-$(date +%s)/models/ --recursive

# Download models on instance startup
aws s3 sync s3://ai-stack-models-$(date +%s)/models/ ~/ai_stack/models/

task 7 annotate "S3 bucket configured for model storage"
task 7 done
```

#### EFS for Shared Model Storage (Multi-Instance)

```bash
task add "Setup EFS for shared models" project:vps_ai.aws.storage +advanced
task start 8

# Create EFS filesystem
aws efs create-file-system \
  --performance-mode generalPurpose \
  --throughput-mode bursting \
  --tags Key=Name,Value=ai-stack-models

# Get filesystem ID
EFS_ID=$(aws efs describe-file-systems \
  --query 'FileSystems[?Name==`ai-stack-models`].FileSystemId' \
  --output text)

# Create mount target
aws efs create-mount-target \
  --file-system-id $EFS_ID \
  --subnet-id <your-subnet-id> \
  --security-groups $SG_ID

# Mount on EC2 instance
sudo apt install -y amazon-efs-utils
sudo mount -t efs $EFS_ID:/ ~/ai_stack/models

task 8 annotate "EFS mounted for shared model storage across instances"
task 8 done
```

### AWS Auto-Scaling Setup

```bash
task add "Configure AWS auto-scaling" project:vps_ai.aws.scaling +production
task start 9

# Create launch template
aws ec2 create-launch-template \
  --launch-template-name ai-stack-asg-template \
  --version-description "Auto-scaling template" \
  --launch-template-data file://launch-template.json

# Create auto-scaling group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name ai-stack-asg \
  --launch-template LaunchTemplateName=ai-stack-asg-template \
  --min-size 1 \
  --max-size 5 \
  --desired-capacity 2 \
  --vpc-zone-identifier "subnet-12345,subnet-67890" \
  --health-check-type ELB \
  --health-check-grace-period 300

# Create scaling policy (CPU-based)
aws autoscaling put-scaling-policy \
  --auto-scaling-group-name ai-stack-asg \
  --policy-name cpu-scale-out \
  --policy-type TargetTrackingScaling \
  --target-tracking-configuration '{
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "ASGAverageCPUUtilization"
    },
    "TargetValue": 70.0
  }'

task 9 annotate "Auto-scaling configured for production workloads"
task 9 done
```

### AWS vs GCP vs Generic VPS Comparison

```bash
# Create comparison task
task add "Document cloud provider comparison" project:vps_ai.planning +documentation

cat > ~/ai_stack/CLOUD_COMPARISON.md << 'EOF'
# Cloud Provider Comparison

## Tier 2 (8GB RAM, 2-4 CPUs)

| Provider | Instance Type | Monthly Cost | Pros | Cons |
|----------|--------------|--------------|------|------|
| **AWS** | t3.large | ~$60 | Auto-scaling, huge ecosystem | Complex pricing |
| **GCP** | e2-standard-2 | ~$50 | Simple pricing, good docs | Smaller ecosystem |
| **DigitalOcean** | 8GB Droplet | ~$48 | Simple, developer-friendly | Limited services |
| **Vultr** | 8GB Instance | ~$48 | Good performance | Basic features |
| **Hetzner** | CPX21 | ~$25 | Cheapest, great value | EU-only, basic |

## Tier 3 (16GB RAM, 4-8 CPUs)

| Provider | Instance Type | Monthly Cost | Notes |
|----------|--------------|--------------|-------|
| **AWS** | t3.xlarge | ~$120 | Burstable, good for variable load |
| **GCP** | e2-standard-4 | ~$100 | Consistent performance |
| **Hetzner** | CPX41 | ~$50 | Best value, EU only |

## Tier 4 (GPU Instances)

| Provider | Instance Type | GPU | Monthly Cost | Best For |
|----------|--------------|-----|--------------|----------|
| **AWS** | g5.xlarge | A10G (24GB) | ~$730 (~$250 spot) | Production |
| **GCP** | g2-standard-4 | L4 (24GB) | ~$450 | Development |
| **RunPod** | RTX 4090 Pod | RTX 4090 (24GB) | ~$0.69/hr (~$500/mo) | ML Training |
| **Vast.ai** | Various | Various | ~$0.20-0.50/hr | Batch jobs |

## Recommendation by Use Case

**Development/Learning:**
- Hetzner CPX21 (16GB, €25/mo) + Cloud APIs

**Small Production (<1000 req/day):**
- DigitalOcean 8GB ($48/mo) + Ollama + Cloud APIs

**Medium Production (1000-10000 req/day):**
- AWS t3.xlarge with Auto-scaling + Cloud APIs

**High Performance:**
- AWS g5.xlarge Spot Instance + vLLM

**Cost-Optimized:**
- Hetzner + 100% Cloud APIs (Groq free tier)
EOF
```

---

## Infrastructure as Code (IaC) Deployment

### Terraform Setup

```bash
# Create IaC task chain
task add "Setup Infrastructure as Code" project:vps_ai.iac +infrastructure priority:H
task add "Create Terraform configurations" project:vps_ai.iac.terraform depends:1
task add "Create Docker Compose stack" project:vps_ai.iac.docker depends:1
task add "Create Ansible playbooks" project:vps_ai.iac.ansible depends:1
task add "Setup GitHub Actions CI/CD" project:vps_ai.iac.cicd depends:2,3,4

# Install Terraform
task start 1

wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

terraform --version

task 1 annotate "Terraform $(terraform --version | head -1) installed"
task 1 done
```

### Terraform: AWS Deployment

```bash
task start 2

mkdir -p ~/ai_stack/terraform/aws
cd ~/ai_stack/terraform/aws

cat > main.tf << 'EOF'
# AWS AI Stack - Terraform Configuration
# Deploys Tier 2: t3.large with 8GB RAM

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t3.large"
}

variable "ssh_key_name" {
  description = "SSH key pair name"
  default     = "ai-stack-key"
}

# Data: Latest Ubuntu 22.04 AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

# Security Group
resource "aws_security_group" "ai_stack_sg" {
  name        = "ai-stack-sg"
  description = "Security group for AI stack"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "n8n"
    from_port   = 5678
    to_port     = 5678
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "API Gateway"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Local Models"
    from_port   = 8001
    to_port     = 8002
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ai-stack-sg"
  }
}

# EC2 Instance
resource "aws_instance" "ai_stack" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = var.ssh_key_name

  vpc_security_group_ids = [aws_security_group.ai_stack_sg.id]

  root_block_device {
    volume_size = 50
    volume_type = "gp3"
  }

  user_data = file("${path.module}/user-data.sh")

  tags = {
    Name = "ai-stack-tier2"
  }
}

# Outputs
output "instance_id" {
  value = aws_instance.ai_stack.id
}

output "public_ip" {
  value = aws_instance.ai_stack.public_ip
}

output "ssh_command" {
  value = "ssh -i ~/.ssh/${var.ssh_key_name}.pem ubuntu@${aws_instance.ai_stack.public_ip}"
}
EOF

# User data script (runs on first boot)
cat > user-data.sh << 'EOF'
#!/bin/bash
set -e

# Update system
apt update && apt upgrade -y
apt install -y curl wget git vim htop python3.11 python3.11-venv python3-pip docker.io

# Setup aistack user
useradd -m -s /bin/bash aistack
usermod -aG sudo,docker aistack

# Create directory structure
sudo -u aistack mkdir -p /home/aistack/ai_stack/{models,configs,scripts,workflows,prompts,logs}

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull models
sudo -u aistack ollama pull tinyllama
sudo -u aistack ollama pull phi

# Install Taskwarrior
apt install -y taskwarrior

# Clone AI stack repository (if exists)
# sudo -u aistack git clone https://github.com/yourusername/ai-stack.git /home/aistack/ai_stack

# Install n8n
docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=AIstack2024! \
  -v /home/aistack/.n8n:/home/node/.n8n \
  n8nio/n8n

echo "AI Stack installation complete!" > /home/aistack/setup-complete.txt
EOF

# Variables file
cat > terraform.tfvars << 'EOF'
aws_region    = "us-east-1"
instance_type = "t3.large"
ssh_key_name  = "ai-stack-key"
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
.terraform/
*.tfstate
*.tfstate.backup
.terraform.lock.hcl
terraform.tfvars
*.pem
EOF

task 2 annotate "Terraform AWS configuration created"
task 2 done
```

### Terraform: GCP Deployment

```bash
cd ~/ai_stack/terraform
mkdir -p gcp
cd gcp

cat > main.tf << 'EOF'
# GCP AI Stack - Terraform Configuration
# Deploys Tier 2: e2-standard-2 with 8GB RAM

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# Variables
variable "project_id" {
  description = "GCP Project ID"
}

variable "region" {
  description = "GCP region"
  default     = "us-central1"
}

variable "zone" {
  description = "GCP zone"
  default     = "us-central1-a"
}

variable "machine_type" {
  description = "GCP machine type"
  default     = "e2-standard-2"
}

# Firewall Rules
resource "google_compute_firewall" "ai_stack_allow_ssh" {
  name    = "ai-stack-allow-ssh"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ai-stack"]
}

resource "google_compute_firewall" "ai_stack_allow_services" {
  name    = "ai-stack-allow-services"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["5678", "8001", "8002", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ai-stack"]
}

# Compute Instance
resource "google_compute_instance" "ai_stack" {
  name         = "ai-stack-tier2"
  machine_type = var.machine_type
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 50
      type  = "pd-ssd"
    }
  }

  network_interface {
    network = "default"
    access_config {
      // Ephemeral public IP
    }
  }

  metadata_startup_script = file("${path.module}/startup-script.sh")

  tags = ["ai-stack"]

  service_account {
    scopes = ["cloud-platform"]
  }
}

# Outputs
output "instance_name" {
  value = google_compute_instance.ai_stack.name
}

output "external_ip" {
  value = google_compute_instance.ai_stack.network_interface[0].access_config[0].nat_ip
}

output "ssh_command" {
  value = "gcloud compute ssh ${google_compute_instance.ai_stack.name} --zone=${var.zone}"
}
EOF

# Startup script (same as AWS user-data)
cat > startup-script.sh << 'EOF'
#!/bin/bash
set -e

apt update && apt upgrade -y
apt install -y curl wget git vim htop python3.11 python3.11-venv python3-pip docker.io

useradd -m -s /bin/bash aistack
usermod -aG sudo,docker aistack

sudo -u aistack mkdir -p /home/aistack/ai_stack/{models,configs,scripts,workflows,prompts,logs}

curl -fsSL https://ollama.com/install.sh | sh
sudo -u aistack ollama pull tinyllama
sudo -u aistack ollama pull phi

apt install -y taskwarrior

docker run -d \
  --name n8n \
  --restart unless-stopped \
  -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=AIstack2024! \
  -v /home/aistack/.n8n:/home/node/.n8n \
  n8nio/n8n

echo "AI Stack installation complete!" > /home/aistack/setup-complete.txt
EOF

cat > terraform.tfvars << 'EOF'
project_id   = "your-gcp-project-id"
region       = "us-central1"
zone         = "us-central1-a"
machine_type = "e2-standard-2"
EOF

task add "Terraform GCP configuration created" project:vps_ai.iac.terraform +gcp
task annotate "GCP Terraform config created"
```

### Terraform: Multi-Cloud Module (Generic)

```bash
cd ~/ai_stack/terraform
mkdir -p multi-cloud
cd multi-cloud

cat > main.tf << 'EOF'
# Multi-Cloud AI Stack Deployment
# Supports: AWS, GCP, DigitalOcean, Vultr

variable "provider" {
  description = "Cloud provider: aws, gcp, digitalocean, vultr"
  type        = string
}

variable "tier" {
  description = "Tier: 2 (8GB), 3 (16GB), 4 (GPU)"
  type        = number
  default     = 2
}

module "aws_stack" {
  source = "./aws"
  count  = var.provider == "aws" ? 1 : 0

  instance_type = var.tier == 2 ? "t3.large" : var.tier == 3 ? "t3.xlarge" : "g5.xlarge"
}

module "gcp_stack" {
  source = "./gcp"
  count  = var.provider == "gcp" ? 1 : 0

  machine_type = var.tier == 2 ? "e2-standard-2" : var.tier == 3 ? "e2-standard-4" : "g2-standard-4"
}

output "deployment_info" {
  value = {
    provider = var.provider
    tier     = var.tier
    ip       = var.provider == "aws" ? module.aws_stack[0].public_ip : module.gcp_stack[0].external_ip
  }
}
EOF
```

### Deploy with Terraform

```bash
task add "Deploy AI stack with Terraform" project:vps_ai.iac.terraform +deployment
task start 3

# AWS Deployment
cd ~/ai_stack/terraform/aws

# Initialize Terraform
terraform init

# Plan deployment
terraform plan

# Apply (deploy)
terraform apply -auto-approve

# Get outputs
terraform output -json > outputs.json
PUBLIC_IP=$(terraform output -raw public_ip)

echo "AI Stack deployed at: $PUBLIC_IP"

task 3 annotate "Terraform deployed AWS instance at $PUBLIC_IP"
task 3 done

# To destroy resources
# terraform destroy -auto-approve
```

### Docker Compose Stack

```bash
task start 4

cat > ~/ai_stack/docker-compose.yml << 'EOF'
# AI Stack - Complete Docker Compose Configuration
version: '3.8'

services:
  # n8n Workflow Automation
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=AIstack2024!
      - N8N_HOST=0.0.0.0
      - WEBHOOK_URL=http://localhost:5678/
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - ai_stack_network

  # Ollama (Local LLM Server)
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - ai_stack_network

  # API Gateway (Request Router)
  api_gateway:
    build:
      context: ./gateway
      dockerfile: Dockerfile
    container_name: api_gateway
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
    networks:
      - ai_stack_network

  # Prometheus (Monitoring)
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./configs/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    networks:
      - ai_stack_network

  # Grafana (Dashboards)
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - ai_stack_network

  # Redis (Caching)
  redis:
    image: redis:alpine
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - ai_stack_network

volumes:
  n8n_data:
  ollama_data:
  prometheus_data:
  grafana_data:
  redis_data:

networks:
  ai_stack_network:
    driver: bridge
EOF

# Create API Gateway Dockerfile
mkdir -p ~/ai_stack/gateway

cat > ~/ai_stack/gateway/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY smart_router.py .

CMD ["python", "-u", "smart_router.py"]
EOF

cat > ~/ai_stack/gateway/requirements.txt << 'EOF'
anthropic
openai
requests
flask
redis
python-dotenv
prometheus-client
EOF

# Copy smart router to gateway
cp ~/ai_stack/scripts/smart_router.py ~/ai_stack/gateway/

# Prometheus config
mkdir -p ~/ai_stack/configs

cat > ~/ai_stack/configs/prometheus.yml << 'EOF'
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'api_gateway'
    static_configs:
      - targets: ['api_gateway:8080']
  
  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama:11434']
EOF

task 4 annotate "Docker Compose stack created with n8n, Ollama, Prometheus, Grafana"
task 4 done
```

### Launch Docker Stack

```bash
task add "Launch Docker Compose stack" project:vps_ai.iac.docker +deployment
task start 5

cd ~/ai_stack

# Create .env file
cat > .env << 'EOF'
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
EOF

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Pull Ollama models
docker exec ollama ollama pull tinyllama
docker exec ollama ollama pull phi

task 5 annotate "Docker stack running: n8n (5678), Ollama (11434), Prometheus (9090), Grafana (3000)"
task 5 done

# Access services:
# - n8n: http://localhost:5678 (admin/AIstack2024!)
# - Grafana: http://localhost:3000 (admin/admin)
# - Prometheus: http://localhost:9090
```

### Ansible Playbooks

```bash
task start 6

mkdir -p ~/ai_stack/ansible
cd ~/ai_stack/ansible

# Install Ansible
sudo apt install -y ansible

# Inventory file
cat > inventory.ini << 'EOF'
[ai_stack_servers]
ai-stack-1 ansible_host=<your-server-ip> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/ai-stack-key.pem

[ai_stack_servers:vars]
ansible_python_interpreter=/usr/bin/python3
EOF

# Main playbook
cat > deploy.yml << 'EOF'
---
- name: Deploy AI Stack
  hosts: ai_stack_servers
  become: yes
  
  vars:
    ai_stack_user: aistack
    ai_stack_dir: /home/{{ ai_stack_user }}/ai_stack
    ollama_models:
      - tinyllama
      - phi
    
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
    
    - name: Install required packages
      apt:
        name:
          - curl
          - wget
          - git
          - vim
          - htop
          - python3.11
          - python3.11-venv
          - python3-pip
          - docker.io
          - docker-compose
          - taskwarrior
        state: present
    
    - name: Create aistack user
      user:
        name: "{{ ai_stack_user }}"
        groups: sudo,docker
        shell: /bin/bash
        create_home: yes
    
    - name: Create directory structure
      file:
        path: "{{ ai_stack_dir }}/{{ item }}"
        state: directory
        owner: "{{ ai_stack_user }}"
        group: "{{ ai_stack_user }}"
      loop:
        - models
        - configs
        - scripts
        - workflows
        - prompts
        - logs
    
    - name: Install Ollama
      shell: curl -fsSL https://ollama.com/install.sh | sh
      args:
        creates: /usr/local/bin/ollama
    
    - name: Start Ollama service
      systemd:
        name: ollama
        state: started
        enabled: yes
    
    - name: Pull Ollama models
      become_user: "{{ ai_stack_user }}"
      command: ollama pull {{ item }}
      loop: "{{ ollama_models }}"
      register: ollama_pull
      changed_when: "'already up to date' not in ollama_pull.stdout"
    
    - name: Copy Docker Compose file
      copy:
        src: ../docker-compose.yml
        dest: "{{ ai_stack_dir }}/docker-compose.yml"
        owner: "{{ ai_stack_user }}"
        group: "{{ ai_stack_user }}"
    
    - name: Copy .env file
      copy:
        src: ../.env
        dest: "{{ ai_stack_dir }}/.env"
        owner: "{{ ai_stack_user }}"
        group: "{{ ai_stack_user }}"
        mode: '0600'
    
    - name: Start Docker Compose stack
      become_user: "{{ ai_stack_user }}"
      community.docker.docker_compose:
        project_src: "{{ ai_stack_dir }}"
        state: present
    
    - name: Configure firewall (UFW)
      ufw:
        rule: allow
        port: "{{ item }}"
        proto: tcp
      loop:
        - 22
        - 5678
        - 8080
        - 11434
    
    - name: Enable firewall
      ufw:
        state: enabled
    
    - name: Create Taskwarrior task
      become_user: "{{ ai_stack_user }}"
      command: task add "AI Stack deployed via Ansible" project:vps_ai.iac.ansible +automated
EOF

# Run playbook
cat > deploy.sh << 'EOF'
#!/bin/bash

# Deploy AI Stack using Ansible

echo "Deploying AI Stack..."

ansible-playbook -i inventory.ini deploy.yml

echo "Deployment complete!"
echo ""
echo "Access services:"
echo "- n8n: http://$(grep ansible_host inventory.ini | awk '{print $2}' | cut -d= -f2):5678"
echo "- Grafana: http://$(grep ansible_host inventory.ini | awk '{print $2}' | cut -d= -f2):3000"
EOF

chmod +x deploy.sh

task 6 annotate "Ansible playbooks created for automated deployment"
task 6 done
```

### GitHub Actions CI/CD

```bash
task start 7

mkdir -p ~/ai_stack/.github/workflows

cat > ~/ai_stack/.github/workflows/deploy.yml << 'EOF'
name: Deploy AI Stack

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

env:
  AWS_REGION: us-east-1
  TERRAFORM_VERSION: 1.6.0

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r gateway/requirements.txt
        pip install pytest
    
    - name: Run tests
      run: |
        pytest tests/
    
    - name: Create Taskwarrior task
      run: |
        sudo apt install -y taskwarrior
        task add "CI: Tests passed for commit ${{ github.sha }}" project:vps_ai.iac.cicd +automated

  terraform-plan:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TERRAFORM_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Terraform Init
      run: |
        cd terraform/aws
        terraform init
    
    - name: Terraform Plan
      run: |
        cd terraform/aws
        terraform plan -out=tfplan
    
    - name: Upload plan
      uses: actions/upload-artifact@v3
      with:
        name: terraform-plan
        path: terraform/aws/tfplan

  deploy:
    runs-on: ubuntu-latest
    needs: terraform-plan
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TERRAFORM_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Download plan
      uses: actions/download-artifact@v3
      with:
        name: terraform-plan
        path: terraform/aws/
    
    - name: Terraform Init
      run: |
        cd terraform/aws
        terraform init
    
    - name: Terraform Apply
      run: |
        cd terraform/aws
        terraform apply -auto-approve tfplan
    
    - name: Get outputs
      id: terraform
      run: |
        cd terraform/aws
        echo "public_ip=$(terraform output -raw public_ip)" >> $GITHUB_OUTPUT
    
    - name: Wait for instance ready
      run: |
        sleep 60
        ssh -o StrictHostKeyChecking=no ubuntu@${{ steps.terraform.outputs.public_ip }} 'cat /home/aistack/setup-complete.txt'
    
    - name: Deploy with Ansible
      run: |
        cd ansible
        echo "${{ steps.terraform.outputs.public_ip }}" > inventory_dynamic.ini
        ansible-playbook -i inventory_dynamic.ini deploy.yml
    
    - name: Health check
      run: |
        curl -f http://${{ steps.terraform.outputs.public_ip }}:5678/healthz
    
    - name: Create deployment task
      run: |
        task add "Deployed to production: ${{ steps.terraform.outputs.public_ip }}" project:vps_ai.production +deployment

  docker-build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push API Gateway
      uses: docker/build-push-action@v4
      with:
        context: ./gateway
        push: true
        tags: yourusername/ai-stack-gateway:latest
EOF

# Create test file
mkdir -p ~/ai_stack/tests

cat > ~/ai_stack/tests/test_router.py << 'EOF'
import pytest
import sys
sys.path.insert(0, '/home/aistack/ai_stack/scripts')

def test_complexity_estimation():
    from smart_router import SmartRouter
    router = SmartRouter()
    
    # Simple prompt should have low complexity
    simple = router.estimate_complexity("What is the capital of France?")
    assert simple < 0.4
    
    # Complex prompt should have high complexity
    complex_prompt = router.estimate_complexity("Analyze and write production code with error handling")
    assert complex_prompt > 0.6

def test_routing_logic():
    from smart_router import SmartRouter
    router = SmartRouter()
    
    # Test that router doesn't crash
    result = router.estimate_complexity("Test prompt")
    assert 0 <= result <= 1
EOF

task 7 annotate "GitHub Actions CI/CD pipeline created"
task 7 done
```

### Complete Deployment Script

```bash
task add "Create one-command deployment script" project:vps_ai.iac +automation
task start 8

cat > ~/ai_stack/deploy-all.sh << 'EOF'
#!/bin/bash
# One-command deployment script
# Usage: ./deploy-all.sh [aws|gcp|docker] [tier]

set -e

PROVIDER=${1:-docker}
TIER=${2:-2}

echo "🚀 Deploying AI Stack"
echo "Provider: $PROVIDER"
echo "Tier: $TIER"
echo ""

# Create Taskwarrior task
task add "Deploying AI Stack: $PROVIDER tier $TIER" project:vps_ai.deployment +active

case $PROVIDER in
  aws)
    echo "📦 Deploying to AWS with Terraform..."
    cd terraform/aws
    terraform init
    terraform apply -auto-approve -var="instance_type=t3.$([ $TIER -eq 2 ] && echo 'large' || echo 'xlarge')"
    
    PUBLIC_IP=$(terraform output -raw public_ip)
    echo "✅ AWS instance deployed at: $PUBLIC_IP"
    
    # Wait for instance to be ready
    sleep 60
    
    # Deploy with Ansible
    echo "🔧 Configuring with Ansible..."
    cd ../../ansible
    sed -i "s/ansible_host=.*/ansible_host=$PUBLIC_IP/" inventory.ini
    ansible-playbook -i inventory.ini deploy.yml
    ;;
    
  gcp)
    echo "📦 Deploying to GCP with Terraform..."
    cd terraform/gcp
    terraform init
    terraform apply -auto-approve -var="machine_type=e2-standard-$([ $TIER -eq 2 ] && echo '2' || echo '4')"
    
    INSTANCE_NAME=$(terraform output -raw instance_name)
    echo "✅ GCP instance deployed: $INSTANCE_NAME"
    
    sleep 60
    
    # Get IP
    EXTERNAL_IP=$(terraform output -raw external_ip)
    
    echo "🔧 Configuring with Ansible..."
    cd ../../ansible
    sed -i "s/ansible_host=.*/ansible_host=$EXTERNAL_IP/" inventory.ini
    ansible-playbook -i inventory.ini deploy.yml
    ;;
    
  docker)
    echo "🐳 Deploying with Docker Compose..."
    
    # Check if .env exists
    if [ ! -f .env ]; then
      echo "Creating .env file..."
      cat > .env << 'ENVFILE'
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
ENVFILE
      echo "⚠️  Please edit .env with your API keys!"
    fi
    
    docker-compose up -d
    
    # Wait for services
    sleep 10
    
    # Pull models
    docker exec ollama ollama pull tinyllama
    docker exec ollama ollama pull phi
    
    echo "✅ Docker stack deployed!"
    ;;
    
  *)
    echo "❌ Unknown provider: $PROVIDER"
    echo "Usage: ./deploy-all.sh [aws|gcp|docker] [tier]"
    exit 1
    ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Access your services:"
case $PROVIDER in
  aws|gcp)
    echo "- n8n: http://$PUBLIC_IP:5678 (admin/AIstack2024!)"
    echo "- Grafana: http://$PUBLIC_IP:3000 (admin/admin)"
    ;;
  docker)
    echo "- n8n: http://localhost:5678 (admin/AIstack2024!)"
    echo "- Grafana: http://localhost:3000 (admin/admin)"
    ;;
esac

# Complete task
task add "Deployment completed: $PROVIDER tier $TIER" project:vps_ai.deployment +completed
EOF

chmod +x ~/ai_stack/deploy-all.sh

task 8 annotate "One-command deployment script created"
task 8 done
```

### Usage Examples

```bash
# Deploy to AWS (Tier 2)
./deploy-all.sh aws 2

# Deploy to GCP (Tier 3)
./deploy-all.sh gcp 3

# Deploy locally with Docker
./deploy-all.sh docker

# View deployment tasks
task project:vps_ai.deployment list
```

---

## Creating Your GitHub Repository

### Repository Structure

```bash
task add "Create Git repository structure" project:vps_ai.repo +setup priority:H
task start 100

cd ~/ai_stack

# Initialize Git repository
git init

# Create proper directory structure
cat > REPOSITORY_STRUCTURE.md << 'EOF'
# AI Stack Repository Structure

```
ai-stack/
├── .github/
│   └── workflows/
│       ├── deploy.yml          # CI/CD pipeline
│       ├── test.yml            # Automated testing
│       └── docker-publish.yml  # Container publishing
│
├── terraform/
│   ├── aws/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── user-data.sh
│   │   └── terraform.tfvars.example
│   ├── gcp/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── startup-script.sh
│   │   └── terraform.tfvars.example
│   └── multi-cloud/
│       └── main.tf
│
├── ansible/
│   ├── inventory.ini.example
│   ├── deploy.yml
│   └── deploy.sh
│
├── docker/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   └── .env.example
│
├── gateway/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── smart_router.py
│
├── scripts/
│   ├── smart_router.py
│   ├── moderation_pipeline.py
│   ├── prompt_tester.py
│   ├── orchestrator.py
│   └── tw-helper.sh
│
├── prompts/
│   ├── prompt_templates.py
│   ├── reasoning_prompts.txt
│   ├── programming_prompts.txt
│   └── creative_prompts.txt
│
├── configs/
│   ├── prometheus.yml
│   ├── grafana/
│   └── n8n/
│
├── workflows/
│   ├── smart_routing.json
│   ├── cost_monitor.json
│   └── orchestrator_pipeline.json
│
├── tests/
│   ├── test_router.py
│   ├── test_orchestrator.py
│   └── conftest.py
│
├── docs/
│   ├── DEPLOYMENT.md
│   ├── CONFIGURATION.md
│   ├── TROUBLESHOOTING.md
│   └── ARCHITECTURE.md
│
├── .gitignore
├── .env.example
├── README.md
├── LICENSE
├── deploy-all.sh
├── requirements.txt
└── CONTRIBUTING.md
```
EOF

task 100 annotate "Repository structure documented"
task 100 done
```

### Create .gitignore

```bash
task add "Create .gitignore file" project:vps_ai.repo +setup
task start 101

cat > .gitignore << 'EOF'
# Environment and secrets
.env
*.env
!.env.example
*.pem
*.key
*_rsa
*.tfvars
!*.tfvars.example

# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
.terraform.lock.hcl

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ai_env/
ENV/
env/
.venv

# Model files (too large for Git)
models/*.bin
models/*.safetensors
models/*.gguf
models/*.pt
models/*.pth
!models/.gitkeep

# Logs
*.log
logs/*.log
!logs/.gitkeep

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
*.pid
*.seed
*.pid.lock

# Taskwarrior
.task/
*.data

# n8n
.n8n/

# Ansible
*.retry
EOF

task 101 annotate ".gitignore created with security best practices"
task 101 done
```

### Create README.md

```bash
task add "Create comprehensive README" project:vps_ai.repo +documentation
task start 102

cat > README.md << 'EOF'
# 🤖 AI Stack - Hybrid Cloud/Local Orchestrator

> Production-ready AI orchestration system that intelligently routes requests between local models and cloud APIs to optimize cost and performance.

[![Deploy to AWS](https://img.shields.io/badge/Deploy-AWS-orange.svg)](./docs/DEPLOYMENT.md#aws)
[![Deploy to GCP](https://img.shields.io/badge/Deploy-GCP-blue.svg)](./docs/DEPLOYMENT.md#gcp)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](./docs/DEPLOYMENT.md#docker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

## 🌟 Features

- **Smart Request Routing** - Automatically routes requests to local or cloud models based on complexity
- **Cost Optimization** - 60-80% API cost reduction by using local models for simple tasks
- **Multi-Cloud Support** - Deploy to AWS, GCP, or locally with Docker
- **Infrastructure as Code** - Terraform + Ansible automation
- **Workflow Automation** - n8n integration for complex pipelines
- **Full Observability** - Prometheus + Grafana monitoring
- **Production Ready** - CI/CD with GitHub Actions

## 📊 Architecture

```
┌─────────────────────────────────┐
│   User Request                  │
└──────────────┬──────────────────┘
               ▼
┌─────────────────────────────────┐
│   Smart Router (Complexity AI)  │
│   - Estimates task complexity   │
│   - Routes to best model        │
└──────────────┬──────────────────┘
               ▼
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────────┐
│ Local Model │  │  Cloud APIs     │
│ (Ollama)    │  │  (Claude/GPT)   │
│ - TinyLlama │  │  - High quality │
│ - Phi-2     │  │  - Complex only │
└─────────────┘  └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **For Cloud Deployment:**
  - AWS/GCP account
  - Terraform 1.6+
  - Ansible 2.9+

- **For Local Deployment:**
  - Docker & Docker Compose
  - 4GB+ RAM

### One-Command Deployment

```bash
# Clone repository
git clone https://github.com/jeremylongshore/Hybrid-ai-stack-intent-solutions.git
cd Hybrid-ai-stack-intent-solutions

# Option 1: Deploy to AWS (Tier 2: 8GB RAM)
./deploy-all.sh aws 2

# Option 2: Deploy to GCP (Tier 3: 16GB RAM)
./deploy-all.sh gcp 3

# Option 3: Deploy locally with Docker
./deploy-all.sh docker
```

### Manual Setup

1. **Copy environment template:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Choose deployment method:**

**Docker (Local):**
```bash
docker-compose up -d
docker exec ollama ollama pull tinyllama
```

**Terraform (Cloud):**
```bash
cd terraform/aws  # or terraform/gcp
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars
terraform init
terraform apply
```

3. **Access services:**
- n8n: http://localhost:5678 (admin/AIstack2024!)
- Grafana: http://localhost:3000 (admin/admin)
- API: http://localhost:8080

## 💰 Cost Tiers

| Tier | RAM | Models | Monthly Cost | Use Case |
|------|-----|--------|--------------|----------|
| **1** | 2GB | Cloud only | $26-62 | Learning |
| **2** | 8GB | TinyLlama + Cloud | $30-70 | Small prod |
| **3** | 16GB | Mistral-7B + Cloud | $65-115 | Medium prod |
| **4** | GPU | Any model | $150-310 | High performance |

## 📚 Documentation

- [Deployment Guide](./docs/DEPLOYMENT.md) - Step-by-step deployment
- [Configuration](./docs/CONFIGURATION.md) - Customize your setup
- [Architecture](./docs/ARCHITECTURE.md) - System design
- [Troubleshooting](./docs/TROUBLESHOOTING.md) - Common issues

## 🔧 Configuration

### Environment Variables

```bash
# Cloud APIs
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...

# Routing Configuration
USE_LOCAL_FOR_SIMPLE=true
COMPLEXITY_THRESHOLD=0.5
```

### Supported Models

**Local (CPU):**
- TinyLlama 1.1B - Fast, basic tasks
- Phi-2 2.7B - Good quality, moderate speed
- Mistral 7B Q4 - Excellent quality (16GB+ RAM)

**Cloud:**
- Claude Sonnet 4.5 - Best quality
- GPT-4o-mini - Good balance
- Groq Llama - Free tier available

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test smart router
python scripts/test_router.py

# Load test
locust -f tests/load_test.py
```

## 📊 Monitoring

Access Grafana dashboards:
- Request routing metrics
- Cost tracking
- Model performance
- Error rates

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - Local model runtime
- [n8n](https://n8n.io) - Workflow automation
- [Anthropic](https://anthropic.com) - Claude API
- [vLLM](https://vllm.ai) - GPU inference

## 🔗 Links

- [Documentation](./docs/)
- [Issue Tracker](https://github.com/yourusername/ai-stack/issues)
- [Discussions](https://github.com/yourusername/ai-stack/discussions)

---

**Made with ❤️ by the AI Stack community**
EOF

task 102 annotate "Professional README.md created"
task 102 done
```

### Create .env.example

```bash
task add "Create environment template" project:vps_ai.repo +security
task start 103

cat > .env.example << 'EOF'
# AI Stack Environment Configuration
# Copy this file to .env and fill in your actual values

# ================================
# Cloud API Keys (Required)
# ================================

# Anthropic Claude API
# Get your key: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OpenAI API (Optional)
# Get your key: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-key-here

# Groq API (Optional, has free tier)
# Get your key: https://console.groq.com/
GROQ_API_KEY=gsk_your-key-here

# ================================
# Local Model Configuration
# ================================

# Ollama endpoint (default: http://localhost:11434)
OLLAMA_URL=http://localhost:11434

# TinyLlama endpoint (if using llama.cpp)
TINYLLAMA_URL=http://localhost:8001

# Phi-2 endpoint (if using llama.cpp)
PHI2_URL=http://localhost:8002

# ================================
# Smart Router Configuration
# ================================

# Use local models for simple tasks (true/false)
USE_LOCAL_FOR_SIMPLE=true

# Complexity threshold (0.0-1.0)
# Requests below this go to local models
COMPLEXITY_THRESHOLD=0.5

# Cost optimization mode (aggressive/balanced/quality)
COST_MODE=balanced

# ================================
# n8n Configuration
# ================================

N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=change-me-in-production

# Webhook URL (update with your domain)
N8N_WEBHOOK_URL=http://localhost:5678/

# ================================
# Monitoring & Logging
# ================================

# Log level (DEBUG/INFO/WARNING/ERROR)
LOG_LEVEL=INFO

# Enable Prometheus metrics
ENABLE_METRICS=true

# Grafana admin password
GF_SECURITY_ADMIN_PASSWORD=admin

# ================================
# Production Settings
# ================================

# Domain name (for production)
DOMAIN=ai-stack.yourdomain.com

# SSL/TLS (true/false)
ENABLE_SSL=false

# CORS allowed origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:5678
EOF

task 103 annotate "Environment template created (.env.example)"
task 103 done
```

### Create LICENSE

```bash
task add "Add MIT license" project:vps_ai.repo +legal
task start 104

cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2024 AI Stack Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

task 104 annotate "MIT License added"
task 104 done
```

### Initialize Git and Create Repository

```bash
task add "Initialize Git repository" project:vps_ai.repo +git priority:H
task start 105

# Initialize Git
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: AI Stack with hybrid cloud/local orchestration

- Terraform configs for AWS and GCP
- Docker Compose stack with n8n, Ollama, Prometheus, Grafana
- Smart request router with complexity estimation
- Ansible playbooks for automated deployment
- GitHub Actions CI/CD pipeline
- Complete documentation and examples"

# Create .gitkeep files for empty directories
touch models/.gitkeep
touch logs/.gitkeep

git add models/.gitkeep logs/.gitkeep
git commit -m "Add .gitkeep for empty directories"

task 105 annotate "Git repository initialized with initial commit"
task 105 done
```

### Create GitHub Repository

```bash
task add "Create GitHub repository" project:vps_ai.repo +github
task start 106

cat > CREATE_GITHUB_REPO.md << 'EOF'
# Creating Your GitHub Repository

## Option 1: Using GitHub CLI (Recommended)

```bash
# Install GitHub CLI
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Login to GitHub
gh auth login

# Create repository (public)
gh repo create ai-stack --public --source=. --remote=origin --push

# Or create private repository
gh repo create ai-stack --private --source=. --remote=origin --push
```

## Option 2: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `ai-stack`
3. Description: "Hybrid cloud/local AI orchestration system with smart request routing"
4. Choose Public or Private
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

7. Connect your local repo:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-stack.git
git branch -M main
git push -u origin main
```

## Option 3: Use This as a Template

If you want others to easily clone and customize:

1. Push your repo to GitHub (using Option 1 or 2)
2. Go to your repository settings
3. Check "Template repository"
4. Others can now click "Use this template" to create their own version

## Post-Creation Steps

### Add Repository Secrets (for GitHub Actions)

```bash
# Using GitHub CLI
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set ANTHROPIC_API_KEY
gh secret set DOCKER_USERNAME
gh secret set DOCKER_PASSWORD

# Or via web: Settings → Secrets and variables → Actions → New repository secret
```

### Add Topics/Tags

```bash
gh repo edit --add-topic ai
gh repo edit --add-topic orchestration
gh repo edit --add-topic terraform
gh repo edit --add-topic docker
gh repo edit --add-topic claude
gh repo edit --add-topic ollama
gh repo edit --add-topic n8n
```

### Enable GitHub Pages (Optional)

For hosting documentation:
```bash
gh repo edit --enable-pages --pages-branch gh-pages
```

### Add Branch Protection

```bash
# Protect main branch
gh api repos/:owner/:repo/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["test"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"dismiss_stale_reviews":true}'
```
EOF

task 106 annotate "GitHub repository creation guide documented"
task 106 done
```

### Quick Setup Script

```bash
task add "Create quick setup script for contributors" project:vps_ai.repo +automation
task start 107

cat > setup.sh << 'EOF'
#!/bin/bash
# Quick setup script for contributors

set -e

echo "🚀 AI Stack - Quick Setup"
echo "=========================="
echo ""

# Check prerequisites
command -v git >/dev/null 2>&1 || { echo "❌ git is required but not installed."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ docker is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 is required but not installed."; exit 1; }

echo "✅ Prerequisites check passed"
echo ""

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys before deploying"
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p models logs
touch models/.gitkeep logs/.gitkeep

# Install Taskwarrior if not present
if ! command -v task >/dev/null 2>&1; then
    echo "📋 Installing Taskwarrior..."
    sudo apt install -y taskwarrior
fi

# Initialize Taskwarrior project
echo "✨ Initializing Taskwarrior..."
task rc.confirmation=off add "AI Stack setup completed" project:vps_ai.setup +automated 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Choose deployment method:"
echo "   - Local: ./deploy-all.sh docker"
echo "   - AWS: ./deploy-all.sh aws 2"
echo "   - GCP: ./deploy-all.sh gcp 2"
echo ""
echo "3. Access services:"
echo "   - n8n: http://localhost:5678"
echo "   - Grafana: http://localhost:3000"
echo ""
echo "📚 Read the docs: ./docs/DEPLOYMENT.md"
EOF

chmod +x setup.sh

task 107 annotate "Quick setup script created for contributors"
task 107 done
```

### Push to GitHub

```bash
task add "Push repository to GitHub" project:vps_ai.repo +final priority:H
task start 108

# Install GitHub CLI if needed
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y

# Login to GitHub
gh auth login

# Create repository (choose public or private)
echo "Creating GitHub repository..."
gh repo create ai-stack \
  --public \
  --source=. \
  --remote=origin \
  --description="Hybrid cloud/local AI orchestration system with smart request routing" \
  --push

# Add topics
gh repo edit --add-topic ai,orchestration,terraform,docker,ansible,claude,ollama,n8n,automation

# Set repository secrets (optional, for CI/CD)
echo ""
echo "⚙️  Setting up GitHub Actions secrets..."
echo "You'll need to add these manually or use:"
echo "  gh secret set AWS_ACCESS_KEY_ID"
echo "  gh secret set AWS_SECRET_ACCESS_KEY"
echo "  gh secret set ANTHROPIC_API_KEY"

task 108 annotate "Repository pushed to GitHub successfully"
task 108 done

echo ""
echo "✅ Repository created successfully!"
echo ""
echo "🔗 Your repository: https://github.com/$(gh api user --jq .login)/ai-stack"
echo ""
echo "📝 Next steps:"
echo "1. Add repository secrets for GitHub Actions"
echo "2. Update README.md with your username/repo URL"
echo "3. Share with the community!"
```

### Final Repository Checklist

```bash
task add "Create repository checklist" project:vps_ai.repo +documentation

cat > REPOSITORY_CHECKLIST.md << 'EOF'
# Repository Checklist

## Before Making Public

- [ ] Remove all sensitive data (API keys, passwords, IPs)
- [ ] Update .env.example with placeholder values
- [ ] Add .gitignore for secrets and large files
- [ ] Test deployment from scratch
- [ ] Add comprehensive README.md
- [ ] Include LICENSE file
- [ ] Create CONTRIBUTING.md
- [ ] Set up GitHub Actions secrets
- [ ] Add repository topics/tags
- [ ] Create initial release/tag

## Documentation

- [ ] README with quick start guide
- [ ] Deployment documentation
- [ ] Configuration guide
- [ ] Troubleshooting guide
- [ ] Architecture diagrams
- [ ] API documentation
- [ ] Contributing guidelines

## Code Quality

- [ ] All scripts are executable (chmod +x)
- [ ] Python code follows PEP 8
- [ ] Bash scripts have error handling (set -e)
- [ ] All Terraform configs are validated
- [ ] Docker images build successfully
- [ ] Tests pass (pytest)

## Security

- [ ] No hardcoded credentials
- [ ] .env.example has placeholders only
- [ ] SSH keys are in .gitignore
- [ ] Terraform .tfvars are ignored
- [ ] Secrets use environment variables
- [ ] GitHub Actions use secrets

## Functionality

- [ ] Local deployment works (Docker)
- [ ] AWS deployment works (Terraform)
- [ ] GCP deployment works (Terraform)
- [ ] All services start correctly
- [ ] Smart router functions properly
- [ ] n8n workflows import successfully
- [ ] Monitoring dashboards display data

## Community

- [ ] Issue templates created
- [ ] Pull request template added
- [ ] Code of conduct included
- [ ] Discussion forum enabled
- [ ] Star/watch repository enabled
EOF

echo "✅ Repository checklist created"
```

---

---

## Hybrid Architecture Examples

### Example 1: Content Moderation Pipeline

```bash
# Use case: Moderate user content efficiently
# - TinyLlama does quick classification (safe/unsafe)
# - Claude only reviews flagged content

cat > ~/ai_stack/scripts/moderation_pipeline.py << 'EOF'
#!/usr/bin/