# scripts

Helper scripts and automation utilities for Bob's Brain.

This directory contains:
- Deployment scripts
- Setup and installation scripts
- Data migration utilities
- Development helpers
- **A2A compliance tooling** (a2a-inspector, a2a-tck)

## A2A Compliance Tooling (Developer-Only)

**Purpose:** Local validation and debugging of A2A protocol implementations

**Tools:**
- **run_a2a_inspector_local.md** - Interactive debugger for AgentCard and A2A endpoint validation
- **run_a2a_tck_local.sh** - Automated compliance test suite (Technology Compatibility Kit)

**Status:** Optional developer tools for local validation (not required for CI/CD)

**Usage:**
- See `run_a2a_inspector_local.md` for detailed a2a-inspector usage guide
- Run `./scripts/run_a2a_tck_local.sh` for a2a-tck instructions (requires `A2A_TCK_SUT_URL`)

**Note:** These tools require live A2A endpoints (agents deployed to Agent Engine). They are scaffold-only until we have a dev deployment.

**Documentation:** See `000-docs/6767-121-DR-STND-a2a-compliance-tck-and-inspector.md` for complete standard

---

Updated 2025-11-21.
