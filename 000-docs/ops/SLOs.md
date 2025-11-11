# Bob's Brain — Service Level Objectives (SLOs)

**Last Updated:** 2025-11-11
**Owner:** Build Captain
**Status:** Active

---

## Overview

This document defines the Service Level Objectives (SLOs) and Service Level Indicators (SLIs) for Bob's Brain production gateway service. These targets guide operational excellence and inform alerting thresholds.

## Service Level Objectives

### 1. Gateway Latency (P95)
**SLO:** P95 gateway latency ≤ 10s over 7-day window

**SLI Measurement:**
- Metric: `run.googleapis.com/request_latencies`
- Resource: `cloud_run_revision` (service: `bobs-brain-gateway`)
- Aggregation: 95th percentile, 60s alignment period
- Alert threshold: > 10,000ms sustained for 5 minutes

**Rationale:** Gateway proxies to Vertex AI Reasoning Engine with potential cold starts. 10s P95 allows for engine processing while maintaining good UX.

---

### 2. Gateway Error Rate
**SLO:** Gateway error rate ≤ 5% over 7-day window

**SLI Measurement:**
- Metric: `run.googleapis.com/request_count`
- Resource: `cloud_run_revision` (service: `bobs-brain-gateway`)
- Filter: Response codes 5xx vs all responses
- Calculation: `1 - (2xx+3xx) / total`
- Alert threshold: > 5% sustained for 5 minutes

**Rationale:** Includes both gateway failures and Reasoning Engine timeouts. 5% allows for transient engine errors while maintaining reliability.

---

### 3. Reasoning Engine Error Rate
**SLO:** Reasoning Engine error rate ≤ 5% over 7-day window

**SLI Measurement:**
- Metric: HTTP status codes from Reasoning Engine API
- Source: Gateway logs and OpenTelemetry traces
- Calculation: 5xx responses / total engine calls
- Alert threshold: > 5% sustained for 5 minutes

**Rationale:** Tracks backend reliability independently from gateway. 5% threshold accounts for model timeouts and rate limits.

---

### 4. Service Uptime
**SLO:** Uptime ≥ 99.5% monthly (based on `/_health` endpoint)

**SLI Measurement:**
- Endpoint: `GET /_health`
- Success criteria: HTTP 200 with `{"status": "ok"}`
- Measurement: Synthetic probes every 15 minutes
- Calculation: Successful checks / total checks
- Monthly target: ≥ 99.5% (allows ~3.6 hours downtime/month)

**Rationale:** Health endpoint validates gateway availability and basic connectivity. Does not include full agent execution path.

---

### 5. Canary Deployment Safety
**SLO:** Canary fail-stop within 2 minutes

**SLI Measurement:**
- Trigger: Blue/green deployment workflow
- Health checks: `/_health`, `/invoke`, `/card`
- Timeout: 2 minutes (120 seconds)
- Success criteria: All checks pass OR rollback completes within window

**Rationale:** Fast feedback loop during deployments prevents bad revisions from reaching production traffic.

---

## SLO Monitoring

### Dashboards
- **Cloud Monitoring Dashboard:** `Bob Gateway — Prod`
  - P95 latency trend (7-day rolling window)
  - Error rate % (gateway + engine)
  - Request count and traffic distribution
  - Trace samples with high latency

### Alerts
- **Latency Alert:** Fires when P95 > 10s for 5 minutes
- **Error Rate Alert:** Fires when error % > 5% for 5 minutes
- **Budget Alert:** Fires at 80% and 100% of monthly spend

### Synthetic Checks
- **Frequency:** Every 15 minutes
- **Workflow:** `.github/workflows/synthetic.yaml`
- **Checks:** Health endpoint + basic invoke
- **Timeout:** 5 seconds per check

---

## SLO Review Process

### Weekly Review
- Review dashboard for SLO compliance
- Investigate any SLO violations
- Document patterns in incident log

### Monthly Review
- Calculate SLO achievement percentage
- Adjust thresholds if consistently met or missed
- Update alerting policies as needed

### Quarterly Review
- Validate SLO targets against user needs
- Assess if stricter or looser targets are appropriate
- Update this document with new targets

---

## Error Budget

**Concept:** SLOs define acceptable failure rates. Error budget is the allowed downtime/errors before SLO is breached.

### Calculation
- **Latency Budget:** 5% of requests may exceed 10s P95 (averaged over 7 days)
- **Error Budget:** 5% of requests may fail (5xx) over 7 days
- **Uptime Budget:** 0.5% monthly downtime = ~3.6 hours/month

### Budget Policy
- **Budget healthy (>50% remaining):** Ship new features freely
- **Budget low (10-50% remaining):** Prioritize reliability improvements
- **Budget exhausted (<10% remaining):** Freeze feature work, focus on stability

---

## Incident Response

### SLO Violations
1. **Alert fires** → On-call engineer notified
2. **Triage** → Check dashboard for root cause (latency spike, error cluster, engine timeout)
3. **Mitigate** → Rollback if deployment-related, scale if load-related, escalate if engine-related
4. **Document** → Create incident report in `000-docs/incidents/`
5. **Review** → Post-mortem within 48 hours

### Rollback Procedure
```bash
# Manual rollback to previous revision
make rollback

# Or via gcloud
gcloud run services update-traffic bobs-brain-gateway \
  --region us-central1 \
  --to-revisions PREVIOUS_REVISION=100
```

---

## References

- **Guardrails Config:** `ops/guardrails.yaml`
- **Terraform Module:** `infra/terraform/modules/observability/`
- **Synthetic Probe:** `synthetics/probe_gateway.py`
- **CI/CD Pipeline:** `.github/workflows/deploy-gateway-bluegreen.yml`
- **Rollback Script:** `scripts/rollback_gateway.sh`

---

**Next Review:** 2025-11-18 (weekly)
**SLO Compliance:** See Cloud Monitoring dashboard for current status
