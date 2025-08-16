# DNS Setup for startaitools.com

## Current DNS Records to KEEP:
- MX records (fwd1.porkbun.com, fwd2.porkbun.com) - Keep these for email
- SPF TXT record - Keep this for email
- ACME challenge TXT records - Keep these for SSL

## Records to ADD/CHANGE:

### For www.startaitools.com:
- **Type:** CNAME
- **Host:** www
- **Value:** ghs.googlehosted.com.
- **TTL:** 600

### For startaitools.com (apex/root):
Delete the current A record (35.225.160.0) and add these 4 A records (or use ALIAS if Porkbun supports it):
- **Type:** A
- **Host:** @
- **Value:** 216.239.32.21
- **TTL:** 600

- **Type:** A
- **Host:** @
- **Value:** 216.239.34.21
- **TTL:** 600

- **Type:** A
- **Host:** @
- **Value:** 216.239.36.21
- **TTL:** 600

- **Type:** A
- **Host:** @
- **Value:** 216.239.38.21
- **TTL:** 600

### For domain verification (if needed):
- **Type:** TXT
- **Host:** @
- **Value:** google-site-verification=YOUR_VERIFICATION_CODE
- **TTL:** 600

## After DNS Updates:
1. Wait 5-10 minutes for DNS propagation
2. Run domain verification in GCP
3. Create the domain mapping to Cloud Run service
