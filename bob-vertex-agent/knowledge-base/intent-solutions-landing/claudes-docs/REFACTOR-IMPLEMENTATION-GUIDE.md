# Intent Solutions IO - Complete Refactor Implementation Guide

**Generated**: 2025-11-03
**Purpose**: Comprehensive instructions for implementing the site-wide refactor

---

## Table of Contents

1. [Overview](#overview)
2. [New Files Created](#new-files-created)
3. [Existing Files - Required Updates](#existing-files---required-updates)
4. [Navigation Updates](#navigation-updates)
5. [SEO & Meta Updates](#seo--meta-updates)
6. [Testing Checklist](#testing-checklist)
7. [Deployment Steps](#deployment-steps)

---

## Overview

This refactor implements:
- Model-agnostic positioning (no vendor lock-in)
- "Example MVP" messaging (removing "3 agents" cap)
- Education hub (/learn) with pricing, security, and models pages
- Resellers program with white-label offerings
- Transparent pricing model (flat fee + usage pass-through)
- Vertex vs self-hosted security positioning

---

## New Files Created

All new files have been created in the project:

### Components
- ✅ `/src/components/MvpShowcase.tsx` - Modal showing example MVP configuration
- ✅ `/src/components/PricingBlocks.tsx` - Shared pricing component

### Pages
- ✅ `/src/pages/resellers.astro` - Reseller & white-label program
- ✅ `/src/pages/learn/index.astro` - Education hub landing
- ✅ `/src/pages/learn/pricing.astro` - How pricing works
- ✅ `/src/pages/learn/security.astro` - Security comparison (Vertex vs self-hosted)
- ✅ `/src/pages/learn/models.astro` - Model-agnostic delivery

---

## Existing Files - Required Updates

### 1. Homepage (`src/pages/index.astro`)

#### A. Add Hero Badge

**Location**: Before the Hero component
**Add this import at the top**:
```astro
---
// ... existing imports
import { useState } from 'react'; // if not already imported
---
```

**Add after SiteNav, before Hero**:
```astro
<SiteNav />

<!-- Hero Badge for Resellers -->
<div class="bg-zinc-950 border-b border-zinc-800/50 py-3">
  <div class="container mx-auto px-8">
    <div class="text-center">
      <a
        href="/resellers"
        class="inline-flex items-center gap-2 text-sm text-zinc-400 hover:text-zinc-100 transition-smooth"
      >
        <span class="px-2 py-1 bg-zinc-800/50 border border-zinc-700 rounded text-xs font-semibold">
          NEW
        </span>
        <span>you sell, we build · white-label ai products for agencies</span>
        <span aria-hidden="true">→</span>
      </a>
    </div>
  </div>
</div>

<Hero client:load />
```

#### B. Update "AI Agents" Card with MVP Modal

**Find this section** (~line 24):
```astro
<a href="/agents" class="card-slate h-full flex flex-col">
  <h3 class="text-lg font-semibold text-zinc-50 mb-3">AI Agents</h3>
  <p class="text-sm text-zinc-400 flex-1">
    3 containerized agents: LinkedIn outbound, meeting intelligence, support triage. Deploy in under 2 hours.
  </p>
  <span class="mt-6 text-sm text-zinc-200">See pricing & agents →</span>
</a>
```

**Replace with**:
```astro
<button
  onclick="window.showMvpModal = true"
  class="card-slate h-full flex flex-col text-left cursor-pointer hover:border-zinc-600 transition-all"
>
  <h3 class="text-lg font-semibold text-zinc-50 mb-3">AI Agents</h3>
  <p class="text-sm text-zinc-400 flex-1">
    example mvp: 3 containerized agents (one of many). LinkedIn outbound, meeting intelligence, support triage.
  </p>
  <span class="mt-6 text-sm text-zinc-200">see example mvp →</span>
</button>
```

#### C. Add MVP Modal at Bottom

**Add these imports at the top**:
```astro
---
// ... existing imports
import MvpShowcase from '../components/MvpShowcase';
---
```

**Add before `</Layout>` closing tag**:
```astro
<MvpShowcase client:only="react" isOpen={false} onClose={() => {}} />

<script>
  import { createRoot } from 'react-dom/client';
  import { createElement } from 'react';
  import MvpShowcase from '../components/MvpShowcase';

  let isModalOpen = false;
  let root: any = null;

  function renderModal() {
    const container = document.getElementById('mvp-modal-root');
    if (!container) return;

    if (!root) {
      root = createRoot(container);
    }

    root.render(
      createElement(MvpShowcase, {
        isOpen: isModalOpen,
        onClose: () => {
          isModalOpen = false;
          renderModal();
        }
      })
    );
  }

  // Listen for modal trigger
  window.addEventListener('DOMContentLoaded', () => {
    const modalRoot = document.createElement('div');
    modalRoot.id = 'mvp-modal-root';
    document.body.appendChild(modalRoot);

    renderModal();

    // Watch for modal open trigger
    Object.defineProperty(window, 'showMvpModal', {
      set: (value) => {
        isModalOpen = value;
        renderModal();
      },
      get: () => isModalOpen
    });
  });
</script>
```

---

### 2. AI Agents Page (`src/pages/agents.astro`)

#### A. Update Hero Subtitle

**Find** (~line 22):
```astro
<p class="text-body-lg text-zinc-400 mb-8 max-w-2xl">
  Intelligence agents for service businesses that already have paying clients but aren't managing customer data, meeting notes, or support workflows effectively. Deploy in under 2 hours. No vendor lock-in.
</p>
```

**Replace with**:
```astro
<p class="text-body-lg text-zinc-400 mb-8 max-w-2xl">
  Examples include PipelinePilot, DiagnosticPro, and Vertex-native builds. Model- and cloud-agnostic. No vendor lock-in.
</p>
```

#### B. Add Intro Note Above Agents Grid

**Add after hero section, before "Agents Grid" section**:
```astro
<!-- Intro Note -->
<section class="py-8 bg-zinc-950">
  <div class="container mx-auto px-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-zinc-900/50 border border-zinc-800 rounded-lg p-6">
        <p class="text-zinc-300 text-sm leading-relaxed">
          <strong class="text-zinc-100">Starting points:</strong> Below are example configurations. We mix agents per client needs. Delivery options: self-serve containers, managed cloud, or bespoke builds.
        </p>
      </div>
    </div>
  </div>
</section>
```

#### C. Add "See MVP Example" Link

**Add before the agents grid**:
```astro
<div class="max-w-4xl mx-auto mb-8 text-center">
  <button
    onclick="window.showMvpModal = true"
    class="inline-flex items-center gap-2 text-zinc-200 hover:text-zinc-50 transition-smooth text-sm"
  >
    <span>see a working mvp example</span>
    <span aria-hidden="true">→</span>
  </button>
</div>
```

#### D. Add Footer Line to Each Agent Card

**For each of the 3 agent cards (M1, M2, M3), add this before the closing `</a>` tag**:
```astro
<div class="mt-4 pt-4 border-t border-zinc-800">
  <p class="text-xs text-zinc-500">
    Models and providers are pluggable (Google, AWS, Azure, on-prem).
  </p>
</div>
```

#### E. Add Shared Pricing Component

**Add import at top**:
```astro
---
// ... existing imports
import PricingBlocks from '../components/PricingBlocks';
---
```

**Add before CTA section (after agents grid)**:
```astro
<PricingBlocks />
```

#### F. Add MVP Modal (Same as Homepage)

**Add at bottom before `</Layout>`**:
```astro
<MvpShowcase client:only="react" isOpen={false} onClose={() => {}} />

<!-- Same modal script as homepage -->
```

---

### 3. Private AI Page (`src/pages/private-ai.astro`)

#### A. Update Hero to Show Model-Agnostic

**Find** (~line 20):
```astro
<h1 class="text-h1 font-bold text-zinc-50 mb-6">
  Your AI. Your data. Your control.
</h1>
<p class="text-lg text-zinc-400 leading-relaxed">
  Launch a ChatGPT-style experience that runs entirely inside your infrastructure. No per-seat
  pricing, no mystery data trails—just fast, private AI your team actually trusts.
</p>
```

**Replace with**:
```astro
<h1 class="text-h1 font-bold text-zinc-50 mb-6">
  Your AI. Your data. Your control.
</h1>
<p class="text-lg text-zinc-400 leading-relaxed mb-4">
  Model-agnostic by design. Claude, OpenAI, Gemini, Llama, Mistral, Qwen, fine-tunes, or local. Pick what fits policy, latency, and cost.
</p>
<p class="text-lg text-zinc-400 leading-relaxed">
  Launch a ChatGPT-style experience that runs entirely inside your infrastructure. No per-seat pricing, no mystery data trails—just fast, private AI your team actually trusts.
</p>
```

#### B. Update "AI models" Card Content

**Find the "AI models" card** (~line 139):
```astro
<p class="text-sm text-zinc-400">
  Llama 3.1 70B for deep reasoning, Mistral 7B for quick responses, and Qwen 2.5 14B for
  specialized tasks—plus optional fine-tunes.
</p>
```

**Replace with**:
```astro
<ul class="space-y-2 text-sm text-zinc-400 mb-3">
  <li>• Any model family your governance allows</li>
  <li>• Switch or pin versions on your schedule</li>
  <li>• Optional fine-tunes and RAG pipelines</li>
</ul>
```

#### C. Add FAQ Question About Model Lock-in

**Find FAQ section** (~line 240):
**Add this question before the existing FAQs**:
```astro
<div>
  <h3 class="text-sm font-semibold text-zinc-200 uppercase tracking-widest mb-1">
    Are we limited to one provider?
  </h3>
  <p class="text-sm text-zinc-400">
    No. We are model- and cloud-agnostic. We integrate with your preferred vendors. Switch providers without rebuilding.
  </p>
</div>
```

#### D. Add Shared Pricing Component

**Add import at top**:
```astro
---
// ... existing imports
import PricingBlocks from '../components/PricingBlocks';
---
```

**Add after "What's Included" section**:
```astro
<PricingBlocks />
```

---

### 4. Automation Page (`src/pages/automation.astro`)

#### A. Add Comparison Card: n8n vs Vertex

**Add after the "Automation Menu" section**:
```astro
<!-- Comparison: n8n vs Vertex Agent Engine -->
<section class="py-24 bg-zinc-950 border-b border-zinc-800/60">
  <div class="container mx-auto px-8">
    <div class="max-w-5xl mx-auto">
      <h2 class="text-2xl font-bold text-zinc-50 mb-8">
        when to use n8n vs vertex agent engine
      </h2>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="text-zinc-400 uppercase text-xs tracking-widest border-b border-zinc-800">
            <tr>
              <th class="py-4 pr-4 font-semibold">capability</th>
              <th class="py-4 px-4 font-semibold text-center">n8n</th>
              <th class="py-4 pl-4 font-semibold text-center">vertex agent engine</th>
            </tr>
          </thead>
          <tbody class="text-zinc-300">
            <tr class="border-b border-zinc-800">
              <td class="py-4 pr-4">Human-readable flows</td>
              <td class="py-4 px-4 text-center">✓</td>
              <td class="py-4 pl-4 text-center">✓ (via tools)</td>
            </tr>
            <tr class="border-b border-zinc-800">
              <td class="py-4 pr-4">Long-running, stateful multi-agent reasoning</td>
              <td class="py-4 px-4 text-center text-zinc-500">△</td>
              <td class="py-4 pl-4 text-center">✓</td>
            </tr>
            <tr class="border-b border-zinc-800">
              <td class="py-4 pr-4">Observability and guardrails for LLM agents</td>
              <td class="py-4 px-4 text-center text-zinc-500">△</td>
              <td class="py-4 pl-4 text-center">✓</td>
            </tr>
            <tr class="border-b border-zinc-800">
              <td class="py-4 pr-4">CI/CD for agents, evals, rollback</td>
              <td class="py-4 px-4 text-center text-zinc-500">△</td>
              <td class="py-4 pl-4 text-center">✓</td>
            </tr>
            <tr class="border-b border-zinc-800">
              <td class="py-4 pr-4">Low-code integration quick wins</td>
              <td class="py-4 px-4 text-center">✓</td>
              <td class="py-4 pl-4 text-center text-zinc-500">△</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-8 bg-zinc-900/50 border border-zinc-800 rounded-lg p-6">
        <p class="text-sm text-zinc-400">
          <strong class="text-zinc-300">We pair them often:</strong> n8n for orchestration glue, Vertex Agent Engine for the agent brain. This gives you visual workflow building for integrations while maintaining security and guardrails for AI reasoning.
        </p>
      </div>
    </div>
  </div>
</section>
```

#### B. Add Link to Security Page

**Add at end of automation page, before closing CTA**:
```astro
<div class="mt-8 text-center">
  <a
    href="/learn/security"
    class="inline-flex items-center text-zinc-200 hover:text-zinc-50 transition-smooth text-sm"
  >
    <span>learn: why vertex for production agents</span>
    <span aria-hidden="true">→</span>
  </a>
</div>
```

---

## Navigation Updates

### Update `src/components/SiteNav.astro`

**Find the links array** (~line 2):
```astro
const links = [
  { href: '/', label: 'home' },
  { href: '/about', label: 'about' },
  { href: '/private-ai', label: 'private ai' },
  { href: '/agents', label: 'ai agents' },
  { href: '/automation', label: 'automation' },
  { href: '/cloud', label: 'cloud & data' },
];
```

**Replace with**:
```astro
const links = [
  { href: '/', label: 'home' },
  { href: '/about', label: 'about' },
  { href: '/private-ai', label: 'private ai' },
  { href: '/agents', label: 'ai agents' },
  { href: '/automation', label: 'automation' },
  { href: '/cloud', label: 'cloud & data' },
  { href: '/learn', label: 'learn' },
  { href: '/resellers', label: 'resellers' },
];
```

---

### Update Footer (`src/components/Footer.tsx`)

**Find the social links section** (~line 10):
```tsx
<div class="pt-6 flex justify-center gap-6 text-sm">
  <a
    href="mailto:jeremy@intentsolutions.io"
    className="text-zinc-400 hover:text-zinc-200 transition-smooth"
  >
    email
  </a>
  <a
    href="https://github.com/jeremylongshore"
    target="_blank"
    rel="noopener noreferrer"
    className="text-zinc-400 hover:text-zinc-200 transition-smooth"
  >
    github
  </a>
  <a
    href="https://startaitools.com"
    target="_blank"
    rel="noopener noreferrer"
    className="text-zinc-400 hover:text-zinc-200 transition-smooth"
  >
    blog
  </a>
</div>
```

**Add these links after "blog"**:
```tsx
<a
  href="/learn"
  className="text-zinc-400 hover:text-zinc-200 transition-smooth"
>
  learn
</a>
<a
  href="/resellers"
  className="text-zinc-400 hover:text-zinc-200 transition-smooth"
>
  resellers
</a>
```

---

## SEO & Meta Updates

### Update Layout Component (`src/layouts/Layout.astro`)

#### A. Update Default Description

**Find** (~line 13):
```astro
description = 'independent ai consultant shipping automation, rag agents, and astro + react products for operators who need production results.',
```

**Replace with**:
```astro
description = 'independent ai consultant. model- and cloud-agnostic delivery. automation, rag agents, and private ai. no vendor lock-in.',
```

#### B. Update Meta Tags for AI Agents Page

**In `src/pages/agents.astro`**, update the Layout title:

**Find**:
```astro
<Layout title="AI Agents - Containerized Automation | Intent Solutions">
```

**Replace with**:
```astro
<Layout
  title="AI Agents - Model-Agnostic Examples | Intent Solutions"
  description="Example agent configurations including PipelinePilot. Model- and cloud-agnostic. No vendor lock-in. Vertex-native or self-hosted."
>
```

#### C. Update Meta Tags for Private AI Page

**In `src/pages/private-ai.astro`**, update the Layout:

**Find**:
```astro
<Layout
  title="Private AI Infrastructure"
  description="Keep AI in your own cloud with fixed pricing, compliance-ready guardrails, and a 48-hour rollout."
>
```

**Replace with**:
```astro
<Layout
  title="Private AI Infrastructure - Model-Agnostic | Intent Solutions"
  description="Model-agnostic private AI. Claude, OpenAI, Gemini, Llama, Mistral, Qwen, fine-tunes, or local. Fixed pricing, compliance-ready guardrails, no vendor lock-in."
>
```

---

## Testing Checklist

### Functionality Tests

- [ ] **Homepage**
  - [ ] Hero badge links to `/resellers`
  - [ ] "AI Agents" card opens MVP modal
  - [ ] MVP modal displays correctly
  - [ ] MVP modal links work (agents, pricing, contact)
  - [ ] MVP modal closes with ESC key
  - [ ] MVP modal closes with backdrop click
  - [ ] MVP modal closes with X button

- [ ] **Navigation**
  - [ ] "Learn" link appears in nav
  - [ ] "Resellers" link appears in nav
  - [ ] All nav links work on desktop
  - [ ] Mobile nav shows CTA button

- [ ] **Learn Hub** (`/learn`)
  - [ ] Landing page loads
  - [ ] All 3 cards link correctly (pricing, security, models)
  - [ ] Back to home links work

- [ ] **Learn: Pricing** (`/learn/pricing`)
  - [ ] Page loads
  - [ ] All sections display
  - [ ] Links to other learn pages work
  - [ ] Contact link works

- [ ] **Learn: Security** (`/learn/security`)
  - [ ] Page loads
  - [ ] Comparison table renders
  - [ ] Links to automation page work

- [ ] **Learn: Models** (`/learn/models`)
  - [ ] Page loads
  - [ ] All model cards display
  - [ ] Links work

- [ ] **Resellers Page** (`/resellers`)
  - [ ] Page loads
  - [ ] Form submits successfully
  - [ ] Netlify form captures data
  - [ ] All sections display correctly

- [ ] **AI Agents Page** (`/agents`)
  - [ ] Intro note displays
  - [ ] "See MVP example" link opens modal
  - [ ] Agent cards show model-agnostic footer
  - [ ] PricingBlocks component renders
  - [ ] MVP modal works

- [ ] **Private AI Page** (`/private-ai`)
  - [ ] Model-agnostic messaging displays
  - [ ] AI models card updated
  - [ ] FAQ includes provider question
  - [ ] PricingBlocks component renders

- [ ] **Automation Page** (`/automation`)
  - [ ] n8n vs Vertex comparison table displays
  - [ ] Link to security page works
  - [ ] All content readable

- [ ] **Footer**
  - [ ] "Learn" link works
  - [ ] "Resellers" link works
  - [ ] All other links still work

### Content Review

- [ ] No mentions of "3 agents" as a cap (should be "example mvp")
- [ ] All pages mention "model- and cloud-agnostic"
- [ ] All pages mention "no vendor lock-in"
- [ ] Pricing consistently shows "flat fee + usage at provider list prices"
- [ ] Security messaging positions Vertex as recommended, not required
- [ ] All new pages have proper SEO titles and descriptions

### Cross-Browser Testing

- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari
- [ ] Mobile Chrome
- [ ] Mobile Safari

### Responsive Testing

- [ ] Mobile (< 768px)
- [ ] Tablet (768px - 1024px)
- [ ] Desktop (> 1024px)
- [ ] Large desktop (> 1440px)

### Performance Testing

- [ ] Build completes without errors
- [ ] No console errors on any page
- [ ] Lighthouse score remains 95+
- [ ] Page load time < 2s
- [ ] Modal animation smooth (60fps)

---

## Deployment Steps

### 1. Pre-Deployment

```bash
# Navigate to project
cd /home/jeremy/000-projects/intent-solutions-landing/astro-site

# Install dependencies (if new packages needed)
bun install

# Run development server for testing
bun run dev
# Visit http://localhost:4321 and test all changes
```

### 2. Build & Test

```bash
# Build production
bun run build

# Preview production build locally
bun run preview
# Visit http://localhost:4321 and test again
```

### 3. Run Tests

```bash
# Run Playwright tests
npm run test

# Run mobile tests
npm run test:mobile
```

### 4. Commit Changes

```bash
git status
git add .
git commit -m "feat(site): add learn hub, pricing education, security comparison, and resellers program

- Add MvpShowcase modal component for example agent configurations
- Add PricingBlocks shared component for transparent pricing
- Create learn hub with pricing, security, and models pages
- Add resellers program page with white-label offerings
- Update all pages to show model-agnostic positioning
- Remove ' 3 agents' cap language, replace with 'example mvp'
- Add Vertex vs self-hosted security comparison
- Update navigation to include learn and resellers
- Update footer with learn and resellers links
- Update SEO meta tags to remove restrictive language

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 5. Deploy to Netlify

```bash
# Push to git (auto-deploys on Netlify)
git push origin main

# Or manual Netlify deploy
netlify deploy --prod
```

### 6. Post-Deployment Verification

**After deployment, verify**:
- [ ] Production site loads: https://intentsolutions.io
- [ ] All new pages accessible
- [ ] Forms working (test seller kit form)
- [ ] No 404 errors
- [ ] SSL certificate valid
- [ ] Redirects working (if any)
- [ ] Search engines can crawl (check robots.txt)
- [ ] OpenGraph images display correctly

---

## Optional: Netlify Function for Seller Kit Autoresponder

### Create Netlify Function

**File**: `astro-site/netlify/functions/seller-kit-autoresponder.js`

```javascript
const nodemailer = require('nodemailer');

exports.handler = async (event, context) => {
  // Only handle POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  }

  // Parse form data
  const params = new URLSearchParams(event.body);
  const formName = params.get('form-name');

  // Only handle seller-kit form
  if (formName !== 'seller-kit') {
    return {
      statusCode: 200,
      body: 'OK',
    };
  }

  const email = params.get('email');
  const agencyName = params.get('agency-name');
  const contactName = params.get('contact-name');

  // Configure email transporter
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: process.env.SMTP_PORT,
    secure: true,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  // Email content
  const mailOptions = {
    from: process.env.SMTP_FROM,
    to: email,
    subject: 'Your Intent Solutions Seller Kit',
    html: `
      <h2>Welcome to the Intent Solutions Reseller Program, ${contactName}!</h2>

      <p>Thank you for requesting our seller kit. We're excited to partner with ${agencyName}.</p>

      <h3>What's Included:</h3>
      <ul>
        <li>Pitch Deck (10 slides) - <a href="[LINK_TO_DECK]">Download</a></li>
        <li>Vertical One-Pagers (SDR, Support, Search) - <a href="[LINK_TO_ONE_PAGERS]">Download</a></li>
        <li>Demo Scripts - <a href="[LINK_TO_SCRIPTS]">Download</a></li>
        <li>Pricing Calculator - <a href="[LINK_TO_CALCULATOR]">Open</a></li>
        <li>Case Study Templates - <a href="[LINK_TO_TEMPLATES]">Download</a></li>
      </ul>

      <h3>Next Steps:</h3>
      <ol>
        <li>Review the materials</li>
        <li>Schedule a co-sell strategy call: <a href="[CALENDLY_LINK]">Book Time</a></li>
        <li>Join our partner Slack channel: <a href="[SLACK_INVITE]">Join</a></li>
      </ol>

      <p>Questions? Reply to this email or reach out directly at jeremy@intentsolutions.io</p>

      <p>Best,<br>
      Jeremy Longshore<br>
      Intent Solutions IO</p>
    `,
  };

  try {
    await transporter.sendMail(mailOptions);

    return {
      statusCode: 200,
      body: 'Email sent successfully',
    };
  } catch (error) {
    console.error('Email error:', error);

    return {
      statusCode: 500,
      body: 'Failed to send email',
    };
  }
};
```

### Environment Variables

**Add to Netlify dashboard** (Site settings → Environment variables):

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
SMTP_FROM=jeremy@intentsolutions.io
```

### Test the Function

```bash
# Test locally with Netlify Dev
netlify dev

# Submit test form
# Check logs for function execution
```

---

## Summary of Changes

### Files Created (8 total)
1. `src/components/MvpShowcase.tsx`
2. `src/components/PricingBlocks.tsx`
3. `src/pages/resellers.astro`
4. `src/pages/learn/index.astro`
5. `src/pages/learn/pricing.astro`
6. `src/pages/learn/security.astro`
7. `src/pages/learn/models.astro`
8. `netlify/functions/seller-kit-autoresponder.js` (optional)

### Files to Update (7 total)
1. `src/pages/index.astro` - Add hero badge, MVP modal, update card
2. `src/pages/agents.astro` - Update messaging, add modal, add pricing
3. `src/pages/private-ai.astro` - Model-agnostic positioning, add pricing
4. `src/pages/automation.astro` - Add n8n vs Vertex comparison
5. `src/components/SiteNav.astro` - Add learn and resellers links
6. `src/components/Footer.tsx` - Add learn and resellers links
7. `src/layouts/Layout.astro` - Update default description

### Key Messaging Changes
- ❌ "3 agents" (removed cap language)
- ✅ "example mvp" or "one of many configurations"
- ✅ "model- and cloud-agnostic"
- ✅ "no vendor lock-in"
- ✅ "flat fee + usage at provider list prices"
- ✅ "Vertex recommended for production (we support all options)"

---

## Completion Checklist

- [ ] All new files created and verified
- [ ] All existing files updated per instructions
- [ ] Navigation updated (SiteNav and Footer)
- [ ] SEO meta tags updated
- [ ] Build succeeds without errors
- [ ] Local preview looks correct
- [ ] Tests pass
- [ ] Committed to git
- [ ] Deployed to production
- [ ] Production site verified
- [ ] Forms tested
- [ ] Documentation updated

---

**Implementation Time Estimate**: 2-3 hours for careful, thorough implementation

**Risk Level**: Medium (significant changes, but well-documented)

**Rollback Plan**: Git revert if issues found in production

---

**Questions or Issues?**
- Check this document for detailed instructions
- Review existing working examples in codebase
- Test changes locally before deploying
- Use git branches for safety if needed

**Documentation Generated**: 2025-11-03
**For**: Intent Solutions IO Complete Refactor
**By**: Claude Code (Anthropic)
