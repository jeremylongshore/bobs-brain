# PRD-001: Bob v1 - Simple Slack Bot Template

**Date**: 2025-09-13
**Status**: Implemented
**Branch**: main

## Introduction/Overview

Bob v1 is a beginner-friendly Slack bot template that provides a foundation for developers new to AI assistants. This version serves as an entry point for creating a basic Slack bot with minimal setup requirements and clear, understandable code structure.

## Goals

1. Provide a working Slack bot in under 5 minutes of setup
2. Demonstrate basic message handling and response patterns
3. Offer a clean codebase that beginners can understand and modify
4. Include essential features like duplicate prevention and memory management
5. Support both Socket Mode and HTTP deployment modes

## User Stories

- As a **developer new to Slack bots**, I want to quickly set up a working bot so that I can start experimenting with AI assistants
- As a **team lead**, I want a simple bot template so that my team can build custom automation tools
- As a **hobbyist**, I want readable code with clear documentation so that I can learn how Slack bots work
- As a **Jeremy (the owner)**, I want the bot to recognize me and provide personalized responses

## Functional Requirements

Based on verified code in main branch:

1. **Slack Integration**
   - 1.1 Support Socket Mode for local development
   - 1.2 Support HTTP webhooks for production deployment
   - 1.3 Handle direct messages and channel mentions
   - 1.4 Process events with proper error handling

2. **Message Processing**
   - 2.1 Prevent duplicate message processing
   - 2.2 Maintain conversation history (10 messages per user)
   - 2.3 Thread-aware responses
   - 2.4 Professional business communication style

3. **AI Capabilities**
   - 3.1 Integration with Vertex AI (Gemini 2.0)
   - 3.2 Fallback to Google GenAI SDK
   - 3.3 Knowledge base query via ChromaDB
   - 3.4 Offline mode with knowledge-base only responses

4. **Data Storage**
   - 4.1 ChromaDB vector database for knowledge storage
   - 4.2 Local persistence at `/home/jeremylongshore/bobs-brain/chroma_data`
   - 4.3 Semantic search capabilities
   - 4.4 Knowledge loader for DiagnosticPro content

5. **Special Features**
   - 5.1 Jeremy recognition (knows the owner)
   - 5.2 Health checks for Cloud Run deployment
   - 5.3 Smart memory management
   - 5.4 Thread safety for concurrent operations

## Non-Goals (Out of Scope)

- Complex multi-system integration
- Graph database functionality
- Entity extraction
- Production scraping capabilities
- Advanced learning systems
- BigQuery analytics

## Technical Considerations

**Verified Files in main branch:**
- `src/bob_brain_v5.py` - Main service implementation
- `src/circle_of_life.py` - Learning module (basic)
- `src/forum_scraper.py` - Simple scraping examples
- ChromaDB integration for vector storage
- Flask server for HTTP mode

**Dependencies (from requirements.txt):**
- slack-bolt==1.18.0
- slack-sdk==3.31.0
- chromadb==0.5.0
- google-cloud-aiplatform==1.38.0
- vertexai
- python-dotenv==1.0.0

## Success Metrics

- Setup time < 5 minutes
- First message response < 2 seconds
- Zero configuration errors for new users
- 100% uptime in Socket Mode
- Clear documentation rating > 4/5

## Implementation Status

✅ **FULLY IMPLEMENTED** - Available in main branch
- All core features working
- Documentation complete
- Ready for immediate use

## Open Questions

None - This is a completed, production-ready template.

---

**Note**: This PRD documents the actual implemented features verified in the main branch codebase.