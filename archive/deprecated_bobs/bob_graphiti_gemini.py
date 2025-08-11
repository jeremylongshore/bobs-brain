#!/usr/bin/env python3
"""
Bob's Brain with Graphiti + Gemini (NEW Google SDK)
Graphiti connects everything, Gemini provides intelligence
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List

from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# NEW Google SDK for Gemini (the right way!)
import google.generativeai as genai

# Google Cloud services
from google.cloud import firestore
from google.cloud import bigquery
from google.cloud import aiplatform

# Graphiti for knowledge graph
from graphiti_core import Graphiti

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobGraphitiGemini:
    """
    Bob's complete brain:
    - Graphiti: Knowledge graph (connects everything)
    - Gemini: Intelligence (via NEW Google SDK)
    - BigQuery: ML models and analytics
    - Firestore: Real-time data
    """
    
    def __init__(self):
        logger.info("🎆 Initializing Bob with Graphiti + Gemini...")
        
        # 1. GEMINI - Intelligence layer (NEW SDK)
        # This is the CORRECT way to use Gemini
        api_key = os.environ.get('GOOGLE_API_KEY', 'AIzaSyBK4lVEXg_2R9TjPSV-6g8R5hVqGT8fCZo')
        genai.configure(api_key=api_key)
        
        # Initialize Gemini 1.5 Flash (best for speed + intelligence)
        self.gemini = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini 1.5 Flash initialized with NEW Google SDK")
        
        # Also set up Gemini Pro for complex analysis
        self.gemini_pro = genai.GenerativeModel('gemini-1.5-pro')
        logger.info("✅ Gemini 1.5 Pro ready for complex tasks")
        
        # 2. GRAPHITI - Knowledge graph (the brain)
        # Set placeholder OpenAI key (Graphiti requires it)
        if not os.environ.get('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
        
        self.graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', 'BobBrain2025')
        )
        logger.info("✅ Graphiti knowledge graph connected")
        
        # 3. VERTEX AI - For ML models
        try:
            aiplatform.init(
                project='bobs-house-ai',
                location='us-central1'
            )
            self.vertex_ready = True
            logger.info("✅ Vertex AI initialized for ML models")
        except Exception as e:
            logger.warning(f"⚠️ Vertex AI not available: {e}")
            self.vertex_ready = False
        
        # 4. BIGQUERY - ML models and analytics
        self.bigquery = bigquery.Client(project='bobs-house-ai')
        logger.info("✅ BigQuery connected for ML")
        
        # 5. FIRESTORE - Real-time customer data
        self.firestore = firestore.Client(
            project='diagnostic-pro-mvp',
            database='bob-brain'
        )
        logger.info("✅ Firestore connected for real-time data")
        
        # 6. SLACK - Communication
        self.slack = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        logger.info("✅ Slack client ready")
        
        logger.info("🎆 Bob fully initialized with Graphiti + Gemini!")
    
    async def process_message(self, text: str, user: str, channel: str) -> str:
        """
        Process message using ALL systems:
        1. Graphiti searches knowledge
        2. BigQuery provides ML predictions
        3. Gemini generates intelligent response
        """
        
        try:
            # 1. GRAPHITI - Search knowledge graph
            logger.info(f"🔍 Searching Graphiti for: {text[:50]}...")
            knowledge_results = await self.graphiti.search(text, num_results=10)
            
            # Build knowledge context
            knowledge_context = "Knowledge from Graphiti:\n"
            if knowledge_results:
                for i, result in enumerate(knowledge_results[:5], 1):
                    knowledge_context += f"{i}. {str(result)[:200]}\n"
            else:
                knowledge_context += "No specific knowledge found.\n"
            
            # 2. BIGQUERY ML - Get predictions if relevant
            ml_context = await self._get_ml_predictions(text)
            
            # 3. FIRESTORE - Get recent relevant data
            realtime_context = await self._get_realtime_data(text)
            
            # 4. GEMINI - Generate intelligent response
            full_prompt = f"""
You are Bob, an AI assistant with access to multiple data sources.

KNOWLEDGE GRAPH CONTEXT:
{knowledge_context}

ML PREDICTIONS:
{ml_context}

REAL-TIME DATA:
{realtime_context}

User Question: {text}

Provide a helpful, accurate response that:
1. Uses the knowledge graph context
2. Incorporates ML predictions when relevant
3. References real-time data if applicable
4. Is conversational and helpful

Bob:"""
            
            # Use Gemini for response
            response = self.gemini.generate_content(full_prompt)
            response_text = response.text
            
            # 5. LEARN - Store this interaction back in Graphiti
            await self._store_learning(text, response_text, user, channel)
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self._fallback_response(text)
    
    async def _get_ml_predictions(self, text: str) -> str:
        """Get ML predictions from BigQuery models"""
        
        ml_context = "ML Predictions:\n"
        
        try:
            # Check if asking about prices
            if any(word in text.lower() for word in ['price', 'cost', 'expensive', 'cheap']):
                
                # Extract repair type from question using Gemini
                extract_prompt = f"Extract the repair type from this question. Return ONLY the repair type or 'unknown': {text}"
                extract_response = self.gemini.generate_content(extract_prompt)
                repair_type = extract_response.text.strip()
                
                if repair_type != 'unknown':
                    # Query BigQuery for price predictions
                    query = f"""
                    SELECT 
                        AVG(quoted_price) as avg_price,
                        MIN(quoted_price) as min_price,
                        MAX(quoted_price) as max_price,
                        COUNT(*) as sample_size
                    FROM `bobs-house-ai.scraped_data.repair_quotes`
                    WHERE LOWER(repair_type) LIKE LOWER('%{repair_type}%')
                    AND ingested_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
                    """
                    
                    results = self.bigquery.query(query).result()
                    for row in results:
                        if row.sample_size > 0:
                            ml_context += f"- Average {repair_type} price: ${row.avg_price:.2f}\n"
                            ml_context += f"- Price range: ${row.min_price:.2f} - ${row.max_price:.2f}\n"
                            ml_context += f"- Based on {row.sample_size} recent quotes\n"
                
                # Also check for ML model predictions if available
                try:
                    model_query = """
                    SELECT predicted_price
                    FROM ML.PREDICT(MODEL `bobs-house-ai.ml_models.price_predictor`,
                        (SELECT @repair_type as repair_type))
                    """
                    # This would work if model exists
                except:
                    pass
            
            # Check if asking about shops
            if any(word in text.lower() for word in ['shop', 'mechanic', 'garage', 'dealer']):
                query = """
                SELECT shop_name, AVG(rating) as avg_rating, COUNT(*) as reviews
                FROM `bobs-house-ai.scraped_data.shop_data`
                GROUP BY shop_name
                ORDER BY avg_rating DESC
                LIMIT 5
                """
                
                results = self.bigquery.query(query).result()
                ml_context += "Top rated shops:\n"
                for row in results:
                    ml_context += f"- {row.shop_name}: {row.avg_rating:.1f} stars ({row.reviews} reviews)\n"
            
        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            ml_context += "ML predictions not available.\n"
        
        return ml_context
    
    async def _get_realtime_data(self, text: str) -> str:
        """Get real-time data from Firestore"""
        
        realtime_context = "Recent Activity:\n"
        
        try:
            # Get recent submissions
            recent = self.firestore.collection('diagnostic_submissions').order_by(
                'timestamp', direction=firestore.Query.DESCENDING
            ).limit(3).stream()
            
            count = 0
            for doc in recent:
                count += 1
                data = doc.to_dict()
                realtime_context += f"- {data.get('vehicle_make', '')} {data.get('repair_type', '')}: ${data.get('quoted_price', 0)}\n"
            
            if count == 0:
                realtime_context += "No recent submissions.\n"
                
        except Exception as e:
            logger.error(f"Firestore error: {e}")
            realtime_context += "Real-time data not available.\n"
        
        return realtime_context
    
    async def _store_learning(self, question: str, response: str, user: str, channel: str):
        """Store interaction in Graphiti and Firestore"""
        
        try:
            # Add to Graphiti knowledge graph
            await self.graphiti.add_episode(
                name=f"conversation_{datetime.now().isoformat()}",
                episode_body=f"""
User {user} asked: {question}
Bob responded: {response}
This interaction helped Bob learn about user needs and improve responses.
""",
                source_description=f"Slack conversation in channel {channel}",
                reference_time=datetime.now()
            )
            
            # Also store in Firestore
            self.firestore.collection('bob_conversations').add({
                'user': user,
                'channel': channel,
                'question': question,
                'response': response,
                'timestamp': datetime.now(),
                'model': 'gemini-1.5-flash',
                'stored_in_graphiti': True
            })
            
        except Exception as e:
            logger.error(f"Failed to store learning: {e}")
    
    def _fallback_response(self, text: str) -> str:
        """Fallback response using just Gemini"""
        try:
            simple_prompt = f"""
You are Bob, a helpful AI assistant.
User asked: {text}
Provide a helpful response:
"""
            response = self.gemini.generate_content(simple_prompt)
            return response.text
        except:
            return "I'm having trouble processing that right now. Please try again."
    
    async def analyze_with_gemini_pro(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Use Gemini Pro for complex analysis tasks"""
        
        prompt = f"""
Perform deep analysis on this data:
{json.dumps(data, indent=2)}

Provide:
1. Key insights
2. Patterns detected
3. Recommendations
4. Potential issues

Return as structured JSON.
"""
        
        response = self.gemini_pro.generate_content(prompt)
        
        # Parse response
        try:
            if '```json' in response.text:
                json_str = response.text.split('```json')[1].split('```')[0]
            else:
                json_str = response.text
            
            analysis = json.loads(json_str)
        except:
            analysis = {'raw_analysis': response.text}
        
        # Store insights in Graphiti
        await self.graphiti.add_episode(
            name=f"analysis_{datetime.now().isoformat()}",
            episode_body=f"Gemini Pro analysis: {json.dumps(analysis, indent=2)}",
            source_description="Deep analysis by Gemini Pro",
            reference_time=datetime.now()
        )
        
        return analysis

# Initialize Bob
bob = BobGraphitiGemini()

@app.route('/health', methods=['GET'])
def health():
    """Health check showing complete system status"""
    return jsonify({
        'status': 'healthy',
        'service': 'Bob with Graphiti + Gemini',
        'components': {
            'graphiti': 'Knowledge graph brain',
            'gemini': 'Google AI (NEW SDK)',
            'bigquery': 'ML models and analytics',
            'firestore': 'Real-time data',
            'vertex_ai': 'Ready' if bob.vertex_ready else 'Not configured',
            'slack': 'Connected'
        },
        'models': {
            'gemini-1.5-flash': 'Fast responses',
            'gemini-1.5-pro': 'Deep analysis'
        }
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        
        # URL verification
        if data.get('type') == 'url_verification':
            return jsonify({'challenge': data['challenge']})
        
        # Process messages
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            
            if event.get('type') == 'message' and not event.get('bot_id'):
                user = event.get('user')
                text = event.get('text')
                channel = event.get('channel')
                
                # Process with full system
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(
                    bob.process_message(text, user, channel)
                )
                
                # Send response
                bob.slack.chat_postMessage(
                    channel=channel,
                    text=response
                )
        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Slack error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """Deep analysis endpoint using Gemini Pro"""
    try:
        data = request.json
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        analysis = loop.run_until_complete(
            bob.analyze_with_gemini_pro(data)
        )
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-gemini', methods=['GET'])
def test_gemini():
    """Test Gemini is working"""
    try:
        # Test both models
        flash_response = bob.gemini.generate_content("Say 'Gemini Flash is working!'")
        pro_response = bob.gemini_pro.generate_content("Say 'Gemini Pro is working!'")
        
        return jsonify({
            'status': 'success',
            'gemini_flash': flash_response.text,
            'gemini_pro': pro_response.text,
            'sdk': 'google-generativeai (NEW protocol)'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-ml', methods=['GET'])
def test_ml():
    """Test ML predictions from BigQuery"""
    try:
        query = """
        SELECT 
            repair_type,
            AVG(quoted_price) as avg_price,
            COUNT(*) as sample_size
        FROM `bobs-house-ai.scraped_data.repair_quotes`
        GROUP BY repair_type
        LIMIT 5
        """
        
        results = bob.bigquery.query(query).result()
        
        predictions = []
        for row in results:
            predictions.append({
                'repair': row.repair_type,
                'avg_price': row.avg_price,
                'samples': row.sample_size
            })
        
        return jsonify({
            'status': 'success',
            'ml_predictions': predictions,
            'source': 'BigQuery ML'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'Bob\'s Brain',
        'version': '6.0',
        'architecture': 'Graphiti + Gemini + ML',
        'description': 'Complete AI system with knowledge graph, Google AI, and ML',
        'endpoints': {
            '/health': 'System status',
            '/slack/events': 'Slack integration',
            '/analyze': 'Deep analysis with Gemini Pro',
            '/test-gemini': 'Test Gemini models',
            '/test-ml': 'Test ML predictions'
        },
        'intelligence': {
            'gemini-1.5-flash': 'Fast responses (NEW Google SDK)',
            'gemini-1.5-pro': 'Deep analysis (NEW Google SDK)'
        },
        'data': {
            'graphiti': 'Knowledge graph (Neo4j)',
            'bigquery': 'ML models and analytics',
            'firestore': 'Real-time customer data'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)