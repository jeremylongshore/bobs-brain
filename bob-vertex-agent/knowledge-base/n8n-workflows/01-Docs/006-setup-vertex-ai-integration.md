# Vertex AI Gemini Integration for N8N
**Date**: 2025-10-04
**N8N Instance**: `/home/jeremy/projects/n8n-workflows/`
**Status**: Industry Standard Setup - ONE AND ONLY

---

## ✅ CONFIRMED: Single N8N Instance

**Location**: `/home/jeremy/projects/n8n-workflows/`
**Access**: http://localhost:5678
**Container**: `n8n` (running 26+ hours)
**Data**: `/home/jeremy/projects/n8n-workflows/data/`

**No duplicates** - Starter kit containers removed.

---

## Vertex AI Gemini Integration (Free Tier)

Since you have **free Vertex AI** access, integrate Gemini 2.0 Flash directly into your existing n8n.

### Step 1: Set Up Google Cloud Credentials

**In n8n UI** (http://localhost:5678):

1. Go to **Credentials** (left sidebar)
2. Click **+ Add Credential**
3. Search for **"Google Cloud"** or **"Google Vertex AI"**
4. Select **Google Cloud Vertex AI**

**Configure**:
- **Project ID**: Your GCP project ID
- **Service Account Email**: `your-sa@project.iam.gserviceaccount.com`
- **Private Key**: Paste JSON key from service account

**Alternative**: Use Application Default Credentials
- Set environment variable in docker-compose.yml:
  ```yaml
  environment:
    - GOOGLE_APPLICATION_CREDENTIALS=/keys/gcp-key.json
  volumes:
    - ./gcp-key.json:/keys/gcp-key.json:ro
  ```

### Step 2: Add Vertex AI Node to Workflows

**In n8n workflow**:

1. Add **HTTP Request** node (Vertex AI doesn't have native node yet)
2. Configure:

```
Method: POST
URL: https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_PROJECT_ID/locations/us-central1/publishers/google/models/gemini-2.0-flash-exp:generateContent

Authentication: Predefined Credential Type
Credential Type: Google Cloud Vertex AI API

Headers:
Content-Type: application/json

Body (JSON):
{
  "contents": [{
    "role": "user",
    "parts": [{
      "text": "{{ $json.prompt }}"
    }]
  }],
  "generation_config": {
    "temperature": 0.1,
    "maxOutputTokens": 500,
    "responseMimeType": "application/json"
  }
}
```

### Step 3: RSS Scoring Workflow Example

**Node 1: HTTP Request (Fetch RSS)**
```
URL: {{ $json.feed_url }}
Method: GET
```

**Node 2: RSS Parser**
```
Parse RSS feed items
```

**Node 3: Function (Prepare Prompt)**
```javascript
const article = $input.first().json;
const prompt = `
Analyze this article for content scoring:

Title: ${article.title}
Source: ${article.source}
Description: ${article.description}

Score 1-5 where:
- 5 = Exceptional, C-suite worthy
- 4 = High quality, technical depth
- 3 = Good, relevant
- 2 = Average
- 1 = Low quality

Output JSON:
{
  "score": <1-5>,
  "category": "AI|Tech|Auto|RV|Survival",
  "brandMatches": ["Intent"|"StartAI"|"DixieRoad"],
  "reasoning": "<50 words>"
}
`;

return {
  json: {
    prompt: prompt,
    articleData: article
  }
};
```

**Node 4: HTTP Request (Vertex AI)**
```
(Configuration from Step 2 above)
```

**Node 5: Function (Parse Response)**
```javascript
const response = $input.first().json;
const aiResponse = JSON.parse(response.candidates[0].content.parts[0].text);

return {
  json: {
    ...$node["Function"].json.articleData,
    score: aiResponse.score,
    category: aiResponse.category,
    brandMatches: aiResponse.brandMatches,
    reasoning: aiResponse.reasoning
  }
};
```

**Node 6: Switch (Brand Routing)**
```
Route 1: score >= 4 AND "Intent" in brandMatches → Intent Solutions
Route 2: score >= 3 AND "StartAI" in brandMatches → StartAITools
Route 3: score >= 3 AND "DixieRoad" in brandMatches → DixieRoad
```

### Step 4: Cost Tracking (Free Tier)

**Vertex AI Free Tier Limits**:
- Gemini 2.0 Flash: First 1M tokens/month free (input)
- Then: $0.075 per 1M input tokens, $0.30 per 1M output tokens

**Your Usage Estimate**:
- 600 articles/day × 1,000 tokens/article = 600K tokens/day
- Monthly: 18M tokens input
- Cost after free tier: ~$1.28/month

**Track in GCP Console**:
- Navigate to: Vertex AI > Usage & Billing
- Monitor token usage daily

### Step 5: Enable Vertex AI API

```bash
gcloud services enable aiplatform.googleapis.com
```

**Verify**:
```bash
gcloud services list --enabled | grep aiplatform
```

---

## Integration Checklist

- [ ] ✅ Confirmed ONE n8n instance (no duplicates)
- [ ] Create GCP service account with Vertex AI permissions
- [ ] Download JSON key for service account
- [ ] Add Google Cloud Vertex AI credentials in n8n
- [ ] Test HTTP Request node with Gemini API
- [ ] Build RSS scoring workflow
- [ ] Monitor Vertex AI usage in GCP Console
- [ ] Track costs (should stay under $2/month)

---

## Advantages Over Starter Kit Ollama

**Starter Kit (Ollama)**:
- Requires 1.76GB download (llama3.2 model)
- Runs locally (CPU intensive)
- Limited to local machine resources
- No cloud scalability

**Vertex AI (Your Setup)**:
- No local model download
- Cloud-powered (scales automatically)
- Free tier: 1M tokens/month
- Enterprise-grade reliability
- Native GCP integration

**Result**: You get cloud AI power without local resource usage. Industry standard. ✅

---

## Next Steps for Enterprise RSS Distribution

Now that you have:
- ✅ ONE n8n instance (industry standard)
- ✅ Free Vertex AI Gemini access
- ✅ Clean setup (no duplicates)

**Build the enterprise RSS workflow**:
1. 138 RSS feeds → HTTP Request nodes (parallel)
2. RSS Parser → Extract articles
3. Vertex AI Gemini → Score articles (1-5)
4. Switch node → Route by brand
5. Blog deployment → StartAITools, Intent Solutions, DixieRoad
6. Social media → LinkedIn + X

**Estimated cost**: $1-2/month (after free tier)
**Processing**: 600-800 articles/day
**Fully automated**: Runs every 4 hours via n8n cron

---

**Document Version**: 1.0.0
**N8N Instance**: CONFIRMED SINGLE SETUP
**AI Provider**: Vertex AI Gemini 2.0 Flash (free tier)
**Last Updated**: 2025-10-04
