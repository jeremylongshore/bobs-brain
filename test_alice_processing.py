#!/usr/bin/env python3
"""
Test Alice processing tasks from Bob
"""

import time
from google.cloud import firestore
from mock_alice_listener import MockAlice

def test_alice_processing():
    """Test Alice processing tasks"""

    print("🤖 Testing Alice task processing...")

    # Initialize mock Alice
    alice = MockAlice("diagnostic-pro-mvp")

    # Get pending tasks
    pending_tasks = alice._get_pending_tasks(limit=10)

    if pending_tasks:
        print(f"📝 Found {len(pending_tasks)} pending tasks")

        # Process each task
        for task in pending_tasks:
            print(f"\n🔄 Processing task: {task['description']}")
            alice._process_task(task)
            print(f"✅ Task {task['task_id']} completed")
    else:
        print("😴 No pending tasks found")

    # Check final status
    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")
    completed_tasks = list(
        client.collection("shared_context")
        .where("status", "==", "completed")
        .stream()
    )

    print(f"\n📊 Final status: {len(completed_tasks)} completed tasks")

    for task_doc in completed_tasks[-3:]:  # Show last 3
        task_data = task_doc.to_dict()
        print(f"   ✅ {task_data.get('description', 'No description')}")
        print(f"      Result: {task_data.get('result', {}).get('task_type', 'Unknown')}")

if __name__ == "__main__":
    test_alice_processing()
