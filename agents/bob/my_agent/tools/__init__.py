"""
Bob's Brain - Custom Tools

Add custom tools here to extend agent capabilities.

Tools must follow ADK tool specification (R1).

Example tool structure:
    from google.adk.tools import Tool

    my_tool = Tool(
        name="my_tool_name",
        description="What this tool does",
        parameters={...},  # JSON schema
        func=my_tool_function
    )

Then import in my_agent/agent.py:
    from my_agent.tools import my_tool

    agent = LlmAgent(
        model="gemini-2.0-flash-exp",
        tools=[my_tool],  # Add here
        ...
    )
"""

__all__ = []  # Export tools here as they're added
