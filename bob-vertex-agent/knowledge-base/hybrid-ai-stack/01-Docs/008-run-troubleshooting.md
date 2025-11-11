# 🔧 Troubleshooting Guide

> **Navigation**: [← Back to Monitoring](./MONITORING.md) | [Next: Examples →](./EXAMPLES.md)

<details>
<summary><b>📋 TL;DR</b> - Click to expand</summary>

**Common fixes:**
- Services not starting → `docker-compose logs -f`
- Ollama not responding → `docker-compose restart ollama-cpu`
- API Gateway 500 error → Check `.env` for `ANTHROPIC_API_KEY`
- Models not pulling → Check internet connection, disk space
- Reset everything → `docker-compose down -v && ./deploy-all.sh docker`

</details>

---

## Table of Contents
- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Docker & Container Issues](#docker--container-issues)
- [Ollama & Model Issues](#ollama--model-issues)
- [API Gateway Issues](#api-gateway-issues)
- [Cloud Deployment Issues](#cloud-deployment-issues)
- [Performance Problems](#performance-problems)
- [Data & Cost Tracking Issues](#data--cost-tracking-issues)

---

## Quick Diagnostics

### Health Check Script

```bash
#!/bin/bash
# File: scripts/health_check.sh

echo "=== Hybrid AI Stack Health Check ==="

# 1. Docker Status
echo -e "\n[1/7] Docker Status:"
if docker info > /dev/null 2>&1; then
    echo "  ✅ Docker is running"
else
    echo "  ❌ Docker is not running"
    exit 1
fi

# 2. Container Status
echo -e "\n[2/7] Container Status:"
docker-compose ps

# 3. API Gateway Health
echo -e "\n[3/7] API Gateway Health:"
if curl -s http://localhost:8080/health > /dev/null; then
    curl -s http://localhost:8080/health | jq '.'
    echo "  ✅ API Gateway is healthy"
else
    echo "  ❌ API Gateway is not responding"
fi

# 4. Ollama Health
echo -e "\n[4/7] Ollama Status:"
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "  ✅ Ollama is running"
    echo "  Models loaded:"
    curl -s http://localhost:11434/api/tags | jq -r '.models[].name'
else
    echo "  ❌ Ollama is not responding"
fi

# 5. Prometheus Status
echo -e "\n[5/7] Prometheus Status:"
if curl -s http://localhost:9090/-/healthy > /dev/null; then
    echo "  ✅ Prometheus is healthy"
else
    echo "  ❌ Prometheus is not responding"
fi

# 6. Grafana Status
echo -e "\n[6/7] Grafana Status:"
if curl -s http://localhost:3000/api/health > /dev/null; then
    echo "  ✅ Grafana is healthy"
else
    echo "  ❌ Grafana is not responding"
fi

# 7. Environment Variables
echo -e "\n[7/7] Environment Configuration:"
if [ -f .env ]; then
    echo "  ✅ .env file exists"
    if grep -q "ANTHROPIC_API_KEY=sk-ant-" .env; then
        echo "  ✅ ANTHROPIC_API_KEY is set"
    else
        echo "  ⚠️  ANTHROPIC_API_KEY may not be configured"
    fi
else
    echo "  ❌ .env file not found"
fi

echo -e "\n=== Health Check Complete ==="
```

**Run it:**
```bash
chmod +x scripts/health_check.sh
./scripts/health_check.sh
```

---

## Installation Issues

### Issue: `install.sh` fails with "sudo: command not found"

**Cause**: System doesn't have `sudo` installed (rare, usually root-only systems)

**Solution:**
```bash
# If you're root
apt-get update && apt-get install -y sudo

# Add your user to sudo group
usermod -aG sudo $(whoami)

# Re-run installation
./install.sh
```

---

### Issue: "This script should NOT be run as root"

**Cause**: Running `install.sh` as root user

**Solution:**
```bash
# Don't use sudo
./install.sh

# NOT: sudo ./install.sh
```

---

### Issue: Docker installation fails

**Cause**: Conflicting Docker installations or permission issues

**Solution:**
```bash
# Remove existing Docker installations
sudo apt-get remove docker docker-engine docker.io containerd runc

# Clean up
sudo apt-get purge -y docker-ce docker-ce-cli containerd.io

# Remove data
sudo rm -rf /var/lib/docker
sudo rm -rf /var/lib/containerd

# Reinstall
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
exit
# ... log back in ...

# Verify
docker run hello-world
```

---

### Issue: Python dependencies fail to install

**Cause**: Missing Python development headers or pip

**Solution:**
```bash
# Install Python development packages
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip python3-venv

# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Docker & Container Issues

### Issue: "Cannot connect to the Docker daemon"

**Cause**: Docker daemon not running

**Solution:**
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify
docker ps
```

---

### Issue: Containers keep restarting

**Symptoms:**
```bash
docker-compose ps
# Shows containers with "Restarting" status
```

**Diagnosis:**
```bash
# View logs for the problematic container
docker-compose logs -f [container-name]

# Common container names:
# - api-gateway
# - ollama-cpu
# - n8n
# - prometheus
# - grafana
```

**Common Causes & Solutions:**

#### 1. Port Already in Use
```bash
# Check what's using port 8080
sudo lsof -i :8080

# Kill the process
sudo kill -9 [PID]

# Or change port in docker-compose.yml
```

#### 2. Insufficient Resources
```bash
# Check available RAM
free -h

# Check disk space
df -h

# Solution: Stop other services or upgrade VPS tier
```

#### 3. Configuration Error
```bash
# Check logs for specific error
docker-compose logs api-gateway | grep -i error

# Common: Missing environment variables
# Solution: Check .env file
```

---

### Issue: "docker-compose: command not found"

**Cause**: Docker Compose not installed or wrong version

**Solution:**
```bash
# Install Docker Compose V2
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Verify
docker compose version

# If using old docker-compose (V1)
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

### Issue: Containers start but services not accessible

**Diagnosis:**
```bash
# Check if containers are running
docker-compose ps

# Check port bindings
docker-compose port api-gateway 8080

# Test connectivity
curl -v http://localhost:8080/health
```

**Solutions:**

#### 1. Firewall blocking ports
```bash
# Check firewall rules
sudo ufw status

# Allow required ports
sudo ufw allow 8080/tcp
sudo ufw allow 5678/tcp
sudo ufw allow 3000/tcp
sudo ufw allow 9090/tcp
```

#### 2. Network issues
```bash
# Recreate Docker network
docker-compose down
docker network prune
docker-compose up -d
```

---

## Ollama & Model Issues

### Issue: Ollama container fails to start

**Symptoms:**
```bash
docker-compose logs ollama-cpu
# Error: "failed to initialize"
```

**Common Causes:**

#### 1. Insufficient RAM
```bash
# Check available memory
free -h

# TinyLlama needs: ~700MB
# Phi-2 needs: ~1.6GB
# Solution: Upgrade to higher tier or reduce models
```

#### 2. GPU profile on CPU-only system
```bash
# Check docker-compose.yml profile
docker-compose config | grep profile

# Use CPU profile
docker-compose --profile cpu up -d
```

---

### Issue: Models fail to pull

**Symptoms:**
```bash
docker exec ollama ollama pull tinyllama
# Error: "connection refused" or "timeout"
```

**Solutions:**

#### 1. Network connectivity
```bash
# Test internet connection
ping -c 4 ollama.ai

# Test Ollama registry
curl https://registry.ollama.ai/

# Check DNS
cat /etc/resolv.conf
```

#### 2. Disk space
```bash
# Check available space
df -h

# Models require:
# - TinyLlama: ~700MB
# - Phi-2: ~1.6GB
# - Mistral-7B: ~4GB

# Free up space if needed
docker system prune -a
```

#### 3. Rate limiting
```bash
# If pulling multiple models, space them out
docker exec ollama ollama pull tinyllama
sleep 30
docker exec ollama ollama pull phi
```

---

### Issue: Model inference is slow

**Symptoms:**
- TinyLlama taking >5 seconds per request
- Phi-2 taking >10 seconds

**Diagnosis:**
```bash
# Check CPU usage
top
# Look for ollama process

# Check available RAM
free -h

# Check system load
uptime
```

**Solutions:**

#### 1. CPU-bound (100% CPU usage)
```bash
# Reduce concurrent requests
# Edit gateway/app.py
WORKERS=2  # Reduce from 4

# Or upgrade to higher tier
```

#### 2. RAM pressure (swap usage)
```bash
# Check swap usage
free -h | grep Swap

# If swap is being used:
# - Upgrade VPS tier
# - Remove unused models
docker exec ollama ollama rm mistral
```

#### 3. Disk I/O bottleneck
```bash
# Check disk I/O
iostat -x 1 5

# If %util > 80%:
# - Upgrade to SSD-backed VPS
# - Use faster storage tier
```

---

### Issue: "Model not found" errors

**Symptoms:**
```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -d '{"prompt": "test"}'
# Error: "model tinyllama not found"
```

**Solution:**
```bash
# List available models
docker exec ollama ollama list

# Pull missing models
docker exec ollama ollama pull tinyllama
docker exec ollama ollama pull phi

# Restart API Gateway
docker-compose restart api-gateway
```

---

## API Gateway Issues

### Issue: API Gateway returns 500 errors

**Diagnosis:**
```bash
# View detailed logs
docker-compose logs -f api-gateway

# Check for common errors:
# - "ANTHROPIC_API_KEY not set"
# - "Connection refused to ollama"
# - "ModuleNotFoundError"
```

**Solutions:**

#### 1. Missing API key
```bash
# Check .env file
cat .env | grep ANTHROPIC_API_KEY

# Add if missing
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" >> .env

# Restart gateway
docker-compose restart api-gateway
```

#### 2. Ollama connection refused
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not responding, restart Ollama
docker-compose restart ollama-cpu

# Check OLLAMA_URL in .env
echo "OLLAMA_URL=http://ollama-cpu:11434" >> .env
```

#### 3. Python module errors
```bash
# Rebuild API Gateway image
docker-compose build --no-cache api-gateway
docker-compose up -d api-gateway
```

---

### Issue: Requests timing out

**Symptoms:**
```bash
curl -X POST http://localhost:8080/api/v1/chat \
  -d '{"prompt": "test"}'
# (hangs for 60+ seconds, then timeout)
```

**Diagnosis:**
```bash
# Check Gunicorn timeout
docker-compose logs api-gateway | grep timeout

# Check Ollama response time
time docker exec ollama ollama run tinyllama "test"
```

**Solutions:**

#### 1. Increase Gunicorn timeout
```dockerfile
# Edit gateway/Dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:8080", \
     "--timeout", "300", \  # Increase from 120
     "--workers", "4", "gateway.app:app"]
```

#### 2. Reduce concurrent load
```bash
# Limit concurrent requests in app.py
# Or scale up VPS tier
```

---

### Issue: CORS errors in browser

**Symptoms:**
```
Access to XMLHttpRequest at 'http://localhost:8080/api/v1/chat'
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution:**
```python
# Add to gateway/app.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

## Cloud Deployment Issues

### AWS Issues

#### Issue: Terraform fails with "UnauthorizedOperation"

**Cause:** Insufficient IAM permissions

**Solution:**
```bash
# Check AWS credentials
aws sts get-caller-identity

# Verify permissions
aws iam get-user-policy --user-name YOUR_USER --policy-name YOUR_POLICY

# Required permissions:
# - ec2:RunInstances
# - ec2:CreateSecurityGroup
# - ec2:AuthorizeSecurityGroupIngress
# - iam:PassRole (if using instance profiles)
```

---

#### Issue: Instance not accessible via SSH

**Diagnosis:**
```bash
# Check instance state
aws ec2 describe-instances --instance-ids YOUR_INSTANCE_ID

# Check security group
aws ec2 describe-security-groups --group-ids YOUR_SG_ID

# Test connectivity
nc -zv YOUR_INSTANCE_IP 22
```

**Solutions:**

1. **Security group doesn't allow SSH:**
```bash
# Add SSH rule
aws ec2 authorize-security-group-ingress \
  --group-id YOUR_SG_ID \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32
```

2. **Wrong SSH key:**
```bash
# Verify key name matches
terraform output ssh_command

# Use correct key file
ssh -i /path/to/correct-key.pem ubuntu@YOUR_INSTANCE_IP
```

---

#### Issue: User data script didn't run

**Diagnosis:**
```bash
# View cloud-init logs
ssh -i your-key.pem ubuntu@YOUR_INSTANCE_IP
sudo cat /var/log/cloud-init-output.log
```

**Common Issues:**
- Syntax errors in user data script
- Missing sudo permissions
- Network connectivity during setup

**Solution:**
```bash
# Re-run installation manually
ssh -i your-key.pem ubuntu@YOUR_INSTANCE_IP
cd /home/ubuntu
git clone https://github.com/jeremylongshore/hybrid-ai-stack.git
cd hybrid-ai-stack
./install.sh
nano .env  # Add API key
./deploy-all.sh docker
```

---

### GCP Issues

#### Issue: "API not enabled" errors

**Solution:**
```bash
# Enable required APIs
gcloud services enable compute.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com

# List enabled services
gcloud services list --enabled
```

---

#### Issue: Quota exceeded

**Symptoms:**
```
Error: Error waiting for instance to create:
Quota 'CPUS' exceeded. Limit: 8.0 in region us-central1.
```

**Solution:**
```bash
# Check current quotas
gcloud compute project-info describe --project YOUR_PROJECT_ID

# Request quota increase:
# https://console.cloud.google.com/iam-admin/quotas
```

---

## Performance Problems

### Issue: High latency (>10s per request)

**Diagnosis:**
```bash
# Test each component separately
# 1. Ollama directly
time docker exec ollama ollama run tinyllama "test"

# 2. API Gateway
time curl -X POST http://localhost:8080/api/v1/chat \
  -d '{"prompt": "test"}'

# 3. Check system load
uptime
top
```

**Solutions:**

1. **Ollama is slow** → Upgrade VPS tier
2. **Gateway is slow** → Check logs for errors
3. **High system load** → Reduce concurrent requests or upgrade

---

### Issue: Out of memory errors

**Symptoms:**
```bash
docker-compose logs
# Error: "Cannot allocate memory"
# Or: Containers keep getting killed
```

**Diagnosis:**
```bash
# Check memory usage
free -h
docker stats

# Check OOM killer logs
dmesg | grep -i "out of memory"
```

**Solutions:**

1. **Reduce models:**
```bash
# Remove large models
docker exec ollama ollama rm mistral

# Restart with only TinyLlama
```

2. **Upgrade VPS tier:**
- Tier 1 (2GB) → Tier 2 (4GB)
- Tier 2 (4GB) → Tier 3 (8GB)

3. **Add swap space (temporary):**
```bash
# Create 2GB swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Data & Cost Tracking Issues

### Issue: Taskwarrior not tracking costs

**Diagnosis:**
```bash
# Check if Taskwarrior is installed
task --version

# Check router logs
docker-compose logs api-gateway | grep -i taskwarrior
```

**Solutions:**

1. **Taskwarrior not initialized:**
```bash
# Initialize
task --version  # First run initializes

# Verify
task list
```

2. **Permission issues:**
```bash
# Fix permissions
chmod 755 ~/.task
chmod 644 ~/.taskrc
```

---

### Issue: Prometheus not scraping metrics

**Diagnosis:**
```bash
# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check if metrics endpoint is accessible
curl http://localhost:8080/metrics
```

**Solutions:**

1. **API Gateway metrics not exposed:**
```python
# Verify in gateway/app.py
from prometheus_client import generate_latest
@app.route('/metrics')
def metrics():
    return generate_latest()
```

2. **Prometheus configuration:**
```yaml
# Check prometheus.yml
scrape_configs:
  - job_name: 'api-gateway'
    static_configs:
      - targets: ['api-gateway:8080']
```

---

## Emergency Reset

### Complete System Reset

```bash
#!/bin/bash
# Use this as last resort

echo "⚠️  WARNING: This will delete ALL data!"
read -p "Are you sure? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 1
fi

# Stop all containers
docker-compose down -v

# Remove all containers
docker container prune -f

# Remove all volumes
docker volume prune -f

# Remove all networks
docker network prune -f

# Clean Docker system
docker system prune -a -f

# Reinstall
./install.sh

# Reconfigure
nano .env  # Add your API key

# Redeploy
./deploy-all.sh docker

echo "✅ System reset complete!"
```

---

**Related Documentation:**
- [Quick Start Guide](./QUICKSTART.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Monitoring Guide](./MONITORING.md)
- [Architecture Overview](./ARCHITECTURE.md)

[⬆ Back to Top](#-troubleshooting-guide)
