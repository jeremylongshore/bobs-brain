#!/usr/bin/env python3
"""
Bob Runner - Clean entry point for running Bob agents
"""

import sys
from pathlib import Path

# Add bob package to Python path
sys.path.insert(0, str(Path(__file__).parent))

from bob.core.config import BobConfig
from bob.agents.basic import BobBasic


def main():
    """Run Bob Basic CLI version"""
    try:
        config = BobConfig()
        bob = BobBasic(config)
        bob.run_interactive()
    except ImportError:
        # Fallback to old implementation during transition
        sys.path.insert(0, str(Path(__file__).parent / "agent"))
        from bob_clean import main as old_main
        old_main()


if __name__ == "__main__":
    main()
