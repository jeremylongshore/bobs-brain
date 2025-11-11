# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Slack Integration** - Added missing Cloud Run environment variables (`SLACK_SIGNING_SECRET`, `SLACK_BOT_TOKEN`, `LOCATION`)
  - Bot was not responding due to missing credentials on deployed service
  - Deployed new revision: `slack-webhook-00016-wx6`
  - All events were being marked as duplicates (cache cleared with new revision)

### Added
- **CI/CD Automation** - GitHub Actions workflow for automatic Cloud Run deployments
  - Triggers on push to main (relevant file changes) or manual dispatch
  - Deploys with environment variables from GitHub Secrets
  - Includes endpoint verification testing
  - Posts deployment summary to workflow run
- **Documentation**
  - AAR: Slack Integration Fix (`000-docs/051-AA-REPT-slack-integration-fix.md`)
  - Guide: GitHub Actions Setup (`000-docs/052-OD-GUID-github-actions-setup.md`)

### Changed
- **GitHub Secrets** - Updated all required secrets for automated deployments
  - `SLACK_SIGNING_SECRET` - For webhook signature verification
  - `SLACK_BOT_TOKEN` - For sending bot responses
  - `GCP_WORKLOAD_IDENTITY_PROVIDER` - For Google Cloud authentication
  - `GCP_SERVICE_ACCOUNT` - Service account for deployments
- **README** - Fixed display issue (removed conflicting `.github/README.md`)

## [0.5.1] - 2025-11-11

### Changed
- **Repository Restructure** - Archived legacy implementations to `99-Archive/2025-11-11`
- **Simplified README** - Focused on template/learning resource positioning
- **Cleaned Top-Level** - Removed non-canonical roots for cleaner structure

### Removed
- Archived Flask implementation (`src/`, `02-Src/`, etc.)
- Archived experimental agents (ADK, Genkit, bob-vertex-agent)
- Archived development artifacts (`venv/`, `__pycache__/`, config files)
- Removed `CONTRIBUTING.md` and `Dockerfile` from root

### Documentation
- Night Wrap AAR: Repository cleanup and archival process
- Updated CLAUDE.md with simplified guidance

### Infrastructure
- Enabled auto-delete branches on merge (GitHub repository settings)
- Repository positioned as template/learning resource

## [0.5.0] - 2025-11-10

### Added
- Initial VERSION file
- Keep a Changelog format adoption
- Documentation structure (`000-docs/`)

### Changed
- Repository positioning as template for beginners
- Focus on Slack AI agent starter code

## Earlier Versions

See `99-Archive/` for historical implementations including:
- v4-v5: Flask modular agent with multiple LLM providers
- v2-v3: Vertex AI Agent Engine implementation
- v1: ADK and Genkit experimental versions

---

**Note:** Version 0.5.0 and 0.5.1 represent the "clean slate" repositioning of Bob's Brain as a template/learning resource, with all production implementations archived for reference.
