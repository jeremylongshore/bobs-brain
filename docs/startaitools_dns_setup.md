# DNS Configuration for startaitools.com

## Current Cloud Run Services

1. **Dashboard**: https://startai-dashboard-157908567967.us-central1.run.app
2. **Portfolio**: https://startai-portfolio-157908567967.us-central1.run.app
3. **Form Handler**: https://website-form-integration-157908567967.us-central1.run.app

## DNS Setup Instructions

### Option 1: Domain Mapping with Cloud Run (Recommended)

#### Step 1: Add Domain Mapping in Cloud Run
```bash
# Map main domain to dashboard
gcloud run domain-mappings create \
  --service=startai-dashboard \
  --domain=startaitools.com \
  --region=us-central1

# Map www subdomain to dashboard
gcloud run domain-mappings create \
  --service=startai-dashboard \
  --domain=www.startaitools.com \
  --region=us-central1

# Map portfolio subdomain
gcloud run domain-mappings create \
  --service=startai-portfolio \
  --domain=portfolio.startaitools.com \
  --region=us-central1

# Map api subdomain for forms
gcloud run domain-mappings create \
  --service=website-form-integration \
  --domain=api.startaitools.com \
  --region=us-central1
```

#### Step 2: Get DNS Records to Add
```bash
gcloud run domain-mappings describe \
  --domain=startaitools.com \
  --region=us-central1
```

### Option 2: Manual DNS Configuration

Add these records to your DNS provider (GoDaddy, Namecheap, Cloudflare, etc.):

#### A Records (if using Load Balancer)
```
Type: A
Name: @
Value: [IP from Load Balancer]
TTL: 3600

Type: A
Name: www
Value: [IP from Load Balancer]
TTL: 3600
```

#### CNAME Records (Direct to Cloud Run)
```
Type: CNAME
Name: @
Value: ghs.googlehosted.com
TTL: 3600

Type: CNAME
Name: www
Value: ghs.googlehosted.com
TTL: 3600

Type: CNAME
Name: portfolio
Value: ghs.googlehosted.com
TTL: 3600

Type: CNAME
Name: api
Value: ghs.googlehosted.com
TTL: 3600
```

## Quick Setup with Cloud Run

### 1. Verify Services are Running
```bash
curl https://startai-dashboard-157908567967.us-central1.run.app/health
curl https://startai-portfolio-157908567967.us-central1.run.app/health
```

### 2. Set Up Domain Mapping
```bash
# This will give you the exact DNS records to add
gcloud beta run domain-mappings create \
  --service startai-dashboard \
  --domain startaitools.com \
  --region us-central1
```

### 3. Add DNS Records
The command above will output something like:
```
Please add the following CNAME records:
- Name: startaitools.com
- Type: CNAME
- Value: ghs.googlehosted.com
```

### 4. SSL Certificate
Cloud Run automatically provisions SSL certificates once DNS is verified (can take up to 24 hours).

## Alternative: Using Cloud Load Balancer

If you want more control:

```bash
# 1. Reserve static IP
gcloud compute addresses create startai-ip \
  --global \
  --ip-version IPV4

# 2. Get the IP address
gcloud compute addresses describe startai-ip --global

# 3. Create NEG for Cloud Run
gcloud compute network-endpoint-groups create startai-neg \
  --region=us-central1 \
  --network-endpoint-type=serverless \
  --cloud-run-service=startai-dashboard

# 4. Set up Load Balancer (more complex)
```

## DNS Provider Settings

### If using Cloudflare:
1. Set proxy status to "DNS only" initially
2. After verification, can enable proxy for CDN/DDoS protection

### If using GoDaddy:
1. Remove any existing A records for @
2. Add CNAME records as shown above
3. Set TTL to 1 hour (3600)

### If using Google Domains:
1. Use Custom resource records
2. Add CNAME records directly
3. Google handles SSL automatically

## Verification

After DNS propagation (5-48 hours):
```bash
# Check DNS resolution
nslookup startaitools.com

# Test the site
curl -I https://startaitools.com

# Check SSL certificate
openssl s_client -connect startaitools.com:443 -servername startaitools.com
```

## Troubleshooting

1. **DNS not resolving**: Wait for propagation (up to 48 hours)
2. **SSL certificate error**: Cloud Run needs 24 hours to provision cert
3. **502 errors**: Check Cloud Run service is running
4. **Wrong service loading**: Verify domain mapping configuration

## Current Status
- ✅ Cloud Run services deployed and running
- ⏳ Awaiting domain mapping configuration
- ⏳ Awaiting DNS record updates
- ⏳ SSL certificate auto-provisioning pending

---
Last Updated: August 15, 2025
