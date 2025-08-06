# CRITICAL DEVELOPMENT RULES

## 🚨 NEVER BREAK THESE RULES

### 1. **NEVER COMMIT DIRECTLY TO MAIN BRANCH**
- **ALWAYS** create feature branch first: `git checkout -b feature/your-feature-name`
- Main branch is **PROTECTED** - commits will be rejected

### 2. **NEVER USE --no-verify FLAG**
- This bypasses **ALL** safety checks
- **FORBIDDEN** in all circumstances

### 3. **ALWAYS RUN FULL CHECKS BEFORE COMMITTING**
Required commands:
- `make lint-check` - Code quality checks
- `make test` - Syntax and basic tests
- `make safe-commit` - Complete safety verification

### 4. **CRITICAL: Feature Branch Workflow**
```bash
# Step 1: Create feature branch (REQUIRED)
make feature BRANCH=your-feature-name

# Step 2: Make your changes
# ... edit files ...

# Step 3: Run CRITICAL safety checks
make safe-commit

# Step 4: Commit ONLY if all checks pass
git add .
git commit -m "your commit message"
```

### 5. **Git Hooks Protection**
- Pre-commit hook **BLOCKS** direct main commits
- **Cannot be bypassed** - enforced automatically
- Run `make setup-hooks` to enable

### 6. **CRITICAL Safety Commands**

| Command | Purpose |
|---------|---------|
| `make check-branch` | Verify not on main branch |
| `make feature BRANCH=name` | Create feature branch |
| `make lint-check` | Run code quality checks |
| `make test` | Run syntax tests |
| `make safe-commit` | **Complete safety verification** |
| `make setup-hooks` | Enable main branch protection |

### 7. **Zero Tolerance Policy**
- **ANY** direct main branch commit = **IMMEDIATE FAILURE**
- **ALL** lint/test errors **MUST** be fixed before commit
- **NO EXCEPTIONS** to these rules

---

## 🛡️ Safety First - Quality Always

**These rules protect code quality and prevent deployment disasters.**
