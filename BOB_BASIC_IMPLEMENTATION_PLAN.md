# 🧠 BOB BASIC - CLEAN IMPLEMENTATION PLAN

## Requirements (From Your Notes)
- Simple, functional Bob as personal brain replacement
- 16GB RAM optimized (can run multiple models)
- Non-coder workflow
- Must work with existing 962 knowledge items
- Focus on Bob Basic, not Pimp Bob (long-term)

## Architecture Design

### Core Components
```
Bob Basic Core
├── Simple Chat Interface (no ReAct needed)
├── Smart Model Router
│   ├── Gemma 2B (1.7GB) - Quick responses
│   ├── Mistral 7B (4.4GB) - Complex reasoning
│   └── Qwen2.5-Coder 14B (9GB) - Code generation
├── Knowledge System
│   ├── ChromaDB (existing 962 items)
│   └── Sentence-Transformers embeddings (384 dim)
└── Memory System
    ├── SQLite conversations
    └── Context management
```

## Implementation Steps

### Step 1: Fix Embedding System (5 min)
```python
# Replace OllamaEmbeddings with sentence-transformers
from sentence_transformers import SentenceTransformer
embeddings = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions
```

### Step 2: Create Smart Router (10 min)
```python
class BobRouter:
    def route_query(self, query):
        if len(query) < 50:  # Quick question
            return "gemma:2b"
        elif "code" in query or "implement" in query:
            return "qwen2.5-coder:14b"
        else:
            return "mistral:7b"
```

### Step 3: Simple Conversation Handler (15 min)
```python
class BobBasic:
    def chat(self, message):
        # 1. Search knowledge
        context = self.search_knowledge(message)

        # 2. Route to best model
        model = self.router.route_query(message)

        # 3. Generate response
        response = self.ollama_chat(model, message, context)

        # 4. Save to memory
        self.save_conversation(message, response)

        return response
```

### Step 4: Unified Interface (5 min)
```python
# Single entry point for all interactions
bob = BobBasic()
bob.chat("What's the status of DiagnosticPro?")
bob.search("API keys")
bob.remember("New information")
```

## Performance Optimizations

1. **Async Everything**: Non-blocking I/O
2. **Response Streaming**: Start showing response immediately
3. **Context Caching**: Remember last 10 conversations
4. **Parallel Search**: Query knowledge while model loads

## Memory Usage (16GB RAM)
- OS & System: ~2GB
- Gemma 2B: 1.7GB (always loaded)
- Mistral 7B: 4.4GB (on-demand)
- Qwen 14B: 9GB (on-demand)
- ChromaDB + Embeddings: ~1GB
- Buffer: ~2GB

## Success Metrics
- ✅ Response time < 3 seconds for simple queries
- ✅ Access to all 962 knowledge items
- ✅ Can generate code when needed
- ✅ Remembers conversation context
- ✅ Works reliably without timeouts

## What We're NOT Doing (Keep it Simple)
- ❌ No ReAct chains (unnecessary complexity)
- ❌ No LangGraph (save for Pimp Bob)
- ❌ No multi-agent systems (yet)
- ❌ No web deployments (local only)
- ❌ No complex tool chains

## Deliverable
One clean `bob_basic.py` file that:
1. Works immediately
2. Has no deprecated dependencies
3. Uses all available models efficiently
4. Accesses existing knowledge
5. Provides simple chat interface
