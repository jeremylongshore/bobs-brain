# 🚨 CRITICAL DEVELOPMENT RULES - BOB'S BRAIN

## ⛔ NEVER BREAK THESE RULES

### 1. BRANCH PROTECTION
- **NEVER** commit directly to `main` branch
- **ALWAYS** create feature branch first:
  ```bash
  git checkout -b feature/your-feature-name
  ```

### 2. SAFETY FLAGS
- **NEVER** use `--no-verify` flag (bypasses safety checks)
- **NEVER** use `--force` without team approval
- **NEVER** use `git push -f` on shared branches

### 3. PRE-COMMIT CHECKS
- **ALWAYS** run checks BEFORE committing:
  ```bash
  make check-all        # Run all checks
  make lint-check       # Linting only
  make test            # Tests only
  make security-check  # Security scan
  ```

### 4. COMMIT WORKFLOW
```bash
# Step 1: Create feature branch
git checkout -b feature/my-feature

# Step 2: Make your changes
# ... edit files ...

# Step 3: Run safety checks
make safe-commit

# Step 4: If all passes, commit
git add .
git commit -m "feat: descriptive message"

# Step 5: Push to feature branch
git push origin feature/my-feature
```

## 🛡️ AUTOMATED PROTECTIONS

### Git Hooks Installed
1. **pre-commit**: Prevents commits to main, runs linting
2. **pre-push**: Prevents pushes to main, checks for secrets

### Make Commands
- `make help` - Show all available commands
- `make dev-setup` - Set up complete dev environment
- `make check-all` - Run ALL safety checks
- `make safe-commit` - Verify ready to commit
- `make status` - Show project status

## 📋 CHECKLIST BEFORE EVERY COMMIT

- [ ] On feature branch (not main)
- [ ] Ran `make lint-check` - all passed
- [ ] Ran `make test` - all passed
- [ ] Ran `make security-check` - no secrets
- [ ] No hardcoded tokens/keys/secrets
- [ ] Code is formatted (`make format`)
- [ ] Commit message is descriptive

## 🚫 COMMON MISTAKES TO AVOID

1. **Committing secrets**
   - Never commit .env files
   - Never hardcode tokens
   - Use environment variables

2. **Skipping tests**
   - Always run tests before commit
   - Fix broken tests immediately
   - Don't comment out failing tests

3. **Poor commit messages**
   - ❌ "fix", "update", "changes"
   - ✅ "feat: add user authentication"
   - ✅ "fix: resolve database connection timeout"

## 🔧 FIX COMMON ISSUES

### If you accidentally committed to main:
```bash
# Stash your changes
git stash

# Switch to main and reset
git checkout main
git reset --hard origin/main

# Create feature branch
git checkout -b feature/fix-name

# Apply your changes
git stash pop
```

### If pre-commit hooks fail:
```bash
# Auto-fix formatting
make format

# Check what's failing
make check-all

# Fix issues then retry
git add .
git commit -m "your message"
```

### If you committed secrets:
```bash
# DO NOT PUSH!
# Remove from history
git reset --soft HEAD~1
# Remove the secret from files
# Re-commit without secrets
```

## 📊 COMMIT MESSAGE FORMAT

Use conventional commits:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting, no code change
- `refactor:` - Code change that neither fixes nor adds
- `test:` - Adding tests
- `chore:` - Maintenance

## 🎯 GOLDEN RULES

1. **Branch Protection is Sacred** - Never bypass
2. **Tests Must Pass** - No exceptions
3. **No Secrets in Code** - Ever
4. **Review Before Commit** - Always
5. **Clean Commit History** - Maintain it

## 🆘 EMERGENCY CONTACTS

- GitHub Issues: https://github.com/jeremylongshore/bobs-brain/issues
- Project Lead: Jeremy Longshore
- Documentation: CLAUDE.md

---

**Remember: These rules protect our code, our users, and our sanity. Follow them without exception.**