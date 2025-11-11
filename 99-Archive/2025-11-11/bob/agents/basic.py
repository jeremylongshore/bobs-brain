#!/usr/bin/env python3
"""
Bob Basic Agent - CLI Implementation
Clean development version of Bob
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class BobBasic:
    """Bob's core brain - clean and focused"""

    def __init__(self):
        self.home_dir = Path.home() / ".bob_brain"
        self.db_path = self.home_dir / "bob_memory.db"
        self.knowledge_path = Path(__file__).parent.parent / "data" / "knowledge_base"
        self._setup_directories()
        self._setup_database()
        self._load_jeremy_context()

    def _setup_directories(self):
        """Setup Bob's directory structure"""
        self.home_dir.mkdir(exist_ok=True)
        (self.home_dir / "logs").mkdir(exist_ok=True)
        (self.home_dir / "temp").mkdir(exist_ok=True)

    def _setup_database(self):
        """Setup Bob's memory database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    message TEXT,
                    response TEXT,
                    context TEXT
                )
            """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jeremy_context (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at TEXT
                )
            """
            )

    def _load_jeremy_context(self):
        """Load Jeremy's context from knowledge base"""
        master_save = self.knowledge_path / "BOBS_BRAIN_MASTER_SAVE.json"
        if master_save.exists():
            with open(master_save) as f:
                self.jeremy_context = json.load(f)
        else:
            self.jeremy_context = {}

    def remember_conversation(self, message: str, response: str, context: dict = None):
        """Store conversation in memory"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO conversations (timestamp, message, response, context)
                VALUES (?, ?, ?, ?)
            """,
                (
                    datetime.now().isoformat(),
                    message,
                    response,
                    json.dumps(context or {}),
                ),
            )

    def get_recent_conversations(self, limit: int = 10) -> List[Dict]:
        """Get recent conversations"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT timestamp, message, response, context
                FROM conversations
                ORDER BY id DESC
                LIMIT ?
            """,
                (limit,),
            )
            return [
                {
                    "timestamp": row[0],
                    "message": row[1],
                    "response": row[2],
                    "context": json.loads(row[3] or "{}"),
                }
                for row in cursor.fetchall()
            ]

    def chat(self, message: str) -> str:
        """Simple chat interface"""
        print(f"🧠 Bob: Processing '{message}'")

        # Basic responses based on Jeremy's context
        if "status" in message.lower():
            return self._get_status()
        elif "memory" in message.lower():
            return self._get_memory_summary()
        elif "project" in message.lower():
            return self._get_project_info()
        else:
            response = (
                f"I understand you said: {message}\nHow can I help with your projects?"
            )
            self.remember_conversation(message, response)
            return response

    def _get_status(self) -> str:
        """Get Bob's current status"""
        conv_count = len(self.get_recent_conversations(100))
        return f"""
🤖 Bob's Status:
- Memory: {conv_count} conversations stored
- Knowledge Base: {len(self.jeremy_context)} context items loaded
- Projects: DiagnosticPro, Bob's House AI
- Location: {self.home_dir}
- Ready to help with your repair industry vision!
        """.strip()

    def _get_memory_summary(self) -> str:
        """Get memory summary"""
        recent = self.get_recent_conversations(5)
        if not recent:
            return "No conversations in memory yet."

        summary = "📝 Recent Memory:\n"
        for conv in recent[:3]:
            summary += f"- {conv['timestamp'][:16]}: {conv['message'][:50]}...\n"
        return summary

    def _get_project_info(self) -> str:
        """Get project information"""
        if "current_projects" in self.jeremy_context:
            projects = self.jeremy_context["current_projects"]
            info = "🚀 Current Projects:\n"
            for name, details in projects.items():
                info += f"- {name}: {details.get('status', 'Unknown status')}\n"
            return info
        return "Project information loading..."


def main():
    """Main Bob interface"""
    print("🧠 Bob's Brain - Clean Implementation")
    print("The ONE Bob we've been working on together")
    print("Type 'exit' to quit, 'status' for info")

    bob = BobBrain()

    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("👋 Bob: See you later!")
                break

            if user_input:
                response = bob.chat(user_input)
                print(f"\n🤖 Bob: {response}")

        except KeyboardInterrupt:
            print("\n👋 Bob: Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
