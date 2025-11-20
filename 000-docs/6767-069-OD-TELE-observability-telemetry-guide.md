# Observability & Telemetry Guide for Bob's Brain

**Date:** 2025-11-19
**Project:** Bob's Brain (bobs-brain)
**Purpose:** Guide to observing, monitoring, and analyzing Bob's Brain deployment on Vertex AI Agent Engine
**Status:** Production

---

## Overview

Bob's Brain is deployed to **Vertex AI Agent Engine** with automatic telemetry enabled via the `--trace_to_cloud` flag. This provides comprehensive observability including:

- **Cloud Trace** - Distributed tracing of agent invocations
- **Cloud Logging** - Structured logs with SPIFFE ID propagation
- **Cloud Monitoring** - Performance metrics and dashboards
- **Error Reporting** - Exception tracking and aggregation

---

## Automatic Telemetry with Agent Engine

### What's Included (No Configuration Required)

When deployed with `adk deploy agent_engine --trace_to_cloud`, Agent Engine automatically:

✅ **Traces every agent invocation** with:
- Request/response timing
- Tool execution spans
- Memory service operations (Session + Memory Bank)
- Model inference latency
- Gateway-to-agent communication

✅ **Logs all agent activity** with:
- Structured JSON logging
- SPIFFE ID in every log entry (`spiffe://intent.solutions/agent/bobs-brain/...`)
- Request/response payloads (configurable verbosity)
- Error stack traces

✅ **Metrics for performance** including:
- Agent invocation count
- Average response time
- Token usage
- Error rate
- Memory operations (read/write)

✅ **Error tracking** with:
- Exception grouping
- Stack trace analysis
- Frequency counts
- Affected users

---

## Cloud Trace: Distributed Tracing

### Accessing Cloud Trace

**Console URL:**
```
https://console.cloud.google.com/traces/list?project=bobs-brain-dev
```

Or navigate:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: `bobs-brain-dev`
3. Navigate to: **Operations → Trace → Trace List**

### What You'll See

**Trace Structure:**
```
Agent Invocation (root span)
├── Gateway Request (HTTP)
│   └── Agent Engine API Call
│       ├── LlmAgent Execution
│       │   ├── Session Service Read
│       │   ├── Memory Bank Retrieval
│       │   ├── Model Inference (Gemini)
│       │   ├── Tool Execution (if any)
│       │   └── After Agent Callback (auto-save)
│       └── Session Service Write
└── Gateway Response (HTTP)
```

**Key Metrics per Trace:**
- **Total latency** - End-to-end request time
- **Agent execution time** - Time spent in LlmAgent
- **Model inference time** - LLM response latency
- **Memory operations** - Session/Memory Bank read/write time
- **Tool execution** - Time spent in custom tools (if used)

### Filtering Traces

**By SPIFFE ID (Environment-Specific):**
```
resource.labels.spiffe_id="spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0"
```

**By Time Range:**
- Last hour
- Last 24 hours
- Last 7 days
- Custom range

**By Latency:**
- > 1 second (slow requests)
- > 5 seconds (very slow requests)
- > 10 seconds (timeout risk)

**By Status:**
- Successful (HTTP 200)
- Client errors (HTTP 4xx)
- Server errors (HTTP 5xx)

### Analyzing Slow Requests

1. **Sort by latency** (descending)
2. **Click trace ID** to see detailed span breakdown
3. **Identify bottlenecks:**
   - Model inference taking too long? (check token count)
   - Memory Bank slow? (check index size)
   - Tool execution hanging? (review tool implementation)
4. **Compare to baseline** (normal traces)
5. **Investigate logs** for that trace ID

---

## Cloud Logging: Structured Logs

### Accessing Cloud Logging

**Console URL:**
```
https://console.cloud.google.com/logs/query?project=bobs-brain-dev
```

Or navigate:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: `bobs-brain-dev`
3. Navigate to: **Operations → Logging → Logs Explorer**

### Log Queries

**All Agent Engine logs:**
```
resource.type="aiplatform.googleapis.com/AgentEngine"
resource.labels.agent_engine_id="AGENT_ENGINE_ID"
```

**Logs with SPIFFE ID:**
```
jsonPayload.spiffe_id="spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0"
```

**Error logs only:**
```
severity >= ERROR
resource.type="aiplatform.googleapis.com/AgentEngine"
```

**Recent agent invocations:**
```
jsonPayload.message:"Agent invocation"
timestamp >= "2025-11-19T00:00:00Z"
```

**Memory Bank operations:**
```
jsonPayload.message:"Memory Bank"
OR jsonPayload.message:"auto-save"
```

**Gateway logs (A2A + Slack):**
```
resource.type="cloud_run_revision"
resource.labels.service_name=~"bobs-brain-.*-gateway"
```

### Log Structure

**Agent Invocation Log:**
```json
{
  "timestamp": "2025-11-19T12:34:56.789Z",
  "severity": "INFO",
  "message": "Agent invocation started",
  "jsonPayload": {
    "app_name": "bobs-brain",
    "spiffe_id": "spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0",
    "trace_id": "1234567890abcdef",
    "session_id": "session-abc123",
    "user_message": "What is ADK?",
    "agent_version": "0.6.0"
  }
}
```

**Memory Auto-Save Log:**
```json
{
  "timestamp": "2025-11-19T12:34:57.123Z",
  "severity": "INFO",
  "message": "Successfully saved session to Memory Bank",
  "jsonPayload": {
    "spiffe_id": "spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0",
    "session_id": "session-abc123",
    "memory_bank_id": "memory-xyz789",
    "turn_count": 3
  }
}
```

**Error Log:**
```json
{
  "timestamp": "2025-11-19T12:35:00.456Z",
  "severity": "ERROR",
  "message": "Failed to retrieve from Memory Bank",
  "jsonPayload": {
    "spiffe_id": "spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0",
    "error": "PermissionDenied: Service account lacks roles/aiplatform.user",
    "stack_trace": "..."
  }
}
```

---

## Cloud Monitoring: Dashboards & Metrics

### Accessing Cloud Monitoring

**Console URL:**
```
https://console.cloud.google.com/monitoring?project=bobs-brain-dev
```

Or navigate:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: `bobs-brain-dev`
3. Navigate to: **Operations → Monitoring → Dashboards**

### Key Metrics

**Agent Engine Metrics:**
- `aiplatform.googleapis.com/reasoning_engine/request_count` - Total invocations
- `aiplatform.googleapis.com/reasoning_engine/request_latencies` - Response time distribution
- `aiplatform.googleapis.com/reasoning_engine/error_count` - Failed invocations
- `aiplatform.googleapis.com/reasoning_engine/token_count` - Total tokens consumed

**Cloud Run Gateway Metrics:**
- `run.googleapis.com/request_count` - Gateway HTTP requests
- `run.googleapis.com/request_latencies` - Gateway response time
- `run.googleapis.com/container/cpu/utilization` - CPU usage
- `run.googleapis.com/container/memory/utilization` - Memory usage

### Creating a Custom Dashboard

1. Go to **Monitoring → Dashboards → Create Dashboard**
2. Add these charts:

**Chart 1: Agent Invocations (Line Chart)**
```
Metric: aiplatform.googleapis.com/reasoning_engine/request_count
Filter: agent_engine_id = "AGENT_ENGINE_ID"
Aggregator: Rate (1m)
```

**Chart 2: Average Response Time (Line Chart)**
```
Metric: aiplatform.googleapis.com/reasoning_engine/request_latencies
Filter: agent_engine_id = "AGENT_ENGINE_ID"
Aggregator: 50th percentile (median)
```

**Chart 3: Error Rate (Line Chart)**
```
Metric: aiplatform.googleapis.com/reasoning_engine/error_count
Filter: agent_engine_id = "AGENT_ENGINE_ID"
Aggregator: Rate (1m)
```

**Chart 4: Token Usage (Stacked Area)**
```
Metric: aiplatform.googleapis.com/reasoning_engine/token_count
Filter: agent_engine_id = "AGENT_ENGINE_ID"
Group by: token_type (input/output)
```

**Chart 5: Gateway Health (Heatmap)**
```
Metric: run.googleapis.com/request_latencies
Filter: service_name = "bobs-brain-a2a-gateway"
Aggregator: Heatmap (percentiles)
```

3. **Save dashboard** as "Bob's Brain Production Monitoring"

---

## Error Reporting: Exception Tracking

### Accessing Error Reporting

**Console URL:**
```
https://console.cloud.google.com/errors?project=bobs-brain-dev
```

Or navigate:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select project: `bobs-brain-dev`
3. Navigate to: **Operations → Error Reporting**

### What You'll See

**Error Groups:**
- Automatically grouped by exception type and stack trace
- Frequency counts (last hour, day, week)
- First/last occurrence timestamps
- Affected users (if available)

**Common Error Patterns:**

1. **Permission Errors:**
   ```
   google.api_core.exceptions.PermissionDenied:
   Service account lacks required role
   ```
   **Fix:** Check IAM permissions in `infra/terraform/iam.tf`

2. **Memory Bank Errors:**
   ```
   google.api_core.exceptions.NotFound:
   Memory Bank not found
   ```
   **Fix:** Verify AGENT_ENGINE_ID is correct, check Memory Bank creation

3. **Model Errors:**
   ```
   google.api_core.exceptions.ResourceExhausted:
   Rate limit exceeded
   ```
   **Fix:** Implement exponential backoff, request quota increase

4. **Timeout Errors:**
   ```
   google.api_core.exceptions.DeadlineExceeded:
   Agent execution timeout
   ```
   **Fix:** Optimize tool execution, increase timeout in Agent Engine config

### Setting Up Alerts

1. **Go to Error Reporting → Configure Notifications**
2. **Select error group** (e.g., "PermissionDenied")
3. **Add notification channel:**
   - Email: `claude.buildcaptain@intentsolutions.io`
   - Slack: `#bobs-brain-alerts` (optional)
4. **Set threshold:** Alert if error occurs > 5 times in 1 hour
5. **Save alert**

---

## Alert Policies (Recommended)

### 1. High Error Rate Alert

**Condition:**
```
Metric: aiplatform.googleapis.com/reasoning_engine/error_count
Condition: Rate > 5 errors/minute for 5 minutes
Notification: Email + Slack
```

**Why:** Indicates systemic issue (API failure, permission error, model unavailable)

### 2. Slow Response Time Alert

**Condition:**
```
Metric: aiplatform.googleapis.com/reasoning_engine/request_latencies
Condition: 95th percentile > 10 seconds for 5 minutes
Notification: Email
```

**Why:** Users experiencing poor performance, may indicate resource constraints

### 3. Gateway Downtime Alert

**Condition:**
```
Metric: run.googleapis.com/request_count
Condition: Count = 0 for 5 minutes
Notification: Email + SMS (critical)
```

**Why:** Gateway not receiving requests, deployment may have failed

### 4. Memory Bank Failure Alert

**Condition:**
```
Log-based metric: "Failed to save session to Memory Bank"
Condition: Count > 10 in 10 minutes
Notification: Email
```

**Why:** Memory persistence failing, conversation context being lost

---

## Debugging Agent Issues

### Step-by-Step Debugging Process

**1. Check Agent Engine Deployment**
```bash
gcloud ai reasoning-engines list \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --filter="displayName:bobs-brain"
```

**Expected output:**
```
NAME: projects/.../locations/us-central1/reasoningEngines/AGENT_ENGINE_ID
DISPLAY_NAME: bobs-brain-dev
CREATE_TIME: 2025-11-19T12:00:00Z
UPDATE_TIME: 2025-11-19T12:00:00Z
```

**2. Check Recent Logs**
```
https://console.cloud.google.com/logs/query?project=bobs-brain-dev&query=resource.type%3D%22aiplatform.googleapis.com%2FAgentEngine%22%0Atimestamp%3E%3D%222025-11-19T00%3A00%3A00Z%22
```

**3. Check Cloud Trace for Failed Requests**
- Filter by `status_code >= 400`
- Look for spans with errors
- Check timing of each span

**4. Check Error Reporting**
- Look for new error groups
- Check frequency (one-off vs repeated)
- Review stack traces

**5. Verify Gateway Health**
```bash
curl https://bobs-brain-a2a-gateway-HASH-uc.a.run.app/card
```

**Expected:** AgentCard JSON with SPIFFE ID

**6. Test Agent Directly (Local)**
```bash
cd /home/jeremy/000-projects/iams/bobs-brain/
export PROJECT_ID=bobs-brain-dev
export LOCATION=us-central1
export AGENT_ENGINE_ID=<from step 1>

python3 -c "
from my_agent.agent import create_runner
runner = create_runner()
response = runner.run('What is ADK?', session_id='test-debug')
print(response)
"
```

---

## Performance Optimization

### Baseline Metrics (Target)

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Average response time | < 2 seconds | > 5 seconds |
| P95 response time | < 5 seconds | > 10 seconds |
| Error rate | < 1% | > 5% |
| Token usage (per request) | < 1000 tokens | > 5000 tokens |
| Memory Bank write time | < 500ms | > 2 seconds |

### Optimization Strategies

**1. Reduce Model Latency:**
- Use streaming responses (`stream=True` in LlmAgent)
- Optimize prompt length (shorter instructions)
- Use faster model (gemini-2.0-flash-exp vs gemini-1.5-pro)

**2. Optimize Memory Operations:**
- Limit Memory Bank retrieval count (`max_results=5`)
- Cache recent sessions in gateway (if appropriate)
- Use Session Service for short-term memory (already implemented)

**3. Gateway Performance:**
- Increase Cloud Run max instances (`gateway_max_instances` in tfvars)
- Enable HTTP/2 (default in Cloud Run)
- Use connection pooling for Agent Engine API calls

**4. Cost Optimization:**
- Monitor token usage per user
- Set max_tokens limit in LlmAgent config
- Use cheaper model for simple queries (implement routing logic)

---

## Verification Checklist

After deployment, verify telemetry is working:

- [ ] **Cloud Trace** shows new traces (within 2 minutes of test invocation)
- [ ] **Cloud Logging** shows agent invocation logs with SPIFFE ID
- [ ] **Cloud Monitoring** shows metrics for Agent Engine (request_count > 0)
- [ ] **Error Reporting** is empty (no errors) OR shows expected startup warnings
- [ ] **Gateway logs** show successful requests to Agent Engine API
- [ ] **SPIFFE ID** appears in logs, traces, and HTTP headers
- [ ] **Memory Bank** auto-save logs appear after agent turns
- [ ] **Session Service** logs show session read/write operations

---

## Troubleshooting Common Issues

### "No traces appearing in Cloud Trace"

**Possible causes:**
1. `--trace_to_cloud` flag missing in deployment
2. Agent Engine API permissions issue
3. Trace sampling rate too low (default is 100%)

**Fix:**
```bash
# Verify deployment includes tracing
gcloud ai reasoning-engines describe $AGENT_ENGINE_ID \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --format="value(traceConfig)"
```

### "SPIFFE ID not appearing in logs"

**Possible causes:**
1. `AGENT_SPIFFE_ID` environment variable not set
2. Agent code not propagating SPIFFE ID to logs

**Fix:**
```bash
# Check environment variables in Agent Engine
gcloud ai reasoning-engines describe $AGENT_ENGINE_ID \
  --project=bobs-brain-dev \
  --region=us-central1 \
  --format="value(environmentVariables)"
```

Should include:
```
AGENT_SPIFFE_ID=spiffe://intent.solutions/agent/bobs-brain/dev/us-central1/0.6.0
```

### "Memory Bank auto-save failing"

**Possible causes:**
1. Service account lacks `roles/aiplatform.user`
2. Memory Bank not created yet
3. `after_agent_callback` not wired correctly

**Fix:**
```bash
# Check IAM permissions
gcloud projects get-iam-policy bobs-brain-dev \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:agent-engine@bobs-brain-dev.iam.gserviceaccount.com" \
  --format="table(bindings.role)"
```

Should include `roles/aiplatform.user`.

---

## Next Steps

1. **Deploy to dev environment** (follow `6767-070-OD-RBOK-deployment-runbook.md`)
2. **Verify all telemetry** (use checklist above)
3. **Create custom dashboard** (follow "Creating a Custom Dashboard" section)
4. **Set up alert policies** (use recommended alerts)
5. **Monitor for 24 hours** (establish baseline metrics)
6. **Tune as needed** (optimize based on observed performance)

---

## References

- **Cloud Trace Docs:** https://cloud.google.com/trace/docs
- **Cloud Logging Docs:** https://cloud.google.com/logging/docs
- **Cloud Monitoring Docs:** https://cloud.google.com/monitoring/docs
- **Error Reporting Docs:** https://cloud.google.com/error-reporting/docs
- **Agent Engine Telemetry:** (ADK docs, symlinked in `000-docs/google-reference/adk/`)

---

**Document Status:** Complete ✅
**Last Updated:** 2025-11-19
**Category:** Operations & Deployment - Telemetry

---
