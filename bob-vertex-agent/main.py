"""Bob's Brain - FastAPI Server"""
from fastapi import FastAPI
import os

app = FastAPI(title="Bob's Brain", version="0.4.0")

@app.get("/_health")
def health():
    return {"status": "ok"}

@app.get("/.well-known/agent-card")
def agent_card():
    return {
        "agent_name": "Bob's Brain",
        "capabilities": ["conversation", "rag", "slack"],
        "agent_engine_id": os.getenv("AGENT_ENGINE_ID")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
