#!/usr/bin/env python3
"""
Bob with Native Vertex AI using the NEW protocol
Uses latest Gemini 1.5 Flash via google-generativeai SDK
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

# Use the NEW Google Generative AI SDK (recommended for Gemini)
import google.generativeai as genai
from google.cloud import firestore
from graphiti_core import Graphiti

app = Flask(__name__)

class BobVertexNative:
    """Bob using the NEW Vertex AI protocol with Gemini"""
    
    def __init__(self):
        # Configure Gemini with the NEW protocol
        # This uses google-generativeai which is the recommended way for Gemini
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY') or '<REDACTED_GOOGLE_API_KEY>')
        
        # Initialize the model with latest protocol
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Initialized Gemini 1.5 Flash with NEW protocol")
        
        # Initialize Graphiti for knowledge graph
        if not os.environ.get('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
        
        self.graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', '<REDACTED_NEO4J_PASSWORD>')
        )
        logger.info("✅ Connected to Graphiti knowledge graph")
        
        # Initialize Firestore for customer data
        try:
            self.firestore = firestore.Client(project='diagnostic-pro-mvp', database='bob-brain')
            logger.info("✅ Connected to Firestore")
        except:
            self.firestore = None
            logger.warning("⚠️ Firestore not available")
        
        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        
        logger.info("✅ Bob initialized with NEW Vertex AI protocol")
    
    async def process_message(self, text: str, user: str, channel: str):
        """Process a message using the new Gemini protocol"""
        try:
            # Search for relevant context in Graphiti
            search_results = await self.graphiti.search(text, num_results=5)
            
            # Build context from search results
            context_parts = []
            if search_results:
                for result in search_results[:3]:
                    context_parts.append(f"- {str(result)[:150]}")
            
            # Search Firestore if available
            firestore_context = []
            if self.firestore:
                try:
                    # Quick search in knowledge collection
                    knowledge = self.firestore.collection('knowledge').limit(5).stream()
                    for doc in knowledge:
                        data = doc.to_dict()
                        if text.lower() in str(data).lower():
                            firestore_context.append(f"- {data.get('content', str(data))[:100]}")
                            if len(firestore_context) >= 2:
                                break
                except Exception as e:
                    logger.error(f"Firestore search error: {e}")
            
            # Build complete context
            full_context = "Relevant context from memory:\n"
            if context_parts:
                full_context += "From Knowledge Graph:\n" + "\n".join(context_parts) + "\n"
            if firestore_context:
                full_context += "\nFrom Customer Database:\n" + "\n".join(firestore_context) + "\n"
            
            # Generate response with NEW Gemini protocol
            prompt = f"""You are Bob, an AI assistant for DiagnosticPro.
            
{full_context}

User: {text}
Bob (respond helpfully and concisely):"""
            
            # Use the new generation method
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Store this interaction in Graphiti
            await self.graphiti.add_episode(
                name=f"conversation_{datetime.now().isoformat()}",
                episode_body=f"User {user}: {text}\nBob: {response_text}",
                source_description=f"Slack conversation in {channel}",
                reference_time=datetime.now()
            )
            
            # Also store in Firestore if available
            if self.firestore:
                try:
                    self.firestore.collection('bob_conversations').add({
                        'user': user,
                        'channel': channel,
                        'user_message': text,
                        'bob_response': response_text,
                        'timestamp': datetime.now(),
                        'ai_model': 'gemini-1.5-flash-native'
                    })
                except Exception as e:
                    logger.error(f"Firestore save error: {e}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I encountered an error: {str(e)[:100]}. Let me try again."

# Initialize Bob with NEW Vertex AI protocol
bob = BobVertexNative()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bob's Brain with Native Vertex AI",
        "ai": "Gemini 1.5 Flash (NEW Protocol)",
        "memory": "Neo4j + Graphiti",
        "customer_data": "Firestore" if bob.firestore else "Not connected",
        "protocol": "google-generativeai (latest)"
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
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

@app.route('/test-gemini', methods=['GET'])
def test_gemini():
    """Test endpoint to verify Gemini is working"""
    try:
        response = bob.model.generate_content("Say 'Gemini is working with the new protocol!'")
        return jsonify({
            "status": "success",
            "response": response.text,
            "model": "gemini-1.5-flash",
            "protocol": "google-generativeai"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "Bob's Brain",
        "version": "4.0",
        "features": [
            "Native Vertex AI (Gemini 1.5 Flash)",
            "NEW google-generativeai protocol",
            "Graphiti Knowledge Graph",
            "Neo4j Database",
            "Firestore Customer Data",
            "Slack Integration"
        ],
        "ai_protocol": "google-generativeai (recommended for Gemini)"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)