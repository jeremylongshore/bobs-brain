# Bob's Brain - Slack AI Agent Template

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Clean, simple template for building Slack AI assistants with knowledge base integration.

## Repo Structure

```
bobs-brain/
├── 000-docs/          # Documentation and AARs
├── docs/              # GitHub Pages site
├── gateway/           # API gateway (placeholder for future)
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── 99-Archive/        # Historical implementations
├── requirements.txt   # Python dependencies
├── Makefile           # Development commands
└── README.md          # This file
```

## What This Is

Bob's Brain is a **template repository** for building custom Slack AI assistants. It provides:

- Clean starter code for Slack integration
- Knowledge base patterns (ChromaDB, vector search)
- Example conversation memory
- LLM provider flexibility (Claude, GPT, Gemini, etc.)
- Testable architecture

**This is a learning template** - fork it, customize it, and build your own agent.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/jeremylongshore/bobs-brain.git
cd bobs-brain

# Install dependencies
pip install -r requirements.txt

# Run tests
make test

# Check available commands
make help
```

## Documentation

See `000-docs/` for:
- Architecture documentation
- Implementation guides
- After-action reports (AARs)
- Operational runbooks

## Archived Implementations

The `99-Archive/` directory contains previous implementations:
- Flask-based modular agent (v5)
- Vertex AI Agent Engine implementation
- ADK (Agent Development Kit) version
- Genkit framework version

These are preserved for reference and learning.

## Development

```bash
# Run tests
make test

# Format code
make fmt

# Run full checks
make check-all
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

This is a personal template repository. Feel free to fork and customize for your own use.

---

**Version:** 0.5.1
**Last Updated:** 2025-11-11
**Status:** Template / Learning Resource
