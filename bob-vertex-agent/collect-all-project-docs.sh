#!/bin/bash
# Collect all documentation from all projects for Bob's knowledge base
# This grounds Bob in all project knowledge

set -e

echo "============================================="
echo "Collecting Documentation for Bob's Knowledge Base"
echo "============================================="

# Create knowledge-base directory
KNOWLEDGE_BASE_DIR="./knowledge-base"
mkdir -p "$KNOWLEDGE_BASE_DIR"

# Clear existing content
echo "Clearing existing knowledge base..."
rm -rf "$KNOWLEDGE_BASE_DIR"/*

# Counter
TOTAL_FILES=0

# Function to copy relevant files
collect_docs() {
    local PROJECT_PATH=$1
    local PROJECT_NAME=$(basename "$PROJECT_PATH")

    echo ""
    echo "Processing: $PROJECT_NAME"
    echo "-----------------------------------"

    # Create project subdirectory
    local PROJECT_DIR="$KNOWLEDGE_BASE_DIR/$PROJECT_NAME"
    mkdir -p "$PROJECT_DIR"

    # Find and copy documentation files
    # README files
    find "$PROJECT_PATH" -maxdepth 2 -iname "README*.md" -type f 2>/dev/null | while read file; do
        cp "$file" "$PROJECT_DIR/" 2>/dev/null || true
        echo "  ✓ $(basename $file)"
        ((TOTAL_FILES++)) || true
    done

    # CLAUDE.md files
    find "$PROJECT_PATH" -maxdepth 3 -name "CLAUDE.md" -type f 2>/dev/null | while read file; do
        local rel_path=$(dirname "${file#$PROJECT_PATH/}")
        local dest_dir="$PROJECT_DIR/$rel_path"
        mkdir -p "$dest_dir"
        cp "$file" "$dest_dir/" 2>/dev/null || true
        echo "  ✓ CLAUDE.md ($(dirname $rel_path))"
        ((TOTAL_FILES++)) || true
    done

    # Documentation directories (01-Docs, docs/, claudes-docs/)
    for docs_dir in "01-Docs" "docs" "claudes-docs" "documentation"; do
        if [ -d "$PROJECT_PATH/$docs_dir" ]; then
            local dest="$PROJECT_DIR/$docs_dir"
            mkdir -p "$dest"
            find "$PROJECT_PATH/$docs_dir" -name "*.md" -type f 2>/dev/null | while read file; do
                local rel_path="${file#$PROJECT_PATH/$docs_dir/}"
                local file_dest="$dest/$rel_path"
                mkdir -p "$(dirname $file_dest)"
                cp "$file" "$file_dest" 2>/dev/null || true
                echo "  ✓ $docs_dir/$(basename $file)"
                ((TOTAL_FILES++)) || true
            done
        fi
    done

    # Architecture and design docs
    find "$PROJECT_PATH" -maxdepth 2 \( -iname "*architecture*" -o -iname "*design*" -o -iname "*overview*" \) -name "*.md" -type f 2>/dev/null | while read file; do
        cp "$file" "$PROJECT_DIR/" 2>/dev/null || true
        echo "  ✓ $(basename $file)"
        ((TOTAL_FILES++)) || true
    done

    # API documentation
    find "$PROJECT_PATH" -maxdepth 3 -iname "*api*.md" -type f 2>/dev/null | while read file; do
        cp "$file" "$PROJECT_DIR/" 2>/dev/null || true
        echo "  ✓ $(basename $file)"
        ((TOTAL_FILES++)) || true
    done

    # Count files collected for this project
    local PROJECT_FILES=$(find "$PROJECT_DIR" -type f | wc -l)
    echo "  Total files: $PROJECT_FILES"
}

# Collect from all major projects
echo ""
echo "Scanning /home/jeremy/000-projects/..."
echo "============================================="

# Key projects to include
PROJECTS=(
    "/home/jeremy/000-projects/hustle"
    "/home/jeremy/000-projects/ccpiweb"
    "/home/jeremy/000-projects/iams"
    "/home/jeremy/000-projects/diagnostic-platform"
    "/home/jeremy/000-projects/claude-code-plugins"
    "/home/jeremy/000-projects/blog"
    "/home/jeremy/000-projects/intent-solutions-landing"
    "/home/jeremy/000-projects/ai-devops-intent-solutions"
    "/home/jeremy/000-projects/excel-analyst-pro"
    "/home/jeremy/000-projects/hybrid-ai-stack"
    "/home/jeremy/000-projects/local-rag-agent"
    "/home/jeremy/000-projects/n8n-workflows"
)

for project in "${PROJECTS[@]}"; do
    if [ -d "$project" ]; then
        collect_docs "$project"
    fi
done

# Special: Collect from 002-command-bible
if [ -d "/home/jeremy/002-command-bible" ]; then
    echo ""
    echo "Processing: command-bible"
    echo "-----------------------------------"
    mkdir -p "$KNOWLEDGE_BASE_DIR/command-bible"
    find "/home/jeremy/002-command-bible" -name "*.md" -type f 2>/dev/null | while read file; do
        cp "$file" "$KNOWLEDGE_BASE_DIR/command-bible/" 2>/dev/null || true
        echo "  ✓ $(basename $file)"
        ((TOTAL_FILES++)) || true
    done
fi

# Summary
echo ""
echo "============================================="
echo "Collection Complete!"
echo "============================================="
TOTAL_FILES=$(find "$KNOWLEDGE_BASE_DIR" -type f | wc -l)
TOTAL_SIZE=$(du -sh "$KNOWLEDGE_BASE_DIR" | cut -f1)
echo "Total files collected: $TOTAL_FILES"
echo "Total size: $TOTAL_SIZE"
echo "Location: $KNOWLEDGE_BASE_DIR"
echo ""
echo "Next steps:"
echo "1. Review the collected files: ls -la $KNOWLEDGE_BASE_DIR"
echo "2. Upload to GCS: gsutil -m rsync -r -d $KNOWLEDGE_BASE_DIR/ gs://bobs-brain-bob-vertex-agent-rag/knowledge-base/"
echo "3. Run data ingestion: make data-ingestion"
echo "============================================="
