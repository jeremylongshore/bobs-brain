# Changelog

All notable changes to the Slack Webhook will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-10

### Added
- Initial release of Slack webhook for Bob's Brain
- Vertex AI Agent Engine integration
- Slack event handling (messages, mentions, DMs)
- Event deduplication cache
- Background thread processing for immediate HTTP 200 response
- Secret Manager integration for secure token storage
- Streaming response support from Agent Engine
- Session-based conversation context

### Security
- No hardcoded secrets (uses Google Secret Manager)
- HTTP 200 immediate acknowledgment to prevent retries
- Event deduplication to prevent duplicate processing
- Bot message filtering to prevent loops

### Infrastructure
- Cloud Functions Gen2 deployment
- Python 3.12 runtime
- Workload Identity Federation (WIF) authentication
- Cloud Logging enabled
- Cloud Trace enabled
