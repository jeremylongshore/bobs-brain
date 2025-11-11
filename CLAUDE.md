# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**Bob's Brain** - Template repository for building Slack AI assistants with knowledge base integration.

**Location:** `/home/jeremy/000-projects/iams/bobs-brain/`
**Status:** Template / Learning Resource
**Version:** 0.5.1

---

## Important Context

This repository is a **template/starter kit** for building custom Slack AI agents. It is NOT a production system.

### Multiple Archived Implementations

The `99-Archive/` directory contains **multiple previous implementations**:

1. **99-Archive/2025-11-11/** - Flask app, experimental agents, development artifacts (archived in Night Wrap)
2. **99-Archive/2025-11-10/** - bob-vertex-agent, adk-agent, genkit-agent, Flask modules
3. **99-Archive/02-Src/** - Flask implementation v5 (modular LLM providers)
4. **99-Archive/03-Tests/** - Flask test suite
5. **Historical implementations** - See archive README files for details

**When working on Bob's Brain, focus on the ROOT directory structure unless specifically asked about archived implementations.**

---

## Current Structure

```
bobs-brain/
├── 000-docs/          # Documentation, AARs, runbooks
├── docs/              # GitHub Pages site
├── gateway/           # API gateway (placeholder)
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── 99-Archive/        # All archived implementations
├── requirements.txt   # Python dependencies
├── Makefile           # Development commands
├── CHANGELOG.md       # Version history
├── CLAUDE.md          # This file
├── LICENSE            # MIT License
└── README.md          # Project overview
```

---

## Ground Rules

1. **This is a template** - Not a production system
2. **Archived code** - Do NOT modify files in `99-Archive/`
3. **Documentation** - All new docs go in `000-docs/`
4. **Version tracking** - Update `VERSION` file and `CHANGELOG.md`
5. **Keep it simple** - This is a learning resource

---

## Common Commands

```bash
# Development
make test              # Run test suite
make fmt               # Format code
make check-all         # Run all quality checks

# Documentation
ls 000-docs/           # View available documentation
cat CHANGELOG.md       # View version history
```

---

## Documentation Standards

All documentation follows **Document Filing System v2.0**:

**Format:** `NNN-CC-ABCD-description.md`
- **NNN** = Sequential number (001-999)
- **CC** = Category code (PP, AT, AA, etc.)
- **ABCD** = Document type (4-letter abbreviation)
- **description** = 1-4 words, kebab-case

**Example:** `001-AA-REPT-night-wrap-2025-11-11.md`

---

## Key Files

- `README.md` - Project overview (above-the-fold)
- `CHANGELOG.md` - Version history (Keep a Changelog format)
- `VERSION` - Current version number (semver)
- `requirements.txt` - Python dependencies
- `Makefile` - Development automation
- `000-docs/` - All documentation and AARs

---

## Archived Implementations

If asked about specific archived implementations:

1. **Flask Modular Agent (v5)** - See `99-Archive/2025-11-11/src/` or `99-Archive/02-Src/`
2. **Vertex AI Agent Engine** - See `99-Archive/2025-11-10/2025-11-10-bob-vertex-agent/`
3. **ADK Implementation** - See `99-Archive/2025-11-10/2025-11-10-adk-agent/`
4. **Genkit Implementation** - See `99-Archive/2025-11-10/2025-11-10-genkit-agent/`

Each has its own README with implementation details.

---

## Development Workflow

1. **Make changes** - Edit code or documentation
2. **Test** - Run `make test` to validate
3. **Format** - Run `make fmt` for consistent style
4. **Document** - Create AAR in `000-docs/` if significant
5. **Version** - Update `VERSION` and `CHANGELOG.md`
6. **Commit** - Use conventional commit messages

---

## Version History

- **v0.5.1** (2025-11-11) - Night Wrap: Repository cleanup and archival
- **v0.5.0** (2025-11-10) - Template repositioning, documentation structure
- **Earlier** - See `99-Archive/` for historical implementations

---

## Support

This is a personal template repository. For questions or issues:
1. Check `000-docs/` for existing documentation
2. Review `CHANGELOG.md` for version history
3. Explore `99-Archive/` for implementation examples

---

**Last Updated:** 2025-11-11
**Version:** 0.5.1
**Status:** Template / Learning Resource