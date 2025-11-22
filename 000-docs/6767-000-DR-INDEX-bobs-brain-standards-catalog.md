# 6767 Standards Catalog – Bob's Brain Global Index

**Document Type:** Index / Reference (DR-INDEX)
**Document ID:** 6767-000
**Status:** Active
**Purpose:** Global index and status catalog for all 6767-* standards, guides, and reference docs in bobs-brain
**Last Updated:** 2025-11-21

---

## I. Purpose

This document serves as the **master catalog** for all 6767-prefixed documentation in the Bob's Brain repository.

**6767 Series Overview:**
- **6767-NNN-***  - Numbered canonical standards (e.g., 6767-120, 6767-121)
- **6767-ABCD-*** - Topical/mnemonic standards (e.g., 6767-INLINE, 6767-LAZY, 6767-A2AINSP)

**Scope:**
- All 6767-* docs are considered **canonical** or **reference** material
- These docs are intended to be **cross-repo reusable** where applicable
- These docs have **higher stability requirements** than NNN-* implementation docs

**When to Use 6767-* vs NNN-*:**
- **6767-*** - Standards, guides, runbooks, architecture that should be stable and reusable
- **NNN-*** - Phase-specific work, AARs, plans, status reports tied to specific milestones

---

## II. Quick Start

**New to bobs-brain? Start here:**
1. **6767-000** (this doc) - Global catalog of all 6767 standards
2. **6767-120** - Agent Engine / A2A / Inline Deployment sub-index (if working on deployment/A2A topics)
3. **6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md** - Hard Mode rules (R1-R8)
4. **6767-RB-OPS-adk-department-operations-runbook.md** - Day-to-day operations

**For Operators:**
- Start with **6767-RB-OPS** (operations runbook)
- Then review **6767-120** (Agent Engine sub-index)
- Then drill into specific guides (SLKDEV, AEDEV, etc.)

**For Developers:**
- Start with **6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md** (understand Hard Mode)
- Then review **6767-120** (architecture overview)
- Then drill into implementation guides (6767-LAZY, 6767-INLINE, etc.)

---

## III. Complete 6767 Standards Catalog

### Core Standards (Infrastructure & Compliance)

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md | DR-STND | adk-agent-engine-spec-and-hardmode-rules.md | Canonical (Cross-Repo) | Defines ADK + Agent Engine compliance and Hard Mode rules (R1-R8) for IAM Department |
| 6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md | DR-STND | inline-source-deployment-for-vertex-agent-engine.md | Active | Canonical pattern for deploying ADK agents to Agent Engine via inline source (not pickle) |
| 6767-LAZY-DR-STND-adk-lazy-loading-app-pattern.md | DR-STND | adk-lazy-loading-app-pattern.md | Active | Lazy-loading App pattern for all ADK agents (module-level `app` variable) |
| 6767-DR-STND-arv-minimum-gate.md | DR-STND | arv-minimum-gate.md | Active | Agent Readiness Verification (ARV) minimum gate standard for deployment safety |
| 6767-116-DR-STND-config-and-feature-flags-standard-v1.md | DR-STND | config-and-feature-flags-standard-v1.md | Active | Configuration and feature flags standard v1.0 (cross-cutting) |
| 6767-DR-STND-github-issue-creation-guardrails.md | DR-STND | github-issue-creation-guardrails.md | Active | Safety guardrails for GitHub issue creation (write operations disabled by default) |

### Agent Engine & Deployment

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-120-DR-STND-agent-engine-a2a-and-inline-deploy-index.md | DR-STND | agent-engine-a2a-and-inline-deploy-index.md | Active | **Sub-index** for Agent Engine, A2A, and inline deployment topics (START HERE for deployment work) |
| 6767-AEDEV-DR-GUIDE-agent-engine-dev-wiring-and-smoke-test.md | DR-GUIDE | agent-engine-dev-wiring-and-smoke-test.md | Complete (dev-only) | Guide for Agent Engine dev wiring and smoke test (Phase AE3) |
| 6767-AECOMP-LS-SITR-ae-dev-wireup-complete.md | LS-SITR | ae-dev-wireup-complete.md | Complete (dev-only) | Status report: Agent Engine dev wiring complete (Slack → Cloud Run → Agent Engine) |
| 6767-127-DR-STND-agent-engine-entrypoints.md | DR-STND | agent-engine-entrypoints.md | Active | Standard for Agent Engine entrypoint configuration |

### A2A Protocol & AgentCards

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-DR-STND-agentcards-and-a2a-contracts.md | DR-STND | agentcards-and-a2a-contracts.md | Active | AgentCard and A2A contract standard for ADK-based agent departments |
| 6767-121-DR-STND-a2a-compliance-tck-and-inspector.md | DR-STND | a2a-compliance-tck-and-inspector.md | Active | A2A compliance tooling standard (a2a-inspector + a2a-tck) with phased adoption plan |
| 6767-A2AINSP-AA-REPT-a2a-inspector-integration-for-department-adk-iam.md | AA-REPT | a2a-inspector-integration-for-department-adk-iam.md | Active | AAR: a2a-inspector integration with two-layer validation strategy |
| 6767-123-DR-STND-a2a-inspector-usage-and-local-setup.md | DR-STND | a2a-inspector-usage-and-local-setup.md | Active | A2A Inspector usage and local setup standard |
| 6767-124-DR-STND-a2a-quality-gate-for-department-adk-iam.md | DR-STND | a2a-quality-gate-for-department-adk-iam.md | Active | A2A quality gate standard for IAM department |

### Prompt Design & Agent Architecture

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-115-DR-STND-prompt-design-and-a2a-contracts-for-department-adk-iam.md | DR-STND | prompt-design-and-a2a-contracts-for-department-adk-iam.md | Active | Canonical prompt design and A2A contract patterns for department adk iam (5-part template) |
| 6767-DR-STND-prompt-design-and-agentcard-standard.md | DR-STND | prompt-design-and-agentcard-standard.md | Active | Contract-first prompt design standard with AgentCard integration |
| 6767-125-DR-STND-prompt-design-for-bob-and-department-adk-iam.md | DR-STND | prompt-design-for-bob-and-department-adk-iam.md | Active | Prompt design standard for Bob and IAM department |

### Operations & Deployment

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-RB-OPS-adk-department-operations-runbook.md | RB-OPS | adk-department-operations-runbook.md | Active | Daily operational procedures, monitoring, and troubleshooting for IAM department |
| 6767-DR-STND-live-rag-and-agent-engine-rollout-plan.md | DR-STND | live-rag-and-agent-engine-rollout-plan.md | Active | Rollout strategy for enabling live Vertex AI Search (RAG) and Agent Engine features |
| 6767-118-DR-STND-cicd-pipeline-for-iam-department.md | DR-STND | cicd-pipeline-for-iam-department.md | Active | CI/CD pipeline standard for IAM department |

### Slack Integration

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-SLKDEV-DR-GUIDE-slack-dev-integration-operator-guide.md | DR-GUIDE | slack-dev-integration-operator-guide.md | Production-Ready | Step-by-step guide for Slack bot integration in dev/staging/prod |
| 6767-SLKAUD-LS-SITR-phase-c-slack-integration-audit.md | LS-SITR | phase-c-slack-integration-audit.md | In Progress | Slack integration audit - identified Agent Engine deployment blocker (fixed) |

### Storage & Knowledge Hub

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-AT-ARCH-org-storage-architecture.md | AT-ARCH | org-storage-architecture.md | Active | Org-wide knowledge hub storage architecture (LIVE1-GCS) - centralized GCS bucket |
| 6767-OD-ARCH-datahub-storage-consolidation.md | OD-ARCH | datahub-storage-consolidation.md | Canonical | Datahub-intent consolidation - central knowledge hub for all agent systems (~4GB) |

### Template & Porting Guides

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-DR-GUIDE-porting-iam-department-to-new-repo.md | DR-GUIDE | porting-iam-department-to-new-repo.md | Canonical Guide | Step-by-step guide for porting IAM department template to new product repos |
| 6767-DR-STND-iam-department-template-scope-and-rules.md | DR-STND | iam-department-template-scope-and-rules.md | Reference | Scope and reusability boundaries for IAM department template |
| 6767-DR-STND-iam-department-integration-checklist.md | DR-STND | iam-department-integration-checklist.md | Standard Checklist | Checklist for integrating IAM department into new repos (use with porting guide) |

### User & Developer Guides

| ID | Type | Filename | Status | Summary |
|----|------|----------|--------|---------|
| 6767-DR-GUIDE-iam-department-user-guide.md | DR-GUIDE | iam-department-user-guide.md | User Guide | How to use Bob and IAM department for software engineering tasks |
| 6767-ROADMAP-DR-ROADMAP-bobs-brain-you-are-here.md | DR-ROADMAP | bobs-brain-you-are-here.md | Active | Roadmap and "you are here" orientation for bobs-brain repo |

**Total 6767 Documents:** 24

---

## IV. Suggested Status Adjustments

### Potential Overlaps / Supersessions

**1. Prompt Design Standards (3 docs with overlap)**

**Files:**
- `6767-115-DR-STND-prompt-design-and-a2a-contracts-for-department-adk-iam.md` (Active)
- `6767-DR-STND-prompt-design-and-agentcard-standard.md` (Active)
- `6767-125-DR-STND-prompt-design-for-bob-and-department-adk-iam.md` (Active)

**Analysis:** Three prompt design standards with overlapping scope

**Recommendation:**
- ⏸️ **Review for consolidation** - Determine if 6767-115 and 6767-125 can be merged
- ⏸️ **Or clarify scope** - E.g., 6767-115 = contracts focus, 6767-125 = general prompts
- ✅ **Keep 6767-DR-STND-prompt-design-and-agentcard-standard.md** as foundational doc

**Action:** Review and either merge or clarify distinct purposes (deferred to future cleanup)

---

**2. A2A Inspector Standards (2 docs with potential overlap)**

**Files:**
- `6767-121-DR-STND-a2a-compliance-tck-and-inspector.md` (Active) - New, comprehensive
- `6767-123-DR-STND-a2a-inspector-usage-and-local-setup.md` (Active) - Older, narrower scope

**Analysis:** 6767-121 was created recently and covers a2a-inspector + a2a-tck comprehensively

**Recommendation:**
- ✅ **Keep 6767-121 as primary** - More comprehensive, covers both tools
- ⏸️ **Mark 6767-123 as "Superseded by 6767-121"** or merge into 6767-121 (deferred)

**Action:** Update 6767-123 status header to reference 6767-121 (deferred to future cleanup)

---

**3. Config & Feature Flags (potential duplicate ID)**

**Files:**
- `6767-116-DR-STND-config-and-feature-flags-standard-v1.md` (Active)
- Also appears in NNN-series as `116-DR-STND-config-and-feature-flags-standard-v1.md`

**Analysis:** Same doc with both 6767- and NNN- prefixes

**Recommendation:**
- ✅ **Keep 6767-116 version** - Canonical standards should use 6767- prefix
- ⏸️ **Remove or archive NNN-116 version** - Avoid duplicate copies (deferred)

**Action:** Verify which is authoritative, remove duplicate (deferred to future cleanup)

---

**4. CI/CD Pipeline Standard (potential duplicate ID)**

**Files:**
- `6767-118-DR-STND-cicd-pipeline-for-iam-department.md` (Active)
- Also appears in NNN-series as `118-DR-STND-cicd-pipeline-for-iam-department.md`

**Analysis:** Same doc with both 6767- and NNN- prefixes

**Recommendation:**
- ✅ **Keep 6767-118 version** - Canonical standards should use 6767- prefix
- ⏸️ **Remove or archive NNN-118 version** - Avoid duplicate copies (deferred)

**Action:** Verify which is authoritative, remove duplicate (deferred to future cleanup)

---

## V. How to Use the 6767 Series

### Navigation Strategy

**Start at the Top:**
1. **6767-000** (this doc) - Global catalog
2. **6767-120** - Agent Engine / A2A / Inline sub-index (if working on deployment topics)
3. Drill into specific standards/guides as needed

**By Audience:**

**For Operators:**
- **Primary:** `6767-RB-OPS-adk-department-operations-runbook.md`
- **Slack:** `6767-SLKDEV-DR-GUIDE-slack-dev-integration-operator-guide.md`
- **Agent Engine:** `6767-AEDEV-DR-GUIDE-agent-engine-dev-wiring-and-smoke-test.md`
- **Storage:** `6767-AT-ARCH-org-storage-architecture.md`

**For Developers:**
- **Primary:** `6767-DR-STND-adk-agent-engine-spec-and-hardmode-rules.md` (Hard Mode R1-R8)
- **Deployment:** `6767-INLINE-DR-STND-inline-source-deployment-for-vertex-agent-engine.md`
- **Agents:** `6767-LAZY-DR-STND-adk-lazy-loading-app-pattern.md`
- **A2A:** `6767-DR-STND-agentcards-and-a2a-contracts.md`
- **Prompts:** `6767-115-DR-STND-prompt-design-and-a2a-contracts-for-department-adk-iam.md`

**For Template Adopters:**
- **Porting Guide:** `6767-DR-GUIDE-porting-iam-department-to-new-repo.md`
- **Integration Checklist:** `6767-DR-STND-iam-department-integration-checklist.md`
- **Template Scope:** `6767-DR-STND-iam-department-template-scope-and-rules.md`

**For End Users:**
- **User Guide:** `6767-DR-GUIDE-iam-department-user-guide.md`
- **Roadmap:** `6767-ROADMAP-DR-ROADMAP-bobs-brain-you-are-here.md`

---

### Document Type Codes (6767-ABCD-*)

**Common Mnemonic Codes:**
- **INLINE** - Inline source deployment pattern
- **LAZY** - Lazy-loading app pattern
- **A2AINSP** - A2A Inspector integration
- **AEDEV** - Agent Engine dev wiring
- **AECOMP** - Agent Engine completion status
- **SLKDEV** - Slack dev integration
- **SLKAUD** - Slack audit
- **ROADMAP** - Roadmap / orientation

**Standard Type Codes:**
- **DR-STND** - Documentation/Reference Standard
- **DR-GUIDE** - Documentation/Reference Guide
- **DR-INDEX** - Documentation/Reference Index
- **DR-ROADMAP** - Documentation/Reference Roadmap
- **RB-OPS** - Runbook Operations
- **AA-REPT** - After-Action Report
- **LS-SITR** - Logs/Status SITREP
- **AT-ARCH** - Architecture/Technical
- **OD-ARCH** - Operations/Deployment Architecture

---

### Update Policy

**When to Update 6767-000:**
- ✅ Whenever a new 6767-* document is created
- ✅ Whenever a 6767-* document status changes (Active → Superseded, Draft → Active)
- ✅ Quarterly review (next: 2026-02-21)

**How to Update:**
- Add new entry to appropriate section (III. Complete Catalog)
- Update summary/status if changed
- Update "Last Updated" date in header
- Commit with message: `docs(6767): update global catalog with <new-doc-name>`

---

## VI. Relationship to Other Indexes

**6767-000 (this doc):**
- **Scope:** All 6767-* docs across entire repo
- **Purpose:** Global catalog and navigation aid
- **Audience:** Everyone (developers, operators, template adopters, users)

**6767-120 (Agent Engine / A2A / Inline sub-index):**
- **Scope:** Subset of 6767-* docs related to Agent Engine, A2A, and inline deployment
- **Purpose:** Deep dive into deployment topics
- **Audience:** Developers and operators working on deployment/A2A features

**000-AA-AUDT-000-docs-inventory-and-gap-report.md (NNN-series inventory):**
- **Scope:** All NNN-CC-ABCD-* docs (001-133 range)
- **Purpose:** Gap analysis and historical record
- **Audience:** Developers tracking phase-specific work and AARs

**Hierarchy:**
```
6767-000 (global 6767 catalog)
  └─> 6767-120 (Agent Engine / A2A sub-index)
      └─> Individual 6767-* standards/guides

000-AA-AUDT (NNN-series inventory)
  └─> Individual NNN-* phase docs/AARs
```

---

## VII. Summary

**6767 Series Highlights:**
- **24 canonical documents** covering standards, guides, runbooks, and architecture
- **6767-120 sub-index** provides deep dive into Agent Engine / A2A / inline deployment topics
- **Multiple audiences served:** Developers, operators, template adopters, end users
- **Clear navigation paths** for each audience type

**Key Takeaways:**
1. Start with **6767-000** (this doc) for global orientation
2. Use **6767-120** for Agent Engine / A2A / deployment work
3. Check status column before relying on any 6767 doc
4. Potential overlaps exist (prompt design, a2a-inspector) - deferred cleanup recommended

**Next Actions:**
1. ✅ Link 6767-000 into existing indexes (6767-120, CLAUDE.md)
2. ⏸️ Quarterly review for new 6767-* docs (next: 2026-02-21)
3. ⏸️ Resolve prompt design overlap (consolidate or clarify scope)
4. ⏸️ Mark 6767-123 as superseded by 6767-121 (or merge)

---

**Last Updated:** 2025-11-21
**Status:** Active (initial catalog complete)
**Next Review:** 2026-02-21 (quarterly) or when 5+ new 6767-* docs added
