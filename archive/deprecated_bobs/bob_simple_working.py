#!/usr/bin/env python3
"""
SIMPLE WORKING BOB - Just get it working!
No complex dependencies, just Vertex AI + Slack
"""

import os
import logging
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Simple Vertex AI import
import vertexai
from vertexai.generative_models import GenerativeModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class SimpleBob:
    def __init__(self):
        # Initialize Vertex AI
        project = os.environ.get('GCP_PROJECT', 'bobs-house-ai')
        location = os.environ.get('GCP_LOCATION', 'us-central1')
        
        logger.info(f"Initializing Vertex AI: project={project}, location={location}")
        vertexai.init(project=project, location=location)
        
        # Try different model names until one works
        model_names = [
            'gemini-1.0-pro',
            'gemini-1.0-pro-001',
            'gemini-1.0-pro-002',
            'gemini-pro',
        ]
        
        self.model = None
        for model_name in model_names:
            try:
                self.model = GenerativeModel(model_name)
                logger.info(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {str(e)[:50]}")
                continue
        
        if not self.model:
            logger.error("NO MODELS AVAILABLE - Using fallback")
            self.model = None
        
        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        logger.info("Slack client initialized")
    
    def process_message(self, text):
        """Process a message"""
        try:
            if self.model:
                # Use Vertex AI
                prompt = f"""
You are Bob, a helpful AI assistant with reasoning capabilities.

User: {text}

Think step by step if needed, then respond helpfully:
"""
                response = self.model.generate_content(prompt)
                return response.text
            else:
                # Fallback response
                if "hello" in text.lower() or "hi" in text.lower():
                    return "Hello! I'm Bob. I'm having some technical difficulties with my AI brain, but I'm here to help as best I can!"
                elif "?" in text:
                    return "That's a great question! I'm currently having issues connecting to my AI model, but once that's fixed I'll be able to help you better."
                else:
                    return "I understand you said: '" + text + "'. I'm having connection issues with my AI model right now, but I'm listening!"
        except Exception as e:
            logger.error(f"Error processing: {e}")
            return f"I encountered an error: {str(e)[:100]}. Let me try to help anyway - what do you need?"

bob = SimpleBob()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'SimpleBob',
        'model_loaded': bob.model is not None,
        'project': os.environ.get('GCP_PROJECT', 'bobs-house-ai')
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    try:
        data = request.json
        
        # URL verification
        if data.get('type') == 'url_verification':
            return jsonify({'challenge': data['challenge']})
        
        # Handle messages
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            
            if event.get('type') == 'message' and not event.get('bot_id'):
                text = event.get('text')
                channel = event.get('channel')
                
                # Process and respond
                response = bob.process_message(text)
                
                try:
                    bob.slack_client.chat_postMessage(
                        channel=channel,
                        text=response
                    )
                except SlackApiError as e:
                    logger.error(f"Slack error: {e}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    response = bob.process_message("What is 2+2?")
    return jsonify({
        'question': 'What is 2+2?',
        'response': response,
        'model_loaded': bob.model is not None
    })

@app.route('/', methods=['GET']) 
def index():
    return jsonify({
        'service': 'SimpleBob',
        'status': 'running',
        'model_loaded': bob.model is not None
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)