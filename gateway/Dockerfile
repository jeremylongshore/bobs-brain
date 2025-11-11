FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy gateway code
COPY gateway/ ./gateway/

# Set environment
ENV PORT=8080

# Run uvicorn
CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8080"]
