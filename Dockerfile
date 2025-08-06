FROM python:3.10-slim

WORKDIR /app

# Copy minimal requirements
COPY requirements-minimal.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy cloud Bob
COPY simple_bob_cloud.py .

# Simple startup
CMD ["python", "simple_bob_cloud.py"]
