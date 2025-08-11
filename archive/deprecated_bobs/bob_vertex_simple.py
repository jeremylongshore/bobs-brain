#!/usr/bin/env python3
"""
Bob with Vertex AI - No API key needed!
Uses your GCP project credentials
"""

import os
import logging
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Vertex AI - uses project credentials, no API key!
import vertexai
from vertexai.generative_models import GenerativeModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobVertex:
    """Bob using Vertex AI (no API key needed)"""
    
    def __init__(self):
        # Initialize Vertex AI with project
        project_id = os.environ.get('GCP_PROJECT', 'bobs-house-ai')
        location = os.environ.get('GCP_LOCATION', 'us-central1')
        
        vertexai.init(project=project_id, location=location)
        
        # Use Gemini 1.5 Flash through Vertex AI
        # Try different model names based on what's available
        try:
            self.model = GenerativeModel('gemini-1.5-flash-001')
            logger.info("✅ Using gemini-1.5-flash-001")
        except:
            try:
                self.model = GenerativeModel('gemini-1.0-pro')
                logger.info("✅ Using gemini-1.0-pro as fallback")
            except:
                self.model = GenerativeModel('gemini-pro')
                logger.info("✅ Using gemini-pro as final fallback")
        logger.info(f"✅ Vertex AI Gemini initialized for project {project_id}")
        
        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        logger.info("✅ Slack connected")
        
        # Bob's personality
        self.context = """
        You are Bob, an AI assistant with advanced reasoning capabilities.
        You can:
        - Use logic and reasoning to solve problems
        - Analyze car repair prices and detect overcharging
        - Provide step-by-step explanations
        - Do math and calculations
        - Have natural conversations
        
        Be helpful, friendly, and use your reasoning abilities to give smart answers.
        """
    
    def process_message(self, text: str, user: str = None) -> str:
        """Process a message with Vertex AI Gemini"""
        try:
            # Build prompt
            prompt = f"""
            {self.context}
            
            User: {text}
            
            Think step by step if needed, then respond as Bob:
            """
            
            # Generate response with Vertex AI
            response = self.model.generate_content(prompt)
            
            # Return the response
            return response.text
            
        except Exception as e:
            logger.error(f"Vertex AI error: {e}")
            # Fallback response
            return "I'm having a moment. Let me try again - can you repeat that?"

# Initialize Bob
bob = BobVertex()

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bob with Vertex AI',
        'model': 'Gemini 1.5 Flash (via Vertex AI)',
        'project': os.environ.get('GCP_PROJECT', 'bobs-house-ai'),
        'no_api_key_needed': True
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        
        # Handle Slack URL verification
        if data.get('type') == 'url_verification':
            return jsonify({'challenge': data['challenge']})
        
        # Handle actual messages
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            
            # Only respond to messages (not from bots)
            if event.get('type') == 'message' and not event.get('bot_id'):
                text = event.get('text')
                user = event.get('user')
                channel = event.get('channel')
                
                logger.info(f"Processing message from {user}: {text[:50]}...")
                
                # Get response from Vertex AI
                response = bob.process_message(text, user)
                
                # Send response back to Slack
                try:
                    bob.slack_client.chat_postMessage(
                        channel=channel,
                        text=response
                    )
                    logger.info(f"Sent response to {channel}")
                except SlackApiError as e:
                    logger.error(f"Slack error: {e}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Error handling Slack event: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    try:
        response = bob.process_message("What is 2+2?")
        return jsonify({
            'test': 'What is 2+2?',
            'response': response,
            'status': 'working'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'Bob with Vertex AI',
        'status': 'running',
        'endpoints': {
            '/health': 'Health check',
            '/test': 'Test Bob',
            '/slack/events': 'Slack integration'
        },
        'model': 'Gemini 1.5 Flash via Vertex AI',
        'features': [
            'Advanced reasoning',
            'Logic and problem solving',
            '2 million token context',
            'No API key needed (uses GCP credentials)'
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)