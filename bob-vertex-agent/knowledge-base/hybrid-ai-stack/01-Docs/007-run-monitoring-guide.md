# 📊 Monitoring & Observability Guide

> **Navigation**: [← Back to Cost Optimization](./COST-OPTIMIZATION.md) | [Next: Troubleshooting →](./TROUBLESHOOTING.md)

<details>
<parameter name="summary"><b>📋 TL;DR</b> - Click to expand</summary>

**Quick monitoring setup:**
1. Grafana: http://localhost:3000 (admin/admin)
2. Prometheus: http://localhost:9090
3. Metrics endpoint: http://localhost:8080/metrics
4. Pre-built dashboards in `monitoring/grafana/`

**Key metrics to watch:**
- Request routing distribution (local vs cloud)
- API costs
- Response latency
- Model performance

</details>

---

## Table of Contents
- [Monitoring Stack Overview](#monitoring-stack-overview)
- [Prometheus Setup](#prometheus-setup)
- [Grafana Dashboards](#grafana-dashboards)
- [Key Metrics](#key-metrics)
- [Alerting Rules](#alerting-rules)
- [Log Aggregation](#log-aggregation)
- [Performance Monitoring](#performance-monitoring)

## Monitoring Stack Overview

```mermaid
graph TB
    subgraph "Data Sources"
        AG[API Gateway<br/>Flask App]
        OL[Ollama<br/>Local Models]
        N8[n8n<br/>Workflows]
        TW[Taskwarrior<br/>Task Tracking]
    end

    subgraph "Collection Layer"
        PM[Prometheus<br/>:9090<br/>Metrics Storage]
        LE[Loki<br/>Optional<br/>Log Aggregation]
    end

    subgraph "Visualization Layer"
        GF[Grafana<br/>:3000<br/>Dashboards]
    end

    subgraph "Alerting"
        AM[Alertmanager<br/>Optional<br/>Alert Routing]
        SLACK[Slack<br/>Notifications]
        EMAIL[Email<br/>Alerts]
    end

    AG -->|/metrics| PM
    OL -->|health| PM
    N8 -->|logs| LE
    TW -->|export| AG

    PM --> GF
    LE --> GF

    PM --> AM
    AM --> SLACK
    AM --> EMAIL

    style PM fill:#E27D60
    style GF fill:#85D8CE
    style AG fill:#4A90E2
```

### Components

| Component | Purpose | Port | Status |
|-----------|---------|------|--------|
| **Prometheus** | Metrics collection & storage | 9090 | ✅ Included |
| **Grafana** | Visualization & dashboards | 3000 | ✅ Included |
| **Alertmanager** | Alert routing & grouping | 9093 | ⭕ Optional |
| **Loki** | Log aggregation | 3100 | ⭕ Optional |

---

## Prometheus Setup

### Configuration

**File**: `monitoring/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

# Scrape configurations
scrape_configs:
  # API Gateway metrics
  - job_name: 'api-gateway'
    static_configs:
      - targets: ['api-gateway:8080']
    metrics_path: '/metrics'

  # Ollama health
  - job_name: 'ollama'
    static_configs:
      - targets: ['ollama-cpu:11434']
    metrics_path: '/health'
    scrape_interval: 30s

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # n8n metrics (if enabled)
  - job_name: 'n8n'
    static_configs:
      - targets: ['n8n:5678']
    metrics_path: '/metrics'
```

### Accessing Prometheus

```bash
# Open Prometheus UI
open http://localhost:9090

# Query metrics directly
curl http://localhost:9090/api/v1/query?query=api_gateway_requests_total

# View all available metrics
curl http://localhost:8080/metrics
```

### Prometheus Queries (PromQL)

```promql
# Total requests
sum(api_gateway_requests_total)

# Requests by model
sum by (model) (api_gateway_requests_total)

# Request rate (requests per second)
rate(api_gateway_requests_total[5m])

# Average latency
avg(api_gateway_request_duration_seconds)

# 95th percentile latency
histogram_quantile(0.95, api_gateway_request_duration_seconds_bucket)

# Total API costs
sum(api_gateway_cost_total)

# Cost by model
sum by (model) (api_gateway_cost_total)

# Error rate
rate(api_gateway_requests_total{status="error"}[5m])

# Local vs Cloud ratio
sum(api_gateway_requests_total{backend="local"}) / sum(api_gateway_requests_total)
```

---

## Grafana Dashboards

### Initial Setup

```bash
# Access Grafana
open http://localhost:3000

# Default credentials
Username: admin
Password: admin
# (You'll be prompted to change on first login)
```

### Add Prometheus Data Source

1. Navigate to **Configuration → Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Configure:
   ```
   Name: Prometheus
   URL: http://prometheus:9090
   Access: Server (default)
   ```
5. Click **Save & Test**

### Import Pre-Built Dashboards

**Option 1: Import from file**

```bash
# Grafana UI:
# Create → Import → Upload JSON file
# Select: monitoring/grafana/hybrid-ai-stack-dashboard.json
```

**Option 2: Import via API**

```bash
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @monitoring/grafana/hybrid-ai-stack-dashboard.json
```

### Main Dashboard Panels

#### Panel 1: Request Overview

```json
{
  "title": "Total Requests (24h)",
  "targets": [{
    "expr": "sum(increase(api_gateway_requests_total[24h]))"
  }],
  "type": "stat"
}
```

#### Panel 2: Routing Distribution

```json
{
  "title": "Request Distribution by Model",
  "targets": [{
    "expr": "sum by (model) (api_gateway_requests_total)",
    "legendFormat": "{{model}}"
  }],
  "type": "pie"
}
```

#### Panel 3: Cost Tracking

```json
{
  "title": "API Costs Over Time",
  "targets": [{
    "expr": "sum(api_gateway_cost_total)",
    "legendFormat": "Total Cost"
  }],
  "type": "graph"
}
```

#### Panel 4: Latency Heatmap

```json
{
  "title": "Response Latency Distribution",
  "targets": [{
    "expr": "histogram_quantile(0.95, api_gateway_request_duration_seconds_bucket)"
  }],
  "type": "heatmap"
}
```

### Complete Dashboard JSON

**File**: `monitoring/grafana/hybrid-ai-stack-dashboard.json`

```json
{
  "dashboard": {
    "title": "Hybrid AI Stack - Main Dashboard",
    "panels": [
      {
        "id": 1,
        "title": "Total Requests (24h)",
        "type": "stat",
        "gridPos": {"x": 0, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "sum(increase(api_gateway_requests_total[24h]))",
          "refId": "A"
        }]
      },
      {
        "id": 2,
        "title": "Local vs Cloud Requests",
        "type": "pie",
        "gridPos": {"x": 6, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "sum by (backend) (api_gateway_requests_total)",
          "legendFormat": "{{backend}}",
          "refId": "A"
        }]
      },
      {
        "id": 3,
        "title": "Total API Costs (30d)",
        "type": "stat",
        "gridPos": {"x": 12, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "sum(api_gateway_cost_total)",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "currencyUSD"
          }
        }
      },
      {
        "id": 4,
        "title": "Average Latency",
        "type": "stat",
        "gridPos": {"x": 18, "y": 0, "w": 6, "h": 4},
        "targets": [{
          "expr": "avg(api_gateway_request_duration_seconds)",
          "refId": "A"
        }],
        "fieldConfig": {
          "defaults": {
            "unit": "s"
          }
        }
      },
      {
        "id": 5,
        "title": "Requests by Model Over Time",
        "type": "graph",
        "gridPos": {"x": 0, "y": 4, "w": 12, "h": 8},
        "targets": [{
          "expr": "sum by (model) (rate(api_gateway_requests_total[5m]))",
          "legendFormat": "{{model}}",
          "refId": "A"
        }],
        "yaxes": [
          {"format": "reqps", "label": "Requests/sec"},
          {"format": "short"}
        ]
      },
      {
        "id": 6,
        "title": "Cost Accumulation",
        "type": "graph",
        "gridPos": {"x": 12, "y": 4, "w": 12, "h": 8},
        "targets": [{
          "expr": "sum by (model) (api_gateway_cost_total)",
          "legendFormat": "{{model}}",
          "refId": "A"
        }],
        "yaxes": [
          {"format": "currencyUSD", "label": "Cost"},
          {"format": "short"}
        ]
      },
      {
        "id": 7,
        "title": "Response Latency by Model",
        "type": "graph",
        "gridPos": {"x": 0, "y": 12, "w": 24, "h": 8},
        "targets": [
          {
            "expr": "histogram_quantile(0.50, sum by (model, le) (rate(api_gateway_request_duration_seconds_bucket[5m])))",
            "legendFormat": "{{model}} p50",
            "refId": "A"
          },
          {
            "expr": "histogram_quantile(0.95, sum by (model, le) (rate(api_gateway_request_duration_seconds_bucket[5m])))",
            "legendFormat": "{{model}} p95",
            "refId": "B"
          },
          {
            "expr": "histogram_quantile(0.99, sum by (model, le) (rate(api_gateway_request_duration_seconds_bucket[5m])))",
            "legendFormat": "{{model}} p99",
            "refId": "C"
          }
        ]
      }
    ],
    "refresh": "30s",
    "time": {
      "from": "now-24h",
      "to": "now"
    }
  }
}
```

---

## Key Metrics

### Request Metrics

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `api_gateway_requests_total` | Counter | Total requests processed | `sum(api_gateway_requests_total)` |
| `api_gateway_request_duration_seconds` | Histogram | Request latency distribution | `histogram_quantile(0.95, ...)` |
| `api_gateway_requests_in_progress` | Gauge | Concurrent requests | `api_gateway_requests_in_progress` |

**Labels:**
- `model`: tinyllama, phi2, claude-sonnet
- `backend`: local, cloud
- `status`: success, error
- `complexity`: low, medium, high

### Cost Metrics

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `api_gateway_cost_total` | Counter | Cumulative API costs | `sum(api_gateway_cost_total)` |
| `api_gateway_cost_per_request` | Gauge | Average cost per request | `sum(api_gateway_cost_total) / sum(api_gateway_requests_total)` |

**Labels:**
- `model`: Model that incurred the cost

### Performance Metrics

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `api_gateway_model_latency_seconds` | Histogram | Model inference time | `avg(api_gateway_model_latency_seconds)` |
| `api_gateway_routing_latency_seconds` | Histogram | Routing decision time | `avg(api_gateway_routing_latency_seconds)` |

### Health Metrics

| Metric | Type | Description | Example Query |
|--------|------|-------------|---------------|
| `api_gateway_health` | Gauge | Service health status (1=healthy, 0=unhealthy) | `api_gateway_health` |
| `ollama_models_loaded` | Gauge | Number of models loaded | `ollama_models_loaded` |

---

## Alerting Rules

### Prometheus Alert Rules

**File**: `monitoring/prometheus/alert.rules.yml`

```yaml
groups:
  - name: hybrid-ai-stack
    interval: 30s
    rules:
      # High API costs
      - alert: HighAPICosts
        expr: rate(api_gateway_cost_total[1h]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High API costs detected"
          description: "API costs are increasing rapidly ({% raw %}{{ $value }}{% endraw %}/hour)"

      # High error rate
      - alert: HighErrorRate
        expr: rate(api_gateway_requests_total{status="error"}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
          description: "Error rate is {% raw %}{{ $value }}{% endraw %}/sec"

      # Slow response times
      - alert: SlowResponses
        expr: histogram_quantile(0.95, rate(api_gateway_request_duration_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Slow response times"
          description: "95th percentile latency is {% raw %}{{ $value }}{% endraw %}s"

      # Ollama service down
      - alert: OllamaDown
        expr: up{job="ollama"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Ollama service is down"
          description: "Local model inference is unavailable"

      # Too many cloud requests
      - alert: ExcessiveCloudUsage
        expr: sum(rate(api_gateway_requests_total{backend="cloud"}[1h])) / sum(rate(api_gateway_requests_total[1h])) > 0.5
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Excessive cloud API usage"
          description: "{{ $value | humanizePercentage }} of requests going to cloud"

      # Low local routing
      - alert: LowLocalRouting
        expr: sum(rate(api_gateway_requests_total{backend="local"}[1h])) / sum(rate(api_gateway_requests_total[1h])) < 0.3
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "Low local model usage"
          description: "Only {{ $value | humanizePercentage }} of requests using local models"
```

### Alertmanager Configuration

**File**: `monitoring/alertmanager/config.yml`

```yaml
global:
  resolve_timeout: 5m
  slack_api_url: 'YOUR_SLACK_WEBHOOK_URL'

route:
  group_by: ['alertname', 'severity']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'default'

  routes:
    # Critical alerts to Slack + Email
    - match:
        severity: critical
      receiver: 'critical-alerts'

    # Warnings to Slack only
    - match:
        severity: warning
      receiver: 'warning-alerts'

receivers:
  - name: 'default'
    email_configs:
      - to: 'admin@example.com'
        from: 'prometheus@example.com'
        smarthost: 'smtp.example.com:587'
        auth_username: 'prometheus@example.com'
        auth_password: 'YOUR_PASSWORD'

  - name: 'critical-alerts'
    slack_configs:
      - channel: '#alerts-critical'
        title: '🚨 Critical Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
    email_configs:
      - to: 'admin@example.com'

  - name: 'warning-alerts'
    slack_configs:
      - channel: '#alerts-warning'
        title: '⚠️ Warning: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'
```

---

## Log Aggregation

### Loki Setup (Optional)

```yaml
# docker-compose.yml addition
services:
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./monitoring/loki/config.yml:/etc/loki/config.yml
      - loki_data:/loki
    command: -config.file=/etc/loki/config.yml
    networks:
      - demo

  promtail:
    image: grafana/promtail:latest
    volumes:
      - ./monitoring/promtail/config.yml:/etc/promtail/config.yml
      - /var/log:/var/log
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    networks:
      - demo
```

### Viewing Logs in Grafana

```bash
# Add Loki data source in Grafana
# Configuration → Data Sources → Add data source → Loki
# URL: http://loki:3100

# Create Explore query
# Select Loki data source
# Query: {job="api-gateway"} |= "error"
```

---

## Performance Monitoring

### System Resource Monitoring

```bash
# Add node_exporter to docker-compose.yml
services:
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    networks:
      - demo
```

### Key System Metrics

```promql
# CPU usage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Memory usage
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk usage
(1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100

# Network throughput
rate(node_network_receive_bytes_total[5m])
```

### Application Performance

```bash
# Add Python profiling
pip install py-spy

# Profile API Gateway
py-spy top --pid $(pgrep -f gunicorn)

# Generate flame graph
py-spy record -o profile.svg --pid $(pgrep -f gunicorn) --duration 60
```

---

## Monitoring Best Practices

### 1. Set Up Alerting Early

```bash
# Test alerts
curl -X POST http://localhost:9090/-/reload

# Verify alert rules
curl http://localhost:9090/api/v1/rules
```

### 2. Create Custom Dashboards

Focus on:
- Request volume and distribution
- Cost tracking and trends
- Performance metrics (latency, throughput)
- Error rates and types
- Resource utilization

### 3. Regular Review

```bash
# Weekly: Review cost trends
# Monthly: Analyze routing decisions
# Quarterly: Optimize thresholds
```

### 4. Retention Policy

```yaml
# prometheus.yml
storage:
  tsdb:
    retention.time: 30d
    retention.size: 10GB
```

### 5. Backup Configuration

```bash
# Backup Prometheus data
docker exec prometheus tar czf /tmp/prometheus-backup.tar.gz /prometheus

# Backup Grafana dashboards
curl http://admin:admin@localhost:3000/api/dashboards/export > dashboards-backup.json
```

---

**Related Documentation:**
- [Architecture Overview](./ARCHITECTURE.md)
- [Cost Optimization](./COST-OPTIMIZATION.md)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [Deployment Guide](./DEPLOYMENT.md)

[⬆ Back to Top](#-monitoring--observability-guide)
