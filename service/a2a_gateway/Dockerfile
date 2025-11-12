# A2A Gateway - Cloud Run Deployment
# R3 Compliant: Gateway only (no Runner)

FROM python:3.12-slim

WORKDIR /app

# Copy gateway requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy A2A card module (needed for AgentCard)
# Note: We only copy what's needed - NOT the full agent runtime
COPY ../../my_agent/a2a_card.py ./my_agent/a2a_card.py
COPY ../../my_agent/__init__.py ./my_agent/__init__.py

# Copy gateway service
COPY main.py .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8080/health')"

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
