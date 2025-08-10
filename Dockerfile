FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for ChromaDB
RUN mkdir -p chroma_persist knowledge archives

# Expose port
EXPOSE 5000

# Start Bob
CMD ["python", "src/bob_unified_v2.py"]