#!/usr/bin/env python3
"""
Clear Firestore slack_events cache to allow testing with fresh events.
"""
from google.cloud import firestore

PROJECT_ID = "bobs-brain"

def clear_slack_events():
    """Delete all documents in slack_events collection."""
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection('slack_events')

    # Get all documents
    docs = collection_ref.stream()

    count = 0
    for doc in docs:
        print(f"Deleting event: {doc.id}")
        doc.reference.delete()
        count += 1

    print(f"\n✅ Cleared {count} events from Firestore cache")
    return count

if __name__ == "__main__":
    print("Clearing Firestore slack_events cache...")
    clear_slack_events()
