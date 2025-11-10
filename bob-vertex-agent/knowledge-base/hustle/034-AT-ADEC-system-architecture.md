# Architecture

How Hustle is built and why we made these decisions.

**Version:** v00.00.00
**Last Updated:** 2025-10-05

---

## 🎯 Overview

Hustle is a Next.js application deployed as a containerized service on Google Cloud Run, backed by Cloud SQL PostgreSQL. We prioritize simplicity, security, and scalability.

```
┌─────────────────────────────────────────┐
│          Users (Parents)                │
└────────────────┬────────────────────────┘
                 │
                 │ HTTPS
                 ▼
┌─────────────────────────────────────────┐
│     Google Cloud Run (Containers)       │
│  ┌────────────────────────────────────┐ │
│  │       Next.js 15.5.4 App           │ │
│  │  ┌──────────────┐  ┌─────────────┐│ │
│  │  │  React UI    │  │  API Routes ││ │
│  │  │ (shadcn/ui)  │  │  (NextAuth) ││ │
│  │  └──────────────┘  └─────────────┘│ │
│  └────────────────────────────────────┘ │
└──────────────────┬──────────────────────┘
                   │
                   │ VPC Connector
                   ▼
       ┌───────────────────────────┐
       │   Cloud SQL PostgreSQL    │
       │      (Prisma ORM)         │
       └───────────────────────────┘
```

---

## 🏗️ Architecture Decisions

### ADR-001: Next.js with App Router

**Decision:** Use Next.js 15.5.4 with App Router (not Pages Router)

**Rationale:**
- Server Components by default (better performance)
- Simplified routing with file-based conventions
- Built-in API routes (no separate backend needed)
- Turbopack for faster development builds
- Future-proof (App Router is the future of Next.js)

**Trade-offs:**
- Steeper learning curve vs Pages Router
- Some third-party libraries not optimized yet
- More complex mental model for rendering

**Status:** ✅ Implemented

---

### ADR-002: NextAuth v5 for Authentication

**Decision:** Use NextAuth v5 with JWT strategy (migrated from SuperTokens)

**Rationale:**
- Industry-standard authentication library
- JWT strategy simplifies deployment (no session database needed)
- Extensive provider support for future OAuth
- Server-side session validation via `await auth()`
- Seamless Next.js App Router integration

**Trade-offs:**
- JWT sessions can't be invalidated instantly
- Requires proper secret management
- More complex than simple cookie-based auth

**Previous Approach:** SuperTokens (too complex for our needs)

**Status:** ✅ Implemented (complete security audit passed)

---

### ADR-003: PostgreSQL with Prisma ORM

**Decision:** PostgreSQL 15 via Cloud SQL, accessed through Prisma ORM

**Rationale:**
- PostgreSQL: Robust, ACID-compliant, excellent for relational data
- Cloud SQL: Managed service, automatic backups, scalable
- Prisma: Type-safe queries, excellent TypeScript support, easy migrations
- Better than NoSQL for our structured data (players, games, verification)

**Trade-offs:**
- More expensive than serverless databases (Firestore, DynamoDB)
- Prisma adds some query overhead
- Requires VPC connector for Cloud Run access

**Status:** ✅ Implemented

---

### ADR-004: Google Cloud Run for Deployment

**Decision:** Deploy as Docker containers on Cloud Run (not App Engine, not VMs)

**Rationale:**
- Serverless: Pay only when traffic hits
- Containerized: Consistent across environments
- Auto-scaling: Handles traffic spikes automatically
- Easy rollbacks: Simple to revert to previous versions
- Cost-effective: Minimal cost at low usage

**Trade-offs:**
- Cold starts (mitigated by min instances if needed)
- Requires Docker knowledge
- VPC connector needed for database access

**Status:** ✅ Implemented

---

### ADR-005: Kiranism Dashboard Starter

**Decision:** Use Kiranism next-shadcn-dashboard-starter for UI framework

**Rationale:**
- Professional dashboard components out-of-box
- Built on shadcn/ui (Radix UI primitives)
- Tailwind CSS for styling
- Responsive sidebar navigation
- Dark mode support ready
- Saves weeks of custom UI development

**Trade-offs:**
- Opinionated component structure
- Some components we don't need (but can ignore)
- Dependency on external starter template

**Previous Approach:** Custom UI from scratch (too time-consuming)

**Status:** ✅ Implemented

---

### ADR-006: Terraform for Infrastructure as Code

**Decision:** Manage all GCP infrastructure via Terraform

**Rationale:**
- Version-controlled infrastructure
- Reproducible deployments
- Easy to spin up dev/staging/prod environments
- Clear dependency management
- Disaster recovery simplified

**Trade-offs:**
- Requires Terraform knowledge
- State file management complexity
- Can't use GCP console for infrastructure changes

**Status:** ✅ Implemented

---

## 📐 System Components

### Frontend Architecture

**Location:** `src/app/` and `src/components/`

```
src/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Auth routes group
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/         # Protected dashboard
│   │   ├── layout.tsx     # Session-protected layout
│   │   ├── page.tsx       # Dashboard home
│   │   └── add-athlete/   # Athlete creation
│   ├── api/               # API routes
│   └── page.tsx           # Landing page
│
├── components/
│   ├── ui/                # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── skeleton.tsx
│   └── layout/            # Kiranism layout components
│       ├── app-sidebar-simple.tsx
│       ├── user-nav.tsx
│       └── header.tsx
│
├── lib/
│   ├── auth.ts            # NextAuth configuration
│   ├── prisma.ts          # Prisma client singleton
│   └── utils.ts           # Utility functions
│
└── hooks/
    └── use-mobile.tsx     # Mobile detection hook
```

**Key Patterns:**
- Server Components by default
- Client Components only when needed (`'use client'`)
- Path aliases via `@/*` for clean imports
- Collocated route handlers in `api/` directories

---

### Backend Architecture

**Location:** `src/app/api/` and `src/lib/`

```
api/
├── auth/
│   ├── [...nextauth]/route.ts  # NextAuth handler
│   └── register/route.ts       # User registration
│
├── players/
│   ├── route.ts                # GET all players (filtered)
│   ├── create/route.ts         # POST create player
│   └── upload-photo/route.ts   # POST upload photo
│
├── games/route.ts              # GET/POST games
├── verify/route.ts             # POST verify game
└── healthcheck/route.ts        # GET health status
```

**Authentication Pattern (Every Protected Route):**

```typescript
import { auth } from '@/lib/auth';
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // 1. Authenticate
  const session = await auth();
  if (!session?.user?.id) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // 2. Authorize (verify ownership)
  const resource = await prisma.resource.findUnique({
    where: { id: resourceId },
    select: { parentId: true }
  });

  if (resource.parentId !== session.user.id) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }

  // 3. Execute business logic
  // ...
}
```

**Key Principles:**
- Never trust client-provided user IDs
- Always get user ID from session
- Verify ownership before operations
- Return 401 (Unauthorized) vs 403 (Forbidden) appropriately

---

### Database Architecture

**Schema:** `prisma/schema.prisma`

```prisma
model User {
  id            String    @id @default(cuid())
  firstName     String
  lastName      String
  email         String    @unique
  emailVerified DateTime?
  phone         String?
  password      String    // bcrypt hashed
  players       Player[]
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Player {
  id        String   @id @default(cuid())
  name      String
  birthday  DateTime
  position  String
  teamClub  String
  photoUrl  String?
  parentId  String
  parent    User     @relation(fields: [parentId], references: [id], onDelete: Cascade)
  games     Game[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([parentId])
}

model Game {
  id            String    @id @default(cuid())
  playerId      String
  player        Player    @relation(fields: [playerId], references: [id], onDelete: Cascade)
  date          DateTime
  opponent      String
  result        String    // Win/Loss/Tie
  finalScore    String
  minutesPlayed Int
  goals         Int       @default(0)
  assists       Int       @default(0)
  saves         Int?      // Goalkeeper only
  goalsAgainst  Int?      // Goalkeeper only
  cleanSheet    Boolean?  // Goalkeeper only
  verified      Boolean   @default(false)
  verifiedAt    DateTime?
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  @@index([playerId])
  @@index([verified])
}

// NextAuth models (Account, Session, VerificationToken)
```

**Design Decisions:**
- CUIDs for primary keys (not auto-increment integers)
- Cascade deletes (delete user → delete their players → delete their games)
- Indexes on foreign keys and frequently queried fields
- Nullable fields for goalkeeper-specific stats
- Timestamps on all entities

---

### Infrastructure Architecture

**Location:** `06-Infrastructure/terraform/`

```
GCP Architecture:
┌─────────────────────────────────────────┐
│         Google Cloud Project            │
│  ┌──────────────────────────────────┐  │
│  │    Cloud Run Service             │  │
│  │  - Region: us-central1           │  │
│  │  - Auto-scaling: 0-10 instances  │  │
│  │  - CPU: 1 core                   │  │
│  │  - Memory: 512MB                 │  │
│  │  - Timeout: 300s                 │  │
│  └──────────────┬───────────────────┘  │
│                 │                       │
│                 │ VPC Connector         │
│                 ▼                       │
│  ┌──────────────────────────────────┐  │
│  │  Cloud SQL PostgreSQL            │  │
│  │  - Version: 15                   │  │
│  │  - Tier: db-f1-micro (dev)       │  │
│  │  - Private IP: 10.240.0.3        │  │
│  │  - Backups: Daily                │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Artifact Registry               │  │
│  │  - Docker images                 │  │
│  │  - Multi-region replication      │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Key Resources:**
- Cloud Run service (hustle-app)
- Cloud SQL instance (hustle-db)
- VPC network (hustle-vpc)
- VPC connector (hustle-vpc-connector)
- Service accounts with least-privilege IAM
- Artifact Registry for Docker images

---

## 🔒 Security Architecture

### Authentication Flow

```
1. User enters email/password
   ↓
2. POST /api/auth/register (if new user)
   - Validate input
   - Hash password (bcrypt, 10 rounds)
   - Store in database
   ↓
3. User logs in at /login
   ↓
4. NextAuth credentials provider validates
   - Fetch user from database
   - Compare bcrypt hashes
   ↓
5. Create JWT session (30-day expiry)
   - User ID, email, name in token
   - Signed with NEXTAUTH_SECRET
   ↓
6. Session cookie set (HttpOnly, Secure)
   ↓
7. Dashboard layout calls await auth()
   - Verifies JWT signature
   - Checks expiry
   - Extracts user data
   ↓
8. If valid → render dashboard
   If invalid → redirect to /login
```

### API Security Pattern

```
Every protected API route:

1. const session = await auth()
2. if (!session) → 401 Unauthorized
3. Fetch resource from database
4. if (resource.userId !== session.user.id) → 403 Forbidden
5. Execute operation
6. Return success
```

**Security Principles:**
- Never trust client input
- Always validate and sanitize
- Use parameterized queries (Prisma)
- Hash passwords (bcrypt, 10 rounds)
- Server-side session validation
- Least-privilege database user
- HTTPS only in production

---

## 📊 Data Flow

### Creating a Player

```
1. Parent navigates to /dashboard/add-athlete
2. Fills out form (name, birthday, position, team)
3. Clicks "Create Athlete"
   ↓
4. Client: POST /api/players/create
   Body: { name, birthday, position, teamClub }
   ↓
5. API Route:
   - await auth() → get session.user.id
   - Validate all fields
   - prisma.player.create({ ...data, parentId: session.user.id })
   ↓
6. Database: INSERT INTO players
   ↓
7. Return: { success: true, player }
   ↓
8. Client: Redirect to /dashboard
   ↓
9. Dashboard: GET /api/players (filtered by session.user.id)
   ↓
10. Display: Player card shows in UI
```

### Logging a Game

```
1. Parent clicks on player
2. Navigates to game logging form
3. Enters: date, opponent, result, score, stats
   ↓
4. Client: POST /api/games
   Body: { playerId, date, opponent, ...stats }
   ↓
5. API Route:
   - await auth() → get session.user.id
   - Fetch player: prisma.player.findUnique({ where: { id: playerId }})
   - Verify: player.parentId === session.user.id
   - prisma.game.create({ ...data, verified: false })
   ↓
6. Database: INSERT INTO games (verified = false)
   ↓
7. Return: { success: true, game }
   ↓
8. Client: Show success message
```

### Verifying a Game

```
1. Parent sees unverified game in list
2. Clicks "Verify"
   ↓
3. Client: POST /api/verify
   Body: { gameId }
   ↓
4. API Route:
   - await auth() → get session.user.id
   - Fetch game with player: prisma.game.findUnique({ include: { player: true }})
   - Verify: game.player.parentId === session.user.id
   - Update: prisma.game.update({ verified: true, verifiedAt: now })
   ↓
5. Database: UPDATE games SET verified = true, verifiedAt = NOW()
   ↓
6. Return: { success: true }
   ↓
7. Client: Update UI (verified badge appears)
```

---

## 🚀 Deployment Architecture

### Build Process

```
1. Developer: git push origin main
   ↓
2. GitHub: Trigger (future CI/CD)
   ↓
3. Build Docker image:
   - Stage 1: Install dependencies (node_modules)
   - Stage 2: Build Next.js app (npm run build)
   - Stage 3: Create production image (standalone output)
   ↓
4. Push to Artifact Registry:
   - Tag: us-central1-docker.pkg.dev/.../hustle-app:latest
   ↓
5. Deploy to Cloud Run:
   - Pull latest image
   - Update service
   - Roll out new containers
   - Zero-downtime deployment
   ↓
6. Health check: GET /api/healthcheck
   ↓
7. If healthy → traffic switches to new version
   If unhealthy → rollback to previous
```

### Environment Variables

**Development (`.env.local`):**
```
DATABASE_URL=postgresql://localhost:5432/hustle_mvp
NEXTAUTH_SECRET=dev-secret
NEXTAUTH_URL=http://localhost:4000
NODE_ENV=development
```

**Production (Cloud Run):**
```
DATABASE_URL=postgresql://10.240.0.3:5432/hustle_mvp (via VPC)
NEXTAUTH_SECRET=<strong-production-secret>
NEXTAUTH_URL=https://hustle-app-....run.app
NODE_ENV=production
```

---

## 📈 Scalability Considerations

### Current State (v00.00.00)
- Single Cloud Run service
- Single Cloud SQL instance
- No caching layer
- No CDN
- Auto-scales 0-10 instances

**Suitable for:** 100-1,000 active users

### Future Improvements

**For 1,000-10,000 users:**
- Add Redis cache (Memorystore)
- Implement CDN for static assets (Cloud CDN)
- Database read replicas
- Connection pooling (PgBouncer)

**For 10,000+ users:**
- Multi-region deployment
- Horizontal database sharding (by user ID)
- Background job processing (Cloud Tasks)
- Advanced monitoring (Cloud Monitoring/Prometheus)

---

## 🔍 Monitoring & Observability

### Current Monitoring

**Cloud Run Metrics:**
- Request count
- Request latency (p50, p95, p99)
- Error rate
- Instance count
- CPU/Memory utilization

**Cloud SQL Metrics:**
- Connection count
- Query latency
- Storage usage
- Replication lag

**Logs:**
- Cloud Logging (stdout/stderr from containers)
- NextAuth debug logs (development only)
- API error logs

### Future Improvements

- Error tracking (Sentry)
- Performance monitoring (New Relic/DataDog)
- User analytics (PostHog)
- Custom dashboards (Grafana)
- Alerting (PagerDuty)

---

## 🛠️ Development Workflow

### Local Development

```
1. Clone repository
2. npm install
3. Copy .env.example → .env.local
4. npx prisma db push (sync local database)
5. npm run dev -- -p 4000
6. Visit http://localhost:4000
```

**Database:** Local PostgreSQL or Docker container

### Testing Changes

```
1. Make code changes
2. npm run lint (check code quality)
3. npm run build (verify builds)
4. Manual testing in browser
5. Check console for errors
```

### Deployment

```
1. Commit changes to main branch
2. Build Docker image locally (or CI/CD)
3. Push to Artifact Registry
4. Update Cloud Run service via Terraform or gcloud
5. Verify /api/healthcheck
```

---

## 📚 Architecture Resources

### References

- [Next.js App Router Docs](https://nextjs.org/docs/app)
- [NextAuth.js v5 Docs](https://authjs.dev)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Terraform GCP Provider](https://registry.terraform.io/providers/hashicorp/google/latest/docs)

### Related Documentation

- `01-Docs/015-adr-nextauth-migration.md` - NextAuth decision record
- `01-Docs/028-aar-complete-nextauth-security-fix.md` - Security audit
- `CLAUDE.md` - Codebase guide for AI assistants
- `README.md` - Project overview

---

**This architecture prioritizes simplicity, security, and scalability. We build for today's needs while preparing for tomorrow's growth.**

---

**Last Updated:** 2025-10-05
**Next Review:** After v00.00.05
