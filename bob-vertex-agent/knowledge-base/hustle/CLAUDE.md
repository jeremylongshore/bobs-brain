# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hustle is a youth soccer statistics tracking application with an embedded NWSL documentary video generation pipeline. It's a Next.js 15 application with PostgreSQL database, deployed on Google Cloud Run.

## Technology Stack

- **Frontend**: Next.js 15.5.4, React 19.1.0, TypeScript 5.x, Tailwind CSS
- **Backend**: Next.js API Routes, Prisma ORM 6.16.3
- **Database**: PostgreSQL (Cloud SQL in production, Docker locally)
- **Authentication**: NextAuth v5.0.0-beta.29 with credentials provider
- **Testing**: Vitest (unit), Playwright (e2e), Testing Library
- **Deployment**: Google Cloud Run with Docker containers
- **CI/CD**: GitHub Actions with Workload Identity Federation
- **Video Pipeline**: Vertex AI Veo 3.0, Lyria audio, FFmpeg assembly
- **Monitoring**: Sentry error tracking, Google Cloud Logging

## Common Commands

### Development
```bash
# Install dependencies
npm install

# Run development server with Turbopack
npm run dev                # Runs on http://localhost:3000 (default Next.js port)

# Database operations (Prisma)
npx prisma generate        # Generate Prisma Client after schema changes
npx prisma migrate dev     # Create and apply migration
npx prisma db push         # Push schema changes without migration
npx prisma studio          # Open Prisma Studio GUI (database browser)
npx prisma db pull         # Pull schema from existing database
npx prisma migrate reset   # Reset database (WARNING: deletes all data)

# Testing
npm test                   # Run all tests (unit + e2e)
npm run test:unit          # Unit tests with Vitest
npm run test:watch         # Vitest watch mode
npm run test:coverage      # Unit tests with coverage report
npm run test:e2e           # E2E tests with Playwright
npm run test:e2e:ui        # Playwright interactive UI mode
npm run test:e2e:headed    # Playwright headed browser mode
npm run test:report        # Show Playwright HTML report
npm run test:security      # Run npm audit

# Linting & Type Checking
npm run lint               # Run ESLint
npx tsc --noEmit          # TypeScript type check (no build output)

# Build
npm run build             # Production build with Turbopack
npm start                 # Start production server
```

### Docker (Local Development)
```bash
# Start PostgreSQL database
cd 06-Infrastructure/docker
docker-compose up -d postgres

# Stop all services
docker-compose down

# View logs
docker-compose logs -f postgres

# Access database directly
docker exec -it hustle-postgres psql -U hustle_admin -d hustle_mvp
```

### Deployment
```bash
# Build for production
npm run build

# Deploy to staging (auto via GitHub Actions)
git push origin main

# Manual Cloud Run deployment (requires gcloud auth)
gcloud run deploy hustle-staging --source . --region us-central1 --project hustle-dev-202510
gcloud run deploy hustle-production --source . --region us-central1 --project hustle-devops

# Check deployment status
gcloud run services describe hustle-staging --region us-central1
gcloud run services logs read hustle-staging --limit=50 --region us-central1
```

### NWSL Video Pipeline
```bash
# Navigate to NWSL directory
cd nwsl/

# CI-ONLY pipeline (requires GitHub Actions with WIF)
# Trigger via GitHub Actions: Actions tab → "Assemble NWSL Documentary" → Run workflow

# Local inspection only (generation requires CI)
ls -la 0000-docs/*-DR-REFF-veo-seg-*.md    # View 8 segment canon files
cat 0000-docs/032-OD-CONF-generation-switches.md  # Generation configuration
cat vertex_ops.log                          # View Vertex AI operations log (after CI run)
```

## Architecture & Key Patterns

### Database Models (Prisma)
The application uses 8 core Prisma models defined in `prisma/schema.prisma`:
- **User**: Authentication, profile data, COPPA compliance tracking
- **Player**: Youth player profiles with parent relationship
- **Game**: Game records with position-specific statistics
- **Account/Session**: NextAuth v5 session management
- **PasswordResetToken**: Time-limited password reset tokens
- **EmailVerificationToken**: Email verification flow
- **VerificationToken**: Generic verification tokens (NextAuth)
- **Waitlist**: Early access signup tracking

### Key Architectural Patterns

**Authentication & Authorization**
- NextAuth v5 with credentials provider (`src/lib/auth.ts`)
- JWT-based sessions (30-day expiry)
- Bcrypt password hashing (10 salt rounds)
- Email verification required before login
- Custom session callbacks extend user object with firstName/lastName

**Database Patterns**
- Prisma Client singleton pattern (`src/lib/prisma.ts`)
- Cascade deletes on parent-child relationships (User → Player → Game)
- Composite indexes for query optimization (e.g., Player parentId + createdAt DESC)
- Position-specific nullable fields (tackles for defenders, saves for goalkeepers)

**API Route Structure**
All routes in `src/app/api/` follow Next.js 15 App Router conventions:
- Route handlers export GET/POST/PUT/DELETE functions
- Authentication via `auth()` from NextAuth
- Zod schema validation in `src/lib/validations/`
- Error responses use standardized JSON format

**Component Organization**
- Server Components by default (Next.js 15 App Router)
- Client components marked with 'use client' directive
- Shared UI components in `src/components/ui/` (shadcn/ui)
- Dashboard components in `src/app/dashboard/`

### NWSL Video Pipeline Architecture
The `nwsl/` directory is a separate CI-only video generation pipeline:
- **Canon System**: 8 markdown specifications define each video segment
- **Vertex AI Integration**: Veo 3.0 for video, Lyria for audio
- **GitHub Actions Only**: Enforced via `gate.sh` - no local execution
- **9-Segment Assembly**: 8×8s video segments + 4s end card = 68s total
- **Workload Identity Federation**: No service account keys, WIF authentication only

Detailed architecture documented in `nwsl/CLAUDE.md`

## Project Structure

```
hustle/
├── src/                           # Source code root
│   ├── app/                       # Next.js 15 App Router
│   │   ├── api/                   # API route handlers
│   │   ├── dashboard/             # Dashboard pages (auth-protected)
│   │   ├── login/                 # Login page
│   │   ├── register/              # Registration page
│   │   ├── forgot-password/       # Password reset flow
│   │   ├── verify-email/          # Email verification
│   │   ├── layout.tsx             # Root layout
│   │   └── page.tsx               # Landing page
│   ├── components/                # React components
│   │   └── ui/                    # shadcn/ui components
│   ├── lib/                       # Core utilities
│   │   ├── auth.ts                # NextAuth v5 configuration
│   │   ├── prisma.ts              # Prisma Client singleton
│   │   ├── email.ts               # Resend email service
│   │   ├── logger.ts              # Google Cloud Logging
│   │   ├── tokens.ts              # Token generation/validation
│   │   └── validations/           # Zod schemas
│   ├── hooks/                     # Custom React hooks
│   ├── types/                     # TypeScript type definitions
│   └── schema/                    # Additional schemas
├── prisma/
│   ├── schema.prisma              # Database schema (8 models)
│   └── migrations/                # Prisma migrations
├── nwsl/                          # NWSL video pipeline (separate project)
│   ├── 0000-docs/                 # Canon specifications (8 segments)
│   ├── 0000-images/               # Reference images
│   ├── 020-audio/                 # Lyria-generated audio
│   ├── 030-video/                 # Veo-generated segments
│   ├── 050-scripts/               # Pipeline shell scripts
│   ├── gate.sh                    # CI enforcement gate
│   └── CLAUDE.md                  # NWSL-specific docs
├── 06-Infrastructure/
│   ├── docker/                    # Docker Compose for local PostgreSQL
│   └── terraform/                 # Cloud Run infrastructure
├── tests/                         # Test suites
│   ├── e2e/                       # Playwright E2E tests
│   └── unit/                      # Vitest unit tests
├── .github/workflows/             # GitHub Actions (7 workflows)
│   ├── ci.yml                     # Continuous integration
│   ├── deploy.yml                 # Cloud Run deployment
│   └── assemble.yml               # NWSL video assembly
└── 000-docs/                      # ALL project documentation (ONLY doc folder)
```

## Environment Variables

Required environment variables (see `.env.example`):
```bash
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/hustle_mvp"

# NextAuth Authentication
NEXTAUTH_SECRET="your-secret-here-min-32-chars"  # Generate: openssl rand -base64 32
NEXTAUTH_URL="http://localhost:4000"             # Local dev uses port 4000

# App Configuration
NODE_ENV="development"                           # development | production
NEXT_PUBLIC_API_DOMAIN="http://localhost:4000"
NEXT_PUBLIC_WEBSITE_DOMAIN="http://localhost:4000"

# Email Service (Resend)
RESEND_API_KEY="re_xxxxx"                        # From resend.com/api-keys
EMAIL_FROM="Your App <noreply@yourdomain.com>"

# Sentry Error Tracking
NEXT_PUBLIC_SENTRY_DSN="https://your-key@sentry.io/project-id"
NEXT_PUBLIC_SENTRY_ENVIRONMENT="development"
SENTRY_AUTH_TOKEN="your-auth-token"
SENTRY_ORG="your-org-slug"
SENTRY_PROJECT="your-project-slug"

# Google Cloud Platform
GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
GCP_PROJECT="your-gcp-project-id"
GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
LOG_RETENTION_DAYS="30"
```

**Note**: The app runs on port 4000 in development (not the default Next.js 3000).

## Testing Strategy

**Test Framework Setup**
- Unit tests: Vitest with @testing-library/react
- E2E tests: Playwright with multiple browsers (Chromium, Firefox, WebKit)
- Coverage: @vitest/coverage-v8
- Mocking: MSW (Mock Service Worker) for API mocking

**Test Organization**
- Unit tests: `src/__tests__/` and co-located `*.test.ts` files
- E2E tests: `tests/e2e/` with auth, dashboard flows
- Test utilities: `vitest.setup.ts`, `playwright.config.ts`

**Running Specific Tests**
```bash
# Run single test file
npx vitest run src/lib/game-utils.test.ts

# Run tests matching pattern
npx vitest run --grep "authentication"

# Run single Playwright spec
npx playwright test tests/e2e/auth.spec.ts

# Debug specific test
npx playwright test --debug tests/e2e/auth.spec.ts
```

## Deployment Configuration

### Google Cloud Run
- **Staging**: `hustle-staging` in `hustle-dev-202510` project
- **Production**: `hustle-production` in `hustle-devops` project
- **Region**: `us-central1`
- **Database**: Cloud SQL PostgreSQL with private IP
- **Secrets**: Google Secret Manager (no .env files in containers)
- **Authentication**: Workload Identity Federation (no service account keys)

### Docker Build
- Multi-stage build in `Dockerfile`
- Base image: node:22-alpine
- Prisma Client generation in build stage
- Runs on port 8080 in container
- Non-root user (nextjs:nodejs)

### GitHub Actions Workflows
Seven automated workflows in `.github/workflows/`:
1. **ci.yml** - Tests, linting, type checking on every push
2. **deploy.yml** - Cloud Run deployment to staging/production
3. **assemble.yml** - NWSL video generation pipeline (CI-only)
4. **release.yml** - Version releases and changelogs
5. **auto-fix.yml** - Automated code formatting
6. **branch-protection.yml** - PR checks enforcement
7. **pages.yml** - GitHub Pages deployment

## Important Development Notes

**Database Workflow**
- Always run `npx prisma generate` after schema changes
- Use `npx prisma migrate dev` for schema changes (creates migration + applies)
- Use `npx prisma db push` for rapid prototyping (no migration file)
- Migrations are committed to Git and run in production

**Authentication Testing**
- Email verification required before login (enforced in authorize callback)
- Test accounts must verify email via verification token flow
- Password reset uses time-limited tokens (check PasswordResetToken model)

**COPPA Compliance**
- User model tracks `agreedToTerms`, `agreedToPrivacy`, `isParentGuardian`
- Players are child profiles linked to parent User accounts
- All player data cascade deletes when parent User is deleted

**Turbopack Usage**
- Development and build use `--turbopack` flag for faster builds
- Turbopack is Next.js 15's new bundler (replaces Webpack)

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: deletes all data)
npx prisma migrate reset

# Check database connection
npx prisma db pull

# View/edit data visually
npx prisma studio

# Check migration status
npx prisma migrate status

# Fix "client out of sync" error
npx prisma generate
```

### Authentication Issues
```bash
# Check if email is verified
npx prisma studio  # Open users table, check emailVerified column

# Manually verify email for testing
# Update emailVerified = new Date() in Prisma Studio

# Check NextAuth session
# Look in browser DevTools → Application → Cookies → next-auth.session-token
```

### Build/Deploy Issues
```bash
# Test production build locally
npm run build
npm start

# Check Cloud Run deployment logs
gcloud run services logs read hustle-staging --limit=50 --region us-central1

# Check service status
gcloud run services describe hustle-staging --region us-central1

# Test deployed service health
curl -I https://hustle-staging-[hash].a.run.app/api/health
```

### NWSL Pipeline Issues
```bash
# NWSL pipeline runs in CI only - check GitHub Actions logs
# Go to: Actions tab → "Assemble NWSL Documentary" → Select run → View logs

# Check WIF authentication (in CI logs)
gcloud auth list --filter=status:ACTIVE

# Verify canon files exist
ls -la nwsl/0000-docs/*-DR-REFF-veo-seg-*.md  # Should show 8 files
```

## Documentation Policy

**CRITICAL: Single Documentation Directory**

This project uses a single flat documentation directory:

- **ONLY 000-docs/** exists for ALL documentation
- **NO claudes-docs/** or any other doc folders
- **NO subdirectories** within 000-docs/
- **All AI-generated docs** go in 000-docs/ with proper naming
- **Format:** `NNN-CC-ABCD-description.ext` (Document Filing System v2.0)

Current status: **168 documents** in 000-docs/ (sequences 001-168)