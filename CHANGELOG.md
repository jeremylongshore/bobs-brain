# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Ongoing improvements to Circle of Life learning system
- Potential additional AI provider support
- Performance optimization for graph database queries
- Enhanced Slack interaction capabilities

## [5.0.0] - 2025-10-05
### Added
- Modular AI agent with pluggable LLM providers (Anthropic, Google, OpenRouter, Ollama)
- Configurable storage backends (state, vector, graph, cache, artifacts)
- Circle of Life learning system
- REST API with authentication
- Prometheus metrics
- Optional Slack integration
- Comprehensive test suite with 65% coverage floor

### Changed
- Refactored from Google-specific to provider-agnostic architecture
- Migrated to modular storage backends
- Updated API endpoints

## [0.1.0] - 2025-08-10
### Added
- Initial Bob's Brain implementation
- Google Gemini integration
- Neo4j graph database
- BigQuery analytics

## Legend
- `Added` for new features
- `Changed` for modifications in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
