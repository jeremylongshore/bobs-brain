import hashlib
import json
import logging
import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

from src.features.circle_of_life import CircleOfLife
from src.features.knowledge_orchestrator import get_knowledge_orchestrator
from src.shared.policy import guard_request
from src.core.providers import (
    artifact_store,
    cache_client,
    graph_db,
    llm_client,
    state_db,
    vector_store,
)
from src.features.skills import load_skills
from src.features.smart_router import SmartRouter

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("bobs-brain")

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}, r"/slack/*": {"origins": "*"}})
limiter = Limiter(get_remote_address, app=app, default_limits=["60/minute"])

API_KEY = os.getenv("BB_API_KEY")
OPEN_PATHS = {
    "/",
    "/health",
    "/metrics",
    "/config",
    "/health/backends",
    "/slack/events",
}


@app.before_request
def auth():
    if request.path in OPEN_PATHS:
        return
    key = request.headers.get("X-API-Key")
    if not API_KEY or key != API_KEY:
        return jsonify({"error": "unauthorized"}), 401


REQS = Counter("bb_requests_total", "Requests total", ["route"])


@app.after_request
def _count(resp):
    try:
        REQS.labels(request.path).inc()
    except Exception:
        pass
    return resp


# Backends
LLM = llm_client()
STATE = state_db()
VEC = vector_store()
GRAPH = graph_db()
CACHE = cache_client()
ARTS = artifact_store()
SKILLS = load_skills()
KNOWLEDGE = get_knowledge_orchestrator()  # LlamaIndex multi-source knowledge
ROUTER = SmartRouter()  # Smart routing: Ollama + Groq + Gemini + Claude


def llm_insights(payload: dict):
    prompt = "Return ONLY JSON array of {pattern, action, confidence} based on: " + json.dumps(
        payload.get("analysis", {})
    )
    txt = LLM(prompt)
    try:
        return json.loads(txt)
    except Exception:
        return []


COL = CircleOfLife(neo4j_driver=GRAPH, bq_client=None, llm_call=llm_insights, logger=log)


# ========== CONVERSATION MEMORY HELPERS ==========

def get_conversation_history(user_id: str, limit: int = 10) -> list:
    """
    Retrieve conversation history for a user from Redis.
    Returns list of {"role": "user/assistant", "content": "..."}
    """
    if not CACHE:
        return []

    try:
        key = f"conversation:{user_id}"
        messages = CACHE.lrange(key, 0, limit - 1)
        return [json.loads(msg) for msg in messages]
    except Exception as e:
        log.warning(f"Failed to get conversation history: {e}")
        return []


def add_to_conversation(user_id: str, role: str, content: str, ttl: int = 86400):
    """
    Add a message to conversation history.
    TTL = 24 hours (86400 seconds)
    """
    if not CACHE:
        return

    try:
        key = f"conversation:{user_id}"
        message = json.dumps({"role": role, "content": content})

        # Add to beginning of list (most recent first)
        CACHE.lpush(key, message)

        # Keep only last 20 messages
        CACHE.ltrim(key, 0, 19)

        # Set expiry
        CACHE.expire(key, ttl)
    except Exception as e:
        log.warning(f"Failed to add to conversation: {e}")


def build_conversation_prompt(history: list, current_query: str, knowledge_context: str = "") -> str:
    """
    Build a prompt with conversation history + current query.
    """
    if not history:
        # No history, just use current query
        if knowledge_context:
            return f"Context from knowledge bases:\n{knowledge_context}\n\nQuestion: {current_query}\n\nAnswer based on the context above, keep it concise:"
        return current_query

    # Build conversation context
    conversation = []
    for msg in reversed(history):  # Oldest to newest
        role = msg.get("role", "")
        content = msg.get("content", "")
        if role == "user":
            conversation.append(f"User: {content}")
        elif role == "assistant":
            conversation.append(f"Assistant: {content}")

    # Add knowledge context if available
    context_section = ""
    if knowledge_context:
        context_section = f"Context from knowledge bases:\n{knowledge_context}\n\n"

    # Build full prompt
    prompt = f"""{context_section}Previous conversation:
{chr(10).join(conversation)}

User: {current_query}

Assistant (respond naturally, keep it concise):"""

    return prompt


# ========== LLM RESPONSE CACHING HELPERS ==========

def get_cached_llm_response(query: str) -> dict:
    """
    Check if we've answered this exact question recently.
    Returns {"cached": True, "answer": "..."} or None
    """
    if not CACHE:
        return None

    try:
        # Create cache key from query hash
        cache_key = f"llm_cache:{hashlib.md5(query.lower().strip().encode()).hexdigest()}"

        cached = CACHE.get(cache_key)
        if cached:
            log.info(f"Cache HIT for query: {query[:50]}...")
            return {"cached": True, "answer": cached.decode('utf-8')}

        return None
    except Exception as e:
        log.warning(f"Failed to get cached response: {e}")
        return None


def cache_llm_response(query: str, answer: str, ttl: int = 3600):
    """
    Cache an LLM response for future use.
    TTL = 1 hour (3600 seconds) by default
    """
    if not CACHE:
        return

    try:
        cache_key = f"llm_cache:{hashlib.md5(query.lower().strip().encode()).hexdigest()}"
        CACHE.setex(cache_key, ttl, answer)
        log.info(f"Cached response for query: {query[:50]}...")
    except Exception as e:
        log.warning(f"Failed to cache response: {e}")


@app.get("/")
def root():
    return jsonify({"name": "bobs-brain", "version": "5.0", "status": "ok"})


@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": time.time(), "graph": bool(GRAPH)})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/config")
def config_view():
    return jsonify(
        {
            "provider": os.getenv("PROVIDER", "anthropic"),
            "model": os.getenv("MODEL", "claude-3-5-sonnet-20240620"),
            "state": os.getenv("STATE_BACKEND", "sqlite"),
            "vector": os.getenv("VECTOR_BACKEND", "chroma"),
            "graph": os.getenv("GRAPH_BACKEND", "none"),
            "cache": os.getenv("CACHE_BACKEND", "none"),
            "artifact": os.getenv("ARTIFACT_BACKEND", "local"),
        }
    )


@app.get("/health/backends")
def health_backends():
    ok = {}
    try:
        conn = STATE.connect()
        conn.close()
        ok["state"] = "ok"
    except Exception as e:
        ok["state"] = f"fail:{e}"
    try:
        if GRAPH:
            with GRAPH.session() as s:
                s.run("RETURN 1")
        ok["graph"] = "ok" if GRAPH else "disabled"
    except Exception as e:
        ok["graph"] = f"fail:{e}"
    ok["vector"] = os.getenv("VECTOR_BACKEND", "chroma")
    ok["cache"] = "ok" if CACHE else "disabled"
    ok["artifact"] = os.getenv("ARTIFACT_BACKEND", "local")
    return jsonify(ok)


@app.post("/api/query")
def api_query():
    """
    Smart Query with Knowledge Integration

    POST /api/query
    {
        "query": "What is Python?",
        "force_provider": "groq"  // optional: ollama, groq, google, anthropic
    }

    Returns:
    {
        "ok": true,
        "answer": "...",
        "routing": {
            "provider": "groq",
            "model": "llama-3.1-70b-versatile",
            "complexity": 0.25,
            "reasoning": "Medium complexity - using Groq (free tier)",
            "estimated_cost": 0.0
        },
        "knowledge_used": true
    }
    """
    body = request.get_json(force=True) or {}
    try:
        guard_request("/api/query", body)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    query = body.get("query", "")
    force_provider = body.get("force_provider")

    if not query:
        return jsonify({"error": "query required"}), 400

    try:
        # 1. Check cache first (unless force_provider is specified)
        if not force_provider:
            cached_result = get_cached_llm_response(query)
            if cached_result:
                return jsonify({
                    "ok": True,
                    "answer": cached_result['answer'],
                    "cached": True,
                    "routing": {"provider": "cache", "model": "cached"},
                    "knowledge_used": False
                })

        # 2. Route to optimal provider based on complexity
        routing = ROUTER.route(query, force_provider=force_provider)

        # 3. Query knowledge base for context (if complexity warrants it)
        knowledge_context = ""
        if routing['complexity'] > 0.3:
            try:
                knowledge_result = KNOWLEDGE.query(query, mode='auto')
                knowledge_context = knowledge_result.get('answer', '')
            except Exception as e:
                log.warning(f"Knowledge query failed: {e}")

        # 4. Generate answer using selected provider
        # Set environment for llm_client() to use selected provider
        original_provider = os.getenv("PROVIDER")
        original_model = os.getenv("MODEL")

        os.environ["PROVIDER"] = routing['provider']
        os.environ["MODEL"] = routing['model']

        # Get fresh LLM client with new provider
        llm = llm_client()

        # Build prompt with knowledge context if available
        if knowledge_context:
            prompt = f"Context from knowledge base:\n{knowledge_context}\n\nQuestion: {query}\n\nAnswer based on the context above:"
        else:
            prompt = query

        # Generate answer
        answer = llm(prompt)

        # Restore original provider settings
        if original_provider:
            os.environ["PROVIDER"] = original_provider
        if original_model:
            os.environ["MODEL"] = original_model

        # 5. Cache the response
        cache_llm_response(query, answer, ttl=3600)

        # Track cost
        ROUTER.track_cost(routing['estimated_cost'])

        return jsonify({
            "ok": True,
            "answer": answer,
            "routing": routing,
            "knowledge_used": bool(knowledge_context),
            "cached": False
        })

    except Exception as e:
        log.error(f"Query failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.post("/learn")
def learn():
    body = request.get_json(force=True) or {}
    ev = {
        "type": "correction",
        "correction": body.get("correction", ""),
        "context": body.get("context"),
    }
    result = COL.run_once([ev])
    return jsonify({"ok": True, "circle_of_life": result})


@app.post("/api/skill")
def api_skill():
    body = request.get_json(force=True) or {}
    name = body.get("name")
    payload = body.get("payload", {})
    fn = SKILLS.get(name)
    if not fn:
        return jsonify({"error": "unknown skill"}), 404
    out = fn(payload)
    return jsonify({"ok": True, "result": out})


@app.post("/api/knowledge")
def api_knowledge():
    """
    Query multi-source knowledge (Research + Knowledge DB + Analytics)

    POST /api/knowledge
    {
        "query": "What are LLM gateway best practices?",
        "mode": "auto"  // auto, research, knowledge, analytics, all
    }
    """
    body = request.get_json(force=True) or {}
    query = body.get("query", "")
    mode = body.get("mode", "auto")

    if not query:
        return jsonify({"error": "query required"}), 400

    try:
        result = KNOWLEDGE.query(query, mode=mode)
        return jsonify({"ok": True, **result})
    except Exception as e:
        log.error(f"Knowledge query failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.get("/api/knowledge/status")
def knowledge_status():
    """Check knowledge orchestrator status"""
    status = KNOWLEDGE.get_status()
    return jsonify(status)


@app.get("/api/router/status")
def router_status():
    """
    Check smart router status

    GET /api/router/status

    Returns available providers and usage stats
    """
    status = ROUTER.get_status()
    return jsonify(status)


# Deduplication cache for Slack events (prevent retries from processing twice)
_slack_event_cache = {}

def _process_slack_message(text, channel, user, event_id):
    """Background processing of Slack messages"""
    try:
        # 1. Check cache first (exact match)
        cached_result = get_cached_llm_response(text)
        if cached_result:
            # Send cached response to Slack
            try:
                from slack_sdk import WebClient
                slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
                response_text = f"{cached_result['answer']}\n\n_[cached]_"
                slack_client.chat_postMessage(
                    channel=channel,
                    text=response_text,
                    unfurl_links=False,
                    unfurl_media=False
                )
                log.info(f"Sent cached response to channel {channel}")

                # Still add to conversation history
                add_to_conversation(user, "user", text)
                add_to_conversation(user, "assistant", cached_result['answer'])
                return
            except Exception as e:
                log.error(f"Failed to send cached Slack message: {e}")
                # Fall through to generate new response

        # 2. Get conversation history for context
        conversation_history = get_conversation_history(user, limit=10)
        log.info(f"Loaded {len(conversation_history)} previous messages for user {user}")

        # 3. Route to optimal LLM provider based on complexity
        routing = ROUTER.route(text)
        log.info(f"Slack query routed to: {routing['provider']} (complexity: {routing['complexity']:.2f})")

        # 4. Query knowledge bases for context (if complex enough)
        knowledge_context = ""
        if routing['complexity'] > 0.3:
            try:
                knowledge_result = KNOWLEDGE.query(text, mode='auto')
                knowledge_context = knowledge_result.get('answer', '')
                log.info(f"Knowledge context retrieved: {len(knowledge_context)} chars")
            except Exception as e:
                log.warning(f"Knowledge query failed: {e}")

        # 5. Generate answer using selected provider
        original_provider = os.getenv("PROVIDER")
        original_model = os.getenv("MODEL")

        os.environ["PROVIDER"] = routing['provider']
        os.environ["MODEL"] = routing['model']

        llm = llm_client()
        prompt = build_conversation_prompt(conversation_history, text, knowledge_context)
        answer = llm(prompt)

        # Restore original provider settings
        if original_provider:
            os.environ["PROVIDER"] = original_provider
        if original_model:
            os.environ["MODEL"] = original_model

        # 6. Cache the response
        cache_llm_response(text, answer, ttl=3600)

        # 7. Add to conversation history
        add_to_conversation(user, "user", text)
        add_to_conversation(user, "assistant", answer)

        # 8. Send to Slack
        try:
            from slack_sdk import WebClient
            slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
            response_text = f"{answer}\n\n_[via {routing['provider']}]_"
            slack_client.chat_postMessage(
                channel=channel,
                text=response_text,
                unfurl_links=False,
                unfurl_media=False
            )
            log.info(f"Sent Slack response to channel {channel}")
        except Exception as e:
            log.error(f"Failed to send Slack message: {e}")

        # 9. Learn from interaction
        COL.run_once([{
            "type": "slack_message",
            "text": text,
            "answer": answer,
            "provider": routing['provider'],
            "knowledge_used": bool(knowledge_context),
            "had_conversation_context": len(conversation_history) > 0
        }])

        # Track cost
        ROUTER.track_cost(routing['estimated_cost'])

    except Exception as e:
        log.error(f"Background Slack processing failed: {e}")
    finally:
        # Remove from dedup cache after processing (keep for 60 seconds)
        import threading
        threading.Timer(60, lambda: _slack_event_cache.pop(event_id, None)).start()


@app.post("/slack/events")
def slack_events():
    """
    Slack Event Handler

    Responds to messages in Slack using:
    1. Smart Router to pick LLM provider (Ollama/Groq/Gemini/Claude)
    2. Knowledge Orchestrator for context from knowledge bases
    3. Circle of Life for learning

    IMPORTANT: Returns HTTP 200 immediately to prevent Slack retries.
    Processes messages in background thread.
    """
    payload = request.get_json(silent=True) or {}

    # Handle Slack URL verification (first-time setup)
    if payload.get("type") == "url_verification":
        return jsonify({"challenge": payload.get("challenge")})

    event = payload.get("event", {})
    event_type = event.get("type")
    event_id = payload.get("event_id", "")

    # Deduplicate: Slack retries if we don't respond fast enough
    if event_id and event_id in _slack_event_cache:
        log.info(f"Ignoring duplicate event: {event_id}")
        return jsonify({"ok": True})

    if event_id:
        _slack_event_cache[event_id] = True

    # Ignore bot messages to prevent loops
    if event.get("bot_id") or event.get("user") == "USLACKBOT":
        return jsonify({"ok": True})

    # Only respond to messages
    if event_type not in ["message", "app_mention"]:
        return jsonify({"ok": True})

    text = event.get("text", "")
    channel = event.get("channel")
    user = event.get("user")

    if not text or not channel:
        return jsonify({"ok": True})

    # Process message in background thread to return HTTP 200 immediately
    import threading
    thread = threading.Thread(
        target=_process_slack_message,
        args=(text, channel, user, event_id),
        daemon=True
    )
    thread.start()

    # Return HTTP 200 immediately to acknowledge receipt
    log.info(f"Queued Slack message from {user} in {channel} for background processing")
    return jsonify({"ok": True})


# Scheduler
SCHED = BackgroundScheduler(daemon=True)
if os.getenv("COL_SCHEDULE"):
    from apscheduler.triggers.cron import CronTrigger

    def scheduled_col():
        try:
            COL.run_once([{"type": "heartbeat", "ts": time.time()}])
        except Exception as e:
            log.warning("CoL scheduled run failed: %s", e)

    SCHED.add_job(scheduled_col, CronTrigger.from_crontab(os.getenv("COL_SCHEDULE")))
    SCHED.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
