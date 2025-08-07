#!/usr/bin/env python3
"""
Test Firestore connectivity and permissions
"""

from google.cloud import firestore
import json

def test_firestore():
    """Test Firestore connection and basic operations"""

    print("🧪 Testing Firestore connectivity...")

    try:
        # Initialize client
        client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")
        print("✅ Firestore client initialized")

        # Test write operation
        test_doc = {
            "test": "data",
            "timestamp": firestore.SERVER_TIMESTAMP
        }

        doc_ref = client.collection("test_collection").document("test_doc")
        doc_ref.set(test_doc)
        print("✅ Test write successful")

        # Test read operation
        doc = doc_ref.get()
        if doc.exists:
            print("✅ Test read successful")
            print(f"   Data: {doc.to_dict()}")
        else:
            print("❌ Test read failed - document not found")
            return False

        # Clean up test document
        doc_ref.delete()
        print("✅ Test cleanup successful")

        return True

    except Exception as e:
        print(f"❌ Firestore test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_firestore()
    if success:
        print("🎉 Firestore is ready!")
    else:
        print("⚠️  Firestore test failed")
