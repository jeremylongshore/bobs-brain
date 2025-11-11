---
name: Bug report
about: Create a report to help us improve the workflow
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Import workflow into N8N
2. Configure with these settings: '...'
3. Send request to '...'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Error Messages**
```
Paste any error messages from N8N logs here
```

**Environment Information:**
- N8N Version: [e.g. 1.0.5]
- N8N Hosting: [Cloud/Self-hosted]
- Node.js Version: [e.g. 18.17.0]
- Workflow Version: [e.g. 1.0.0]

**Workflow Configuration:**
- Number of resellers in CSV: [e.g. 50]
- CSV source: [e.g. GitHub, Google Sheets, etc.]
- SMTP provider: [e.g. Gmail, SendGrid, etc.]
- Google Sheets integration: [Yes/No]

**Sample Data (if applicable):**
```csv
# Paste sample CSV data that reproduces the issue (remove sensitive info)
id,name,email,region,trust_score
TEST123,Test Reseller,test@example.com,US,8.5
```

**Request Payload (if applicable):**
```json
{
  "csvUrl": "https://example.com/resellers.csv",
  "product": {
    "brand": "Test Brand",
    "model": "Test Model"
  }
}
```

**Screenshots**
If applicable, add screenshots of N8N workflow editor or error dialogs.

**Additional context**
Add any other context about the problem here. Include relevant N8N node configurations if they might be related to the issue.