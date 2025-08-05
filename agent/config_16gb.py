"""
Bob Configuration for 16GB RAM System
Optimized for e2-highmem-2 instance
"""

# Model configurations for 16GB RAM - ALL THE GOOD STUFF!
MODEL_CONFIGS = {
    # Full power configuration
    "full_stack": {
        "general": "mistral:latest",  # 4.5GB - Primary brain
        "reasoning": "gemma:7b",  # 3.5GB - Deep thinking
        "code": "codellama:7b",  # 3.8GB - Code specialist
        "fast": "gemma:2b",  # 1.7GB - Quick responses
        "embeddings": "nomic-embed-text",  # 0.5GB - For RAG
    },
    # Balanced configuration (recommended)
    "balanced": {
        "general": "mistral:latest",  # 4.5GB
        "code": "codellama:7b",  # 3.8GB
        "embeddings": "gemma:2b",  # 1.7GB for embeddings
    },
}

# With 16GB you can run ALL of these:
ENABLED_FEATURES = [
    "Multiple models simultaneously",
    "Advanced RAG with large documents",
    "Complex multi-agent workflows",
    "Real-time model switching",
    "Parallel tool execution",
    "Large context windows",
    "CrewAI multi-agent teams",
    "LangGraph orchestration",
    "Full LangChain tool suite",
]

# Memory allocation guide
MEMORY_BUDGET = {
    "models": "12GB",  # For LLMs
    "system": "2GB",  # OS and services
    "applications": "2GB",  # Python, ChromaDB, etc
}
