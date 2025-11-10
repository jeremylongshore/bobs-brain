# 🏗️ System Architecture

> **Navigation**: [← Back to Docs Hub](./README.md) | [Next: Smart Router →](./SMART-ROUTER.md)

<details>
<summary><b>📋 TL;DR</b> - Click to expand</summary>

**System in 3 bullet points:**
- API Gateway receives requests and estimates complexity
- Smart Router sends simple tasks to local models (free), complex to cloud (paid)
- Result: 60-80% cost savings vs cloud-only

**Key Insight:** Most AI requests are simple - answer them locally!

</details>

---

## Table of Contents
- [High-Level Overview](#high-level-overview)
- [Request Flow](#request-flow)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Deployment Architecture](#deployment-architecture)
- [Technology Stack](#technology-stack)

## High-Level Overview

The Hybrid AI Stack is designed around one core principle: **route requests to the cheapest model that can handle them**.

```mermaid
graph TB
    subgraph "User Layer"
        A[Application/User]
    end
    
    subgraph "Gateway Layer"
        B[API Gateway :8080]
        C[Smart Router]
    end
    
    subgraph "Model Layer"
        D[TinyLlama<br/>Local CPU<br/>$0.00]
        E[Phi-2<br/>Local CPU<br/>$0.00]
        F[Claude Sonnet<br/>Cloud API<br/>$0.003-0.015]
    end
    
    subgraph "Monitoring Layer"
        G[Prometheus]
        H[Grafana]
        I[Taskwarrior]
    end
    
    A -->|HTTP POST| B
    B --> C
    C -->|Complexity < 0.3| D
    C -->|0.3 - 0.6| E
    C -->|> 0.6| F
    
    D -->|Response| A
    E -->|Response| A
    F -->|Response| A
    
    B -.->|Metrics| G
    G -.->|Dashboard| H
    C -.->|Tasks| I
    
    style D fill:#90EE90,stroke:#2d5016
    style E fill:#87CEEB,stroke:#1e3a5f
    style F fill:#FFB6C1,stroke:#8b0040
```

## Request Flow

### 1. Request Reception & Complexity Estimation

```mermaid
sequenceDiagram
    participant U as User
    participant G as API Gateway
    participant R as Smart Router
    participant TL as TinyLlama
    participant P2 as Phi-2
    participant C as Claude
    
    U->>G: POST /api/v1/chat
    Note over G: {"prompt": "..."}
    
    G->>R: Estimate Complexity
    
    Note over R: Analyze:<br/>- Length<br/>- Keywords<br/>- Code presence<br/>- Task type
    
    R->>R: Calculate Score (0-1)
    
    alt Complexity < 0.3 (Simple)
        R->>TL: Execute Request
        TL->>R: Response (Cost: $0)
        R->>G: Return Result
    else Complexity 0.3-0.6 (Medium)
        R->>P2: Execute Request
        P2->>R: Response (Cost: $0)
        R->>G: Return Result
    else Complexity > 0.6 (Complex)
        R->>C: Execute Request
        C->>R: Response (Cost: $0.003-0.015)
        R->>G: Return Result
    end
    
    G->>U: JSON Response
    Note over G: Includes:<br/>- Model used<br/>- Cost<br/>- Latency<br/>- Routing reason
```

### 2. Complexity Estimation Algorithm

The Smart Router evaluates multiple factors:

```mermaid
graph LR
    A[Incoming Prompt] --> B{Analyze Factors}
    
    B --> C[Length<br/>0-0.5 points]
    B --> D[Keywords<br/>-0.1 to 0.3 points]
    B --> E[Code Detection<br/>0-0.3 points]
    B --> F[Task Type<br/>-0.1 to 0.2 points]
    
    C --> G[Sum Scores]
    D --> G
    E --> G
    F --> G
    
    G --> H[Normalize 0-1]
    H --> I{Select Model}
    
    I -->|< 0.3| J[TinyLlama]
    I -->|0.3-0.6| K[Phi-2]
    I -->|> 0.6| L[Claude]
    
    style J fill:#90EE90
    style K fill:#87CEEB
    style L fill:#FFB6C1
```

**Scoring Factors:**

| Factor | Weight | Examples |
|--------|--------|----------|
| **Length** | 0-0.5 | <100 chars = 0.1, 100-500 = 0.3, >500 = 0.5 |
| **Complex Keywords** | 0-0.3 | "analyze", "design", "implement", "refactor" |
| **Simple Keywords** | -0.1 | "what is", "list", "summarize" |
| **Code Presence** | 0-0.3 | Code blocks, function definitions |
| **Task Type** | -0.1 to 0.2 | Questions = -0.1, Creative = 0.2 |

## Component Architecture

```mermaid
graph TB
    subgraph "Docker Stack"
        subgraph "Core Services"
            AG[API Gateway<br/>Flask + Gunicorn<br/>Port 8080]
            OL[Ollama<br/>Local LLM Server<br/>Port 11434]
            SR[Smart Router<br/>Python Module]
        end
        
        subgraph "Automation"
            N8[n8n<br/>Workflow Engine<br/>Port 5678]
            PG[PostgreSQL<br/>n8n Database]
        end
        
        subgraph "Monitoring"
            PM[Prometheus<br/>Metrics<br/>Port 9090]
            GF[Grafana<br/>Dashboards<br/>Port 3000]
        end
        
        subgraph "Data"
            RD[Redis<br/>Caching<br/>Port 6379]
            QD[Qdrant<br/>Vector DB<br/>Port 6333]
        end
    end
    
    AG --> SR
    SR --> OL
    AG --> RD
    N8 --> AG
    N8 --> PG
    AG --> PM
    PM --> GF
    
    style AG fill:#4A90E2
    style SR fill:#E27D60
    style OL fill:#85D8CE
```

### Component Responsibilities

#### API Gateway (`gateway/app.py`)
- **Purpose**: Main HTTP entry point
- **Responsibilities**:
  - Accept HTTP requests
  - Call Smart Router
  - Return JSON responses
  - Export Prometheus metrics
  - Health checks
- **Technology**: Flask, Gunicorn
- **Endpoints**:
  - `POST /api/v1/chat` - Main chat endpoint
  - `POST /api/v1/complexity` - Complexity estimation only
  - `GET /api/v1/stats` - Routing statistics
  - `GET /health` - Health check
  - `GET /metrics` - Prometheus metrics

#### Smart Router (`scripts/smart_router.py`)
- **Purpose**: Intelligent request routing
- **Responsibilities**:
  - Estimate prompt complexity
  - Select optimal model
  - Execute requests
  - Track costs
  - Log to Taskwarrior
- **Logic**:
  ```python
  def select_model(complexity):
      if complexity < 0.3:
          return 'tinyllama'  # Free, fast
      elif complexity < 0.6:
          return 'phi2'       # Free, good quality
      else:
          return 'claude-sonnet'  # Paid, best quality
  ```

#### Ollama Server
- **Purpose**: Local model inference
- **Models**: TinyLlama (1.1B), Phi-2 (2.7B), Mistral-7B (optional)
- **API**: HTTP REST at `localhost:11434`
- **Resource Usage**:
  - TinyLlama: ~700MB RAM
  - Phi-2: ~1.6GB RAM
  - Mistral-7B: ~4GB RAM

#### n8n Workflows
- **Purpose**: Automation and orchestration
- **Workflows**:
  1. Smart Routing Workflow
  2. Cost Monitoring
  3. Performance Tracking
  4. Orchestrator Pipeline

#### Monitoring Stack
- **Prometheus**: Scrapes metrics from API Gateway
- **Grafana**: Visualizes metrics and costs
- **Metrics Tracked**:
  - `api_gateway_requests_total{model, backend, status}`
  - `api_gateway_request_duration_seconds{model, backend}`
  - `api_gateway_cost_total{model}`

## Data Flow

### Request Processing

```mermaid
flowchart TD
    Start([User Request]) --> Receive[API Gateway Receives]
    Receive --> Log1[Log to Prometheus]
    
    Receive --> Estimate[Smart Router:<br/>Estimate Complexity]
    Estimate --> Decision{Complexity?}
    
    Decision -->|< 0.3| Local1[Execute on TinyLlama]
    Decision -->|0.3-0.6| Local2[Execute on Phi-2]
    Decision -->|> 0.6| Cloud[Execute on Claude]
    
    Local1 --> Cost1[Cost: $0.00]
    Local2 --> Cost2[Cost: $0.00]
    Cloud --> Cost3[Cost: $0.003-0.015]
    
    Cost1 --> Track[Track in Taskwarrior]
    Cost2 --> Track
    Cost3 --> Track
    
    Track --> Metrics[Update Prometheus]
    Metrics --> Response[Return JSON Response]
    Response --> End([User Receives Result])
    
    style Local1 fill:#90EE90
    style Local2 fill:#87CEEB
    style Cloud fill:#FFB6C1
    style Cost1 fill:#90EE90
    style Cost2 fill:#90EE90
    style Cost3 fill:#FFB6C1
```

### Cost Tracking Flow

```mermaid
sequenceDiagram
    participant SR as Smart Router
    participant TW as Taskwarrior
    participant PM as Prometheus
    participant GF as Grafana
    
    SR->>SR: Execute Request
    SR->>SR: Calculate Actual Cost
    
    SR->>TW: Create Task
    Note over TW: project:vps_ai.router<br/>+routing<br/>cost: $X
    
    SR->>PM: Increment Metric
    Note over PM: api_gateway_cost_total<br/>{model="claude"}
    
    PM->>GF: Query Metrics
    GF->>GF: Generate Dashboard
    Note over GF: Total Costs<br/>Cost by Model<br/>Savings vs Cloud-Only
```

## Deployment Architecture

### Docker Deployment

```mermaid
graph TB
    subgraph "Host Machine"
        subgraph "Docker Network: demo"
            AG[api-gateway:8080]
            N8[n8n:5678]
            OL[ollama-cpu:11434]
            PM[prometheus:9090]
            GF[grafana:3000]
            RD[redis:6379]
            PG[postgres:5432]
        end
        
        VOL1[(Volume:<br/>n8n_storage)]
        VOL2[(Volume:<br/>ollama_storage)]
        VOL3[(Volume:<br/>prometheus_data)]
    end
    
    AG --> OL
    AG --> RD
    N8 --> PG
    N8 --> VOL1
    OL --> VOL2
    PM --> VOL3
    PM --> GF
    
    USER([User]) -->|Port 8080| AG
    USER -->|Port 5678| N8
    USER -->|Port 3000| GF
```

### Cloud Deployment (AWS/GCP)

```mermaid
graph TB
    subgraph "Cloud Provider"
        subgraph "VPC"
            subgraph "Security Group"
                EC2[EC2/Compute Instance<br/>Ubuntu 22.04]
            end
            
            subgraph "Instance"
                DOCKER[Docker Stack<br/>Same as Local]
            end
        end
        
        EIP[Elastic IP/Static IP]
        SG[Security Group Rules]
    end
    
    INTERNET([Internet]) --> EIP
    EIP --> SG
    SG -->|Allow 22,5678,8080,3000,9090| EC2
    EC2 --> DOCKER
    
    SG -.->|SSH| EC2
    SG -.->|n8n| EC2
    SG -.->|API| EC2
    SG -.->|Grafana| EC2
```

## Technology Stack

### Backend
- **Python 3.11+**: Core language
- **Flask 3.1**: Web framework
- **Gunicorn**: WSGI server
- **Anthropic SDK**: Claude API client
- **Requests**: HTTP client

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **Ollama**: Local LLM server
- **Redis**: Caching layer
- **PostgreSQL**: n8n database

### Monitoring
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Taskwarrior**: Task tracking

### Automation
- **n8n**: Workflow engine
- **Terraform**: Infrastructure as Code
- **Ansible**: Configuration management

### Models
- **TinyLlama 1.1B**: Ultra-lightweight (700MB)
- **Phi-2 2.7B**: Quality lightweight (1.6GB)
- **Mistral 7B**: High-quality (4GB, optional)
- **Claude Sonnet 4**: Cloud (via API)

## Design Principles

### 1. Cost Optimization First
Every decision prioritizes reducing API costs:
- Local models for simple tasks
- Smart complexity estimation
- Automatic routing
- Cost tracking built-in

### 2. Production-Grade Reliability
- Proper error handling
- Health checks
- Graceful degradation
- Comprehensive logging

### 3. Observable by Default
- Prometheus metrics
- Grafana dashboards
- Taskwarrior integration
- Request tracing

### 4. Easy to Deploy
- One-command installation
- Docker-based deployment
- Infrastructure as Code
- Minimal configuration

### 5. Extensible Architecture
- Modular components
- Clear interfaces
- Easy to add new models
- Workflow automation ready

## Performance Characteristics

### Latency

| Model | Typical Latency | Use Case |
|-------|----------------|----------|
| **TinyLlama** | 0.5-2s | Simple Q&A, classifications |
| **Phi-2** | 1-3s | Explanations, summaries |
| **Claude Sonnet** | 2-5s | Code gen, complex analysis |

### Throughput

| Component | Max RPS | Bottleneck |
|-----------|---------|------------|
| **API Gateway** | 100+ | CPU-bound |
| **Ollama (CPU)** | 10-20 | Model inference |
| **Claude API** | 50+ | Rate limits |

### Resource Usage (Tier 2)

| Service | RAM | CPU | Disk |
|---------|-----|-----|------|
| **Ollama** | ~2GB | 1-2 cores | 5GB models |
| **API Gateway** | ~200MB | 0.5 cores | Minimal |
| **n8n** | ~300MB | 0.25 cores | 1GB |
| **Monitoring** | ~500MB | 0.25 cores | 2GB |
| **Total** | ~3GB | ~2 cores | ~8GB |

---

**Related Documentation:**
- [Smart Router Details](./SMART-ROUTER.md)
- [VPS Tier Selection](./VPS-TIERS.md)
- [Deployment Guide](./DEPLOYMENT.md)
- [Cost Optimization](./COST-OPTIMIZATION.md)

[⬆ Back to Top](#️-system-architecture)
