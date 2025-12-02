# Running a2a-inspector Locally (Developer Guide)

**Purpose:** Interactive validation and debugging of A2A protocol implementations using a2a-inspector.

**Status:** Optional developer tool for local validation (not required for CI/CD)

---

## Prerequisites

1. **Clone a2a-inspector repository:**
   ```bash
   # Clone outside this repository (e.g., in ~/tools/ or ~/dev/)
   git clone https://github.com/a2aproject/a2a-inspector.git
   cd a2a-inspector
   ```

2. **Install dependencies:**
   ```bash
   # Follow installation instructions from a2a-inspector README
   # Typically involves npm/yarn install or pip install
   # Example (check official docs for current instructions):
   npm install
   ```

3. **Verify installation:**
   ```bash
   # Run a2a-inspector help to confirm installation
   ./bin/a2a-inspector --help
   ```

---

## Usage Scenarios

### Scenario 1: Validate AgentCard JSON Files

**Goal:** Inspect AgentCard JSON schemas before committing

**Steps:**
1. Navigate to your bobs-brain repo
2. Point a2a-inspector at an AgentCard file:
   ```bash
   # Example: Validate bob's AgentCard
   ~/tools/a2a-inspector/bin/a2a-inspector validate \
     --agentcard agents/bob/.well-known/agent-card.json
   ```

3. Review validation output:
   - Schema compliance (valid JSON, required fields)
   - SPIFFE ID format
   - Skill definitions (input/output schemas)

4. Fix any issues discovered and re-validate

---

### Scenario 2: Test A2A Endpoints (After Deployment)

**Goal:** Interactively test A2A endpoints once agents are deployed to Agent Engine

**Prerequisites:**
- At least one agent deployed to Agent Engine dev environment
- A2A endpoint URL accessible for testing (e.g., `https://dev-bob-a2a.example.com`)

**Steps:**
1. Start a2a-inspector in interactive mode:
   ```bash
   ~/tools/a2a-inspector/bin/a2a-inspector interactive \
     --endpoint https://dev-bob-a2a.example.com
   ```

2. Interactively test A2A operations:
   - Submit task requests
   - Check task status
   - Retrieve task results
   - Test session management

3. Debug any protocol issues discovered:
   - Authentication failures
   - Malformed task payloads
   - Status transition errors

---

### Scenario 3: Test Foreman → Worker Delegation

**Goal:** Validate A2A delegation flows between foreman and worker agents

**Prerequisites:**
- Foreman agent deployed (iam-senior-adk-devops-lead)
- At least one worker agent deployed (e.g., iam-adk)
- Both agents have valid AgentCards

**Steps:**
1. Point a2a-inspector at foreman A2A endpoint:
   ```bash
   ~/tools/a2a-inspector/bin/a2a-inspector interactive \
     --endpoint https://dev-iam-foreman-a2a.example.com
   ```

2. Submit a task that triggers delegation:
   ```json
   {
     "task_type": "pipeline_request",
     "input": {
       "repository": "example-repo",
       "issue_url": "https://github.com/example/repo/issues/123"
     }
   }
   ```

3. Monitor delegation flow:
   - Foreman accepts task
   - Foreman delegates to appropriate worker (e.g., iam-adk)
   - Worker processes task
   - Foreman aggregates results
   - Task marked complete

4. Debug delegation issues:
   - Worker selection logic
   - Task routing
   - Result aggregation

---

## Common Use Cases

**Before Committing AgentCard Changes:**
```bash
# Validate AgentCard JSON schema
~/tools/a2a-inspector/bin/a2a-inspector validate \
  --agentcard agents/YOUR_AGENT/.well-known/agent-card.json
```

**Testing New A2A Skills:**
```bash
# Interactively test new skill definitions
~/tools/a2a-inspector/bin/a2a-inspector interactive \
  --endpoint https://dev-YOUR-AGENT-a2a.example.com \
  --skill YOUR_SKILL_NAME
```

**Debugging A2A Protocol Issues:**
```bash
# Run with verbose logging
~/tools/a2a-inspector/bin/a2a-inspector interactive \
  --endpoint https://dev-YOUR-AGENT-a2a.example.com \
  --verbose \
  --log-file a2a_debug.log
```

---

## Configuration

**Environment Variables:**
- `A2A_INSPECTOR_ENDPOINT` - Default A2A endpoint URL (optional)
- `A2A_INSPECTOR_AUTH_TOKEN` - Authentication token for A2A endpoints (optional)
- `A2A_INSPECTOR_LOG_LEVEL` - Logging verbosity (debug, info, warn, error)

**Example .env Configuration:**
```bash
# Optional: Set default endpoint for a2a-inspector
export A2A_INSPECTOR_ENDPOINT=https://dev-bob-a2a.example.com
export A2A_INSPECTOR_LOG_LEVEL=debug
```

---

## Troubleshooting

**Issue:** a2a-inspector not found
- **Solution:** Ensure you cloned the repository and followed installation instructions
- **Check:** `which a2a-inspector` or verify path to `./bin/a2a-inspector`

**Issue:** AgentCard validation fails with "Invalid JSON"
- **Solution:** Run `jq . agents/YOUR_AGENT/.well-known/agent-card.json` to validate JSON syntax
- **Fix:** Correct JSON syntax errors and re-validate

**Issue:** Cannot connect to A2A endpoint
- **Solution:** Verify endpoint URL and network connectivity
- **Check:** `curl -I https://dev-YOUR-AGENT-a2a.example.com` to test connectivity

**Issue:** Authentication failures
- **Solution:** Ensure `A2A_INSPECTOR_AUTH_TOKEN` is set correctly
- **Check:** Verify API key or OAuth token has correct permissions

---

## Integration with bobs-brain Workflow

**Step 1: Local Development**
- Develop AgentCard JSON files (`agents/*/. well-known/agent-card.json`)
- Validate with a2a-inspector before committing

**Step 2: Pre-Commit Validation**
- Run `a2a-inspector validate` as part of local checks
- Fix any validation errors discovered

**Step 3: Post-Deployment Testing (Future)**
- Deploy agents to Agent Engine dev environment
- Use a2a-inspector to interactively test A2A endpoints
- Validate delegation flows between foreman and workers

**Step 4: Automated Compliance (Future)**
- Transition to a2a-tck for automated compliance checks in CI
- See `scripts/run_a2a_tck_local.sh` and `.github/workflows/a2a-compliance.yml`

---

## References

**a2a-inspector Documentation:**
- GitHub: https://github.com/a2aproject/a2a-inspector
- Official Docs: See repository README for latest usage instructions

**A2A Protocol Specification:**
- Specification: https://a2a-protocol.org/latest/specification/
- Definitions: https://a2a-protocol.org/latest/definitions/

**Related bobs-brain Documentation:**
- Standard: `000-docs/6767-121-DR-STND-a2a-compliance-tck-and-inspector.md`
- AgentCard Contracts: `000-docs/6767-DR-STND-agentcards-and-a2a-contracts.md`
- Master Index: `000-docs/6767-120-DR-STND-agent-engine-a2a-and-inline-deploy-index.md`

---

**Last Updated:** 2025-11-21
**Status:** Developer guide for optional local validation
**Next Steps:** Deploy agents to Agent Engine, then test with a2a-inspector
