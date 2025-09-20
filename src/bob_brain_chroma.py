#!/usr/bin/env python3
"""
BOB BRAIN v6.0 - ChromaDB Edition
Local AI assistant with vector memory, no cloud dependencies
"""

import asyncio
import hashlib
import json
import logging
import os
import sqlite3
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional

import chromadb
import google.generativeai as genai
from flask import Flask, jsonify, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bob_brain.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BobBrainChroma:
    """
    Bob's Brain with ChromaDB vector memory and local SQLite storage
    No cloud dependencies required for basic operation
    """

    def __init__(self):
        self.app = Flask(__name__)
        self.executor = ThreadPoolExecutor(max_workers=4)

        # Initialize ChromaDB for vector memory
        self.chroma_client = None
        self.conversations = None
        self.knowledge_base = None

        # Initialize SQLite for structured data
        self.sqlite_db = None

        # Initialize AI and Slack
        self.genai_client = None
        self.slack_client = None

        # Setup all components
        self._setup_chromadb()
        self._setup_sqlite()
        self._setup_genai()
        self._setup_slack()
        self._setup_routes()

        logger.info("🧠 Bob's Brain v6.0 (ChromaDB Edition) initialized")

    def _setup_chromadb(self):
        """Initialize ChromaDB for vector memory"""
        try:
            # Create persistent ChromaDB client
            self.chroma_client = chromadb.PersistentClient(path="./bob_memory_chroma")

            # Create collections for different types of memory
            self.conversations = self.chroma_client.get_or_create_collection(
                name="conversations",
                metadata={"description": "User conversations with semantic search"}
            )

            self.knowledge_base = self.chroma_client.get_or_create_collection(
                name="knowledge_base",
                metadata={"description": "Equipment repair knowledge and solutions"}
            )

            logger.info("✅ ChromaDB vector memory initialized")

        except Exception as e:
            logger.error(f"❌ ChromaDB initialization failed: {e}")
            self.chroma_client = None

    def _setup_sqlite(self):
        """Initialize SQLite for structured data"""
        try:
            self.sqlite_db = sqlite3.connect("bob_data.db", check_same_thread=False)
            self.sqlite_db.row_factory = sqlite3.Row

            # Create tables for user data and metadata
            cursor = self.sqlite_db.cursor()

            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    preferences TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Learning metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS learning_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_name TEXT,
                    metric_value REAL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Corrections table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS corrections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    original_response TEXT,
                    correction TEXT,
                    context TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            self.sqlite_db.commit()
            logger.info("✅ SQLite database initialized")

        except Exception as e:
            logger.error(f"❌ SQLite initialization failed: {e}")
            self.sqlite_db = None

    def _setup_genai(self):
        """Initialize Google Generative AI"""
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.genai_client = genai.GenerativeModel('gemini-2.0-flash-exp')
                logger.info("✅ Google Generative AI initialized")
            else:
                logger.warning("⚠️ No GOOGLE_API_KEY found - AI responses disabled")

        except Exception as e:
            logger.error(f"❌ Google Gen AI initialization failed: {e}")
            self.genai_client = None

    def _setup_slack(self):
        """Initialize Slack client"""
        try:
            slack_token = os.getenv('SLACK_BOT_TOKEN')
            if slack_token:
                self.slack_client = WebClient(token=slack_token)
                logger.info("✅ Slack client initialized")
            else:
                logger.warning("⚠️ No SLACK_BOT_TOKEN found - Slack disabled")

        except Exception as e:
            logger.error(f"❌ Slack initialization failed: {e}")
            self.slack_client = None

    def store_conversation(self, user: str, message: str, response: str):
        """Store conversation in ChromaDB with vector embeddings"""
        if not self.conversations:
            return False

        try:
            conversation_id = hashlib.md5(f"{user}{message}{datetime.now()}".encode(), usedforsecurity=False).hexdigest()

            # Store in ChromaDB with automatic embeddings
            self.conversations.add(
                documents=[f"User: {message}\nBob: {response}"],
                metadatas=[{
                    "user": user,
                    "timestamp": datetime.now().isoformat(),
                    "message_type": "conversation"
                }],
                ids=[conversation_id]
            )

            logger.info(f"💾 Stored conversation for {user}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to store conversation: {e}")
            return False

    def search_memory(self, query: str, user: str = None, limit: int = 5) -> List[Dict]:
        """Search conversation memory using semantic similarity"""
        if not self.conversations:
            return []

        try:
            # Build metadata filter
            where = {}
            if user:
                where["user"] = user

            # Semantic search in ChromaDB
            results = self.conversations.query(
                query_texts=[query],
                n_results=limit,
                where=where if where else None
            )

            memory_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    memory_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })

            return memory_results

        except Exception as e:
            logger.error(f"❌ Memory search failed: {e}")
            return []

    def store_knowledge(self, title: str, content: str, source: str = "manual"):
        """Store knowledge in ChromaDB knowledge base"""
        if not self.knowledge_base:
            return False

        try:
            knowledge_id = hashlib.md5(f"{title}{content}".encode(), usedforsecurity=False).hexdigest()

            self.knowledge_base.add(
                documents=[content],
                metadatas=[{
                    "title": title,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[knowledge_id]
            )

            logger.info(f"📚 Stored knowledge: {title}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to store knowledge: {e}")
            return False

    def search_knowledge(self, query: str, limit: int = 3) -> List[Dict]:
        """Search knowledge base using semantic similarity"""
        if not self.knowledge_base:
            return []

        try:
            results = self.knowledge_base.query(
                query_texts=[query],
                n_results=limit
            )

            knowledge_results = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    knowledge_results.append({
                        "content": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results['distances'] else 0
                    })

            return knowledge_results

        except Exception as e:
            logger.error(f"❌ Knowledge search failed: {e}")
            return []

    def store_correction(self, user: str, original: str, correction: str, context: str):
        """Store user correction in SQLite for learning"""
        if not self.sqlite_db:
            return False

        try:
            cursor = self.sqlite_db.cursor()
            cursor.execute("""
                INSERT INTO corrections (user_id, original_response, correction, context)
                VALUES (?, ?, ?, ?)
            """, (user, original, correction, context))
            self.sqlite_db.commit()

            logger.info(f"📝 Stored correction from {user}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to store correction: {e}")
            return False

    async def generate_response(self, user_message: str, user: str = "user") -> str:
        """Generate AI response with memory context"""
        try:
            # Search memory for relevant context
            memory_context = self.search_memory(user_message, user, limit=3)
            knowledge_context = self.search_knowledge(user_message, limit=2)

            # Build context for AI
            context_parts = []

            if memory_context:
                context_parts.append("Previous relevant conversations:")
                for mem in memory_context:
                    context_parts.append(f"- {mem['content'][:200]}...")

            if knowledge_context:
                context_parts.append("Relevant knowledge:")
                for kb in knowledge_context:
                    context_parts.append(f"- {kb['content'][:200]}...")

            # Create prompt with context
            full_context = "\n".join(context_parts) if context_parts else "No previous context available."

            prompt = f"""You are Bob, Jeremy's AI assistant. You have persistent memory and learn from conversations.

Context from previous interactions:
{full_context}

User message: {user_message}

Respond as Bob with:
1. Acknowledge relevant context if applicable
2. Provide helpful, detailed response
3. Remember this conversation for future reference
"""

            if self.genai_client:
                response = await asyncio.get_event_loop().run_in_executor(
                    self.executor,
                    lambda: self.genai_client.generate_content(prompt).text
                )

                # Store this conversation
                self.store_conversation(user, user_message, response)

                return response
            else:
                fallback_response = f"I heard you say: '{user_message}'. My AI is currently offline, but I've stored this in memory."
                self.store_conversation(user, user_message, fallback_response)
                return fallback_response

        except Exception as e:
            logger.error(f"❌ Response generation failed: {e}")
            return f"Sorry, I encountered an error: {str(e)[:100]}"

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route('/health', methods=['GET'])
        def health():
            status = {
                "status": "healthy",
                "chromadb": bool(self.chroma_client),
                "sqlite": bool(self.sqlite_db),
                "genai": bool(self.genai_client),
                "slack": bool(self.slack_client),
                "timestamp": datetime.now().isoformat()
            }
            return jsonify(status)

        @self.app.route('/test', methods=['POST'])
        def test():
            data = request.json
            message = data.get('message', 'Hello Bob!')

            # Run async response generation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(
                self.generate_response(message, "test_user")
            )
            loop.close()

            return jsonify({
                "message": message,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })

        @self.app.route('/memory/search', methods=['POST'])
        def search_memory_endpoint():
            data = request.json
            query = data.get('query', '')
            user = data.get('user')
            limit = data.get('limit', 5)

            results = self.search_memory(query, user, limit)

            return jsonify({
                "query": query,
                "results": results,
                "count": len(results)
            })

        @self.app.route('/knowledge/add', methods=['POST'])
        def add_knowledge():
            data = request.json
            title = data.get('title', '')
            content = data.get('content', '')
            source = data.get('source', 'manual')

            success = self.store_knowledge(title, content, source)

            return jsonify({
                "success": success,
                "title": title,
                "source": source
            })

        @self.app.route('/slack/events', methods=['POST'])
        def slack_events():
            data = request.json

            # Handle Slack URL verification
            if data.get('type') == 'url_verification':
                return jsonify({'challenge': data.get('challenge')})

            # Handle Slack events
            if data.get('type') == 'event_callback':
                event = data.get('event', {})

                if event.get('type') == 'message' and not event.get('bot_id'):
                    user = event.get('user')
                    text = event.get('text', '')
                    channel = event.get('channel')

                    # Generate response
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    response = loop.run_until_complete(
                        self.generate_response(text, user)
                    )
                    loop.close()

                    # Send to Slack
                    if self.slack_client:
                        try:
                            self.slack_client.chat_postMessage(
                                channel=channel,
                                text=response
                            )
                        except SlackApiError as e:
                            logger.error(f"Slack error: {e}")

            return jsonify({'status': 'ok'})

def main():
    """Main entry point"""
    bob = BobBrainChroma()

    # Add some initial knowledge
    bob.store_knowledge(
        "Bob Introduction",
        "I am Bob, Jeremy's AI assistant. I have persistent memory using ChromaDB and can help with technical questions, equipment repair, and general assistance.",
        "system"
    )

    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 Starting Bob's Brain v6.0 on port {port}")
    bob.app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()