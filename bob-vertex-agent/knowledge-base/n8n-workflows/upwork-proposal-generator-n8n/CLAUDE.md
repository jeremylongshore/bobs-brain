# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Upwork Proposal Generator is an automated N8N workflow that analyzes Upwork job listings, scores them based on custom criteria, and generates tailored proposals using AI.

**Status**: Production-ready workflow
**Created**: 2025-10-04
**Workflow Type**: Job application automation
**Complexity**: 10 nodes, AI-powered scoring and proposal generation

## Quick Commands

```bash
# Navigate to workflow directory
cd /home/jeremy/projects/n8n-workflows/upwork-proposal-generator-n8n

# Validate workflow JSON
jq . workflow.json > /dev/null && echo "Valid JSON"

# Import workflow into N8N (requires N8N CLI or API)
n8n import:workflow --input=workflow.json

# View workflow structure
jq '.nodes[] | {name: .name, type: .type}' workflow.json
```

## Workflow Architecture

### Purpose
Automate the process of:
1. Finding relevant Upwork jobs via Apify scraper
2. Scoring jobs with AI (1-5 scale) based on custom criteria
3. Filtering jobs above score threshold
4. Generating personalized proposals with GPT-5-mini
5. Storing results in Google Sheets for tracking

### Node Breakdown

**Total Nodes**: 10

| Node | Type | Function | Key Dependencies |
|------|------|----------|-----------------|
| When clicking 'Execute workflow' | Manual Trigger | Start workflow | None |
| Run an Actor | Apify | Scrape Upwork jobs | Apify credentials |
| Get dataset items | Apify | Retrieve scraped data | Apify credentials |
| Limit | Limit | Cap processing (optional) | None |
| Edit Fields | Set | Define scoring criteria | None |
| Message a model | OpenAI | AI scoring (GPT-5-mini) | OpenAI API key |
| Filter | Filter | Keep score >= 1 | None |
| Loop Over Items | Split In Batches | Process sequentially | None |
| Message a model1 | OpenAI | Generate proposals | OpenAI API key |
| Append or update row in sheet | Google Sheets | Store results | Google OAuth2 |

### Data Flow

```
Manual Trigger
    ↓
Apify Actor (Upwork Job Scraper)
    ↓
Get Dataset Items (Job listings with metadata)
    ↓
Limit (Optional: process first N jobs)
    ↓
Edit Fields (Set scoring rules + proposal template)
    ↓
Message a model (AI scoring: 1-5 scale)
    ↓
Filter (Keep jobs with score >= 1)
    ↓
Loop Over Items (Batch processing)
    ↓
Message a model1 (Generate custom proposal)
    ↓
Google Sheets (Store job + proposal + score)
    ↓
Loop (Continue until all jobs processed)
```

## Critical Configuration

### 1. Apify Actor Settings
**Node**: "Run an Actor"
```json
{
  "actorId": "XYTgO05GT5qAoSlxy",
  "customBody": {
    "query": "make.com"  // Change this to your search term
  }
}
```

**Common search queries**:
- `"n8n automation"`
- `"make.com integration"`
- `"airtable automation"`
- `"workflow automation"`

### 2. Scoring Criteria
**Node**: "Edit Fields" → assignments → score
```
I'm looking for a job that pays a fixed rate over $1000, or is at least $50 USD/hour. Scoring is out of 5 and here's how points are awarded:
– 2 points if it's super related to n8n, Make.com or Airtable, or 1 point if it's somewhat related to one of them
– 1 point if it's over $50 USD/hour or a fixed rate over $1,000
– 1 point if the fixed rate contract
– 1 point if it's a service based business
```

**Customization**: Edit this text to change scoring logic

### 3. Proposal Template
**Node**: "Edit Fields" → assignments → proposal
```
Hello, my name is Nicola. I'm an AI automation expert and entrepreneur who has founded two companies that collectively generate $170,000 in monthly recurring revenue. I have a proven track record in business and specialize in building automations that drive real results. I'd love to create the same value for you and establish a long-term business relationship.

Why choose me?
	•	I founded an e-commerce store generating over $100K in MRR
	•	I built a vacation rental company that operates on autopilot, producing $70K in MRR
	•	I helped a CPA firm save 30 hours per week through document management automation

I believe there's a great opportunity for us to work together. Are you available for a call tomorrow to discuss the details?
Best regards, Nicola
```

**IMPORTANT**: Update this with YOUR credentials, name, and examples

### 4. AI Model Configuration
**Node**: "Message a model" (Scoring)
```json
{
  "modelId": "gpt-5-mini",
  "temperature": 0.0  // Deterministic scoring
}
```

**Node**: "Message a model1" (Proposal Generation)
```json
{
  "modelId": "gpt-5-mini",
  "temperature": 0.2  // Slight creativity for proposals
}
```

### 5. Google Sheets Setup
**Node**: "Append or update row in sheet"
```json
{
  "documentId": "1eiAPspwYVMZ_ieBaI_eI0y7pFPqxLREyPkQQ33nIvtc",
  "sheetName": "Foglio1",
  "matchingColumns": ["Job title"]  // Deduplication key
}
```

**Required columns**:
- Job title
- Job Description
- Budget
- Job type
- Client rating
- Client hire rate %
- Client total spent
- Client location
- Experience level
- Score
- Proposal text
- Date found
- Date submitted
- Link to job

## Required Credentials

### Apify OAuth2 API
- **Credential ID**: `xgne1WHIiozClkAi`
- **Name**: "Apify account"
- **Setup**: N8N Credentials Manager → Apify OAuth2 API

### OpenAI API
- **Credential ID**: `SA2epS7nRWo9arvt`
- **Name**: "251003_Open AI"
- **Setup**: N8N Credentials Manager → OpenAI API
- **Model**: GPT-5-mini (cost-effective for high-volume processing)

### Google Sheets OAuth2
- **Credential ID**: `WGlszVKNryFYQ1vj`
- **Name**: "Google Sheets account 3"
- **Setup**: N8N Credentials Manager → Google Sheets OAuth2 API
- **Permissions**: Read/write access to target spreadsheet

## Common Modifications

### Change Search Query
Update Apify Actor node:
```json
{
  "customBody": {
    "query": "YOUR_SEARCH_TERM"
  }
}
```

### Adjust Score Threshold
Update Filter node:
```json
{
  "conditions": [
    {
      "leftValue": "={{ $json.message.content.toNumber() }}",
      "rightValue": 3,  // Change from 1 to 3 for stricter filtering
      "operator": {
        "type": "number",
        "operation": "gte"
      }
    }
  ]
}
```

### Add Rate Limiting
Insert "Wait" node after "Message a model1":
```json
{
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 2,
    "unit": "seconds"
  }
}
```

### Limit Jobs Processed
Update "Limit" node:
```json
{
  "parameters": {
    "maxItems": 10  // Process only 10 jobs per run
  }
}
```

## Troubleshooting

### Issue: Apify Actor Times Out
**Cause**: Large search query or Apify platform issues
**Solution**:
1. Check Apify Actor status in Apify dashboard
2. Reduce search query scope
3. Add timeout handling in N8N

### Issue: AI Returns Invalid Scores
**Cause**: Prompt unclear or model hallucinating
**Solution**:
1. Check "Message a model" prompt clarity
2. Add explicit instructions: "Output ONLY a number 1-5"
3. Set temperature to 0 for deterministic output

### Issue: Proposals Not Generated
**Cause**: Jobs filtered out by score threshold
**Solution**:
1. Lower Filter threshold (e.g., >= 1 instead of >= 3)
2. Adjust scoring criteria to be less strict
3. Check Limit node isn't excluding too many jobs

### Issue: Google Sheets Authentication Fails
**Cause**: OAuth token expired
**Solution**:
1. Reconnect Google Sheets credentials in N8N
2. Grant necessary permissions again
3. Test connection before running workflow

### Issue: Duplicate Jobs in Spreadsheet
**Cause**: Matching column not working
**Solution**:
1. Verify "matchingColumns" is set to "Job title"
2. Check for slight title variations (whitespace, punctuation)
3. Consider using URL as unique identifier instead

## Performance Optimization

### Current Performance
- **Processing time**: ~20-30 seconds per job
- **Cost per job**: ~$0.01-0.03 (GPT-5-mini)
- **Bottleneck**: AI proposal generation

### Optimization Strategies

**1. Batch API Calls**
Combine multiple jobs into single API request:
```json
// Instead of: Loop → AI call → Loop
// Use: Batch jobs → Single AI call with JSON array
```

**2. Cache Similar Jobs**
If job descriptions are similar, reuse proposals:
```javascript
// Add Code node to check if similar job exists
if (similarity > 0.9) {
  return cached_proposal;
}
```

**3. Parallel Processing**
Split jobs into batches and process concurrently:
```
Loop Over Items → Set batchSize: 5
```

**4. Reduce Limit Node**
Process fewer jobs per run:
```json
{
  "maxItems": 5  // Start small, scale up
}
```

## File Structure

```
upwork-proposal-generator-n8n/
├── workflow.json          # N8N workflow definition
├── README.md             # User-facing documentation
└── CLAUDE.md             # AI development guide (this file)
```

## Integration Points

### Upstream Data Sources
- **Apify Upwork Job Scraper**: XYTgO05GT5qAoSlxy
- **Search query**: Configurable via workflow

### Downstream Storage
- **Google Sheets**: Spreadsheet ID 1eiAPspwYVMZ_ieBaI_eI0y7pFPqxLREyPkQQ33nIvtc
- **Sheet**: Foglio1 (gid=0)

### External APIs
- **OpenAI GPT-5-mini**: Scoring and proposal generation
- **Apify Platform**: Job scraping actor

## Version Control

**Current Version**: 1.0.0
**Workflow ID**: kxLOEK2pOWeRfyKs
**Version ID**: 59e71b1f-2a8b-4752-9161-4ac77fbfee72

### Version History
- **1.0.0** (2025-10-04): Initial workflow creation

## Related Workflows

- **Daily Energizer**: Content generation from RSS feeds
- **News Pipeline**: Tech news intelligence automation
- **Disposable Marketplace**: Instant marketplace creation
- **Gmail Drive Organizer**: Email attachment automation

## Best Practices

### Before Running
1. Test with Limit node set to 5 jobs
2. Verify all credentials are connected
3. Check Google Sheets has correct columns
4. Review scoring criteria for your needs

### During Development
1. Enable "Save Execution Progress" in workflow settings
2. Use Error Trigger node for production monitoring
3. Log failed jobs to separate sheet for review
4. Monitor OpenAI API costs

### After Deployment
1. Review first 10-20 generated proposals manually
2. Adjust scoring criteria based on false positives
3. Update proposal template quarterly
4. Monitor success rate (interviews/applications)

## Security Considerations

### Credentials
- Never commit credentials to git
- Use N8N's secure credential storage
- Rotate API keys quarterly

### Data Privacy
- Job listings may contain sensitive client info
- Store Google Sheets securely (private access only)
- Consider GDPR compliance for EU clients

### API Usage
- Set reasonable Limit node values (avoid runaway costs)
- Monitor OpenAI usage dashboard
- Implement error handling to prevent infinite loops

## Support & Maintenance

### Regular Maintenance Tasks
- **Monthly**: Review and update proposal template
- **Quarterly**: Audit scoring criteria accuracy
- **Yearly**: Rotate API credentials

### Known Limitations
- Apify Actor may rate-limit for high-volume scraping
- GPT-5-mini occasionally generates formatting errors
- Google Sheets API has rate limits (100 requests/100 seconds per user)

### Future Enhancements
- [ ] Add Slack notification when high-scoring jobs found
- [ ] Implement A/B testing for different proposal templates
- [ ] Add sentiment analysis to client feedback
- [ ] Integrate with Upwork API (when available) for direct submission

---

**Last Updated**: 2025-10-04
**Status**: ✅ Production-ready
**Maintainer**: n8n-workflows repository
