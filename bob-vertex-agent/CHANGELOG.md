# Changelog

All notable changes to Bob's Brain will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-10

### Fixed
- Fixed Slack webhook to use correct `stream_query()` method for ADK agents
- Resolved "Default method 'query' not found" error
- Added proper streaming response handling

### Changed
- Migrated from `async_stream_query()` to `stream_query()` (correct ADK method)
- Removed async/asyncio dependencies (not needed)
- Added detailed event logging for debugging
- Enhanced error logging with stack traces

### Added
- Session management for conversation context (per-user-per-channel)
- Comprehensive GitHub Actions workflow for automated deployment
- Version tracking with VERSION file
- This CHANGELOG

## [0.1.0] - 2025-11-09

### Added
- Initial Vertex AI Agent Engine deployment
- Slack integration via Cloud Functions Gen2
- IAM1 Regional Manager (Bob) with 4 IAM2 specialists
- RAG system with Vertex AI Search
- A2A Protocol for peer coordination
- Cloud Logging and Trace integration
