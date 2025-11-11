# Hustle Codebase Architecture Overview

**Last Updated:** 2025-11-08  
**Project:** Hustle - Youth Sports Statistics Tracking Application  
**Location:** `/home/jeremy/000-projects/hustle/`

---

## Executive Summary

**Hustle** is a modern Next.js 15 application for tracking youth soccer player statistics. The project features a full-stack web application with authentication, player management, game logging, and administrative verification capabilities. The main codebase also includes an NWSL documentary video generation pipeline within the `/nwsl` subdirectory.

### Key Statistics
- **Frontend Framework:** Next.js 15 with React 19 and TypeScript
- **Database:** PostgreSQL with Prisma ORM (6 main models)
- **Authentication:** NextAuth v5 with email verification
- **Deployment:** Google Cloud Run (us-central1)
- **Testing:** Vitest (unit), Playwright (E2E)
- **CI/CD:** GitHub Actions with Google Cloud WIF
- **Monitoring:** Sentry (error tracking) + Google Cloud Logging

---

## Project Structure

```
hustle/
├── 000-docs/                  # Project documentation (33+ docs)
├── 03-Tests/                  # Test configurations & reports
├── 04-Assets/                 # Static assets
├── 05-Scripts/                # Build & deployment scripts
├── 06-Infrastructure/         # Docker, backup terraform
├── 07-Releases/               # Release artifacts
├── 99-Archive/                # Old/unused survey project
├── nwsl/                       # NWSL Documentary video pipeline
│   ├── 000-docs/              # Documentary specifications
│   ├── 001-assets/            # Media assets
│   ├── 020-audio/             # Audio files
│   ├── 030-video/             # Video segments
│   ├── 040-overlays/          # Video overlays
│   ├── 050-scripts/           # Render scripts (Veo, Lyria, FFmpeg)
│   ├── 060-renders/           # Final output
│   └── .github/workflows/     # CI/CD for documentary
├── prisma/                    # Database schemas & migrations
├── public/                    # Static files
├── src/                       # Application source code
│   ├── app/                   # Next.js app directory
│   ├── components/            # React components
│   ├── config/                # Configuration
│   ├── hooks/                 # React hooks
│   ├── lib/                   # Utility libraries
│   ├── prompts/               # AI prompts
│   ├── schema/                # Zod validation schemas
│   ├── types/                 # TypeScript types
│   └── __tests__/             # Unit tests
├── security/                  # Security credentials
├── templates/                 # Email templates
├── terraform/                 # Infrastructure as Code
├── tests/                     # Test setup & scripts
├── .github/workflows/         # CI/CD pipelines
├── .env.example               # Environment template
├── Dockerfile                 # Container image (Node 22 Alpine)
├── next.config.ts             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── playwright.config.ts       # E2E testing configuration
├── vitest.config.mts          # Unit test configuration
├── eslint.config.mjs          # Linting rules
├── package.json               # Dependencies & scripts
└── README.md (not present - documentation in 000-docs/)
```

---

## Technology Stack

### Frontend & Framework
- **Next.js 15.5.4** - React meta-framework with App Router
- **React 19.1.0** - UI library with concurrent features
- **TypeScript 5** - Type-safe development
- **Tailwind CSS 3.4.18** - Utility-first styling
- **Shadcn/ui** - Component library (via components.json)
- **Lucide React 0.544.0** - Icon library
- **Recharts 3.2.1** - Chart/visualization library

### Backend & Server
- **Next.js API Routes** - Serverless API endpoints
- **Prisma 6.16.3** - ORM for PostgreSQL
- **NextAuth v5.0.0-beta.29** - Authentication
- **Resend 6.1.2** - Email service provider
- **Bcrypt/Bcryptjs** - Password hashing
- **Zod 4.1.11** - Runtime schema validation

### Cloud & Infrastructure
- **Google Cloud Platform:**
  - Cloud Run (Serverless container deployment)
  - Cloud SQL (PostgreSQL database)
  - Artifact Registry (Docker image storage)
  - Secret Manager (Secrets storage)
- **Sentry** - Error tracking & monitoring
- **Google Cloud Logging** - Structured logging

### Testing
- **Vitest 3.2.4** - Unit test framework
- **Playwright 1.56.0** - E2E browser testing
- **Testing Library** - Component testing utilities
- **MSW 2.11.4** - Mock Service Worker for API mocking

### Build & DevOps
- **Turbopack** - Next.js fast bundler
- **Docker** - Container runtime (Alpine-based)
- **Terraform** - Infrastructure as Code
- **GitHub Actions** - CI/CD automation

---

## Key Components & Models

### Database Schema (Prisma)

**Core Models:**

1. **User** - Account holders (parents/guardians)
   - Fields: id, firstName, lastName, email, password, phone
   - Legal Compliance: COPPA terms agreement, privacy acceptance
   - Verification: emailVerified, verificationPinHash
   - Relations: players, accounts, sessions, tokens

2. **Player** - Young athletes (children of users)
   - Fields: id, name, birthday, position, teamClub, photoUrl
   - Relations: parent (User), games (Game[])
   - Index: (parentId, createdAt DESC) for efficient queries

3. **Game** - Match statistics
   - Universal Stats: goals, assists, minutesPlayed, result
   - Defensive Stats: tackles, interceptions, clearances, blocks, aerialDuelsWon
   - Goalkeeper Stats: saves, goalsAgainst, cleanSheet
   - Verification: verified, verifiedAt flags
   - Relations: player (Player)

4. **NextAuth Models:**
   - Account - OAuth/credentials provider links
   - Session - Active user sessions
   - VerificationToken - Email verification

5. **Auth Tokens:**
   - PasswordResetToken - Password recovery
   - EmailVerificationToken - Email confirmation

6. **Waitlist** - Early access signups
   - Fields: email, firstName, lastName, source, createdAt

**Indexes:** Composite index on Player for efficient list queries

### Directory Structure - Source Code

```
src/
├── app/                              # Next.js App Router
│   ├── api/                          # API Routes (RESTful endpoints)
│   │   ├── auth/                     # Authentication endpoints
│   │   │   ├── [...nextauth]/        # NextAuth handler
│   │   │   ├── register/             # User registration
│   │   │   ├── login/                # Login endpoint
│   │   │   ├── verify-email/         # Email verification
│   │   │   ├── forgot-password/      # Password reset request
│   │   │   ├── reset-password/       # Password reset submission
│   │   │   └── resend-verification/  # Resend verification email
│   │   ├── players/                  # Player management
│   │   │   ├── [id]/                 # Individual player routes
│   │   │   └── list/                 # Player listing
│   │   ├── games/                    # Game statistics
│   │   │   └── [id]/                 # Individual game routes
│   │   ├── account/                  # User account management
│   │   │   └── pin/                  # Verification PIN
│   │   ├── admin/                    # Admin operations
│   │   │   └── verify-user/          # Admin user verification
│   │   ├── verify/                   # Email verification handler
│   │   ├── waitlist/                 # Waitlist signup
│   │   ├── migrate/                  # Database migration
│   │   ├── healthcheck/              # Health check endpoint
│   │   └── hello/                    # Test endpoint
│   ├── dashboard/                    # Main application dashboard
│   ├── games/                        # Game logging features
│   ├── login/                        # Login page
│   ├── register/                     # Registration page
│   ├── verify-email/                 # Email verification page
│   ├── verify/                       # Verification flow
│   ├── forgot-password/              # Password reset request
│   ├── reset-password/               # Password reset form
│   ├── resend-verification/          # Resend verification
│   ├── privacy/                      # Privacy policy
│   ├── terms/                        # Terms of service
│   ├── page.tsx                      # Home page
│   ├── layout.tsx                    # Root layout
│   └── globals.css                   # Global styles
├── components/
│   ├── layout/                       # Layout components
│   ├── ui/                           # Shadcn/ui components
│   ├── delete-athlete-button.tsx     # Athlete deletion
│   ├── error-boundary.tsx            # Error handling
│   └── waitlist-form.tsx             # Waitlist form
├── hooks/                            # Custom React hooks
├── lib/
│   ├── auth.ts                       # NextAuth configuration
│   ├── email.ts                      # Email service (Resend)
│   ├── email-templates.ts            # Email HTML templates
│   ├── prisma.ts                     # Prisma client
│   ├── logger.ts                     # Structured logging
│   ├── tokens.ts                     # Token generation
│   ├── game-utils.ts                 # Game stat utilities
│   ├── player-utils.ts               # Player utilities
│   ├── utils.ts                      # General utilities
│   ├── auth-security.test.ts         # Auth security tests
│   └── validations/
│       ├── game-schema.ts            # Zod schemas for games
│       └── game-schema.test.ts       # Schema validation tests
├── config/
│   └── env.mjs                       # Environment validation
├── schema/                           # Validation schemas
├── prompts/                          # AI prompt templates
├── types/                            # TypeScript type definitions
└── __tests__/                        # Unit tests
```

---

## API Routes

### Authentication (`/api/auth/`)
- **POST `/api/auth/register`** - Create new user account
- **POST `/api/auth/login`** - Authenticate with credentials (handled by NextAuth)
- **POST `/api/auth/verify-email`** - Verify email address
- **POST `/api/auth/resend-verification`** - Resend verification email
- **POST `/api/auth/forgot-password`** - Request password reset
- **POST `/api/auth/reset-password`** - Complete password reset
- **GET|POST `/api/auth/[...nextauth]`** - NextAuth provider endpoint

### Players (`/api/players/`)
- **GET `/api/players/list`** - List all players for authenticated user
- **POST `/api/players/`** - Create new player
- **GET `/api/players/[id]`** - Get player details
- **PUT `/api/players/[id]`** - Update player
- **DELETE `/api/players/[id]`** - Delete player

### Games (`/api/games/`)
- **GET `/api/games/`** - List games for a player
- **POST `/api/games/`** - Log new game/statistics
- **GET `/api/games/[id]`** - Get game details
- **PUT `/api/games/[id]`** - Update game stats
- **DELETE `/api/games/[id]`** - Delete game record

### Account (`/api/account/`)
- **POST `/api/account/pin`** - Set/verify PIN for stats verification

### Admin (`/api/admin/`)
- **POST `/api/admin/verify-user`** - Verify user as admin

### Other
- **GET `/api/healthcheck`** - Service health check
- **POST `/api/waitlist`** - Add to waitlist
- **POST `/api/migrate`** - Database migration endpoint

---

## Authentication & Authorization

### NextAuth v5 Configuration (src/lib/auth.ts)
- **Provider:** CredentialsProvider (email/password)
- **Password Hashing:** bcrypt (secure password storage)
- **Email Verification:** Required before login
- **Session Management:** JWT-based with Prisma adapter
- **Session Timeout:** Configurable via NextAuth

### Security Features
- Bcrypt password hashing (salting + iterations)
- Email verification tokens (random, expires in 24h)
- Password reset tokens (random, single-use)
- Verification PIN for game stat validation
- COPPA compliance (parental consent tracking)
- Secure HTTP-only cookies (production)

### Token Models
1. **EmailVerificationToken** - 24-hour expiry, single-use
2. **PasswordResetToken** - 1-hour expiry, single-use
3. **Session Token** - NextAuth managed, configurable TTL

---

## Email Service Integration

### Provider: Resend
- **Configuration:** Located in `src/lib/email.ts`
- **Free Tier:** 3,000 emails/month, 100/day
- **API Key:** Set via `RESEND_API_KEY` env var
- **Sender:** Configured via `EMAIL_FROM` env var

### Email Types
1. **Verification Email** - Account activation
2. **Password Reset** - Password recovery
3. **Welcome Email** - New account greeting

### Templates
- Located in `src/lib/email-templates.ts`
- HTML-based with responsive design
- Fallback plain text versions

---

## Build & Deployment

### Build Configuration (next.config.ts)
```typescript
- output: 'standalone'        // Self-contained deployment
- reactStrictMode: true       // Detect side effects
- eslint.ignoreDuringBuilds   // Speed up builds
- typescript.ignoreBuildErrors // Fix issues later
- Sentry integration          // Error tracking
```

### Deployment Target
- **Platform:** Google Cloud Run
- **Container:** Docker (Node 22 Alpine)
- **Port:** 8080 (configurable)
- **Environment:** Production/Staging/Development

### Docker Build Pipeline
1. **base** - Node 22 Alpine image
2. **deps** - Install npm dependencies
3. **builder** - Generate Prisma client, build application
4. **runner** - Production image with optimized files

### Environment Separation
- **Production:** `hustleapp-production` GCP project
- **Staging:** `hustleapp-production` (same project, different service)
- **Development:** Local or dev environment

---

## Continuous Integration & Deployment

### GitHub Actions Workflows

#### 1. CI Workflow (`.github/workflows/ci.yml`)
**Triggers:** Push to main, PR to main
**Jobs:**
- Lint with ESLint
- Type check with TypeScript
- Build with Next.js
- Unit tests with Vitest
- E2E tests with Playwright
- Security audit (npm audit)

#### 2. Deploy Workflow (`.github/workflows/deploy.yml`)
**Triggers:** Push to main (production), PR (staging)
**Production Job:**
1. Checkout code
2. Authenticate to Google Cloud (WIF)
3. Build Docker image
4. Push to Artifact Registry
5. Deploy to Cloud Run
6. Set environment variables from Secret Manager
7. Verify deployment (health check)

**Staging Job:**
1. Same as production but:
   - Triggers on PR
   - Deploys to staging service
   - Comments PR with staging URL

#### 3. Assemble Workflow (`.github/workflows/assemble.yml` - NWSL)
**Triggers:** Manual (workflow_dispatch)
**Inputs:** dry_run (boolean, default true)
**Jobs:**
1. Gate check (verify pipeline readiness)
2. Import NWSL repository specs
3. Generate placeholder media (if dry run)
4. Render Lyria score (orchestral audio)
5. Render Veo segments (AI video generation)
6. Assembly preflight checks
7. Assemble master video with overlays
8. Quality control (ffprobe validation)
9. Upload artifacts to GCS
10. Write CI documentation

### Deployment Secrets (GitHub Actions)
- `WIF_PROVIDER` - Workload Identity Provider
- `WIF_SERVICE_ACCOUNT` - Service account for authentication
- `GCP_PROJECT_ID` - Google Cloud Project (NWSL specific)
- `ORG_READ_TOKEN` - GitHub org token for NWSL repo access

### Cloud Run Configuration
- **CPU:** 1 (adjustable)
- **Memory:** 512MB-4GB (configurable)
- **Concurrency:** 80 (default)
- **Max Instances:** Auto (cost controlled)
- **Min Instances:** 0 (cold start acceptable)
- **Timeout:** 3600 seconds (1 hour)

---

## Testing Strategy

### Unit Tests (Vitest)
**Location:** `src/**/*.{test,spec}.ts{x}` and `src/__tests__/`
**Configuration:** `vitest.config.mts`
**Features:**
- JSDOM environment for DOM testing
- Coverage reporting (v8 provider)
- Test setup file for globals

**Key Test Files:**
- `src/lib/auth-security.test.ts` - Authentication tests
- `src/lib/game-utils.test.ts` - Game stat utilities
- `src/lib/validations/game-schema.test.ts` - Schema validation

### E2E Tests (Playwright)
**Location:** `03-Tests/e2e/`
**Configuration:** `playwright.config.ts`
**Browsers:** Chromium, Firefox, WebKit
**Devices:** Desktop (3), Mobile Chrome, Mobile Safari, Edge, Chrome
**Features:**
- Screenshots on failure
- Video on failure
- HTML report generation
- Trace collection

**Test Base URL:** `http://localhost:4000` (configurable)
**Dev Server:** Starts automatically on port 4000

### Test Commands
```bash
npm run test              # Run unit + E2E
npm run test:unit        # Unit tests only
npm run test:watch       # Watch mode
npm run test:coverage    # Coverage report
npm run test:e2e         # E2E only
npm run test:e2e:ui      # Interactive E2E
npm run test:e2e:headed  # Headed browser
npm run test:report      # Show Playwright HTML report
npm run test:security    # Npm audit
```

---

## NWSL Documentary Pipeline

### Overview
A sophisticated multi-phase video generation pipeline for the NWSL documentary "Why Won't They Answer?" embedded within the main Hustle project under `/nwsl/`.

### Architecture

**Input Phase:**
1. Documentary specs from `/nwsl/000-docs/`
2. Asset references and continuity rules
3. Overlay specifications and timing data

**Processing Phases:**
1. **Veo Rendering** - AI video generation (Google Vertex AI Veo 3.0)
2. **Lyria Rendering** - Orchestral score generation
3. **Overlay Processing** - Text, graphics, scene overlays
4. **Audio Mixing** - Loudness normalization, final mix
5. **Assembly** - 9-segment concatenation with seamless transitions

**Output Phase:**
- Master 16:9 (1920x1080, 24fps)
- Social formats (9:16, 1:1)
- Quality assurance validation

### Key Scripts (050-scripts/)
- `veo_render.sh` - Submit Veo API requests, manage LROs
- `lyria_render.sh` - Generate orchestral composition
- `ffmpeg_assembly_9seg.sh` - 9-segment video assembly
- `ffmpeg_overlay_pipeline.sh` - Overlay application
- `audio_qc.sh` - Audio loudness validation
- `video_qc.sh` - Video format validation
- `generate_checksums.sh` - Output verification
- `query_vertex_logs.sh` - Monitor Vertex AI operations

### Technical Stack
- **API:** Google Vertex AI (Veo 3.0, Imagen)
- **Orchestration:** GitHub Actions with WIF
- **Processing:** FFmpeg, ImageMagick
- **Storage:** Google Cloud Storage
- **Authentication:** Workload Identity Federation

### Documentation Standards
- Numbered files with filing codes (001-PP-PROD, etc.)
- Category codes (PP=Product, AT=Architecture, etc.)
- Document types (PROD, PLAN, REFF, DEPL, etc.)
- Comprehensive audit trail of all decisions

### Current Status (as of Nov 8, 2025)
- Phase 1-4 complete: Scaffold, overlays, Lyria, Veo
- Phase 5 in progress: 9-segment assembly
- Canon-locked: Specifications frozen for reproducibility
- GitHub Actions CI: Fully functional with WIF
- Outputs: GCS storage with run-specific paths

---

## Configuration & Environment

### Environment Variables

**Required:**
```
DATABASE_URL              # PostgreSQL connection string
NEXTAUTH_SECRET           # Min 32 chars, for session encryption
NEXTAUTH_URL              # Public callback URL (http://localhost:4000 or prod domain)
```

**Google Cloud:**
```
GCP_PROJECT               # GCP project ID
GOOGLE_APPLICATION_CREDENTIALS  # Path to service account JSON
```

**Email (Resend):**
```
RESEND_API_KEY           # Resend email service API key
EMAIL_FROM               # Sender address (e.g., "HUSTLE <noreply@domain.com>")
```

**Sentry (Error Tracking):**
```
SENTRY_DSN               # Sentry client-side DSN
SENTRY_ENVIRONMENT       # Environment (development/staging/production)
SENTRY_ORG, SENTRY_PROJECT, SENTRY_AUTH_TOKEN  # For source map upload
APP_VERSION              # Application version
```

**Optional:**
```
NODE_ENV                 # development/production
LOG_RETENTION_DAYS       # Cloud Logging retention (default 30)
NEXT_PUBLIC_*            # Any public env vars (browser-accessible)
```

### Secret Management
- **Development:** `.env.local` file
- **Production:** Google Secret Manager
- **CI/CD:** GitHub secrets + Secret Manager

---

## Documentation

### Main Documentation (000-docs/)
33+ markdown files covering:
- Product requirements and roadmaps
- Architecture decisions
- Deployment guides
- Infrastructure setup
- Test strategies
- Troubleshooting guides

### Key Documents
- `001-PP-PROD-hustle-mvp-v1.md` - MVP requirements
- `002-PP-PROD-hustle-mvp-v2-lean.md` - Lean version spec
- `010-OD-DEPL-cloud-run-deployment.md` - Deployment guide
- `015-AT-ADEC-nextauth-migration.md` - Auth architecture
- `017-RA-ANLY-devops-system-analysis.md` - System analysis

### NWSL Documentation (nwsl/000-docs/)
73+ files covering documentary pipeline:
- Segment specifications with timing
- Continuity rules and style guides
- Overlay specifications
- Audio mix manifests
- Phase completion reports
- CI/CD implementation details

---

## Development Workflow

### Local Development
```bash
# Install dependencies
npm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with local values

# Run development server
npm run dev
# Opens on http://localhost:3000 (next) or port 4000 (configured)

# Run tests in watch mode
npm run test:watch

# Type checking
npx tsc --noEmit

# Linting
npm run lint
```

### Database Management
```bash
# View database schema
npx prisma studio

# Run migrations
npx prisma migrate dev --name [migration_name]

# Generate Prisma client
npx prisma generate

# View database state
npx prisma db pull  # Update schema from database
npx prisma db push  # Push schema to database
```

### Production Build
```bash
# Build application
npm run build

# Start production server
npm start

# Or via Docker
docker build -t hustle:latest .
docker run -p 8080:8080 -e DATABASE_URL=... hustle:latest
```

---

## Key Architectural Decisions

1. **Next.js 15 with App Router** - Modern React framework with server components
2. **PostgreSQL + Prisma** - Type-safe ORM with migrations
3. **NextAuth v5** - Flexible authentication with email verification
4. **Email via Resend** - Reliable, free-tier email service
5. **Sentry Integration** - Production error tracking
6. **Google Cloud Run** - Serverless, cost-effective deployment
7. **Standalone Build** - Docker optimized, deployable anywhere
8. **TypeScript Strict Mode** - Catch errors at compile time
9. **Playwright E2E** - Cross-browser testing
10. **GitHub Actions + WIF** - Secure, token-free CI/CD

---

## Unique Patterns & Practices

1. **Embedded NWSL Pipeline** - Documentary video generation within main project
2. **Comprehensive Documentation** - Filing system with categorized numbered docs
3. **Google Cloud WIF** - Keyless authentication for CI/CD
4. **Vertex AI Integration** - Advanced AI models for video/audio generation
5. **Canon-Locked Specs** - Documentary specifications frozen for reproducibility
6. **Multi-Format Export** - 16:9, 9:16, 1:1 aspect ratios from same content
7. **Phase-Based Development** - Documentary pipeline phases with gate checks
8. **GCS Artifact Storage** - Run-specific storage paths for CI output

---

## Performance Optimizations

1. **Turbopack** - Faster builds and dev server
2. **Standalone Output** - Optimized for Cloud Run
3. **Prisma Composable Schemas** - Efficient queries
4. **Image Optimization** - Next.js Image component
5. **Database Indexes** - Composite index on Player queries
6. **API Response Caching** - Configurable via Next.js headers
7. **Sentry Sampling** - 10% production traces, 100% dev

---

## Monitoring & Observability

### Error Tracking
- **Sentry** - JavaScript/Python error monitoring
- **Filters** - Sensitive data redaction (tokens, passwords)
- **Sampling** - Production: 10%, Development: 100%

### Logging
- **Google Cloud Logging** - Structured logging
- **Log Retention** - 30 days (configurable)
- **Integration** - Automatic via Google Application Credentials

### Health Checks
- **GET /api/healthcheck** - Service availability
- **CI/CD Verification** - Post-deployment health check
- **Database Connectivity** - Implicit in migrations

---

## Deployment Checklist

Before deploying to production:
- [ ] All CI checks pass
- [ ] E2E tests pass
- [ ] Database migrations reviewed
- [ ] Environment variables configured
- [ ] Sentry DSN updated
- [ ] Email service keys verified
- [ ] Google Cloud quotas checked
- [ ] Secrets Manager populated
- [ ] WIF credentials active
- [ ] Health check passing

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `package.json` | Dependencies & npm scripts |
| `tsconfig.json` | TypeScript configuration |
| `.env.example` | Environment template |
| `next.config.ts` | Next.js configuration |
| `Dockerfile` | Container image definition |
| `prisma/schema.prisma` | Database schema |
| `src/lib/auth.ts` | NextAuth configuration |
| `src/lib/email.ts` | Email service |
| `sentry.server.config.ts` | Error tracking |
| `.github/workflows/ci.yml` | CI pipeline |
| `.github/workflows/deploy.yml` | Deployment pipeline |
| `nwsl/.github/workflows/assemble.yml` | Documentary pipeline |
| `playwright.config.ts` | E2E test configuration |
| `vitest.config.mts` | Unit test configuration |

---

## Contact & Support

**Project Location:** `/home/jeremy/000-projects/hustle/`  
**Documentation:** `000-docs/` directory  
**CI/CD Status:** `.github/workflows/` (check GitHub Actions)  
**Issues & PRs:** GitHub repository

---

Generated: 2025-11-08  
Codebase Analysis: Complete  
