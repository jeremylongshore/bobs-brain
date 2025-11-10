# DOCUMENT FILING SYSTEM STANDARD v2.0

**Purpose:** Universal standard for organizing project documentation with category-based classification

---

## FORMAT SPECIFICATION

### Primary Format
```
NNN-CC-ABCD-short-description.ext
```

**Components:**
- **NNN** = Zero-padded sequence number (001-999) - enforces chronology
- **CC** = Two-letter category code (see Category Table)
- **ABCD** = Four-letter document type abbreviation (see Type Tables)
- **short-description** = 1-4 words, kebab-case, lowercase
- **ext** = File extension (.md, .pdf, .txt, etc.)

### Sub-Tasks Format
When a document has multiple related sub-documents:

**Option A - Letter Suffix:**
```
005-PM-TASK-api-endpoints.md
005a-PM-TASK-auth-endpoints.md
005b-PM-TASK-payment-endpoints.md
```

**Option B - Numeric Suffix:**
```
006-PM-RISK-security-audit.md
006-1-PM-RISK-encryption-review.md
006-2-PM-RISK-access-controls.md
```

---

## CATEGORY CODES (2-LETTER)

| Code | Category | Description |
|------|----------|-------------|
| **PP** | Product & Planning | Requirements, roadmaps, business planning |
| **AT** | Architecture & Technical | Technical decisions, system design |
| **DC** | Development & Code | Code documentation, modules, components |
| **TQ** | Testing & Quality | Test plans, QA, bugs, security audits |
| **OD** | Operations & Deployment | DevOps, deployment, infrastructure |
| **LS** | Logs & Status | Status logs, work logs, progress tracking |
| **RA** | Reports & Analysis | Reports, analytics, research findings |
| **MC** | Meetings & Communication | Meeting notes, memos, presentations |
| **PM** | Project Management | Tasks, sprints, backlogs, risks |
| **DR** | Documentation & Reference | Guides, manuals, references, SOPs |
| **UC** | User & Customer | User docs, onboarding, training, feedback |
| **BL** | Business & Legal | Contracts, compliance, policies, legal |
| **RL** | Research & Learning | Research, experiments, POCs, proposals |
| **AA** | After Action & Review | Post-mortems, retrospectives, lessons |
| **WA** | Workflows & Automation | Workflow docs, n8n, automation, webhooks |
| **DD** | Data & Datasets | Data documentation, CSV, SQL, exports |
| **MS** | Miscellaneous | General, drafts, archives, work-in-progress |

---

## DOCUMENT TYPE ABBREVIATIONS (4-LETTER)

### PP - Product & Planning
| Code | Full Name | Usage |
|------|-----------|-------|
| **PROD** | Product Requirements Document | Core product requirements |
| **PLAN** | Plan/Planning Document | Strategic plans, project plans |
| **RMAP** | Roadmap | Product or project roadmaps |
| **BREQ** | Business Requirements Document | Business-level requirements |
| **FREQ** | Functional Requirements Document | Functional specifications |
| **SOWK** | Statement of Work | Project scope and deliverables |
| **KPIS** | Key Performance Indicators | Success metrics definition |
| **OKRS** | Objectives and Key Results | Goal-setting framework |

### AT - Architecture & Technical
| Code | Full Name | Usage |
|------|-----------|-------|
| **ADEC** | Architecture Decision Record | Technical decision documentation |
| **ARCH** | Technical Architecture Document | System architecture specs |
| **DSGN** | Design Document/Specification | Detailed design specs |
| **APIS** | API Documentation | API specifications |
| **SDKS** | SDK Documentation | Software development kit docs |
| **INTG** | Integration Documentation | Integration guides and specs |
| **DIAG** | Diagram/Visual Documentation | Architecture diagrams |

### DC - Development & Code
| Code | Full Name | Usage |
|------|-----------|-------|
| **DEVN** | Development Notes | Developer notes and annotations |
| **CODE** | Code Documentation | Code-level documentation |
| **LIBR** | Library Documentation | Library usage and APIs |
| **MODL** | Module Documentation | Module specifications |
| **COMP** | Component Documentation | Component specs and usage |
| **UTIL** | Helper/Utility Documentation | Utility function documentation |

### TQ - Testing & Quality
| Code | Full Name | Usage |
|------|-----------|-------|
| **TEST** | Test Plan/Strategy | Overall testing strategy |
| **CASE** | Test Case Documentation | Specific test cases |
| **QAPL** | Quality Assurance Plan | QA strategy and process |
| **BUGR** | Bug Report/Analysis | Bug documentation |
| **PERF** | Performance Testing | Performance test results |
| **SECU** | Security Audit/Testing | Security assessments |
| **PENT** | Penetration Test Results | Pentest findings |

### OD - Operations & Deployment
| Code | Full Name | Usage |
|------|-----------|-------|
| **OPNS** | Operations Documentation | Operational procedures |
| **DEPL** | Deployment Guide/Log | Deployment instructions |
| **INFR** | Infrastructure Documentation | Infrastructure specs |
| **CONF** | Configuration Documentation | Config file documentation |
| **ENVR** | Environment Setup | Environment configuration |
| **RELS** | Release Notes | Version release notes |
| **CHNG** | Change Log/Management | Change documentation |
| **INCD** | Incident Report | Incident documentation |
| **POST** | Post-Mortem/Incident Analysis | Incident analysis |

### LS - Logs & Status
| Code | Full Name | Usage |
|------|-----------|-------|
| **LOGS** | Status Log/Journal | General status logging |
| **WORK** | Work Log/Session Notes | Daily work logs |
| **PROG** | Progress Report | Progress documentation |
| **STAT** | Status Report/Update | Status updates |
| **CHKP** | Checkpoint/Milestone Log | Milestone tracking |

### RA - Reports & Analysis
| Code | Full Name | Usage |
|------|-----------|-------|
| **REPT** | General Report | Standard reports |
| **ANLY** | Analysis/Research Report | Analytical findings |
| **AUDT** | Audit Report | Audit results |
| **REVW** | Review Document | Review findings |
| **RCAS** | Root Cause Analysis | Problem analysis |
| **DATA** | Data Analysis | Data analysis reports |
| **METR** | Metrics Report | Metrics and KPIs |
| **BNCH** | Benchmark Results | Performance benchmarks |

### MC - Meetings & Communication
| Code | Full Name | Usage |
|------|-----------|-------|
| **MEET** | Meeting Notes/Minutes | Meeting documentation |
| **AGND** | Agenda | Meeting agendas |
| **ACTN** | Action Items | Action item tracking |
| **SUMM** | Summary/Executive Summary | High-level summaries |
| **MEMO** | Memo/Communication | Internal memos |
| **PRES** | Presentation | Presentation materials |
| **WKSP** | Workshop Notes | Workshop documentation |

### PM - Project Management
| Code | Full Name | Usage |
|------|-----------|-------|
| **TASK** | Task Breakdown/List | Task documentation |
| **BKLG** | Backlog | Product/sprint backlog |
| **SPRT** | Sprint Plan/Notes | Sprint planning docs |
| **RETR** | Retrospective | Sprint retrospectives |
| **STND** | Standup Notes | Daily standup logs |
| **RISK** | Risk Register/Assessment | Risk documentation |
| **ISSU** | Issue Tracker/Log | Issue tracking |

### DR - Documentation & Reference
| Code | Full Name | Usage |
|------|-----------|-------|
| **REFF** | Reference Material/Guide | Reference documentation |
| **GUID** | User Guide/Handbook | User guides |
| **MANL** | Manual | Operation manuals |
| **FAQS** | FAQ Document | Frequently asked questions |
| **GLOS** | Glossary | Term definitions |
| **SOPS** | Standard Operating Procedure | Procedural documentation |
| **TMPL** | Template | Document templates |
| **CHKL** | Checklist | Process checklists |

### UC - User & Customer
| Code | Full Name | Usage |
|------|-----------|-------|
| **USER** | User Documentation | End-user documentation |
| **ONBD** | Onboarding Guide | User onboarding materials |
| **TRNG** | Training Materials | Training documentation |
| **FDBK** | Feedback/User Feedback | User feedback logs |
| **SURV** | Survey Results | Survey data and analysis |
| **INTV** | Interview Notes/Transcripts | Interview documentation |
| **PERS** | Persona Documentation | User personas |

### BL - Business & Legal
| Code | Full Name | Usage |
|------|-----------|-------|
| **CNTR** | Contract/Agreement | Legal contracts |
| **NDAS** | Non-Disclosure Agreement | Confidentiality agreements |
| **LICN** | License Documentation | Licensing information |
| **CMPL** | Compliance Documentation | Compliance records |
| **POLI** | Policy Document | Company policies |
| **TERM** | Terms & Conditions | Terms documentation |
| **PRIV** | Privacy Documentation | Privacy policies |

### RL - Research & Learning
| Code | Full Name | Usage |
|------|-----------|-------|
| **RSRC** | Research Notes | Research documentation |
| **LERN** | Learning/Study Notes | Study materials |
| **EXPR** | Experiment/POC Documentation | Proof of concept docs |
| **PROP** | Proposal | Project proposals |
| **WHIT** | Whitepaper | Technical whitepapers |
| **CSES** | Case Study | Case study documentation |

### AA - After Action & Review
| Code | Full Name | Usage |
|------|-----------|-------|
| **AACR** | After Action Report | After-action reviews |
| **LESN** | Lessons Learned | Lessons documentation |
| **PMRT** | Post-Mortem/Incident Review | Incident post-mortems |

### WA - Workflows & Automation
| Code | Full Name | Usage |
|------|-----------|-------|
| **WFLW** | Workflow Documentation | Workflow specs |
| **N8NS** | n8n Workflow Documentation | n8n-specific workflows |
| **AUTO** | Automation Documentation | Automation scripts/docs |
| **HOOK** | Webhook Documentation | Webhook configuration |

### DD - Data & Datasets
| Code | Full Name | Usage |
|------|-----------|-------|
| **DSET** | Data Documentation | Dataset documentation |
| **CSVS** | CSV Dataset Documentation | CSV file documentation |
| **SQLS** | SQL/Database Documentation | Database documentation |
| **EXPT** | Data Export Documentation | Export specifications |

### MS - Miscellaneous
| Code | Full Name | Usage |
|------|-----------|-------|
| **MISC** | Miscellaneous/General | General documents |
| **DRFT** | Draft/Temporary | Draft documents |
| **ARCH** | Archive Notes | Archived materials |
| **OLDV** | Deprecated/Old Version | Deprecated docs |
| **WIPS** | Work in Progress | Work in progress docs |
| **INDX** | Index/Table of Contents | Index files |

---

## EXAMPLE CHRONOLOGY

### Project Documentation Structure
```
000-docs/
├── 001-AT-ADEC-initial-architecture.md
├── 002-PP-PROD-core-features.md
├── 003-MC-MEET-kickoff-notes.md
├── 004-PP-PLAN-sprint-1-roadmap.pdf
├── 005-PM-TASK-api-endpoints.md
├── 005a-PM-TASK-auth-endpoints.md
├── 005b-PM-TASK-payment-endpoints.md
├── 006-PM-RISK-data-security.md
├── 007-AT-ADEC-database-choice.md
├── 008-MC-MEET-client-feedback.md
├── 009-AA-AACR-sprint-1-review.md
├── 010-LS-LOGS-error-analysis.txt
├── 011-TQ-TEST-integration-strategy.md
├── 012-OD-DEPL-production-guide.md
├── 013-UC-USER-onboarding-flow.md
├── 014-DR-GUID-api-reference.md
├── 015-RA-ANLY-user-metrics.xlsx
```

### Real-World Examples
```
001-PP-PROD-hustle-mvp-requirements.md
002-AT-ARCH-hustle-system-design.pdf
003-PM-TASK-authentication-implementation.md
004-TQ-SECU-hustle-security-audit.md
005-OD-DEPL-gcp-cloud-run-setup.md
006-MC-MEET-stakeholder-demo-notes.md
007-UC-GUID-parent-user-manual.pdf
008-LS-WORK-october-development-log.md
009-RA-METR-q3-performance-metrics.xlsx
010-AA-LESN-beta-launch-learnings.md
```

---

## BENEFITS OF THIS SYSTEM

### Enhanced Organization
- **Category visibility** - Immediately identify document type by category code
- **Improved sorting** - Documents naturally group by category, then chronology
- **Better searchability** - Search by category (PP, AT, etc.) or type (TASK, MEET)

### Scalability
- **Consistent 4-letter codes** - Uniform length for all document types
- **Clear hierarchy** - Category → Type → Description
- **Room for growth** - 17 categories × many types = extensive coverage

### Cross-Project Compatibility
- **Universal abbreviations** - Use across all projects
- **Standardized structure** - Team members recognize patterns
- **Easy onboarding** - New team members learn system quickly

---

## MIGRATION FROM OLD SYSTEM

### Converting Existing Files

**Old Format:**
```
005-tsk-api-endpoints.md
006-rsk-security-audit.md
007-adr-database-choice.md
```

**New Format:**
```
005-PM-TASK-api-endpoints.md
006-PM-RISK-security-audit.md
007-AT-ADEC-database-choice.md
```

### Migration Script Pattern
```bash
# Example: Convert 3-letter to category + 4-letter
# Old: NNN-abc-description.ext
# New: NNN-CC-ABCD-description.ext

# tsk → PM-TASK
# rsk → PM-RISK
# adr → AT-ADEC
# prd → PP-PROD
# mtg → MC-MEET
```

---

## QUICK REFERENCE CARD

### Most Common Combinations

| Code | Document Type | Example |
|------|--------------|---------|
| PP-PROD | Product Requirements | 001-PP-PROD-feature-spec.md |
| AT-ADEC | Architecture Decision | 002-AT-ADEC-tech-stack.md |
| PM-TASK | Task Documentation | 003-PM-TASK-build-api.md |
| MC-MEET | Meeting Notes | 004-MC-MEET-sprint-planning.md |
| TQ-TEST | Test Plan | 005-TQ-TEST-integration-tests.md |
| OD-DEPL | Deployment Guide | 006-OD-DEPL-production.md |
| LS-WORK | Work Log | 007-LS-WORK-daily-log.md |
| RA-ANLY | Analysis Report | 008-RA-ANLY-user-data.md |
| DR-GUID | User Guide | 009-DR-GUID-user-manual.md |
| AA-LESN | Lessons Learned | 010-AA-LESN-sprint-retro.md |

---

## NAMING BEST PRACTICES

### DO's
✅ Use lowercase for description
✅ Use kebab-case (hyphens) for multi-word descriptions
✅ Keep descriptions 1-4 words maximum
✅ Use descriptive file extensions (.md, .pdf, .xlsx)
✅ Pad sequence numbers (001, 002, not 1, 2)
✅ Maintain chronological sequence

### DON'Ts
❌ Don't skip sequence numbers
❌ Don't use underscores or camelCase in descriptions
❌ Don't use special characters except hyphens
❌ Don't exceed 4 words in description
❌ Don't use non-standard category codes
❌ Don't omit category or type codes

---

## CATEGORY DECISION TREE

**Not sure which category? Use this guide:**

1. **Is it about product/business planning?** → PP
2. **Is it a technical/architecture decision?** → AT
3. **Is it code or development documentation?** → DC
4. **Is it about testing or quality?** → TQ
5. **Is it about deployment or operations?** → OD
6. **Is it a log or status update?** → LS
7. **Is it a report or analysis?** → RA
8. **Is it meeting notes or communication?** → MC
9. **Is it project management (tasks/risks)?** → PM
10. **Is it a reference guide or manual?** → DR
11. **Is it for end users or customers?** → UC
12. **Is it legal or business policy?** → BL
13. **Is it research or experimental?** → RL
14. **Is it a post-mortem or retrospective?** → AA
15. **Is it about workflows or automation?** → WA
16. **Is it about data or datasets?** → DD
17. **Doesn't fit anywhere?** → MS

---

## DIRECTORY STRUCTURE

**IMPORTANT:** This standard uses a **FLAT** directory structure.

### Standard Layout
```
[PROJECT-ROOT]/
├── 000-docs/                          # FLAT - All documents here
│   ├── 000-INDEX.md                   # Auto-generated inventory
│   ├── 001-PP-PROD-requirements.md
│   ├── 002-AT-ARCH-system-design.pdf
│   ├── 003-MC-MEET-kickoff.md
│   └── ...
├── src/
├── tests/
└── README.md
```

**No subdirectories in 000-docs/** - Keep it FLAT for:
- ✅ Easy chronological browsing
- ✅ Simple grep/search operations
- ✅ No deep nesting complexity
- ✅ Instant visual timeline

---

**DOCUMENT FILING SYSTEM STANDARD v2.0**
*Category-based organization for professional project documentation*

---

**Last Updated:** 2025-10-26
**Status:** ✅ Production Standard
**Applies To:** All projects in `/home/jeremy/000-projects/`
**Related Commands:** `/doc-filing` - Auto-organize docs into 000-docs/
