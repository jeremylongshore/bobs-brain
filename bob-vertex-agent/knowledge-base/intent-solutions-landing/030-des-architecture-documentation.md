# Architecture

This document describes the technical architecture of the Intent Solutions landing page.

## Technology Stack

### Frontend
- **React 18** - UI library with hooks and functional components
- **TypeScript** - Type-safe JavaScript with strict mode enabled
- **Vite** - Lightning-fast build tool with HMR
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - High-quality React component library (57 components)

### Build & Runtime
- **Bun** - Fast JavaScript runtime and package manager
- **ESBuild** - Bundler (via Vite)
- **PostCSS** - CSS processing

### Deployment
- **Netlify** - Hosting platform with atomic deploys
- **GitHub** - Version control and CI trigger
- **Custom Domain**: intentsolutions.io

## Component Architecture

### Directory Structure
```
src/
├── components/        # Reusable UI components
│   └── ui/           # shadcn/ui design system (57 components)
├── pages/            # Route-level components
│   ├── Index.tsx    # Landing page
│   └── NotFound.tsx # 404 error page
├── hooks/            # Custom React hooks
│   ├── use-mobile.tsx
│   └── use-toast.ts
├── lib/              # Utility functions
│   └── utils.ts     # cn(), formatters, etc.
└── assets/           # Static assets
```

### Component Hierarchy
```
App.tsx
 ├── Index.tsx (Landing Page)
 │    ├── Header (Navigation)
 │    ├── Hero (Above fold)
 │    ├── Services (Features grid)
 │    ├── Testimonials (Social proof)
 │    ├── Contact (Form)
 │    └── Footer
 └── NotFound.tsx (404 Page)
```

## State Management

### Current Approach
- **Local State**: React useState for component-level state
- **Context**: Not currently used (static landing page)
- **No Global State**: No Redux/Zustand needed for static site

### Future Considerations
When adding dynamic features:
- Use React Context for theme/user preferences
- Consider Zustand for complex client-side state
- Use TanStack Query for server state (if API added)

## Routing

### Current Setup
- **Static Routes**: Index (/) and NotFound (404)
- **Router**: Configured in Vite/React Router (if applicable)
- **Netlify Redirects**: SPA fallback configured in `netlify.toml`

## Styling Strategy

### Tailwind CSS
- **Utility-First**: Compose styles with utility classes
- **Mobile-First**: Responsive breakpoints (sm, md, lg, xl, 2xl)
- **Design System**: Consistent spacing, colors, typography

### Component Styling
```typescript
import { cn } from "@/lib/utils"

// Conditional classes with cn() helper
<Button className={cn("base-classes", conditional && "active-classes")} />
```

### Theme Configuration
- Defined in `tailwind.config.ts`
- Custom colors, fonts, spacing
- shadcn/ui theme integration

## Build & Deployment Pipeline

### Development Workflow
```
1. Developer writes code
2. Vite HMR updates instantly
3. TypeScript type-checks in IDE
4. Changes visible at http://localhost:8080
```

### Production Workflow
```
1. Push to GitHub main branch
2. Netlify webhook triggered
3. Bun install dependencies
4. Vite builds production bundle
5. Netlify deploys to CDN
6. Site live at intentsolutions.io
```

### Build Optimization
- **Tree-shaking**: Removes unused code
- **Code splitting**: Lazy load routes/components
- **Asset optimization**: Images, CSS, JS minified
- **Cache busting**: Hashed filenames for cache invalidation

## Performance Optimizations

### Bundle Size
- **Target**: < 200KB gzipped
- **Current**: ~180KB estimated
- **Techniques**:
  - Dynamic imports for large components
  - Selective shadcn/ui component imports
  - Image optimization (lazy loading, WebP)

### Runtime Performance
- **Lighthouse Score Target**: 95+
- **Core Web Vitals**:
  - LCP (Largest Contentful Paint): < 2.5s
  - FID (First Input Delay): < 100ms
  - CLS (Cumulative Layout Shift): < 0.1

### Caching Strategy
- **Static Assets**: 1 year cache (immutable)
- **HTML**: No cache (Netlify handles updates)
- **Service Worker**: Not implemented (consider for offline support)

## Security Architecture

### Client-Side Security
- **CSP**: Content Security Policy headers (Netlify)
- **HSTS**: HTTP Strict Transport Security
- **XSS Prevention**: React escapes content by default
- **No Inline Scripts**: All JavaScript bundled

### Build-Time Security
- **Dependency Scanning**: Future - Dependabot (not yet implemented)
- **Type Safety**: TypeScript strict mode
- **Secrets Management**: Environment variables (not committed to Git)

## Data Flow

### Static Site (Current)
```
User Request
    ↓
Netlify CDN
    ↓
Static HTML/CSS/JS
    ↓
React Hydration
    ↓
Interactive Page
```

### Future (With API)
```
User Action
    ↓
React Component
    ↓
API Call (fetch/axios)
    ↓
Backend Service
    ↓
Response
    ↓
Update Component State
    ↓
Re-render UI
```

## Testing Strategy (Future)

### Test Pyramid
```
     E2E Tests (5%)
    ↗            ↖
Integration Tests (15%)
    ↗            ↖
  Unit Tests (80%)
```

### Testing Tools (When Implemented)
- **Vitest**: Unit and integration tests
- **Testing Library**: Component testing
- **Playwright**: End-to-end tests
- **Lighthouse CI**: Performance regression tests

## Monitoring (Future)

### Metrics to Track
- **Performance**: Lighthouse scores, Core Web Vitals
- **Errors**: Sentry or similar error tracking
- **Analytics**: Google Analytics or Plausible
- **Uptime**: Netlify status or external monitoring

## Accessibility

### Standards
- **WCAG 2.1 Level AA** compliance target
- **Semantic HTML**: Proper heading hierarchy
- **ARIA Labels**: For interactive elements
- **Keyboard Navigation**: All features accessible via keyboard
- **Screen Reader**: Tested with NVDA/JAWS

## Browser Support

### Target Browsers
- **Chrome/Edge**: Last 2 versions
- **Firefox**: Last 2 versions
- **Safari**: Last 2 versions
- **Mobile**: iOS Safari, Chrome Android

### Polyfills
- None required (modern ES6+ features only)
- Consider adding if supporting older browsers

## Future Architecture Enhancements

### Short-Term (Next 3 Months)
- Add CI/CD pipeline (GitHub Actions)
- Implement automated testing (Vitest)
- Add ESLint + Prettier automation
- Set up error tracking (Sentry)

### Long-Term (6-12 Months)
- Add CMS integration (Sanity or Contentful)
- Implement analytics dashboard
- Add blog functionality
- Internationalization (i18n) support

---
**Last Updated**: October 4, 2025
**Architecture Version**: 1.0.0
