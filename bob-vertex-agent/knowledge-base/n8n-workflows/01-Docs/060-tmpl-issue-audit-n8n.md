---
name: Audit — n8n Workflows
description: Audit repo for structure, security, docs, CI readiness
labels: ["audit","n8n"]
body:
  - type: markdown
    attributes:
      value: |
        **Scope:** /workflows/*.json, /packages/*, env handling, CI configs
  - type: checkboxes
    id: tasks
    attributes:
      label: Tasks
      options:
        - label: Validate workflows against n8n schema; flag cycles and broken creds
        - label: Check CODEOWNERS, branch protection, secret scanning
        - label: Classify issues (audit:{infra|security|docs|code}, severity)
        - label: Open one Issue per finding with repro + fix steps
        - label: Create tracking issue with severity counts
  - type: textarea
    id: secrets
    attributes:
      label: Secrets & Config (document only)
      description: Add .env.example placeholders (N8N_ENCRYPTION_KEY, N8N_HOST, N8N_PORT, provider keys)
  - type: markdown
    attributes:
      value: |
        **Deliverables:** Issues + labels + milestone; audit-summary.md; minimal README update (Intro, Quickstart, Deploy, Secrets, Support)
        **Enhancement:** Add workflow schema snapshots in /workflow-spec/ to catch node reorder diffs
---