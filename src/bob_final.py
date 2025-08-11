#!/usr/bin/env python3
"""
BOB FINAL - The definitive production version
Integrates: Graphiti (Neo4j) + Vertex AI Gemini + BigQuery ML + Firestore + Slack
This is THE Bob that runs in production.
"""

import os
import logging
import json
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.cloud import bigquery
from google.cloud import firestore
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
import time
from concurrent.futures import ThreadPoolExecutor
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobFinal:
    """The final, definitive Bob implementation"""
    
    def __init__(self):
        """Initialize all Bob's components"""
        
        # Core configuration
        self.project_id = os.environ.get('GCP_PROJECT', 'bobs-house-ai')
        self.location = os.environ.get('GCP_LOCATION', 'us-central1')
        
        logger.info("=" * 60)
        logger.info("🤖 INITIALIZING BOB FINAL - THE DEFINITIVE VERSION")
        logger.info(f"📍 Project: {self.project_id}")
        logger.info(f"📍 Location: {self.location}")
        logger.info("=" * 60)
        
        # Initialize components
        self._init_vertex_ai()
        self._init_graphiti()
        self._init_bigquery()
        self._init_firestore()
        self._init_slack()
        
        # Tracking for duplicate prevention
        self.processed_events = set()
        self.max_events = 1000
        
        # Thread pool for async operations
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        logger.info("✅ BOB FINAL INITIALIZATION COMPLETE!")
        logger.info("=" * 60)
    
    def _init_vertex_ai(self):
        """Initialize Vertex AI with correct Gemini model"""
        try:
            vertexai.init(project=self.project_id, location=self.location)
            
            # Use Gemini 1.5 Flash - the correct model for our use case
            # Best for: adaptive thinking, cost efficiency, low-latency, agentic use
            self.model = GenerativeModel(
                'gemini-1.5-flash',  # Correct model name
                generation_config=GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                    top_p=0.95,
                    top_k=40
                )
            )
            logger.info("✅ Vertex AI: Gemini 1.5 Flash initialized")
            
        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {e}")
            # Try fallback
            try:
                self.model = GenerativeModel('gemini-1.0-pro')
                logger.info("⚠️ Vertex AI: Fallback to Gemini 1.0 Pro")
            except:
                self.model = None
                logger.error("❌ Vertex AI: No models available")
    
    def _init_graphiti(self):
        """Initialize Graphiti knowledge graph"""
        try:
            # Neo4j connection (running on GCP VM)
            neo4j_uri = os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687')
            neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
            neo4j_password = os.environ.get('NEO4J_PASSWORD', 'BobBrain2025')
            
            # Initialize Graphiti with OpenAI for now (will migrate to Vertex later)
            openai_key = os.environ.get('OPENAI_API_KEY', '')
            
            if openai_key:
                self.graphiti = Graphiti(
                    uri=neo4j_uri,
                    user=neo4j_user,
                    password=neo4j_password,
                    llm_client=None,  # Will use default OpenAI
                    embedder=None     # Will use default OpenAI
                )
                logger.info(f"✅ Graphiti: Connected to Neo4j at {neo4j_uri}")
            else:
                # Graphiti without OpenAI - just for storage
                self.graphiti = None
                logger.warning("⚠️ Graphiti: No OpenAI key, knowledge graph disabled")
                
        except Exception as e:
            logger.error(f"❌ Graphiti initialization failed: {e}")
            self.graphiti = None
    
    def _init_bigquery(self):
        """Initialize BigQuery for ML predictions"""
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
            
            # Test connection
            query = "SELECT 1 as test"
            list(self.bq_client.query(query).result())
            
            logger.info("✅ BigQuery: ML predictions ready")
            
        except Exception as e:
            logger.warning(f"⚠️ BigQuery not available: {e}")
            self.bq_client = None
    
    def _init_firestore(self):
        """Initialize Firestore for data access"""
        try:
            # Connect to Firestore in diagnostic-pro-mvp where data lives
            self.firestore_client = firestore.Client(project='diagnostic-pro-mvp')
            
            # Test connection
            test_collection = self.firestore_client.collection('diagnostic_submissions').limit(1).get()
            
            logger.info("✅ Firestore: Connected to diagnostic-pro-mvp")
            
        except Exception as e:
            logger.warning(f"⚠️ Firestore not available: {e}")
            self.firestore_client = None
    
    def _init_slack(self):
        """Initialize Slack client"""
        self.slack_token = os.environ.get('SLACK_BOT_TOKEN')
        
        if self.slack_token:
            self.slack_client = WebClient(token=self.slack_token)
            logger.info("✅ Slack: Client initialized")
        else:
            logger.warning("⚠️ Slack: No SLACK_BOT_TOKEN found")
            self.slack_client = None
    
    async def search_knowledge_graph(self, query):
        """Search Graphiti knowledge graph"""
        if not self.graphiti:
            return None
        
        try:
            # Search for relevant knowledge
            results = await self.graphiti.search(
                query=query,
                num_results=3
            )
            
            if results:
                context = "Knowledge from memory:\n"
                for result in results:
                    if hasattr(result, 'content'):
                        context += f"- {result.content}\n"
                return context
                
        except Exception as e:
            logger.warning(f"Knowledge graph search failed: {e}")
        
        return None
    
    async def store_in_knowledge_graph(self, text, response, user=None):
        """Store interaction in Graphiti"""
        if not self.graphiti:
            return
        
        try:
            # Create episode from the interaction
            episode_content = f"User asked: {text}\nBob responded: {response[:500]}"
            
            await self.graphiti.add_episode(
                name=f"conversation_{datetime.now().isoformat()}",
                episode_body=episode_content,
                source_description=f"Slack conversation with {user or 'unknown'}",
                reference_time=datetime.now(),
                episode_type=EpisodeType.message
            )
            
            logger.info("💾 Stored interaction in knowledge graph")
            
        except Exception as e:
            logger.warning(f"Failed to store in knowledge graph: {e}")
    
    def get_ml_predictions(self, query_text):
        """Get ML predictions from BigQuery"""
        if not self.bq_client:
            return None
        
        predictions = []
        
        try:
            # Check if asking about prices
            if any(word in query_text.lower() for word in ['price', 'cost', 'expensive', 'cheap']):
                
                # Get average repair prices
                price_query = """
                SELECT 
                    'brake_replacement' as repair_type,
                    AVG(quoted_price) as avg_price,
                    MIN(quoted_price) as min_price,
                    MAX(quoted_price) as max_price
                FROM `bobs-house-ai.scraped_data.repair_quotes`
                WHERE repair_type LIKE '%brake%'
                UNION ALL
                SELECT 
                    'oil_change' as repair_type,
                    AVG(quoted_price) as avg_price,
                    MIN(quoted_price) as min_price,
                    MAX(quoted_price) as max_price
                FROM `bobs-house-ai.scraped_data.repair_quotes`
                WHERE repair_type LIKE '%oil%'
                LIMIT 5
                """
                
                results = self.bq_client.query(price_query).result()
                
                for row in results:
                    predictions.append(
                        f"{row.repair_type}: ${row.avg_price:.2f} "
                        f"(range: ${row.min_price:.2f}-${row.max_price:.2f})"
                    )
            
            # Check if asking about shops
            if any(word in query_text.lower() for word in ['shop', 'mechanic', 'garage']):
                
                shop_query = """
                SELECT 
                    shop_name,
                    AVG(quoted_price - fair_price) as avg_overcharge,
                    COUNT(*) as num_quotes
                FROM `bobs-house-ai.scraped_data.repair_quotes`
                WHERE shop_name IS NOT NULL
                GROUP BY shop_name
                ORDER BY avg_overcharge DESC
                LIMIT 3
                """
                
                results = self.bq_client.query(shop_query).result()
                
                for row in results:
                    if row.avg_overcharge > 100:
                        predictions.append(
                            f"⚠️ {row.shop_name}: Typically overcharges by ${row.avg_overcharge:.2f}"
                        )
            
        except Exception as e:
            logger.warning(f"ML prediction error: {e}")
        
        return "\n".join(predictions) if predictions else None
    
    def get_firestore_context(self, query_text):
        """Get relevant context from Firestore"""
        if not self.firestore_client:
            return None
        
        try:
            # Search for relevant submissions
            docs = self.firestore_client.collection('diagnostic_submissions').limit(5).get()
            
            relevant_data = []
            query_lower = query_text.lower()
            
            for doc in docs:
                data = doc.to_dict()
                
                # Check if document is relevant to query
                if any(word in str(data).lower() for word in query_lower.split()):
                    if 'repair_type' in data and 'quoted_price' in data:
                        relevant_data.append(
                            f"{data['repair_type']}: ${data['quoted_price']}"
                        )
            
            if relevant_data:
                return f"Recent cases: {', '.join(relevant_data[:3])}"
                
        except Exception as e:
            logger.warning(f"Firestore context error: {e}")
        
        return None
    
    def process_message(self, text, user=None, channel=None):
        """Process message with all integrations"""
        
        try:
            # Run async operations
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Search knowledge graph
            kg_context = loop.run_until_complete(self.search_knowledge_graph(text))
            
            # Get ML predictions
            ml_predictions = self.get_ml_predictions(text)
            
            # Get Firestore context
            db_context = self.get_firestore_context(text)
            
            # Build context for response
            context_parts = []
            
            if kg_context:
                context_parts.append(f"📚 {kg_context}")
            
            if ml_predictions:
                context_parts.append(f"📊 ML Analysis:\n{ml_predictions}")
            
            if db_context:
                context_parts.append(f"📁 {db_context}")
            
            context = "\n\n".join(context_parts) if context_parts else ""
            
            # Build prompt
            prompt = f"""You are Bob, an AI assistant for Bob's House of AI.

Company: Bob's House of AI (formerly DiagnosticPro)
Owner: Jeremy Longshore
Mission: Help customers avoid getting scammed on car repairs using data and ML insights

User Question: {text}

{context}

Instructions:
- Be helpful, friendly, and concise
- Use any ML predictions or data insights in your response
- If discussing prices, be specific when you have data
- Think step-by-step about the user's needs

Response:"""

            # Generate response with Gemini
            if self.model:
                response = self.model.generate_content(
                    prompt,
                    generation_config=GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=1024
                    )
                )
                
                # Extract text
                if hasattr(response, 'text'):
                    final_response = response.text
                else:
                    final_response = "I processed your request but couldn't generate a response. Please try again."
            else:
                # Fallback without model
                final_response = self._get_fallback_response(text, context)
            
            # Store in knowledge graph (async)
            loop.run_until_complete(
                self.store_in_knowledge_graph(text, final_response, user)
            )
            
            return final_response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return f"I encountered an error: {str(e)[:100]}. Let me try to help anyway - what do you need?"
    
    def _get_fallback_response(self, text, context=""):
        """Fallback response when Gemini is unavailable"""
        text_lower = text.lower()
        
        response = "I'm having trouble with my AI model, but "
        
        if context:
            response += f"I found this information:\n{context}\n\n"
        
        if 'hello' in text_lower or 'hi' in text_lower:
            response += "Hello! I'm Bob from Bob's House of AI. How can I help?"
        elif 'price' in text_lower:
            response += "For pricing, I recommend getting multiple quotes. "
            if context:
                response += "See the data above for typical prices."
        else:
            response += f"Regarding '{text}' - I'm here to help once my AI is back online."
        
        return response

# Initialize Bob
bob = BobFinal()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bob Final - Production',
        'version': '3.0.0',
        'model': 'Gemini 1.5 Flash' if bob.model else 'No model',
        'components': {
            'vertex_ai': bob.model is not None,
            'graphiti': bob.graphiti is not None,
            'bigquery_ml': bob.bq_client is not None,
            'firestore': bob.firestore_client is not None,
            'slack': bob.slack_client is not None
        },
        'project': bob.project_id,
        'timestamp': time.time()
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        
        # URL verification
        if data.get('type') == 'url_verification':
            return jsonify({'challenge': data['challenge']})
        
        # Handle events
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            event_id = data.get('event_id')
            
            # Prevent duplicates
            if event_id in bob.processed_events:
                return jsonify({'status': 'duplicate'})
            
            bob.processed_events.add(event_id)
            
            # Clean old events
            if len(bob.processed_events) > bob.max_events:
                bob.processed_events = set(list(bob.processed_events)[-500:])
            
            # Process messages
            if event.get('type') == 'message' and not event.get('bot_id'):
                text = event.get('text', '')
                channel = event.get('channel')
                user = event.get('user')
                
                # Process and respond
                response = bob.process_message(text, user, channel)
                
                # Send to Slack
                if bob.slack_client and channel:
                    try:
                        bob.slack_client.chat_postMessage(
                            channel=channel,
                            text=response
                        )
                        logger.info(f"✅ Responded in channel {channel}")
                    except SlackApiError as e:
                        logger.error(f"Slack error: {e}")
            
            # Handle mentions
            elif event.get('type') == 'app_mention':
                text = event.get('text', '')
                channel = event.get('channel')
                user = event.get('user')
                
                # Clean mention
                text = ' '.join(w for w in text.split() if not w.startswith('<@'))
                
                response = bob.process_message(text, user, channel)
                
                if bob.slack_client and channel:
                    try:
                        bob.slack_client.chat_postMessage(
                            channel=channel,
                            text=response
                        )
                    except SlackApiError as e:
                        logger.error(f"Slack error: {e}")
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Slack event error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET', 'POST'])
def test():
    """Test endpoint"""
    if request.method == 'POST':
        data = request.json or {}
        text = data.get('text', 'Hello Bob!')
    else:
        text = request.args.get('text', 'Hello Bob!')
    
    response = bob.process_message(text)
    
    return jsonify({
        'question': text,
        'response': response,
        'components_status': {
            'vertex_ai': '✅' if bob.model else '❌',
            'graphiti': '✅' if bob.graphiti else '❌',
            'bigquery_ml': '✅' if bob.bq_client else '❌',
            'firestore': '✅' if bob.firestore_client else '❌',
            'slack': '✅' if bob.slack_client else '❌'
        }
    })

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Bob\'s Brain - Final Production Version',
        'status': 'operational',
        'version': '3.0.0',
        'description': 'The definitive Bob with all integrations',
        'endpoints': {
            '/': 'This help message',
            '/health': 'Health check with component status',
            '/test': 'Test Bob\'s response',
            '/slack/events': 'Slack event handler'
        },
        'architecture': {
            'ai_model': 'Gemini 1.5 Flash (Vertex AI)',
            'knowledge_graph': 'Graphiti with Neo4j',
            'ml_predictions': 'BigQuery ML models',
            'data_storage': 'Firestore (1,100 documents)',
            'deployment': 'Google Cloud Run'
        },
        'features': [
            '✅ Gemini 1.5 Flash for natural language',
            '✅ Graphiti knowledge graph memory',
            '✅ BigQuery ML price predictions',
            '✅ Firestore data access',
            '✅ Slack integration',
            '✅ Duplicate message prevention',
            '✅ Async operations'
        ],
        'owner': 'Jeremy Longshore',
        'company': 'Bob\'s House of AI'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"🚀 Starting Bob Final on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)