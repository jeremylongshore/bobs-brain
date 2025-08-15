# Porkbun DNS Configuration for startaitools.com

## Step-by-Step Porkbun Setup

### 1. Login to Porkbun
Go to https://porkbun.com and login to your account

### 2. Access DNS Settings
- Click on **Domain Management**
- Find **startaitools.com**
- Click **DNS** button next to your domain

### 3. Delete Default Records
Remove any existing A records for @ and www (Porkbun adds defaults)

### 4. Add These DNS Records

#### Main Website (startaitools.com)
```
Type: ALIAS (or CNAME)
Host: (leave blank for root)
Answer: startai-dashboard-157908567967.us-central1.run.app
TTL: 600
```

#### WWW Subdomain
```
Type: CNAME
Host: www
Answer: startai-dashboard-157908567967.us-central1.run.app
TTL: 600
```

#### Portfolio Subdomain
```
Type: CNAME
Host: portfolio
Answer: startai-portfolio-157908567967.us-central1.run.app
TTL: 600
```

#### API Subdomain (for forms)
```
Type: CNAME
Host: api
Answer: website-form-integration-157908567967.us-central1.run.app
TTL: 600
```

### 5. Domain Verification (Optional but Recommended)
To enable Cloud Run domain mapping later:

```
Type: TXT
Host: (leave blank)
Answer: google-site-verification=YOUR_VERIFICATION_CODE
TTL: 600
```

(Get verification code from Google Search Console)

## Exact Porkbun Interface Steps

1. **Login** → https://porkbun.com/account/login

2. **Navigate** → Account → Domain Management

3. **Find Domain** → Click "Details" dropdown → Select "DNS"

4. **Clear Defaults**:
   - Delete any A records for "*" and blank host
   - Delete ALIAS record if exists
   - Keep MX records if using email

5. **Add Root Domain**:
   - Click "Add Record"
   - Type: Select "ALIAS"
   - Host: Leave completely empty
   - Answer: `startai-dashboard-157908567967.us-central1.run.app`
   - TTL: 600
   - Priority: Leave blank
   - Click "Add Record"

6. **Add WWW**:
   - Click "Add Record"
   - Type: Select "CNAME"
   - Host: `www`
   - Answer: `startai-dashboard-157908567967.us-central1.run.app`
   - TTL: 600
   - Click "Add Record"

7. **Add Portfolio**:
   - Click "Add Record"
   - Type: Select "CNAME"
   - Host: `portfolio`
   - Answer: `startai-portfolio-157908567967.us-central1.run.app`
   - TTL: 600
   - Click "Add Record"

8. **Add API**:
   - Click "Add Record"
   - Type: Select "CNAME"
   - Host: `api`
   - Answer: `website-form-integration-157908567967.us-central1.run.app`
   - TTL: 600
   - Click "Add Record"

## Important Porkbun Notes

### Root Domain Setup
- Porkbun supports ALIAS records for root domain (better than CNAME)
- If ALIAS doesn't work, use their "URL Forwarding" to redirect root to www

### SSL/HTTPS
- Cloud Run provides free SSL certificates
- No need to buy SSL from Porkbun
- Certificates auto-provision in 15-60 minutes after DNS propagates

### Email Settings
- Keep existing MX records if you use email
- Don't delete TXT records for email authentication (SPF, DKIM)

## Verify DNS Propagation

After 5-30 minutes, test:

```bash
# Check DNS resolution
nslookup startaitools.com
nslookup www.startaitools.com
nslookup portfolio.startaitools.com

# Test with dig
dig startaitools.com
dig www.startaitools.com

# Check if site loads (may take up to 1 hour)
curl -I https://startaitools.com
```

## Troubleshooting

### If Root Domain Doesn't Work:
Porkbun alternative approach:
1. Set up URL forwarding for root domain
2. Forward startaitools.com → www.startaitools.com
3. Use CNAME only for www subdomain

### URL Forwarding Setup (if needed):
1. In Porkbun DNS page
2. Click "URL Forwarding"
3. Add forward:
   - From: startaitools.com
   - To: https://www.startaitools.com
   - Type: Temporary (302) or Permanent (301)
   - Include path: Yes
   - Enable wildcard: No

## Quick Copy-Paste Values

For easy copying into Porkbun:

**Dashboard Service:**
```
startai-dashboard-157908567967.us-central1.run.app
```

**Portfolio Service:**
```
startai-portfolio-157908567967.us-central1.run.app
```

**API Service:**
```
website-form-integration-157908567967.us-central1.run.app
```

## Expected Result

After DNS propagates (5-60 minutes):
- ✅ https://startaitools.com → StartAI Dashboard
- ✅ https://www.startaitools.com → StartAI Dashboard
- ✅ https://portfolio.startaitools.com → Portfolio Site
- ✅ https://api.startaitools.com → Form Handler API

## Status Checklist
- [ ] Logged into Porkbun
- [ ] Deleted default A records
- [ ] Added ALIAS/CNAME for root
- [ ] Added CNAME for www
- [ ] Added CNAME for portfolio
- [ ] Added CNAME for api
- [ ] Saved all changes
- [ ] Tested with nslookup
- [ ] Site loads with HTTPS

---
Porkbun Support: support@porkbun.com
Last Updated: August 15, 2025
