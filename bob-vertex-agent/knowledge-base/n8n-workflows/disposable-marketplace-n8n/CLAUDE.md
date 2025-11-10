# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an N8N workflow project that creates **disposable marketplaces** for instant quote collection from hundreds of resellers. The system allows users to upload a CSV of reseller contacts and automatically collect ranked offers for products (luxury watches, classic cars, art, etc.) within minutes.

## Core Architecture

### Main Components
- **`workflow.json`** - Complete N8N workflow (15KB) with webhook endpoints, CSV processing, and automated outreach
- **`example-resellers.csv`** - Sample reseller data structure with email/API endpoints
- **`test-requests.sh`** - API testing script for workflow validation

### Workflow Structure
The N8N workflow consists of interconnected nodes:
1. **Start Webhook** (`/disposable-marketplace/start`) - Accepts CSV URL and product details
2. **Input Validation** - Validates CSV URLs and product information
3. **CSV Processing** - Fetches and parses reseller data
4. **Batch Processing** - Splits resellers into manageable batches
5. **Dual Outreach** - Sends quotes requests via email and API calls
6. **Offer Collection** (`/disposable-marketplace/offer`) - Webhook for receiving quotes
7. **Ranking System** - Scores offers based on price, trust, response time, and terms
8. **Summary Endpoint** (`/disposable-marketplace/summary`) - Returns top-ranked offers

## Key Endpoints

### Start Collection
```bash
POST /webhook/disposable-marketplace/start
# Requires: csvUrl, product details, callbackBaseUrl
```

### Receive Offers
```bash
POST /webhook/disposable-marketplace/offer
# Webhook for resellers to submit quotes
```

### Get Results
```bash
GET /webhook/disposable-marketplace/summary
# Returns top 5 ranked offers
```

## Development Commands

### Testing Workflow
```bash
# Make test script executable
chmod +x test-requests.sh

# Run complete workflow test
./test-requests.sh

# Test specific endpoints
curl -X POST "https://your-n8n.com/webhook/disposable-marketplace/start" \
  -H "Content-Type: application/json" \
  -d @test-payload.json
```

### N8N Operations
```bash
# Import workflow into N8N instance
# Upload workflow.json through N8N web interface

# Export updated workflow
# Download from N8N interface and replace workflow.json

# Validate JSON structure
jq . workflow.json > /dev/null && echo "Valid JSON"
```

## Configuration Requirements

### N8N Setup
- N8N instance with webhook access
- Google Sheets integration for offer tracking
- SMTP credentials for email outreach
- HTTP Request node permissions for API calls

### Environment Variables
Update the following in the workflow:
- **Webhook URLs**: Replace `YOUR_N8N_URL` in workflow nodes
- **Google Sheets ID**: Configure in Google Sheets nodes
- **SMTP Settings**: Email server credentials for outreach
- **Timeout Settings**: Configurable in workflow (default: 60 minutes)

## Data Flow Architecture

### Input Processing
1. User provides CSV URL with reseller contacts
2. Workflow validates and fetches CSV data
3. Each reseller record requires: `id`, `name`, `email`, `trust_score`, `region`
4. Optional fields: `api_url`, `specialty`

### Scoring Algorithm
```
Final Score = Base Price + Trust Bonus - Time Penalty + Terms Bonus
```
- **Price**: Primary ranking factor
- **Trust Score**: 0-10 scale bonus (from CSV)
- **Response Time**: Penalty for slow responses
- **Terms**: Bonus for favorable payment terms

### Output Format
Top offers include:
- Reseller details and contact information
- Offer price and currency
- Payment terms and conditions
- Trust score and response time
- Final calculated ranking score

## CSV Structure Requirements

Required columns:
```csv
id,name,email,region,trust_score
```

Optional columns:
```csv
api_url,specialty
```

Example:
```csv
ROLEX_SPEC,Rolex Specialists Inc,rolex@rolexspec.com,US,9.5,Rolex Only
```

## Security Considerations

- CSV URLs must be HTTPS and end in `.csv` or `.txt`
- Maximum 500 resellers per batch (configurable)
- Request timeout limits prevent indefinite processing
- No sensitive data stored in workflow; uses temporary processing
- All outreach includes unique request IDs for tracking

## Common Issues

- **Invalid CSV URLs**: Must be publicly accessible HTTPS endpoints
- **SMTP Configuration**: Required for email outreach functionality
- **Google Sheets Permissions**: Needed for offer tracking and summaries
- **Webhook Timeouts**: Long processing times may require timeout adjustments
- **Batch Size Limits**: Large reseller lists may need batch size tuning

## Use Cases

The workflow supports various disposable marketplace scenarios:
- Luxury watches (Rolex, Patek Philippe, Omega)
- Classic cars (Ferrari, Porsche, vintage models)
- Art & collectibles (paintings, rare books, wine)
- Real estate (commercial properties, land)
- Industrial equipment (manufacturing machinery)