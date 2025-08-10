# Base Agent Framework Implementation Plan
**Complete Technical Blueprint for Modular AI Agent System**
**Created:** 2025-08-10
**Status:** Ready for Review

## 📋 EXECUTIVE SUMMARY

We will build a **modular base agent framework** that serves as a template for all future agents. This framework combines:
- **Graphiti** for intelligent memory (knowledge graphs)
- **Google Cloud Platform** services (Model Garden, Firestore, Cloud Run)
- **Open-source tools** (LangChain, Playwright)
- **Existing Bob code** as foundation

The first specialization will be a **Research Agent** capable of web scraping, data analysis, and intelligent conversation.

---

## 🏗️ COMPLETE SYSTEM ARCHITECTURE

```
┌──────────────────────────────────────────────────────────┐
│                    USER INTERFACES                        │
│  startaitools.com (HQ) | diagnosticpro.io (Customers)    │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│                  BASE AGENT FRAMEWORK                     │
│         agent_framework/base_agent/__init__.py           │
├───────────────────────────────────────────────────────────┤
│  Core Components:                                         │
│  • Memory Manager (Graphiti + Firestore)                  │
│  • Model Router (200+ Model Garden models)                │
│  • Tool Registry (Web scraping, PDF, APIs)                │
│  • Interface Layer (Chat, API, Webhooks)                  │
└────────┬──────────────────────────────────────────────────┘
         │
┌────────▼─────────────────────────────────────────────────┐
│               SPECIALIZED AGENTS                          │
│  Research Agent | Bob | Future Agents                     │
└───────────────────────────────────────────────────────────┘
```

---

## 📦 WHAT WE'LL BUILD (STEP BY STEP)

### Phase 1: Base Framework Core (Week 1)

#### 1.1 Project Structure
```
bobs-brain/
├── agent_framework/
│   ├── base_agent/
│   │   ├── __init__.py
│   │   ├── memory/
│   │   │   ├── graphiti_manager.py    # Knowledge graph operations
│   │   │   ├── firestore_manager.py   # Document storage
│   │   │   └── vector_manager.py      # Embeddings & search
│   │   ├── models/
│   │   │   ├── router.py              # Intelligent model selection
│   │   │   ├── model_configs.yaml     # Model parameters
│   │   │   └── providers/
│   │   │       ├── gemini.py          # Gemini models
│   │   │       ├── claude.py          # Claude via Model Garden
│   │   │       └── specialized.py     # Codey, Imagen, etc.
│   │   ├── tools/
│   │   │   ├── web_scraper.py         # Playwright scraping
│   │   │   ├── pdf_processor.py       # Document AI
│   │   │   ├── data_analyzer.py       # Analysis tools
│   │   │   └── api_connector.py       # External APIs
│   │   ├── interfaces/
│   │   │   ├── chat_interface.py      # Streamlit UI
│   │   │   ├── api_server.py          # FastAPI endpoints
│   │   │   └── webhook_handler.py     # Event processing
│   │   └── core/
│   │       ├── agent_base.py          # Base agent class
│   │       ├── conversation.py        # Dialog management
│   │       └── context_manager.py     # Context tracking
│   ├── agents/
│   │   ├── research_agent/
│   │   │   ├── __init__.py
│   │   │   ├── research_tools.py      # Specialized research tools
│   │   │   ├── data_pipeline.py       # Data processing
│   │   │   └── knowledge_builder.py   # Knowledge construction
│   │   └── bob_agent/
│   │       └── __init__.py            # Existing Bob integration
│   ├── shared/
│   │   ├── config.py                  # Global configuration
│   │   ├── utils.py                   # Shared utilities
│   │   └── constants.py               # System constants
│   ├── requirements.txt
│   ├── setup.py
│   └── tests/
│       ├── test_memory.py
│       ├── test_models.py
│       └── test_agents.py
├── deployments/
│   ├── cloud_run/
│   │   ├── Dockerfile
│   │   └── deploy.sh
│   └── docker-compose.yml              # Local development
├── configs/
│   ├── gcp_services.yaml              # GCP configuration
│   ├── model_garden.yaml              # Model configurations
│   └── agent_configs.yaml             # Agent-specific configs
└── docs/
    ├── API.md
    ├── DEPLOYMENT.md
    └── DEVELOPMENT.md
```

#### 1.2 Core Components Implementation

**Memory Manager (Graphiti + Firestore Hybrid)**
```python
# agent_framework/base_agent/memory/graphiti_manager.py
from graphiti import Graphiti
from neo4j import GraphDatabase
import firebase_admin
from google.cloud import firestore

class HybridMemory:
    def __init__(self):
        # Graphiti for relationships and temporal reasoning
        self.graphiti = Graphiti(
            neo4j_uri=os.getenv("NEO4J_URI"),
            neo4j_user=os.getenv("NEO4J_USER"),
            neo4j_password=os.getenv("NEO4J_PASSWORD")
        )
        
        # Firestore for document storage
        self.firestore = firestore.Client(
            project='diagnostic-pro-mvp',
            database='agent-knowledge'
        )
        
        # Vector search for semantic retrieval
        self.vector_index = self._init_vector_search()
    
    def store_knowledge(self, content, metadata):
        # Store in Graphiti for relationships
        entities = self.graphiti.extract_entities(content)
        self.graphiti.add_entities(entities)
        
        # Store in Firestore for persistence
        doc_ref = self.firestore.collection('knowledge').add({
            'content': content,
            'metadata': metadata,
            'timestamp': datetime.now()
        })
        
        # Generate embeddings for search
        embedding = self.generate_embedding(content)
        self.vector_index.add(embedding, doc_ref.id)
        
        return doc_ref.id
```

**Model Router (Intelligent Model Selection)**
```python
# agent_framework/base_agent/models/router.py
from vertexai import ModelGarden
import yaml

class ModelRouter:
    def __init__(self):
        self.model_configs = self._load_configs()
        self.usage_tracker = {}
        
    def select_model(self, task_type, context_size, priority='balanced'):
        """
        Intelligently route to the best model based on:
        - Task type (chat, research, code, vision)
        - Context size requirements
        - Cost/performance priority
        """
        if task_type == 'conversation':
            if context_size < 32000:
                return self.get_model('gemini-2.0-flash')
            else:
                return self.get_model('gemini-1.5-pro')
                
        elif task_type == 'research':
            if priority == 'quality':
                return self.get_model('gemini-1.5-pro')
            else:
                return self.get_model('gemini-2.0-flash')
                
        elif task_type == 'code':
            return self.get_model('codey')
            
        elif task_type == 'vision':
            return self.get_model('imagen')
            
        elif task_type == 'complex_reasoning':
            return self.get_model('claude-3-opus')
            
        else:
            return self.get_model('gemini-2.0-flash')  # Default
```

---

### Phase 2: Research Agent Specialization (Week 2)

#### 2.1 Research Agent Components

**Web Scraping System**
```python
# agent_framework/agents/research_agent/research_tools.py
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import asyncio

class ResearchScraper:
    def __init__(self):
        self.rate_limiter = RateLimiter(requests_per_second=1)
        self.user_agent = "ResearchAgent/1.0 (Compatible; For research purposes)"
        
    async def scrape_public_data(self, urls):
        """
        Scrape public forums, documentation, PDFs
        - Respects robots.txt
        - Rate limiting
        - Grey area exploration with ethics
        """
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            
            for url in urls:
                if self._check_robots_txt(url):
                    page = await browser.new_page()
                    await page.goto(url)
                    content = await page.content()
                    
                    # Parse with BeautifulSoup
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Extract meaningful data
                    data = self._extract_data(soup)
                    results.append(data)
                    
                    await self.rate_limiter.wait()
                    
        return results
```

**Knowledge Building Pipeline**
```python
# agent_framework/agents/research_agent/knowledge_builder.py
class KnowledgeBuilder:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.quality_scorer = QualityScorer()
        
    def process_research_data(self, raw_data):
        """
        Transform raw scraped data into structured knowledge
        """
        # Quality filtering
        high_quality = [d for d in raw_data 
                       if self.quality_scorer.score(d) > 0.7]
        
        # Entity extraction
        entities = self.extract_entities(high_quality)
        
        # Relationship mapping
        relationships = self.map_relationships(entities)
        
        # Temporal tracking
        temporal_facts = self.extract_temporal_facts(high_quality)
        
        # Store in hybrid memory
        for fact in temporal_facts:
            self.memory.store_knowledge(
                content=fact['content'],
                metadata={
                    'source': fact['source'],
                    'confidence': fact['confidence'],
                    'timestamp': fact['timestamp']
                }
            )
        
        return {
            'entities': entities,
            'relationships': relationships,
            'facts': temporal_facts
        }
```

---

### Phase 3: Integration & Deployment (Week 3)

#### 3.1 Cloud Run Deployment

**Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY agent_framework/ ./agent_framework/
COPY configs/ ./configs/

# Environment variables
ENV PORT=8080
ENV GCP_PROJECT=diagnostic-pro-mvp

# Start the application
CMD ["python", "-m", "agent_framework.base_agent.interfaces.api_server"]
```

**API Server**
```python
# agent_framework/base_agent/interfaces/api_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Agent Framework API")

class QueryRequest(BaseModel):
    agent_type: str
    query: str
    context: dict = {}

@app.post("/query")
async def query_agent(request: QueryRequest):
    """
    Route queries to appropriate agent
    """
    agent = AgentRegistry.get_agent(request.agent_type)
    if not agent:
        raise HTTPException(404, f"Agent {request.agent_type} not found")
    
    response = await agent.process_query(
        query=request.query,
        context=request.context
    )
    
    return {
        "agent": request.agent_type,
        "response": response,
        "metadata": agent.get_metadata()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": AgentRegistry.list_agents()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
```

---

## 🔄 IMPLEMENTATION WORKFLOW

### Week 1: Foundation
| Day | Task | Deliverable |
|-----|------|------------|
| 1 | Set up project structure | Complete directory tree |
| 2 | Implement Graphiti memory manager | Working knowledge graph |
| 3 | Build Model Router | Multi-model selection |
| 4 | Create base agent class | Reusable template |
| 5 | Integrate with existing Bob | Migration complete |

### Week 2: Research Agent
| Day | Task | Deliverable |
|-----|------|------------|
| 1 | Build web scraper | Public data collection |
| 2 | Implement PDF processor | Document AI integration |
| 3 | Create knowledge builder | Data structuring |
| 4 | Add quality scoring | Content filtering |
| 5 | Test research pipeline | End-to-end working |

### Week 3: Deployment
| Day | Task | Deliverable |
|-----|------|------------|
| 1 | Set up Cloud Run | Container deployed |
| 2 | Create API endpoints | REST API working |
| 3 | Build UI (Streamlit) | Chat interface |
| 4 | Connect to startaitools.com | HQ portal live |
| 5 | Final testing & optimization | Production ready |

---

## 🔧 TECHNICAL IMPLEMENTATION DETAILS

### Dependencies (requirements.txt)
```
# Core
google-cloud-aiplatform==1.71.1
google-cloud-firestore==2.11.1
google-cloud-documentai==2.20.0

# Memory
graphiti==0.3.0
neo4j==5.14.0

# Framework
langchain==0.1.0
langchain-google-vertexai==0.0.3

# Web Scraping
playwright==1.40.0
beautifulsoup4==4.12.2
scrapy==2.11.0

# API & UI
fastapi==0.104.1
uvicorn==0.24.0
streamlit==1.28.2

# Utils
pydantic==2.5.0
python-dotenv==1.0.0
pandas==2.1.3
numpy==1.26.2
```

### Environment Variables (.env)
```bash
# GCP
GCP_PROJECT=diagnostic-pro-mvp
GCP_REGION=us-central1

# Graphiti/Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Model Garden
VERTEX_AI_LOCATION=us-central1
MODEL_GARDEN_ENDPOINT=your-endpoint

# Firestore
FIRESTORE_DATABASE=agent-knowledge

# Slack (for Bob integration)
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
```

---

## 💡 KEY DESIGN DECISIONS

### Why This Architecture?

1. **Modular Design**: Each agent inherits from base_agent but can override any component
2. **Hybrid Memory**: Graphiti for intelligence, Firestore for persistence, Vector for search
3. **Model Router**: Optimize cost by using appropriate models for each task
4. **Open Source First**: Use free tools where possible, GCP only where necessary
5. **Reuse Existing Code**: Leverage Bob's working components

### Critical Success Factors

1. **Memory System**: Graphiti must successfully extract and relate entities
2. **Model Routing**: Must reduce costs by 80% vs using only premium models
3. **Scraping Ethics**: Stay in grey area without crossing legal lines
4. **Performance**: <200ms response time for queries
5. **Scalability**: Handle 1000+ concurrent users without degradation

---

## 🚀 IMMEDIATE NEXT STEPS

### Before Starting Implementation:

1. **Verify GCP Access**
   ```bash
   gcloud auth list
   gcloud config get-value project
   gcloud services list --enabled
   ```

2. **Set Up Neo4j for Graphiti**
   ```bash
   docker run -d \
     --name neo4j \
     -p 7474:7474 -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/password \
     neo4j:latest
   ```

3. **Clone and Set Up Repository**
   ```bash
   cd ~/bobs-brain
   mkdir -p agent_framework
   pip install graphiti langchain google-cloud-aiplatform
   ```

4. **Test Model Garden Access**
   ```python
   from google.cloud import aiplatform
   aiplatform.init(project='diagnostic-pro-mvp')
   models = aiplatform.Model.list()
   print(f"Available models: {len(models)}")
   ```

---

## ✅ VALIDATION CRITERIA

### Phase 1 Complete When:
- [ ] Base agent class can be instantiated
- [ ] Memory system stores and retrieves facts
- [ ] Model router selects appropriate models
- [ ] Basic chat interface works

### Phase 2 Complete When:
- [ ] Research agent scrapes 10 public sites
- [ ] Processes 5 PDFs successfully
- [ ] Builds knowledge graph with 100+ entities
- [ ] Engages in intelligent conversation about findings

### Phase 3 Complete When:
- [ ] Deployed to Cloud Run
- [ ] Accessible via startaitools.com
- [ ] API endpoints respond < 200ms
- [ ] Handles 10 concurrent users

---

## 📊 COST ANALYSIS

### Monthly Operating Costs
| Service | Usage | Cost |
|---------|-------|------|
| Gemini 2.0 Flash | 10M tokens | $0.75 |
| Gemini 1.5 Pro | 1M tokens | $1.25 |
| Cloud Run | 100 hours | $20 |
| Firestore | 10GB | $10 |
| Neo4j (Container) | Always on | $30 |
| **Total** | - | **$62/month** |

### With Your $1000 Credits
- **16 months of operation** at current estimates
- Plenty of runway for development and scaling

---

## 🎯 SUCCESS METRICS

### Technical Metrics
- Response time: < 200ms (p95)
- Uptime: 99.9%
- Memory retrieval accuracy: > 90%
- Cost per query: < $0.001

### Business Metrics
- Research quality score: > 8/10
- User satisfaction: > 4.5/5
- Knowledge base growth: 1000+ facts/week
- Agent specializations: 3+ in 3 months

---

## 🔒 RISK MITIGATION

| Risk | Mitigation |
|------|------------|
| Graphiti complexity | Start with simple relationships, expand gradually |
| Model costs | Strict routing rules, caching, rate limiting |
| Scraping blocks | Rotate user agents, respect rate limits |
| Memory inconsistency | Regular validation, duplicate detection |
| Deployment failures | Blue-green deployments, rollback strategy |

---

## READY TO BUILD?

This plan provides:
1. **Clear architecture** with all components defined
2. **Step-by-step implementation** over 3 weeks
3. **Reusable framework** for infinite agent variations
4. **Cost-effective** operation within your budget
5. **Scalable design** from 1 to 1000+ users

**Next Action**: Review this plan and let me know if you want to proceed with Phase 1 implementation.