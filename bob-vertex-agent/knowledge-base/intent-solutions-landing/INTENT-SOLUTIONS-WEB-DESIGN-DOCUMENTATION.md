# Intent Solutions IO: Complete Web Design & Content Documentation

**Generated**: 2025-11-03
**Project Version**: 2.1.1
**Framework**: Astro 5.14 + React 19 Islands
**Domain**: intentsolutions.io
**Status**: Production Live on Netlify

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Site Architecture Overview](#site-architecture-overview)
3. [Design System](#design-system)
4. [Navigation & Routing Map](#navigation--routing-map)
5. [Page-by-Page Content Analysis](#page-by-page-content-analysis)
6. [Component Library](#component-library)
7. [Layout Patterns](#layout-patterns)
8. [Technical Implementation](#technical-implementation)
9. [Forms & Integrations](#forms--integrations)
10. [SEO & Meta Implementation](#seo--meta-implementation)

---

## Executive Summary

Intent Solutions IO is a professional services landing page showcasing AI automation, private AI infrastructure, cloud architecture, and agent development services. The site employs a monochrome charcoal slate design system with subtle animations and a focus on conversion-oriented content.

### Key Stats
- **Total Pages**: 37 pages (including survey flow)
- **Main Service Pages**: 4 (AI Agents, Private AI, Automation, Cloud & Data)
- **Survey Pages**: 15 sequential steps
- **Legal Pages**: 3 (Terms, Privacy, Acceptable Use)
- **Framework**: Static site generation with Astro 5.14
- **UI Library**: React 19 islands for interactive components
- **Styling**: Tailwind CSS 4 with custom charcoal slate theme
- **Performance Target**: Lighthouse 95+ scores
- **Page Weight**: < 500KB total
- **First Paint**: < 1s

### Core Value Proposition
"Creating industries that don't exist" - Independent AI consultant building automation, RAG agents, and production-ready systems for operators.

---

## Site Architecture Overview

### Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Framework | Astro | 5.14.1 | Static site generation |
| UI Components | React | 19.2.0 | Interactive islands (partial hydration) |
| Styling | Tailwind CSS | 4.1.14 | Utility-first CSS |
| Animations | Framer Motion | 12.23.22 | Page and component animations |
| Smooth Scroll | Lenis | 1.3.11 | Smooth scrolling experience |
| Forms | React Hook Form | 7.64.0 | Form state management |
| Validation | Zod | 4.1.12 | Schema validation |
| Icons | Phosphor Icons | 2.1.10 | Icon library |
| SEO | astro-seo | 0.8.4 | Meta tags and OpenGraph |
| Hosting | Netlify | - | Static hosting + forms + functions |

### Project Structure

```
astro-site/
├── src/
│   ├── components/          # React islands
│   │   ├── Contact.tsx      # Contact form with validation
│   │   ├── Footer.tsx       # Site footer
│   │   ├── Hero.tsx         # Homepage hero
│   │   ├── Products.tsx     # Products showcase
│   │   ├── Services.tsx     # Services grid
│   │   └── SiteNav.astro    # Navigation bar
│   ├── layouts/
│   │   └── Layout.astro     # Base layout with SEO
│   ├── pages/               # All page routes (37 total)
│   │   ├── index.astro      # Homepage
│   │   ├── about.astro      # About page
│   │   ├── agents.astro     # AI Agents service page
│   │   ├── automation.astro # Automation service page
│   │   ├── cloud.astro      # Cloud & Data service page
│   │   ├── private-ai.astro # Private AI service page
│   │   ├── intel-engine.astro # IAE: Model 1 product page
│   │   ├── survey.astro     # Survey landing page
│   │   ├── survey/          # Survey flow (15 pages)
│   │   │   ├── 1.astro through 15.astro
│   │   │   └── thank-you.astro
│   │   ├── terms.astro      # Legal: Terms of Service
│   │   ├── privacy.astro    # Legal: Privacy Policy
│   │   ├── acceptable-use.astro # Legal: AUP
│   │   ├── support.astro    # Support options
│   │   └── [additional detail pages]
│   ├── styles/
│   │   └── global.css       # Charcoal slate theme
│   └── utils/               # Helper functions
├── public/                  # Static assets
│   ├── favicon.svg
│   └── og-image.svg         # OpenGraph image
├── dist/                    # Build output
├── tests/                   # Playwright tests
├── astro.config.mjs        # Astro configuration
├── netlify.toml            # Netlify configuration
├── package.json            # Dependencies
└── tsconfig.json           # TypeScript config
```

---

## Design System

### Theme: Charcoal Slate (Theme 7)

Professional monochrome design with charcoal backgrounds and subtle gradients.

#### Color Palette

```css
/* Primary Backgrounds */
--color-bg-primary: 24 24 27     /* #18181B - zinc-900 */
--color-bg-secondary: 39 39 42   /* #27272A - zinc-800 */
--color-bg-tertiary: 9 9 11      /* #09090B - zinc-950 */

/* Text Colors */
--color-text-primary: 250 250 250     /* #FAFAFA - zinc-50 */
--color-text-secondary: 161 161 170   /* #A1A1AA - zinc-400 */
--color-text-tertiary: 212 212 216    /* #D4D4D8 - zinc-300 */

/* Accent Colors */
--color-accent-primary: 228 228 231   /* #E4E4E7 - zinc-200 */
--color-accent-hover: 250 250 250     /* #FAFAFA - zinc-50 */
--color-accent-indigo: indigo-500     /* For CTAs and highlights */

/* Border Colors */
--color-border: 39 39 42              /* #27272A - zinc-800 */
--color-border-subtle: 161 161 170/0.2 /* zinc-400 20% */
```

#### Typography

**Font Family**: Inter (Google Fonts)
- Primary font for all headings and body text
- Weights: 400, 500, 600, 700, 800, 900

**Type Scale**:

```css
/* Display (4.5rem / 72px) */
.text-display {
  font-size: 4.5rem;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

/* Hero (3.5rem / 56px) */
.text-hero {
  font-size: 3.5rem;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

/* H1 (2.5rem / 40px) */
.text-h1 {
  font-size: 2.5rem;
  line-height: 1.2;
  letter-spacing: -0.01em;
}

/* H2 (2rem / 32px) */
.text-h2 {
  font-size: 2rem;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

/* Body Large (1.125rem / 18px) */
.text-body-lg {
  font-size: 1.125rem;
  line-height: 1.75;
}
```

**Mobile Responsive Typography**:
- Display: 3rem (48px)
- Hero: 2.5rem (40px)
- H1: 2rem (32px)
- H2: 1.75rem (28px)

#### UI Components

**Cards** (`.card-slate`):
```css
background: rgba(var(--color-bg-secondary), 0.6);
border: 1px solid rgb(39 39 42 / 0.2);
border-radius: 0.75rem;
padding: 1.5rem;
backdrop-filter: blur(8px);
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

Hover State:
```css
background: rgb(39 39 42 / 0.8);
border-color: rgb(161 161 170);
box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
```

**Buttons** (`.btn-primary`):
```css
background: rgb(228 228 231);    /* zinc-200 */
color: rgb(24 24 27);           /* zinc-900 */
padding: 0.875rem 1.75rem;
border-radius: 0.5rem;
font-weight: 600;
transition: all 0.3s ease;
```

Hover State:
```css
background: rgb(250 250 250);    /* zinc-50 */
box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
```

#### Gradients

**Main Gradient** (`.bg-gradient-main`):
```css
background: linear-gradient(180deg,
  rgb(var(--color-bg-primary)) 0%,     /* zinc-900 */
  rgb(var(--color-bg-secondary)) 100%  /* zinc-800 */
);
```

**Card Gradient** (`.bg-gradient-card`):
```css
background: rgba(var(--color-bg-secondary), 0.6);
```

#### Spacing System

Follows Tailwind CSS default spacing scale:
- xs: 0.5rem (8px)
- sm: 0.75rem (12px)
- md: 1rem (16px)
- lg: 1.5rem (24px)
- xl: 2rem (32px)
- 2xl: 3rem (48px)
- 3xl: 4rem (64px)

#### Animation System

**Framer Motion Page Animations**:
- Initial: `opacity: 0, y: 20`
- Animate: `opacity: 1, y: 0`
- Duration: 0.8s
- Easing: `[0.4, 0, 0.2, 1]` (cubic-bezier)
- Stagger: 0.1s to 0.15s between elements

**Smooth Scroll** (Lenis):
- Enabled site-wide
- Smooth interpolation
- Native-like feel

**Transitions** (`.transition-smooth`):
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Navigation & Routing Map

### Primary Navigation

Located in `SiteNav.astro` - Sticky navigation bar at top of all pages.

**Desktop Navigation** (visible ≥768px):
```
intent solutions io [logo/home link]
├── home (/)
├── about (/about)
├── private ai (/private-ai)
├── ai agents (/agents)
├── automation (/automation)
├── cloud & data (/cloud)
└── [CTA Button] start a project (/#contact)
```

**Mobile Navigation** (visible <768px):
```
intent solutions io [logo]
└── [CTA Button] start (/#contact)
```

### Complete Site Map

#### Homepage Section Anchors
- `/` - Main landing page
  - `/#contact` - Contact form section (scroll anchor)
  - `/#products` - Products section (scroll anchor)

#### Service Pages
- `/agents` - AI Agents service page
  - `/#pricing` - Pricing comparison section
- `/private-ai` - Private AI infrastructure page
- `/automation` - Automation programs page
- `/cloud` - Cloud & Data architecture page

#### Product Pages
- `/intel-engine` - IAE: Model 1 detailed product page
  - `/#how-it-works` - How it works section

#### Information Pages
- `/about` - About Intent Solutions IO
- `/support` - Support options and contact

#### Survey Flow
- `/survey` - Survey landing page
- `/survey/1` through `/survey/15` - Sequential survey pages (15 steps)
- `/survey/thank-you` - Survey completion page

#### Legal Pages
- `/terms` - Terms of Service
- `/privacy` - Privacy Policy
- `/acceptable-use` - Acceptable Use Policy

#### Supporting Detail Pages
- `/infrastructure` - Infrastructure details
- `/ai-models` - AI models catalog
- `/applications` - Applications playbook
- `/security-compliance` - Security & compliance
- `/a2a` - Agent-to-Agent communication
- `/ai-agents` - Additional AI agents info
- `/thank-you` - General thank you page

### External Links

**Footer Links**:
- Email: `mailto:jeremy@intentsolutions.io`
- GitHub: `https://github.com/jeremylongshore`
- Blog: `https://startaitools.com`
- Portfolio: `https://jeremylongshore.com`

**Hero Section Links**:
- Portfolio: `https://jeremylongshore.com`

**Products Section Links** (external projects):
- Claude Code Plugins Hub: `https://github.com/jeremylongshore/claude-code-plugins-plus`
- DiagnosticPro: `https://diagnosticpro.io`
- StartAITools Blog: `https://startaitools.com`
- Bob's Brain: `https://github.com/jeremylongshore/bobs-brain`
- AI DevOps Documentation: `https://github.com/jeremylongshore/ai-devops-intent-solutions`
- Waygate MCP: `https://github.com/jeremylongshore/waygate-mcp`
- News Pipeline: `https://github.com/jeremylongshore/news-pipeline-n8n`
- Disposable Marketplace: `https://github.com/jeremylongshore/disposable-marketplace-n8n`

---

## Page-by-Page Content Analysis

### 1. Homepage (`/`)

**Purpose**: Primary landing page showcasing services and converting visitors to leads.

**Layout Structure**:
```
├── SiteNav (sticky header)
├── Hero Section (full-height)
├── Tailored Build Paths Section
├── Products Showcase Section (#products)
├── Services Grid Section
├── Contact Form Section (#contact)
└── Footer
```

**Hero Section**:
- **Background**: Gradient from zinc-900 to zinc-800 with subtle glow effect
- **Headline**: "creating industries that don't exist" (text-hero, zinc-50)
- **Subline**: "jeremy_longshore · independent ai consultant" with link to jeremylongshore.com
- **Description**: Value proposition paragraph (text-body-lg, zinc-400)
- **Focus Areas** (bulleted list):
  - "automation programs that eliminate manual reporting"
  - "ai agents and rag systems grounded in your data"
  - "production-ready astro, react, and n8n launches"
- **CTAs**:
  - Primary: "start a project" → `#contact` (btn-primary)
  - Secondary: "view the hustle research survey →" → `/survey` (text link)
- **Animations**: Framer Motion fade-in with stagger effect

**Tailored Build Paths Section**:
- **Background**: zinc-950 with border-top and border-bottom
- **Heading**: "explore tailored build paths" (text-h1, center-aligned)
- **Description**: Single paragraph explaining the options
- **Grid Layout**: 4 cards (responsive: 1 col mobile, 2 cols tablet, 4 cols desktop)

  **Card 1**: AI Agents
  - Link: `/agents`
  - Title: "AI Agents"
  - Description: "3 containerized agents: LinkedIn outbound, meeting intelligence, support triage. Deploy in under 2 hours."
  - CTA: "See pricing & agents →"

  **Card 2**: Private AI
  - Link: `/private-ai`
  - Title: "Private AI"
  - Description: "Keep data on your cloud while offering a ChatGPT-style experience to every teammate."
  - CTA: "Review pricing & ROI →"

  **Card 3**: Automation
  - Link: `/automation`
  - Title: "Automation"
  - Description: "n8n + Netlify workflows that eliminate manual reporting, onboarding, and follow-ups."
  - CTA: "Automation menu →"

  **Card 4**: Cloud & Data
  - Link: `/cloud`
  - Title: "Cloud & Data"
  - Description: "Google Cloud-native architectures—Vertex AI, BigQuery, Firebase—with observability baked in."
  - CTA: "See cloud blueprint →"

**Products Section** (`#products`):
- **Background**: zinc-900
- **Heading**: "products i've shipped" (text-h1, center-aligned)
- **Grid Layout**: 3 columns (responsive: 1 col mobile, 2 cols tablet, 3 cols desktop)
- **9 Product Cards** (card-slate):

  1. **Claude Code Plugins Hub**
     - Description: "227 plugins for Claude Code with Skills Powerkit for plugin management—197 GitHub stars, 26 forks, community-driven development."
     - Badge: "JavaScript • Open Source • 197★"
     - Link: GitHub repo

  2. **DiagnosticPro**
     - Description: "Live automotive diagnostics for service centers—Vertex AI orchestrates triage while Firebase keeps technicians synced in real time."
     - Badge: "TypeScript • React • Vertex AI"
     - Link: diagnosticpro.io

  3. **StartAITools**
     - Description: "Technical research blog documenting real AI implementations, production systems, and practical development guides for engineers."
     - Badge: "Hugo • Technical Writing • Education"
     - Link: startaitools.com

  4. **Bob's Brain**
     - Description: "Collaborative AI assistant with Slack integration—Google Gemini 2.5 Flash, Neo4j knowledge graphs, BigQuery analytics, Cloud Run deployment."
     - Badge: "Python • Gemini • Neo4j"
     - Link: GitHub repo

  5. **AI DevOps Documentation**
     - Description: "Claude-powered runbook generator that ships enterprise-ready docs in minutes; teams deploy it to unblock audits and handoffs."
     - Badge: "JavaScript • Claude API • 19★"
     - Link: GitHub repo

  6. **Waygate MCP**
     - Description: "Secure Model Context Protocol server that drops into enterprise stacks so operators can run AI agents with container isolation."
     - Badge: "Python • Docker • Security"
     - Link: GitHub repo

  7. **HUSTLE**
     - Description: "Youth sports performance tracking backed by a 76-question parent research study—now collecting beta testers via Netlify forms."
     - Badge: "Next.js • PostgreSQL • Research"
     - Link: /survey (internal)

  8. **News Pipeline**
     - Description: "Automated monitoring that converts daily news into structured intelligence briefs for decision makers."
     - Badge: "n8n • AI Analysis • 4★"
     - Link: GitHub repo

  9. **Disposable Marketplace**
     - Description: "Instant micro-marketplaces for manufacturers to collect quotes—CSV-driven inventory, ranked responses, zero custom CMS required."
     - Badge: "Shell • n8n • Automation"
     - Link: GitHub repo

**Services Section**:
- **Background**: Gradient main
- **Heading**: "what i build" (text-h1, center-aligned)
- **Grid Layout**: 2 columns (responsive: 1 col mobile, 2 cols desktop)
- **4 Service Cards** (card-slate):

  1. **automation programs**
     - "Design and implement n8n, Netlify Functions, and Vertex AI workflows that replace manual reporting and onboarding tasks."

  2. **ai agents & rag systems**
     - "Deploy Claude- and OpenAI-powered agents backed by your docs, vector stores, and safety rails so teams trust every recommendation."

  3. **data & infra foundations**
     - "Architect BigQuery, Firebase, and Postgres pipelines with telemetry, access control, and monitoring baked in from day one."

  4. **launch-ready product builds**
     - "Ship Astro + React experiences, surveys, and admin tools with coherent design systems, copy, and analytics instrumentation included."

**Contact Section** (`#contact`):
- **Background**: zinc-900
- **Heading**: "ready to build something?" (text-h1, center-aligned)
- **Description**: "whether you need automation, rapid prototyping, or a full product built from scratch - let's talk."
- **Form** (React Hook Form + Zod validation):
  - Name field (required, min 2 chars)
  - Email field (required, valid email)
  - Project Type dropdown (required):
    - automation
    - prototyping
    - ai-agent
    - data-platform
    - not-sure
  - Message textarea (required, min 10 chars)
  - Honeypot spam protection (hidden "bot-field")
  - Submit button (btn-primary, full width)
- **Form Integration**: Netlify Forms with server-side validation
- **Success Message**: "Thanks for reaching out—expect a reply within one business day."
- **Error Handling**: Displays validation errors and submission errors
- **Direct Contact Section**:
  - Email: jeremy@intentsolutions.io
  - Location: "gulf shores, alabama"

**Footer**:
- Company name: "intent solutions io"
- Tagline: "creating industries that don't exist"
- Location: "gulf shores, alabama"
- **Social Links**:
  - Email: jeremy@intentsolutions.io
  - GitHub: github.com/jeremylongshore
  - Blog: startaitools.com
- **Legal Links**:
  - Terms of Service: /terms
  - Privacy Policy: /privacy
  - Acceptable Use: /acceptable-use
- Copyright: "© 2025 intent solutions io. all rights reserved."

---

### 2. AI Agents Page (`/agents`)

**Purpose**: Showcase the Intent Agent Engine (IAE) multi-level agency system with pricing.

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Agents Grid (3 models)
├── Pricing Comparison Section (#pricing)
├── Custom Tier Section
├── CTA Section
└── Footer
```

**Hero Section**:
- **Background**: Gradient main with glow effect
- **Label**: "containerized ai agents" (uppercase, small, zinc-400)
- **Headline**: "intent-driven agents, solutions delivered" (text-hero)
- **Description**: "Intelligence agents for service businesses that already have paying clients but aren't managing customer data, meeting notes, or support workflows effectively. Deploy in under 2 hours. No vendor lock-in."
- **CTAs**:
  - Primary: "see pricing" → `#pricing`
  - Secondary: "book a demo →" → email link

**Agents Grid**:
- **Background**: zinc-950
- **Layout**: 3-column grid (responsive)
- **Card Style**: Hoverable with border color change

**IAE: Model 1** (Intelligence Core):
- **Link**: `/intel-engine` (detailed product page)
- **Hover Effect**: Border changes to indigo-500/50
- **Title**: "IAE: Model 1 →"
- **Description**: "Intelligence Core. Analyzes your closed deals, learns your ICP, scores leads from one data source. Intelligence only—no execution. Google Cloud native."
- **What's Included**:
  - Vertex AI Anthropic
  - 1 Data Connector
  - ICP Scoring
  - BigQuery Analytics
- **Replaces**: "1-2 data analysts at $80-160K/year salary. Save 78-89% with managed service at $1,497/mo."
- **Pricing Options**:
  - Self-serve: $497/mo
  - Managed: $1,497/mo
  - Custom build: $15-30K + $497/mo

**IAE: Model 2** (Execution Layer):
- **Link**: Email inquiry
- **Hover Effect**: Border changes to zinc-700
- **Title**: "IAE: Model 2 →"
- **Description**: "Execution Layer. Takes scored leads from M1, executes personalized outreach, captures meeting intelligence, sends feedback to M1. Multi-channel orchestration."
- **What It Adds**:
  - LinkedIn Outreach
  - Email Campaigns
  - Meeting Intelligence
  - Feedback Loop
- **Replaces**: "3-5 SDRs at $225-375K/year salary. 10x better response rates. Total with M1: $2,997/mo bundle."
- **Pricing Options**:
  - A la carte: $1,997/mo
  - M1+M2 bundle: $2,997/mo (save $497/mo)

**IAE: Model 3** (Support Intelligence):
- **Link**: Email inquiry
- **Hover Effect**: Border changes to zinc-700
- **Title**: "IAE: Model 3 →"
- **Description**: "Support Intelligence. Monitors support tickets, identifies pain points, sends churn signals to M1, drafts responses using M2 execution layer. Human-in-the-loop approval."
- **What It Adds**:
  - Ticket Triage
  - Response Drafting
  - Churn Prediction
  - ICP Refinement
- **Replaces**: "2 support agents at $120-160K/year salary. First response in 4 minutes vs 4 hours. Full stack: $3,997/mo bundle."
- **Pricing Options**:
  - A la carte: $997/mo
  - Full stack bundle: $3,997/mo (save $1,491/mo)

**Pricing Comparison Section** (`#pricing`):
- **Heading**: "compare deployment options"
- **Description**: "Self-serve: You deploy on your infrastructure. Managed: We host and manage everything."
- **2-Column Grid**:

  **Self-Serve Column**:
  - Deploy on your AWS/GCP infrastructure
  - Docker container with full source access
  - Deploy in under 2 hours with docs
  - Email support within 24 hours
  - Fully exportable configs and data—no lock-in
  - **Price**: Starting at $97/month

  **Managed Column** (Recommended badge):
  - We host on secure cloud infrastructure
  - 99.9% uptime SLA with monitoring
  - Instant access—no deployment needed
  - Priority support within 4 hours
  - Daily backups and auto-scaling included
  - Export your data anytime—no lock-in
  - **Price**: Starting at $297/month

**Custom Tier Section**:
- **Title**: "Custom Development"
- **Description**: "Bespoke agent development for complex, industry-specific workflows"
- **Features**:
  - Custom integrations with proprietary systems
  - Advanced ML tuning for your specific use case
  - Dedicated support and SLA guarantees
- **Pricing**: $5,000–$15,000 one-time setup + $297/mo maintenance
- **CTA**: "Discuss Custom Build" (email link)

**CTA Section**:
- **Background**: zinc-950 with border-top
- **Heading**: "intentional ai, practical solutions"
- **Description**: "Book a 15-minute demo to see the agents in action and discuss your use case."
- **CTAs**:
  - Primary: "book a demo" (email link)
  - Secondary: "see pricing again ↑" → `#pricing`
- **Fine Print**: "jeremy@intentsolutions.io · no contracts · no lock-in · export your data anytime"

---

### 3. Private AI Page (`/private-ai`)

**Purpose**: Sell private AI infrastructure deployments for enterprises needing data sovereignty.

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Problem Statement Section
├── Pricing Section
├── What's Included Section
├── FAQ Section
└── Footer
```

**Hero Section**:
- **Background**: zinc-900 with border-bottom
- **Label**: "private ai for enterprises" (uppercase, small, zinc-500)
- **Headline**: "Your AI. Your data. Your control."
- **Description**: "Launch a ChatGPT-style experience that runs entirely inside your infrastructure. No per-seat pricing, no mystery data trails—just fast, private AI your team actually trusts."

**Problem Statement Section** ("Why cloud AI falls short"):
- **Background**: zinc-950 with border-bottom
- **Layout**: 2-column grid (text + comparison table)
- **Left Column**:
  - Heading: "Why cloud AI falls short"
  - Three pain points (red dots):
    1. **Data privacy**: "Every prompt leaves your environment and lives on somebody else's servers."
    2. **Compliance risk**: "HIPAA, SOC 2, and privilege requirements all hinge on keeping records in-house."
    3. **Total cost**: "$60+ per user adds up fast when every seat needs access."
- **Right Column** (card-slate):
  - **Table**: Side-by-side snapshot
    - Cloud AI vs Your Private AI comparison
    - Rows:
      - Data on vendor servers → Data never leaves your network
      - $60/user/month → $3k/month, unlimited users
      - Forced updates + terms → You decide when models change
      - Limited customization → Full control over prompts + policies

**Pricing Section**:
- **Heading**: "Simple pricing that scales with trust"
- **2-Column Grid**:

  **Professional Package**:
  - Best for teams getting started with private AI
  - Starting at $8,000 one-time (infrastructure deployment, 3 models, team training)
  - Starting at $3,000/month (hosting, monitoring, support, unlimited users)
  - Includes onboarding playbooks and documentation handoff

  **Enterprise Package**:
  - For organizations needing deeper integrations and oversight
  - Starting at $15,000 one-time (custom integrations, fine-tuning, extended onboarding)
  - Starting at $5,000/month (priority support, dedicated optimization)
  - Includes compliance documentation and change management playbooks

**What's Included Section**:
- **Layout**: 2-column grid
- **Left Column** (Linked Cards):

  1. **Infrastructure** → `/infrastructure`
     - "Runs in your cloud account (GCP, AWS, or Azure) with enterprise GPUs, auto-scaling, and 99.9% uptime SLA."

  2. **AI models** → `/ai-models`
     - "Llama 3.1 70B for deep reasoning, Mistral 7B for quick responses, and Qwen 2.5 14B for specialized tasks—plus optional fine-tunes."

  3. **Applications** → `/applications`
     - "Web app, mobile apps, Office add-ins, and open APIs so your workflows stay seamless."

  4. **Security & compliance** → `/security-compliance`
     - "Encryption, RBAC, audit logging, HIPAA/SOC2 readiness, and data residency controls."

  5. **Support** → `/support`
     - "White-glove onboarding, 24/7 monitoring, 4-hour response SLA (1-hour for enterprise), and monthly optimization reviews."

- **Right Column** (card-slate):
  - **Example scopes & pain points**:
    - Healthcare practice · Birmingham, AL
    - Law firm · Gulf Shores, AL
    - CPA firm · Mobile, AL
  - **48-hour launch plan**:
    1. Kickoff call (30 minutes)
    2. Infrastructure deployed
    3. Models installed & tested
    4. Team training session
    5. Go live with support
  - **Security-first data flow** diagram:
    - Cloud AI: User → Internet → Vendor → Training Data → Response
    - Private AI: User → Your Network → Response
    - "Zero external transmission. Ever."

**FAQ Section**:
- **Layout**: 2-column grid
- **Left Column** (Common questions):
  - Can we customize it?
  - What if intent solutions io disappears?
  - How do you handle compliance?
  - Can we integrate it?
- **Right Column** (card-slate):
  - **Ready to get started?**
    - Book 15-minute demo
    - Email: jeremy@intentsolutions.io
  - **About intent solutions io**
    - Jeremy Longshore background
    - Location: Gulf Shores

---

### 4. Automation Page (`/automation`)

**Purpose**: Showcase automation programs using n8n and Netlify.

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Automation Menu Section
├── Stack Section
├── Runbook & Support Section
├── CTA & FAQ Section
└── Footer
```

**Hero Section**:
- **Label**: "automation" (uppercase, small, zinc-500)
- **Headline**: "Automations that feel like an extra teammate"
- **Description**: "We design n8n and Netlify automation programs that handle the boring stuff—reporting, onboarding, follow-ups—while keeping humans in the driver's seat. Everything is documented, observable, and ready for audits."

**Automation Menu Section**:
- **Background**: zinc-950
- **Heading**: "Automation menu"
- **Grid**: 3 columns (responsive)
- **6 Cards** (card-slate):
  1. **Sales & quoting** - "Auto-generate proposals, route approvals, and sync updates back to CRM without the copy-paste grind."
  2. **Customer onboarding** - "Collect docs, spin up accounts, assign tasks, and nudge teams when human touch is required."
  3. **Operations dashboards** - "Pull from spreadsheets, ERPs, and APIs to build daily snapshots with alerts for outliers."
  4. **Revenue collection** - "Trigger reminders, process payments, and reconcile ledgers with audit trails intact."
  5. **Internal comms** - "Schedule updates, summarize meetings, and push highlights to Slack, Teams, or email digests."
  6. **Field service** - "Log work orders, sync photos, and dispatch follow-up tasks so nothing slips through the cracks."

**Stack Section**:
- **Heading**: "Our automation stack"
- **Layout**: 2-column grid
- **Left Column** (Stack description):
  - n8n: Visual builders with TypeScript nodes
  - Netlify Functions: Lightweight serverless endpoints
  - Supabase & Firestore: Secure storage
  - Playwright: Browser automations
  - Observability: Structured logging, dashboards
- **Right Column** (card-slate - Implementation process):
  1. Map the current workflow
  2. Prototype in sandbox
  3. Shadow period with human review
  4. Roll into production with monitoring
  - Typical timeline: 10 business days

**Runbook & Support Section**:
- **Heading**: "Runbook & support"
- **Grid**: 2x2 cards
  1. **Documented playbooks** - "Editable runbooks, diagrams, rollback steps"
  2. **Training included** - "Onboard operators, teach request process"
  3. **Fixed monthly support** - "Flat-rate monitoring, patching, tweaks"
  4. **Compliance friendly** - "Audit logs, access controls, approval trails"

**CTA & FAQ Section**:
- **Layout**: 2-column grid
- **Left Column**:
  - Heading: "Ready to map an automation trail?"
  - Description: "Bring one workflow, we'll show you a path to full automation plus the reporting leadership wants."
  - CTA: "Request an automation audit" → `/#contact`
- **Right Column** (card-slate - FAQ):
  - How do you price automations?
  - Can you integrate with legacy systems?
  - How do we request changes?

---

### 5. Cloud & Data Page (`/cloud`)

**Purpose**: Showcase Google Cloud architecture and data engineering services.

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Core Capabilities Section
├── Engagement Blueprint Section
├── Why Choose Section
├── CTA & FAQ Section
└── Footer
```

**Hero Section**:
- **Label**: "cloud & data" (uppercase, small, zinc-500)
- **Headline**: "Google Cloud foundations built for speed and safety"
- **Description**: "From Vertex AI pipelines to BigQuery analytics and Firebase backends, we build cloud systems that ship fast, stay compliant, and remain simple enough for your team to maintain."

**Core Capabilities Section**:
- **Background**: zinc-950
- **Heading**: "Core capabilities"
- **Grid**: 3 columns (responsive)
- **6 Cards** (card-slate):
  1. **Vertex AI pipelines** - "Model training, evaluation, and deployment workflows with automated guardrails and rollback."
  2. **BigQuery analytics** - "Data warehouses with dbt, scheduled transformations, and Looker Studio dashboards your ops team can trust."
  3. **Firebase / Firestore** - "Real-time application backends with security rules, multitenant support, and offline-first UX."
  4. **Cloud Run & Functions** - "Serverless APIs, cron jobs, and automation endpoints that scale without upkeep."
  5. **Identity & access** - "IAM, service accounts, and workload identity federation configured to keep auditors happy."
  6. **Observability** - "Cloud Logging, Metrics, and Grafana dashboards wired from day one so issues surface immediately."

**Engagement Blueprint Section**:
- **Layout**: 2-column grid
- **Left Column** (Numbered list):
  1. Audit your current architecture and capture success metrics
  2. Design reference architecture diagrams and IaC templates
  3. Implement environments with CI/CD, testing, and monitoring hooks
  4. Roll out to production with training
  - "Most foundations deploy within four weeks"
- **Right Column** (card-slate - Tooling):
  - Terraform, Pulumi, Google Cloud Deploy
  - Cloud Build, GitHub Actions, Artifact Registry
  - Secret Manager + KMS
  - Cloud Armor, VPC Service Controls, BeyondCorp

**Why Choose Section**:
- **Background**: zinc-950
- **Heading**: "Why operators choose intent solutions io"
- **Grid**: 2x2 cards
  1. **Ship fast, stay sane** - "Prioritize workable MVPs with clear handoff docs"
  2. **Operator-first communication** - "Weekly syncs, shared Kanban boards, transparent burn rates"
  3. **Compliance ready** - "Access policies, logging, and backup strategies tuned for HIPAA, SOC2, PCI, or CJIS"
  4. **Handoff without drama** - "Internal teams get training, runbooks, and co-working sessions"

**CTA & FAQ Section**:
- **Layout**: 2-column grid
- **Left Column**:
  - Heading: "Let's tune your cloud roadmap"
  - Description: "Bring your current diagrams (or napkin sketches). We'll highlight gaps, quick wins, and rollout strategies."
  - CTA: "Schedule a cloud workshop" → `/#contact`
- **Right Column** (card-slate - FAQ):
  - Do you only work on Google Cloud?
  - Can you support us after launch?
  - What about data migrations?

---

### 6. About Page (`/about`)

**Purpose**: Establish credibility and explain the company's approach.

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Expertise Grid Section
├── Cloud Partnership Section
├── Production Systems Section
└── Footer
```

**Hero Section**:
- **Label**: "about" (uppercase, small, zinc-500)
- **Headline**: "Pioneering AI with operator-first execution"
- **Description**: "intent solutions io sits where practical operations meets modern AI. We design, ship, and maintain production systems that eliminate manual busywork while keeping data private and compliant. Every build is crafted in Gulf Shores, Alabama, and tuned to go live fast."

**Expertise Grid Section**:
- **Background**: zinc-950 with border
- **Grid**: 4 columns (responsive: 1 col mobile, 2 cols tablet, 4 cols desktop)
- **4 Cards** (card-slate):
  1. **AI / ML Expertise** - "Fine-tuned agents, RAG pipelines, and reasoning systems that deliver measurable wins, not just demos."
  2. **Universal Diagnostics** - "From automotive to healthcare, we build platforms that surface the right insight in the right moment."
  3. **Youth Development** - "The HUSTLE research initiative powers sports families with data-driven coaching and survey-backed insights."
  4. **Market Leadership** - "Active in right-to-repair and emerging AI standards so your infrastructure stays future-ready."

**Cloud Partnership Section**:
- **Layout**: 2-column grid
- **Left Column**:
  - Heading: "Built for cloud partnership"
  - Description paragraph
  - Bullet points:
    - Enterprise-ready AI/ML workloads delivered with IaC
    - Cloud-native design tuned for scale, redundancy, and compliance
    - Continuous R&D to keep your stack modern without breaking production
- **Right Column**:
  - **4-Card Grid** (2x2, card-slate, centered text):
    - AI / ML - Core Technology
    - Cloud - Native Architecture
    - Scale - Enterprise Ready
    - Innovation - Continuous R&D

**Production Systems Section**:
- **Heading**: "Production systems we've shipped"
- **Description**: "We partner directly with operators—dealership principals, partners, and practice owners—to design software that outlasts the hype cycle."
- **Grid**: 2 columns
- **4 Cards** (card-slate):
  1. **DiagnosticPro** - "AI-powered vehicle diagnostics that triage repair orders across multiple rooftops in real time."
  2. **Enterprise Automation** - "n8n and Netlify powered flows that offload onboarding, reporting, and compliance tasks across departments."
  3. **Firebase + Firestore** - "Scalable real-time backends supporting distributed teams and customer-facing analytics."
  4. **Vertex AI Integrations** - "End-to-end pipelines that run on Google Cloud with guardrails around privacy and cost."

---

### 7. IAE: Model 1 Product Page (`/intel-engine`)

**Purpose**: Deep-dive product page for Intent Agent Engine Model 1 (Intelligence Core).

**Layout Structure**:
```
├── SiteNav
├── Hero Section
├── Problem Statement Section
├── How It Works Section (#how-it-works)
├── Add-On Models Section
├── ROI Calculator Section
├── Technical Stack Section
├── Pricing Section
├── CTA Section
└── Footer
```

**Hero Section**:
- **Badge**: "IAE: MODEL 1" (small, bg-zinc-800/50)
- **Headline**: "intelligence before automation"
- **Description**: "Intent Agent Engine with multi-level agency architecture. Intelligence layer learns from your closed deals and scores every lead. Execution agents handle outreach on high-probability targets only. Continuous feedback loop. Google Cloud native. 10x better response rates."
- **CTAs**:
  - Primary: "book a demo" (email link)
  - Secondary: "see how it works ↓" → `#how-it-works`

**Problem Statement Section**:
- **Heading**: "the problem with current automation"
- **Layout**: 2-column comparison
- **Left Card** (Red border - Traditional approach):
  - Scrape 10,000 leads from Apollo
  - Send generic template to everyone
  - 0.5% response rate (50 responses)
  - Burn domain reputation
  - No learning or improvement
- **Right Card** (Green border - Intel Engine approach):
  - Analyze your 50+ closed deals
  - Build ICP model from YOUR wins
  - Score all 10,000 leads
  - Contact only top 500 A-tier (5%)
  - 5-10% response rate (250+ responses)
- **Result Box**: "5x more meetings from 95% less outreach"

**How It Works Section** (`#how-it-works`):
- **Background**: zinc-950
- **Heading**: "how it works"
- **3 Step Cards** (large cards):

  **Step 1: Data Ingestion**
  - Data Sources:
    - Apollo.io (firmographics)
    - Sales Navigator (LinkedIn signals)
    - HubSpot/CRM (closed deals)
    - Clearbit (enrichment)
  - What It Learns:
    - Which verticals close fastest
    - Optimal company size range
    - Tech stack compatibility
    - Funding stage patterns

  **Step 2: ICP Model Training**
  - Builds dynamic scoring model from YOUR closed deals
  - Example pattern discovery (code block):
    ```
    "Series A fintech companies with 20-50 employees
    using Salesforce convert at 42% in 45 days.
    Healthcare takes 6+ months (deprioritize)."
    ```

  **Step 3: Lead Scoring**
  - Scores every prospect 0-100
  - Tiers:
    - A-Tier (80-100): Top 5%, highest conversion probability
    - B-Tier (60-79): Good fit, contact after A-tier exhausted
    - C-Tier (below 60): Low probability, skip or deprioritize

- **Model 1 Output Card**:
  - Code block showing example A-tier leads:
    ```
    A-Tier Leads (Score: 85+)
    • Stripe - Score: 94 - Series A fintech, 35 employees, uses Salesforce
    • Plaid - Score: 89 - Series A fintech, 28 employees, recent $50M raise
    • Brex - Score: 87 - Series B fintech, 45 employees, fast growth signals

    Intelligence insights ready. Add IAE: Model 2 for execution or export for manual outreach.
    ```

**Add-On Models Section**:
- **Heading**: "build your intelligence workflow"
- **Grid**: 2 columns

  **IAE: Model 2 Card**:
  - Execution Layer
  - What It Adds:
    - LinkedIn connection requests
    - Personalized email campaigns
    - Meeting transcription and action items
    - Response tracking and conversion analytics
    - Feedback loop to improve M1 accuracy
  - Pricing:
    - A la carte: $1,997/mo
    - M1+M2 bundle: $2,997/mo (save $497/mo)

  **IAE: Model 3 Card**:
  - Support Intelligence
  - What It Adds:
    - Zendesk/Intercom integration
    - Urgent ticket escalation (4 min vs 4 hours)
    - Response drafting with human approval
    - Churn prediction signals to M1
    - Customer health scoring
  - Pricing:
    - A la carte: $997/mo
    - Full stack bundle: $3,997/mo (save $1,491/mo)

- **Additional Data Connectors Card**:
  - Model 1 includes ONE data source connector
  - Add more sources for richer intelligence
  - 5-column grid showing connector badges:
    - Apollo.io: +$197/mo
    - Sales Navigator: +$197/mo
    - HubSpot: +$197/mo
    - Clearbit: +$197/mo
    - ZoomInfo: +$197/mo

**ROI Calculator Section**:
- **Heading**: "roi breakdown"
- **Layout**: 2-column comparison

  **Traditional SDR Team**:
  - 3 SDRs × $75K salary: $225K/yr
  - Benefits (30%): $67K/yr
  - Tools (Apollo, Sales Nav): $12K/yr
  - **Total Annual Cost**: $304K (red, large)

  **IAE: Model 1**:
  - Managed service: $18K/yr
  - One-time setup: $22.5K
  - Data sources: $3K/yr
  - **Total Year 1 Cost**: $43.5K (green, large)

- **Result Box** (indigo border):
  - "Save $260K in Year 1"
  - "86% cost reduction + 10x better response rates"

**Technical Stack Section**:
- **Heading**: "technical architecture"
- **Grid**: 2 columns + 1 full-width card

  **Intelligence Layer**:
  - Vertex AI (Anthropic Claude)
  - Cloud Run (containerized)
  - Firestore (real-time data)
  - BigQuery (analytics)
  - Google Cloud SDK

  **Execution Agents**:
  - Cloud Run (multi-agent)
  - Pub/Sub (event-driven)
  - Cloud Functions (automation)
  - Firestore (state management)
  - Google Cloud APIs

  **Multi-Level Agency Card** (full-width):
  - Diagram (code block):
    ```
    Intelligence → Pub/Sub → Execution Agents
    Execution Agents → Firestore → Intelligence
    Intelligence: Update model and improve
    ```

**Pricing Section**:
- **Heading**: "pricing"
- **Grid**: 3 columns

  **Self-Serve** ($497/mo):
  - Docker containers delivered
  - You deploy on your infrastructure
  - Email support (24h response)
  - Full source code access
  - CTA: "Get Started" (email link)

  **Managed** ($1,497/mo) - RECOMMENDED badge:
  - We host and manage everything
  - 99.9% uptime SLA
  - Priority support (4h response)
  - Monitoring & auto-scaling
  - Export your data anytime
  - CTA: "Get Started" (email link, indigo button)

  **Custom Build** ($15-30K setup):
  - Bespoke integrations
  - Custom ML model tuning
  - Industry-specific workflows
  - 90-day optimization period
  - + $497/mo maintenance
  - CTA: "Discuss Build" (email link)

**CTA Section**:
- **Heading**: "ready to 10x your outbound?"
- **Description**: "Book a 15-minute demo to see IAE in action with your data."
- **CTA**: "book a demo" (email link)
- **Fine Print**: "jeremy@intentsolutions.io · no contracts · export your data anytime"

---

### 8. Survey Landing Page (`/survey`)

**Purpose**: Recruit beta testers for HUSTLE youth sports tracking app.

**Layout Structure**:
```
├── Minimal Home Link (top-left)
├── Hero Section
├── What You'll Help Build Section
├── Social Proof Section
├── Final CTA Section
└── Custom Footer (not standard Footer component)
```

**Hero Section**:
- **Background**: Gradient main with glow effect
- **Home Link**: "← home" (top-left corner, absolute positioned)
- **Headline**: "help us build the future of youth sports tracking" (text-hero, center-aligned)
- **Subheadline**: "share your experience as a sports parent—get 1 year free when we launch"
- **Benefits Grid**: 4 columns (responsive)

  1. ⏱️ **8-10 minutes** - quick & easy
  2. 💡 **your feedback** - shapes what we build
  3. 🎁 **1 year free** - beta testers reward
  4. 🔒 **fully private** - anonymous responses

- **CTA**: "start survey →" → `/survey/1` (btn-primary, large)
- **Legal Consent Notice** (card with bg-zinc-800/30):
  - "By participating, you agree to our Terms of Service, Acceptable Use Policy, and Privacy Policy."
  - Links to: /terms, /acceptable-use, /privacy
  - COPPA/GDPR compliance notice

**What You'll Help Build Section**:
- **Background**: zinc-950
- **Heading**: "what you'll help us build"
- **Content** (3 paragraphs):
  - What HUSTLE is
  - Why we're building it
  - How your feedback will shape it

**Social Proof Section**:
- **Background**: zinc-900 with border-top
- **Text**: "join sports parents helping us build HUSTLE"
- **Badge Grid**: Flexbox wrap
  - ECNL, MLS Next, AAU, USAG, Perfect Game, USSSA, USA Volleyball, ASA/USA Softball, High School Varsity, Travel Teams
  - Each badge: bg-zinc-800/50, rounded-lg

**Final CTA Section**:
- **Background**: zinc-950
- **Heading**: "ready to share your experience?"
- **Description**: "complete the survey and get early access to HUSTLE when we launch"
- **CTA**: "start survey →" → `/survey/1` (btn-primary, large)

**Custom Footer**:
- Similar to standard footer but integrated into page layout
- Company name, tagline, location
- Social links: email, github, portfolio, blog
- Legal links: terms, privacy
- Copyright notice

**Survey Flow** (`/survey/1` through `/survey/15`):
- 15 sequential survey pages
- Each page captures specific information about youth sports participation
- Navigation: Progress indicator, previous/next buttons
- Final page: `/survey/thank-you` - Confirmation and next steps
- **Integration**: Netlify Forms backend for data collection

---

### 9. Legal Pages

#### Terms of Service (`/terms`)
- **Purpose**: Legal terms governing use of the website and services
- **Layout**: Standard legal document format
- **Content**: Terms, conditions, limitations of liability, etc.

#### Privacy Policy (`/privacy`)
- **Purpose**: Explain data collection, use, and protection practices
- **Layout**: Standard legal document format
- **Content**: GDPR, COPPA compliance, data handling, cookies, etc.

#### Acceptable Use Policy (`/acceptable-use`)
- **Purpose**: Define acceptable and prohibited uses of services
- **Layout**: Standard legal document format
- **Content**: Prohibited activities, enforcement, termination

All legal pages follow the same layout:
```
├── SiteNav
├── Hero Section (simple, with page title)
├── Content Section (legal text)
└── Footer
```

---

### 10. Supporting Detail Pages

These pages provide additional information linked from main service pages:

- **`/infrastructure`** - Infrastructure deployment details
- **`/ai-models`** - AI models catalog and specifications
- **`/applications`** - Applications playbook and integrations
- **`/security-compliance`** - Security guardrails and compliance
- **`/support`** - Support options and SLA details
- **`/a2a`** - Agent-to-Agent communication architecture
- **`/ai-agents`** - Additional AI agents information
- **`/thank-you`** - General thank you page for form submissions

All follow similar layout patterns:
- SiteNav at top
- Hero section with page title
- Content sections with cards and grids
- Footer at bottom

---

## Component Library

### React Components (Interactive Islands)

Located in `src/components/`

#### 1. Hero Component (`Hero.tsx`)

**Purpose**: Homepage hero section with animations.

**Props**: None (static content)

**Features**:
- Framer Motion animations (fade-in with stagger)
- Gradient background with glow effect
- Focus areas bulleted list
- Two CTAs (primary and secondary)
- External link to jeremylongshore.com

**Animation Sequence**:
```javascript
const animations = {
  container: { initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 }, duration: 0.8 },
  label: { delay: 0.15 },
  headline: { delay: 0.25 },
  description: { delay: 0.3 },
  byline: { delay: 0.4 },
  focusAreas: { delay: 0.5 },
  ctas: { delay: 0.6 }
}
```

**Hydration**: `client:load` (loads immediately on page load)

---

#### 2. Products Component (`Products.tsx`)

**Purpose**: Showcase portfolio of shipped products.

**Props**: None (static product array)

**Features**:
- Intersection Observer for scroll-triggered animation
- 9 product cards in 3-column grid
- External links to GitHub repos and live sites
- Technology badges
- Staggered fade-in animation

**Data Structure**:
```typescript
interface Product {
  name: string;
  description: string;
  badge: string;
  link: string;
}
```

**Products**:
1. Claude Code Plugins Hub
2. DiagnosticPro
3. StartAITools
4. Bob's Brain
5. AI DevOps Documentation
6. Waygate MCP
7. HUSTLE
8. News Pipeline
9. Disposable Marketplace

**Hydration**: `client:visible` (loads when scrolled into view)

---

#### 3. Services Component (`Services.tsx`)

**Purpose**: Display service offerings in grid format.

**Props**: None (static services array)

**Features**:
- Intersection Observer for scroll-triggered animation
- 4 service cards in 2-column grid
- Staggered fade-in animation
- Gradient background

**Data Structure**:
```typescript
interface Service {
  title: string;
  description: string;
}
```

**Services**:
1. automation programs
2. ai agents & rag systems
3. data & infra foundations
4. launch-ready product builds

**Hydration**: `client:visible` (loads when scrolled into view)

---

#### 4. Contact Component (`Contact.tsx`)

**Purpose**: Contact form with validation and Netlify Forms integration.

**Props**: None

**Features**:
- React Hook Form for state management
- Zod schema validation
- Netlify Forms integration (server-side submission)
- Honeypot spam protection
- Success/error message handling
- Intersection Observer for scroll-triggered animation

**Form Fields**:
```typescript
interface ContactForm {
  name: string;        // min 2 chars
  email: string;       // valid email
  projectType: string; // required selection
  message: string;     // min 10 chars
}
```

**Project Type Options**:
- automation
- prototyping
- ai-agent
- data-platform
- not-sure

**Validation Rules**:
- Name: Minimum 2 characters
- Email: Valid email format
- Project Type: Must be selected
- Message: Minimum 10 characters

**Form Submission Flow**:
1. Client-side Zod validation
2. Encode form data as URL-encoded
3. POST to `/` with Netlify Forms headers
4. Display success/error message
5. Reset form on success
6. Auto-hide success message after 5 seconds

**Netlify Forms Integration**:
- Hidden field: `form-name="contact"`
- Honeypot field: `bot-field` (hidden)
- Server-side processing by Netlify
- Automated email notifications

**Direct Contact Section**:
- Email: jeremy@intentsolutions.io (clickable mailto link)
- Location: "gulf shores, alabama"

**Hydration**: `client:visible` (loads when scrolled into view)

---

#### 5. Footer Component (`Footer.tsx`)

**Purpose**: Site footer with links and company information.

**Props**: None

**Features**:
- Company branding
- Social links (email, GitHub, blog)
- Legal links (terms, privacy, acceptable use)
- Copyright notice

**Link Structure**:
```
Footer
├── Company Info
│   ├── Name: "intent solutions io"
│   ├── Tagline: "creating industries that don't exist"
│   └── Location: "gulf shores, alabama"
├── Social Links
│   ├── Email: jeremy@intentsolutions.io
│   ├── GitHub: github.com/jeremylongshore
│   └── Blog: startaitools.com
├── Legal Links
│   ├── Terms of Service: /terms
│   ├── Privacy Policy: /privacy
│   └── Acceptable Use: /acceptable-use
└── Copyright: "© 2025 intent solutions io. all rights reserved."
```

**Styling**:
- Background: zinc-950
- Border-top: zinc-800/50
- Centered layout with max-width
- Hover effects on all links (zinc-400 → zinc-200)

**Hydration**: Static (no client-side JavaScript needed)

---

### Astro Components

#### SiteNav Component (`SiteNav.astro`)

**Purpose**: Sticky navigation bar for all pages.

**Features**:
- Sticky positioning (top: 0)
- Backdrop blur effect
- Responsive design (desktop/mobile layouts)
- Active link highlighting

**Navigation Links**:
```typescript
const links = [
  { href: '/', label: 'home' },
  { href: '/about', label: 'about' },
  { href: '/private-ai', label: 'private ai' },
  { href: '/agents', label: 'ai agents' },
  { href: '/automation', label: 'automation' },
  { href: '/cloud', label: 'cloud & data' },
];
```

**Desktop Layout** (≥768px):
- Full navigation with all links
- Logo/home link on left
- Navigation links in center
- CTA button on right: "start a project" → `/#contact`

**Mobile Layout** (<768px):
- Logo/home link on left
- Simplified CTA button on right: "start" → `/#contact`
- No inline navigation links (streamlined for mobile)

**Styling**:
- Background: `backdrop-blur-md bg-zinc-950/70`
- Border-bottom: `border-zinc-800/60`
- Height: 64px (4rem)
- z-index: 50 (above page content)

---

### Layout Component (`Layout.astro`)

**Purpose**: Base layout wrapper for all pages.

**Props**:
```typescript
interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}
```

**Features**:
- HTML document structure
- Global CSS import
- SEO meta tags (astro-seo)
- OpenGraph tags
- Twitter Card tags
- Google Fonts (Inter family)
- Favicon

**Default Values**:
- Description: "independent ai consultant shipping automation, rag agents, and astro + react products for operators who need production results."
- OG Image: `${Astro.site}og-image.svg`

**SEO Configuration**:
- Canonical URLs (auto-generated from page path)
- Site name: "intent solutions io"
- OpenGraph type: "website"
- Twitter card: "summary_large_image"

**Font Loading**:
- Preconnect to fonts.googleapis.com and fonts.gstatic.com
- Inter font family: weights 400, 500, 600, 700, 800, 900
- Display: swap (for performance)

---

## Layout Patterns

### Common Page Layout

Most pages follow this structure:

```astro
---
import Layout from '../layouts/Layout.astro';
import SiteNav from '../components/SiteNav.astro';
import Footer from '../components/Footer';
---

<Layout title="Page Title" description="Page description">
  <SiteNav />

  <main class="bg-zinc-900">
    <!-- Hero Section -->
    <section class="py-24 border-b border-zinc-800/60">
      <div class="container mx-auto px-8">
        <div class="max-w-3xl">
          <p class="uppercase tracking-[0.3em] text-xs font-semibold text-zinc-500 mb-4">
            label
          </p>
          <h1 class="text-h1 font-bold text-zinc-50 mb-6">
            Page Headline
          </h1>
          <p class="text-lg text-zinc-400 leading-relaxed">
            Page description
          </p>
        </div>
      </div>
    </section>

    <!-- Content Sections -->
    <section class="py-24 bg-zinc-950 border-b border-zinc-800/60">
      <!-- Content -->
    </section>

    <!-- More sections... -->
  </main>

  <Footer />
</Layout>
```

### Section Patterns

#### Hero Section Pattern
```astro
<section class="min-h-[60vh] flex items-center bg-gradient-main relative overflow-hidden">
  <div class="absolute w-96 h-96 bg-zinc-100/5 rounded-full blur-3xl top-0 right-0 -translate-y-1/2 translate-x-1/2" />

  <div class="container mx-auto px-8 py-24 relative z-10">
    <div class="max-w-4xl">
      <!-- Hero content -->
    </div>
  </div>
</section>
```

#### Content Section Pattern
```astro
<section class="py-24 bg-zinc-950 border-b border-zinc-800/60">
  <div class="container mx-auto px-8">
    <h2 class="text-h1 font-bold text-zinc-50 mb-12 text-center">
      Section Heading
    </h2>

    <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
      <!-- Cards -->
    </div>
  </div>
</section>
```

#### Grid Layouts
```css
/* 3-column grid */
.grid gap-6 md:grid-cols-2 lg:grid-cols-3

/* 4-column grid */
.grid gap-6 md:grid-cols-2 lg:grid-cols-4

/* 2-column grid */
.grid gap-6 md:grid-cols-2

/* Responsive container */
.container mx-auto px-8
.max-w-3xl mx-auto  /* narrow content */
.max-w-4xl mx-auto  /* medium content */
.max-w-5xl mx-auto  /* wide content */
.max-w-6xl mx-auto  /* very wide content */
```

### Card Pattern
```astro
<div class="card-slate">
  <h3 class="text-lg font-semibold text-zinc-100 mb-2">
    Card Title
  </h3>
  <p class="text-sm text-zinc-400">
    Card description
  </p>
</div>
```

### Link Card Pattern (Hoverable)
```astro
<a href="/page" class="card-slate block transition-smooth hover:border-zinc-600 group">
  <h3 class="text-lg font-semibold text-zinc-100 mb-2 group-hover:text-zinc-50">
    Card Title
  </h3>
  <p class="text-sm text-zinc-400">
    Card description
  </p>
  <span class="mt-3 text-sm text-zinc-200 group-hover:text-zinc-50 inline-flex items-center gap-2">
    Learn more
    <span aria-hidden="true">→</span>
  </span>
</a>
```

---

## Technical Implementation

### Build Configuration

**Astro Config** (`astro.config.mjs`):
```javascript
export default defineConfig({
  site: 'https://intentsolutions.io',
  integrations: [react()],
  vite: {
    plugins: [tailwindcss()]
  }
});
```

**Key Features**:
- React integration for islands architecture
- Tailwind CSS via Vite plugin
- Site URL configured for canonical URLs and sitemap

### Deployment

**Platform**: Netlify

**Build Configuration** (`netlify.toml`):
```toml
[build]
  command = "bun run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"
```

**Netlify Features**:
- Automatic deployments on git push
- Branch previews
- Netlify Forms integration
- Netlify Functions for serverless endpoints
- Custom domain: intentsolutions.io
- SSL/TLS certificates (automatic)

### Performance Optimization

**Astro Islands Architecture**:
- Static HTML generation for non-interactive content
- React islands for interactive components only
- Partial hydration strategies:
  - `client:load` - Load immediately (Hero component)
  - `client:visible` - Load when in viewport (Products, Services, Contact)
  - No JavaScript for static components (Footer, Nav, most content)

**Code Splitting**:
- Automatic code splitting by Astro
- Each React island is a separate bundle
- Lazy loading of non-critical components

**Image Optimization**:
- SVG favicon (small file size)
- SVG OpenGraph image (scalable, small)
- No raster images in current implementation

**CSS Optimization**:
- Tailwind CSS purging of unused styles
- Critical CSS inlined
- Font loading optimization with preconnect

### Testing

**Framework**: Playwright

**Test Coverage**:
- E2E tests for critical user flows
- Contact form submission
- Navigation functionality
- Survey flow
- Cross-browser testing (Chromium, Firefox, WebKit)
- Mobile testing (Mobile Chrome, Mobile Safari)

**Test Commands**:
```bash
npm run test              # Run all tests
npm run test:ui           # Interactive UI mode
npm run test:headed       # Headed browser mode
npm run test:debug        # Debug mode
npm run test:chromium     # Chromium only
npm run test:firefox      # Firefox only
npm run test:webkit       # WebKit only
npm run test:mobile       # Mobile browsers
npm run test:all          # All browsers + mobile
npm run test:report       # View test report
```

---

## Forms & Integrations

### Contact Form Integration

**Technology Stack**:
- React Hook Form (client-side state management)
- Zod (schema validation)
- Netlify Forms (server-side processing)

**Form Configuration**:
```html
<form
  name="contact"
  method="POST"
  data-netlify="true"
  netlify-honeypot="bot-field"
  onSubmit={handleSubmit(onSubmit)}
>
  <input type="hidden" name="form-name" value="contact" />
  <p class="hidden">
    <label>
      Don't fill this out if you're human: <input name="bot-field" />
    </label>
  </p>
  <!-- Form fields -->
</form>
```

**Validation Schema**:
```typescript
const contactSchema = z.object({
  name: z.string().min(2, 'name must be at least 2 characters'),
  email: z.string().email('invalid email address'),
  projectType: z.string().min(1, 'please select a project type'),
  message: z.string().min(10, 'message must be at least 10 characters'),
});
```

**Submission Flow**:
1. **Client-Side Validation**: Zod validates form fields
2. **Form Encoding**: Convert to URL-encoded format
3. **Server Submission**: POST to Netlify Forms endpoint
4. **Response Handling**: Display success/error messages
5. **Email Notification**: Netlify sends email to admin
6. **Form Reset**: Clear form on successful submission

**Spam Protection**:
- Honeypot field (hidden from humans, visible to bots)
- Netlify's built-in spam filtering
- reCAPTCHA can be added if needed

### Survey Form Integration

**Technology**: Netlify Forms

**Survey Structure**:
- 15 sequential pages
- Progressive disclosure of questions
- State management via URL parameters or session storage
- Final submission to Netlify Forms
- Confirmation page with next steps

**Data Collection**:
- Anonymous responses (no PII required)
- COPPA/GDPR compliant design
- Data stored securely by Netlify
- Export capability for analysis

---

## SEO & Meta Implementation

### SEO Strategy

**Core Elements**:
- Unique title tags for every page
- Meta descriptions optimized for click-through
- Canonical URLs to prevent duplicate content
- OpenGraph tags for social sharing
- Twitter Card tags for Twitter sharing
- Structured data (future enhancement)
- XML sitemap (auto-generated by Astro)
- robots.txt (configured for crawlers)

### Meta Tags per Page

**Homepage**:
```html
<title>intent solutions io - ai consultant building real products</title>
<meta name="description" content="independent ai consultant shipping automation, rag agents, and astro + react products for operators who need production results." />
<meta property="og:title" content="intent solutions io - ai consultant building real products" />
<meta property="og:description" content="independent ai consultant shipping automation, rag agents, and astro + react products for operators who need production results." />
<meta property="og:image" content="https://intentsolutions.io/og-image.svg" />
<meta property="og:url" content="https://intentsolutions.io/" />
<meta name="twitter:card" content="summary_large_image" />
```

**AI Agents Page**:
```html
<title>AI Agents - Containerized Automation | Intent Solutions</title>
<meta property="og:url" content="https://intentsolutions.io/agents" />
<!-- Other meta tags follow similar pattern -->
```

**Private AI Page**:
```html
<title>Private AI Infrastructure</title>
<meta name="description" content="Keep AI in your own cloud with fixed pricing, compliance-ready guardrails, and a 48-hour rollout." />
<!-- Other meta tags follow similar pattern -->
```

### OpenGraph Image

**File**: `/public/og-image.svg`
- Format: SVG (scalable, small file size)
- Dimensions: Optimized for social media (1200x630 recommended)
- Content: Brand identity and value proposition
- Used across all pages by default

### Performance SEO

**Core Web Vitals Targets**:
- **LCP (Largest Contentful Paint)**: < 2.5s
- **FID (First Input Delay)**: < 100ms
- **CLS (Cumulative Layout Shift)**: < 0.1
- **FCP (First Contentful Paint)**: < 1s

**Optimization Strategies**:
- Minimal JavaScript (islands architecture)
- Critical CSS inlining
- Font display: swap
- Preconnect to external domains
- Lazy loading of images (when added)
- Code splitting and tree shaking

---

## Appendices

### A. Color Reference

```css
/* Backgrounds */
zinc-950: #09090B (darkest background)
zinc-900: #18181B (primary background)
zinc-800: #27272A (secondary background)

/* Text */
zinc-50: #FAFAFA (primary text)
zinc-300: #D4D4D8 (tertiary text)
zinc-400: #A1A1AA (secondary text)
zinc-500: #71717A (muted text)
zinc-600: #52525B (very muted text)

/* Accents */
zinc-200: #E4E4E7 (light accent)
zinc-700: #3F3F46 (dark accent)
indigo-400: #818CF8 (highlight - medium)
indigo-500: #6366F1 (highlight - strong)
indigo-600: #4F46E5 (highlight - stronger)

/* Borders */
zinc-800: #27272A (standard border)
zinc-700: #3F3F46 (hover border)
zinc-800/50: 50% opacity zinc-800
zinc-800/60: 60% opacity zinc-800

/* Status Colors */
green-400: #4ADE80 (success)
green-500: #22C55E (success strong)
red-400: #F87171 (error)
red-500: #EF4444 (error strong)
```

### B. Typography Reference

```css
/* Font Sizes */
text-xs: 0.75rem (12px)
text-sm: 0.875rem (14px)
text-base: 1rem (16px)
text-lg: 1.125rem (18px) [text-body-lg]
text-xl: 1.25rem (20px)
text-2xl: 1.5rem (24px)
text-3xl: 1.875rem (30px)
text-h2: 2rem (32px)
text-h1: 2.5rem (40px)
text-hero: 3.5rem (56px)
text-display: 4.5rem (72px)

/* Font Weights */
font-normal: 400
font-medium: 500
font-semibold: 600
font-bold: 700
font-extrabold: 800
font-black: 900

/* Line Heights */
leading-none: 1
leading-tight: 1.25
leading-snug: 1.375
leading-normal: 1.5
leading-relaxed: 1.625
leading-loose: 2

/* Letter Spacing */
tracking-tighter: -0.05em
tracking-tight: -0.025em
tracking-normal: 0
tracking-wide: 0.025em
tracking-wider: 0.05em
tracking-widest: 0.1em
tracking-[0.3em]: 0.3em (used for labels)
```

### C. Spacing Reference

```css
/* Padding/Margin Scale */
0: 0
0.5: 0.125rem (2px)
1: 0.25rem (4px)
2: 0.5rem (8px)
3: 0.75rem (12px)
4: 1rem (16px)
5: 1.25rem (20px)
6: 1.5rem (24px)
8: 2rem (32px)
10: 2.5rem (40px)
12: 3rem (48px)
16: 4rem (64px)
20: 5rem (80px)
24: 6rem (96px)
32: 8rem (128px)

/* Common Patterns */
py-24: padding-top & bottom 6rem (96px) [section spacing]
px-8: padding-left & right 2rem (32px) [container padding]
gap-6: gap 1.5rem (24px) [grid gap]
mb-6: margin-bottom 1.5rem (24px) [heading margin]
```

### D. Breakpoints

```css
/* Tailwind Default Breakpoints */
sm: 640px   (mobile landscape, small tablets)
md: 768px   (tablets)
lg: 1024px  (small laptops)
xl: 1280px  (desktops)
2xl: 1536px (large desktops)

/* Common Usage Patterns */
/* Mobile-first approach */
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  <!-- 1 col mobile, 2 cols tablet, 3 cols desktop -->
</div>

/* Hidden on mobile */
<div class="hidden md:flex">
  <!-- Visible tablet and up -->
</div>

/* Mobile only */
<div class="md:hidden">
  <!-- Visible mobile only -->
</div>
```

### E. Animation Timing Functions

```css
/* Easing Functions */
ease-linear: cubic-bezier(0, 0, 1, 1)
ease-in: cubic-bezier(0.4, 0, 1, 1)
ease-out: cubic-bezier(0, 0, 0.2, 1)
ease-in-out: cubic-bezier(0.4, 0, 0.2, 1)

/* Custom Easing (used throughout) */
transition-smooth: cubic-bezier(0.4, 0, 0.2, 1)

/* Duration Scale */
duration-75: 75ms
duration-150: 150ms
duration-300: 300ms
duration-500: 500ms
duration-700: 700ms
duration-1000: 1000ms
```

### F. External Resource Links

**Documentation**:
- Astro: https://docs.astro.build
- React: https://react.dev
- Tailwind CSS: https://tailwindcss.com/docs
- Framer Motion: https://www.framer.com/motion/
- React Hook Form: https://react-hook-form.com
- Zod: https://zod.dev
- Netlify Forms: https://docs.netlify.com/forms/setup/

**Tools**:
- Lighthouse: https://developers.google.com/web/tools/lighthouse
- Playwright: https://playwright.dev
- Google Fonts: https://fonts.google.com

**Repository**:
- GitHub: (private repo, not provided)

---

## Maintenance & Updates

### Content Updates

**To update content**:
1. Locate the relevant page in `src/pages/`
2. Edit the Astro/React component
3. Test locally with `bun run dev`
4. Build with `bun run build`
5. Preview with `bun run preview`
6. Deploy via git push (auto-deploys to Netlify)

### Design System Updates

**To update colors**:
1. Edit `src/styles/global.css`
2. Modify CSS custom properties in `:root`
3. Rebuild and test across all pages

**To update typography**:
1. Edit `src/styles/global.css`
2. Modify `.text-*` utility classes
3. Ensure responsive typography scales properly

### Adding New Pages

1. Create new `.astro` file in `src/pages/`
2. Import Layout and SiteNav
3. Follow established layout patterns
4. Add navigation link to `SiteNav.astro` if needed
5. Update sitemap (automatic with Astro)
6. Test build and deployment

### Adding New Components

1. Create component in `src/components/`
2. Use TypeScript for type safety
3. Follow existing component patterns
4. Add Framer Motion animations if needed
5. Choose appropriate hydration strategy:
   - `client:load` for immediate interaction
   - `client:visible` for scroll-triggered loading
   - Static (no directive) for no JavaScript needed

---

## Conclusion

This documentation provides a comprehensive overview of the Intent Solutions IO website, covering design system, content structure, routing, components, and technical implementation. Use this as the master reference for planning and implementing changes to the website.

For questions or clarifications, contact:
- **Email**: jeremy@intentsolutions.io
- **Location**: Gulf Shores, Alabama

---

**Document Version**: 1.0
**Last Updated**: 2025-11-03
**Maintained By**: Claude Code (Anthropic)
**For**: Intent Solutions IO
