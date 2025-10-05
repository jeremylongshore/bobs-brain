#!/bin/bash
# Start Bob's Brain Unified Bot

echo "🤖 Starting Bob's Brain..."

# Navigate to Bob's directory
cd /home/jeremylongshore/bob-consolidation

# Check for virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update requirements
echo "Installing requirements..."
pip install -q -r requirements.txt

# Export environment variables
export $(cat .env | grep -v '^#' | xargs)

# Start Bob
echo "Starting Bob on port ${PORT:-5000}..."
python src/bob_unified_v2.py