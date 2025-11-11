# Disposable Marketplace N8N Documentation

## Overview
N8N workflow project for creating disposable marketplaces that collect instant quotes from hundreds of resellers.

## Quick Links
- [Quickstart](quickstart.md)
- [Deploy](deploy.md) (n8n Cloud / Private)
- [Secrets Configuration](secrets.md)
- [Troubleshooting](troubleshooting.md)
- [Releases](releases.md)

## Architecture
The workflow enables users to upload a CSV of reseller contacts and automatically collect ranked offers for products (luxury watches, classic cars, art, etc.) within minutes.

### Workflow Diagram

```mermaid
graph LR
    A[Webhook: Start] --> B[Parse CSV]
    B --> C[Batch Resellers]
    C --> D[Email Outreach]
    C --> E[API Outreach]
    D --> F[Webhook: Collect Offers]
    E --> F
    F --> G[Score & Rank]
    G --> H[Top 5 Results]
    H --> I[Webhook: Summary]
```

### Key Components
- Webhook endpoints for starting collection and receiving offers
- CSV processing and reseller batch management
- Dual outreach via email and API calls
- Intelligent ranking system based on price, trust, response time, and terms
- Summary endpoint for retrieving top-ranked offers

## Getting Started
1. Import `workflow.json` into your N8N instance
2. Configure environment variables (see [Secrets](secrets.md))
3. Test with the provided `test-requests.sh` script
4. Upload your reseller CSV and start collecting offers

For detailed setup instructions, see the [Quickstart Guide](quickstart.md).