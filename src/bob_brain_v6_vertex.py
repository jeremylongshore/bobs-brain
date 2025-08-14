#!/usr/bin/env python3
"""
BOB BRAIN v6.0 - VERTEX AI GEMINI INTEGRATION
Complete Circle of Life with proper Vertex AI Gemini
This version uses GCP's Vertex AI for Gemini access
"""

import asyncio
import hashlib
import json
import logging
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional

import pytz

# Vertex AI imports for Gemini
import vertexai
from flask import Flask, jsonify, request
from google.cloud import bigquery, datastore

# Neo4j for Graphiti
from neo4j import GraphDatabase
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from vertexai.generative_models import Content, GenerativeModel, Part

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)


class BobBrainVertex:
    """Bob's Brain with Vertex AI Gemini integration"""

    def __init__(self):
        """Initialize Bob with Vertex AI"""

        # Core configuration
        self.project_id = os.environ.get("GCP_PROJECT", "bobs-house-ai")
        # Use us-east4 where Gemini models are available
        self.location = os.environ.get("GCP_LOCATION", "us-east4")
        self.user_id = "jeremy"

        # Set timezone
        self.timezone = pytz.timezone("America/Chicago")

        logger.info("=" * 60)
        logger.info("🧠 BOB BRAIN v6.0 - VERTEX AI GEMINI")
        logger.info(f"📍 Project: {self.project_id}")
        logger.info(f"📅 Current Time: {self.get_current_time()}")
        logger.info("=" * 60)

        # Initialize all components
        self._init_vertex_gemini()
        self._init_graphiti()
        self._init_bigquery()
        self._init_datastore()
        self._init_circle_of_life()
        self._init_slack()

        # Memory and context
        self.conversation_history = []
        self.max_history = 20
        self.processed_events = set()
        self.max_events = 1000

        # Thread pool
        self.executor = ThreadPoolExecutor(max_workers=3)

        logger.info("✅ BOB BRAIN v6.0 READY WITH VERTEX AI!")
        logger.info("🔄 Circle of Life Active")
        logger.info("=" * 60)

    def get_current_time(self):
        """Get current date and time"""
        now = datetime.now(self.timezone)
        return now.strftime("%A, %B %d, %Y at %I:%M %p %Z")

    def get_current_date(self):
        """Get current date"""
        now = datetime.now(self.timezone)
        return now.strftime("%Y-%m-%d")

    def _init_vertex_gemini(self):
        """Initialize Vertex AI Gemini"""
        try:
            # Initialize Vertex AI
            vertexai.init(project=self.project_id, location=self.location)

            # Use correct Vertex AI model names
            model_names = [
                "gemini-1.5-flash",  # Latest flash model
                "gemini-1.5-pro",  # Latest pro model
                "gemini-pro",  # Stable version
                "gemini-pro-vision",  # Vision-capable model
            ]

            self.model = None
            self.model_name = None

            for model_name in model_names:
                try:
                    logger.info(f"Trying model: {model_name}")
                    model = GenerativeModel(model_name)

                    # Test the model
                    response = model.generate_content("Say 'Bob is ready' if you work")

                    if response and response.text:
                        logger.info(f"✅ Vertex AI Gemini ready: {model_name}")
                        logger.info(f"   Response: {response.text[:100]}")
                        self.model = model
                        self.model_name = model_name
                        self.gemini_available = True
                        break

                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {str(e)[:100]}")
                    continue

            if not self.model:
                logger.error("❌ No Vertex AI models available")
                self.gemini_available = False

        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {e}")
            logger.error(traceback.format_exc())
            self.model = None
            self.gemini_available = False

    def _init_graphiti(self):
        """Initialize Graphiti/Neo4j"""
        try:
            # Neo4j Aura credentials
            neo4j_uri = os.environ.get("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
            neo4j_user = os.environ.get("NEO4J_USER", "neo4j")
            neo4j_password = os.environ.get("NEO4J_PASSWORD", "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE")

            self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

            # Verify connection
            self.neo4j_driver.verify_connectivity()

            # Get stats
            with self.neo4j_driver.session() as session:
                result = session.run("MATCH (n) RETURN count(n) as count LIMIT 1")
                count = result.single()["count"]
                logger.info(f"✅ Neo4j connected: {count} nodes")

            self.graphiti_available = True

            # Import Graphiti integration
            try:
                from graphiti_integration import CircleOfLifeGraphiti

                self.graphiti = CircleOfLifeGraphiti()
                logger.info("✅ Graphiti integration loaded")
            except:
                logger.warning("⚠️ Graphiti module not found")
                self.graphiti = None

        except Exception as e:
            logger.error(f"❌ Neo4j failed: {e}")
            self.neo4j_driver = None
            self.graphiti_available = False
            self.graphiti = None

    def _init_bigquery(self):
        """Initialize BigQuery"""
        try:
            self.bq_client = bigquery.Client(project=self.project_id)

            # Test
            query = "SELECT 1 as test"
            list(self.bq_client.query(query).result())

            logger.info("✅ BigQuery connected")
            self.bigquery_available = True

        except Exception as e:
            logger.error(f"❌ BigQuery failed: {e}")
            self.bq_client = None
            self.bigquery_available = False

    def _init_datastore(self):
        """Initialize Datastore"""
        try:
            self.datastore_client = datastore.Client(project=self.project_id)
            logger.info("✅ Datastore connected")
            self.datastore_available = True

        except Exception as e:
            logger.error(f"❌ Datastore failed: {e}")
            self.datastore_client = None
            self.datastore_available = False

    def _init_circle_of_life(self):
        """Initialize Circle of Life"""
        self.circle_of_life = {
            "learning_enabled": True,
            "feedback_loop": True,
            "continuous_improvement": True,
            "active": True,
        }
        logger.info("✅ Circle of Life active")

    def _init_slack(self):
        """Initialize Slack"""
        try:
            self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN", "")

            if self.slack_bot_token and not self.slack_bot_token.startswith("placeholder"):
                self.slack_client = WebClient(token=self.slack_bot_token)

                # Test
                auth = self.slack_client.auth_test()
                self.bot_user_id = auth["user_id"]
                logger.info(f"✅ Slack connected: {auth['user']}")
                self.slack_available = True
            else:
                logger.info("ℹ️ Slack not configured (needs real token)")
                self.slack_available = False

        except Exception as e:
            logger.error(f"❌ Slack failed: {e}")
            self.slack_available = False

    def generate_response(self, user_message: str, user_id: str = None) -> str:
        """Generate response using Vertex AI Gemini"""

        # Get context from Graphiti
        context = ""
        if self.graphiti:
            try:
                context = self.graphiti.get_context_for_bob(user_message)
                logger.info(f"📚 Retrieved context: {len(context)} chars")
            except:
                pass

        # Build history
        history = "\n".join([f"User: {h['user']}\nBob: {h['bob']}" for h in self.conversation_history[-5:]])

        # Create prompt
        prompt = f"""You are Bob, an expert AI assistant specializing in equipment repair and diagnostics.
You have extensive knowledge about Bobcat, John Deere, Caterpillar, Ford, Cummins, and other equipment.

Current Date/Time: {self.get_current_time()}
User: {user_id or 'User'}

Recent History:
{history}

Knowledge Base:
{context}

User Question: {user_message}

Provide a helpful, accurate, and concise response. Use specific part numbers, error codes, and repair procedures when relevant.

Bob's Response:"""

        try:
            if self.gemini_available and self.model:
                # Generate with Vertex AI
                response = self.model.generate_content(
                    prompt,
                    generation_config={"temperature": 0.7, "max_output_tokens": 1024, "top_p": 0.95, "top_k": 40},
                )

                if response and response.text:
                    bob_response = response.text.strip()
                    logger.info(f"✅ Generated response: {len(bob_response)} chars")
                else:
                    bob_response = "I'm having trouble generating a response. Please try again."
            else:
                # Fallback
                bob_response = f"I'm currently offline but here's what I know: {context[:500] if context else 'Please check back soon.'}"

            # Store conversation
            self.conversation_history.append(
                {"user": user_message, "bob": bob_response, "timestamp": datetime.now().isoformat()}
            )

            # Learn from interaction
            if self.graphiti:
                try:
                    self.graphiti.learn_from_conversation(user_message, bob_response)
                    logger.info("✅ Learned from conversation")
                except:
                    pass

            # Manage history size
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history :]

            return bob_response

        except Exception as e:
            logger.error(f"Response error: {e}")
            logger.error(traceback.format_exc())
            return "I encountered an error. Please try again."

    def handle_slack_event(self, event: Dict) -> Optional[str]:
        """Handle Slack events"""

        # Skip processed events
        event_id = event.get("client_msg_id") or event.get("ts")
        if event_id in self.processed_events:
            return None

        self.processed_events.add(event_id)

        # Cleanup old events
        if len(self.processed_events) > self.max_events:
            self.processed_events = set(list(self.processed_events)[-self.max_events :])

        # Get details
        text = event.get("text", "")
        user = event.get("user", "unknown")
        channel = event.get("channel")
        thread_ts = event.get("thread_ts") or event.get("ts")

        # Skip bots
        if event.get("bot_id") or (hasattr(self, "bot_user_id") and user == self.bot_user_id):
            return None

        # Check mentions
        if (hasattr(self, "bot_user_id") and f"<@{self.bot_user_id}>" in text) or event.get("channel_type") == "im":
            clean_text = text.replace(f"<@{self.bot_user_id if hasattr(self, 'bot_user_id') else ''}>", "").strip()

            if clean_text:
                response = self.generate_response(clean_text, user)

                if self.slack_available:
                    try:
                        self.slack_client.chat_postMessage(channel=channel, text=response, thread_ts=thread_ts)
                        logger.info(f"✅ Sent to Slack")
                    except:
                        pass

                return response

        return None

    def get_system_status(self) -> Dict:
        """Get system status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "current_time": self.get_current_time(),
            "model": self.model_name if self.gemini_available else "offline",
            "components": {
                "vertex_gemini": self.gemini_available,
                "graphiti": self.graphiti_available,
                "neo4j": bool(self.neo4j_driver),
                "bigquery": self.bigquery_available,
                "datastore": self.datastore_available,
                "slack": self.slack_available,
                "circle_of_life": self.circle_of_life["active"],
            },
            "stats": {"conversations": len(self.conversation_history), "processed_events": len(self.processed_events)},
        }

        # Neo4j stats
        if self.neo4j_driver:
            try:
                with self.neo4j_driver.session() as session:
                    result = session.run("MATCH (n) RETURN count(n) as total")
                    status["neo4j_nodes"] = result.single()["total"]
            except:
                pass

        return status


# Global instance
bob = None


def get_bob():
    """Get or create Bob"""
    global bob
    if bob is None:
        bob = BobBrainVertex()
    return bob


# Flask Routes


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    bob_instance = get_bob()
    status = bob_instance.get_system_status()

    # Check health
    healthy = status["components"]["vertex_gemini"] and status["components"]["neo4j"]

    return (
        jsonify(
            {
                "status": "healthy" if healthy else "degraded",
                "service": "Bob's Brain v6.0 Vertex",
                "model": status["model"],
                "components": status["components"],
                "stats": status["stats"],
                "timestamp": status["timestamp"],
            }
        ),
        200 if healthy else 503,
    )


@app.route("/chat", methods=["POST"])
def chat():
    """Chat endpoint"""
    bob_instance = get_bob()

    data = request.json or {}
    message = data.get("message", "")
    user = data.get("user", "test")

    if not message:
        return jsonify({"error": "No message"}), 400

    try:
        response = bob_instance.generate_response(message, user)

        return jsonify(
            {
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "model": bob_instance.model_name if bob_instance.gemini_available else "offline",
            }
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Slack events"""
    bob_instance = get_bob()

    data = request.json

    # URL verification
    if data.get("type") == "url_verification":
        return jsonify({"challenge": data.get("challenge")})

    # Events
    if data.get("type") == "event_callback":
        event = data.get("event", {})
        bob_instance.executor.submit(bob_instance.handle_slack_event, event)
        return jsonify({"status": "received"}), 200

    return jsonify({"status": "ignored"}), 200


@app.route("/learn", methods=["POST"])
def learn():
    """Learning endpoint"""
    bob_instance = get_bob()

    data = request.json or {}
    content = data.get("content", "")

    if not content:
        return jsonify({"error": "No content"}), 400

    try:
        if bob_instance.graphiti:
            episode_id = bob_instance.graphiti.memory.add_episode(
                content=content, source=data.get("source", "api"), metadata=data.get("metadata", {})
            )

            return jsonify({"status": "learned", "episode_id": episode_id})
        else:
            return jsonify({"error": "Graphiti not available"}), 503

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Status endpoint"""
    bob_instance = get_bob()
    return jsonify(bob_instance.get_system_status())


if __name__ == "__main__":
    # Initialize
    bob = BobBrainVertex()

    # Run
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
