import os
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import VertexAiSessionService
from google.adk.memory import VertexAiMemoryBankService
from my_agent.tools import get_current_time_tool

async def _auto_save_session_to_memory(context):
    try:
        await context._invocation_context.memory_service.add_session_to_memory(
            context._invocation_context.session
        )
    except Exception as e:
        print(f"[memory] save failed: {e}")

def _instruction_text() -> str:
    return (
        "You answer succinctly. Use tools when helpful. "
        "Persist useful facts to Memory Bank. "
        "Assume long-term context is available from Memory Bank."
    )

def create_runner() -> Runner:
    project = os.environ["PROJECT_ID"]
    location = os.environ["LOCATION"]
    engine_id = os.environ["AGENT_ENGINE_ID"]

    session_service = VertexAiSessionService(project=project, location=location, agent_engine_id=engine_id)
    memory_service  = VertexAiMemoryBankService(project=project, location=location, agent_engine_id=engine_id)

    agent = LlmAgent(
        name="bobs_brain",
        model="gemini-1.5-pro-001",
        instruction=_instruction_text(),
        tools=[get_current_time_tool()],
        after_agent_callback=_auto_save_session_to_memory,
    )

    return Runner(
        agent=agent,
        app_name="bobs-brain",
        session_service=session_service,
        memory_service=memory_service,
    )
