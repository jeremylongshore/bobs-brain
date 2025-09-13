# 🚀 AI Dev Tasks System

Structured workflow for AI-assisted development using Claude Code.

## 📁 Structure

```
ai-dev-tasks/
├── templates/      # 📝 Working templates (START HERE)
├── PRDs/          # 📋 Product Requirements Documents
├── todos/         # ✅ Task lists and tracking
└── master/        # 🔒 Protected originals (DON'T EDIT)
```

## 🔄 The 3-Step Workflow

### Step 1: Define Requirements
```
📝 templates/create-prd.md 
    ↓
📋 PRDs/feature-name-prd.md
```

### Step 2: Generate Tasks
```
📝 templates/generate-tasks.md + 📋 PRD
    ↓
✅ todos/feature-name-tasks.md
```

### Step 3: Execute Tasks
```
📝 templates/process-task-list.md + ✅ task list
    ↓
🎯 Completed feature
```

## 💡 How to Use

1. **Start a new feature HERE:**
   - Tell Claude: "Create a PRD for [your feature]"
   - Claude uses `templates/create-prd.md`
   - Saves to `PRDs/`

2. **Break it into tasks:**
   - Tell Claude: "Generate tasks from that PRD"
   - Claude uses `templates/generate-tasks.md`
   - Saves to `todos/`

3. **Move to project & build:**
   - Copy PRD and tasks to target project (e.g., `~/projects/scraper/`)
   - Tell Claude: "Start with task 1.1"
   - Claude builds the actual code in that project
   - Uses `process-task-list.md` to work through tasks

## ✨ Benefits

- **Structured approach** - No more monolithic requests
- **Review checkpoints** - Approve each step
- **Clear documentation** - Track what you're building
- **Progress visibility** - See tasks getting completed

## 🎯 Quick Start

```bash
# View templates
ls templates/

# Check your PRDs
ls PRDs/

# See task lists
ls todos/
```

Tell Claude: "I want to build [feature]" and let the workflow guide you!