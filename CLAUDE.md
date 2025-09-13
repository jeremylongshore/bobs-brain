# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bob is a unified AI business partner for DiagnosticPro.io, specializing in vehicle diagnostics, repair industry expertise, and strategic business support. Built with professional Python architecture, Slack integration, and ChromaDB knowledge management with 970+ curated industry knowledge items.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
make test
# or directly:
python -m pytest tests/ -v

# Lint and code quality checks
make lint-check
# Full safety check before commit
make safe-commit

# Test Bob's core functionality (non-interactive)
python3 test_bob.py

# Run Bob interactively
python3 run_bob.py

# Run Bob Slack Bot (production)
python3 run_slack_bot.py
```

### Production Deployment
```bash
# Start Bob Unified v2 (production)
./scripts/start_unified_bob_v2.sh

# Check Bob's status
ps aux | grep bob_unified
tail -f logs/bob_unified_v2.log
```

## Professional Architecture

Bob follows a clean, modular Python package structure:

```
bobs-brain/
├── bob/                    # Main application package
│   ├── agents/            # Agent implementations
│   │   ├── unified_v2.py  # Production Slack bot
│   │   └── basic.py       # Development CLI version
│   ├── core/              # Shared functionality
│   │   ├── config.py      # Configuration management
│   │   ├── knowledge.py   # ChromaDB integration
│   │   └── slack.py       # Slack utilities
│   └── utils/             # Utility functions
├── ai-dev-tasks/          # Development task management system
│   ├── analysis/          # Research and analysis documents
│   ├── templates/         # ADR, llms.txt, and other templates
│   └── PRDs/              # Product requirement documents
├── config/                # Configuration files (.env, templates)
├── data/knowledge_base/   # Knowledge base data
├── tests/                 # Test suite
├── scripts/               # Deployment scripts
├── docker/                # Docker configurations
├── logs/                  # Application logs
└── archive/               # Legacy code (versions/, agent/, src/)
```

### Core Components

- **bob.agents.unified_v2.BobUnifiedV2**: Production Slack bot with enterprise features
  - Duplicate response prevention via message ID tracking
  - Smart conversation memory system
  - Professional business communication patterns
  - ChromaDB integration for knowledge base queries
  - Socket mode for real-time Slack communication

- **bob.agents.basic.BobBasic**: Development CLI version
  - Direct ChromaDB access
  - Command system (status, memory, project)
  - Lightweight for testing and development

- **bob.core.config.BobConfig**: Centralized configuration management
- **bob.core.knowledge.KnowledgeBase**: ChromaDB knowledge base interface
- **bob.core.slack.SlackClient**: Enhanced Slack communication utilities

### Key Design Patterns
- **Clean Architecture**: Separation of concerns with core, agents, and utilities
- **Configuration Management**: Centralized config with environment variables
- **Knowledge Base**: ChromaDB persistent storage at `~/.bob_brain/chroma`
- **Message Deduplication**: Tracks processed message IDs to prevent duplicate responses
- **Context Awareness**: Maintains user context and conversation history
- **Professional Communication**: Different response patterns for Jeremy vs team members

## Configuration

### Environment Variables
Configure in `config/.env` (copy from `config/.env.template`):
- `SLACK_BOT_TOKEN`: xoxb- prefixed bot token
- `SLACK_APP_TOKEN`: xapp- prefixed app token for socket mode
- `CHROMA_PERSIST_DIR`: ChromaDB storage location (defaults to ~/.bob_brain/chroma)
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `BOB_MODE`: development or production

### Slack Integration
Bob uses Socket Mode for real-time messaging, requiring:
- Bot permissions: `app_mentions:read`, `chat:write`, `channels:history`, `im:history`
- Socket Mode enabled with app-level token

## Testing Strategy

- Unit tests go in `agent/tests/`
- Use `test_bob.py` for quick functionality verification
- The Makefile provides safety checks via `make safe-commit`

## Migration Notes

The codebase has been restructured for professional architecture:
- **Archive**: Old code moved to `archive/` (versions/, agent/, src/)
- **New Structure**: Clean Python package in `bob/`
- **Entry Points**: `run_bob.py` (CLI), `run_slack_bot.py` (Slack)
- **Backward Compatibility**: Legacy scripts still work during transition

## Important Notes

- The production script expects specific paths: `/home/jeremylongshore/bob-consolidation`
- ChromaDB knowledge base must exist at `/home/jeremylongshore/.bob_brain/chroma`
- Bob tracks recent messages to prevent duplicates (30-minute cleanup cycle)
- Different greeting patterns for Jeremy (owner) vs other users