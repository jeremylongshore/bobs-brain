# Hustle™ System Architecture

**Document Type:** Reference - Technical Architecture
**Status:** Active
**Last Updated:** 2025-10-08
**Version:** 1.0.0
**Engineer:** Jeremy (DevOps Lead)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Data Models](#data-models)
5. [Authentication & Security](#authentication--security)
6. [Infrastructure](#infrastructure)
7. [Third-Party Services](#third-party-services)

---

## Executive Summary

**Hustle™** is a Next.js-based web application for tracking youth soccer player statistics. Parents manage player profiles, log game stats, and track performance over time with team verification capabilities.

### Current State

**Environment:** Development (local + Docker)
**Production Status:** Not yet deployed to Cloud Run
**Scale:** MVP stage, single instance
**Users:** None yet (pre-launch)

### Core Capabilities

- User registration with email verification
- Password reset flows
- Player profile management (birthday, position, team)
- Game statistics logging (goals, assists, saves, etc.)
- Team-based verification system
- Professional email notifications

### Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Framework** | Next.js 15.5.4 | Modern React framework with SSR, API routes, great DX |
| **Build Tool** | Turbopack | Faster builds than webpack, Next.js native |
| **Authentication** | NextAuth v5 | Industry standard, JWT-based, flexible |
| **Database** | PostgreSQL 15 | Relational data, ACID compliance, proven at scale |
| **ORM** | Prisma | Type-safe, great DX, migration tools |
| **Email** | Resend | Generous free tier (3k/month), simple API |
| **Deployment** | Cloud Run | Scales to zero, pay-per-use, Docker-based |
| **IaC** | Terraform | Infrastructure as code, version controlled |

---

## Technology Stack

### Frontend/UI

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 19.1.0 | UI library |
| **Next.js** | 15.5.4 | React framework with App Router |
| **TypeScript** | 5.x | Type safety |
| **Tailwind CSS** | 3.4.18 | Utility-first styling |
| **shadcn/ui** | Latest | Radix UI + Tailwind components |
| **Lucide Icons** | 0.544.0 | Icon library |
| **React Hook Form** | 7.64.0 | Form management |
| **Zod** | 4.1.11 | Schema validation |

### Backend/API

| Technology | Version | Purpose |
|------------|---------|---------|
| **Next.js API Routes** | 15.5.4 | RESTful API endpoints |
| **NextAuth** | 5.0.0-beta.29 | Authentication |
| **Prisma** | 6.16.3 | ORM and migrations |
| **bcrypt** | 6.0.0 | Password hashing |
| **jsonwebtoken** | 9.0.2 | JWT token handling |

### Database

| Technology | Version | Purpose |
|------------|---------|---------|
| **PostgreSQL** | 15.x | Primary database |
| **Prisma Client** | 6.16.3 | Type-safe query builder |

### Infrastructure

| Technology | Version | Purpose |
|------------|---------|---------|
| **Docker** | Latest | Containerization |
| **Docker Compose** | Latest | Local orchestration |
| **Terraform** | 1.5+ | Infrastructure as Code |
| **Google Cloud Run** | N/A | Serverless container platform |
| **Cloud SQL** | PostgreSQL 15 | Managed database |

### Development Tools

| Technology | Version | Purpose |
|------------|---------|---------|
| **Playwright** | 1.56.0 | E2E testing |
| **ESLint** | 9.x | Code linting |
| **TypeScript Compiler** | 5.x | Type checking |

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Browser   │  │   Mobile    │  │   Desktop   │         │
│  │  (Chrome)   │  │  (Safari)   │  │   (Edge)    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘         │
│         │                │                │                  │
│         └────────────────┴────────────────┘                  │
│                         │                                     │
│                    HTTPS/443                                 │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                         │                                     │
│              ┌──────────▼──────────┐                         │
│              │    Next.js App      │                         │
│              │   (Cloud Run)       │                         │
│              │                     │                         │
│              │  ┌───────────────┐  │                         │
│              │  │  React Pages  │  │                         │
│              │  │  (SSR/CSR)    │  │                         │
│              │  └───────────────┘  │                         │
│              │                     │                         │
│              │  ┌───────────────┐  │                         │
│              │  │  API Routes   │  │                         │
│              │  │  /api/*       │  │                         │
│              │  └───────┬───────┘  │                         │
│              │          │          │                         │
│              │  ┌───────▼───────┐  │                         │
│              │  │   NextAuth    │  │                         │
│              │  │   (JWT)       │  │                         │
│              │  └───────┬───────┘  │                         │
│              │          │          │                         │
│              │  ┌───────▼───────┐  │                         │
│              │  │ Prisma Client │  │                         │
│              │  └───────┬───────┘  │                         │
│              └──────────┼──────────┘                         │
│                         │                                     │
└─────────────────────────┼───────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────┐
│                    DATA LAYER                                │
│                         │                                     │
│              ┌──────────▼──────────┐                         │
│              │   PostgreSQL 15     │                         │
│              │   (Cloud SQL)       │                         │
│              │                     │                         │
│              │  ┌───────────────┐  │                         │
│              │  │     users     │  │                         │
│              │  │    players    │  │                         │
│              │  │     games     │  │                         │
│              │  │    tokens     │  │                         │
│              │  └───────────────┘  │                         │
│              └─────────────────────┘                         │
│                                                               │
└───────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                           │
│                                                               │
│              ┌─────────────────────┐                         │
│              │    Resend API       │                         │
│              │ (Email Delivery)    │                         │
│              └─────────────────────┘                         │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Request Flow

**1. User Registration Flow**
```
User → /register page (React)
  ↓
Form submit → POST /api/auth/register
  ↓
API validates input
  ↓
bcrypt hashes password
  ↓
Prisma creates user in DB (emailVerified = null)
  ↓
Generate verification token (crypto.randomBytes)
  ↓
Store token in DB with 24h expiration
  ↓
Send email via Resend API
  ↓
Return success to user
```

**2. Login Flow**
```
User → /login page (React)
  ↓
Form submit → NextAuth signIn()
  ↓
POST /api/auth/[...nextauth]
  ↓
NextAuth authorize() function
  ↓
Query user from DB (Prisma)
  ↓
bcrypt.compare(password, hashedPassword)
  ↓
Check if emailVerified is set
  ↓
If verified: Generate JWT token
  ↓
Set session cookie
  ↓
Redirect to /dashboard
```

**3. Protected Page Access**
```
User → /dashboard (React Server Component)
  ↓
Server checks session: await auth()
  ↓
If no session: redirect('/login')
  ↓
If session exists: render page with user data
```

**4. Game Logging Flow**
```
User → /games/new page (React)
  ↓
Form submit → POST /api/games
  ↓
API checks session (await auth())
  ↓
Validate input with Zod schema
  ↓
Prisma creates game record
  ↓
Links to player (via playerId foreign key)
  ↓
Sets verified = false initially
  ↓
Return success
```

### Directory Structure

```
/home/jeremy/projects/hustle/
├── src/
│   ├── app/                        # Next.js App Router
│   │   ├── api/                    # API Routes
│   │   │   ├── auth/
│   │   │   │   ├── [...nextauth]/  # NextAuth handler
│   │   │   │   ├── register/       # User registration
│   │   │   │   ├── verify-email/   # Email verification
│   │   │   │   ├── forgot-password/
│   │   │   │   ├── reset-password/
│   │   │   │   └── resend-verification/
│   │   │   ├── players/            # Player CRUD
│   │   │   ├── games/              # Game stats CRUD
│   │   │   ├── healthcheck/        # Health endpoint
│   │   │   └── migrate/            # Database migration
│   │   ├── dashboard/              # Protected dashboard
│   │   ├── login/                  # Login page
│   │   ├── register/               # Registration page
│   │   ├── verify-email/           # Email verification page
│   │   ├── forgot-password/        # Password reset request
│   │   ├── reset-password/         # Password reset page
│   │   ├── resend-verification/    # Resend verification email
│   │   ├── page.tsx                # Landing page
│   │   └── layout.tsx              # Root layout
│   ├── components/
│   │   ├── ui/                     # shadcn/ui components
│   │   └── layout/                 # Layout components
│   ├── lib/
│   │   ├── auth.ts                 # NextAuth config
│   │   ├── prisma.ts               # Prisma client singleton
│   │   ├── email.ts                # Resend email service
│   │   ├── email-templates.ts      # Email HTML templates
│   │   └── tokens.ts               # Token generation/validation
│   └── types/
│       └── next-auth.d.ts          # NextAuth type declarations
├── prisma/
│   ├── schema.prisma               # Database schema
│   └── migrations/                 # Database migrations
├── public/                         # Static assets
├── 01-Docs/                        # Documentation
├── 06-Infrastructure/
│   ├── docker/
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   └── .dockerignore
│   └── terraform/                  # Infrastructure as Code
│       ├── main.tf
│       ├── compute.tf              # Cloud Run
│       ├── database.tf             # Cloud SQL
│       ├── network.tf              # VPC
│       ├── storage.tf              # Storage buckets
│       └── outputs.tf
└── 99-Archive/                     # Archived code
```

---

## Data Models

### Entity Relationship Diagram

```
┌──────────────────┐
│      User        │
├──────────────────┤
│ id (PK)          │
│ firstName        │
│ lastName         │
│ email (unique)   │
│ emailVerified    │
│ phone            │
│ password (hash)  │
│ createdAt        │
│ updatedAt        │
└────────┬─────────┘
         │
         │ 1:N
         │
┌────────▼─────────┐
│     Player       │
├──────────────────┤
│ id (PK)          │
│ name             │
│ birthday         │
│ position         │
│ teamClub         │
│ photoUrl         │
│ parentId (FK)    │◄───┐
│ createdAt        │    │
│ updatedAt        │    │
└────────┬─────────┘    │
         │              │
         │ 1:N          │
         │              │
┌────────▼─────────┐    │
│      Game        │    │
├──────────────────┤    │
│ id (PK)          │    │
│ playerId (FK)    │────┘
│ date             │
│ opponent         │
│ result           │
│ finalScore       │
│ minutesPlayed    │
│ goals            │
│ assists          │
│ saves            │
│ goalsAgainst     │
│ cleanSheet       │
│ verified         │
│ verifiedAt       │
│ createdAt        │
│ updatedAt        │
└──────────────────┘

┌────────────────────────────┐
│  EmailVerificationToken    │
├────────────────────────────┤
│ id (PK)                    │
│ token (unique)             │
│ userId (FK) → User.id      │
│ expires                    │
│ createdAt                  │
└────────────────────────────┘

┌────────────────────────────┐
│   PasswordResetToken       │
├────────────────────────────┤
│ id (PK)                    │
│ token (unique)             │
│ userId (FK) → User.id      │
│ expires                    │
│ createdAt                  │
└────────────────────────────┘

┌────────────────────────────┐
│      NextAuth Models       │
├────────────────────────────┤
│ Account                    │
│ Session                    │
│ VerificationToken          │
└────────────────────────────┘
```

### Core Models

#### User

**Purpose:** Parent/guardian accounts that manage player profiles

```prisma
model User {
  id            String    @id @default(cuid())
  firstName     String
  lastName      String
  email         String    @unique
  emailVerified DateTime?
  phone         String?
  password      String    // bcrypt hashed
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  // Relations
  players                  Player[]
  passwordResetTokens      PasswordResetToken[]
  emailVerificationTokens  EmailVerificationToken[]
  accounts                 Account[]
  sessions                 Session[]
}
```

**Key Fields:**
- `emailVerified`: Null until email verified, then timestamp
- `password`: bcrypt hashed with 10 rounds
- `phone`: Optional field (not required for registration)

#### Player

**Purpose:** Youth soccer player profiles (ages 8-18)

```prisma
model Player {
  id        String   @id @default(cuid())
  name      String
  birthday  DateTime
  position  String
  teamClub  String
  photoUrl  String?
  parentId  String   // FK to User
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  parent User   @relation(fields: [parentId], references: [id], onDelete: Cascade)
  games  Game[]
}
```

**Key Fields:**
- `birthday`: Stored as DateTime, age calculated dynamically in UI
- `position`: Free text (e.g., "Forward", "Midfielder", "Goalkeeper")
- `teamClub`: Free text team name
- `photoUrl`: Optional path to uploaded player photo

**Cascade Delete:** If parent user is deleted, all players are deleted

#### Game

**Purpose:** Individual game statistics and performance data

```prisma
model Game {
  id            String    @id @default(cuid())
  playerId      String    // FK to Player
  date          DateTime  @default(now())
  opponent      String
  result        String    // "Win", "Loss", "Tie"
  finalScore    String    // "3-2"
  minutesPlayed Int

  // Universal stats
  goals         Int       @default(0)
  assists       Int       @default(0)

  // Goalkeeper stats (nullable)
  saves         Int?
  goalsAgainst  Int?
  cleanSheet    Boolean?

  // Verification
  verified      Boolean   @default(false)
  verifiedAt    DateTime?

  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  player Player @relation(fields: [playerId], references: [id], onDelete: Cascade)

  @@index([playerId])
  @@index([verified])
}
```

**Key Fields:**
- `verified`: Initially false, set to true after team verification
- `verifiedAt`: Timestamp when verified
- Goalkeeper-specific fields nullable (only used for goalkeepers)

**Indexes:**
- `playerId`: Fast lookup of player's games
- `verified`: Filter verified vs unverified games

#### Authentication Tokens

**EmailVerificationToken**
```prisma
model EmailVerificationToken {
  id        String   @id @default(cuid())
  token     String   @unique      // 64-char hex from crypto.randomBytes(32)
  userId    String
  expires   DateTime              // 24 hours from creation
  createdAt DateTime @default(now())

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([token])
  @@index([userId])
  @@index([expires])
}
```

**PasswordResetToken**
```prisma
model PasswordResetToken {
  id        String   @id @default(cuid())
  token     String   @unique      // 64-char hex from crypto.randomBytes(32)
  userId    String
  expires   DateTime              // 1 hour from creation
  createdAt DateTime @default(now())

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@index([token])
  @@index([userId])
  @@index([expires])
}
```

**Security Features:**
- One-time use (deleted after verification/reset)
- Short expiration (24h for email, 1h for password)
- Cryptographically secure tokens
- Cascade delete with user

---

## Authentication & Security

### NextAuth v5 Configuration

**Strategy:** JWT-based sessions (no database sessions)

**Location:** `/src/lib/auth.ts`

```typescript
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    CredentialsProvider({
      authorize: async (credentials) => {
        // 1. Find user by email
        const user = await prisma.user.findUnique({
          where: { email: credentials.email }
        });

        // 2. Validate password with bcrypt
        const isValid = await bcrypt.compare(
          credentials.password,
          user.password
        );

        // 3. Check email verification
        if (!user.emailVerified) {
          throw new Error("Please verify your email...");
        }

        return user;
      }
    })
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60  // 30 days
  }
});
```

**Flow:**
1. User submits credentials
2. Find user in database
3. Compare password with bcrypt
4. Check email verified
5. Generate JWT token
6. Set HTTP-only cookie

### Password Security

**Hashing Algorithm:** bcrypt with 10 rounds

```typescript
// Registration
const hashedPassword = await bcrypt.hash(password, 10);

// Login
const isValid = await bcrypt.compare(plainPassword, hashedPassword);
```

**Requirements:**
- Minimum 8 characters
- Stored as hash only (never plaintext)
- 10 rounds of bcrypt (per CLAUDE.md security standards)

### Token Generation

**Method:** Cryptographically secure random bytes

```typescript
import crypto from 'crypto';

function generateSecureToken(): string {
  return crypto.randomBytes(32).toString('hex');  // 64 chars
}
```

**Token Lifecycle:**
1. Generate on demand (email verify, password reset)
2. Store in database with expiration
3. Delete old tokens for user (one active token per type)
4. Validate on use (check expiration)
5. Delete after successful use

### Email Verification Enforcement

**Server-Side Protection:**

```typescript
// In layout.tsx (Server Component)
import { auth } from '@/lib/auth';
import { redirect } from 'next/navigation';

export default async function DashboardLayout({ children }) {
  const session = await auth();

  if (!session?.user) {
    redirect('/login');
  }

  return <div>{children}</div>;
}
```

**Login Enforcement:**

```typescript
// In NextAuth authorize()
if (!user.emailVerified) {
  throw new Error("Please verify your email before logging in...");
}
```

### Security Best Practices Implemented

✅ **No Email Enumeration**
```typescript
// Always return success, never reveal if email exists
if (!user) {
  return { success: true, message: "If account exists, email sent" };
}
```

✅ **CSRF Protection**
- NextAuth handles CSRF tokens automatically
- Double-submit cookie pattern

✅ **SQL Injection Prevention**
- Prisma parameterizes all queries
- No raw SQL used

✅ **XSS Prevention**
- React escapes all output by default
- CSP headers (configured in next.config.ts)

✅ **Secure Cookies**
- HTTP-only (no JavaScript access)
- Secure flag (HTTPS only in production)
- SameSite=Lax

---

## Infrastructure

### Current Architecture (Local Development)

```
┌─────────────────────────────────────┐
│         Local Machine               │
│                                     │
│  ┌──────────────┐  ┌─────────────┐ │
│  │  Next.js Dev │  │ PostgreSQL  │ │
│  │  Port 3003   │  │ Port 5432   │ │
│  │              │  │             │ │
│  │  (npm run    │  │ (Docker or  │ │
│  │   dev)       │  │  native)    │ │
│  └──────────────┘  └─────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

### Planned Production Architecture (Cloud Run)

```
┌────────────────────────────────────────────────────────┐
│                  Google Cloud Platform                  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Cloud Load Balancer                 │  │
│  │              (HTTPS Termination)                 │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       │                                 │
│  ┌────────────────────▼─────────────────────────────┐  │
│  │              Cloud Run Service                   │  │
│  │              "hustle"                            │  │
│  │                                                  │  │
│  │  ┌────────────────────────────────────────────┐ │  │
│  │  │   Next.js Container                       │ │  │
│  │  │   (Docker Image)                          │ │  │
│  │  │                                           │ │  │
│  │  │   - Min instances: 0                     │ │  │
│  │  │   - Max instances: 10                    │ │  │
│  │  │   - Memory: 512Mi                        │ │  │
│  │  │   - CPU: 1                               │ │  │
│  │  └────────────────────────────────────────────┘ │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       │                                 │
│                       │ VPC Connector                   │
│                       │                                 │
│  ┌────────────────────▼─────────────────────────────┐  │
│  │              Cloud SQL (PostgreSQL 15)          │  │
│  │                                                  │  │
│  │  - Instance: db-f1-micro                        │  │
│  │  - Storage: 10GB SSD                            │  │
│  │  - Backups: Daily, 7 days retention            │  │
│  │  - Private IP only                              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  External Services                       │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Resend API                          │  │
│  │              (Email Delivery)                    │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Terraform Resources

**Location:** `/home/jeremy/projects/hustle/06-Infrastructure/terraform/`

**Managed Resources:**

1. **Networking** (`network.tf`)
   - VPC network
   - Subnet
   - VPC connector for Cloud Run ↔ Cloud SQL

2. **Database** (`database.tf`)
   - Cloud SQL PostgreSQL instance
   - Database
   - User credentials
   - Backup configuration

3. **Compute** (`compute.tf`)
   - Cloud Run service
   - IAM bindings
   - Environment variables

4. **Storage** (`storage.tf`)
   - GCS buckets for static assets (if needed)

**State Management:**
- Local state file: `terraform.tfstate`
- Future: Migrate to GCS backend for team collaboration

---

## Third-Party Services

### Resend (Email Delivery)

**Purpose:** Send authentication and notification emails

**Integration:** `/src/lib/email.ts`

**API Key:** Stored in `.env.local` as `RESEND_API_KEY`

**Free Tier:**
- 3,000 emails/month
- 100 emails/day
- Perfect for MVP stage

**Emails Sent:**
1. Email verification (registration)
2. Welcome email (after verification)
3. Password reset
4. Password changed confirmation

**Dashboard:** https://resend.com/emails

**Monitoring:**
- Email delivery status
- Bounce/complaint rates
- Usage metrics

### Google Cloud Platform

**Services Used:**

| Service | Purpose | Cost Estimate |
|---------|---------|---------------|
| Cloud Run | App hosting | $5-20/month |
| Cloud SQL | PostgreSQL database | $10-30/month |
| VPC Connector | Cloud Run ↔ Cloud SQL | $8/month |
| Artifact Registry | Docker images | $0.10/GB |
| **Total** | | **~$25-60/month** |

**Project ID:** (To be set during deployment)

**Region:** us-central1 (Iowa)

### Future Integrations

**Planned:**
- Google Cloud Storage (player photos)
- Cloud CDN (static asset delivery)
- Cloud Monitoring (metrics and alerts)
- Error Reporting (error tracking)

---

## Performance Characteristics

### Current Metrics (Local Dev)

**Page Load Times:**
- Landing page: ~500ms
- Dashboard: ~800ms
- Login/Register: ~600ms

**API Response Times:**
- Registration: ~200ms (+ email send time)
- Login: ~150ms
- Player CRUD: ~50-100ms
- Game CRUD: ~50-100ms

**Database Queries:**
- User lookup: ~5ms
- Player list: ~10ms
- Game stats: ~15ms

### Expected Production Performance

**Cold Start:** ~2-3 seconds (first request after idle)
**Warm Request:** ~200-500ms
**Database Queries:** ~10-30ms (with Cloud SQL)

### Optimization Opportunities

1. **Implement caching**
   - Redis for session data
   - Cache player/game data

2. **Database indexing**
   - Already indexed: `playerId`, `verified`, `email`, `token`
   - Future: Add composite indexes for common queries

3. **Image optimization**
   - Next.js Image component (automatic)
   - Convert to WebP
   - Lazy loading

4. **Code splitting**
   - Already done by Next.js
   - Route-based splitting

---

## Scalability Considerations

### Current Limits

**Database:**
- PostgreSQL handles millions of rows
- Current schema optimized for <100k users

**Cloud Run:**
- Auto-scales to 10 instances (configurable)
- Each instance handles ~100 concurrent requests

**Expected Scale:**
- 0-1,000 users: Current architecture sufficient
- 1,000-10,000 users: May need caching layer
- 10,000+ users: Consider read replicas

### Bottlenecks to Watch

1. **Database connections**
   - Prisma connection pooling helps
   - Monitor connection count

2. **Email sending**
   - Resend free tier: 100/day
   - Upgrade plan if needed

3. **Cold starts**
   - Set min instances > 0 if cold starts become issue

---

**Document Maintenance:**
- Update when architecture changes
- Document new integrations
- Keep diagrams current

**Last Updated:** 2025-10-08
**Next Review:** 2026-01-08
