# Bob's Brain v5 — Sovereign Agent

Clone-and-run personal agent with pluggable LLMs (Claude, Google, OpenRouter, Ollama), modular storage, Circle-of-Life learning, Slack/API surfaces.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # edit BB_API_KEY etc.
export BB_API_KEY=test
python -m flask --app src.app run --host 0.0.0.0 --port 8080
```

## Endpoints
- GET / GET /health GET /metrics GET /config GET /health/backends
- POST /api/query  (header: X-API-Key)
- POST /learn      (header: X-API-Key)
- POST /slack/events (optional)

## Switch providers

Set .env → PROVIDER=anthropic|google|openrouter|ollama, MODEL=....

## Circle of Life

Feedback → analysis → insights → memory. Scheduler via COL_SCHEDULE.

## Skills

POST /api/skill with {"name":"web_search","payload":{...}}. Add new skills under src/skills/.

## Security

API key on /api/*. Add Slack signature verify in production.

## License

MIT