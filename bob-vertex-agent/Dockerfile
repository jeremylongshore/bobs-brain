FROM python:3.12-slim
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy application code
COPY . .

# Set environment defaults
ENV PORT=8080
ENV RUN_MODE=api_server

# Expose service port
EXPOSE 8080

# Dual-mode entrypoint:
# - RUN_MODE=api_server: ADK API Server for local development (port 8000)
# - RUN_MODE=service: FastAPI production service (port 8080)
CMD ["/bin/sh", "-c", "if [ \"$RUN_MODE\" = \"service\" ]; then uv run uvicorn service.main:app --host 0.0.0.0 --port ${PORT}; else uv run python -m google.adk.cli api_server; fi"]
