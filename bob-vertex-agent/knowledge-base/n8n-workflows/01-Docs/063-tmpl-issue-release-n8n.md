---
name: Release — n8n Workflows
description: Cut a clean semver release with verification
labels: ["release","n8n"]
body:
  - type: input
    id: version
    attributes:
      label: Version (semver, e.g., v1.2.0)
  - type: checkboxes
    id: verify
    attributes:
      label: Verify
      options:
        - label: All workflows load in headless n8n
        - label: .env.example matches actual required keys
        - label: Smoke + chaos checks pass
  - type: textarea
    id: notes
    attributes:
      label: Release notes
  - type: markdown
    attributes:
      value: |
        **Actions:** Tag vX.Y.Z, generate changelog, publish release with artifacts (release-summary.md, zipped /workflow-spec)
        **Enhancement:** Release verification pipeline: import → execute → export before tagging
---