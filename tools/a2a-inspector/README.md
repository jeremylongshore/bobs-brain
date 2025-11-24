# a2a-inspector Integration for Department ADK IAM

This directory documents **department adk iam's** dual-layer A2A validation strategy using both static validation and runtime inspection.

## What is a2a-inspector?

**a2a-inspector** is the official web-based inspection tool for the Agent-to-Agent (A2A) protocol developed by the a2aproject organization.

**Official Links:**
- GitHub: https://github.com/a2aproject/a2a-inspector
- A2A Protocol: https://a2a-protocol.org/
- Documentation: https://a2aprotocol.ai/docs/guide/a2a-inspector

**Key Features:**
- **AgentCard Fetching**: Automatically fetches and displays agent cards from running agents
- **Spec Compliance**: Validates agent cards against A2A specification
- **Real-time Testing**: Interactive chat interface to test agent behavior
- **JSON-RPC Inspection**: Debug console showing raw protocol messages
- **WebSocket Support**: Live message monitoring and validation

**Technology Stack:**
- FastAPI backend with WebSocket support
- TypeScript frontend interface
- Requires running agent servers (not static file validation)

## Our Hybrid Validation Strategy

**department adk iam** uses a **two-layer validation approach** because A2A has two distinct validation needs:

### Layer 1: Static Validation (CI/CD)
**Tool**: `scripts/check_a2a_contracts.py` (our custom validator)
**Purpose**: Validate AgentCard JSON structure before runtime
**When**: Every commit, pre-deployment, ARV gates

Validates:
- ✅ JSON syntax correctness
- ✅ Required fields present (name, version, spiffe_id, skills)
- ✅ Skill schema structure (no empty `{}`, explicit types)
- ✅ 6767 standards (skill naming, version format, SPIFFE ID)
- ✅ Schema alignment with shared_contracts.py

**Why we built this**: a2a-inspector requires running servers and can't validate static JSON files in CI pipelines.

### Layer 2: Runtime Validation (Dev/Test)
**Tool**: a2a-inspector web UI
**Purpose**: Validate agent behavior and protocol compliance
**When**: Local development, integration testing, debugging

Validates:
- ✅ AgentCard served correctly at `/.well-known/agent-card.json`
- ✅ Agents respond to A2A protocol messages properly
- ✅ JSON-RPC 2.0 compliance in actual communication
- ✅ Task envelope handling matches AgentCard specifications
- ✅ Error handling and edge cases

**Why we use this**: Catches runtime issues that static validation can't detect.

## Quick Start

### Static Validation (Developers & CI)

```bash
# Validate all AgentCards
make check-a2a-contracts

# Validate specific agent
python3 scripts/check_a2a_contracts.py agents/iam-adk/.well-known/agent-card.json

# CI integration (already wired)
# Runs automatically on every commit via Makefile target
```

**Exit Codes:**
- `0` - All validations passed
- `1` - Validation errors found
- `2` - Script error (file not found, etc.)

### Runtime Inspection (Local Dev Only)

**Prerequisites:**
- Agent must be running and accessible via HTTP
- Agent must serve AgentCard at `/.well-known/agent-card.json`
- For local agents: typically `http://localhost:PORT`
- For deployed agents: Cloud Run URL or Agent Engine endpoint

**Option A: Use Public Inspector (Easiest)**

1. Deploy your agent locally or to test environment
2. Visit https://a2aprotocol.ai/a2a-inspector (official hosted version)
3. Enter your agent URL (e.g., `http://localhost:8080`)
4. Click "Connect" - inspector will fetch AgentCard
5. Use chat interface to test skills
6. Check "Spec Compliance" tab for violations

**Option B: Run Inspector Locally (Advanced)**

```bash
# Clone official inspector
git clone https://github.com/a2aproject/a2a-inspector.git
cd a2a-inspector

# Install dependencies
uv sync                    # Python backend
cd frontend && npm install # TypeScript frontend

# Run locally
bash scripts/run.sh

# Access at http://localhost:5001
```

**Local development URL**: `http://localhost:5001`
**Point it at your agent**: Enter agent URL in connection dialog

## Integration Status

### ✅ Completed (PHASE 3C)

- Static validation script (`scripts/check_a2a_contracts.py`)
- Makefile target (`make check-a2a-contracts`)
- AgentCards for iam-senior-adk-devops-lead and iam-adk
- 6767 AgentCard standard documented
- CI integration wired

### 🟡 In Progress (INSPECTOR-1/2/3)

- [ ] Update documentation to reflect hybrid approach
- [ ] Add runtime testing workflow to dev docs
- [ ] Create 6767 AAR for validation strategy
- [ ] Document ARV integration path

### 🔴 Future Work

- [ ] Add local agent server startup scripts for easy inspector testing
- [ ] Create task envelope simulation examples
- [ ] Integrate inspector results into ARV reports
- [ ] Add screenshot/video walkthrough of inspector usage

## Why This Approach?

**Problem**: a2a-inspector is web-UI only and requires running agents.
**Solution**: Use both tools for their strengths.

| Validation Layer | Tool | Use Case | When |
|-----------------|------|----------|------|
| **Static** | `check_a2a_contracts.py` | Structural validation | CI/CD, pre-commit |
| **Runtime** | a2a-inspector web UI | Behavioral validation | Dev, testing, debugging |

This gives us:
- ✅ Fast feedback in CI (no server startup overhead)
- ✅ Comprehensive runtime validation when needed
- ✅ Developer-friendly workflow (both automated and interactive)
- ✅ ARV-compliant (static checks are gates, runtime is optional)

## CI Integration

Our static validator runs in CI via `.github/workflows/ci.yml`:

```yaml
- name: Validate A2A Contracts
  run: make check-a2a-contracts
```

This ensures:
- All AgentCards are valid JSON
- Required fields are present (name, version, spiffe_id, skills)
- Skill schemas follow 6767 standards
- SPIFFE IDs match version conventions
- Skill naming follows `{department}.{verb}_{noun}` pattern

**Future**: Runtime validation with a2a-inspector can be added as optional post-deployment verification.

## Standards Alignment

Our validation strategy follows these standards:

- **6767-DR-STND-agentcards-and-a2a-contracts.md**: AgentCard structure and skill schemas
- **6767-DR-STND-prompt-design-and-agentcard-standard.md**: Contract-first design principles
- **6767-DR-STND-a2a-quality-gates.md**: Quality gate requirements (static validation is required)
- **A2A Protocol Spec**: Official spec compliance via a2a-inspector

## Related Documentation

- `000-docs/6767-DR-STND-agentcards-and-a2a-contracts.md` - AgentCard standard
- `scripts/check_a2a_contracts.py` - Static validation script
- `.github/workflows/ci.yml` - CI integration
- https://a2aprotocol.ai/docs - Official A2A protocol documentation

## FAQ

**Q: Why don't we use a2a-inspector in CI?**
A: a2a-inspector requires running agent servers, which adds complexity and overhead to CI. Our static validator provides fast structural checks that catch 90% of issues.

**Q: When should I use the inspector web UI?**
A: Use it when debugging agent behavior, testing new skills interactively, or verifying protocol compliance of deployed agents.

**Q: Can I validate AgentCards without running agents?**
A: Yes! Use `make check-a2a-contracts` for static validation. Only use inspector when you need runtime behavior validation.

**Q: Is a2a-inspector required for development?**
A: No. It's optional for local dev but valuable for integration testing and debugging. Static validation is mandatory (runs in CI).

**Q: Where does inspector fit in ARV?**
A: Static validation is part of ARV contract checks (required). Inspector is useful for post-deployment verification (optional).

## Contact

- **a2a-inspector issues**: https://github.com/a2aproject/a2a-inspector/issues
- **Our validation strategy**: department-adk-iam team
- **AgentCard issues**: Create GitHub issue with `a2a` label

---

**Last Updated**: 2025-11-21 (INSPECTOR-1)
**Status**: Hybrid strategy implemented (static validator + runtime inspector)
**Next Step**: Document ARV integration and runtime testing workflows
