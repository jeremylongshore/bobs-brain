# Vertex AI Agent Engine Inventory

**Document ID:** 085-OD-INVT-vertex-agent-inventory
**Date:** 2025-11-19
**Author:** claude.buildcaptain@intentsolutions.io
**Category:** Operations & Deployment - Inventory
**Status:** Active

## Overview

This is the canonical inventory of Vertex AI Agent Engine instances (reasoning engines) related to the `bobs-brain` repository and project. This inventory tracks all deployed agents, their purposes, and their relationship to the codebase.

## Agents

| Full Resource Name | Last 4 | Display Name | Purpose | Status | Repo Reference |
|-------------------|--------|--------------|---------|--------|----------------|
| `projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448` | 6448 | bob-battalion-commander | Production Bob | `canonical_production_bob` | `archive/2025-11-11-final-cleanup/2025-11-10-bob-vertex-agent/slack-adk-integration/.env.example` |
| `projects/205354194989/locations/us-central1/reasoningEngines/1616875829109719040` | 9040 | Unknown | Unknown test/dev | `legacy/unknown` | None found |
| `projects/205354194989/locations/us-central1/reasoningEngines/7211261359978184704` | 4704 | Unknown | Unknown test/dev | `legacy/unknown` | None found |

### Agent Details

#### Agent 6448 - Canonical Production Bob
- **Purpose:** Current production Slack AI assistant
- **Deployment Date:** November 10-11, 2025 (based on archive dates)
- **Source Code:** Archived in `bob-vertex-agent/` directory
- **Integration:** Connected to Slack webhook at `https://slack-webhook-eow2wytafa-uc.a.run.app`
- **Decision:** Keep as production until Hard Mode migration

#### Agent 9040 - Legacy/Unknown
- **Purpose:** Unknown - likely test or development deployment
- **Deployment Date:** Unknown
- **Source Code:** Not found in repository
- **Integration:** Unknown
- **Decision:** Schedule for investigation and potential decommissioning

#### Agent 4704 - Legacy/Unknown
- **Purpose:** Unknown - likely test or development deployment
- **Deployment Date:** Unknown
- **Source Code:** Not found in repository
- **Integration:** Unknown
- **Decision:** Schedule for investigation and potential decommissioning

## Relationship to Repository

### Current State
- The **Hard Mode** implementation in `agents/bob/` is complete but **NOT deployed**
- Agent 6448 is deployed from older code now in `archive/2025-11-11-final-cleanup/2025-11-10-bob-vertex-agent/`
- There is **no Terraform management** of existing agents
- The repository is prepared for deployment but waiting for migration strategy

### Code Locations
- **Current Bob (undeployed):** `agents/bob/` - Hard Mode compliant, ADK-based
- **Production Bob (6448 source):** `archive/2025-11-11-final-cleanup/2025-11-10-bob-vertex-agent/`
- **Infrastructure (ready):** `infra/terraform/` - Complete but not managing existing agents

## Future State / Migration Plan

### Goals
1. **Terraform Management:** All agents managed as Infrastructure as Code
2. **Single Canonical Bob:** One production Bob from Hard Mode codebase
3. **Resource Hygiene:** Legacy agents properly decommissioned
4. **Complete Tracking:** All resources documented and tagged

### High-Level Migration Steps

#### Phase 1: Discovery & Documentation ✅
- [x] Identify all existing agents
- [x] Document in canonical inventory (this document)
- [x] Create postmortem (084-PM-MORT)

#### Phase 2: Terraform Import (Planned)
- [ ] Import agent 6448 into Terraform state:
  ```hcl
  terraform import google_vertex_ai_reasoning_engine.bob \
    projects/205354194989/locations/us-central1/reasoningEngines/5828234061910376448
  ```
- [ ] Create terraform configuration matching existing agent
- [ ] Verify no changes with `terraform plan`

#### Phase 3: Investigation (Planned)
- [ ] Use GCP Console to inspect agents 9040 and 4704:
  - Check creation dates
  - Review any associated metadata
  - Verify no active connections
- [ ] Document findings in investigation AAR

#### Phase 4: Hard Mode Deployment (Future)
- [ ] Deploy new Hard Mode Bob from `agents/bob/`
- [ ] Run parallel with agent 6448 for validation
- [ ] Migrate Slack integration to new agent
- [ ] Create migration AAR

#### Phase 5: Decommissioning (Future)
- [ ] Archive agent 6448 configuration
- [ ] Delete agent 6448 from Agent Engine
- [ ] Delete agents 9040 and 4704 (after investigation)
- [ ] Verify billing stops for deleted resources

### Required Infrastructure Changes

#### Terraform Import Configuration
```hcl
# To be added to infra/terraform/imports.tf
resource "google_vertex_ai_reasoning_engine" "existing_bob" {
  # Import existing agent 6448
  name         = "5828234061910376448"
  location     = "us-central1"
  display_name = "bob-battalion-commander"

  lifecycle {
    prevent_destroy = true  # Until migration complete
  }
}
```

#### Resource Tagging Standards
All agents must have:
- `environment`: dev|staging|prod
- `managed_by`: terraform|manual
- `purpose`: production|test|experimental
- `owner`: team-name
- `created_date`: YYYY-MM-DD
- `ttl`: days (0 = permanent)

## Monitoring & Compliance

### Quarterly Review Checklist
- [ ] Verify all agents in inventory still exist
- [ ] Check for new untracked agents
- [ ] Review costs for each agent
- [ ] Update status and purpose as needed
- [ ] Archive any decommissioned agents

### Compliance Requirements
- All production agents must be Terraform-managed
- All agents must have proper tagging
- No orphaned/unknown agents older than 90 days
- Cost allocation must be trackable per agent

## References

- **Postmortem:** `000-docs/084-PM-MORT-vertex-ai-agents-discovery.md`
- **Deployment Status:** `000-docs/061-PM-NOTE-deployment-status.md`
- **Deployment Runbook:** `000-docs/070-OD-RBOK-deployment-runbook.md`
- **GCP Project:** 205354194989
- **Console URL:** https://console.cloud.google.com/vertex-ai/reasoning-engines?project=205354194989

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-11-19 | Initial inventory creation | claude.buildcaptain |

---

**Next Review Date:** 2025-02-19 (Quarterly)
**Distribution:** Engineering, SRE, Finance