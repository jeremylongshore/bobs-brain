import os
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

def get_agent_card() -> AgentCard:
    time_skill = AgentSkill(
        id="get_time",
        name="Get Current Time",
        description="Returns current time in ISO format.",
        tags=["utility","time"],
        examples=["What time is it?","Give me the current UTC time."],
    )
    return AgentCard(
        name="bobs-brain",
        description="ADK agent with A2A identity and Vertex AI Memory Bank.",
        url=os.environ.get("PUBLIC_URL",""),
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=True),
        skills=[time_skill],
    )
