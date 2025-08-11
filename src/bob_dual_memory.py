#!/usr/bin/env python3
"""
Bob with Dual Memory System: Firestore (for live customer data) + Graphiti (for knowledge graph)
Keeps Firestore integrated for website data collection while using Graphiti for intelligence
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from google.cloud import firestore
from graphiti_core import Graphiti
import vertexai
from vertexai.generative_models import GenerativeModel

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobDualMemory:
    """Bob with both Firestore (customer data) and Graphiti (knowledge graph)"""
    
    def __init__(self):
        # Initialize Firestore for customer data
        self.firestore_client = firestore.Client(
            project='diagnostic-pro-mvp', 
            database='bob-brain'
        )
        logger.info("✅ Connected to Firestore for customer data")
        
        # Initialize Graphiti for knowledge graph
        if not os.environ.get('OPENAI_API_KEY'):
            os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY', 'sk-placeholder')
        
        self.graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', 'BobBrain2025')
        )
        logger.info("✅ Connected to Graphiti knowledge graph")
        
        # Initialize Vertex AI for responses
        vertexai.init(project='bobs-house-ai', location='us-central1')
        self.model = GenerativeModel('gemini-1.5-flash')
        
        # Slack client
        self.slack_client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        
        logger.info("✅ Bob initialized with Dual Memory System")
    
    async def check_firestore_for_new_data(self):
        """Check Firestore for new customer submissions"""
        try:
            # Check diagnostic_submissions for new data
            submissions = self.firestore_client.collection('diagnostic_submissions')
            recent_docs = submissions.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(5).stream()
            
            new_data = []
            for doc in recent_docs:
                data = doc.to_dict()
                # Check if this has been processed
                if not data.get('processed_by_bob', False):
                    new_data.append({
                        'id': doc.id,
                        'data': data,
                        'type': 'customer_submission'
                    })
            
            return new_data
        except Exception as e:
            logger.error(f"Error checking Firestore: {e}")
            return []
    
    async def sync_firestore_to_graphiti(self):
        """Sync new Firestore data to Graphiti knowledge graph"""
        new_data = await self.check_firestore_for_new_data()
        
        if new_data:
            logger.info(f"Found {len(new_data)} new customer submissions")
            
            for item in new_data:
                try:
                    # Add to Graphiti knowledge graph
                    await self.graphiti.add_episode(
                        name=f"customer_submission_{item['id']}",
                        episode_body=json.dumps(item['data']),
                        source_description="Customer submission from website",
                        reference_time=item['data'].get('timestamp', datetime.now())
                    )
                    
                    # Mark as processed in Firestore
                    doc_ref = self.firestore_client.collection('diagnostic_submissions').document(item['id'])
                    doc_ref.update({'processed_by_bob': True, 'processed_at': datetime.now()})
                    
                    logger.info(f"✅ Synced customer submission {item['id']}")
                    
                except Exception as e:
                    logger.error(f"Failed to sync {item['id']}: {e}")
    
    async def search_all_memory(self, query):
        """Search both Firestore and Graphiti for relevant information"""
        results = {
            'graphiti': [],
            'firestore': [],
            'customer_data': []
        }
        
        # Search Graphiti knowledge graph
        try:
            graphiti_results = await self.graphiti.search(query, num_results=5)
            results['graphiti'] = graphiti_results[:3] if graphiti_results else []
        except Exception as e:
            logger.error(f"Graphiti search error: {e}")
        
        # Search Firestore knowledge collection
        try:
            knowledge_col = self.firestore_client.collection('knowledge')
            # Simple text search (in production, use proper indexing)
            docs = knowledge_col.limit(100).stream()
            
            for doc in docs:
                data = doc.to_dict()
                content = data.get('content', '')
                if query.lower() in content.lower():
                    results['firestore'].append({
                        'id': doc.id,
                        'content': content[:200],
                        'metadata': data.get('metadata', {})
                    })
                    if len(results['firestore']) >= 3:
                        break
        except Exception as e:
            logger.error(f"Firestore search error: {e}")
        
        # Check for customer-specific data
        try:
            # Search diagnostic_submissions for customer issues
            submissions = self.firestore_client.collection('diagnostic_submissions')
            recent = submissions.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(10).stream()
            
            for doc in recent:
                data = doc.to_dict()
                if query.lower() in str(data).lower():
                    results['customer_data'].append({
                        'id': doc.id,
                        'summary': f"Customer: {data.get('customer_name', 'Unknown')} - {data.get('issue', 'No issue')}",
                        'timestamp': data.get('timestamp')
                    })
        except Exception as e:
            logger.error(f"Customer data search error: {e}")
        
        return results
    
    async def process_message(self, text: str, user: str, channel: str):
        """Process a message using both memory systems"""
        try:
            # First, sync any new customer data
            await self.sync_firestore_to_graphiti()
            
            # Search all memory systems
            search_results = await self.search_all_memory(text)
            
            # Build context from all sources
            context = "Context from memory systems:\n\n"
            
            if search_results['graphiti']:
                context += "Knowledge Graph:\n"
                for result in search_results['graphiti'][:2]:
                    context += f"- {str(result)[:150]}...\n"
            
            if search_results['firestore']:
                context += "\nHistorical Knowledge:\n"
                for result in search_results['firestore'][:2]:
                    context += f"- {result['content'][:150]}...\n"
            
            if search_results['customer_data']:
                context += "\nRecent Customer Data:\n"
                for result in search_results['customer_data'][:2]:
                    context += f"- {result['summary']}\n"
            
            # Generate response with Vertex AI
            prompt = f"""You are Bob, an AI assistant for DiagnosticPro.
            You have access to both historical knowledge and live customer data.
            
{context}

User: {text}
Bob (respond helpfully, mentioning relevant customer data if applicable):"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Store this interaction in both systems
            # 1. Add to Graphiti knowledge graph
            await self.graphiti.add_episode(
                name=f"conversation_{datetime.now().isoformat()}",
                episode_body=f"User {user}: {text}\nBob: {response_text}",
                source_description=f"Slack conversation in {channel}",
                reference_time=datetime.now()
            )
            
            # 2. Add to Firestore for persistence
            self.firestore_client.collection('bob_conversations').add({
                'user': user,
                'channel': channel,
                'user_message': text,
                'bob_response': response_text,
                'timestamp': datetime.now(),
                'context_used': {
                    'graphiti_results': len(search_results['graphiti']),
                    'firestore_results': len(search_results['firestore']),
                    'customer_data': len(search_results['customer_data'])
                }
            })
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "I'm having trouble accessing my memory systems. Let me try again."

# Initialize Bob with Dual Memory
bob = BobDualMemory()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Bob's Brain with Dual Memory",
        "memory_systems": {
            "firestore": "Connected (Customer Data)",
            "graphiti": "Connected (Knowledge Graph)",
            "sync": "Active"
        },
        "ai": "Vertex AI (Gemini)"
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

@app.route('/sync', methods=['POST'])
def sync_data():
    """Manual sync endpoint for Firestore to Graphiti"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bob.sync_firestore_to_graphiti())
        
        return jsonify({
            "status": "success",
            "message": "Firestore data synced to Graphiti"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/customer-webhook', methods=['POST'])
def customer_webhook():
    """Webhook endpoint for website to send customer data directly"""
    try:
        data = request.json
        
        # Store in Firestore
        doc_ref = bob.firestore_client.collection('diagnostic_submissions').add({
            'customer_name': data.get('name'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'vehicle': data.get('vehicle'),
            'issue': data.get('issue'),
            'quote': data.get('quote'),
            'timestamp': datetime.now(),
            'source': 'website_webhook',
            'processed_by_bob': False
        })
        
        # Trigger sync to Graphiti
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bob.sync_firestore_to_graphiti())
        
        return jsonify({
            "status": "success",
            "message": "Customer data received and processed",
            "id": doc_ref[1].id
        })
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        "service": "Bob's Brain",
        "version": "3.0",
        "features": [
            "Dual Memory System",
            "Firestore (Customer Data)",
            "Graphiti (Knowledge Graph)",
            "Real-time Sync",
            "Vertex AI",
            "Slack Integration",
            "Customer Webhook"
        ]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)