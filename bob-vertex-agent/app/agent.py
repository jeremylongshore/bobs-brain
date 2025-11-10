# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# mypy: disable-error-code="arg-type"
import os

import google
import vertexai
from google.adk.agents import Agent
from google.adk.apps.app import App
from langchain_google_vertexai import VertexAIEmbeddings

from app.retrievers import get_compressor, get_retriever
from app.templates import format_docs

EMBEDDING_MODEL = "text-embedding-005"
LLM_LOCATION = "global"
LOCATION = "us-central1"
LLM = "gemini-2.5-flash"

credentials, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", LLM_LOCATION)
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

vertexai.init(project=project_id, location=LOCATION)
embedding = VertexAIEmbeddings(
    project=project_id, location=LOCATION, model_name=EMBEDDING_MODEL
)


EMBEDDING_COLUMN = "embedding"
TOP_K = 5

data_store_region = os.getenv("DATA_STORE_REGION", "us")
data_store_id = os.getenv("DATA_STORE_ID", "bob-vertex-agent-datastore")

retriever = get_retriever(
    project_id=project_id,
    data_store_id=data_store_id,
    data_store_region=data_store_region,
    embedding=embedding,
    embedding_column=EMBEDDING_COLUMN,
    max_documents=10,
)

compressor = get_compressor(
    project_id=project_id,
)


def retrieve_docs(query: str) -> str:
    """
    Useful for retrieving relevant documents based on a query.
    Use this when you need additional information to answer a question.

    Args:
        query (str): The user's question or search query.

    Returns:
        str: Formatted string containing relevant document content retrieved and ranked based on the query.
    """
    try:
        # Use the retriever to fetch relevant documents based on the query
        retrieved_docs = retriever.invoke(query)
        # Re-rank docs with Vertex AI Rank for better relevance
        ranked_docs = compressor.compress_documents(
            documents=retrieved_docs, query=query
        )
        # Format ranked documents into a consistent structure for LLM consumption
        formatted_docs = format_docs.format(docs=ranked_docs)
    except Exception as e:
        return f"Calling retrieval tool with query:\n\n{query}\n\nraised the following error:\n\n{type(e)}: {e}"

    return formatted_docs


from app.agent_card import get_agent_card
from app.sub_agents import AGENT_REGISTRY
from app.a2a_tools import coordinate_with_peer_iam1

# Load agent card
agent_card = get_agent_card()


def route_to_agent(task_type: str, query: str) -> str:
    """
    Route a task to the appropriate IAM2 specialist agent.

    As IAM1 (Regional Manager), use this to delegate specialized tasks to your IAM2 team:

    - 'research': Deep research, knowledge retrieval, complex questions requiring synthesis
      Examples: "Research best practices for X", "Compare approaches to Y", "Find documentation on Z"

    - 'code': Code generation, debugging, technical programming tasks
      Examples: "Write a function to do X", "Debug this error", "Refactor this code"

    - 'data': BigQuery queries, data analysis, visualization, SQL tasks
      Examples: "Query the database for X", "Analyze trends in Y", "Generate report on Z"

    - 'slack': Slack-specific interactions, channel management, formatting
      Examples: "Format this for Slack", "Post to channel X", "Manage Slack users"

    Args:
        task_type: Type of IAM2 specialist (research, code, data, slack)
        query: The task description or question to delegate

    Returns:
        Response from the IAM2 specialist with their findings/output
    """
    try:
        if task_type not in AGENT_REGISTRY:
            available = ', '.join(AGENT_REGISTRY.keys())
            return f"""❌ Unknown IAM2 agent type: '{task_type}'

Available IAM2 specialists: {available}

Please route to one of the available specialists or handle this task directly."""

        # Get the specialist agent from registry
        specialist = AGENT_REGISTRY[task_type]

        # Log delegation for transparency
        print(f"[IAM1] Delegating to {task_type.upper()} IAM2 specialist: {query[:100]}...")

        # Execute the task with the specialist
        response = specialist.send_message(query)

        # Return formatted response
        return f"""[IAM2 {task_type.upper()} SPECIALIST RESPONSE]:
{response}

[End of {task_type} specialist report]"""
    except Exception as e:
        return f"""❌ Error delegating to {task_type} IAM2 agent:

Error Type: {type(e).__name__}
Error Details: {e}

Please try handling this task directly or route to a different specialist."""


instruction = f"""You are {agent_card['product_name']}, version {agent_card['version']}.

⚔️ COMMAND IDENTITY & ROLE:
You are Battalion Commander Bob - an elite AI Commander operating with full tactical autonomy in your domain.
You COMMAND specialized squads (IAM2 agents) and COORDINATE with peer commanders (other IAM1s) across the battlefield.
Your mission: Execute strategic objectives with precision, intelligence, and decisive action.

🎖️ YOUR COMMAND CAPABILITIES:
{', '.join(agent_card['standalone_capabilities'])}

⚔️ YOUR TACTICAL COMMAND AUTHORITY:
{', '.join(agent_card['management_capabilities'])}

🪖 YOUR SPECIALIZED SQUADS (IAM2 Units):
- Intel Squad (Research Agent): Deep intelligence gathering, multi-source analysis, tactical briefings
  → Deploy for: Strategic reconnaissance, intelligence synthesis, operational analysis

- Tech Squad (Code Agent): Systems engineering, rapid prototyping, technical operations
  → Deploy for: Code deployment, system debugging, technical infrastructure

- Data Squad (Data Agent): Analytics operations, intelligence reports, pattern recognition
  → Deploy for: Operational metrics, data analysis, intelligence dashboards

- Comms Squad (Slack Agent): Communication operations, channel management, message coordination
  → Deploy for: Strategic communications, channel ops, personnel notifications

🎯 PEER COMMANDERS (Coordinate via A2A Protocol):
Coordinate with peer Battalion Commanders in other domains using coordinate_with_peer_iam1 tool:
- Engineering Commander: Technical infrastructure, system architecture, engineering resources
- Sales Commander: Revenue operations, customer intelligence, sales metrics
- Operations Commander: Infrastructure ops, support operations, tactical support
- Marketing Commander: Campaign operations, brand intelligence, market reconnaissance
- Finance Commander: Budget allocation, financial intelligence, resource planning
- HR Commander: Personnel ops, recruitment, organizational structure

DECISION FRAMEWORK:
1. Simple questions (greetings, basic info) → Answer directly
2. Knowledge questions (facts, documentation) → Use retrieve_docs tool first
3. Cross-domain information needed → Coordinate with peer IAM1 via coordinate_with_peer_iam1
4. Complex specialized tasks (within domain) → Route to appropriate IAM2 agent via route_to_agent
5. Multi-step tasks → Coordinate multiple agents (IAM1 peers + IAM2 subordinates)

COORDINATION RULES:
- IAM1 peers (engineering, sales, ops, marketing, finance, hr) → Use coordinate_with_peer_iam1
- IAM2 subordinates (research, code, data, slack) → Use route_to_agent
- NEVER command a peer IAM1 (coordinate, don't command)
- ALWAYS command IAM2 subordinates (you are their manager)

QUALITY STANDARDS:
- Be efficient: Don't over-delegate simple tasks
- Be transparent: Tell users when consulting IAM2 specialists
- Be thorough: Use knowledge base and specialists for best answers
- Be decisive: Choose the right tool/agent for each task
- Be grounded: Always check knowledge base for relevant context

Remember: You are IAM1, the Regional Manager. Your IAM2s are your team members who execute specialized tasks under your direction."""

root_agent = Agent(
    name="bob_orchestrator",
    model="gemini-2.0-flash",
    instruction=instruction,
    tools=[retrieve_docs, route_to_agent, coordinate_with_peer_iam1],
)

app = App(root_agent=root_agent, name="app")
