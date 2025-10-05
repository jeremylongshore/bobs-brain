#!/usr/bin/env python3
"""
Bob with Gemini Flash - SIMPLE & WORKING
Just Bob + Gemini, no complex stuff
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Google's NEW Gemini SDK
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobGemini:
    """Simple Bob with just Gemini - no databases, no complexity"""
    
    def __init__(self):
        # Initialize Gemini with API key
        api_key = os.environ.get('GOOGLE_API_KEY', '<REDACTED_GOOGLE_API_KEY>')
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Flash (fast and smart)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini 1.5 Flash initialized")
        
        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        logger.info("✅ Slack connected")
        
        # Bob's personality and knowledge
        self.context = """
        You are Bob, an AI assistant. You're helpful, friendly, and knowledgeable.
        You can help with:
        - Auto repair questions and pricing
        - General questions and conversation
        - Technical assistance
        - Just chatting
        
        Be conversational and helpful. Keep responses concise.
        """
    
    def process_message(self, text: str, user: str = None) -> str:
        """Process a message with Gemini"""
        try:
            # Build prompt
            prompt = f"""
            {self.context}
            
            User: {text}
            
            Bob:
            """
            
            # Generate response with Gemini
            response = self.model.generate_content(prompt)
            
            # Return the response
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            return "I'm having trouble thinking right now. Can you try again?"

# Initialize Bob
bob = BobGemini()

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bob with Gemini',
        'model': 'Gemini 1.5 Flash',
        'ready': True
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Direct chat endpoint for testing"""
    try:
        data = request.json
        message = data.get('message', 'Hello')
        
        response = bob.process_message(message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
                
                # Get response from Gemini
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
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'Bob with Gemini',
        'status': 'running',
        'endpoints': {
            '/health': 'Health check',
            '/chat': 'Direct chat (POST with {"message": "your text"})',
            '/slack/events': 'Slack integration'
        },
        'model': 'Gemini 1.5 Flash',
        'description': 'Simple Bob - just Gemini and Slack'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)