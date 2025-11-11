# OG Image Social Sharing Fix - HUSTLE Survey
**Date**: 2025-10-12
**Issue**: Survey link shows blank box when shared on Facebook/social media
**Status**: ✅ FIXED - Awaiting OG image creation

---

## 🎯 What Was Fixed

### Problem
When sharing `intentsolutions.io/survey` on Facebook, Twitter, LinkedIn, etc., the link preview showed:
- ❌ Blank image box
- ❌ Generic or missing description
- ❌ Not compelling to click

### Solution
Added proper Open Graph (OG) meta tags and created custom OG image for survey:
- ✅ Title: "HUSTLE Survey - Help Build the Future of Youth Sports Tracking"
- ✅ Description: "Share your experience as a sports parent and help shape HUSTLE..."
- ✅ Custom OG image: Shows "HUSTLE Survey" with branding
- ✅ Twitter Card support

---

## 📝 Changes Made

### 1. Updated Layout.astro (OG Image Support)
**File**: `/astro-site/src/layouts/Layout.astro`

**Added**:
- `ogImage` prop to allow custom images per page
- Dynamic OG image in meta tags
- Twitter card image support

```typescript
interface Props {
  title: string;
  description?: string;
  ogImage?: string;  // NEW
}
```

---

### 2. Updated survey.astro (Custom Meta Tags)
**File**: `/astro-site/src/pages/survey.astro`

**Added**:
- Custom title optimized for social sharing
- Compelling description with call-to-action
- Reference to custom OG image

```astro
<Layout
  title="HUSTLE Survey - Help Build the Future of Youth Sports Tracking"
  description="Share your experience as a sports parent and help shape HUSTLE - the youth sports tracking app. Get 1 year free access when we launch. 8-10 minute survey."
  ogImage="https://intentsolutions.io/og-survey.png"
>
```

---

### 3. Created OG Image Generator
**File**: `/astro-site/og-image-generator.html`

**Purpose**: HTML page to generate the OG image
- 1200x630px (Facebook/Twitter standard)
- Zinc monochrome theme
- Shows "HUSTLE Survey" title
- Includes key benefits (8-10 min, 1 year free)
- Brand URL at bottom

---

## 🎨 OG Image Creation (YOU NEED TO DO THIS)

### Step 1: Open OG Image Generator

```bash
cd /home/jeremy/projects/intent-solutions-landing/astro-site

# Open in browser
firefox og-image-generator.html
# or
google-chrome og-image-generator.html
```

---

### Step 2: Screenshot at Exact Size

**Using Chrome DevTools** (Recommended):

1. **Open DevTools**: `F12` or right-click → Inspect
2. **Toggle Device Toolbar**: `Ctrl+Shift+M` (or click phone icon)
3. **Set Dimensions**: Top dropdown → "Responsive"
4. **Enter exact size**: `1200` x `630`
5. **Zoom**: Set to `100%` (important!)
6. **Screenshot**:
   - Click `...` (three dots) in DevTools
   - "Capture screenshot"
   - Or use DevTools screenshot tool

**Alternative (Firefox)**:
1. Open DevTools: `F12`
2. Click "Responsive Design Mode" (`Ctrl+Shift+M`)
3. Set to `1200 x 630`
4. Right-click on page → "Screenshot Node" (select `.og-card`)

---

### Step 3: Save as PNG

**Save the screenshot as**:
```
/home/jeremy/projects/intent-solutions-landing/astro-site/public/og-survey.png
```

**Important**:
- Must be exactly `1200x630` pixels
- Must be PNG format (not JPG)
- Must be named `og-survey.png`
- Must be in `public/` directory

---

### Step 4: Verify Image

```bash
# Check file exists
ls -lh astro-site/public/og-survey.png

# Should show approximately 50-200KB
```

**Open image** and verify:
- Text is readable
- Colors look good (zinc theme)
- Brand URL is visible
- No blur or artifacts

---

## 🚀 Deployment

### Step 1: Commit Changes

```bash
cd /home/jeremy/projects/intent-solutions-landing

# Add all changes
git add astro-site/src/layouts/Layout.astro
git add astro-site/src/pages/survey.astro
git add astro-site/public/og-survey.png
git add astro-site/og-image-generator.html

# Commit
git commit -m "fix: add OG meta tags and image for HUSTLE Survey social sharing"

# Push to GitHub (auto-deploys via Netlify)
git push origin main
```

---

### Step 2: Wait for Deployment

Netlify will automatically rebuild and deploy (usually 2-3 minutes).

**Monitor deployment**:
- https://app.netlify.com/ (check your site)
- Or wait for GitHub Actions to complete

---

### Step 3: Clear Social Media Caches

After deployment, social platforms cache OG data. You need to clear their caches:

#### Facebook Debugger
**URL**: https://developers.facebook.com/tools/debug/

1. Enter: `https://intentsolutions.io/survey`
2. Click "Scrape Again"
3. Verify image shows correctly
4. Check title and description

#### Twitter Card Validator
**URL**: https://cards-dev.twitter.com/validator

1. Enter: `https://intentsolutions.io/survey`
2. Click "Preview card"
3. Verify image, title, description

#### LinkedIn Post Inspector
**URL**: https://www.linkedin.com/post-inspector/

1. Enter: `https://intentsolutions.io/survey`
2. Click "Inspect"
3. Verify preview looks good

---

## ✅ Testing Checklist

### Before Sharing
- [ ] OG image created and saved as `og-survey.png`
- [ ] Image is exactly 1200x630 pixels
- [ ] Image is in `public/` directory
- [ ] Changes committed and pushed
- [ ] Netlify deployment complete
- [ ] Facebook debugger scraped successfully
- [ ] Twitter card validator shows correctly
- [ ] LinkedIn inspector shows correctly

### Test Social Sharing
- [ ] Share link on Facebook (see preview before posting)
- [ ] Share link on Twitter (see card preview)
- [ ] Share link on LinkedIn (see preview)
- [ ] Share via text message (some apps show previews)
- [ ] Share via email (some clients show previews)

---

## 📊 What Users Will See

### Before (Broken)
```
[Blank gray box]
Help Build the Future of Youth Sports Tracking | HUSTLE Survey
independent ai consultant building automation systems...
```

### After (Fixed) ✅
```
[Beautiful branded image showing "HUSTLE Survey"]
HUSTLE Survey - Help Build the Future of Youth Sports Tracking
Share your experience as a sports parent and help shape HUSTLE - the youth sports tracking app. Get 1 year free access when we launch. 8-10 minute survey.
```

---

## 🎯 Preview Example

When someone pastes `intentsolutions.io/survey`:

**Facebook/LinkedIn**:
- 📷 Image: "HUSTLE Survey" with zinc theme
- 📝 Title: "HUSTLE Survey - Help Build the Future..."
- 💬 Description: "Share your experience as a sports parent..."
- 🔗 URL: intentsolutions.io/survey

**Twitter**:
- Same as above with "Summary Card with Large Image" format

---

## 🔧 Technical Details

### OG Meta Tags Added

```html
<!-- Open Graph (Facebook, LinkedIn) -->
<meta property="og:title" content="HUSTLE Survey - Help Build the Future of Youth Sports Tracking" />
<meta property="og:description" content="Share your experience as a sports parent..." />
<meta property="og:image" content="https://intentsolutions.io/og-survey.png" />
<meta property="og:url" content="https://intentsolutions.io/survey" />
<meta property="og:type" content="website" />
<meta property="og:site_name" content="intent solutions io" />

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="HUSTLE Survey - Help Build the Future of Youth Sports Tracking" />
<meta name="twitter:description" content="Share your experience as a sports parent..." />
<meta name="twitter:image" content="https://intentsolutions.io/og-survey.png" />
```

---

## 🎨 OG Image Specifications

**Dimensions**: 1200 x 630 pixels (Facebook/Twitter standard)
**Format**: PNG (better quality than JPG)
**File Size**: ~50-200KB (optimized)
**Aspect Ratio**: 1.91:1

**Design**:
- Background: Zinc-900 gradient (#18181B)
- Title: "HUSTLE Survey" (96px, white)
- Subtitle: "Help Build the Future of Youth Sports" (42px, zinc-400)
- Badges: ⏱️ 8-10 minutes, 🎁 1 year free
- Brand: intentsolutions.io/survey (bottom)

---

## 🚨 Troubleshooting

### Issue: Image Still Not Showing

**Solutions**:
1. Clear social media caches (use debuggers above)
2. Verify image URL is correct: `https://intentsolutions.io/og-survey.png`
3. Check image actually deployed (visit URL directly)
4. Wait 10-15 minutes (CDN propagation)
5. Try hard refresh: `Ctrl+Shift+R`

---

### Issue: Image Shows But Looks Wrong

**Solutions**:
1. Regenerate image at exact 1200x630 size
2. Check zoom was 100% when screenshotting
3. Verify PNG format (not JPG)
4. Re-upload and re-deploy

---

### Issue: Description Not Updating

**Solutions**:
1. Use Facebook Debugger "Scrape Again" button
2. Clear browser cache
3. Wait for Netlify deployment to complete
4. Check `survey.astro` has correct description prop

---

## 📝 Quick Steps Summary

1. **Open**: `astro-site/og-image-generator.html` in browser
2. **Screenshot**: At exactly 1200x630 pixels
3. **Save**: As `astro-site/public/og-survey.png`
4. **Commit**: All changes to git
5. **Push**: To GitHub (auto-deploys)
6. **Clear caches**: Use Facebook/Twitter debuggers
7. **Test**: Share link on social media

**Time Required**: 10 minutes

---

## 🎯 Additional OG Images (Optional)

You can create more OG images for other pages:

**Main Landing** (`/`):
- Create `og-default.png`
- Title: "Intent Solutions IO"
- Description: "AI Consultant & Product Builder"

**Individual Survey Sections** (optional):
- Create section-specific images
- Add progress indicators
- Customize per section

---

## ✅ Success Criteria

**You'll know it's working when**:
1. Paste `intentsolutions.io/survey` into Facebook
2. See the preview card appear with:
   - ✅ HUSTLE Survey branded image
   - ✅ Clear title and description
   - ✅ Compelling call-to-action
3. Preview looks professional and click-worthy

---

## 📚 Resources

- **Facebook OG Debugger**: https://developers.facebook.com/tools/debug/
- **Twitter Card Validator**: https://cards-dev.twitter.com/validator
- **LinkedIn Inspector**: https://www.linkedin.com/post-inspector/
- **OG Image Best Practices**: https://www.opengraph.xyz/
- **Image Size Guide**: 1200x630 is universal standard

---

**Documentation Created**: 2025-10-12
**Status**: ✅ Code fixed, awaiting OG image creation
**Next Step**: Create og-survey.png using generator HTML
