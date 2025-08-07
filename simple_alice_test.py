#!/usr/bin/env python3
"""
Simple Alice test with basic Firestore queries
"""

from google.cloud import firestore
import time
import random

def simple_alice_test():
    """Test Alice with simple queries"""

    print("🤖 Testing Alice with simple Firestore queries...")

    client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")

    # Get all documents from shared_context (simple query)
    print("📝 Checking shared_context collection...")

    all_tasks = list(client.collection("shared_context").stream())
    print(f"   Total tasks: {len(all_tasks)}")

    # Process pending tasks
    processed_count = 0

    for task_doc in all_tasks:
        task_data = task_doc.to_dict()

        # Check if pending
        if task_data.get("status") == "pending":
            print(f"\n🔄 Processing task: {task_data.get('description', 'No description')}")

            # Simulate processing
            time.sleep(random.uniform(1, 3))

            # Mock result
            result = {
                "task_type": task_data.get("task_type", "unknown"),
                "status": "completed",
                "processed_by": "mock_alice",
                "processing_time": random.uniform(2, 8),
                "mock_result": f"Successfully processed {task_data.get('task_type', 'task')}"
            }

            # Update task status
            try:
                task_doc.reference.update({
                    "status": "completed",
                    "completed_at": firestore.SERVER_TIMESTAMP,
                    "result": result,
                    "processed_by": "mock_alice"
                })

                print(f"   ✅ Task completed: {result['mock_result']}")
                processed_count += 1

            except Exception as e:
                print(f"   ❌ Error updating task: {e}")

    print(f"\n📊 Processing complete: {processed_count} tasks processed")

    # Show completed tasks
    if processed_count > 0:
        print("\n✅ Completed tasks:")
        completed_tasks = [doc for doc in all_tasks
                          if doc.to_dict().get("status") == "completed"]

        for task_doc in completed_tasks:
            task_data = task_doc.to_dict()
            description = task_data.get("description", "No description")
            result_type = task_data.get("result", {}).get("task_type", "unknown")
            print(f"   - {description} ({result_type})")

if __name__ == "__main__":
    simple_alice_test()
