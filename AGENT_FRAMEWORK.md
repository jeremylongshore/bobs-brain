# Unified Agent Framework Documentation
**The Single Source of Truth for Multi-Agent AI System**
**Last Updated:** 2025-08-10
**Status:** Architecture Phase

## 🎯 EXECUTIVE VISION

Building a **modular, cloud-native agent framework** that creates specialized AI agents sharing a unified knowledge layer. Starting with a research agent, expanding to domain-specific assistants, all powered by Google Cloud Platform's Model Garden and open-source tools.

### Core Philosophy
- **One Brain, Many Specialists**: Unified knowledge, specialized agents
- **Cloud-Native Minimalism**: GCP-only, no local dependencies
- **Open-Source Framework**: Graphiti + LangChain + Google ADK
- **Model Garden Maximization**: Use all 200+ models intelligently

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                   GCP Model Garden                       │
│  Gemini | Claude | Llama | PaLM | Codey | Imagen | 200+ │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│              Vertex AI Orchestration Layer              │
│         Model Router | Context Manager | RAG            │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│           Unified Knowledge Layer (Hybrid)              │
│   Graphiti (Neo4j) + Firestore + Vector Search         │
└────────────────┬────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│            Base Agent Framework (Template)              │
│     LangChain + Google ADK + Custom Orchestration      │
└──────┬──────────────┬──────────────┬───────────────────┘
       │              │              │
┌──────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
│  Research  │ │    Bob    │ │   Future  │
│   Agent    │ │  (Slack)  │ │   Agents  │
└────────────┘ └───────────┘ └───────────┘
```

## 🧠 UNIFIED KNOWLEDGE LAYER

### Hybrid Database Architecture

**1. Graphiti (Knowledge Graphs)**
- **Purpose**: Relationship intelligence, temporal reasoning
- **Deployment**: Cloud Run with Neo4j container
- **Use Cases**: 
  - Entity relationships (customers → equipment → repairs)
  - Temporal tracking (when facts changed)
  - Pattern recognition across data

**2. Firestore (Document Store)**
- **Purpose**: Fast key-value, user data, configurations
- **Collections**:
  - `agents/` - Agent configurations
  - `conversations/` - Chat histories
  - `knowledge/` - Static knowledge docs
  - `users/` - User profiles

**3. Vertex AI Vector Search**
- **Purpose**: Semantic search, RAG retrieval
- **Index Config**: 768 dimensions, STREAM_UPDATE
- **Content**: Embeddings of all knowledge

### Data Flow
```
User Query → Agent → Graphiti (relationships)
                  ↓
              Firestore (context)
                  ↓
            Vector Search (RAG)
                  ↓
            Model Garden (inference)
                  ↓
              Response
```

## 🤖 MODEL GARDEN INTEGRATION STRATEGY

### Multi-Model Routing Logic

```python
# Pseudo-code for model selection
def select_model(task_type, context_size, urgency):
    if task_type == "conversation":
        return "gemini-2.0-flash"  # Fast, cheap
    elif task_type == "research":
        return "gemini-1.5-pro"    # Smart, large context
    elif task_type == "code":
        return "codey"             # Specialized
    elif task_type == "image":
        return "imagen"            # Visual
    elif task_type == "complex_reasoning":
        return "claude-3-opus"     # Through Model Garden
    elif context_size > 200000:
        return "gemini-1.5-pro"    # 2M context window
    else:
        return "gemini-2.0-flash"  # Default
```

### Cost Optimization with $1000 Credits

| Model | Cost/1M Tokens | Use Case | Monthly Budget |
|-------|---------------|----------|----------------|
| Gemini 2.0 Flash | $0.075 | Primary (80%) | $60 |
| Gemini 1.5 Pro | $1.25 | Complex (15%) | $30 |
| Claude 3 | $15 | Special (4%) | $8 |
| Embeddings | $0.025 | Continuous | $2 |
| **Total** | - | - | **$100/month** |

Your $1000 credits = 10 months runway

## 🔧 BASE AGENT FRAMEWORK

### Core Components (Open-Source Stack)

**1. Orchestration Layer**
```python
# Framework selection
- LangChain: UI components, tool chains
- Google ADK: GCP-native orchestration  
- Crew AI: Multi-agent coordination (future)
- Graphiti: Memory and relationships
```

**2. Agent Template Structure**
```
base_agent/
├── memory/
│   ├── graphiti_connector.py    # Knowledge graphs
│   └── firestore_connector.py   # Document store
├── models/
│   ├── model_router.py          # Intelligent model selection
│   └── model_configs.yaml       # Model parameters
├── tools/
│   ├── web_scraper.py          # Playwright/BeautifulSoup
│   ├── pdf_processor.py        # Document AI
│   └── data_analyzer.py        # Pandas/NumPy
├── interfaces/
│   ├── chat_ui.py              # Streamlit/Gradio
│   └── api_endpoints.py        # FastAPI
└── specializations/
    └── research_agent.py        # First specialization
```

### Open-Source Dependencies
```yaml
# requirements.txt
langchain==0.1.0
google-cloud-aiplatform==1.71.1
graphiti==0.3.0
neo4j==5.0.0
playwright==1.40.0
beautifulsoup4==4.12.0
streamlit==1.28.0
fastapi==0.104.0
```

## 🔬 RESEARCH AGENT (First Specialization)

### Capabilities
1. **Web Scraping**
   - Public forums (Reddit, StackOverflow)
   - PDF processing (manuals, papers)
   - No-login sites only
   - Grey-area exploration with ethics

2. **Data Analysis**
   - Pattern recognition
   - Sentiment analysis
   - Trend identification
   - Source credibility scoring

3. **Knowledge Building**
   - Auto-categorization
   - Relationship mapping
   - Temporal tracking
   - Quality filtering

### Research Agent Workflow
```
1. Receive research query
2. Route to appropriate model (Gemini Flash default)
3. Search existing knowledge (Graphiti + Vector Search)
4. If insufficient:
   a. Scrape relevant sources
   b. Process with Document AI
   c. Analyze with specialized models
   d. Store in knowledge layer
5. Synthesize findings
6. Engage in intelligent discussion
```

## 🌐 INTERFACE ARCHITECTURE

### Two-Portal System

**1. startaitools.com (HQ/Command Center)**
- **Purpose**: Admin dashboard for all agents
- **Tech Stack**: 
  - Frontend: React/Next.js or Streamlit
  - Auth: Firebase Auth
  - Backend: Cloud Run + FastAPI
- **Features**:
  - Agent management console
  - Knowledge graph visualizer
  - Research agent interface
  - Analytics dashboard
  - Model usage/costs tracking

**2. diagnosticpro.io (Customer Portal)**
- **Current**: Live and functional
- **Future Integration**:
  - Read-only access to agent knowledge
  - Embedded chat widget (Phase 2)
  - API endpoints for agent queries

## 📊 IMPLEMENTATION PHASES

### Phase 1: Foundation (Weeks 1-2)
- [ ] Set up GCP project with Model Garden access
- [ ] Deploy Graphiti on Cloud Run
- [ ] Create base agent framework
- [ ] Connect Firestore + Vector Search
- [ ] Basic model router implementation

### Phase 2: Research Agent (Weeks 3-4)
- [ ] Implement web scraping tools
- [ ] PDF processing with Document AI
- [ ] Knowledge categorization system
- [ ] Conversation interface (Streamlit)
- [ ] Deploy to startaitools.com

### Phase 3: Integration (Weeks 5-6)
- [ ] Connect to DiagnosticPro database
- [ ] Build unified knowledge API
- [ ] Implement cross-agent communication
- [ ] Add monitoring and analytics
- [ ] Cost optimization pass

### Phase 4: Scale (Months 2-3)
- [ ] Second specialized agent
- [ ] Customer-facing features
- [ ] Advanced model routing
- [ ] Performance optimization
- [ ] Security hardening

## 💰 BUDGET & RESOURCES

### Monthly Costs (Estimated)
| Service | Cost | Notes |
|---------|------|-------|
| Model Garden | $100 | From free credits initially |
| Cloud Run | $50 | Auto-scaling containers |
| Firestore | $30 | Document storage |
| Vector Search | $40 | Embeddings index |
| Neo4j (Graphiti) | $50 | Graph database |
| **Total** | **$270/month** | Scales with usage |

### Development Resources
- **You**: Product vision, testing, feedback
- **Claude Code (Me)**: Architecture, implementation guidance
- **Open-Source**: Graphiti, LangChain, Playwright
- **GCP Credits**: $1000 (3-4 months runway)

## 🚀 IMMEDIATE NEXT STEPS

1. **Verify GCP Setup**
   ```bash
   gcloud config get-value project
   gcloud services list --enabled | grep aiplatform
   ```

2. **Create Project Structure**
   ```bash
   mkdir -p agent-framework/{base_agent,research_agent,shared}
   cd agent-framework
   git init
   ```

3. **Install Core Dependencies**
   ```bash
   pip install langchain google-cloud-aiplatform graphiti
   ```

4. **Deploy Graphiti Container**
   ```bash
   # Deploy Neo4j + Graphiti on Cloud Run
   gcloud run deploy graphiti-memory \
     --image neo4j:latest \
     --region us-central1
   ```

5. **Test Model Garden Access**
   ```python
   from vertexai import ModelGarden
   models = ModelGarden.list_models()
   print(f"Available models: {len(models)}")
   ```

## 🎯 SUCCESS METRICS

### Phase 1 Success
- [ ] Base framework deploys successfully
- [ ] Can route between 3+ models
- [ ] Graphiti stores and retrieves facts
- [ ] Basic UI accessible at startaitools.com

### Research Agent Success
- [ ] Scrapes 10+ sources successfully
- [ ] Processes 50+ PDFs
- [ ] Maintains conversation context
- [ ] Provides intelligent analysis
- [ ] Costs < $50/month to operate

### Long-term Success
- [ ] 5+ specialized agents deployed
- [ ] < 200ms response time
- [ ] 99.9% uptime
- [ ] Customer adoption on DiagnosticPro
- [ ] Self-sustaining on revenue

## 🔒 SECURITY & COMPLIANCE

### Data Security
- All data encrypted at rest (GCP default)
- API authentication via Firebase/OAuth
- Role-based access control (RBAC)
- Audit logging for all operations

### Scraping Ethics
- Respect robots.txt
- Identify agent in user-agent string
- Rate limiting (1-2 sec delays)
- No credential stuffing
- Public data only

## 📝 ARCHITECTURE DECISIONS LOG

### Why Graphiti over Vertex AI Memory Bank?
- **Open-source**: No vendor lock-in
- **Graph structure**: Better relationship modeling
- **Temporal reasoning**: Native time tracking
- **Cost**: Neo4j cheaper than Memory Bank
- **Control**: Full customization possible

### Why Hybrid Database?
- **Graphiti**: Relationships and intelligence
- **Firestore**: Speed and simplicity
- **Vector Search**: Semantic retrieval
- Each tool for its strength

### Why Model Garden over Single Model?
- **Cost optimization**: Use cheap models when possible
- **Specialization**: Right tool for each task
- **Flexibility**: New models instantly available
- **No lock-in**: Switch models anytime

## 🤝 COLLABORATION NOTES

### What You Own
- Product vision and priorities
- Customer relationships
- Business strategy
- Testing and feedback

### What I (Claude) Provide
- Technical architecture
- Implementation guidance
- Code examples
- Problem solving

### What Open-Source Provides
- Graphiti (memory)
- LangChain (orchestration)
- Playwright (scraping)
- Streamlit (UI)

---

## REMEMBER: Start Simple, Iterate Fast

1. Get base framework working
2. Deploy research agent
3. Gather feedback
4. Improve and expand

**This is a living document - update after each phase!**