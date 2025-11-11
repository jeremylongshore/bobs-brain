# Bob's Brain - Agent Container for Vertex AI Agent Engine
# Hard Mode: ADK + Agent Engine only (R1, R2)
# Last Updated: 2025-11-11

# Use official Python runtime
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY my_agent/ ./my_agent/

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

# Expose port (Agent Engine manages this)
EXPOSE 8080

# Health check (optional - Agent Engine has its own)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import sys; sys.exit(0)"

# Run agent (Agent Engine invokes this)
# Note: Agent Engine manages the runner lifecycle
# This entry point is for local testing only
CMD ["python", "-m", "my_agent.agent"]
