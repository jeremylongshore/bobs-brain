# Troubleshooting Guide

Common issues and solutions for the Intent Solutions landing page project.

## Build Issues

### Error: "Cannot find module 'bun'"

**Problem**: Bun runtime not installed

**Solution**:
```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Restart terminal and verify
bun --version
```

### Error: "Module not found" after `bun install`

**Problem**: Dependency installation incomplete or corrupted

**Solution**:
```bash
# Clear cache and reinstall
rm -rf node_modules bun.lockb
bun install
```

### Error: TypeScript errors during build

**Problem**: Type checking failed

**Solution**:
```bash
# Check TypeScript errors
bun run tsc --noEmit

# Fix type errors in reported files
# Then rebuild
bun run build
```

## Development Server Issues

### Port 8080 Already in Use

**Problem**: Another process using port 8080

**Solution**:
```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port
PORT=3000 bun run dev
```

### HMR (Hot Module Replacement) Not Working

**Problem**: Changes not reflected in browser

**Solution**:
1. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Restart dev server
3. Clear browser cache
4. Check console for errors

### Tailwind Classes Not Applying

**Problem**: Tailwind CSS not processing styles

**Solution**:
```bash
# Verify tailwind.config.ts is correct
# Check content paths include all source files

# Restart dev server
bun run dev
```

## Deployment Issues

### Netlify Build Failed

**Problem**: Build errors on Netlify

**Solution**:
1. Check Netlify build logs for specific error
2. Verify `netlify.toml` configuration:
```toml
[build]
  command = "bun install && bun run build"
  publish = "dist"
```
3. Test build locally:
```bash
bun run build
bun run preview
```

### Custom Domain Not Working

**Problem**: intentsolutions.io not resolving

**Solution**:
1. Verify DNS records in Porkbun:
   - A record: @ → 75.2.60.5
   - CNAME: www → [your-site].netlify.app
2. Wait for DNS propagation (5-10 minutes)
3. Check: https://www.whatsmydns.net/#A/intentsolutions.io

### HTTPS Certificate Issues

**Problem**: SSL/TLS certificate not provisioning

**Solution**:
1. Netlify → Site settings → Domain management
2. Click "Verify DNS configuration"
3. Click "Provision certificate"
4. Wait 1-2 minutes

## Component Issues

### shadcn/ui Component Not Found

**Problem**: `import { Button } from "@/components/ui/button"` fails

**Solution**:
```bash
# Verify file exists
ls src/components/ui/button.tsx

# Check tsconfig.json path alias
# Should have: "@/*": ["./src/*"]

# Restart dev server
```

### Tailwind Classes Not Working on Component

**Problem**: Custom component styles not applying

**Solution**:
1. Verify component file is in `tailwind.config.ts` content array
2. Use `cn()` helper for dynamic classes:
```typescript
import { cn } from "@/lib/utils"
<div className={cn("base-class", conditional && "active")} />
```

## VSCode Issues

### IntelliSense Not Working

**Problem**: No autocomplete for imports

**Solution**:
1. Install recommended extensions (.vscode/extensions.json)
2. Restart VSCode
3. Run: TypeScript: Restart TS Server (Cmd+Shift+P)

### Prettier Not Formatting on Save

**Problem**: Code not auto-formatting

**Solution**:
1. Install Prettier extension
2. Verify `.vscode/settings.json`:
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```
3. Restart VSCode

## Git Issues

### Cannot Push to GitHub

**Problem**: Authentication failed

**Solution**:
```bash
# Use personal access token (not password)
# GitHub Settings → Developer settings → Personal access tokens

# Or use SSH
git remote set-url origin git@github.com:jeremylongshore/intent-solutions-landing.git
```

### Merge Conflicts

**Problem**: Git merge conflicts

**Solution**:
```bash
# View conflicts
git status

# Edit conflicted files (remove markers)
# Choose correct version

# Mark as resolved
git add <file>
git commit -m "fix: resolve merge conflicts"
```

## Performance Issues

### Slow Development Server

**Problem**: Dev server sluggish

**Solution**:
1. Clear Vite cache:
```bash
rm -rf node_modules/.vite
```
2. Restart dev server
3. Check system resources (CPU, RAM)

### Large Bundle Size

**Problem**: Production build > 300KB

**Solution**:
1. Analyze bundle:
```bash
bun run build
# Check dist/ folder sizes
```
2. Dynamic import large components:
```typescript
const Heavy = React.lazy(() => import('./Heavy'))
```
3. Remove unused shadcn/ui components

## Common Error Messages

### "Cannot read property 'map' of undefined"

**Cause**: Data not loaded before rendering

**Solution**:
```typescript
// Add null check
{data?.map(item => <div key={item.id}>{item.name}</div>)}
```

### "Maximum update depth exceeded"

**Cause**: setState in render causing infinite loop

**Solution**:
```typescript
// Move setState to useEffect or event handler
useEffect(() => {
  setState(value)
}, [value])
```

### "Hydration failed"

**Cause**: Server/client HTML mismatch (rare in Vite)

**Solution**:
1. Check for `window` usage in SSR code
2. Wrap in `useEffect` if client-only logic

## Getting Help

### Still Stuck?

1. **Search existing issues**: Check GitHub issues for similar problems
2. **Check logs**: Read complete error messages (don't skip stack traces)
3. **Minimal reproduction**: Create minimal example to isolate issue
4. **Ask for help**:
   - GitHub Discussions (for questions)
   - GitHub Issues (for bugs)
   - Security email (for vulnerabilities - see 10-SECURITY.md)

### Before Asking

Provide:
- Error message (full text)
- Steps to reproduce
- Expected vs actual behavior
- Environment (OS, Bun version, browser)
- Relevant code snippets

### Useful Commands

```bash
# System info
bun --version
node --version
git --version

# Project info
ls -la
cat package.json

# Logs
cat netlify.log  # If exists
```

---
**Last Updated**: October 4, 2025
**Need more help?** See `05-CONTRIBUTING.md` for community guidelines.
