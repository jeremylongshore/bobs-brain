# Intent Solutions - Netlify Deployment Guide
**Date**: 2025-10-04
**Project**: Intent Solutions Landing Page
**Repository**: https://github.com/jeremylongshore/intent-solutions-landing

---

## ✅ Setup Complete - Ready to Deploy

**Everything is configured and ready. Just need to import to Netlify.**

### What's Already Done:
1. ✅ Installed Bun runtime
2. ✅ Created `netlify.toml` with build configuration
3. ✅ Saved Netlify auth token to `~/security/netlify-auth-token.txt`
4. ✅ Pushed configuration to GitHub
5. ✅ Repository ready for import

---

## 🚀 Deploy to Netlify (5 Minutes)

### Step 1: Import Repository to Netlify

1. **Open Netlify**: https://app.netlify.com/
2. **Login**: jeremylongshore@gmail.com
3. **Click**: "Add new site" → "Import an existing project"
4. **Choose**: GitHub
5. **Select repository**: `jeremylongshore/intent-solutions-landing`
6. **Netlify auto-detects settings** from `netlify.toml`:
   - Build command: `bun install && bun run build`
   - Publish directory: `dist`
   - Base directory: (leave empty)
7. **Click**: "Deploy site"
8. **Wait 2-3 minutes** for build to complete

### Step 2: Verify Deployment

Your site will be live at a temporary URL like:
```
https://intent-solutions-abc123.netlify.app
```

**Test the site** - make sure it loads correctly.

---

## 🌐 Add Custom Domain (intentsolutions.io)

### Step 3: Configure Custom Domain in Netlify

1. **In Netlify dashboard** → Go to your new site
2. **Click**: "Site settings" → "Domain management"
3. **Click**: "Add custom domain"
4. **Enter**: `intentsolutions.io`
5. **Click**: "Verify" → "Add domain"

Netlify will show you DNS configuration instructions.

### Step 4: Update DNS in Porkbun

**Login to Porkbun**: https://porkbun.com/account/domainsSpeedy

**Find**: `intentsolutions.io` domain

**Add these DNS records**:

#### A Record (Root Domain)
```
Type: A
Host: @  (or leave blank)
Answer: 75.2.60.5
TTL: 600
```

#### CNAME Record (www subdomain)
```
Type: CNAME
Host: www
Answer: [your-site-name].netlify.app  (from Netlify)
TTL: 600
```

**Example CNAME value**: `intent-solutions-abc123.netlify.app`

### Step 5: Wait for DNS Propagation

- **Typical time**: 5-10 minutes
- **Maximum time**: 24-48 hours (rare)
- **Check status**: https://www.whatsmydns.net/#A/intentsolutions.io

---

## 🔒 Enable HTTPS (Automatic)

Netlify automatically provisions SSL certificate from Let's Encrypt.

**After DNS propagates**:
1. Go to Netlify → Site settings → Domain management
2. Click "Verify DNS configuration"
3. Click "Provision certificate" (if not automatic)
4. Wait 1-2 minutes
5. ✅ HTTPS enabled at https://intentsolutions.io

---

## 📋 Post-Deployment Checklist

- [ ] Site deployed to Netlify
- [ ] Test temporary Netlify URL
- [ ] Custom domain `intentsolutions.io` added in Netlify
- [ ] DNS A record added in Porkbun (@ → 75.2.60.5)
- [ ] DNS CNAME added in Porkbun (www → netlify.app)
- [ ] DNS propagated (check whatsmydns.net)
- [ ] HTTPS certificate provisioned
- [ ] Test https://intentsolutions.io
- [ ] Test https://www.intentsolutions.io (should redirect to non-www)

---

## 🛠️ Configuration Details

### Netlify Configuration (netlify.toml)

```toml
[build]
  command = "bun install && bun run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"
  BUN_VERSION = "1.0.0"

# HTTP → HTTPS redirect
[[redirects]]
  from = "http://intentsolutions.io/*"
  to = "https://intentsolutions.io/:splat"
  status = 301
  force = true

# www → non-www redirect
[[redirects]]
  from = "https://www.intentsolutions.io/*"
  to = "https://intentsolutions.io/:splat"
  status = 301
  force = true

# SPA routing (React Router)
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Authentication

**Netlify Auth Token** (stored securely):
- Location: `~/security/netlify-auth-token.txt`
- Permissions: chmod 600 (owner read-only)
- Account: jeremylongshore@gmail.com

---

## 🔧 Troubleshooting

### Build Fails

**Check Netlify build logs**:
1. Netlify dashboard → Deploys → Failed deploy
2. Click "Deploy log"
3. Look for error messages

**Common issues**:
- Missing dependencies → Check package.json
- Bun version mismatch → Update BUN_VERSION in netlify.toml
- Build command wrong → Verify in netlify.toml

### DNS Not Working

**Verify DNS records**:
```bash
dig intentsolutions.io
dig www.intentsolutions.io
```

**Should show**:
- A record: 75.2.60.5
- CNAME: [site].netlify.app

**Check propagation**: https://www.whatsmydns.net/

### HTTPS Not Enabling

1. Verify DNS is fully propagated
2. Netlify → Domain settings → "Verify DNS configuration"
3. Wait 5-10 minutes
4. Click "Provision certificate" if needed

---

## 📞 Support

**Netlify Account**: jeremylongshore@gmail.com
**GitHub Repo**: https://github.com/jeremylongshore/intent-solutions-landing
**DNS Provider**: Porkbun.com

**Existing Netlify Sites** (for reference):
- startaitools.com (https://startaitools.com)
- jeremylongshore.com (https://jeremylongshore.com)

---

## 🎯 Next Steps After Deployment

1. **Test all pages** on live site
2. **Verify contact forms** work correctly
3. **Check mobile responsiveness**
4. **Test page load speed** (Google PageSpeed Insights)
5. **Add to Google Search Console**
6. **Submit sitemap** to search engines
7. **Set up analytics** (Google Analytics)

---

**Ready to deploy! Start at Step 1: https://app.netlify.com/**
