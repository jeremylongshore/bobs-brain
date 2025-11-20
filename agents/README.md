# Agents Directory

This directory contains all agent implementations for the Bob's Brain agent factory.

## Structure

```
agents/
├── bob/          # Orchestrator agent (user-facing via Slack)
├── iam-adk/      # ADK specialist (backend A2A worker)
└── [future agents...]
```

## Adding New Agents

Each agent should follow the canonical structure:
- `agent.py` - Agent implementation with `get_agent()` and `create_runner()`
- `tools/` - Custom tool implementations
- `a2a_card.py` - AgentCard for A2A protocol
- `system-prompt.md` - Agent instructions

See `templates/` for scaffolding templates.
