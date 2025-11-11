# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## DiagnosticPro AI Platform v2.0.0

✅ **PRODUCTION RELEASE COMPLETE** - DiagnosticPro AI diagnostic platform with proprietary 15-section analysis framework and production-grade PDF generation

A professional equipment diagnostic platform leveraging proprietary AI analysis to provide comprehensive diagnostic reports for vehicles, machinery, and equipment. Customers submit diagnostic forms, make $4.99 payments via Stripe, and receive detailed 2000+ word PDF reports with conversation coaching and shop interrogation strategies.

⚠️ **RECENT ROLLBACK (2025-10-14)**: Photo upload system (~5,000 lines) developed but rolled back due to undefined payment flow. All code preserved on branch `feature/photo-upload-identity-system`. Infrastructure deployed (GCS, Pub/Sub, BigQuery) but unused ($0 cost). Production fully operational. See `01-docs/067-log-photo-upload-rollback.md` for complete details.

## Current Production Stack (LIVE v1.0.0)

### **Frontend**
- Hosting: Firebase Hosting (`diagnosticpro.io`)
- Framework: React 18 + TypeScript + Vite
- UI: shadcn/ui + Tailwind CSS
- Status: ✅ PRODUCTION READY

### **Backend**
- Platform: Google Cloud Run (`diagnosticpro-vertex-ai-backend`)
- Database: Firestore (3 collections: diagnosticSubmissions, orders, emailLogs)
- AI: Vertex AI Gemini 2.5 Flash with proprietary 14-section framework
- Payment: Stripe with webhook integration ($4.99 per diagnostic)
- Storage: Cloud Storage with signed URL access
- Status: ✅ FULLY OPERATIONAL

### **Architecture**
- **GCP Project**: `diagnostic-pro-prod`
- **Domain**: `diagnosticpro.io` (primary production domain)
- **Backend**: Cloud Run (us-central1)
- **AI Engine**: Vertex AI Gemini 2.5 Flash

## Core Workflow (Production v1.0.0)
1. Customer submits diagnostic form → **Firestore** (`diagnosticSubmissions` collection)
2. Payment processed via Stripe ($4.99) → **Firestore** (`orders` collection)
3. Webhook triggers proprietary 14-section AI analysis → **Vertex AI Gemini 2.5 Flash**
4. Comprehensive 2000+ word PDF report generated → **Cloud Storage** with signed URLs
5. Customer downloads report with conversation coaching and shop interrogation strategies

## Proprietary AI Framework (v2.0)
### 15-Section Diagnostic Analysis:
🎯 1. **PRIMARY DIAGNOSIS** - Root cause with confidence percentage
🔍 2. **DIFFERENTIAL DIAGNOSIS** - Alternative causes ranked by likelihood
✅ 3. **DIAGNOSTIC VERIFICATION** - Exact tests shops must perform
❓ 4. **SHOP INTERROGATION** - 5 technical questions to expose incompetence
🗣️ 5. **CONVERSATION SCRIPTING** - Word-for-word customer coaching
💸 6. **COST BREAKDOWN** - Fair pricing vs overcharge identification
🚩 7. **RIPOFF DETECTION** - Scam identification and protection
⚖️ 8. **AUTHORIZATION GUIDE** - Approve/reject/second opinion recommendations
🔧 9. **TECHNICAL EDUCATION** - System operation and failure mechanisms
📦 10. **OEM PARTS STRATEGY** - Specific part numbers and sourcing
💬 11. **NEGOTIATION TACTICS** - Professional negotiation strategies
🔬 12. **LIKELY CAUSES** - Ranked confidence percentages
📊 13. **RECOMMENDATIONS** - Immediate actions and maintenance
🔗 14. **SOURCE VERIFICATION** - Authoritative links and TSB references
🔬 15. **ROOT CAUSE ANALYSIS** - Critical diagnostic component (v2.0 addition)

## Commands

### Development
```bash
# Start development server
npm run dev
make dev

# Install dependencies and hooks
npm install
make install

# Run all safety checks (REQUIRED before commits)
make safe-commit
```

### Testing & Quality
```bash
# Run tests
npm test
npm run test:watch
npm run test:coverage

# Type checking
npx tsc --noEmit

# Linting
npm run lint

# Formatting
npx prettier --write "src/**/*.{ts,tsx,js,jsx,json,css,md}"
npx prettier --check "src/**/*.{ts,tsx,js,jsx,json,css,md}"

# All checks at once
make full-check
```

### Build & Deploy
```bash
# Production build
npm run build

# Development build
npm run build:dev

# Preview production build
npm run preview
```

### Firebase/Google Cloud Commands
```bash
# Firebase deployment (PRODUCTION)
firebase deploy --only hosting              # Deploy React app
firebase deploy --only functions           # Deploy Cloud Functions
firebase deploy --only firestore          # Deploy database rules
firebase deploy                           # Deploy everything

# Development & Testing
npm run dev                               # Local development
npm run build                            # Production build
npm run preview                          # Test production build

# Firestore operations
firebase firestore:indexes               # Deploy database indexes
firebase emulators:start                # Start local emulators

# Cloud Functions logs & monitoring
firebase functions:log                   # View function logs
gcloud functions logs read --limit 50   # Alternative log viewing

# Vertex AI monitoring
gcloud ai endpoints list                 # List AI endpoints
```

### Environment Configuration
```bash
# Firebase Configuration (Production - LIVE)
VITE_FIREBASE_PROJECT_ID="diagnostic-pro-prod"
VITE_FIREBASE_API_KEY="AIzaSyBmuntVKosh_EGz5yxQLlIoNXlxwYE6tMg"
VITE_FIREBASE_AUTH_DOMAIN="diagnostic-pro-prod.firebaseapp.com"
VITE_FIREBASE_STORAGE_BUCKET="diagnostic-pro-prod.firebasestorage.app"

# API Configuration (Currently disabled until Cloud Functions deploy)
VITE_API_BASE=""
VITE_DISABLE_API="true"
```

### Git Workflow (ENFORCED)
```bash
# Create feature branch
git checkout -b feature/name
make create-branch

# Before ANY commit
make safe-commit

# NEVER commit directly to main
# NEVER use --no-verify flag
```

## PDF Generation Architecture (v2.0)

### Production-Grade PDF System
The PDF generation has been completely rebuilt with:

1. **PDFValidationSystem Class**
   - Validates all 15 sections are present
   - Checks for Root Cause Analysis
   - Detects and removes excessive whitespace
   - Provides detailed error/warning reporting

2. **TypographyManager Class**
   - Professional bullet point rendering with hanging indents
   - Orphan/widow control (no stranded lines)
   - Controlled pagination (no auto-page sprawl)
   - IBM Plex Mono font support

3. **DiagnosticPDFGenerator Class**
   - Controlled page creation with `autoFirstPage: false`
   - Section validation before rendering
   - Default content for missing sections
   - Professional cover page and disclaimer

4. **Key Technical Fixes**
   - All text() calls use `continued: false` to prevent auto-pagination
   - Page breaks are manually controlled
   - Content is cleaned before rendering
   - 2:1 page ratio bug eliminated

### Files
- `reportPdfProduction.js` - Production PDF generator (501 lines)
- `reportPdf.js` - Legacy generator (deprecated)
- `fonts/` - IBM Plex Mono TTF files

## Architecture

### Directory Structure
```
fix-it-detective-ai/
├── src/
│   ├── components/           # React components (shadcn/ui)
│   │   ├── ui/              # Base UI components
│   │   └── __tests__/       # Component tests
│   ├── pages/               # Route components
│   ├── config/              # Configuration files
│   │   └── email.config.ts  # Email service configuration
│   ├── utils/               # Utility functions
│   │   └── emailService.ts  # Nodemailer implementation
│   ├── integrations/        # External service integrations
│   │   └── supabase/        # Database client & types
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Shared utilities
│   └── data/                # Static data (manufacturers)
├── supabase/
│   ├── functions/           # Edge Functions (Deno)
│   │   ├── analyze-diagnostic/     # GPT-4 analysis engine
│   │   ├── send-diagnostic-email/  # Email delivery
│   │   ├── generate-report-pdf/    # PDF generation
│   │   ├── stripe-webhook/         # Payment processing
│   │   ├── manual-send-email/      # Manual email trigger
│   │   ├── test-email/            # Email testing
│   │   └── send-slack-notification/ # System alerts
│   ├── migrations/          # Database schema
│   └── config.toml          # Supabase configuration
├── public/                  # Static assets
└── dist/                    # Build output
```

### Tech Stack
- **Frontend**: React 18 + TypeScript + Vite
- **UI**: shadcn/ui + Radix UI + Tailwind CSS
- **Backend**: Supabase (PostgreSQL + Edge Functions)
- **AI**: OpenAI GPT-4 API
- **Payments**: Stripe
- **Email**: Nodemailer (Gmail SMTP)
- **Testing**: Jest + React Testing Library
- **Deployment**: Lovable/Vercel

### Key Integrations
- **Supabase Project**: jjxvrxehmawuyxltrvql
- **Database**: PostgreSQL with Row Level Security
- **Edge Functions**: 8 functions for core business logic
- **Stripe**: Payment processing and webhooks
- **OpenAI**: GPT-4 for diagnostic analysis
- **Gmail SMTP**: Email delivery service

## Environment Variables

### Required for Development
```bash
# Supabase
VITE_SUPABASE_URL=https://jjxvrxehmawuyxltrvql.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-key

# OpenAI
OPENAI_API_KEY=your-openai-key

# Stripe
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# Email (Gmail SMTP)
GMAIL_APP_PASSWORD=your-app-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

## AI Analysis System

### GPT-4 Prompt Structure
The analyze-diagnostic function uses a comprehensive 12-section format:
1. Initial Assessment
2. Diagnostic Tests (with specific values: PSI, voltage, resistance)
3. Test Results Analysis
4. Component-Specific Checks
5. Root Cause Analysis
6. Repair Recommendations
7. Priority & Safety Assessment
8. Cost Estimates ($29.99 tier analysis)
9. Preventive Maintenance
10. Technical Specifications
11. Parts & Tools Required
12. Professional vs DIY Assessment

### Supported Equipment Types
- Vehicles (cars, trucks, motorcycles)
- Machinery (construction, agricultural)
- Industrial equipment
- Electronics and appliances

## Database Schema (Migration Status)

### Current Supabase Tables (Being Migrated)
- `diagnostic_submissions`: Customer form data (25+ fields)
- `orders`: Payment and processing status  
- `email_logs`: Email delivery tracking

### Target Firestore Collections (Friday Migration)
- `diagnosticSubmissions`: Customer form data (snake_case → camelCase)
- `orders`: Payment tracking with Stripe integration
- `emailLogs`: Email delivery tracking and status

### Migration Notes
- **No data migration needed** - Supabase contains only test data
- **Field conversions**: analysis_status → analysisStatus, created_at → createdAt
- **Anonymous submissions**: userId can be null in diagnosticSubmissions
- **Document references**: orderId ↔ submissionId relationships

### Security (Post-Migration)
- Firestore security rules (replacing Supabase RLS)
- Firebase Auth service account access
- Customer PII protection maintained
- Google Cloud IAM management

## Development Guidelines

### Git Workflow Rules (ENFORCED)
1. **NEVER** commit directly to main branch
2. **ALWAYS** create feature branches
3. **MUST** run `make safe-commit` before any commit
4. Pre-commit hooks prevent direct main commits
5. All checks must pass: lint, type-check, format, tests

### Code Quality Standards
- TypeScript strict mode enabled
- No `any` types without justification
- Jest tests for critical functionality
- Prettier formatting enforced
- ESLint rules strictly followed
- Component tests using React Testing Library

### Critical Safety Checks
The Makefile enforces these checks before any commit:
- ESLint (code quality)
- TypeScript (type safety)
- Prettier (formatting)
- Jest (tests)

## Testing Strategy

### Test Files Location
- Component tests: `src/components/__tests__/`
- Utility tests: `src/utils/__tests__/`
- Setup: `src/setupTests.ts`

### Current Test Coverage
- Button component tests
- DiagnosticForm component tests
- Hero component tests
- Validation utility tests

### Test Commands
```bash
# Run all tests
npm test

# Watch mode for development
npm run test:watch

# Coverage report
npm run test:coverage

# Run single test file
npm test Button.test.tsx
```

## Email Service

### Implementation
- Located in: `src/utils/emailService.ts`
- Uses Nodemailer with Gmail SMTP
- Configuration in: `src/config/email.config.ts`
- Sends from: reports@diagnosticpro.io

### Email Flow
1. Customer completes payment
2. Stripe webhook triggers analysis
3. analyze-diagnostic generates report
4. send-diagnostic-email delivers PDF report
5. Email logged to email_logs table

## Migration Status - COMPLETED ✅

### Migration Results (September 23, 2025)
1. **✅ Frontend Migration**: Successfully deployed to Firebase Hosting
   - React app now hosted on Firebase (`diagnosticpro.io`)
   - All static assets and routing working correctly

2. **✅ Database Migration**: Firestore fully integrated
   - Created comprehensive Firestore service layer
   - Migrated all 3 collection schemas (diagnosticSubmissions, orders, emailLogs)
   - Updated all API services to use Firestore directly

3. **✅ Configuration Migration**: Firebase environment setup
   - All environment variables configured for Firebase
   - Firestore rules deployed and active
   - Authentication and storage initialized

4. **🔧 Cloud Functions**: Pending deployment resolution
   - Functions built successfully locally
   - Deployment blocked by Cloud Build issues (unrelated to code)
   - Temporary workaround: API disabled until functions deploy
   - All function code ready for deployment

### Migration Benefits Achieved
1. **Performance**: Direct Firestore integration eliminates API latency
2. **Scalability**: Firebase autoscaling handles traffic spikes
3. **Integration**: Native Google Cloud integration for Vertex AI
4. **Cost**: More predictable pricing model
5. **Reliability**: Google Cloud SLA and uptime guarantees

### Current Status
- **Frontend**: 100% migrated and deployed ✅
- **Database**: 100% migrated to Firestore ✅
- **API Layer**: 100% updated for Firebase ✅
- **Cloud Functions**: Code ready, deployment pending 🔧
- **DNS**: diagnosticpro.io pointing to Firebase ✅

### Next Steps
1. Resolve Cloud Functions deployment (infrastructure issue)
2. Enable API integration once functions are deployed
3. Test complete end-to-end workflow
4. Monitor and optimize performance

## Performance Targets
- End-to-end Success Rate: >95%
- Email Delivery Rate: >98%
- Response Time: <10 minutes
- Customer Satisfaction: >4.5/5

## Debugging & Monitoring

### Log Access (Post-Migration)
```bash
# Google Cloud Function logs
gcloud functions logs read analyze-diagnostic --limit 50

# Firestore operations
firebase firestore:indexes

# BigQuery analytics
bq query --use_legacy_sql=false "SELECT * FROM diagnostic_reports LIMIT 10"

# Email delivery status  
# Check emailLogs Firestore collection
```

### Legacy Log Access (Until Friday)
```bash
# ⚠️ Supabase functions (being shut down)
supabase functions logs analyze-diagnostic --follow
```

### Migration Considerations
- Cloud Function timeout: 540s (vs Supabase 10min limit)
- Vertex AI API rate limits (replacing OpenAI)
- Firestore security rules (replacing Supabase RLS)
- BigQuery integration for AI report analytics

## Project Context

This is part of the DiagnosticPro platform ecosystem with related projects:
- `schema/`: BigQuery schemas (266 tables)
- `scraper/`: Data collection systems
- `rss_feeds/`: Content curation (226 feeds)

The fix-it-detective-ai project serves as the customer-facing diagnostic service, integrating with the broader platform's data and analytics infrastructure.