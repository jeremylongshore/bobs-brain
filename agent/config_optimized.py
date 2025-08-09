"""
BOB Optimized Configuration - Performance Tuned
Memory and model settings optimized for your system
"""

from pathlib import Path

# Base paths
BASE_DIR = Path.home() / ".bob_consolidated"
DATA_DIR = Path(__file__).parent.parent / "data" / "consolidated_db"

# Model Configuration - Optimized for 16GB RAM
MODEL_CONFIG = {
    "primary": {
        "model": "gemma:2b",  # Fast, efficient for quick responses
        "temperature": 0.7,
        "max_tokens": 2048,
        "context_window": 8192,
    },
    "advanced": {
        "model": "mistral:7b",  # More capable for complex tasks
        "temperature": 0.3,
        "max_tokens": 4096,
        "context_window": 32768,
    },
    "code": {
        "model": "codellama:13b",  # Specialized for code tasks
        "temperature": 0.1,
        "max_tokens": 4096,
        "context_window": 16384,
    },
}

# Memory Settings - Optimized for performance
MEMORY_CONFIG = {
    "conversation_buffer": 10,  # Last N exchanges to keep in memory
    "max_memory_tokens": 2000,
    "sqlite_db": str(DATA_DIR / "bob_main.db"),
    "cache_ttl": 3600,  # 1 hour cache
    "batch_size": 5,  # Process memories in batches
}

# Vector Store Configuration - ChromaDB optimized
VECTOR_CONFIG = {
    "persist_directory": str(BASE_DIR / "chroma_db"),
    "collection_name": "bob_knowledge",
    "embedding_model": "gemma:2b",  # Use same model for embeddings
    "chunk_size": 512,
    "chunk_overlap": 50,
    "similarity_top_k": 5,
}

# Agent Configuration
AGENT_CONFIG = {
    "max_iterations": 10,
    "early_stopping": True,
    "verbose": False,  # Reduce console output
    "handle_errors": True,
    "max_execution_time": 30,  # seconds
}

# Performance Optimizations
PERFORMANCE_CONFIG = {
    "enable_caching": True,
    "parallel_processing": True,
    "lazy_loading": True,
    "compression": True,
    "batch_operations": True,
}

# Ollama Server Settings
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "timeout": 120,
    "num_gpu": 1,  # Use GPU if available
    "num_thread": 8,  # CPU threads
    "num_ctx": 8192,  # Context size
    "keep_alive": "5m",  # Keep models in memory
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": "INFO",
    "file": str(Path(__file__).parent.parent / "logs" / "bob.log"),
    "max_size": "10MB",
    "backup_count": 3,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
}

# Tool Settings
TOOLS_CONFIG = {
    "enable_web_search": True,
    "enable_file_ops": True,
    "enable_shell": False,  # Disabled for security
    "enable_python_repl": True,
    "max_tool_output": 2000,  # Truncate long outputs
}

# System Resources
RESOURCE_LIMITS = {
    "max_memory_percent": 50,  # Use up to 50% of system RAM
    "max_cpu_percent": 80,
    "max_concurrent_tasks": 3,
}


def get_config(profile="balanced"):
    """
    Get configuration based on profile
    Profiles: 'fast', 'balanced', 'quality'
    """
    configs = {
        "fast": {
            "model": MODEL_CONFIG["primary"],
            "memory": {**MEMORY_CONFIG, "conversation_buffer": 5},
            "agent": {**AGENT_CONFIG, "max_iterations": 5},
        },
        "balanced": {
            "model": MODEL_CONFIG["primary"],
            "memory": MEMORY_CONFIG,
            "agent": AGENT_CONFIG,
        },
        "quality": {
            "model": MODEL_CONFIG["advanced"],
            "memory": {**MEMORY_CONFIG, "conversation_buffer": 15},
            "agent": {**AGENT_CONFIG, "max_iterations": 15},
        },
    }
    return configs.get(profile, configs["balanced"])
