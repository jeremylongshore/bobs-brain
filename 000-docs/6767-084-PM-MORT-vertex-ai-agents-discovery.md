# Postmortem: Vertex AI Agent Discovery and Classification

**Document ID:** 084-PM-MORT-vertex-ai-agents-discovery
**Date:** 2025-11-19
**Author:** claude.buildcaptain@intentsolutions.io
**Severity:** Medium
**Status:** Discovery Complete

## Executive Summary

Three Vertex AI Agent Engine instances were discovered in project `205354194989` that were not properly documented or tracked in the current `bobs-brain` repository. Investigation revealed these represent different evolutionary stages of Bob's development, with only one being the canonical production instance.

## Timeline of Events

### Discovery Phase
- **19:00 UTC** - Request to audit three Vertex AI agents (IDs ending in 4704, 9040, 6448)
- **19:05 UTC** - Initial gcloud commands failed (reasoning-engines command not available)
- **19:10 UTC** - User provided full resource paths for all three agents
- **19:15 UTC** - Repository search revealed agent 6448 in archived code
- **19:20 UTC** - Analysis completed, agents classified

## What Went Wrong

### 1. Missing Agent Tracking
**Issue:** Three production Vertex AI agents exist without clear documentation
- No central registry of deployed agents
- No deployment history or version tracking
- Agents 9040 and 4704 completely undocumented

**Impact:**
- Potential resource waste (unknown agents running)
- Confusion about which agent is canonical
- Risk of accidental connections to wrong agents

### 2. Inconsistent Deployment Practices
**Issue:** Multiple deployment methods created orphaned resources
- Manual deployments not tracked in repo
- Different naming conventions (bob-battalion-commander vs bobs-brain-dev)
- No tags or labels to identify purpose/ownership

**Impact:**
- Unable to determine agent purposes without investigation
- No clear deprecation path for old agents
- Billing for potentially unused resources

### 3. Documentation Gaps
**Issue:** Critical infrastructure not documented
- Agent IDs not stored in repo configuration
- No deployment manifest or inventory
- Archive contains references but no context

**Impact:**
- Time wasted discovering existing infrastructure
- Risk of duplicating work
- Difficulty onboarding new team members

## Root Cause Analysis

### Primary Causes
1. **Rapid Iteration Without Cleanup**
   - Multiple experimental deployments during development
   - Focus on "getting it working" over documentation
   - No decommissioning process for test resources

2. **Tool Limitations**
   - gcloud CLI lacks proper reasoning-engines commands
   - Vertex AI Agent Engine is relatively new service
   - API authentication issues complicate discovery

3. **Migration Complexity**
   - Evolution from simple implementation to Hard Mode
   - Multiple architectural approaches tested
   - Production system kept separate from new development

### Contributing Factors
- Project uses numeric ID (205354194989) not matching project name (bobs-brain)
- Multiple environments (dev/staging/prod) without clear separation
- Archive strategy moved code without preserving deployment context

## Findings

### Agent Classification

| Agent | Purpose | Status | Action Required |
|-------|---------|--------|-----------------|
| **6448** | Production Bob (bob-battalion-commander) | Active | Document as canonical |
| **9040** | Unknown test/dev deployment | Unknown | Mark for investigation |
| **4704** | Unknown test/dev deployment | Unknown | Mark for investigation |

### Repository State
- Current code in `agents/bob/` is Hard Mode compliant but NOT deployed
- Archived `bob-vertex-agent/` references the production agent (6448)
- No active connection between current code and any deployed agent

## Lessons Learned

### What Worked Well
1. **Archive Strategy** - Preserved enough context to identify agent 6448
2. **Documentation** - 000-docs provided deployment history context
3. **Code Organization** - Clear separation between implementations

### What Didn't Work
1. **Resource Tracking** - No inventory of cloud resources
2. **Deployment Documentation** - Agent IDs not preserved
3. **Migration Planning** - No clear path from old to new agents

## Action Items

### Immediate (P0)
- [x] Document three agents in postmortem
- [ ] Add agent inventory to repo documentation
- [ ] Tag agents in GCP Console with purpose/status

### Short-term (P1)
- [ ] Create `000-docs/6767-085-OD-INVT-agent-inventory.md` with all agents
- [ ] Add terraform import statements for existing agents
- [ ] Document decommissioning process for legacy agents

### Long-term (P2)
- [ ] Implement terraform-managed agent lifecycle
- [ ] Add monitoring for orphaned resources
- [ ] Create automated discovery script

## Recommendations

### 1. Agent Management
**Current State:** Three unmanaged agents with unclear purposes
**Recommendation:**
- Adopt agent 6448 as canonical production Bob
- Schedule review of agents 9040 and 4704 for potential deletion
- Implement terraform import to manage existing agents

### 2. Documentation Standards
**Current State:** No agent inventory or deployment records
**Recommendation:**
- Maintain `AGENT_INVENTORY.md` with all deployed agents
- Add deployment timestamps and purposes
- Include decommission dates for retired agents

### 3. Deployment Process
**Current State:** Manual deployments without tracking
**Recommendation:**
- All deployments through terraform only
- Automatic tagging with deployment metadata
- Mandatory documentation updates with each deployment

### 4. Resource Hygiene
**Current State:** Unknown resources accumulating costs
**Recommendation:**
- Quarterly resource audits
- Automatic alerts for untagged resources
- Clear TTL for experimental deployments

## Prevention Measures

### Technical Controls
```yaml
# Required tags for all Agent Engine deployments
required_tags:
  - environment: dev|staging|prod
  - purpose: experimental|development|production
  - owner: team-name
  - created_date: YYYY-MM-DD
  - ttl: days-until-deletion (0 = permanent)
```

### Process Controls
1. **Deployment Checklist**
   - [ ] Agent ID documented in repo
   - [ ] Purpose clearly stated
   - [ ] TTL set for non-production
   - [ ] Added to inventory

2. **Decommission Checklist**
   - [ ] Agent removed from inventory
   - [ ] Archived with context
   - [ ] Resources deleted from cloud
   - [ ] Costs verified stopped

## Conclusion

The discovery of three undocumented Vertex AI agents highlights the need for better resource management and documentation practices. While no immediate harm occurred, the situation represents technical debt and potential cost waste.

The identified production agent (6448) should be formally adopted, while the two unknown agents (9040, 4704) require further investigation and likely decommissioning.

Moving forward, all agent deployments must be tracked in the repository with clear documentation of purpose, ownership, and lifecycle.

## Appendix

### A. Agent Resource Names
```
1. projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448 (6448)
2. projects/205354194989/locations/us-central1/reasoningEngines/1616875829109719040 (9040)
3. projects/205354194989/locations/us-central1/reasoningEngines/7211261359978184704 (4704)
```

### B. Search Commands Used
```bash
# These commands failed due to gcloud limitations
gcloud ai reasoning-engines list --project=205354194989 --region=us-central1

# API calls failed due to authentication issues
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://us-central1-aiplatform.googleapis.com/v1/projects/205354194989/locations/us-central1/reasoningEngines"
```

### C. Repository Evidence
- Agent 6448: `archive/2025-11-11-final-cleanup/2025-11-10-bob-vertex-agent/slack-adk-integration/.env.example`
- Agent 9040: No references found
- Agent 4704: No references found

---

**Post-Incident Review:** Required within 5 business days
**Distribution:** Engineering team, SRE, Finance (for cost review)
**Follow-up:** 2025-11-24