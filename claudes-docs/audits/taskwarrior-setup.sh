#!/bin/bash

# TaskWarrior Project: dir-audit
# Date: 2025-10-05
# Purpose: Track directory audit remediation tasks

echo "Creating TaskWarrior project: dir-audit"
echo "========================================"

# Master task
task add project:dir-audit +MASTER priority:H "Complete directory audit and transformation"

# SECURITY tasks (CRITICAL - TODAY)
echo ""
echo "SECURITY TASKS (CRITICAL - P0):"
task add project:dir-audit +SECURITY priority:H due:today "Rotate exposed Google API key and Neo4j password"
task add project:dir-audit +SECURITY priority:H due:today "Remove hardcoded password from deploy_phase5.sh"
task add project:dir-audit +SECURITY priority:H due:today "Redact secrets from archived code files"
task add project:dir-audit +SECURITY priority:H due:tomorrow "Create SECURITY.md with vulnerability reporting process"
task add project:dir-audit +SECURITY priority:H due:tomorrow "Add security scanning to CI/CD pipeline (bandit, safety)"

# PERFORMANCE tasks (CRITICAL - TODAY)
echo ""
echo "PERFORMANCE TASKS (CRITICAL - P0):"
task add project:dir-audit +PERFORMANCE priority:H due:today "Update .gitignore to exclude cache directories"
task add project:dir-audit +PERFORMANCE priority:H due:today "Remove 137MB cache files from git tracking"
task add project:dir-audit +PERFORMANCE priority:H due:today "Delete local cache directories"
task add project:dir-audit +PERFORMANCE priority:M due:tomorrow "Verify caches regenerate correctly"

# STRUCTURE tasks (HIGH - TOMORROW)
echo ""
echo "STRUCTURE TASKS (HIGH - P1):"
task add project:dir-audit +STRUCTURE priority:H due:tomorrow "DECIDE: Migrate to standard structure OR remove standard dirs"
task add project:dir-audit +STRUCTURE priority:H due:tomorrow "Move 5 root scripts to 05-Scripts/deploy/"
task add project:dir-audit +STRUCTURE priority:M due:3days "Consolidate archive/ into 99-Archive/legacy/"
task add project:dir-audit +STRUCTURE priority:M due:3days "Update .gitignore for cache directories"

# DOCS tasks (MEDIUM - THIS WEEK)
echo ""
echo "DOCUMENTATION TASKS (MEDIUM - P2):"
task add project:dir-audit +DOCS priority:H due:3days "Populate CHANGELOG.md with version history"
task add project:dir-audit +DOCS priority:H due:3days "Create CONTRIBUTING.md with dev guidelines"
task add project:dir-audit +DOCS priority:M due:1week "Enhance README.md with prerequisites and troubleshooting"
task add project:dir-audit +DOCS priority:M due:1week "Add architecture diagram to README"

# NAMING tasks (LOW - NEXT WEEK)
echo ""
echo "NAMING TASKS (LOW - P3):"
task add project:dir-audit +NAMING priority:M due:1week "Rename 5 root-level scripts to kebab-case"
task add project:dir-audit +NAMING priority:H due:1week "Rename circle_of_life.py and update imports"
task add project:dir-audit +NAMING priority:L due:2weeks "Rename test_reports directory and files"

# CONTENT tasks (MEDIUM - THIS WEEK)
echo ""
echo "CONTENT TASKS (MEDIUM - P2):"
task add project:dir-audit +CONTENT priority:M due:1week "Consolidate ai-dev-tasks to 01-Docs/"
task add project:dir-audit +CONTENT priority:L due:2weeks "Consolidate reports to claudes-docs/reports/"

echo ""
echo "=========================================="
echo "TaskWarrior project created successfully!"
echo ""
echo "View all tasks:"
echo "  task project:dir-audit list"
echo ""
echo "View by priority:"
echo "  task project:dir-audit priority:H list"
echo ""
echo "View by tag:"
echo "  task project:dir-audit +SECURITY list"
echo "  task project:dir-audit +PERFORMANCE list"
echo "  task project:dir-audit +STRUCTURE list"
echo "  task project:dir-audit +DOCS list"
echo ""
