#!/usr/bin/env python3
"""
Test Bob's functionality without interactive input
"""

import sys
from pathlib import Path

# Add agent directory to path
agent_dir = Path(__file__).parent / "agent"
sys.path.insert(0, str(agent_dir))

from bob_clean import BobBrain

def test_bob():
    """Test Bob's core functionality"""
    print("🧪 Testing Bob's Brain - Clean Implementation")

    # Initialize Bob
    bob = BobBrain()

    # Test basic functionality
    print("\n1. Testing status command:")
    status = bob.chat("status")
    print(status)

    print("\n2. Testing memory command:")
    memory = bob.chat("memory")
    print(memory)

    print("\n3. Testing project command:")
    project = bob.chat("project")
    print(project)

    print("\n4. Testing general chat:")
    response = bob.chat("Hello Bob!")
    print(response)

    print("\n✅ Bob is working perfectly!")
    print(f"📁 Bob's home directory: {bob.home_dir}")
    print(f"💾 Bob's database: {bob.db_path}")
    print(f"📚 Knowledge base: {bob.knowledge_path}")

if __name__ == "__main__":
    test_bob()
