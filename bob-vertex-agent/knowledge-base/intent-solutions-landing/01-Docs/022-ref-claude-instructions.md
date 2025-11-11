# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Intent Solutions Landing Page** - Professional React/TypeScript landing page for Intent Solutions services, deployed on Netlify with custom domain `intentsolutions.io`.

## Technology Stack

- **Runtime**: Bun (fast JavaScript runtime and package manager)
- **Framework**: React 18 with TypeScript (strict mode)
- **Build Tool**: Vite with SWC (fast refresh, HMR on port 8080)
- **UI Library**: shadcn/ui (57 components) + Tailwind CSS
- **Routing**: React Router DOM
- **State Management**: TanStack Query (React Query)
- **Deployment**: Netlify (auto-deploy from GitHub main branch)
- **Domain**: intentsolutions.io (DNS via Porkbun)

## Development Commands

### Essential Commands
```bash
# Install dependencies (Bun required)
bun install

# Development server (http://localhost:8080)
bun run dev

# Production build
bun run build

# Preview production build locally
bun run preview

# Type checking
bun run type-check    # If configured

# Linting
bun run lint         # If configured
```

### Deployment
- **Auto-deploy**: Push to `main` branch triggers Netlify build
- **Manual deploy**: Via Netlify CLI or dashboard
- **Build command**: `bun install && bun run build` (configured in netlify.toml)
- **Output directory**: `dist/`

## Architecture

### Component Structure
```
src/
├── components/
│   ├── Navigation.tsx      # Sticky header navigation
│   ├── Hero.tsx           # Above-fold hero section
│   ├── About.tsx          # Company overview
│   ├── Platforms.tsx      # Service platforms showcase
│   ├── Market.tsx         # Market positioning
│   ├── Founder.tsx        # Founder section
│   ├── ExpertCTA.tsx      # Call-to-action
│   ├── Contact.tsx        # Contact form
│   ├── Footer.tsx         # Site footer
│   └── ui/                # shadcn/ui components (57 total)
├── pages/
│   ├── Index.tsx          # Landing page (main route)
│   └── NotFound.tsx       # 404 error page
├── hooks/
│   ├── use-mobile.tsx     # Mobile detection hook
│   └── use-toast.ts       # Toast notification hook
├── lib/
│   └── utils.ts           # Utility functions (cn, etc.)
└── assets/                # Images and static files
```

### Page Component Flow
```
App.tsx
 └── BrowserRouter
      ├── Route "/" → Index.tsx
      │    └── Renders sections in order:
      │        1. Navigation (sticky)
      │        2. Hero
      │        3. About
      │        4. Platforms
      │        5. ExpertCTA
      │        6. Market
      │        7. Founder
      │        8. Contact
      │        9. Footer
      └── Route "*" → NotFound.tsx
```

### Key Technical Details

**Vite Configuration** (`vite.config.ts`):
- Dev server on `::` (IPv6) port 8080
- Path alias: `@/` → `./src/`
- Lovable tagger plugin (development only)
- React SWC plugin for fast refresh

**Tailwind Configuration** (`tailwind.config.ts`):
- Dark mode support via `class` strategy
- Custom theme with CSS variables (HSL colors)
- Extended utilities: gradients, shadows, spacing
- Font family: Inter (primary sans-serif)
- Responsive breakpoints: sm, md, lg, xl, 2xl (max 1400px container)

**Routing & Redirects** (`netlify.toml`):
- HTTP → HTTPS redirect (301)
- www → non-www redirect (301)
- SPA fallback routing (all routes → /index.html with 200 status)
- Security headers: CSP, HSTS, X-Frame-Options, etc.

## Important Patterns

### Component Styling
- Use `cn()` utility from `@/lib/utils` for conditional classes
- Tailwind utility-first approach with custom theme variables
- Mobile-first responsive design

### State Management
- Local state: React `useState` for component-level state
- Server state: TanStack Query for API calls (if needed)
- No global state management (Zustand/Redux) currently needed

### Path Aliases
- `@/components` → `02-Src/components`
- `@/lib` → `02-Src/lib`
- `@/hooks` → `02-Src/hooks`
- `@/pages` → `02-Src/pages`

## Deployment Pipeline

### Netlify Auto-Deploy Flow
1. Push to GitHub `main` branch
2. Netlify webhook triggers build
3. Runs: `bun install && bun run build`
4. Deploys `dist/` to Netlify CDN
5. Site live at https://intentsolutions.io

### Performance Targets
- Lighthouse Score: 95+
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3.5s
- Cumulative Layout Shift: < 0.1

## Security

### Implemented Security (netlify.toml)
- Content Security Policy (CSP) headers
- HTTP Strict Transport Security (HSTS)
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Permissions-Policy for geolocation/camera/microphone

## Documentation Files

Comprehensive documentation in project root (numeric prefixes for organization):
- `00-CLAUDE.md` - Previous AI context (now superseded by this file)
- `01-README.md` - General project overview
- `02-NETLIFY-DEPLOYMENT-GUIDE.md` - Deployment instructions
- `03-LICENSE.md` - License information
- `05-CONTRIBUTING.md` - Contribution guidelines
- `06-CHANGELOG.md` - Version history
- `07-ARCHITECTURE.md` - Detailed architecture documentation
- `08-COMPONENT-API.md` - Component API reference
- `09-TROUBLESHOOTING.md` - Common issues and solutions
- `10-SECURITY.md` - Security practices

### Claude-Generated Documentation
All AI-generated audits, reports, and analysis documents are in 01-Docs:
- `01-Docs/audits/` - System audits and assessments (7 files)
- `01-Docs/reports/` - Transformation and release reports (6 files)
- `01-Docs/analysis/` - DevOps and system analysis (2 files)
- `01-Docs/plans/`, `tasks/`, `logs/`, `misc/` - Future use

## Critical Notes

### Bun Runtime Required
- This project uses **Bun**, not npm/yarn/pnpm
- Commands like `npm install` will fail
- Always use `bun` commands: `bun install`, `bun run dev`, etc.

### Custom Domain Configuration
- Primary domain: intentsolutions.io
- DNS provider: Porkbun
- Netlify handles SSL/TLS certificates (Let's Encrypt)
- All HTTP traffic redirects to HTTPS
- www subdomain redirects to non-www

### Adding New Routes
- Add routes in `App.tsx` **ABOVE** the catch-all `*` route
- Update Netlify redirects if needed (already configured for SPA)
- 404 page handled by `NotFound.tsx`

### Adding shadcn/ui Components
- Components already installed in `src/components/ui/`
- 57 components available
- Use import: `import { Button } from "@/components/ui/button"`
- Customize via Tailwind config or component files

## Common Development Tasks

### Adding a New Section to Landing Page
1. Create component in `src/components/[SectionName].tsx`
2. Import in `src/pages/Index.tsx`
3. Add to component hierarchy in appropriate order
4. Style with Tailwind using existing theme variables

### Modifying Styles
1. Global styles: `src/index.css` (CSS variables)
2. Component styles: Tailwind classes in component files
3. Theme customization: `tailwind.config.ts`
4. Use existing design tokens (colors, spacing, shadows)

### Testing Changes Locally
1. Run `bun run dev`
2. Open http://localhost:8080
3. Make changes (hot module reload enabled)
4. Test responsive breakpoints (mobile, tablet, desktop)

### Deploying Changes
1. Commit changes to feature branch
2. Test locally: `bun run build && bun run preview`
3. Merge to `main` branch
4. Netlify auto-deploys (watch build logs in dashboard)
5. Verify at https://intentsolutions.io

## Browser Support

- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile: iOS Safari, Chrome Android
- No IE11 support (modern ES6+ only)

---

**Last Updated**: October 4, 2025
**Status**: ✅ Production deployment active at intentsolutions.io
