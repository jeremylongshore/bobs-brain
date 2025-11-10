# Intent Solutions Landing: Complete System Analysis & Operations Guide

**For**: DevOps Engineer Onboarding
**Generated**: October 4, 2025
**System Version**: 1.0.0 (commit: 0fab822)
**Current Branch**: main
**Production URL**: https://intentsolutions.io

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Technology Stack Deep-Dive](#technology-stack-deep-dive)
4. [Directory Structure Analysis](#directory-structure-analysis)
5. [Deployment Pipeline & Operations](#deployment-pipeline--operations)
6. [Security & Access Management](#security--access-management)
7. [Monitoring & Observability](#monitoring--observability)
8. [Performance & Cost Analysis](#performance--cost-analysis)
9. [Development Workflow](#development-workflow)
10. [Dependencies & Supply Chain](#dependencies--supply-chain)
11. [Current State Assessment](#current-state-assessment)
12. [Quick Reference](#quick-reference)
13. [Recommendations Roadmap](#recommendations-roadmap)

---

## Executive Summary

**What This System Does**
Intent Solutions Landing is a production-grade, high-performance static landing page built with React 18 and TypeScript, deployed on Netlify's global CDN. It serves as the primary web presence for Intent Solutions, showcasing services, platforms, and providing contact capabilities. The site is optimized for Core Web Vitals with target Lighthouse scores of 95+.

**Current State**
✅ **PRODUCTION ACTIVE** at https://intentsolutions.io
- Live deployment via Netlify (auto-deploy from GitHub main branch)
- Custom domain configured with Porkbun DNS
- SSL/TLS via Let's Encrypt (managed by Netlify)
- Security headers implemented (CSP, HSTS, X-Frame-Options)
- Zero downtime deployments with atomic rollback capability

**Technology Foundation**
This is a modern JAMstack architecture built on:
- **Runtime**: Bun (fast JavaScript runtime, NOT npm/yarn)
- **Framework**: React 18 with TypeScript strict mode
- **Build Tool**: Vite with SWC for sub-second HMR
- **UI System**: shadcn/ui (57 pre-built components) + Tailwind CSS
- **Deployment**: Netlify with GitHub webhook triggers
- **Repository**: https://github.com/jeremylongshore/intent-solutions-landing

**Key Architectural Decisions**
1. **Static-First Architecture**: No backend/database = maximum performance, minimal attack surface, zero server costs
2. **Bun Over Node**: 3-4x faster installs and builds compared to npm
3. **shadcn/ui Component Library**: Copy-paste components instead of package dependencies = full control, no breaking changes
4. **Atomic Deployments**: Netlify's immutable deploys enable instant rollbacks
5. **Security-First Headers**: Implemented comprehensive security headers from day one

---

## System Architecture Overview

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Runtime** | Bun | 1.0.0+ | JavaScript runtime & package manager |
| **Frontend** | React | 18.x | UI library with hooks |
| **Language** | TypeScript | 5.x | Type-safe JavaScript (strict mode) |
| **Build Tool** | Vite | 5.x | Lightning-fast bundler with HMR |
| **UI Library** | shadcn/ui | latest | 57 accessible React components |
| **Styling** | Tailwind CSS | 3.x | Utility-first CSS framework |
| **Routing** | React Router DOM | 6.x | Client-side routing |
| **State Management** | TanStack Query | 5.x | Server state management |
| **CDN/Hosting** | Netlify | N/A | Global CDN with atomic deploys |
| **DNS** | Porkbun | N/A | Domain registrar & DNS provider |
| **SSL/TLS** | Let's Encrypt | N/A | Free SSL (managed by Netlify) |

### Cloud Services in Use

| Service | Purpose | Environment | Key Config |
|---------|---------|-------------|------------|
| **Netlify Hosting** | Static site CDN | Production | Auto-deploy from GitHub main |
| **Netlify Functions** | Serverless functions (future) | N/A | Not yet implemented |
| **GitHub Actions** | CI/CD (future) | N/A | Not yet implemented |
| **Porkbun DNS** | Domain management | Production | A record: 75.2.60.5 |
| **Let's Encrypt** | SSL/TLS certificates | Production | Auto-renewed by Netlify |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     USER BROWSER                        │
│              (Desktop, Mobile, Tablet)                  │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ HTTPS (443)
                         │
┌────────────────────────▼────────────────────────────────┐
│                  NETLIFY GLOBAL CDN                     │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Edge Nodes (150+ locations)              │  │
│  │  • Security Headers (CSP, HSTS, X-Frame-Options) │  │
│  │  • SSL/TLS Termination (Let's Encrypt)          │  │
│  │  • HTTP → HTTPS Redirect (301)                  │  │
│  │  • www → non-www Redirect (301)                 │  │
│  │  • Brotli/Gzip Compression                       │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Atomic Deployment Storage              │  │
│  │  • Immutable builds (instant rollback)           │  │
│  │  • Asset fingerprinting (cache busting)          │  │
│  │  • /dist/ artifacts                              │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         │ Webhook trigger on push to main
                         │
┌────────────────────────▼────────────────────────────────┐
│                   GITHUB REPOSITORY                     │
│         jeremylongshore/intent-solutions-landing        │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  main branch → Triggers Netlify Build            │  │
│  │  feature/* → No auto-deploy                      │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

BUILD PIPELINE (Netlify):
┌─────────────────────────────────────────────────────────┐
│  1. Git clone from GitHub                               │
│  2. bun install (dependencies)                          │
│  3. bun run build (Vite production build)               │
│  4. Deploy /dist to CDN                                 │
│  5. Atomic swap (zero downtime)                         │
│  Duration: ~90 seconds                                  │
└─────────────────────────────────────────────────────────┘

COMPONENT ARCHITECTURE (Browser):
┌─────────────────────────────────────────────────────────┐
│  App.tsx (Root)                                         │
│   ├── BrowserRouter                                     │
│   ├── TanStack QueryClient                             │
│   └── Routes                                            │
│        ├── / → Index.tsx (Landing Page)                │
│        │     ├── Navigation (sticky header)            │
│        │     ├── Hero (above fold)                     │
│        │     ├── About                                 │
│        │     ├── Platforms                             │
│        │     ├── ExpertCTA                             │
│        │     ├── Market                                │
│        │     ├── Founder                               │
│        │     ├── Contact                               │
│        │     └── Footer                                │
│        └── /* → NotFound.tsx (404 page)                │
└─────────────────────────────────────────────────────────┘
```

### Data Flow

**Static Site (Current)**
```
1. User requests https://intentsolutions.io
2. DNS resolves to Netlify edge node (75.2.60.5)
3. Netlify serves cached static HTML/CSS/JS from nearest edge
4. Browser downloads React bundle (~180KB gzipped)
5. React hydrates and renders interactive components
6. Page fully interactive in <3.5s (TTI target)
```

**No Backend Dependencies**
- ✅ No database = no data breach risk
- ✅ No API = no rate limiting or auth needed
- ✅ No server = no patching or maintenance
- ⚠️ Contact form submission requires future implementation (Netlify Forms or external service)

---

## Technology Stack Deep-Dive

### Build Configuration (`vite.config.ts`)

```typescript
{
  server: {
    host: "::",           // IPv6 (all interfaces)
    port: 8080,          // Dev server port
  },
  plugins: [
    react(),             // React Fast Refresh (SWC)
    componentTagger(),   // Lovable dev mode tagging
  ],
  resolve: {
    alias: {
      "@": "./src"       // Path alias for imports
    }
  }
}
```

**Key Features**:
- **SWC Plugin**: 20x faster than Babel for React transforms
- **Path Aliases**: `@/components/...` instead of `../../../components/...`
- **HMR**: Sub-second hot module replacement
- **IPv6 Support**: Binds to all network interfaces

### Tailwind Configuration (`tailwind.config.ts`)

**Custom Theme Extensions**:
- **Colors**: HSL-based design system with CSS variables
- **Fonts**: Inter as primary sans-serif
- **Container**: Max-width 1400px, centered with padding
- **Gradients**: `bg-gradient-hero`, `bg-gradient-section`, `bg-gradient-card`
- **Shadows**: `shadow-card`, `shadow-hover`, `shadow-glow`
- **Breakpoints**: sm (640px), md (768px), lg (1024px), xl (1280px), 2xl (1400px)

**Dark Mode**: Class-based strategy (`class` in config)

### Netlify Configuration (`netlify.toml`)

**Build Settings**:
```toml
[build]
  command = "bun install && bun run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"
  BUN_VERSION = "1.0.0"
```

**Redirects**:
1. HTTP → HTTPS (301 permanent)
2. www → non-www (301 permanent)
3. SPA fallback: `/*` → `/index.html` (200 OK)

**Security Headers**:
- `X-Frame-Options: DENY` (clickjacking protection)
- `X-Content-Type-Options: nosniff` (MIME sniffing prevention)
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`
- `Content-Security-Policy`: Default-src 'self' with specific allowances
- `Strict-Transport-Security`: 1-year HSTS with preload

---

## Directory Structure Analysis

### Project Size & Metrics
- **Total Size**: 2.2 MB (including node_modules)
- **TypeScript Files**: 68 files (.ts/.tsx)
- **Components**: 57 shadcn/ui + 9 custom landing sections
- **Documentation**: 12 markdown files (numbered 00-10 + CLAUDE.md)
- **Git History**: 10+ commits, active development

### Root-Level Files

```
intent-solutions-landing/
├── 📋 Documentation (Numbered for Organization)
│   ├── 00-CLAUDE.md                   # Legacy AI context
│   ├── 01-README.md                   # Project overview
│   ├── 02-NETLIFY-DEPLOYMENT-GUIDE.md # Deployment manual
│   ├── 03-LICENSE.md                  # MIT License
│   ├── 04-Makefile                    # Build automation (future)
│   ├── 05-CONTRIBUTING.md             # Contribution guidelines
│   ├── 06-CHANGELOG.md                # Version history
│   ├── 07-ARCHITECTURE.md             # Architecture documentation
│   ├── 08-COMPONENT-API.md            # Component reference
│   ├── 09-TROUBLESHOOTING.md          # Debug guide
│   ├── 10-SECURITY.md                 # Security practices
│   └── CLAUDE.md                      # 🔑 Current AI context (primary)
│
├── ⚙️  Configuration Files
│   ├── bun.lockb                      # Bun lock file (binary)
│   ├── netlify.toml                   # Netlify deployment config
│   ├── tailwind.config.ts             # Tailwind theme
│   ├── vite.config.ts                 # Vite build config
│   └── .gitignore                     # Git exclusions
│
├── 📁 Project Directories
│   ├── .claude-docs/                  # AI-generated docs (13 files)
│   ├── .git/                          # Git repository
│   ├── .github/                       # GitHub templates
│   │   └── ISSUE_TEMPLATE/            # Issue templates
│   ├── .vscode/                       # VS Code settings
│   │   ├── extensions.json            # Recommended extensions
│   │   └── settings.json              # Editor config
│   ├── docs/                          # Additional docs (if any)
│   ├── public/                        # Static assets
│   ├── src/                           # Source code
│   └── tests/                         # Test files (future)
```

### `/src` Directory (Source Code)

```
src/
├── 📱 Entry Points
│   ├── main.tsx                       # Application entry point
│   ├── App.tsx                        # Root component
│   ├── App.css                        # App-level styles
│   ├── index.css                      # Global styles + CSS variables
│   └── vite-env.d.ts                  # Vite type definitions
│
├── 🧩 Components (Landing Page Sections - Order Matters!)
│   ├── Navigation.tsx                 # Sticky header navigation
│   ├── Hero.tsx                       # Above-fold hero section
│   ├── About.tsx                      # Company overview
│   ├── Platforms.tsx                  # Service platforms showcase
│   ├── ExpertCTA.tsx                  # Call-to-action section
│   ├── Market.tsx                     # Market positioning
│   ├── Founder.tsx                    # Founder information
│   ├── Contact.tsx                    # Contact form
│   └── Footer.tsx                     # Site footer
│
├── 🎨 UI Components (shadcn/ui - 57 Total)
│   └── ui/
│       ├── accordion.tsx              ├── input.tsx
│       ├── alert.tsx                  ├── input-otp.tsx
│       ├── alert-dialog.tsx           ├── label.tsx
│       ├── aspect-ratio.tsx           ├── menubar.tsx
│       ├── avatar.tsx                 ├── navigation-menu.tsx
│       ├── badge.tsx                  ├── pagination.tsx
│       ├── breadcrumb.tsx             ├── popover.tsx
│       ├── button.tsx                 ├── progress.tsx
│       ├── calendar.tsx               ├── radio-group.tsx
│       ├── card.tsx                   ├── resizable.tsx
│       ├── carousel.tsx               ├── scroll-area.tsx
│       ├── chart.tsx                  ├── select.tsx
│       ├── checkbox.tsx               ├── separator.tsx
│       ├── collapsible.tsx            ├── sheet.tsx
│       ├── command.tsx                ├── sidebar.tsx
│       ├── context-menu.tsx           ├── skeleton.tsx
│       ├── dialog.tsx                 ├── slider.tsx
│       ├── drawer.tsx                 ├── sonner.tsx
│       ├── dropdown-menu.tsx          ├── switch.tsx
│       ├── form.tsx                   ├── table.tsx
│       ├── hover-card.tsx             ├── tabs.tsx
│       ├── textarea.tsx               └── use-toast.ts
│       ├── toast.tsx
│       ├── toaster.tsx
│       ├── toggle.tsx
│       ├── toggle-group.tsx
│       └── tooltip.tsx
│
├── 📄 Pages (Routes)
│   ├── Index.tsx                      # Landing page (/)
│   └── NotFound.tsx                   # 404 error page (/*)
│
├── 🪝 Custom Hooks
│   ├── use-mobile.tsx                 # Mobile viewport detection
│   └── use-toast.ts                   # Toast notification manager
│
├── 🛠️  Utilities
│   └── lib/
│       └── utils.ts                   # cn() class merger, helpers
│
└── 🖼️  Assets
    └── assets/
        ├── hero-bg.jpg                # Hero background image
        ├── diagnostic-pro.jpg         # Platform screenshot
        └── hustle-platform.jpg        # Platform screenshot
```

### `/public` Directory (Static Assets)

```
public/
├── favicon.ico                        # Browser favicon
├── placeholder.svg                    # Placeholder graphic
└── robots.txt                         # SEO crawler instructions
```

**Asset Handling**:
- Files in `/public` served at root (`/favicon.ico`)
- Vite processes `/src/assets` during build (fingerprinting)
- Images optimized during build (compression, format conversion)

### `.claude-docs/` Directory (AI-Generated Reports)

**Current Reports** (13 documents):
```
.claude-docs/
├── 0001-AUDIT-100425-initial-directory-assessment.md
├── 0002-AUDIT-100425-naming-convention-violations.md
├── 0003-AUDIT-100425-hierarchical-structure-analysis.md
├── 0004-AUDIT-100425-content-organization-intelligence.md
├── 0005-AUDIT-100425-documentation-excellence-assessment.md
├── 0006-AUDIT-100425-performance-efficiency-metrics.md
├── 0007-AUDIT-100425-compliance-security-posture.md
├── 0008-CHORE-100425-transformation-execution-plan.md
├── 0009-CHORE-100425-naming-standardization-complete.md
├── 0010-CHORE-100425-structure-migration-complete.md
├── 0011-CHORE-100425-documentation-suite-created.md
├── 0012-RELEASE-100425-excellence-certification.md
└── 0013-RELEASE-100425-final-transformation-report.md
```

**Naming Convention**: `NNNN-TYPE-MMDDYY-description.md`
- `NNNN`: Sequential number (0001-9999)
- `TYPE`: AUDIT | CHORE | RELEASE | DEVOPS
- `MMDDYY`: Date (100425 = October 4, 2025)

**Purpose**: All Claude-generated analysis, audits, and reports stored here per project standards.

---

## Deployment Pipeline & Operations

### Netlify Auto-Deploy Workflow

**Trigger**: Push to GitHub `main` branch

**Pipeline Stages**:
```
1. GitHub Webhook → Netlify (instant)
2. Git Clone (5-10 seconds)
3. Dependency Install: bun install (~15 seconds)
4. Production Build: bun run build (~30 seconds)
5. Asset Upload to CDN (~20 seconds)
6. Atomic Deployment Swap (~5 seconds)
7. Cache Invalidation (instant)

Total Duration: ~90 seconds
```

**Build Environment**:
- **OS**: Ubuntu 22.04 LTS
- **Node**: v20 (for compatibility)
- **Bun**: 1.0.0
- **Build Command**: `bun install && bun run build`
- **Output Directory**: `dist/`

**Deployment Characteristics**:
- **Atomic**: All-or-nothing deploys (no partial updates)
- **Immutable**: Each deploy gets unique URL for rollback
- **Instant Rollback**: Click "Rollback" in Netlify dashboard
- **Zero Downtime**: Traffic switches instantly to new version
- **Asset Fingerprinting**: Files hashed for cache busting

### Local Development Workflow

**Prerequisites**:
```bash
# Required tools
- Bun 1.0.0+ (NOT npm/yarn/pnpm)
- Git
- Code editor (VS Code recommended)

# Install Bun (if not installed)
curl -fsSL https://bun.sh/install | bash
```

**Setup & Run**:
```bash
# 1. Clone repository
git clone https://github.com/jeremylongshore/intent-solutions-landing.git
cd intent-solutions-landing

# 2. Install dependencies
bun install

# 3. Start development server
bun run dev
# → Opens at http://localhost:8080

# 4. Make changes (HMR auto-refreshes)

# 5. Build for production (test locally)
bun run build
bun run preview
# → Preview at http://localhost:4173
```

**Development Server Features**:
- **Hot Module Replacement**: Instant updates without page reload
- **TypeScript Checking**: Real-time type errors in terminal
- **Fast Refresh**: Preserves component state during edits
- **IPv6 Support**: Accessible on all network interfaces

### Staging Deployment

⚠️ **CURRENT STATUS**: No dedicated staging environment

**Recommended Approach** (To Implement):
1. **Branch Deploys**: Enable Netlify branch deploys for `staging` branch
2. **Preview URLs**: Use Netlify preview deploys for PRs
3. **Environment Variables**: Separate staging vs production env vars

**Temporary Workaround**:
```bash
# Test production build locally before pushing to main
bun run build
bun run preview
# Verify all functionality works

# Then deploy to production
git push origin main
```

### Production Deployment

**Pre-Deployment Checklist**:
```markdown
- [ ] All changes tested locally (bun run dev)
- [ ] Production build successful (bun run build)
- [ ] Preview build verified (bun run preview)
- [ ] TypeScript types valid (no errors in IDE)
- [ ] No console errors or warnings
- [ ] Responsive design tested (mobile, tablet, desktop)
- [ ] Security headers unchanged in netlify.toml
- [ ] No secrets committed (.env files excluded)
```

**Deployment Command**:
```bash
# Merge to main branch (triggers auto-deploy)
git checkout main
git merge feature/your-feature
git push origin main

# Monitor build in Netlify dashboard
# → https://app.netlify.com/sites/[your-site]/deploys
```

**Post-Deployment Verification**:
1. Visit https://intentsolutions.io (verify site loads)
2. Check browser console (no errors)
3. Test navigation (all links work)
4. Verify mobile responsiveness
5. Check Lighthouse score (target: 95+)

**Rollback Procedure**:
```
If deployment fails or has issues:

1. Open Netlify dashboard
2. Go to Deploys tab
3. Find previous successful deploy
4. Click "Publish deploy"
5. Rollback completes in ~30 seconds
```

### Environment Variables

**Current State**: No environment variables in use

**Future Implementation** (When Needed):
```bash
# In Netlify dashboard:
# Site settings → Environment variables

# Example variables:
VITE_API_URL=https://api.intentsolutions.io
VITE_ANALYTICS_ID=UA-XXXXXXXXX-X
VITE_CONTACT_FORM_ENDPOINT=https://...
```

**Access in Code**:
```typescript
const apiUrl = import.meta.env.VITE_API_URL
```

**Security**:
- ✅ Never commit `.env` files (in `.gitignore`)
- ✅ Use Netlify UI for secret management
- ✅ Prefix public vars with `VITE_` (exposed to client)
- ⚠️ Never store API secrets in client-side code

---

## Security & Access Management

### Authentication & Access

**Netlify Account**:
- **Email**: jeremylongshore@gmail.com
- **Dashboard**: https://app.netlify.com
- **Auth Token**: Stored in `~/security/netlify-auth-token.txt` (chmod 600)

**GitHub Repository**:
- **URL**: https://github.com/jeremylongshore/intent-solutions-landing
- **Access**: Private repository
- **Collaborators**: Owner only (currently)

**Domain Management**:
- **Registrar**: Porkbun (https://porkbun.com)
- **Domain**: intentsolutions.io
- **DNS Records**:
  - A record: `@` → `75.2.60.5` (Netlify)
  - CNAME: `www` → `[site-name].netlify.app`

### Security Posture

**Client-Side Security** (netlify.toml):
```toml
[headers.values]
  X-Frame-Options = "DENY"                          # No iframe embedding
  X-Content-Type-Options = "nosniff"                # No MIME sniffing
  Referrer-Policy = "strict-origin-when-cross-origin"
  Permissions-Policy = "geolocation=(), microphone=(), camera=()"
  Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline'; ..."
  Strict-Transport-Security = "max-age=31536000; includeSubDomains; preload"
```

**HTTPS Enforcement**:
- Let's Encrypt SSL certificate (auto-renewed)
- HTTP → HTTPS redirect (301 permanent)
- HSTS preload ready (1-year max-age)

**Vulnerability Management**:
- **Dependency Scanning**: Manual `bun audit` (no automated scanning yet)
- **Secret Detection**: `.gitignore` excludes `.env`, `*.pem`, `*.key`, `*.cert`
- **Code Review**: Manual review before merge to main

**Known Security Gaps**:
1. ⚠️ No automated dependency scanning (Dependabot not enabled)
2. ⚠️ No pre-commit hooks for secret detection
3. ⚠️ CSP allows `unsafe-inline` (required for Vite, could be stricter)
4. ⚠️ No security.txt file (future: `/.well-known/security.txt`)

**Incident Response**:
- **Contact**: security@intentsolutions.io
- **Response Time**: 48 hours for initial response
- **Severity Levels**: Critical (1-3 days), High (1 week), Medium (2 weeks), Low (next release)

### Secrets Management

**Current Secrets** (None in use yet):
- Netlify auth token: `~/security/netlify-auth-token.txt` (local only)

**Future Secrets** (When Needed):
- API keys → Netlify environment variables
- Service credentials → Netlify environment variables
- Signing keys → External secret manager (AWS Secrets Manager, etc.)

**Best Practices**:
1. Never commit secrets to Git
2. Use Netlify UI for environment variables
3. Rotate credentials quarterly
4. Use different keys for staging/production

---

## Monitoring & Observability

### Current Monitoring

⚠️ **STATUS**: Minimal monitoring in place

**Available Metrics** (Netlify Dashboard):
- Deploy status (success/failure)
- Build time duration
- Bandwidth usage
- Site visitors (basic analytics)

**Missing Observability**:
- ❌ No error tracking (Sentry, Rollbar, etc.)
- ❌ No performance monitoring (Core Web Vitals over time)
- ❌ No uptime monitoring (external service)
- ❌ No log aggregation (CloudWatch, Datadog, etc.)
- ❌ No alerting system

### Recommended Monitoring Stack

**Phase 1: Essential Monitoring** (Implement First)
```yaml
Error Tracking:
  Tool: Sentry (free tier)
  Coverage: Runtime errors, unhandled rejections
  Alerts: Email on new errors

Performance:
  Tool: Lighthouse CI (GitHub Actions)
  Coverage: Core Web Vitals regression detection
  Alerts: Fail build if score < 90

Uptime:
  Tool: UptimeRobot (free tier)
  Coverage: HTTP 200 checks every 5 minutes
  Alerts: Email/SMS on downtime
```

**Phase 2: Advanced Observability** (After Phase 1)
```yaml
Real User Monitoring (RUM):
  Tool: Google Analytics 4 or Plausible
  Coverage: User behavior, page views, conversions

Log Aggregation:
  Tool: Netlify logs + external viewer (Papertrail)
  Coverage: Build logs, function logs (when added)
```

### Key Metrics to Track

**Performance Targets**:
| Metric | Target | Current | Tool |
|--------|--------|---------|------|
| Lighthouse Score | 95+ | Unknown | Manual audits |
| First Contentful Paint (FCP) | < 1.5s | Unknown | Lighthouse |
| Largest Contentful Paint (LCP) | < 2.5s | Unknown | Lighthouse |
| Time to Interactive (TTI) | < 3.5s | Unknown | Lighthouse |
| Cumulative Layout Shift (CLS) | < 0.1 | Unknown | Lighthouse |
| Total Blocking Time (TBT) | < 200ms | Unknown | Lighthouse |

**Operational Metrics**:
- Deploy success rate (target: 100%)
- Build duration (target: < 120 seconds)
- Rollback frequency (target: < 1% of deploys)
- MTTR (Mean Time to Recovery): < 10 minutes

### Alerting Strategy

**Severity Levels**:

| Severity | Trigger | Response Time | Notification |
|----------|---------|---------------|--------------|
| **P0 - Critical** | Site down (5xx errors) | Immediate | SMS + Email + Slack |
| **P1 - High** | Build failures | 15 minutes | Email + Slack |
| **P2 - Medium** | Performance degradation | 4 hours | Email |
| **P3 - Low** | Dependency vulnerabilities | Next business day | Email |

**Current Alerts** (None configured):
- ⚠️ No alerting system in place

**Recommended First Alerts**:
1. Netlify deploy failure → Email
2. Site downtime (UptimeRobot) → SMS + Email
3. New Sentry errors → Email (daily digest)

---

## Performance & Cost Analysis

### Current Performance Baseline

**Bundle Size** (Estimated):
- Initial JS bundle: ~180 KB gzipped
- CSS bundle: ~15 KB gzipped
- Images: 3 assets (~500 KB total)
- Total first load: ~700 KB

**Optimization Opportunities**:
1. ✅ Already optimized: Vite tree-shaking, minification
2. ✅ Already optimized: Brotli/Gzip compression (Netlify)
3. ⚠️ To implement: Image lazy loading
4. ⚠️ To implement: Route-based code splitting
5. ⚠️ To implement: WebP/AVIF image formats

### Cost Analysis

**Monthly Cloud Spend**: $0 (Free Tier)

| Service | Cost | Usage | Limit |
|---------|------|-------|-------|
| **Netlify Hosting** | $0 | Static site | 100 GB bandwidth/month |
| **Netlify Functions** | $0 | Not used | N/A |
| **GitHub** | $0 | Private repo | Unlimited |
| **Porkbun DNS** | ~$10/year | Domain renewal | N/A |
| **Let's Encrypt SSL** | $0 | SSL cert | Unlimited renewals |

**Total Monthly Cost**: ~$0.83 (domain only)

**Scaling Considerations**:
- Netlify free tier sufficient for 100K+ visitors/month
- Upgrade to Pro ($19/mo) if bandwidth exceeds 100 GB
- Functions tier ($25/mo) if adding serverless backend

### Performance Optimization Roadmap

**Week 1: Quick Wins**
- [ ] Implement image lazy loading (`loading="lazy"`)
- [ ] Convert images to WebP format
- [ ] Add `<link rel="preload">` for critical assets

**Month 1: Advanced Optimizations**
- [ ] Implement route-based code splitting (React.lazy)
- [ ] Add service worker for offline support
- [ ] Optimize font loading (FOIT/FOUT prevention)

**Quarter 1: Performance Monitoring**
- [ ] Set up Lighthouse CI in GitHub Actions
- [ ] Implement RUM (Real User Monitoring)
- [ ] Establish performance budgets

---

## Development Workflow

### Code Quality Standards

**TypeScript Configuration**:
- Strict mode enabled (`strict: true`)
- No implicit any (`noImplicitAny: true`)
- Unused locals/params flagged

**Linting & Formatting** (To Implement):
```bash
# Recommended setup
bun add -d eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
bun add -d prettier eslint-config-prettier
bun add -d husky lint-staged

# Pre-commit hook (husky)
npm run lint && npm run type-check
```

**Current State**:
- ⚠️ No ESLint configured
- ⚠️ No Prettier configured
- ⚠️ No pre-commit hooks
- ⚠️ No automated formatting

### Git Workflow

**Branch Strategy**:
```
main              # Production (auto-deploys to Netlify)
 ├── feature/*    # Feature branches
 ├── bugfix/*     # Bug fixes
 └── hotfix/*     # Emergency fixes
```

**Commit Convention** (Recommended):
```bash
# Format: type(scope): description

feat(hero): add video background
fix(contact): resolve form validation bug
docs(readme): update deployment instructions
chore(deps): update React to 18.3
```

**Pull Request Flow**:
1. Create feature branch from `main`
2. Make changes and commit
3. Push to GitHub
4. Create PR (no automated checks yet)
5. Manual review
6. Merge to `main` (triggers deploy)

### Testing Strategy

**Current State**: ❌ No tests implemented

**Recommended Test Pyramid**:
```
     E2E Tests (5%)          ← Playwright
    ↗            ↖
Integration Tests (15%)      ← React Testing Library
    ↗            ↖
  Unit Tests (80%)            ← Vitest
```

**Implementation Plan**:
```bash
# Phase 1: Setup test infrastructure
bun add -d vitest @testing-library/react @testing-library/jest-dom
bun add -d @playwright/test

# Phase 2: Write unit tests for utilities
# Test files: src/**/*.test.tsx

# Phase 3: Component integration tests
# Test files: src/components/**/*.test.tsx

# Phase 4: E2E smoke tests
# Test files: tests/e2e/**/*.spec.ts
```

**Test Coverage Targets**:
- Utilities: 100% coverage
- Components: 80% coverage
- Pages: 60% coverage (E2E preferred)

### CI/CD Pipeline (Future)

**Recommended GitHub Actions Workflow**:
```yaml
name: CI/CD

on:
  pull_request:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run type-check
      - run: bun run lint
      - run: bun run test
      - run: bun run build

  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: treosh/lighthouse-ci-action@v10
        with:
          urls: https://intentsolutions.io
          uploadArtifacts: true
```

---

## Dependencies & Supply Chain

### Direct Dependencies

**Production Dependencies** (from package.json - needs verification):
```json
{
  "@tanstack/react-query": "^5.x",
  "react": "^18.x",
  "react-dom": "^18.x",
  "react-router-dom": "^6.x",
  "@radix-ui/*": "latest",        // shadcn/ui peer deps
  "tailwindcss": "^3.x",
  "clsx": "^2.x",
  "tailwind-merge": "^2.x"
}
```

**Development Dependencies**:
```json
{
  "@vitejs/plugin-react-swc": "^3.x",
  "typescript": "^5.x",
  "vite": "^5.x",
  "tailwindcss-animate": "^1.x",
  "lovable-tagger": "latest"
}
```

### Security Scanning

**Current Process**:
```bash
# Manual security audit
bun audit

# Manually check for outdated packages
bun outdated
```

**Recommended Automation**:
1. Enable GitHub Dependabot alerts
2. Configure Dependabot auto-updates for security patches
3. Set up Snyk or Mend (formerly WhiteSource) scanning

### Dependency Update Strategy

**Patch Updates** (automatic):
- Security patches: Apply within 48 hours
- Bug fixes: Review and apply weekly

**Minor Updates** (manual review):
- New features: Test in staging, deploy monthly
- Breaking changes (rare): Evaluate impact, plan migration

**Major Updates** (planned migration):
- Framework updates (React 19, etc.): Quarterly review
- Build tool updates (Vite 6, etc.): Evaluate breaking changes

### Third-Party Services

| Service | Purpose | Auth Method | Criticality | SLA |
|---------|---------|-------------|-------------|-----|
| **Netlify** | Hosting & CDN | OAuth (GitHub) | Critical | 99.99% |
| **GitHub** | Source control | SSH key | Critical | 99.95% |
| **Porkbun** | DNS | Password | High | 99.9% |
| **Let's Encrypt** | SSL certs | ACME (auto) | High | N/A |

**External API Dependencies**: None (static site)

---

## Current State Assessment

### What's Working Well

**✅ Infrastructure Excellence**:
- Atomic deployments with instant rollback capability
- Global CDN with 150+ edge locations (Netlify)
- Zero-downtime deploys (proven in production)
- Comprehensive security headers (CSP, HSTS, X-Frame-Options)

**✅ Developer Experience**:
- Bun runtime: 3-4x faster than npm/yarn
- Vite HMR: Sub-second hot reload
- TypeScript strict mode: Excellent type safety
- Component library: 57 pre-built shadcn/ui components

**✅ Documentation Quality**:
- 12 numbered documentation files (excellent organization)
- Comprehensive architecture documentation (07-ARCHITECTURE.md)
- Security practices documented (10-SECURITY.md)
- Deployment guide with step-by-step instructions

**✅ Code Organization**:
- Clean component separation (9 landing sections)
- Path aliases reduce import complexity (`@/components`)
- Logical file structure (components, pages, hooks, utils)

### Areas Needing Attention

**⚠️ Testing Gap (HIGH PRIORITY)**:
- **Issue**: Zero test coverage (no unit, integration, or E2E tests)
- **Impact**: Risk of regressions, difficult refactoring
- **Recommendation**: Implement Vitest + React Testing Library (Week 1 priority)

**⚠️ CI/CD Pipeline (HIGH PRIORITY)**:
- **Issue**: No automated quality checks before merge
- **Impact**: Manual process prone to human error
- **Recommendation**: GitHub Actions workflow with linting, type checking, tests

**⚠️ Monitoring & Observability (MEDIUM PRIORITY)**:
- **Issue**: No error tracking, performance monitoring, or alerting
- **Impact**: Blind to production issues until user reports
- **Recommendation**: Sentry + Lighthouse CI + UptimeRobot

**⚠️ Staging Environment (MEDIUM PRIORITY)**:
- **Issue**: No dedicated staging environment
- **Impact**: Testing in production (risky)
- **Recommendation**: Enable Netlify branch deploys for `staging` branch

**⚠️ Dependency Management (MEDIUM PRIORITY)**:
- **Issue**: No automated security scanning or updates
- **Impact**: Vulnerable to known CVEs
- **Recommendation**: Enable Dependabot + weekly update schedule

**⚠️ Code Quality Tooling (LOW PRIORITY)**:
- **Issue**: No ESLint, Prettier, or pre-commit hooks
- **Impact**: Inconsistent code style, potential bugs
- **Recommendation**: Set up ESLint + Prettier + Husky

### Technical Debt Inventory

**High-Impact Debt**:
1. **Test Coverage**: 0% → Target 80% (4-6 weeks effort)
2. **CI/CD Pipeline**: None → Full automation (1-2 weeks effort)
3. **Monitoring**: None → Production-ready observability (2-3 weeks effort)

**Medium-Impact Debt**:
4. **Staging Environment**: None → Netlify branch deploys (2 days effort)
5. **Image Optimization**: JPG → WebP/AVIF + lazy loading (3 days effort)
6. **Code Splitting**: Single bundle → Route-based splitting (1 week effort)

**Low-Impact Debt**:
7. **Linting/Formatting**: Manual → Automated (1 day effort)
8. **Documentation**: Good → Excellent (ongoing)
9. **Performance Budget**: None → Lighthouse CI budgets (2 days effort)

### Security Posture Score: 7/10

**Strengths**:
- ✅ Security headers implemented (CSP, HSTS, etc.)
- ✅ HTTPS enforced with HSTS preload
- ✅ Secrets excluded from Git (.gitignore)
- ✅ Static site = minimal attack surface

**Weaknesses**:
- ⚠️ No automated dependency scanning
- ⚠️ CSP allows `unsafe-inline` (Vite requirement)
- ⚠️ No pre-commit secret detection
- ⚠️ No security.txt file

---

## Quick Reference

### Essential Commands

```bash
# 🚀 Local Development
bun install                    # Install dependencies
bun run dev                    # Start dev server (port 8080)
bun run build                  # Production build
bun run preview                # Preview production build locally

# 🔍 Quality Checks (when implemented)
bun run lint                   # Run ESLint
bun run type-check             # TypeScript validation
bun run test                   # Run test suite
bun run test:watch             # Run tests in watch mode

# 📦 Dependency Management
bun outdated                   # Check for outdated packages
bun update                     # Update all dependencies
bun audit                      # Security vulnerability scan

# 🔧 Git Operations
git checkout -b feature/name   # Create feature branch
git push origin feature/name   # Push feature branch
git push origin main           # Deploy to production (triggers Netlify)

# 🚨 Emergency Procedures
# Rollback: Netlify dashboard → Deploys → Previous deploy → "Publish deploy"
# Build failure: Check Netlify logs → Fix → Redeploy
# DNS issues: Porkbun dashboard → DNS settings → Verify records
```

### Critical Endpoints

**Production**:
- Site: https://intentsolutions.io
- www redirect: https://www.intentsolutions.io → https://intentsolutions.io

**Development**:
- Local dev: http://localhost:8080
- Preview build: http://localhost:4173

**Monitoring** (Future):
- Netlify dashboard: https://app.netlify.com/sites/[site-name]/overview
- Sentry: (to be set up)
- Lighthouse CI: (to be set up)

**Documentation**:
- GitHub repo: https://github.com/jeremylongshore/intent-solutions-landing
- Netlify docs: https://docs.netlify.com
- Bun docs: https://bun.sh/docs

### First Week Checklist

```markdown
Day 1: Access & Environment
- [ ] Verify Netlify account access (jeremylongshore@gmail.com)
- [ ] Clone GitHub repository
- [ ] Install Bun runtime (curl -fsSL https://bun.sh/install | bash)
- [ ] Install dependencies (bun install)
- [ ] Start local dev server (bun run dev)
- [ ] Verify site loads at http://localhost:8080

Day 2: Documentation Review
- [ ] Read 01-README.md (project overview)
- [ ] Read 07-ARCHITECTURE.md (system architecture)
- [ ] Read 02-NETLIFY-DEPLOYMENT-GUIDE.md (deployment process)
- [ ] Read 10-SECURITY.md (security practices)
- [ ] Read this document (DevOps guide)

Day 3: Deployment Practice
- [ ] Create test feature branch
- [ ] Make trivial change (update README)
- [ ] Test locally (bun run build && bun run preview)
- [ ] Push to GitHub (observe Netlify build)
- [ ] Verify production deployment
- [ ] Practice rollback in Netlify dashboard

Day 4: Monitoring Setup
- [ ] Set up UptimeRobot (free tier)
- [ ] Configure Sentry error tracking
- [ ] Enable GitHub Dependabot alerts
- [ ] Create Lighthouse CI baseline

Day 5: CI/CD Pipeline
- [ ] Create GitHub Actions workflow (.github/workflows/ci.yml)
- [ ] Add type checking job
- [ ] Add build verification job
- [ ] Test workflow with PR
```

---

## Recommendations Roadmap

### Week 1: Critical Foundation

**Priority 1: Testing Infrastructure** (2-3 days)
```bash
# Set up Vitest + React Testing Library
bun add -d vitest @testing-library/react @testing-library/jest-dom

# Create basic test for utils
# File: src/lib/utils.test.ts
# Target: 100% coverage of cn() function

# Create component test example
# File: src/components/Hero.test.tsx
# Target: Render validation + props testing
```

**Priority 2: CI/CD Pipeline** (1-2 days)
```yaml
# Create .github/workflows/ci.yml
# Jobs:
#   1. Type checking (tsc --noEmit)
#   2. Linting (when ESLint added)
#   3. Tests (vitest run)
#   4. Build verification (bun run build)
#   5. Lighthouse CI (performance budgets)
```

**Priority 3: Error Monitoring** (1 day)
```bash
# Set up Sentry
bun add @sentry/react

# Configure in main.tsx
# Capture unhandled errors, performance metrics
# Send to Sentry dashboard

# Alert on new errors (email)
```

### Month 1: Production Readiness

**Week 2: Staging Environment**
- Enable Netlify branch deploys for `staging` branch
- Configure staging environment variables
- Test full deploy workflow (staging → prod)

**Week 3: Observability Stack**
- Set up UptimeRobot (5-minute checks)
- Implement Lighthouse CI in GitHub Actions
- Configure performance budgets (95+ score)
- Add RUM with Google Analytics 4 or Plausible

**Week 4: Code Quality**
- Add ESLint + Prettier
- Set up Husky pre-commit hooks
- Implement lint-staged (run linters on changed files only)
- Document code style guide

### Quarter 1: Operational Excellence

**Month 2: Advanced Testing**
- Increase test coverage to 80%
- Add E2E tests with Playwright (smoke tests)
- Implement visual regression testing (Percy or Chromatic)
- Set up test coverage reporting (Codecov)

**Month 3: Performance Optimization**
- Implement route-based code splitting (React.lazy)
- Convert images to WebP/AVIF formats
- Add service worker for offline support
- Optimize font loading (preload, font-display: swap)

**Month 3: Security Hardening**
- Enable Dependabot auto-updates (security patches)
- Add pre-commit secret detection (truffleHog, git-secrets)
- Implement stricter CSP (nonce-based, remove unsafe-inline)
- Create security.txt file (/.well-known/security.txt)

### Long-Term Vision (6-12 Months)

**Q2: Feature Expansion**
- Add blog functionality (MDX or headless CMS)
- Implement contact form backend (Netlify Forms or API)
- Add internationalization (i18n) support
- Create admin dashboard (if needed)

**Q3: Scale & Reliability**
- Implement service worker + offline mode
- Add A/B testing capability (Netlify Split Testing)
- Set up multi-region failover (if needed)
- Optimize for markets outside US (CDN edge locations)

**Q4: Enterprise Features**
- SOC 2 compliance (if needed for enterprise clients)
- Implement SSO/SAML (if adding auth)
- Add comprehensive audit logging
- Create disaster recovery runbooks

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| **Atomic Deploy** | All-or-nothing deployment where entire site updates simultaneously (no partial updates) |
| **Bun** | Fast JavaScript runtime and package manager (alternative to Node.js/npm) |
| **CDN** | Content Delivery Network (serves static files from edge locations near users) |
| **CSP** | Content Security Policy (HTTP header preventing XSS attacks) |
| **HMR** | Hot Module Replacement (updates code in browser without full page reload) |
| **HSTS** | HTTP Strict Transport Security (forces HTTPS for specified duration) |
| **JAMstack** | JavaScript, APIs, Markup (modern web architecture for static sites) |
| **RUM** | Real User Monitoring (tracks actual user performance metrics) |
| **SWC** | Speedy Web Compiler (Rust-based JavaScript/TypeScript compiler) |
| **TTI** | Time to Interactive (when page becomes fully interactive) |

### B. Reference Links

**Project Resources**:
- GitHub Repository: https://github.com/jeremylongshore/intent-solutions-landing
- Production Site: https://intentsolutions.io
- Netlify Dashboard: https://app.netlify.com

**Documentation**:
- Bun Docs: https://bun.sh/docs
- Vite Docs: https://vitejs.dev
- React Docs: https://react.dev
- Tailwind CSS: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com
- Netlify Docs: https://docs.netlify.com

**Tools**:
- Lighthouse: https://developers.google.com/web/tools/lighthouse
- Sentry: https://sentry.io/welcome
- UptimeRobot: https://uptimerobot.com

### C. Troubleshooting Guide

**Build Failures**:
```bash
# Issue: "bun: command not found"
# Solution: Install Bun runtime
curl -fsSL https://bun.sh/install | bash
source ~/.bashrc

# Issue: "Module not found" errors
# Solution: Clear cache and reinstall
rm -rf node_modules bun.lockb
bun install

# Issue: Type errors during build
# Solution: Check TypeScript config
bunx tsc --noEmit --pretty
```

**Deployment Issues**:
```bash
# Issue: Netlify build fails
# Solution: Check build logs in Netlify dashboard
# Common causes:
#   1. Dependency installation failure → Check bun.lockb
#   2. Build command error → Verify netlify.toml
#   3. TypeScript errors → Run local build first

# Issue: Site shows old content after deploy
# Solution: Clear CDN cache
# Netlify → Deploys → Trigger deploy → Clear cache and deploy
```

**DNS Problems**:
```bash
# Issue: Domain not resolving
# Solution: Verify DNS records
dig intentsolutions.io

# Should show:
# A record: 75.2.60.5
# TTL: 600 seconds

# Issue: www not redirecting
# Solution: Check CNAME record
dig www.intentsolutions.io

# Should show:
# CNAME: [site-name].netlify.app
```

**Performance Degradation**:
```bash
# Issue: Slow page load
# Solution: Check Lighthouse score
npx lighthouse https://intentsolutions.io --view

# Common issues:
#   1. Large bundle size → Analyze with vite-bundle-visualizer
#   2. Unoptimized images → Convert to WebP, add lazy loading
#   3. Missing caching → Check Netlify headers config
```

### D. Change Management

**How to Keep This Document Updated**:

1. **After Infrastructure Changes**:
   - Update [System Architecture](#system-architecture-overview) section
   - Update [Cloud Services](#cloud-services-in-use) table
   - Document changes in `.claude-docs/` with new numbered file

2. **After Adding Dependencies**:
   - Update [Dependencies](#dependencies--supply-chain) section
   - Run `bun audit` and document security status

3. **After Configuration Changes**:
   - Update relevant config sections (Vite, Tailwind, Netlify)
   - Update [Quick Reference](#quick-reference) if commands changed

4. **Monthly Review**:
   - Verify all URLs and links still work
   - Update performance metrics with latest data
   - Review and update [Recommendations Roadmap](#recommendations-roadmap)

5. **Quarterly Review**:
   - Full audit of all sections for accuracy
   - Update version numbers and dates
   - Archive outdated information

**Document Ownership**:
- **Primary**: DevOps team
- **Contributors**: Development team, Security team
- **Reviewers**: Engineering leadership

---

**Last Updated**: October 4, 2025
**Document Version**: 1.0.0
**Next Review Date**: January 4, 2026
**Maintained By**: DevOps Team

**Status**: ✅ Production system actively serving traffic at https://intentsolutions.io
