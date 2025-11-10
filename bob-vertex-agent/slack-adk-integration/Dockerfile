FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/app

EXPOSE 8080

CMD exec uvicorn app.main:fastapi_app --host 0.0.0.0 --port ${PORT:-8080}
