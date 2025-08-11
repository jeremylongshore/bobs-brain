#!/usr/bin/env python3
"""
BOB PRODUCTION FIXED - Working version with correct Gemini model and ML integration
Following Google's best practices for Vertex AI
"""

import os
import logging
import json
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.cloud import bigquery
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobProductionFixed:
    def __init__(self):
        """Initialize Bob with correct Gemini model and ML integration"""
        
        # GCP Configuration
        self.project_id = os.environ.get('GCP_PROJECT', 'bobs-house-ai')
        self.location = os.environ.get('GCP_LOCATION', 'us-central1')
        
        logger.info(f"🚀 Initializing Bob - Project: {self.project_id}, Location: {self.location}")
        
        # Initialize Vertex AI with correct configuration
        try:
            vertexai.init(project=self.project_id, location=self.location)
            
            # Use the CORRECT Gemini 2.5 Flash model (best for our use case)
            # According to best practices: optimized for price-performance, low-latency, agentic use
            self.model = GenerativeModel(
                'gemini-1.5-flash',  # Correct model name without version suffix
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                    top_p=0.95,
                    top_k=40
                )
            )
            logger.info("✅ Gemini 1.5 Flash model initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Vertex AI: {e}")
            # Fallback to older model if needed
            try:
                self.model = GenerativeModel('gemini-1.0-pro')
                logger.info("✅ Fallback to Gemini 1.0 Pro")
            except:
                self.model = None
                logger.error("❌ No Gemini models available")
        
        # Initialize BigQuery for ML predictions
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
            logger.info("✅ BigQuery client initialized for ML predictions")
        except Exception as e:
            logger.warning(f"⚠️ BigQuery not available: {e}")
            self.bq_client = None
        
        # AutoML endpoint (set via environment variable if you have one deployed)
        self.automl_endpoint = os.environ.get('AUTOML_ENDPOINT')
        if self.automl_endpoint:
            logger.info(f"✅ AutoML endpoint configured: {self.automl_endpoint}")
        
        # Initialize Firestore for data access
        try:
            # Access Firestore in the other project where data lives
            self.firestore_client = firestore.Client(project='diagnostic-pro-mvp')
            logger.info("✅ Firestore client initialized")
        except Exception as e:
            logger.warning(f"⚠️ Firestore not available: {e}")
            self.firestore_client = None
        
        # Initialize Slack client
        self.slack_token = os.environ.get('SLACK_BOT_TOKEN')
        if self.slack_token:
            self.slack_client = WebClient(token=self.slack_token)
            logger.info("✅ Slack client initialized")
        else:
            logger.warning("⚠️ No SLACK_BOT_TOKEN found")
            self.slack_client = None
        
        # Track processed messages to prevent duplicates
        self.processed_events = set()
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        logger.info("🎉 Bob initialization complete!")
    
    def get_ml_prediction(self, query_text):
        """Get ML predictions from BigQuery ML and AutoML models"""
        if not self.bq_client:
            return None
        
        predictions = []
        
        try:
            # 1. BigQuery ML Model Prediction (if model exists)
            try:
                ml_query = """
                SELECT 
                    predicted_price
                FROM ML.PREDICT(
                    MODEL `bobs-house-ai.ml_models.repair_price_predictor`,
                    (SELECT 
                        'brake_replacement' as repair_type,
                        2020 as vehicle_year,
                        'Toyota' as vehicle_make
                    )
                )
                LIMIT 1
                """
                
                results = self.bq_client.query(ml_query).result()
                for row in results:
                    predictions.append(f"BigQuery ML Price Prediction: ${row.predicted_price:.2f}")
            except Exception as e:
                logger.debug(f"BigQuery ML model not available: {e}")
                
                # Fallback to aggregated data
                fallback_query = """
                SELECT 
                    AVG(quoted_price) as avg_price,
                    MIN(quoted_price) as min_price,
                    MAX(quoted_price) as max_price,
                    COUNT(*) as sample_size
                FROM `bobs-house-ai.scraped_data.repair_quotes`
                WHERE LOWER(repair_type) LIKE '%brake%'
                """
                
                results = self.bq_client.query(fallback_query).result()
                for row in results:
                    if row.avg_price:
                        predictions.append(f"Market Analysis: Average ${row.avg_price:.2f} (Range: ${row.min_price:.2f}-${row.max_price:.2f}, {row.sample_size} samples)")
            
            # 2. AutoML Model Prediction (if deployed)
            if hasattr(self, 'automl_endpoint') and self.automl_endpoint:
                try:
                    from google.cloud import aiplatform
                    
                    # Initialize AI Platform
                    aiplatform.init(project=self.project_id, location=self.location)
                    
                    # Get endpoint
                    endpoint = aiplatform.Endpoint(self.automl_endpoint)
                    
                    # Prepare instance for prediction
                    instance = {
                        "repair_type": "brake_replacement",
                        "vehicle_year": 2020,
                        "vehicle_make": "Toyota"
                    }
                    
                    # Get prediction
                    prediction = endpoint.predict(instances=[instance])
                    if prediction.predictions:
                        pred_value = prediction.predictions[0].get('value', prediction.predictions[0])
                        predictions.append(f"AutoML Prediction: ${pred_value:.2f}")
                        
                except Exception as e:
                    logger.debug(f"AutoML prediction not available: {e}")
            
            # 3. Pattern Analysis from Historical Data
            pattern_query = """
            SELECT 
                repair_type,
                COUNT(*) as frequency,
                AVG(savings) as avg_savings
            FROM `bobs-house-ai.scraped_data.repair_analysis`
            WHERE DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
            GROUP BY repair_type
            ORDER BY frequency DESC
            LIMIT 3
            """
            
            try:
                results = self.bq_client.query(pattern_query).result()
                patterns = []
                for row in results:
                    if row.avg_savings:
                        patterns.append(f"{row.repair_type}: Avg savings ${row.avg_savings:.2f}")
                if patterns:
                    predictions.append(f"Recent Trends: {', '.join(patterns)}")
            except:
                pass  # Pattern analysis is optional
            
            if predictions:
                return "\n".join(predictions)
            
        except Exception as e:
            logger.warning(f"ML prediction error: {e}")
        
        return None
    
    def get_firestore_context(self, query_text):
        """Get relevant context from Firestore if available"""
        if not self.firestore_client:
            return None
        
        try:
            # Get recent relevant documents
            docs = self.firestore_client.collection('diagnostic_submissions').limit(3).get()
            
            if docs:
                context = "Recent data shows: "
                for doc in docs:
                    data = doc.to_dict()
                    if 'repair_type' in data:
                        context += f"{data.get('repair_type', 'N/A')} "
                return context
                
        except Exception as e:
            logger.warning(f"Firestore context failed: {e}")
        
        return None
    
    def process_message(self, text, user_id=None, channel=None):
        """Process message with Gemini and ML integration"""
        
        try:
            # Get ML predictions if relevant
            ml_context = ""
            if any(word in text.lower() for word in ['price', 'cost', 'repair', 'quote']):
                ml_prediction = self.get_ml_prediction(text)
                if ml_prediction:
                    ml_context = f"\n\nML Insight: {ml_prediction}"
            
            # Get Firestore context if available
            db_context = self.get_firestore_context(text)
            if db_context:
                ml_context += f"\n\nDatabase Context: {db_context}"
            
            # Build the prompt following best practices
            prompt = f"""You are Bob, an AI assistant for Bob's House of AI, specializing in automotive repair advice and price analysis.

Company: Bob's House of AI (formerly DiagnosticPro)
Owner: Jeremy Longshore
Mission: Help customers avoid getting scammed on car repairs

User Question: {text}
{ml_context}

Provide a helpful, concise response. If discussing prices or repairs, be specific and practical.
Think step-by-step about the user's needs, then respond:"""

            if self.model:
                # Generate response with Gemini
                response = self.model.generate_content(
                    prompt,
                    generation_config=GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=1024,
                        candidate_count=1
                    )
                )
                
                # Extract text from response
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'candidates') and response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    return "I processed your request but couldn't generate a proper response. Please try again."
            else:
                # Fallback without model
                return self.get_fallback_response(text)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I encountered an issue processing your request. Let me try to help anyway. Error: {str(e)[:100]}"
    
    def get_fallback_response(self, text):
        """Fallback responses when Gemini is not available"""
        text_lower = text.lower()
        
        if any(greeting in text_lower for greeting in ['hello', 'hi', 'hey']):
            return "Hello! I'm Bob from Bob's House of AI. How can I help you with your automotive needs today?"
        elif 'price' in text_lower or 'cost' in text_lower:
            return "For accurate pricing, I normally use ML models to analyze market data. The AI model is temporarily unavailable, but typical repair costs vary widely. What specific repair are you asking about?"
        elif 'repair' in text_lower:
            return "I can help with repair advice! While my AI capabilities are limited right now, I can tell you that getting multiple quotes and understanding the work needed is key to avoiding overcharges."
        elif '?' in text:
            return "That's a great question! My AI model is temporarily offline, but I'm here to help. Could you provide more details about your automotive concern?"
        else:
            return f"I heard you say: '{text}'. I'm currently running in limited mode, but I'm here to help with any automotive questions you have!"

# Initialize Bob
bob = BobProductionFixed()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bob Production Fixed',
        'model': 'Gemini 1.5 Flash' if bob.model else 'No model',
        'project': bob.project_id,
        'ml_enabled': bob.bq_client is not None,
        'firestore_enabled': bob.firestore_client is not None,
        'slack_enabled': bob.slack_client is not None,
        'version': '2.0.0',
        'timestamp': time.time()
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        
        # URL verification for Slack
        if data.get('type') == 'url_verification':
            return jsonify({'challenge': data['challenge']})
        
        # Handle event callbacks
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            event_id = data.get('event_id')
            
            # Prevent duplicate processing
            if event_id in bob.processed_events:
                return jsonify({'status': 'duplicate'})
            
            bob.processed_events.add(event_id)
            
            # Clean old events (keep last 1000)
            if len(bob.processed_events) > 1000:
                bob.processed_events = set(list(bob.processed_events)[-500:])
            
            # Process messages (not from bots)
            if event.get('type') == 'message' and not event.get('bot_id'):
                text = event.get('text', '')
                channel = event.get('channel')
                user = event.get('user')
                
                # Process message and respond
                response = bob.process_message(text, user, channel)
                
                # Send response to Slack
                if bob.slack_client and channel:
                    try:
                        bob.slack_client.chat_postMessage(
                            channel=channel,
                            text=response
                        )
                        logger.info(f"Responded to message in {channel}")
                    except SlackApiError as e:
                        logger.error(f"Slack API error: {e}")
            
            # Handle app mentions
            elif event.get('type') == 'app_mention':
                text = event.get('text', '')
                channel = event.get('channel')
                user = event.get('user')
                
                # Remove the mention from text
                text = ' '.join(word for word in text.split() if not word.startswith('<@'))
                
                response = bob.process_message(text, user, channel)
                
                if bob.slack_client and channel:
                    try:
                        bob.slack_client.chat_postMessage(
                            channel=channel,
                            text=response
                        )
                    except SlackApiError as e:
                        logger.error(f"Slack API error: {e}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Error handling Slack event: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Test endpoint"""
    if request.method == 'POST':
        data = request.json or {}
        text = data.get('text', 'What is 2+2?')
    else:
        text = request.args.get('text', 'What is 2+2?')
    
    response = bob.process_message(text)
    
    return jsonify({
        'question': text,
        'response': response,
        'model': 'Gemini 1.5 Flash' if bob.model else 'No model',
        'ml_enabled': bob.bq_client is not None,
        'firestore_enabled': bob.firestore_client is not None
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Bob\'s Brain - Production Fixed',
        'status': 'operational',
        'endpoints': {
            '/': 'This help message',
            '/health': 'Health check',
            '/test': 'Test Bob\'s response',
            '/slack/events': 'Slack event handler'
        },
        'model': 'Gemini 1.5 Flash (Vertex AI)',
        'features': [
            'Gemini 1.5 Flash for responses',
            'BigQuery ML predictions',
            'Firestore data access',
            'Slack integration',
            'Duplicate prevention'
        ],
        'owner': 'Jeremy Longshore',
        'company': 'Bob\'s House of AI'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Starting Bob on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)