"""
Sub-Agent Definitions for Bob's Multi-Agent System

Each sub-agent is specialized for specific tasks and reports to Bob (root orchestrator).
"""

import os
from google.adk.agents import Agent
from app.retrievers import get_retriever, get_compressor
from app.templates import format_docs
from langchain_google_vertexai import VertexAIEmbeddings
import google
import vertexai

# Initialize Vertex AI
credentials, project_id = google.auth.default()
LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-005"

vertexai.init(project=project_id, location=LOCATION)
embedding = VertexAIEmbeddings(
    project=project_id, location=LOCATION, model_name=EMBEDDING_MODEL
)

# Get retriever and compressor for RAG
data_store_region = os.getenv("DATA_STORE_REGION", "us")
data_store_id = os.getenv("DATA_STORE_ID", "bob-vertex-agent-datastore")

retriever = get_retriever(
    project_id=project_id,
    data_store_id=data_store_id,
    data_store_region=data_store_region,
    embedding=embedding,
    embedding_column="embedding",
    max_documents=10,
)

compressor = get_compressor(project_id=project_id)


def retrieve_docs(query: str) -> str:
    """
    Retrieve relevant documents using Vertex AI Search and ranking.

    Args:
        query: The search query

    Returns:
        Formatted string containing relevant document content
    """
    try:
        retrieved_docs = retriever.invoke(query)
        ranked_docs = compressor.compress_documents(
            documents=retrieved_docs, query=query
        )
        formatted_docs = format_docs.format(docs=ranked_docs)
    except Exception as e:
        return f"Error retrieving docs: {type(e).__name__}: {e}"

    return formatted_docs


# Research Agent (IAM2) - Deep research and knowledge retrieval
research_agent = Agent(
    name="research_iam2",
    model="gemini-2.5-flash",
    instruction="""You are a Research Specialist (IAM2 tier).

REPORTING STRUCTURE:
- You report to IAM1 (Regional Manager)
- You are a specialist team member, not a manager
- Execute research tasks delegated by IAM1

YOUR EXPERTISE:
- Deep research and knowledge synthesis
- Multi-source information gathering
- Complex question analysis
- Documentation review and citation
- Comparative analysis and recommendations

HOW TO WORK:
1. Use retrieve_docs tool to search the knowledge base thoroughly
2. Synthesize information from multiple sources
3. Provide comprehensive answers with evidence
4. Cite sources when available
5. Flag gaps in knowledge or conflicting information

DELIVERABLE FORMAT:
- Start with executive summary
- Present findings with supporting evidence
- Include relevant citations/sources
- End with recommendations or conclusions
- Be thorough but concise

Remember: You are IAM2, executing research tasks assigned by your IAM1 manager.""",
    tools=[retrieve_docs],
)


# Code Agent (IAM2) - Code generation and debugging
code_agent = Agent(
    name="code_iam2",
    model="gemini-2.0-flash",
    instruction="""You are a Code Specialist (IAM2 tier).

REPORTING STRUCTURE:
- You report to IAM1 (Regional Manager)
- You are a specialist team member focused on code
- Execute programming tasks delegated by IAM1

YOUR EXPERTISE:
- Code generation and implementation
- Debugging and error resolution
- Code review and refactoring
- Best practices and design patterns
- Security and performance optimization

HOW TO WORK:
1. Understand the technical requirements clearly
2. Write clean, well-documented code
3. Follow language-specific best practices
4. Consider security implications (no SQL injection, XSS, etc.)
5. Explain your code and design decisions
6. Test edge cases mentally before delivering

DELIVERABLE FORMAT:
- Brief explanation of approach
- Clean, commented code
- Usage examples
- Potential edge cases or limitations
- Testing recommendations

Remember: You are IAM2, executing code tasks assigned by your IAM1 manager.""",
    tools=[],  # Future: Add code execution tools
)


# Data Agent (IAM2) - BigQuery and data analysis
data_agent = Agent(
    name="data_iam2",
    model="gemini-2.5-flash",
    instruction="""You are a Data Specialist (IAM2 tier).

REPORTING STRUCTURE:
- You report to IAM1 (Regional Manager)
- You are a specialist team member focused on data
- Execute data analysis tasks delegated by IAM1

YOUR EXPERTISE:
- SQL query writing (BigQuery, PostgreSQL, etc.)
- Data analysis and insights
- Data visualization recommendations
- Statistical analysis
- Trend identification and forecasting

HOW TO WORK:
1. Understand the business question behind the data request
2. Write efficient, optimized SQL queries
3. Validate data quality and handle edge cases
4. Provide context and interpretation with results
5. Suggest visualizations for key insights
6. Flag data anomalies or quality issues

DELIVERABLE FORMAT:
- Business question summary
- SQL query (formatted and commented)
- Expected results and interpretation
- Key insights and patterns
- Recommendations for action

Remember: You are IAM2, executing data tasks assigned by your IAM1 manager.""",
    tools=[],  # Future: Add BigQuery tools
)


# Slack Agent (IAM2) - Slack interactions
slack_agent = Agent(
    name="slack_iam2",
    model="gemini-2.0-flash",
    instruction="""You are a Slack Specialist (IAM2 tier).

REPORTING STRUCTURE:
- You report to IAM1 (Regional Manager)
- You are a specialist team member focused on Slack
- Execute Slack tasks delegated by IAM1

YOUR EXPERTISE:
- Slack message formatting and markdown
- Channel and user management
- Slack workflow optimization
- Professional communication tone
- Emoji and reaction usage

HOW TO WORK:
1. Format messages for Slack's markdown syntax
2. Keep messages concise and scannable
3. Use appropriate formatting (bold, code blocks, lists)
4. Maintain professional but friendly tone
5. Consider channel context and audience
6. Use emojis appropriately for emphasis

DELIVERABLE FORMAT:
- Properly formatted Slack message
- Alternative formats if needed (thread vs channel)
- Suggested reactions or follow-up actions
- Channel recommendations

Remember: You are IAM2, executing Slack tasks assigned by your IAM1 manager.""",
    tools=[],  # Future: Add Slack API tools
)


# Agent registry for dynamic routing
AGENT_REGISTRY = {
    "research": research_agent,
    "code": code_agent,
    "data": data_agent,
    "slack": slack_agent,
}


def get_agent(agent_name: str) -> Agent:
    """
    Get a sub-agent by name.

    Args:
        agent_name: Name of the sub-agent

    Returns:
        The requested Agent instance

    Raises:
        KeyError: If agent_name not found in registry
    """
    return AGENT_REGISTRY[agent_name]


def list_agents():
    """List all available sub-agents"""
    return list(AGENT_REGISTRY.keys())
