#!/usr/bin/env python3
"""
Bob's Firestore integration tools
"""

from google.cloud import firestore
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

class BobFirestoreTools:
    """Bob's tools for Firestore integration"""

    def __init__(self):
        self.firestore_client = firestore.Client(project="diagnostic-pro-mvp", database="bob-brain")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def search_knowledge(self, query: str, limit: int = 5) -> str:
        """Search knowledge in Firestore"""
        try:
            # Simple text-based search for now (can be upgraded to vector search later)
            docs = self.firestore_client.collection("knowledge").limit(20).stream()

            results = []
            for doc in docs:
                data = doc.to_dict()
                content = data.get("content", "")
                if query.lower() in content.lower():
                    results.append(content)
                    if len(results) >= limit:
                        break

            if results:
                return f"Found {len(results)} results:\n" + "\n---\n".join(results[:limit])
            else:
                return f"No results found for '{query}'"

        except Exception as e:
            return f"Error searching knowledge: {str(e)}"

    def get_conversations(self, limit: int = 5) -> str:
        """Get recent conversations"""
        try:
            docs = list(self.firestore_client.collection("bob_conversations").limit(limit).stream())

            if not docs:
                return "No conversations found"

            results = []
            for doc in docs:
                data = doc.to_dict()
                message = data.get("message", "")
                response = data.get("response", "")
                results.append(f"Q: {message}\nA: {response}")

            return f"Recent {len(results)} conversations:\n" + "\n---\n".join(results)

        except Exception as e:
            return f"Error getting conversations: {str(e)}"

    def apply_automation_rules(self, query: str) -> str:
        """Apply automation rules"""
        try:
            docs = list(self.firestore_client.collection("automation_rules").stream())

            for doc in docs:
                rule_data = doc.to_dict()
                trigger = rule_data.get("trigger_condition", "")
                action = rule_data.get("action_type", "")

                if trigger and trigger.lower() in query.lower():
                    return f"Automation rule triggered: {action}"

            return "No applicable automation rules found"

        except Exception as e:
            return f"Error applying automation rules: {str(e)}"

    def get_insights(self, query: str = "") -> str:
        """Get smart insights"""
        try:
            docs = list(self.firestore_client.collection("insights").stream())

            if not docs:
                return "No insights found"

            results = []
            for doc in docs:
                data = doc.to_dict()
                title = data.get("title", "")
                description = data.get("description", "")
                confidence = data.get("confidence", 0.0)

                insight_text = f"**{title}** (Confidence: {confidence:.0%})\n{description}"
                results.append(insight_text)

            return "Smart Insights:\n" + "\n---\n".join(results)

        except Exception as e:
            return f"Error getting insights: {str(e)}"

    def delegate_to_alice(self, task: str, priority: str = "medium", task_type: str = "general") -> str:
        """Delegate task to Alice"""
        try:
            task_data = {
                "agent_from": "bob",
                "agent_to": "alice",
                "task_type": task_type,
                "description": task,
                "priority": priority,
                "status": "pending",
                "created_at": firestore.SERVER_TIMESTAMP,
                "attempts": 0,
                "max_attempts": 3,
                "metadata": {
                    "delegated_by": "bob-firestore-tools",
                    "timestamp": str(firestore.SERVER_TIMESTAMP)
                }
            }

            doc_ref = self.firestore_client.collection("shared_context").add(task_data)
            task_id = doc_ref[1].id

            return f"✅ Task delegated to Alice: {task}\n   Task ID: {task_id}\n   Priority: {priority}"

        except Exception as e:
            return f"Error delegating to Alice: {str(e)}"

def test_bob_tools():
    """Test Bob's Firestore tools"""

    print("🧪 Testing Bob's Firestore tools...")

    tools = BobFirestoreTools()

    # Test search
    print("\n🔍 Testing knowledge search:")
    result = tools.search_knowledge("project")
    print(result[:200] + "..." if len(result) > 200 else result)

    # Test conversations
    print("\n💬 Testing conversations:")
    result = tools.get_conversations(2)
    print(result[:200] + "..." if len(result) > 200 else result)

    # Test insights
    print("\n🧠 Testing insights:")
    result = tools.get_insights()
    print(result[:300] + "..." if len(result) > 300 else result)

    # Test task delegation
    print("\n🚀 Testing task delegation:")
    result = tools.delegate_to_alice("Test automated deployment monitoring", "high", "deployment")
    print(result)

    print("\n✅ Bob tools test complete!")

if __name__ == "__main__":
    test_bob_tools()
