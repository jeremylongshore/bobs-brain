import os
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from google.adk.serving.fastapi import add_adk_routes, add_a2a_routes, AdkServingConfig
from my_agent.agent import create_runner
from my_agent.a2a_manager import get_agent_card
from opentelemetry import trace

app = FastAPI(title="bobs-brain", description="ADK agent with A2A + Memory Bank")
runner = create_runner()
agent_card = get_agent_card()
add_a2a_routes(app=app, agent_card=agent_card)
add_adk_routes(app=app, runner=runner, config=AdkServingConfig(app_name=agent_card.name))

@app.get("/_health")
def health(request: Request):
    span = trace.get_current_span()
    ctx = span.get_span_context() if span else None
    trace_id = f"{ctx.trace_id:032x}" if ctx and ctx.is_valid else None
    headers = {"X-Trace-Id": trace_id} if trace_id else {}
    return JSONResponse({"status": "ok", "engine_id": os.getenv("AGENT_ENGINE_ID"), "trace_id": trace_id}, headers=headers)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
