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

from src.circle_of_life import CircleOfLife
from src.policy import guard_request
from src.providers import (
    artifact_store,
    cache_client,
    graph_db,
    llm_client,
    state_db,
    vector_store,
)
from src.skills import load_skills

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
log = logging.getLogger("bobs-brain")

app = Flask(__name__)
CORS(
    app, resources={r"/api/*": {"origins": "*"}, r"/slack/*": {"origins": "*"}}
)
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


def llm_insights(payload: dict):
    prompt = (
        "Return ONLY JSON array of {pattern, action, confidence} based on: "
        + json.dumps(payload.get("analysis", {}))
    )
    txt = LLM(prompt)
    try:
        return json.loads(txt)
    except Exception:
        return []


COL = CircleOfLife(
    neo4j_driver=GRAPH, bq_client=None, llm_call=llm_insights, logger=log
)


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
    body = request.get_json(force=True) or {}
    try:
        guard_request("/api/query", body)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    # Simple answer for demo
    answer = f"Query received: {body.get('query', '')}"
    return jsonify({"ok": True, "answer": answer})


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


@app.post("/slack/events")
def slack_events():
    payload = request.get_json(silent=True) or {}
    text = payload.get("event", {}).get("text") or ""
    result = COL.run_once([{"type": "slack_message", "text": text}])
    return jsonify({"ok": True, "circle_of_life": result})


# Scheduler
SCHED = BackgroundScheduler(daemon=True)
if os.getenv("COL_SCHEDULE"):
    from apscheduler.triggers.cron import CronTrigger

    def scheduled_col():
        try:
            COL.run_once([{"type": "heartbeat", "ts": time.time()}])
        except Exception as e:
            log.warning("CoL scheduled run failed: %s", e)

    SCHED.add_job(
        scheduled_col, CronTrigger.from_crontab(os.getenv("COL_SCHEDULE"))
    )
    SCHED.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
