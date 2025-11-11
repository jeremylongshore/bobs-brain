#!/bin/bash
# Bob Unified v2 Startup Script - Enhanced Communication Edition

SCRIPT_NAME="Bob Unified v2 Startup"
SCRIPT_VERSION="2.0.0"
BOB_HOME="/home/jeremylongshore/bob-consolidation"
LOG_DIR="$BOB_HOME/logs"
BACKUP_DIR="$BOB_HOME/backup"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🤖 $SCRIPT_NAME v$SCRIPT_VERSION${NC}"
echo -e "${BLUE}Enhanced with: Duplicate prevention, Smart memory, Professional communication${NC}"
echo -e "${BLUE}===============================================================${NC}"

log_info() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

log_warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Setup directories
log_info "Setting up directories..."
mkdir -p "$LOG_DIR"

# Load Slack tokens from secure backup
TOKENS_FILE="$BACKUP_DIR/bob_backup_*/slack_tokens.env"
if ls $TOKENS_FILE 1> /dev/null 2>&1; then
    LATEST_BACKUP=$(ls -t $TOKENS_FILE | head -1)
    log_info "Loading Slack tokens from: $LATEST_BACKUP"
    source "$LATEST_BACKUP"
    
    if [ -z "$SLACK_BOT_TOKEN" ] || [ -z "$SLACK_APP_TOKEN" ]; then
        log_error "Slack tokens not properly loaded from backup"
        exit 1
    fi
    
    export SLACK_BOT_TOKEN
    export SLACK_APP_TOKEN
    log_info "✅ Slack tokens loaded successfully"
else
    log_error "Slack tokens backup not found"
    exit 1
fi

# Verify ChromaDB knowledge base
CHROMA_PATH="/home/jeremylongshore/.bob_brain/chroma"
if [ ! -d "$CHROMA_PATH" ]; then
    log_error "ChromaDB knowledge base not found at $CHROMA_PATH"
    exit 1
fi

CHROMA_FILES=$(find "$CHROMA_PATH" -name "*.sqlite*" -o -name "data_level*" | wc -l)
log_info "✅ ChromaDB knowledge base found ($CHROMA_FILES files)"

# Check for existing Bob processes
EXISTING_BOB=$(ps aux | grep "bob_unified" | grep -v grep | wc -l)
if [ $EXISTING_BOB -gt 0 ]; then
    log_warn "⚠️  Existing Bob process detected - will be replaced"
    ps aux | grep "bob_unified" | grep -v grep
fi

# Verify enhanced Bob script exists
BOB_SCRIPT="$BOB_HOME/src/bob_unified_v2.py"
if [ ! -f "$BOB_SCRIPT" ]; then
    log_error "Bob unified v2 script not found: $BOB_SCRIPT"
    exit 1
fi

# Pre-flight checks
python3 -c "import slack_sdk, chromadb" 2>/dev/null
if [ $? -ne 0 ]; then
    log_error "Required Python dependencies not installed"
    exit 1
fi

log_info "✅ All pre-flight checks passed for Bob v2"
log_info "🚀 Launching Bob Unified v2 (Enhanced Communication Edition)..."

# Change to Bob home directory
cd "$BOB_HOME"

# Start enhanced Bob
exec python3 "$BOB_SCRIPT" 2>&1 | tee -a "$LOG_DIR/bob_v2_startup_$(date +%Y%m%d_%H%M%S).log"