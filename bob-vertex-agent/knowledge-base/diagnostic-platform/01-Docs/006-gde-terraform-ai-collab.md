# DevOps Guide: AI-Assisted Terraform Migration

**For:** DiagnosticPro DevOps Engineer
**Purpose:** Step-by-step instructions for working with Claude Code on Terraform migration
**Related Docs:**
- **PRD**: `054-prd-terraform-infrastructure-migration.md`
- **Tasks**: `055-ref-terraform-migration-tasks.md` (47 sub-tasks)
- **ADR**: `059-adr-terraform-infrastructure-as-code.md`

---

## Quick Start: Your First AI-Assisted Task

### Step 1: Open Claude Code
```bash
# In your terminal from DiagnosticPro directory
cd /home/jeremy/projects/diagnostic-platform/DiagnosticPro
claude  # Or however you launch Claude Code
```

### Step 2: Start with Task 1.1 (Directory Setup)
**Say this to Claude Code:**
```
I'm ready to start the Terraform migration. Please begin with Task 1.1
from 055-ref-terraform-migration-tasks.md - create the production
Terraform directory structure.
```

**Claude will:**
1. Create `terraform/`, `terraform/modules/`, `terraform/environments/prod/` directories
2. Show you what it's doing with commands
3. Ask for confirmation before making changes

### Step 3: Review Changes Before Saying "Yes"
```
YOU: Can I see exactly what directories you're creating?
CLAUDE: [Shows directory structure]
YOU: Looks good, proceed.
CLAUDE: [Creates directories and confirms completion]
```

---

## How to Work with Claude Code (Best Practices)

### ✅ DO: Give Claude Context
**GOOD:**
```
I'm working on Task 2.3 - importing the diagnosticpro-vertex-ai-backend
Cloud Run service. The service is already running in us-central1.
Can you generate the terraform import command and explain what it does?
```

**WHY:** Claude knows exactly where you are in the task list and what you need.

### ✅ DO: Ask Claude to Explain Complex Commands
**GOOD:**
```
Before I run this terraform import command, can you explain:
1. What resources it will import
2. What changes it will make to the state file
3. What I should verify after running it
```

**WHY:** You understand what's happening before executing commands.

### ✅ DO: Ask Claude to Check Your Work
**GOOD:**
```
I just ran terraform plan and got this output:
[paste output]

Does this look correct? Should I see 0 changes or are there expected differences?
```

**WHY:** Claude can validate your work against the migration plan.

### ❌ DON'T: Say "Do everything"
**BAD:**
```
Just complete all the Terraform tasks for me.
```

**WHY:** You need to understand each step. AI assists, doesn't replace your expertise.

### ❌ DON'T: Skip Validation Steps
**BAD:**
```
Skip the terraform plan step, just import everything.
```

**WHY:** Validation prevents production issues. Always verify state matches reality.

---

## Task-by-Task Workflow (Use This Pattern)

### Pattern for Each Task:
```
1. READ the task from 055-ref-terraform-migration-tasks.md
2. ASK Claude to explain the task in plain English
3. REVIEW Claude's proposed commands
4. EXECUTE commands (Claude can run them for you)
5. VERIFY results with Claude's help
6. MARK task complete in 055-ref-terraform-migration-tasks.md
```

### Example: Task 1.2 (Move Existing Modules)

**STEP 1: Read Task**
```
Task 1.2: Move existing research modules from
08-features/09-terraform-research/modules/ to terraform/modules/
```

**STEP 2: Ask Claude**
```
YOU: I'm ready for Task 1.2. Can you:
1. Show me what modules exist in 08-features/09-terraform-research/modules/
2. Explain what each module does
3. Generate the mv commands to move them to terraform/modules/
```

**STEP 3: Review Claude's Response**
```
CLAUDE: Found 4 modules:
- cloud-run/ - Creates Cloud Run services with autoscaling
- iam/ - Manages service accounts and IAM bindings
- firestore/ - Creates Firestore database
- storage/ - Creates Cloud Storage buckets with lifecycle rules

Commands to move them:
mv 08-features/09-terraform-research/modules/cloud-run terraform/modules/
mv 08-features/09-terraform-research/modules/iam terraform/modules/
[etc...]

Should I proceed?
```

**STEP 4: Execute**
```
YOU: Yes, please move the modules.
CLAUDE: [Executes mv commands and confirms]
```

**STEP 5: Verify**
```
YOU: Can you verify all 4 modules are now in terraform/modules/?
CLAUDE: [Shows ls terraform/modules/ output]
All 4 modules successfully moved.
```

**STEP 6: Mark Complete**
```
YOU: Please mark Task 1.2 as complete in the task list.
CLAUDE: [Updates 055-ref-terraform-migration-tasks.md with [x]]
```

---

## Working with Terraform Import Commands

### Understanding Terraform Import

**What it does:**
- Adds existing GCP resources to Terraform state
- Does NOT recreate resources (zero downtime)
- Allows Terraform to manage existing infrastructure

**Example from Task 2.3:**
```bash
terraform import \
  module.vertex_ai_backend.google_cloud_run_service.main \
  projects/diagnostic-pro-prod/locations/us-central1/services/diagnosticpro-vertex-ai-backend
```

### How to Use AI for Import Tasks

**STEP 1: Ask Claude to Generate Import Command**
```
YOU: I'm on Task 2.3 - importing diagnosticpro-vertex-ai-backend.
Can you generate the import command with the correct resource path?
```

**STEP 2: Ask Claude to Explain Before Running**
```
YOU: Before I run this, explain:
- What module is this importing to? (module.vertex_ai_backend)
- What resource type? (google_cloud_run_service.main)
- What GCP resource? (diagnosticpro-vertex-ai-backend service)
```

**STEP 3: Run Command with Claude's Assistance**
```
YOU: Run the import command for me.
CLAUDE: [Executes terraform import and shows output]
```

**STEP 4: Verify with terraform plan**
```
YOU: Now run terraform plan to verify 0 changes.
CLAUDE: [Runs terraform plan]

Expected output: "No changes. Your infrastructure matches the configuration."
```

### Critical Validation Pattern

**After EVERY import, run this check:**
```bash
terraform plan
```

**Expected result:** `No changes. Infrastructure matches configuration.`

**If you see changes:**
1. **STOP** - Do not run `terraform apply`
2. Ask Claude: "I'm seeing changes after import. Is this expected?"
3. Review differences with Claude's help
4. Update Terraform code to match actual infrastructure

---

## Common AI Prompts for Terraform Tasks

### Module Development
```
Generate a Terraform module for Secret Manager that:
1. Creates secret metadata only (not values)
2. Accepts secret_id and rotation_policy as variables
3. Outputs the secret name for reference
4. Follows Google Cloud best practices
```

### Debugging Terraform Errors
```
I got this Terraform error:
[paste error output]

Can you:
1. Explain what caused it
2. Show me how to fix it
3. Suggest ways to prevent it in the future
```

### Security Scanning
```
I ran tfsec on terraform/ and got these warnings:
[paste tfsec output]

For each warning:
1. Explain the security risk
2. Show me the fix
3. Help me update the code
```

### State Management Issues
```
I'm seeing a state lock error. Can you help me:
1. Understand what caused the lock
2. Check if it's safe to force-unlock
3. Prevent this in the future
```

---

## Sprint Planning with AI

### Sprint 1: Project Setup & Cloud Run (Oct 7-18)

**Week 1 Focus:** Tasks 1.0 (Project Setup)
```
YOU: I want to complete all of Task 1.0 this week. Can you:
1. List all 8 sub-tasks (1.1 through 1.8)
2. Estimate time for each sub-task
3. Identify any blockers or dependencies
4. Create a daily plan for me
```

**Claude will generate:**
- Monday: Tasks 1.1-1.3 (directory setup, module migration)
- Tuesday: Tasks 1.4-1.5 (backend config, terraform init)
- Wednesday: Tasks 1.6-1.7 (validation, security scanning)
- Thursday: Task 1.8 (fix security issues)
- Friday: Review and documentation

**Week 2 Focus:** Tasks 2.0 (Cloud Run Import)
```
YOU: I'm ready for Cloud Run imports (Task 2.0). Walk me through
importing the first service step-by-step.
```

### Sprint 2: Firestore, Secrets, Storage (Oct 21-Nov 1)

**Week 1 Kickoff:**
```
YOU: Starting Sprint 2 with Secret Manager (Task 3.0). Can you:
1. Show me the 8 secrets I need to import
2. Generate import commands for all of them
3. Explain the 90-day rotation policy requirement
```

### Sprint 3: IAM, Networking, CI/CD (Nov 4-15)

**Week 1 Kickoff:**
```
YOU: Starting Sprint 3 with IAM (Task 4.0). Can you:
1. List all 12 service accounts
2. Explain the IAM role bindings for each
3. Generate import commands
4. Warn me about common IAM pitfalls
```

---

## Safety Checks (Always Do This)

### Before Running ANY Terraform Command

**Ask Claude:**
```
Before I run [command], can you confirm:
1. What changes will this make?
2. Is this safe to run in production?
3. Can I rollback if something goes wrong?
4. What should I verify after running it?
```

### Before Committing Code

**Ask Claude:**
```
I'm about to commit my Terraform changes. Can you:
1. Review my terraform files for issues
2. Check if I followed best practices
3. Verify security scanning passed (tfsec)
4. Suggest a good commit message
```

### Before Merging to Main

**Ask Claude:**
```
I have a PR ready to merge. Can you:
1. Review the terraform plan output
2. Confirm no unexpected changes
3. Check all validation tasks completed
4. Verify CI/CD tests passed
```

---

## AI-Assisted Documentation

### Auto-Generate Module Docs
```
YOU: I just finished the cloud-run module. Can you:
1. Run terraform-docs to generate README
2. Explain how to use the module
3. Add usage examples
4. Document all input variables and outputs
```

**Claude will run:**
```bash
terraform-docs markdown table terraform/modules/cloud-run > terraform/modules/cloud-run/README.md
```

### Create Disaster Recovery Runbook
```
YOU: I need to create the disaster recovery runbook (Task 5.6). Can you:
1. Document the full terraform destroy && terraform apply procedure
2. Add pre-flight checks
3. Include rollback steps
4. Estimate recovery time
5. Save to 01-docs/061-gde-terraform-disaster-recovery.md
```

---

## Troubleshooting with AI

### Scenario 1: Import Failed
```
YOU: terraform import failed with this error:
[paste error]

What's wrong and how do I fix it?
```

**Claude will:**
1. Diagnose the error (wrong resource ID, missing permissions, etc.)
2. Show the correct import command
3. Help you verify the resource exists in GCP

### Scenario 2: State Drift Detected
```
YOU: terraform plan shows unexpected changes after import:
[paste plan output]

Should I see these changes or is something wrong?
```

**Claude will:**
1. Explain each detected change
2. Identify if it's expected or indicates drift
3. Show how to update Terraform code to match reality
4. Help you decide: accept changes or fix infrastructure

### Scenario 3: Module Not Working
```
YOU: I copied the cloud-run module but it's giving errors:
[paste error]

Can you debug this?
```

**Claude will:**
1. Analyze the error message
2. Check module inputs/outputs
3. Validate provider configuration
4. Test the module with terraform validate

---

## Using Claude for Code Review

### Before Each Commit
```
YOU: Review my Terraform code before I commit:
[paste terraform files or specify path]

Check for:
1. Security issues
2. Best practices violations
3. Missing documentation
4. Incorrect variable types
```

### PR Review Assistance
```
YOU: I have a PR with these Terraform changes:
[paste git diff or describe changes]

Can you:
1. Review the changes
2. Suggest improvements
3. Check for breaking changes
4. Write a PR description
```

---

## CI/CD Pipeline with AI (Task 5.1-5.5)

### Creating GitHub Actions Workflow
```
YOU: I'm on Task 5.1 - creating .github/workflows/terraform.yml.
Can you generate a workflow that:
1. Runs terraform plan on every PR
2. Posts plan output as PR comment
3. Runs terraform apply on merge to main
4. Includes manual approval gate
```

**Claude will generate complete workflow file with:**
- Terraform setup action
- GCP authentication
- Plan/apply logic
- Comment posting
- Approval gates

---

## Quick Reference: Claude Code Commands

### Getting Started
```bash
# Ask Claude to read task list
"Read 055-ref-terraform-migration-tasks.md and tell me what Task 1.1 requires"

# Ask Claude to explain a concept
"Explain how Terraform state locking works with GCS backend"

# Ask Claude to generate code
"Generate a Cloud Run module with autoscaling from 0 to 10 instances"
```

### Execution Assistance
```bash
# Let Claude run commands for you
"Run terraform init in the terraform/ directory"

# Let Claude validate results
"Run terraform plan and tell me if the output looks correct"

# Let Claude check status
"List all Cloud Run services in diagnostic-pro-prod and show their status"
```

### Documentation Help
```bash
# Generate docs
"Run terraform-docs on all modules and create READMEs"

# Update task list
"Mark Task 1.3 as complete in 055-ref-terraform-migration-tasks.md"

# Create runbooks
"Create a disaster recovery runbook based on our Terraform setup"
```

---

## Daily Workflow Example

### Morning Standup with AI
```
YOU: Good morning! I'm starting Day 3 of Sprint 1. Can you:
1. Show me what tasks I completed yesterday
2. List what's next on my task list
3. Identify any blockers
4. Suggest today's focus
```

### During Development
```
YOU: I'm working on Task 2.4 (import stripe-webhook service).
Walk me through this step-by-step.

CLAUDE: [Provides step-by-step guidance with explanations]

YOU: [Follows steps with Claude's help]

YOU: Task complete. Mark 2.4 as done and show me Task 2.5.
```

### End of Day
```
YOU: End of day summary. What did I accomplish today?

CLAUDE: Today you completed:
- Task 2.3: Imported vertex-ai-backend ✅
- Task 2.4: Imported stripe-webhook ✅
- Task 2.5: Imported simple-diagnosticpro ✅
All imports verified with terraform plan (0 changes)

YOU: Create an end-of-day report in 01-docs/
```

---

## Emergency: When Things Go Wrong

### If You Accidentally Run terraform apply
```
YOU: HELP! I accidentally ran terraform apply and it's making changes
I didn't expect. What do I do?

CLAUDE:
1. CTRL+C to stop if still running
2. Check what changes were made: terraform show
3. Review state file backup: terraform state pull
4. I'll help you assess damage and create rollback plan
```

### If You Break the State File
```
YOU: My terraform state file is corrupted. Can you help me recover?

CLAUDE:
1. GCS backend has versioning enabled
2. List previous versions: gsutil ls -la gs://diagnostic-pro-prod-terraform-state/
3. Restore previous version: [Claude shows commands]
4. Verify state integrity: terraform state list
```

### If You Can't Figure Something Out
```
YOU: I'm completely stuck on Task 3.7 (composite indexes). I don't
understand what I'm supposed to do.

CLAUDE: Let me break this down:
1. Firestore composite indexes allow querying multiple fields
2. You need 4 indexes for: [explains each one]
3. Here's the Terraform code: [generates code]
4. Here's how to test: [shows validation]
```

---

## Success Metrics (Check with AI)

### After Each Sprint
```
YOU: Sprint 1 is complete. Can you generate a summary showing:
1. All tasks completed (should be 16/16)
2. All terraform plan outputs showing 0 changes
3. All security scans passed
4. All health checks passing
5. Any issues or concerns for next sprint
```

### Project Completion Check
```
YOU: All 3 sprints complete. Can you verify we hit all success metrics
from the PRD (054-prd-terraform-infrastructure-migration.md)?

CLAUDE: [Reviews success metrics]
✅ Deployment time: 8h → 15min (achieved)
✅ Configuration errors: 3-5/month → 0 (achieved)
✅ Disaster recovery: 8h → 30min (achieved)
✅ Infrastructure audit trail: Git history (achieved)
✅ Environment parity: Code-defined (achieved)
```

---

## Final Tips for Working with AI

### 1. Be Specific
❌ "Fix this"
✅ "This terraform import command is failing with error X. Can you help me debug it?"

### 2. Ask for Explanations
❌ Just copy/paste commands blindly
✅ "Explain what this command does before I run it"

### 3. Verify Everything
❌ Trust AI output without validation
✅ "Run terraform plan to verify this worked correctly"

### 4. Build Understanding
❌ Let AI do everything without learning
✅ "Why did you choose this approach over alternatives?"

### 5. Document Your Work
❌ Forget to update task list
✅ "Mark this task complete and create a summary of what we did"

---

## Need Help? Ask Claude These Questions

```
"I don't understand what Task X.X is asking me to do. Can you explain it?"

"What's the safest way to approach this task?"

"Can you walk me through this step-by-step?"

"Is there anything I should be careful about with this command?"

"How do I verify this worked correctly?"

"What should I do if this fails?"

"Can you review my work before I commit?"

"What's the next task after this one?"

"Am I on track to finish this sprint on time?"

"What are the biggest risks with this migration?"
```

---

**Remember:** Claude Code is your AI pair programmer. Use it to:
- ✅ Explain complex concepts
- ✅ Generate boilerplate code
- ✅ Debug issues
- ✅ Validate your work
- ✅ Document your progress

**But YOU are the expert.** Final decisions are yours. Claude assists, you decide.

---

**Good luck with your Terraform migration!** 🚀

Start with Task 1.1 and work through the list systematically. Claude will be with you every step of the way.

---

**Last Updated:** 2025-10-06
**Next Review:** After Sprint 1 completion (Oct 18, 2025)
