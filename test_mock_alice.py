#!/usr/bin/env python3
"""
Test mock Alice listener
"""

from google.cloud import firestore
import time
from datetime import datetime

def create_test_task():
    """Create a test task for Alice"""

    print("🚀 Creating test task for Alice...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Create a test task
    task_data = {
        "agent_from": "bob",
        "agent_to": "alice",
        "task_type": "gcp_monitoring",
        "description": "Check health of bob-brain Firestore database",
        "priority": "medium",
        "metadata": {
            "service": "firestore",
            "database": "bob-brain"
        },
        "status": "pending",
        "created_at": firestore.SERVER_TIMESTAMP,
        "attempts": 0,
        "max_attempts": 3
    }

    # Add to shared_context collection
    doc_ref = client.collection("shared_context").add(task_data)
    task_id = doc_ref[1].id

    print(f"✅ Created test task: {task_id}")
    return task_id

def test_task_delegation():
    """Test Bob's task delegation to Alice"""

    print("🧪 Testing Bob -> Alice task delegation...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Create task
    task_id = create_test_task()

    # Wait a moment
    time.sleep(2)

    # Check if task exists
    task_doc = client.collection("shared_context").document(task_id).get()
    if task_doc.exists:
        task_data = task_doc.to_dict()
        print(f"✅ Task exists: {task_data['description']}")
        print(f"   Status: {task_data['status']}")
        return True
    else:
        print("❌ Task not found")
        return False

if __name__ == "__main__":
    success = test_task_delegation()
    if success:
        print("🎉 Task delegation test passed!")
        print("\n📋 Next steps:")
        print("1. Run: python3 mock_alice_listener.py")
        print("2. In another terminal, create more tasks to test")
    else:
        print("❌ Task delegation test failed")
