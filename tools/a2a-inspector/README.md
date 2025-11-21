# a2a-inspector Integration

This directory contains tooling and documentation for integrating **a2a-inspector** with the bobs-brain repository.

## What is a2a-inspector?

**a2a-inspector** is a web-based debugging tool for A2A (Agent-to-Agent) protocol validation and testing. It provides:

- **AgentCard Discovery**: Load and visualize AgentCards from agents
- **Schema Validation**: Validate skill input/output schemas against JSON Schema
- **Task Simulation**: Test A2A task envelopes before deployment
- **Contract Verification**: Ensure foreman→worker contracts match expectations
- **Live Debugging**: Monitor A2A messages in real-time (future)

**Project Links:**
- Web UI: `https://a2a-inspector.dev` (or self-hosted)
- Documentation: `https://github.com/a2a-protocol/inspector`
- Protocol Spec: `https://a2a-protocol.org/spec`

## Why We Use It

In **department adk iam**, we use a2a-inspector to:

1. **Validate AgentCards** before deployment
   - Catch schema errors early (missing required fields, malformed JSON)
   - Verify skill schemas match shared_contracts.py expectations
   - Ensure SPIFFE IDs are correctly formatted

2. **Test Delegation Patterns** before implementation
   - Simulate foreman→worker task envelopes
   - Validate input data matches skill input_schema
   - Verify output format matches skill output_schema

3. **Debug A2A Issues** in development
   - Inspect actual A2A messages sent between agents
   - Compare expected vs actual payloads
   - Identify contract mismatches

4. **Maintain Quality Gates** in CI
   - Automated AgentCard validation on every commit
   - Block PRs if AgentCards are invalid or out-of-sync
   - Ensure all agents follow 6767 AgentCard standards

## Integration Status

### ✅ Completed

- AgentCards created for iam-senior-adk-devops-lead and iam-adk
- AGENTCARD_PATH constants added to agent.py files
- 6767 standard documents created

### 🟡 In Progress (PHASE 3C)

- [ ] Stub validation script (`scripts/check_a2a_contracts.py`)
- [ ] Makefile target (`make check-a2a-contracts`)
- [ ] CI integration plan documented

### 🔴 Future Work

- [ ] Wire a2a-inspector into local development workflow
- [ ] Add live A2A message capture in Agent Engine
- [ ] Create task simulation playground for testing delegation
- [ ] Integrate with 6767-123 quality gates

## Quick Start

### Validate AgentCards Locally

Once implemented, you'll be able to run:

```bash
# Validate all AgentCards
make check-a2a-contracts

# Validate specific agent
python3 scripts/check_a2a_contracts.py agents/iam-adk/.well-known/agent-card.json

# Validate with implementation cross-check
python3 scripts/check_a2a_contracts.py \
  agents/iam-adk/.well-known/agent-card.json \
  --check-implementation agents/iam_adk/agent.py
```

### Use a2a-inspector Web UI

1. Go to `https://a2a-inspector.dev`
2. Load AgentCard: Click "Load AgentCard" → paste JSON or upload file
3. Validate: Click "Validate Schema" to check compliance
4. Test Task: Create a task envelope and test against skill input_schema
5. Export Report: Download validation report for documentation

### CI Integration

The validation script will be integrated into CI via `.github/workflows/ci.yml`:

```yaml
- name: Validate A2A Contracts
  run: make check-a2a-contracts
```

This ensures:
- All AgentCards are valid JSON
- Required fields are present
- Skill schemas follow 6767 standards
- SPIFFE IDs match version conventions

## Standards Alignment

Our a2a-inspector integration follows these standards:

- **6767-DR-STND-agentcards-and-a2a-contracts.md**: AgentCard structure and skill schemas
- **6767-DR-STND-prompt-design-and-agentcard-standard.md**: Contract-first design principles
- **6767-DR-STND-a2a-inspector-usage.md**: How to use a2a-inspector for validation

## Related Documentation

- `000-docs/6767-DR-STND-agentcards-and-a2a-contracts.md` - AgentCard standard
- `000-docs/6767-DR-STND-a2a-quality-gates.md` - Quality gate requirements
- `scripts/check_a2a_contracts.py` - Validation script (stub)
- `.github/workflows/ci.yml` - CI integration

## Contact

- Questions about a2a-inspector: See project documentation
- Questions about our integration: department-adk-iam team
- Issues with AgentCards: Create GitHub issue with `a2a` label

---

**Last Updated**: 2025-11-20 (PHASE 3C)
**Status**: Stub - validation script not yet implemented
**Next Step**: Complete `scripts/check_a2a_contracts.py` and Makefile target
