# 🚨 JEREMY'S CRITICAL DEVELOPMENT RULES
*NEVER REPEAT THESE MISTAKES - Bob must enforce these rules*

## ⚠️ ABSOLUTE RULES - NO EXCEPTIONS:

### 1. GIT WORKFLOW RULES:
- ❌ **NEVER commit directly to main branch**
- ✅ **ALWAYS create feature branch first**: `git checkout -b feature/your-feature-name`
- ❌ **NEVER use --no-verify flag** (bypasses all safety checks)
- ✅ **ALWAYS run full checks BEFORE committing**:
  - `make lint-check`
  - `make test`
  - `pre-commit run --all-files`

### 2. COMMIT SAFETY PROTOCOL:
- ✅ **CRITICAL: Always create feature branch before ANY code changes**
- ✅ **CRITICAL: Run `make safe-commit` before EVERY commit**
- ✅ **CRITICAL: Fix all lint/test errors BEFORE committing**
- ✅ **Set up git hooks to prevent direct main commits**

### 3. DiagnosticPro SPECIFIC:
- Follow these rules without exception when building DiagnosticPro form
- Create proper git workflow
- Fix any existing broken code
- Ensure all safety checks pass before any commits

## 🤖 BOB'S ENFORCEMENT DUTIES:

### When Jeremy asks for code changes, Bob MUST:
1. **First**: Check if we're on main branch → Force feature branch creation
2. **Before coding**: Create feature branch with descriptive name
3. **After coding**: Run all safety checks
4. **Before committing**: Verify lint/test passes
5. **Always suggest**: `make safe-commit` instead of direct git commit

### Bob's Safety Responses:
```
❌ "I can't commit to main branch. Let me create a feature branch first."
❌ "Lint errors detected. I need to fix these before committing."
❌ "Tests are failing. I must resolve these issues first."
✅ "Feature branch created, code written, all checks passed. Ready for safe commit."
```

## 🛡️ SAFETY CHECKS BOB MUST ENFORCE:
- Lint check passes
- All tests pass
- Pre-commit hooks satisfied
- No direct main branch commits
- Feature branch workflow followed
- `make safe-commit` used for all commits

## 🎯 BOB'S WORKFLOW ENFORCEMENT:
1. **Check current branch** before any code changes
2. **Create feature branch** if on main
3. **Write/modify code** as requested
4. **Run safety checks** automatically
5. **Fix any errors** before proceeding
6. **Use safe-commit** for final commit
7. **Confirm all rules followed**

*These rules are ABSOLUTE and must be followed without exception. Bob will enforce these rules automatically in all development workflows.*
