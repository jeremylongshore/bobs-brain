# A2A Framework: Technical Architecture Specification
**Detailed System Design**

**Date:** 2025-10-27
**Status:** Architecture Design
**Author:** Claude (intent solutions io)

---

## System Overview

The A2A (Agent-to-Agent) Framework is a **two-container microservices architecture** that separates intelligence from automation:

```
┌─────────────────────────────────────────────────────────┐
│                    CLIENT ENVIRONMENT                     │
│                                                           │
│  ┌────────────────────┐      ┌─────────────────────┐   │
│  │  Intelligence      │◄────►│  Automation         │   │
│  │  Agent Container   │ A2A  │  Agent Container    │   │
│  │                    │      │                     │   │
│  │  - FastAPI         │      │  - FastAPI          │   │
│  │  - PostgreSQL      │      │  - PostgreSQL       │   │
│  │  - LangChain       │      │  - n8n workflows    │   │
│  │  - scikit-learn    │      │  - API clients      │   │
│  └────────────────────┘      └─────────────────────┘   │
│           ▲                           ▲                  │
│           │                           │                  │
│           └───────────────┬───────────┘                  │
│                           │                              │
│                    Docker Network                        │
└───────────────────────────┼──────────────────────────────┘
                            │
                    ┌───────▼────────┐
                    │  External APIs  │
                    ├────────────────┤
                    │ - Apollo.io    │
                    │ - Sales Nav    │
                    │ - HubSpot      │
                    │ - Clearbit     │
                    └────────────────┘
```

---

## Container 1: Intelligence Agent

### Purpose
Analyzes third-party data, builds ICP models, scores leads, and provides strategic recommendations to the Automation Agent.

### Technology Stack

**Runtime:**
- Python 3.12 (official Docker image)
- FastAPI 0.104.0 (async web framework)
- Uvicorn (ASGI server)

**Data Storage:**
- PostgreSQL 15 (relational database)
- Pgvector extension (vector embeddings)

**ML/AI:**
- LangChain 0.1.0 (RAG framework)
- scikit-learn 1.3.0 (ML models)
- pandas 2.1.0 (data manipulation)
- numpy 1.26.0 (numerical computing)

**Integrations:**
- Apollo API client
- LinkedIn Sales Navigator API
- HubSpot API client
- Clearbit API client

### Database Schema

```sql
-- Historical closed deals (training data)
CREATE TABLE closed_deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    company_name VARCHAR(255),
    company_size_range VARCHAR(50),
    company_revenue_range VARCHAR(50),
    industry VARCHAR(100),
    tech_stack JSONB,
    funding_stage VARCHAR(50),
    decision_maker_title VARCHAR(100),
    deal_size_usd DECIMAL(12, 2),
    sales_cycle_days INTEGER,
    closed_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ICP model weights (learned patterns)
CREATE TABLE icp_models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    model_version INTEGER,
    weights JSONB, -- scoring weights
    patterns JSONB, -- learned patterns
    accuracy_score DECIMAL(5, 4),
    trained_on_deals_count INTEGER,
    last_trained_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Scored leads
CREATE TABLE scored_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    lead_id VARCHAR(255) UNIQUE,
    company_name VARCHAR(255),
    contact_name VARCHAR(255),
    contact_title VARCHAR(100),
    icp_score INTEGER, -- 0-100
    priority VARCHAR(10), -- A, B, C
    reasoning JSONB, -- why this score
    recommended_messaging JSONB,
    source VARCHAR(50), -- apollo, sales_nav, etc
    scored_at TIMESTAMP DEFAULT NOW()
);

-- Feedback from automation agent
CREATE TABLE automation_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id VARCHAR(255),
    action_taken VARCHAR(100),
    response_received BOOLEAN,
    response_time_hours INTEGER,
    outcome VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API Endpoints

**POST /api/v1/ingest-data**
```json
Request:
{
  "client_id": "uuid",
  "source": "apollo",
  "data": [
    {
      "company_name": "Acme Corp",
      "company_size": "50-200",
      "industry": "fintech",
      "tech_stack": ["salesforce", "aws", "react"],
      "funding_stage": "series_a"
    }
  ]
}

Response:
{
  "status": "success",
  "records_ingested": 1000,
  "processing_time_seconds": 12.5
}
```

**POST /api/v1/train-icp**
```json
Request:
{
  "client_id": "uuid",
  "lookback_months": 12
}

Response:
{
  "status": "success",
  "model_version": 3,
  "trained_on_deals": 45,
  "accuracy_score": 0.8723,
  "top_patterns": [
    {"pattern": "series_a_fintech", "conversion_rate": 0.42},
    {"pattern": "salesforce_user", "conversion_rate": 0.38}
  ]
}
```

**POST /api/v1/score-leads**
```json
Request:
{
  "client_id": "uuid",
  "leads": [
    {
      "lead_id": "abc123",
      "company_name": "Acme Corp",
      "contact_name": "Sarah Chen",
      "contact_title": "VP Sales",
      "company_data": {...}
    }
  ]
}

Response:
{
  "scored_leads": [
    {
      "lead_id": "abc123",
      "icp_score": 87,
      "priority": "A",
      "reasoning": {
        "why_good_fit": [
          "Series A fintech (perfect vertical match)",
          "Using Salesforce (integration works)",
          "Hired 5 SDRs in 30 days (scaling signal)"
        ],
        "expected_close_rate": 0.40,
        "expected_deal_size_usd": 50000,
        "expected_sales_cycle_days": 45
      },
      "recommended_messaging": {
        "hook": "Congrats on the new role",
        "pain_point": "Scaling sales team",
        "solution_fit": "LinkedIn agent for SDR onboarding"
      }
    }
  ]
}
```

**POST /api/v1/feedback**
```json
Request:
{
  "lead_id": "abc123",
  "action_taken": "linkedin_message_sent",
  "response_received": true,
  "response_time_hours": 4,
  "outcome": "meeting_booked",
  "notes": "Loved the fintech case study"
}

Response:
{
  "status": "success",
  "model_updated": true,
  "new_accuracy_score": 0.8756
}
```

### Docker Configuration

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src /app/src

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml (Intelligence Agent)
version: '3.8'

services:
  intelligence-agent:
    build: ./intelligence-agent
    container_name: intelligence-agent
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/intelligence
      - APOLLO_API_KEY=${APOLLO_API_KEY}
      - LINKEDIN_API_KEY=${LINKEDIN_API_KEY}
      - HUBSPOT_API_KEY=${HUBSPOT_API_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    networks:
      - a2a-network

  postgres:
    image: pgvector/pgvector:pg15
    container_name: intelligence-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=intelligence
    volumes:
      - intelligence-data:/var/lib/postgresql/data
    networks:
      - a2a-network

volumes:
  intelligence-data:

networks:
  a2a-network:
    driver: bridge
```

---

## Container 2: Automation Agent

### Purpose
Receives scored leads from Intelligence Agent, executes outreach campaigns, tracks responses, and sends feedback back to Intelligence Agent.

### Technology Stack

**Runtime:**
- Python 3.12 (official Docker image)
- FastAPI 0.104.0 (async web framework)
- Uvicorn (ASGI server)

**Workflow Orchestration:**
- n8n 1.0.0 (self-hosted workflow automation)

**Data Storage:**
- PostgreSQL 15 (campaign tracking)

**API Clients:**
- Apollo Python SDK
- LinkedIn API client
- HubSpot API client
- SendGrid (email fallback)

### Database Schema

```sql
-- Outreach campaigns
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID NOT NULL,
    campaign_name VARCHAR(255),
    status VARCHAR(50), -- active, paused, completed
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    total_leads INTEGER,
    messages_sent INTEGER DEFAULT 0,
    responses_received INTEGER DEFAULT 0,
    meetings_booked INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Campaign leads (received from Intelligence Agent)
CREATE TABLE campaign_leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id),
    lead_id VARCHAR(255) UNIQUE,
    company_name VARCHAR(255),
    contact_name VARCHAR(255),
    contact_linkedin_url VARCHAR(500),
    contact_email VARCHAR(255),
    icp_score INTEGER,
    priority VARCHAR(10),
    recommended_messaging JSONB,
    status VARCHAR(50), -- pending, sent, responded, meeting_booked
    sent_at TIMESTAMP,
    response_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Message logs
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id VARCHAR(255),
    channel VARCHAR(50), -- linkedin, email
    message_template VARCHAR(100),
    message_body TEXT,
    sent_at TIMESTAMP,
    response_received BOOLEAN DEFAULT FALSE,
    response_body TEXT,
    response_at TIMESTAMP
);
```

### API Endpoints

**POST /api/v1/execute-outreach**
```json
Request:
{
  "campaign_id": "uuid",
  "leads": [
    {
      "lead_id": "abc123",
      "contact_linkedin_url": "linkedin.com/in/sarah-chen",
      "recommended_messaging": {
        "hook": "Congrats on the new role",
        "body": "Saw you're scaling the sales team..."
      },
      "send_at": "2025-01-15T10:00:00Z"
    }
  ]
}

Response:
{
  "status": "success",
  "queued_messages": 100,
  "estimated_send_time": "2025-01-15T12:00:00Z"
}
```

**GET /api/v1/campaign-status/{campaign_id}**
```json
Response:
{
  "campaign_id": "uuid",
  "status": "active",
  "stats": {
    "total_leads": 500,
    "messages_sent": 450,
    "responses_received": 45,
    "response_rate": 0.10,
    "meetings_booked": 18,
    "booking_rate": 0.04
  }
}
```

**POST /api/v1/log-response**
```json
Request:
{
  "lead_id": "abc123",
  "response_body": "Thanks for reaching out! Let's chat next week.",
  "response_at": "2025-01-15T14:30:00Z"
}

Response:
{
  "status": "success",
  "feedback_sent_to_intelligence": true
}
```

### n8n Workflow Integration

**Workflow: LinkedIn Outreach**
```
Trigger: HTTP POST /execute-outreach
↓
For Each Lead:
  ├─ Check rate limits (50 per day)
  ├─ Personalize message template
  ├─ Send LinkedIn connection request
  ├─ Wait 24 hours
  ├─ Send LinkedIn message
  ├─ Log to database
  └─ Send feedback to Intelligence Agent
```

**Workflow: Response Monitor**
```
Trigger: Schedule (every 1 hour)
↓
For Each Campaign:
  ├─ Check LinkedIn for new responses
  ├─ Parse response sentiment
  ├─ If positive → Book meeting link
  ├─ If neutral → Follow up template
  ├─ If negative → Mark as closed-lost
  └─ Send feedback to Intelligence Agent
```

### Docker Configuration

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install n8n dependencies
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install n8n
RUN npm install -g n8n@1.0.0

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src /app/src

# Expose API and n8n ports
EXPOSE 8001 5678

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

# Start both services
CMD ["sh", "-c", "n8n start & uvicorn src.main:app --host 0.0.0.0 --port 8001"]
```

```yaml
# docker-compose.yml (Automation Agent)
version: '3.8'

services:
  automation-agent:
    build: ./automation-agent
    container_name: automation-agent
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/automation
      - INTELLIGENCE_AGENT_URL=http://intelligence-agent:8000
      - APOLLO_API_KEY=${APOLLO_API_KEY}
      - LINKEDIN_API_KEY=${LINKEDIN_API_KEY}
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
    ports:
      - "8001:8001"  # FastAPI
      - "5678:5678"  # n8n UI
    depends_on:
      - postgres
    networks:
      - a2a-network

  postgres:
    image: postgres:15
    container_name: automation-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=automation
    volumes:
      - automation-data:/var/lib/postgresql/data
    networks:
      - a2a-network

volumes:
  automation-data:

networks:
  a2a-network:
    external: true
```

---

## Agent-to-Agent Communication (A2A Protocol)

### Protocol: JSON-RPC 2.0 over HTTPS

**Why JSON-RPC:**
- Standard protocol (RFC 4627)
- Request/response pattern
- Error handling built-in
- Supported by Google's A2A initiative

### Message Format

**Intelligence → Automation: Send Scored Leads**
```json
{
  "jsonrpc": "2.0",
  "method": "automation.execute_outreach",
  "params": {
    "campaign_id": "uuid",
    "leads": [
      {
        "lead_id": "abc123",
        "icp_score": 87,
        "priority": "A",
        "contact_info": {...},
        "recommended_messaging": {...}
      }
    ]
  },
  "id": 1
}
```

**Automation → Intelligence: Send Feedback**
```json
{
  "jsonrpc": "2.0",
  "method": "intelligence.receive_feedback",
  "params": {
    "lead_id": "abc123",
    "action_taken": "linkedin_message_sent",
    "response_received": true,
    "outcome": "meeting_booked",
    "feedback": "Salesforce messaging resonated"
  },
  "id": 2
}
```

### Authentication

**Shared Secret (JWT)**
```python
import jwt

# Intelligence Agent generates token
token = jwt.encode(
    {
        "iss": "intelligence-agent",
        "aud": "automation-agent",
        "exp": datetime.utcnow() + timedelta(hours=1)
    },
    SHARED_SECRET,
    algorithm="HS256"
)

# Automation Agent validates token
payload = jwt.decode(token, SHARED_SECRET, algorithms=["HS256"])
```

### Error Handling

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32600,
    "message": "Invalid Request",
    "data": "Missing required field: lead_id"
  },
  "id": 1
}
```

**Error Codes:**
- `-32700`: Parse error
- `-32600`: Invalid request
- `-32601`: Method not found
- `-32602`: Invalid params
- `-32603`: Internal error

---

## Deployment Architecture

### Single-Client Deployment

```
┌─────────────────────────────────────────┐
│        Hetzner VPS (Ubuntu 22.04)       │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Docker Compose                 │   │
│  │                                 │   │
│  │  ┌──────────┐   ┌───────────┐  │   │
│  │  │ Intel.   │   │ Autom.    │  │   │
│  │  │ Agent    │◄─►│ Agent     │  │   │
│  │  └──────────┘   └───────────┘  │   │
│  │                                 │   │
│  │  ┌──────────┐   ┌───────────┐  │   │
│  │  │ Postgres │   │ Postgres  │  │   │
│  │  │ (Intel)  │   │ (Autom)   │  │   │
│  │  └──────────┘   └───────────┘  │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Nginx Reverse Proxy            │   │
│  │  - SSL termination              │   │
│  │  - Rate limiting                │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Specs:**
- Hetzner VPS: 4 vCPU, 16GB RAM, 160GB SSD
- Cost: ~$30/mo
- OS: Ubuntu 22.04 LTS
- Docker Engine 24.0+
- Docker Compose v2

### Multi-Client Deployment (Future)

```
┌──────────────────────────────────────────────┐
│        Google Cloud Run (Managed)            │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  Intelligence Agent (Shared)           │ │
│  │  - Multi-tenant PostgreSQL             │ │
│  │  - Separate schema per client          │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  ┌────────────────────────────────────────┐ │
│  │  Automation Agent (Per-Client)         │ │
│  │  - Isolated containers                 │ │
│  │  - Per-client API keys                 │ │
│  └────────────────────────────────────────┘ │
└──────────────────────────────────────────────┘
```

---

## Security Considerations

### 1. API Key Management
```python
# Store in environment variables, NOT code
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

# Rotate keys every 90 days
# Use Google Secret Manager in production
```

### 2. Data Encryption
```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

cipher = Fernet(ENCRYPTION_KEY)
encrypted_email = cipher.encrypt(email.encode())

# Decrypt when needed
decrypted_email = cipher.decrypt(encrypted_email).decode()
```

### 3. Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/score-leads")
@limiter.limit("100/minute")
async def score_leads(request: Request):
    ...
```

### 4. Input Validation
```python
from pydantic import BaseModel, Field

class Lead(BaseModel):
    lead_id: str = Field(..., min_length=1, max_length=255)
    company_name: str = Field(..., min_length=1, max_length=255)
    icp_score: int = Field(..., ge=0, le=100)
```

### 5. Audit Logging
```python
import logging

logging.info(
    "ICP model trained",
    extra={
        "client_id": client_id,
        "model_version": 3,
        "accuracy": 0.8723,
        "timestamp": datetime.utcnow()
    }
)
```

---

## Monitoring & Observability

### Metrics to Track

**Intelligence Agent:**
- ICP model accuracy over time
- Average scoring time per lead
- Feedback loop latency
- Database query performance

**Automation Agent:**
- Message send success rate
- Response rate by priority tier
- Meeting booking rate
- Campaign performance metrics

**System Health:**
- Container CPU/memory usage
- Database connection pool status
- API response times
- Error rates by endpoint

### Monitoring Stack

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter
    environment:
      - DATA_SOURCE_NAME=postgresql://user:pass@postgres:5432/intelligence?sslmode=disable
```

---

## Scalability Considerations

### Vertical Scaling
- Start: 4 vCPU, 16GB RAM
- Scale to: 8 vCPU, 32GB RAM
- Database read replicas for heavy queries

### Horizontal Scaling
- Multiple Automation Agents (one per client)
- Single Intelligence Agent (multi-tenant)
- Load balancer for API requests

### Caching Strategy
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_icp_model(client_id: str):
    # Cache ICP models for 1 hour
    return db.query(ICPModel).filter_by(client_id=client_id).first()
```

---

## Testing Strategy

### Unit Tests
```python
# test_intelligence_agent.py
def test_score_lead_a_tier():
    lead = create_test_lead(company_size="50-200", industry="fintech")
    score = intelligence_agent.score_lead(lead)
    assert score >= 80

def test_icp_model_training():
    deals = create_test_deals(count=50)
    model = intelligence_agent.train_icp(deals)
    assert model.accuracy_score > 0.75
```

### Integration Tests
```python
# test_a2a_communication.py
async def test_intelligence_to_automation():
    # Intelligence sends scored leads
    response = await intelligence_agent.send_scored_leads(leads)
    assert response.status == "success"

    # Automation receives and confirms
    received = await automation_agent.get_queued_leads()
    assert len(received) == len(leads)
```

### Load Tests
```python
# locustfile.py
from locust import HttpUser, task

class LoadTestUser(HttpUser):
    @task
    def score_leads(self):
        self.client.post("/api/v1/score-leads", json={
            "leads": generate_test_leads(count=100)
        })
```

---

## Conclusion

This architecture provides:
- ✅ **Separation of concerns** (intelligence vs automation)
- ✅ **Scalability** (containerized microservices)
- ✅ **Maintainability** (clear API contracts)
- ✅ **Observability** (comprehensive monitoring)
- ✅ **Security** (encryption, rate limiting, audit logs)

**Next Steps:**
1. Build Intelligence Agent MVP
2. Build Automation Agent MVP
3. Implement A2A communication layer
4. Deploy to Hetzner VPS for pilot testing

---

**Document Filing Reference:**
Category: AT (Architecture & Technical)
Type: ARCH (Architecture)
Last Updated: 2025-10-27
