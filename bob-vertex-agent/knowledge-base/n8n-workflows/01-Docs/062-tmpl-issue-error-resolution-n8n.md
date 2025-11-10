---
name: Error Resolution — n8n Repos
description: Resolve build, dependency, and secret issues
labels: ["bug","triage","n8n"]
body:
  - type: checkboxes
    id: tasks
    attributes:
      label: Tasks
      options:
        - label: Update Node LTS; dedupe packages; re-lock
        - label: CI setup-node LTS; cache npm; lint /workflows/*.json
        - label: Normalize via workflow snapshots
        - label: Replace inline tokens with env refs; rotate keys; add .env.example
        - label: Schema validate + dry import to test n8n
  - type: markdown
    attributes:
      value: |
        **Deliverables:** PR with grouped commits; error-report.md
        **Enhancement:** Add chaos checks for 429/500 to ensure clean failures
---