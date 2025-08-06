#!/usr/bin/env python3
"""
Bob Basic - Clean, Efficient Personal Brain Assistant
Simple architecture that actually works
"""

import json
import sqlite3
import chromadb
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class BobBasic:
    """Bob Basic - Your personal brain assistant"""

    def __init__(self):
        """Initialize Bob with existing knowledge and models"""
        self.home_dir = Path.home() / ".bob_brain"
        self.db_path = self.home_dir / "bob_memory.db"

        # Initialize components
        self._setup_database()
        self._setup_knowledge()
        self._setup_models()

        # Conversation context
        self.context_window = []
        self.max_context = 5

        logger.info("🧠 Bob Basic initialized!")
        logger.info(f"📚 Knowledge items: {self._count_knowledge()}")
        logger.info("🤖 Models: Gemma 2B (fast) | Mistral 7B (smart) | Qwen 14B (code)")

    def _setup_database(self):
        """Setup SQLite for conversation memory"""
        self.home_dir.mkdir(exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    message TEXT,
                    response TEXT,
                    model_used TEXT,
                    context_used TEXT
                )
            """)

    def _setup_knowledge(self):
        """Connect to existing ChromaDB knowledge base"""
        try:
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.home_dir / "chroma")
            )
            self.knowledge = self.chroma_client.get_collection("bob_knowledge")
            logger.info("✅ Connected to existing knowledge base")
        except Exception as e:
            logger.error(f"❌ Knowledge base error: {e}")
            self.knowledge = None

    def _setup_models(self):
        """Setup model routing for 16GB RAM optimization"""
        self.models = {
            "fast": "gemma:2b",      # 1.7GB - Quick responses
            "smart": "mistral:7b",    # 4.4GB - Complex reasoning
            "code": "qwen2.5-coder:14b"  # 9GB - Code generation
        }

        # Test Ollama connection
        self.ollama_url = "http://localhost:11434/api/generate"
        if not self._test_ollama():
            logger.warning("⚠️ Ollama not responding - start with: ollama serve")

    def _test_ollama(self) -> bool:
        """Test if Ollama is running"""
        try:
            response = requests.post(
                self.ollama_url,
                json={"model": "gemma:2b", "prompt": "test", "stream": False},
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def _count_knowledge(self) -> int:
        """Count knowledge items"""
        try:
            return self.knowledge.count() if self.knowledge else 0
        except:
            return 0

    def _route_model(self, message: str) -> str:
        """Smart routing to best model for the task"""
        message_lower = message.lower()

        # Quick responses for simple queries
        if len(message) < 50 and "?" in message:
            return self.models["fast"]

        # Code-related queries
        if any(word in message_lower for word in ["code", "implement", "function", "debug", "error"]):
            return self.models["code"]

        # Complex reasoning
        return self.models["smart"]

    def _search_knowledge(self, query: str, n_results: int = 3) -> List[str]:
        """Search ChromaDB for relevant knowledge"""
        if not self.knowledge:
            return []

        try:
            results = self.knowledge.query(
                query_texts=[query],
                n_results=n_results
            )

            if results and results['documents']:
                return results['documents'][0]
            return []
        except Exception as e:
            logger.error(f"Knowledge search error: {e}")
            return []

    def _generate_response(self, prompt: str, model: str, timeout: int = 60) -> str:
        """Generate response using Ollama"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                },
                timeout=timeout
            )

            if response.status_code == 200:
                return response.json().get('response', 'No response generated')
            else:
                return f"Error: Model {model} returned status {response.status_code}"

        except requests.Timeout:
            return "Response timeout - try a simpler question or use 'fast' mode"
        except Exception as e:
            return f"Generation error: {e}"

    def _build_prompt(self, message: str, context: List[str]) -> str:
        """Build prompt with context"""
        prompt_parts = []

        # System context
        prompt_parts.append("""You are Bob, a helpful AI assistant with knowledge about:
- DiagnosticPro (Live at https://diagnosticpro-mvp-970547573997.us-central1.run.app)
- Using secure API key ending in ...c3a6 (old key ...6535 is disabled)
- Jeremy's projects and preferences
- Technical topics and coding

Be concise and helpful.""")

        # Add relevant knowledge
        if context:
            prompt_parts.append("\nRelevant knowledge:")
            for i, ctx in enumerate(context[:3], 1):
                prompt_parts.append(f"{i}. {ctx[:200]}...")

        # Add conversation history
        if self.context_window:
            prompt_parts.append("\nRecent conversation:")
            for prev_msg, prev_resp in self.context_window[-2:]:
                prompt_parts.append(f"User: {prev_msg}")
                prompt_parts.append(f"Bob: {prev_resp[:100]}...")

        # Add current message
        prompt_parts.append(f"\nUser: {message}")
        prompt_parts.append("\nBob:")

        return "\n".join(prompt_parts)

    def _save_conversation(self, message: str, response: str, model: str, context: List[str]):
        """Save conversation to database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO conversations (timestamp, message, response, model_used, context_used)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    datetime.now().isoformat(),
                    message,
                    response,
                    model,
                    json.dumps(context[:2]) if context else "[]"
                ))
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    def chat(self, message: str, force_model: Optional[str] = None) -> str:
        """Main chat interface"""
        logger.info(f"\n💬 You: {message}")

        # Search for relevant knowledge
        context = self._search_knowledge(message)

        # Route to best model
        if force_model and force_model in self.models:
            model = self.models[force_model]
            logger.info(f"🎯 Using forced model: {model}")
        else:
            model = self._route_model(message)
            logger.info(f"🎯 Routed to: {model}")

        # Build prompt with context
        prompt = self._build_prompt(message, context)

        # Generate response
        logger.info("🤔 Thinking...")
        response = self._generate_response(prompt, model)

        # Update context window
        self.context_window.append((message, response))
        if len(self.context_window) > self.max_context:
            self.context_window.pop(0)

        # Save to database
        self._save_conversation(message, response, model, context)

        logger.info(f"🤖 Bob: {response}")
        return response

    def search(self, query: str, n_results: int = 5) -> List[str]:
        """Direct knowledge search"""
        results = self._search_knowledge(query, n_results)
        logger.info(f"🔍 Found {len(results)} results for: {query}")
        for i, result in enumerate(results, 1):
            logger.info(f"{i}. {result[:150]}...")
        return results

    def remember(self, information: str, category: str = "general") -> bool:
        """Add new information to knowledge base"""
        if not self.knowledge:
            logger.error("❌ Knowledge base not available")
            return False

        try:
            doc_id = f"bob_memory_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.knowledge.add(
                documents=[information],
                metadatas=[{
                    "source": "bob_conversation",
                    "category": category,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[doc_id]
            )
            logger.info(f"✅ Remembered: {information[:100]}...")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to remember: {e}")
            return False

    def status(self) -> Dict:
        """Get Bob's current status"""
        status = {
            "knowledge_items": self._count_knowledge(),
            "conversations": len(self.context_window),
            "models_available": list(self.models.keys()),
            "ollama_running": self._test_ollama()
        }

        logger.info("\n📊 Bob Status:")
        logger.info(f"  Knowledge: {status['knowledge_items']} items")
        logger.info(f"  Context: {status['conversations']} recent conversations")
        logger.info(f"  Models: {', '.join(status['models_available'])}")
        logger.info(f"  Ollama: {'✅ Running' if status['ollama_running'] else '❌ Not running'}")

        return status


def main():
    """Interactive Bob session"""
    print("\n" + "=" * 60)
    print("🧠 BOB BASIC - Personal Brain Assistant")
    print("=" * 60)

    bob = BobBasic()

    print("\n💡 Commands:")
    print("  'fast', 'smart', 'code' - Force specific model")
    print("  'search <query>' - Search knowledge base")
    print("  'remember <info>' - Store new information")
    print("  'status' - Show Bob's status")
    print("  'exit' - End session")
    print("\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("👋 Goodbye!")
                break

            elif user_input.lower() == "status":
                bob.status()

            elif user_input.lower().startswith("search "):
                query = user_input[7:]
                bob.search(query)

            elif user_input.lower().startswith("remember "):
                info = user_input[9:]
                bob.remember(info)

            else:
                # Check for forced model
                force_model = None
                if user_input.lower().startswith(("fast ", "smart ", "code ")):
                    parts = user_input.split(" ", 1)
                    force_model = parts[0].lower()
                    user_input = parts[1] if len(parts) > 1 else ""

                if user_input:
                    bob.chat(user_input, force_model)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
