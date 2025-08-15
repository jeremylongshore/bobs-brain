#!/bin/bash
# Start Bob Ferrari with all necessary environment setup

echo "🏎️ Starting Bob Ferrari - Holistic AI Assistant"
echo "================================================"

# Check for .env file
if [ ! -f .env ]; then
    echo "❌ ERROR: .env file not found!"
    echo "Please create .env file with your credentials:"
    echo "  cp .env.example .env"
    echo "  nano .env  # Add your actual credentials"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    exit 1
fi

# Check dependencies
echo "📦 Checking dependencies..."
pip3 install -q -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p chroma_db

# Start Bob Ferrari
echo "🚀 Launching Bob Ferrari..."
echo "Press Ctrl+C to stop"
echo ""

python3 bob_ferrari.py