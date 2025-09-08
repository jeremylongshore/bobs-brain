# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bob is a unified AI business partner for DiagnosticPro.io, specializing in vehicle diagnostics, repair industry expertise, and strategic business support. The system integrates with Slack and uses ChromaDB for knowledge management with 970+ curated industry knowledge items.

## Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
make test
# or directly:
python -m pytest agent/tests/ -v

# Lint and code quality checks
make lint-check
# Full safety check before commit
make safe-commit

# Test Bob's core functionality (non-interactive)
python3 test_bob.py

# Run Bob interactively
python3 run_bob.py
```

### Production Deployment
```bash
# Start Bob Unified v2 (production)
./scripts/start_unified_bob_v2.sh

# Check Bob's status
ps aux | grep bob_unified
tail -f logs/bob_unified_v2.log
```

## Architecture

The codebase follows a modular structure with two main Bob implementations:

### Core Components
- **src/bob_unified_v2.py**: Production Slack bot with enterprise features
  - Duplicate response prevention via message ID tracking
  - Smart conversation memory system
  - Professional business communication patterns
  - ChromaDB integration for knowledge base queries
  - Socket mode for real-time Slack communication

- **agent/bob_clean.py**: Local development version with simplified interface
  - Direct ChromaDB access
  - Command system (status, memory, project)
  - No external dependencies beyond ChromaDB

### Key Design Patterns
- **Knowledge Base**: ChromaDB persistent storage at `~/.bob_brain/chroma`
- **Message Deduplication**: Tracks processed message IDs to prevent duplicate responses
- **Context Awareness**: Maintains user context and conversation history
- **Professional Communication**: Different response patterns for Jeremy vs team members

## Configuration

### Environment Variables
The system expects these in `.env` or loaded from backup:
- `SLACK_BOT_TOKEN`: xoxb- prefixed bot token
- `SLACK_APP_TOKEN`: xapp- prefixed app token for socket mode
- `CHROMA_PERSIST_DIR`: ChromaDB storage location (defaults to ~/.bob_brain/chroma)

### Slack Integration
Bob uses Socket Mode for real-time messaging, requiring:
- Bot permissions: `app_mentions:read`, `chat:write`, `channels:history`, `im:history`
- Socket Mode enabled with app-level token

## Testing Strategy

- Unit tests go in `agent/tests/`
- Use `test_bob.py` for quick functionality verification
- The Makefile provides safety checks via `make safe-commit`

## Important Notes

- The production script expects specific paths: `/home/jeremylongshore/bob-consolidation`
- ChromaDB knowledge base must exist at `/home/jeremylongshore/.bob_brain/chroma`
- Bob tracks recent messages to prevent duplicates (30-minute cleanup cycle)
- Different greeting patterns for Jeremy (owner) vs other users