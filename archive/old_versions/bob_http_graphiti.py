#!/usr/bin/env python3
"""
Bob HTTP Server with Graphiti Memory
Replaces the existing Cloud Run instance with Graphiti-powered Bob
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set OpenAI key if provided (will be replaced with Vertex AI later)
if not os.environ.get('OPENAI_API_KEY'):
    # Key must be provided via environment variable for security
    print("WARNING: OPENAI_API_KEY not set. Graphiti entity extraction may not work.")
    os.environ['OPENAI_API_KEY'] = 'placeholder-key-required'

# Import Graphiti and other dependencies
from graphiti_core import Graphiti
import vertexai
from vertexai.generative_models import GenerativeModel

app = Flask(__name__)

class BobGraphiti:
    """Bob with Graphiti memory on Google Cloud"""

    def __init__(self):
        # Initialize Graphiti with GCP Neo4j (or local for testing)
        # Use GCP internal IP when deployed, localhost for local testing
        neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687')
        if not os.environ.get('DEPLOYED_TO_GCP'):
            # For local testing, use local Neo4j
            neo4j_uri = 'bolt://localhost:7687'

        self.graphiti = Graphiti(
            uri=neo4j_uri,
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', '<REDACTED_NEO4J_PASSWORD>')
        )

        # Initialize Vertex AI for responses
        vertexai.init(project='bobs-house-ai', location='us-central1')
        self.model = GenerativeModel('gemini-1.5-flash')

        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

        logger.info("✅ Bob initialized with Graphiti memory")

    async def process_message(self, text: str, user: str, channel: str):
        """Process a message and generate response"""
        try:
            # Search for relevant context in Graphiti
            search_results = await self.graphiti.search(text, num_results=5)

            # Build context from search results
            context = ""
            if search_results:
                context = "Relevant context from memory:\n"
                for result in search_results[:3]:
                    context += f"- {str(result)[:100]}...\n"

            # Generate response with Vertex AI
            prompt = f"""You are Bob, an AI assistant for DiagnosticPro.

{context}

User: {text}
Bob (respond helpfully and concisely):"""

            response = self.model.generate_content(prompt)
            response_text = response.text

            # Store this interaction in Graphiti
            await self.graphiti.add_episode(
                name=f"conversation_{datetime.now().isoformat()}",
                episode_body=f"User {user}: {text}\nBob: {response_text}",
                source_description=f"Slack conversation in {channel}",
                reference_time=datetime.now()
            )

            return response_text

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I'm having trouble accessing my memory right now. Let me try again."

# Initialize Bob
bob = BobGraphiti()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bob's Brain with Graphiti",
        "memory": "Neo4j + Graphiti",
        "ai": "Vertex AI (Gemini)"
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        # Parse the request
        slack_data = request.json

        # Handle URL verification
        if slack_data.get('type') == 'url_verification':
            return jsonify({"challenge": slack_data['challenge']})

        # Handle events
        if slack_data.get('type') == 'event_callback':
            event = slack_data.get('event', {})

            # Only respond to messages (not from bots)
            if event.get('type') == 'message' and not event.get('bot_id'):
                user = event.get('user')
                text = event.get('text')
                channel = event.get('channel')

                # Process asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    bob.process_message(text, user, channel)
                )

                # Send response to Slack
                try:
                    bob.slack_client.chat_postMessage(
                        channel=channel,
                        text=response
                    )
                except SlackApiError as e:
                    logger.error(f"Slack API error: {e}")

        return jsonify({"status": "ok"})

    except Exception as e:
        logger.error(f"Error handling Slack event: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "Bob's Brain",
        "version": "2.0",
        "features": [
            "Graphiti Knowledge Graph",
            "Neo4j Database",
            "Vertex AI (Gemini)",
            "Slack Integration"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)