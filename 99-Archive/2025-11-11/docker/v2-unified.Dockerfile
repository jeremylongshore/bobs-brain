# Bob v2 Unified - Docker Configuration
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY versions/v2-unified/ /app/
COPY data/knowledge_base/ /app/data/knowledge_base/

# Create necessary directories
RUN mkdir -p /app/logs /app/data/chroma

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BOB_VERSION=v2-unified
ENV BOB_HOME=/app

# Health check for Slack bot
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import slack_sdk; import chromadb; print('healthy')" || exit 1

# Note: Slack tokens must be provided via environment variables
# docker run -e SLACK_BOT_TOKEN=xoxb-... -e SLACK_APP_TOKEN=xapp-...

# Run Bob
CMD ["python", "bob_unified_v2.py"]