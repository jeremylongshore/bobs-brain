---
name: Chore/Fix — n8n Workflows
description: Resolve audit findings with atomic PRs
labels: ["chore","fix","n8n"]
body:
  - type: markdown
    attributes:
      value: |
        **Branching:** chore/<short-title>
  - type: checkboxes
    id: tasks
    attributes:
      label: Tasks
      options:
        - label: Infra fixes (CI, CODEOWNERS, branch protection)
        - label: Security fixes (move inline secrets to env, add .env.example)
        - label: Docs (short README, details in /docs)
        - label: Code (deterministic workflow JSON formatting)
        - label: PR links issue, includes proof (headless n8n import OK/FAIL)
  - type: markdown
    attributes:
      value: |
        **Deliverables:** PRs linked to issues; chore-verification.md; keep README minimal
        **Enhancement:** Add workflow smoke tests (import + dry-run each workflow)
---