# IAM1 Regional Manager - Deployment Guide

## Product: IntentSolutions IAM1
**Version:** 2.0.0
**Tier:** Regional Manager Agent
**Business Model:** Deployable per client/department

---

## Business Model Overview

### IAM1 = Regional Manager / Joint Venture Partner
- **Sovereign** within their domain (department/client)
- **Grounded** in client-specific knowledge (Vertex AI Search RAG)
- **Can coordinate** with peer IAM1s (other regional managers)
- **Can command** IAM2 specialists (team members)
- **Cannot command** peer IAM1s (equals, not subordinates)

### Revenue Streams

1. **IAM1 Basic** - $X/month per deployment
   - Conversational AI
   - RAG knowledge grounding
   - Slack integration

2. **IAM1 + IAM2 Team** - $Y/month
   - IAM1 Basic +
   - IAM2 specialists (Research, Code, Data)
   - Task delegation

3. **Multi-IAM1 Enterprise** - $Z/month
   - Multiple IAM1 deployments
   - A2A coordination between IAM1s
   - Each IAM1 can have IAM2 teams

---

## Deployment Scenarios

### Scenario 1: Single Client, Single Department
**Example:** Deploy IAM1 to Acme Corp Sales Department

```bash
# 1. Create GCP project for client
gcloud projects create acme-sales-iam1

# 2. Set up infrastructure
cd bob-vertex-agent
export CLIENT_NAME="acme"
export DOMAIN="sales"
export PROJECT_ID="acme-sales-iam1"

# 3. Deploy Terraform (creates Vertex AI Search, BigQuery, etc.)
make setup-dev-env

# 4. Upload client's knowledge base to Cloud Storage
gsutil -m rsync -r /path/to/acme/sales/docs gs://acme-sales-iam1-bob-vertex-agent-rag/knowledge-base/

# 5. Run data ingestion
make data-ingestion

# 6. Deploy IAM1
make deploy

# 7. Configure Slack for Acme Corp
# Update Slack app with IAM1's webhook URL
```

**Result:** Acme Sales team has their own IAM1 grounded in sales knowledge

---

### Scenario 2: Single Client, Multiple Departments
**Example:** Acme Corp wants IAM1 for Sales, Engineering, and Support

Deploy 3 separate IAM1 instances:

```bash
# IAM1 for Sales
gcloud projects create acme-sales-iam1
# ... deploy as above

# IAM1 for Engineering
gcloud projects create acme-engineering-iam1
# ... deploy with engineering knowledge

# IAM1 for Support
gcloud projects create acme-support-iam1
# ... deploy with support knowledge
```

**A2A Configuration:**
These 3 IAM1s can **coordinate** (share info) but cannot **command** each other.

```python
# In agent.py, enable A2A discovery
iam1_peers = [
    "acme-sales-iam1",
    "acme-engineering-iam1",
    "acme-support-iam1"
]
```

**Result:**
- 3 revenue streams (3 x IAM1 subscription)
- IAM1-Sales can ask IAM1-Engineering questions
- Each IAM1 is sovereign in their domain

---

### Scenario 3: IAM1 + IAM2 Team
**Example:** Acme Sales wants specialists

```bash
# 1. Deploy IAM1 (already done above)

# 2. Deploy IAM2 specialists
# - Research IAM2 (market research specialist)
# - Data IAM2 (sales analytics specialist)
# - Slack IAM2 (customer communication specialist)

# 3. Configure IAM1 to route tasks to IAM2s
# (Already configured in sub_agents.py)
```

**Hierarchy:**
```
IAM1 (Acme Sales Regional Manager)
├── IAM2-Research (Market research)
├── IAM2-Data (Sales analytics)
└── IAM2-Slack (Customer communication)
```

**Result:**
- IAM1 subscription + 3 x IAM2 add-ons
- IAM1 routes specialized tasks to IAM2s
- IAM2s report only to their IAM1

---

## Quick Deployment Checklist

### For Each New IAM1 Deployment:

- [ ] Create GCP project: `{client}-{domain}-iam1`
- [ ] Enable billing
- [ ] Deploy Terraform infrastructure
- [ ] Upload client knowledge base to Cloud Storage
- [ ] Run data ingestion pipeline
- [ ] Deploy IAM1 via `make deploy`
- [ ] Configure client's Slack workspace
- [ ] Test basic chat functionality
- [ ] Test knowledge retrieval (RAG)
- [ ] (Optional) Deploy IAM2 specialists
- [ ] (Optional) Configure A2A with peer IAM1s

---

## Agent-to-Agent (A2A) Framework

### IAM1-to-IAM1 Communication (Peers)
**Use Case:** Sales IAM1 needs info from Engineering IAM1

```python
# IAM1-Sales can ASK IAM1-Engineering
response = iam1_engineering.query("What's the status of Feature X?")

# IAM1-Sales CANNOT COMMAND IAM1-Engineering
# ❌ iam1_engineering.execute_task("Build Feature Y")  # Not allowed
```

### IAM1-to-IAM2 Communication (Manager → Team)
**Use Case:** Sales IAM1 delegates task to Data IAM2

```python
# IAM1-Sales CAN COMMAND IAM2-Data
response = iam2_data.execute_task("Generate Q4 sales report")

# IAM2-Data reports back to IAM1-Sales
```

---

## Pricing Examples

### Example 1: Small Business
**Client:** Local retail store
**Deployment:** 1 x IAM1 Basic
**Monthly Cost:** $500/month
**Includes:** Chat AI + knowledge grounding + Slack

### Example 2: Growing Company
**Client:** SaaS startup
**Deployment:** 1 x IAM1 + 2 x IAM2 specialists
**Monthly Cost:** $500 (IAM1) + $200/IAM2 (x2) = $900/month
**Includes:** Regional manager + Research + Code specialists

### Example 3: Enterprise
**Client:** Multi-national corporation
**Deployment:** 5 x IAM1 (Sales, Eng, Support, HR, Finance) + 10 x IAM2 across teams
**Monthly Cost:** $500/IAM1 (x5) + $200/IAM2 (x10) = $4,500/month
**Includes:** Full multi-regional AI workforce

---

## Marketing Positioning

### IAM1 Value Proposition

**For Small Business:**
"Get your own AI regional manager grounded in YOUR business knowledge. Talks to your team via Slack. No sharing with other companies."

**For Growing Business:**
"Start with one AI regional manager. Add specialist team members (IAM2s) as you grow. Scale horizontally with more managers or vertically with more specialists."

**For Enterprise:**
"Deploy AI regional managers across departments. They coordinate with each other but remain sovereign in their domains. Your Sales AI doesn't command your Engineering AI - they collaborate as peers."

---

## Technical Specifications

### Per IAM1 Deployment:
- **Model:** Gemini 2.0 Flash (orchestrator)
- **Grounding:** Vertex AI Search (client-specific)
- **Storage:** Cloud Storage bucket (client-isolated)
- **Analytics:** BigQuery (client-isolated)
- **Communication:** Slack integration
- **Telemetry:** Full observability
- **A2A:** Agent-to-Agent framework

### Isolation Guarantee:
- Each client's IAM1 has separate GCP project
- Knowledge bases are NEVER shared between clients
- IAM2s only report to their deployed IAM1
- Full data isolation and privacy

---

## Support & SLA

- **Uptime SLA:** 99.9%
- **Response Time:** < 3 seconds
- **Knowledge Update:** Daily automated ingestion
- **Support:** Business hours (IAM1 Basic), 24/7 (Enterprise)

---

## Contact

**IntentSolutions**
Website: https://intentsolutions.io
Email: contact@intentsolutions.io
