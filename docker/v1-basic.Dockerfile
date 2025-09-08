# Bob v1 Basic - Docker Configuration
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY versions/v1-basic/requirements.txt ./v1-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt || true
RUN pip install --no-cache-dir chromadb python-dotenv

# Copy application code
COPY versions/v1-basic/ /app/
COPY data/knowledge_base/ /app/data/knowledge_base/

# Create necessary directories
RUN mkdir -p /app/data/chroma /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BOB_VERSION=v1-basic

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "from bob_clean import BobBrain; BobBrain()" || exit 1

# Run Bob
CMD ["python", "run_bob.py"]