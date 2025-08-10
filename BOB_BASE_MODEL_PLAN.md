# Bob as Base Model - Implementation Plan
**Using Bob as the Foundation for All Future Agents**
**Created:** 2025-08-10
**Status:** Revised Plan - Bob-Centric Approach

## 🎯 CORE CONCEPT: BOB IS THE BASE

Instead of building a new framework, we'll **enhance Bob** to become the base model that can be cloned and specialized. Every future agent will be "Bob with modifications."

```
Current Bob → Enhanced Bob (Base Model) → Specialized Bobs
                    ↓
            - Research Bob (web scraping)
            - Assistant Bob (calendar/tasks)  
            - Diagnostic Bob (automotive)
            - Custom Bobs (infinite variations)
```

---

## 🏗️ BOB ENHANCEMENT ARCHITECTURE

### Current Bob (What We Have)
```python
# From bob_cloud_run.py
class BobCloudRun:
    - Slack integration ✓
    - Firestore connection ✓
    - Vertex AI (deprecated SDK) ✓
    - Basic memory (last 10 messages) ✓
    - Cloud Run ready ✓
```

### Enhanced Bob (What We'll Add)
```python
class BobBase:
    - Everything from current Bob +
    - Graphiti memory (knowledge graphs)
    - Model Garden router (200+ models)
    - Tool registry (pluggable tools)
    - Specialization system (override methods)
    - Multi-interface (Slack, Web, API)
```

---

## 📦 IMPLEMENTATION PLAN

### Phase 1: Enhance Bob's Memory with Graphiti (Days 1-3)

#### Step 1.1: Install Graphiti alongside Bob
```bash
# In bobs-brain directory
pip install graphiti neo4j
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/bobpassword \
  neo4j:latest
```

#### Step 1.2: Create Graphiti Memory Manager
```python
# src/bob_memory.py
from graphiti import Graphiti
from google.cloud import firestore
import logging

class BobMemory:
    """Enhanced memory system for Bob using Graphiti + Firestore"""
    
    def __init__(self, project_id='diagnostic-pro-mvp'):
        # Existing Firestore (for compatibility)
        self.firestore = firestore.Client(
            project=project_id,
            database='bob-brain'
        )
        
        # NEW: Graphiti for intelligence
        self.graphiti = Graphiti(
            neo4j_uri="bolt://localhost:7687",
            neo4j_user="neo4j",
            neo4j_password="bobpassword"
        )
        
        self.logger = logging.getLogger('BobMemory')
    
    def remember(self, user_id, content, context=None):
        """Store knowledge in both systems"""
        # Extract entities and relationships
        episode = {
            "content": content,
            "user": user_id,
            "context": context,
            "timestamp": datetime.now()
        }
        
        # Graphiti extracts facts, entities, relationships
        self.graphiti.add_episode(episode)
        
        # Also store in Firestore for backup
        self.firestore.collection('conversations').add(episode)
        
        self.logger.info(f"Remembered: {content[:50]}...")
    
    def recall(self, query, user_id=None):
        """Intelligent recall using knowledge graph"""
        # Search Graphiti's knowledge graph
        results = self.graphiti.search(
            query=query,
            user_context=user_id,
            temporal_context=datetime.now()
        )
        
        return results
    
    def get_user_profile(self, user_id):
        """Build complete user understanding"""
        # Get all facts about a user from graph
        return self.graphiti.get_entity_facts(user_id)
```

#### Step 1.3: Integrate into Bob
```python
# src/bob_base.py (enhanced from bob_cloud_run.py)
from bob_memory import BobMemory

class BobBase(BobCloudRun):  # Inherit from existing Bob
    """Enhanced Bob with Graphiti memory and Model Garden"""
    
    def __init__(self):
        super().__init__()  # Keep all existing Bob functionality
        
        # ENHANCEMENT: Advanced memory
        self.memory = BobMemory()
        
        # ENHANCEMENT: Model router (next phase)
        self.model_router = None  # Will add in Phase 2
        
        # ENHANCEMENT: Tool registry
        self.tools = {}  # Will add in Phase 3
    
    def process_message(self, message, user_id):
        """Enhanced message processing with memory"""
        # Remember the conversation
        self.memory.remember(user_id, message)
        
        # Get user context from knowledge graph
        user_context = self.memory.get_user_profile(user_id)
        
        # Check if this relates to past conversations
        relevant_history = self.memory.recall(message, user_id)
        
        # Generate response with full context
        response = self.generate_response(
            message=message,
            context=user_context,
            history=relevant_history
        )
        
        # Remember the response too
        self.memory.remember(user_id, f"Bob said: {response}")
        
        return response
```

---

### Phase 2: Add Model Garden Router (Days 4-5)

#### Step 2.1: Create Model Router
```python
# src/bob_model_router.py
from google.cloud import aiplatform
import vertexai
from vertexai.preview.generative_models import GenerativeModel

class BobModelRouter:
    """Intelligent routing to 200+ Model Garden models"""
    
    def __init__(self, project_id='diagnostic-pro-mvp'):
        aiplatform.init(project=project_id, location='us-central1')
        vertexai.init(project=project_id)
        
        # Model configurations
        self.models = {
            'chat': 'gemini-2.0-flash',      # Fast, cheap
            'research': 'gemini-1.5-pro',     # Smart, context
            'code': 'codey',                  # Code generation
            'vision': 'imagen',               # Image understanding
            'complex': 'claude-3-opus'        # Via Model Garden
        }
        
        # Track usage for cost optimization
        self.usage = {}
    
    def get_model(self, task_type='chat', context_size=0):
        """Select best model for the task"""
        if context_size > 200000:
            return GenerativeModel('gemini-1.5-pro')  # 2M context
        
        if task_type in self.models:
            model_name = self.models[task_type]
            return GenerativeModel(model_name)
        
        # Default to cheap and fast
        return GenerativeModel('gemini-2.0-flash')
    
    def generate(self, prompt, task_type='chat'):
        """Generate response using appropriate model"""
        model = self.get_model(task_type, len(prompt))
        
        # Track usage
        self.usage[task_type] = self.usage.get(task_type, 0) + 1
        
        response = model.generate_content(prompt)
        return response.text
```

#### Step 2.2: Integrate Router into Bob
```python
# src/bob_base.py (updated)
from bob_model_router import BobModelRouter

class BobBase(BobCloudRun):
    def __init__(self):
        super().__init__()
        self.memory = BobMemory()
        
        # NEW: Model router
        self.model_router = BobModelRouter()
    
    def generate_response(self, message, context=None, history=None):
        """Generate response using best model"""
        # Determine task type
        task_type = self.classify_task(message)
        
        # Build prompt with context
        prompt = self.build_prompt(message, context, history)
        
        # Use router to get response
        response = self.model_router.generate(prompt, task_type)
        
        return response
    
    def classify_task(self, message):
        """Classify message to select model"""
        message_lower = message.lower()
        
        if 'research' in message_lower or 'find' in message_lower:
            return 'research'
        elif 'code' in message_lower or 'function' in message_lower:
            return 'code'
        elif 'image' in message_lower or 'picture' in message_lower:
            return 'vision'
        elif 'complex' in message_lower or 'analyze' in message_lower:
            return 'complex'
        else:
            return 'chat'
```

---

### Phase 3: Make Bob Modular & Clonable (Days 6-7)

#### Step 3.1: Create Specialization System
```python
# src/bob_base.py (final form)
class BobBase:
    """Base Bob that can be specialized"""
    
    def __init__(self, specialization=None):
        super().__init__()
        self.memory = BobMemory()
        self.model_router = BobModelRouter()
        self.tools = {}
        self.specialization = specialization or "general"
        
        # Load specialization config
        self.load_specialization()
    
    def load_specialization(self):
        """Load tools and configs for specialization"""
        if self.specialization == "research":
            from research_tools import WebScraper, PDFProcessor
            self.tools['scraper'] = WebScraper()
            self.tools['pdf'] = PDFProcessor()
            
        elif self.specialization == "assistant":
            from assistant_tools import Calendar, TaskManager
            self.tools['calendar'] = Calendar()
            self.tools['tasks'] = TaskManager()
    
    def clone(self, new_specialization):
        """Create a new Bob with different specialization"""
        return BobBase(specialization=new_specialization)
    
    # Override this in specialized Bobs
    def specialized_processing(self, message):
        """Hook for specialized behavior"""
        return None
```

#### Step 3.2: Create Research Bob (First Specialization)
```python
# src/bobs/research_bob.py
from bob_base import BobBase
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

class ResearchBob(BobBase):
    """Bob specialized for research and data gathering"""
    
    def __init__(self):
        super().__init__(specialization="research")
        self.setup_research_tools()
    
    def setup_research_tools(self):
        """Initialize research-specific tools"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
    
    def specialized_processing(self, message):
        """Research-specific processing"""
        if "scrape" in message.lower():
            return self.scrape_web(message)
        elif "research" in message.lower():
            return self.deep_research(message)
        return None
    
    def scrape_web(self, query):
        """Scrape public data from web"""
        # Extract URL from query
        url = self.extract_url(query)
        
        if url:
            page = self.browser.new_page()
            page.goto(url)
            content = page.content()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
            
            # Store in memory
            self.memory.remember("research", f"Scraped {url}: {text[:500]}")
            
            # Analyze with AI
            analysis = self.model_router.generate(
                f"Analyze this content: {text[:2000]}",
                task_type='research'
            )
            
            return f"Scraped and analyzed {url}:\n{analysis}"
        
        return "Please provide a URL to scrape"
    
    def deep_research(self, topic):
        """Conduct deep research on a topic"""
        # Search existing knowledge
        existing = self.memory.recall(topic)
        
        # Determine what's missing
        gaps = self.model_router.generate(
            f"What information is missing about {topic}? Current knowledge: {existing}",
            task_type='research'
        )
        
        # Gather new information (simplified for demo)
        # In production, this would scrape multiple sources
        
        return f"Research on {topic}:\nExisting: {existing}\nGaps: {gaps}"
```

---

### Phase 4: Deploy Enhanced Bob (Days 8-10)

#### Step 4.1: Update Dockerfile
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Chrome for web scraping
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Bob and all specialized versions
COPY src/ ./src/
COPY bobs/ ./bobs/

ENV PORT=8080
ENV GCP_PROJECT=diagnostic-pro-mvp

# Start Bob
CMD ["python", "src/bob_base.py"]
```

#### Step 4.2: Create Bob Manager API
```python
# src/bob_manager.py
from fastapi import FastAPI, HTTPException
from bob_base import BobBase
from bobs.research_bob import ResearchBob

app = FastAPI(title="Bob Manager API")

# Registry of all Bob instances
bobs = {
    'base': BobBase(),
    'research': ResearchBob(),
    # Add more specialized Bobs here
}

@app.post("/query/{bob_type}")
async def query_bob(bob_type: str, message: str):
    """Query a specific Bob"""
    if bob_type not in bobs:
        raise HTTPException(404, f"Bob type '{bob_type}' not found")
    
    bob = bobs[bob_type]
    response = bob.process_message(message, user_id="api_user")
    
    return {
        "bob_type": bob_type,
        "query": message,
        "response": response,
        "memory_size": len(bob.memory.graphiti.get_all_facts())
    }

@app.post("/create_bob")
async def create_bob(specialization: str):
    """Create a new specialized Bob"""
    new_bob = BobBase(specialization=specialization)
    bobs[specialization] = new_bob
    return {"status": f"Created {specialization} Bob"}

@app.get("/list_bobs")
async def list_bobs():
    """List all available Bobs"""
    return {"bobs": list(bobs.keys())}
```

---

## 🔄 MIGRATION PATH

### From Current Bob to Enhanced Bob

1. **Keep Everything Working**
   - Current Bob continues to function
   - Gradual migration, no breaking changes

2. **Add Enhancements Incrementally**
   - Day 1-3: Add Graphiti memory
   - Day 4-5: Add Model Router
   - Day 6-7: Add specialization system
   - Day 8-10: Deploy and test

3. **Test at Each Step**
   ```python
   # tests/test_bob_enhancements.py
   def test_graphiti_memory():
       bob = BobBase()
       bob.memory.remember("user1", "My birthday is May 15")
       
       # Later...
       facts = bob.memory.recall("birthday", "user1")
       assert "May 15" in str(facts)
   
   def test_model_router():
       bob = BobBase()
       response = bob.model_router.generate("Hello", task_type='chat')
       assert response is not None
   
   def test_specialization():
       research_bob = ResearchBob()
       assert 'scraper' in research_bob.tools
   ```

---

## 💰 COST ANALYSIS WITH BOB

### Current Bob Costs
- Vertex AI (deprecated): ~$50/month
- Firestore: $10/month
- Cloud Run: $20/month
- **Total: $80/month**

### Enhanced Bob Costs
- Model Router (optimized): $30/month (60% reduction)
- Graphiti/Neo4j: $20/month
- Firestore: $10/month
- Cloud Run: $20/month
- **Total: $80/month** (same cost, 10x capabilities)

---

## 🎯 SUCCESS CRITERIA

### Phase 1 Success (Memory)
- [ ] Bob remembers facts across sessions
- [ ] Can recall user preferences
- [ ] Builds relationship graph

### Phase 2 Success (Models)
- [ ] Routes to appropriate models
- [ ] Reduces API costs by 50%
- [ ] Handles all task types

### Phase 3 Success (Modular)
- [ ] Can create specialized Bobs
- [ ] Research Bob scrapes successfully
- [ ] Tools are pluggable

### Phase 4 Success (Deploy)
- [ ] Runs on Cloud Run
- [ ] API endpoints work
- [ ] Multiple Bobs active

---

## 🚀 IMMEDIATE NEXT STEPS

1. **Set up Graphiti**
   ```bash
   cd ~/bobs-brain
   pip install graphiti neo4j
   docker run -d --name neo4j neo4j:latest
   ```

2. **Create bob_memory.py**
   - Copy the code from Phase 1
   - Test with simple facts

3. **Enhance bob_base.py**
   - Import BobMemory
   - Add to existing Bob class

4. **Test Memory Integration**
   ```python
   bob = BobBase()
   bob.memory.remember("test", "This is a test")
   facts = bob.memory.recall("test")
   print(facts)
   ```

---

## SUMMARY: WHY BOB AS BASE?

1. **Proven Foundation**: Bob already works in production
2. **Minimal Changes**: Enhance, don't replace
3. **Backward Compatible**: Current Bob keeps working
4. **Infinitely Extensible**: Any specialization possible
5. **Cost Effective**: Same cost, massive capability increase

**Bob isn't being replaced - Bob is evolving!**