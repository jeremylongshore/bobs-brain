# Changelog

All notable changes to Bob's Brain will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2025-11-10

### Fixed
- **ARCHITECTURE CORRECTION**: Verified Agent Engine deployment with proper ADK architecture
- Confirmed `slack-adk-integration` was incorrect (local ADK Runner in Cloud Run)
- Validated correct architecture: Cloud Function → Agent Engine REST API

### Added
- Redeployed agent to Vertex AI Agent Engine (`make deploy`)
- Complete deployment verification with direct Agent Engine testing
- Deployment verification report: `DEPLOYMENT-VERIFICATION-2025-11-10.md`
- Agent Engine playground link for manual testing

### Verified
- ✅ Agent Engine responds correctly to REST API queries
- ✅ Slack webhook (Cloud Function) deployed and healthy
- ✅ Memory Bank and Session Service connected to Agent Engine
- ✅ Full Agent Engine features available (managed runtime, auto-scaling, observability)

### Technical Details
- Agent Engine ID: `projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448`
- Slack Webhook URL: `https://slack-webhook-eow2wytafa-uc.a.run.app`
- Deployment timestamp: 2025-11-10 21:39:51 UTC
- Service Account: `service-205354194989@gcp-sa-aiplatform-re.iam.gserviceaccount.com`

## [0.3.0] - 2025-11-10

### Fixed
- **CRITICAL FIX**: Switched Slack webhook from SDK to REST API to resolve "stream_query() not found" errors
- Fixed "Invalid Session resource name" crashes by removing session_id parameter
- Fixed response parsing to correctly extract text from `content.parts[].text` structure
- Resolved silent failures in Cloud Functions environment

### Changed
- Migrated from Vertex AI SDK to direct REST API calls for Agent Engine queries
- Removed session management (let ADK handle session creation automatically)
- Improved error handling with specific timeout and connection error messages
- Enhanced logging for debugging streaming responses

### Added
- `requests==2.31.0` dependency for REST API calls
- Comprehensive After-Action Report (AAR) in `claudes-docs/reports/`
- Solution guide for Agent Engine query methods in `claudes-docs/`
- Systematic debug protocol with Taskwarrior tracking

### Technical Details
- Cloud Function revision: `slack-webhook-00011-pab`
- Deployment: 2025-11-10 18:30:29 UTC
- Agent Engine ID: `5828234061910376448`
- Fix verified with local testing before production deployment

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
