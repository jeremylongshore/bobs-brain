# 🚨 CRITICAL DEVELOPMENT RULES

**Put these rules into your memory and NEVER repeat these mistakes:**

## 📋 **MANDATORY WORKFLOW RULES**

1. **NEVER commit directly to main branch** - ALWAYS create feature branch first using `git checkout -b feature/your-feature-name`

2. **NEVER use --no-verify flag** as it bypasses all safety checks

3. **ALWAYS run full checks BEFORE committing:**
   - `make lint-check`
   - `make test`
   - `pre-commit run --all-files`

4. **CRITICAL: Always create feature branch before ANY code changes**

5. **CRITICAL: Run `make safe-commit` before EVERY commit**

6. **CRITICAL: Fix all lint/test errors BEFORE committing**

7. **Set up git hooks to prevent direct main commits**

## 🤖 **AI AGENT PROJECT RULES**

### **Branching Strategy:**
- Feature branches: `feature/ai-agent-name` (e.g., `feature/ai-bob-agent`)
- Never commit to main directly
- Always create PR for review

### **Safety Checks:**
- No `--no-verify` flag usage
- All pre-commit hooks must pass
- Lint and test validation required

### **AI Agent Safety:**
- Guardrails in place to prevent unintended AI actions
- No unauthorized API calls
- Tracing tools (AgentOps) for behavior logging
- Environment variables for sensitive data (never hard-coded)

### **Testing Requirements:**
- End-to-end Playwright tests in headless browser
- Validate complete workflow (input → processing → output)
- Test with real email: `jeremylongshore@gmail.com`
- Verify data persistence to database

### **Data & Security:**
- Save all data to designated database (BigQuery/PostgreSQL)
- Verify data storage correctness
- API keys in environment variables only
- No sensitive data in version control

## 🔄 **COMMIT WORKFLOW**

```bash
# 1. Create feature branch
git checkout -b feature/ai-your-feature

# 2. Make changes
# ... development work ...

# 3. Run safety checks
make lint-check
make test
pre-commit run --all-files

# 4. Safe commit
make safe-commit

# 5. Push feature branch
git push origin feature/ai-your-feature

# 6. Create PR with detailed description
```

## 📊 **VALIDATION CHECKLIST**

Before ANY commit:
- [ ] Feature branch created
- [ ] All safety checks pass
- [ ] No lint/test errors
- [ ] AI agent code complete and modular
- [ ] End-to-end tests pass
- [ ] Data persistence verified
- [ ] Security guardrails in place
- [ ] Documentation updated

**Follow these rules without exception for all AI agent projects including Bob's Brain, DiagnosticPro, and future developments.**
