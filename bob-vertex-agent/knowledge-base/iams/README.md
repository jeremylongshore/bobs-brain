# iamNews - News Agent Template

**Intent Agent Manager News** - Reusable TEMPLATE for building AI news platforms with 11 specialized agents.

**Created:** 2025-10-29
**Status:** ⚠️ Template extraction in progress (currently mixed with BrightStream)
**Type:** TEMPLATE (generic, reusable for ANY news platform)
**Tech Stack:** Google ADK, Vertex AI Agent Engine, Terraform, Firestore, Cloud Storage

---

## ⚠️ IMPORTANT: This is a TEMPLATE, Not a Specific Implementation

**What this means:**
- This directory contains GENERIC patterns for building news platforms
- It is NOT a specific news platform (that's what `brightstream/` is)
- Use this template to CREATE implementations like BrightStream, TechStream, BizStream, etc.
- Only generic, reusable components belong here

**Architecture Hierarchy:**
```
iams/                    # Tier 1: ALL agent systems
└── iamnews/             # Tier 2: NEWS TEMPLATE (you are here)
    └── brightstream/    # Tier 3: BrightStream INSTANCE (specific)
```

**See:** `TEMPLATE-SEPARATION-STRATEGY.md` for migration plan

---

## Overview

**iamNews** is a general-purpose agentic news platform designed to be **customized for different implementations**. It provides a complete base architecture that can be tailored for:

- **BrightStream** - Positive news platform (first implementation)
- **TechStream** - Tech news aggregation
- **BizStream** - Business news curation
- Or any other news vertical you want to build

---

## Architecture

### 11 Intelligent Agents (Hierarchical Structure)

**Agent 0: Root Orchestrator** - Main entry point, routes requests to specialized agents
**Agent 1: News Aggregator** - Monitors RSS feeds, filters by date, deduplicates
**Agent 2: Story Scorer** - Scores stories, selects top content, verifies sources
**Agent 3: Content Generation Orchestrator** - Decides which model to use (Lyria/Imagen/Veo)
**Agent 4: Lyria Agent** - Audio/text-to-speech generation
**Agent 5: Imagen Agent** - Static image generation
**Agent 6: Veo Agent** - Video generation
**Agent 7: Quality Assurance** - 4-layer anti-hallucination verification
**Agent 8: Publishing** - Formats and distributes content
**Agent 9: Analytics** - Tracks performance, implements reflection pattern
**Agent 10: Evaluation** - Automated performance evaluation and improvement

### Tech Stack

- **Agent Framework**: Google ADK (Agent Development Kit)
- **Agent Runtime**: Vertex AI Agent Engine (managed service)
- **Backend**: Genkit on Cloud Run
- **Database**: Firestore (metadata, state)
- **Storage**: Cloud Storage (media files with filing system)
- **Communication**: A2A Protocol (Agent-to-Agent, native Vertex AI)
- **Models**: Gemini 1.5 Flash/Pro, Lyria, Imagen, Veo
- **Infrastructure**: Terraform (Infrastructure as Code)

### Storage Filing System

```
gs://iamnews-media/
├── sources/
│   ├── raw/YYYY/MM/DD/*.json
│   └── processed/YYYY/MM/DD/*.json
├── articles/
│   ├── drafts/YYYY/MM/DD/*.json
│   ├── published/YYYY/MM/DD/*.json
│   └── archived/YYYY/MM/*.json
├── media/
│   ├── images/
│   │   ├── originals/YYYY/MM/DD/*.png
│   │   ├── optimized/YYYY/MM/DD/*-web.png
│   │   └── thumbnails/YYYY/MM/DD/*-thumb.png
│   ├── videos/YYYY/MM/DD/*.mp4
│   └── audio/YYYY/MM/DD/*.mp3
├── analytics/daily/YYYY/MM/DD/*.json
├── backups/firestore/YYYY/MM/DD/*.json
└── temp/YYYY/MM/DD/*.tmp (auto-deleted after 24hr)
```

**Lifecycle Management:**
- Temp files → Deleted after 1 day
- Drafts → Nearline after 7 days
- Archived → Coldline after 90 days
- Analytics → Deleted after 365 days

---

## Project Structure

```
iamnews/
├── main.tf                        # Complete base architecture
├── variables.tf                   # All customization points
├── outputs.tf                     # Deployment outputs
├── terraform.tfvars.example       # Template configuration
├── README.md                      # This file
├── 000-docs/                      # General documentation
│   └── (future docs)
└── brightstream/                  # BrightStream implementation
    ├── terraform.tfvars           # BrightStream-specific config
    └── 000-docs/
        └── 001-AT-ANLY-n8n-to-agentic-conversion.md
```

### Implementation Pattern

Each news implementation gets its own folder with:
1. `terraform.tfvars` - Implementation-specific configuration
2. `000-docs/` - Implementation documentation

**Example:**
```
iamnews/
├── brightstream/      # Positive news
├── techstream/        # Tech news (future)
├── bizstream/         # Business news (future)
└── healthstream/      # Health news (future)
```

---

## Quick Start

### 1. Prerequisites

- Google Cloud Project with billing enabled
- Terraform >= 1.5.0 installed
- `gcloud` CLI authenticated
- Enabled APIs:
  - Vertex AI API
  - Cloud Run API
  - Firestore API
  - Cloud Storage API
  - Cloud Build API

### 2. Create Your Implementation

```bash
# Navigate to iamnews
cd iamnews

# Create your implementation folder
mkdir mystream
mkdir mystream/000-docs

# Copy terraform template
cp terraform.tfvars.example mystream/terraform.tfvars

# Edit configuration
vim mystream/terraform.tfvars
```

### 3. Configure Your Implementation

Edit `mystream/terraform.tfvars`:

```hcl
# Required changes
project_id           = "your-gcp-project-id"
project_display_name = "MyStream"
alert_email          = "your-email@example.com"
genkit_container_image = "gcr.io/your-project-id/mystream-genkit:latest"

# RSS Feeds (customize for your niche)
rss_feeds = [
  {
    url      = "https://example.com/feed.xml"
    name     = "Example News"
    category = "general"
    enabled  = true
  }
]

# Content personality (customize tone/style)
content_tone  = "professional"  # or: uplifting, casual, technical
content_style = "journalistic"  # or: conversational, technical
```

### 4. Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment (review changes)
terraform plan -var-file="mystream/terraform.tfvars"

# Deploy infrastructure
terraform apply -var-file="mystream/terraform.tfvars"
```

### 5. Build Genkit Backend

```bash
# Build Docker image (example)
cd mystream-backend/
docker build -t gcr.io/YOUR_PROJECT_ID/mystream-genkit:latest .

# Push to GCR
docker push gcr.io/YOUR_PROJECT_ID/mystream-genkit:latest
```

### 6. Test Deployment

```bash
# Get outputs
terraform output

# Test root orchestrator
curl $(terraform output -raw genkit_backend_url)/health

# View logs
gcloud run services logs tail $(terraform output -raw genkit_backend_name) \
  --region us-central1
```

---

## Cost Estimates

**Typical monthly costs for single implementation:**

| Component | Monthly Cost | Notes |
|-----------|--------------|-------|
| Firestore | $1-2 | Small data volume |
| Cloud Storage | $1-2 | 50GB with lifecycle rules |
| Cloud Run | $0-5 | Min instances = 0 |
| Vertex AI (Gemini) | $5-10 | Depends on article volume |
| **Total** | **$8-20/month** | Per implementation |

**Cost optimization features:**
- Min instances = 0 (no idle costs)
- Lifecycle rules (auto-cleanup)
- Storage class transitions (standard → nearline → coldline)
- Flash model for most tasks (Pro for complex only)

---

## Key Customization Points

### Content Personality

```hcl
content_tone  = "uplifting"      # uplifting, professional, casual, technical
content_style = "inspirational"  # journalistic, conversational, technical
```

### Story Scoring

```hcl
scoring_criteria = {
  relevance_weight  = 0.30  # How relevant to audience
  quality_weight    = 0.25  # Writing quality
  impact_weight     = 0.25  # Potential impact
  timeliness_weight = 0.20  # How fresh
}
```

### Agent Personalities

```hcl
agent_personalities = {
  content_orchestrator = {
    tone       = "inspiring"
    creativity = 0.4
    formality  = "casual"
    verbosity  = "balanced"
  }
  # ... customize all 11 agents
}
```

### Publishing Schedule

```hcl
publishing_schedule = "0 9 * * *"  # 9 AM daily (cron format)
stories_per_day     = 1
enable_auto_publish = true
```

---

## Implementations

### BrightStream (Positive News)

**Status:** Configuration Complete
**RSS Feeds:** 10 positive news sources
**Content Tone:** Uplifting, inspirational
**Publish Time:** 7 AM daily
**Focus:** Stories that inspire and uplift

**Scoring Weights:**
- Relevance: 25%
- Quality: 25%
- Impact: 35% (higher for positive stories)
- Timeliness: 15%

**See:** `brightstream/terraform.tfvars`

---

## Architecture Patterns

### Google ADK Compliance

This architecture follows official Google Agent Development Kit patterns:

✅ **Root Orchestrator Pattern** - Unified entry point for all requests
✅ **Hierarchical Delegation** - Parent-child agent relationships
✅ **Sessions & Memory Bank** - Context persistence across interactions
✅ **Example Store** - Few-shot learning examples
✅ **Evaluation Services** - Automated performance testing
✅ **ReACT Pattern** - Reasoning + Acting loop
✅ **Reflection Pattern** - Self-critique and improvement
✅ **Tool Specialization** - Principle of least privilege

### Anti-Hallucination System (4 Layers)

**Layer 1: Date Filtering** - Only stories within 48 hours
**Layer 2: Source Verification** - Cross-reference with RSS source list
**Layer 3: Prompt Hardening** - Injection protection
**Layer 4: Temperature Zero** - Deterministic QA agent (temp = 0.0)

---

## Monitoring & Observability

### Built-in Alerts

- **Error Rate Alert** - Triggers at 5% error rate
- **Storage Cost Alert** - Triggers when exceeding threshold
- Email notifications to configured address

### Cloud Monitoring

```bash
# View error logs
gcloud logging read "resource.type=cloud_run_revision \
  AND resource.labels.service_name=iamnews-genkit-production" \
  --limit 50

# Monitor agent performance
gcloud ai endpoints list --region=us-central1

# Check storage usage
gsutil du -sh gs://YOUR_PROJECT-iamnews-media-production/
```

### Analytics Dashboard

- Performance metrics in Firestore `/analytics/` collection
- Daily snapshots in Cloud Storage
- Reflection agent analyzes weekly trends

---

## Development Workflow

### Adding a New Implementation

1. Create implementation folder:
   ```bash
   mkdir newstream newstream/000-docs
   ```

2. Copy and customize tfvars:
   ```bash
   cp terraform.tfvars.example newstream/terraform.tfvars
   ```

3. Deploy with new config:
   ```bash
   terraform apply -var-file="newstream/terraform.tfvars"
   ```

### Updating Base Architecture

1. Modify `main.tf`, `variables.tf`, or `outputs.tf`
2. Test with one implementation first
3. Run `terraform plan` to verify changes
4. Apply to all implementations individually

### Adding New Agents

1. Add agent endpoint in `main.tf`
2. Add agent personality in `variables.tf`
3. Update `outputs.tf` with new endpoint
4. Redeploy infrastructure

---

## Security

### IAM & Service Accounts

- Dedicated service account per deployment
- Principle of least privilege
- Separate permissions for each agent type

### Data Protection

- Firestore security rules (TODO)
- Cloud Storage bucket policies
- VPC Service Controls (optional)
- Secret Manager for credentials

### Access Control

```hcl
allow_public_access = false  # Require authentication
service_account_email = "..."  # Specify authorized SA
```

---

## Troubleshooting

### Common Issues

**Issue:** "Agent not found"
**Solution:** Check agent endpoint ID in outputs:
```bash
terraform output agent_endpoints
```

**Issue:** "Firestore permission denied"
**Solution:** Verify service account has `roles/datastore.user`

**Issue:** "Cloud Run cold starts"
**Solution:** Increase `genkit_min_instances` (costs more)

**Issue:** "Storage costs too high"
**Solution:** Review lifecycle rules, check temp file cleanup

### Debug Commands

```bash
# View all outputs
terraform output

# Check agent status
gcloud ai endpoints describe ENDPOINT_ID --region=us-central1

# View Firestore data
gcloud firestore documents list --database=production

# Test storage access
gsutil ls -r gs://YOUR_BUCKET_NAME/
```

---

## Roadmap

### Completed ✅
- [x] Base architecture with 11 agents
- [x] Firestore + Cloud Storage setup
- [x] Filing system with lifecycle rules
- [x] BrightStream configuration
- [x] Terraform IaC complete

### In Progress 🟡
- [ ] Genkit backend implementation
- [ ] Agent prompt templates
- [ ] Firestore security rules
- [ ] CI/CD pipeline

### Planned 🔴
- [ ] TechStream implementation
- [ ] Multi-language support
- [ ] Video optimization (Veo)
- [ ] Advanced analytics dashboard
- [ ] Cost optimization toolkit

---

## Related Documentation

- **BrightStream N8N Conversion:** `brightstream/000-docs/001-AT-ANLY-n8n-to-agentic-conversion.md`
- **IAM Project Docs:** `../000-docs/` (parent project)
- **Google ADK:** https://google.github.io/adk-docs/
- **Vertex AI Agent Engine:** https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview

---

## Contributing

This is the base architecture for all iamNews implementations. When adding features:

1. Add to base (`main.tf`, `variables.tf`, `outputs.tf`)
2. Make it configurable via variables
3. Test with one implementation first
4. Document in this README

---

## Support

For questions or issues:
1. Check troubleshooting section above
2. Review Terraform outputs
3. Check Cloud Logging for errors
4. Review agent endpoint status

---

**Created:** 2025-10-29
**Last Updated:** 2025-10-29
**Version:** 1.0.0
**License:** Internal Use

---

**Next Steps:**
1. Choose your implementation (BrightStream or create new)
2. Customize `terraform.tfvars`
3. Deploy infrastructure with Terraform
4. Build Genkit backend
5. Test agent workflow end-to-end
