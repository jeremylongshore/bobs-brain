#!/usr/bin/env python3
"""
Simple launcher for our clean Bob
"""

import sys
import os
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent / "agent"
sys.path.insert(0, str(agent_dir))

from bob_clean import main

if __name__ == "__main__":
    main()
