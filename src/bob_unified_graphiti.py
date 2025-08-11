#!/usr/bin/env python3
"""
Bob with Graphiti as the Central Hub
Graphiti ties together Firestore, BigQuery, and Vertex AI
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from google.cloud import firestore
from google.cloud import bigquery
from graphiti_core import Graphiti
import vertexai
from vertexai.generative_models import GenerativeModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class BobUnifiedGraphiti:
    """Bob with Graphiti as the central brain connecting everything"""
    
    def __init__(self):
        # GRAPHITI IS THE BRAIN - Everything connects through it
        self.graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', 'BobBrain2025')
        )
        logger.info("🧠 Graphiti initialized as central brain")
        
        # Data Sources that feed into Graphiti
        self.firestore = firestore.Client(project='diagnostic-pro-mvp', database='bob-brain')
        self.bigquery = bigquery.Client(project='bobs-house-ai')
        
        # AI powered by Vertex
        vertexai.init(project='bobs-house-ai', location='us-central1')
        self.ai_model = GenerativeModel('gemini-1.5-flash')
        
        # Slack interface
        self.slack = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
        
        logger.info("✅ All systems connected through Graphiti hub")
    
    async def sync_everything_to_graphiti(self):
        """Sync all data sources into Graphiti knowledge graph"""
        
        # 1. Sync new Firestore customer submissions
        submissions = self.firestore.collection('diagnostic_submissions').where(
            'synced_to_graphiti', '==', False
        ).stream()
        
        for doc in submissions:
            data = doc.to_dict()
            
            # Create rich graph relationships
            episode = f"""
            Customer {data.get('customer_name', 'Unknown')} submitted a quote:
            - Vehicle: {data.get('vehicle_year')} {data.get('vehicle_make')} {data.get('vehicle_model')}
            - Repair: {data.get('repair_type')}
            - Shop: {data.get('shop_name')}
            - Quoted Price: ${data.get('quoted_price')}
            - Fair Price: ${data.get('fair_price', 'Unknown')}
            - Potential Savings: ${data.get('quoted_price', 0) - data.get('fair_price', 0)}
            """
            
            # Add to Graphiti with relationships
            await self.graphiti.add_episode(
                name=f"customer_submission_{doc.id}",
                episode_body=episode,
                source_description="Customer submission from website",
                reference_time=data.get('timestamp', datetime.now())
            )
            
            # Mark as synced
            doc.reference.update({'synced_to_graphiti': True})
            
            logger.info(f"✅ Synced customer {doc.id} to Graphiti")
        
        # 2. Sync BigQuery analytics insights
        query = """
        SELECT 
            shop_name,
            AVG(quoted_price - fair_price) as avg_overcharge,
            COUNT(*) as num_quotes
        FROM `diagnosticpro_analytics.diagnostic_submissions`
        WHERE DATE(timestamp) = CURRENT_DATE()
        GROUP BY shop_name
        HAVING avg_overcharge > 100
        """
        
        try:
            results = self.bigquery.query(query).result()
            for row in results:
                insight = f"""
                Shop Analysis: {row.shop_name}
                - Average overcharge: ${row.avg_overcharge:.2f}
                - Number of quotes analyzed: {row.num_quotes}
                - Classification: Potentially overcharging customers
                """
                
                await self.graphiti.add_episode(
                    name=f"shop_analysis_{row.shop_name}_{datetime.now().date()}",
                    episode_body=insight,
                    source_description="BigQuery analytics insight",
                    reference_time=datetime.now()
                )
        except Exception as e:
            logger.error(f"BigQuery sync error: {e}")
    
    async def think_with_graphiti(self, question: str):
        """Use Graphiti to understand question with full context"""
        
        # 1. Search Graphiti for relevant knowledge
        search_results = await self.graphiti.search(question, num_results=10)
        
        # 2. Build rich context from graph relationships
        context = "Relevant knowledge from Graphiti:\n"
        
        # Graphiti returns related nodes and relationships
        for result in search_results[:5]:
            context += f"- {str(result)[:200]}...\n"
        
        # 3. Get real-time stats from BigQuery through Graphiti's understanding
        if "average" in question.lower() or "typical" in question.lower():
            # Graphiti knows to check analytics
            query = """
            SELECT AVG(quoted_price) as avg_price, 
                   COUNT(*) as num_cases
            FROM `diagnosticpro_analytics.diagnostic_submissions`
            WHERE repair_type LIKE '%brake%'
            """
            try:
                bq_results = self.bigquery.query(query).result()
                for row in bq_results:
                    context += f"\nAnalytics: Average brake repair quote: ${row.avg_price:.2f} across {row.num_cases} cases\n"
            except:
                pass
        
        # 4. Get latest customer data if asking about recent
        if "recent" in question.lower() or "latest" in question.lower():
            recent = self.firestore.collection('diagnostic_submissions').order_by(
                'timestamp', direction=firestore.Query.DESCENDING
            ).limit(3).stream()
            
            context += "\nRecent submissions:\n"
            for doc in recent:
                data = doc.to_dict()
                context += f"- {data.get('vehicle_make')} {data.get('repair_type')}: ${data.get('quoted_price')}\n"
        
        return context
    
    async def process_message(self, text: str, user: str, channel: str):
        """Process message using Graphiti as the central brain"""
        
        # First, sync any new data to Graphiti
        await self.sync_everything_to_graphiti()
        
        # Use Graphiti to understand the question with full context
        context = await self.think_with_graphiti(text)
        
        # Generate response with Vertex AI
        prompt = f"""You are Bob, an AI assistant for DiagnosticPro.
        You have access to a knowledge graph that connects customer data, shop patterns, and pricing insights.
        
{context}

User Question: {text}

Provide a helpful response that:
1. Answers their question directly
2. Includes specific data when available
3. Mentions patterns or insights you've learned
4. Suggests next steps if appropriate

Bob:"""
        
        response = self.ai_model.generate_content(prompt)
        response_text = response.text
        
        # Store this conversation in Graphiti to learn from it
        await self.graphiti.add_episode(
            name=f"conversation_{datetime.now().isoformat()}",
            episode_body=f"User {user} asked: {text}\nBob responded: {response_text}\nContext used: {context[:500]}",
            source_description=f"Slack conversation in {channel}",
            reference_time=datetime.now()
        )
        
        # Also update Firestore for record keeping
        self.firestore.collection('bob_conversations').add({
            'user': user,
            'channel': channel,
            'question': text,
            'response': response_text,
            'timestamp': datetime.now(),
            'graphiti_context_used': len(context)
        })
        
        return response_text

# Initialize Bob with Graphiti as the hub
bob = BobUnifiedGraphiti()

@app.route('/health', methods=['GET'])
def health():
    """Health check showing Graphiti as the hub"""
    return jsonify({
        "status": "healthy",
        "architecture": "Graphiti-Centric",
        "brain": "Graphiti Knowledge Graph (Neo4j)",
        "data_sources": {
            "firestore": "Customer submissions",
            "bigquery": "Analytics and ML",
            "vertex_ai": "Intelligence"
        },
        "integration": "All connected through Graphiti"
    })

@app.route('/slack/events', methods=['POST'])
def slack_events():
    """Handle Slack events"""
    try:
        data = request.json
        
        if data.get('type') == 'url_verification':
            return jsonify({"challenge": data['challenge']})
        
        if data.get('type') == 'event_callback':
            event = data.get('event', {})
            
            if event.get('type') == 'message' and not event.get('bot_id'):
                user = event.get('user')
                text = event.get('text')
                channel = event.get('channel')
                
                # Process through Graphiti hub
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
        
        return jsonify({"status": "ok"})
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/learn', methods=['POST'])
def learn_pattern():
    """Endpoint to teach Bob new patterns through Graphiti"""
    try:
        data = request.json
        pattern = data.get('pattern')
        
        # Add pattern to Graphiti knowledge graph
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            bob.graphiti.add_episode(
                name=f"learned_pattern_{datetime.now().isoformat()}",
                episode_body=pattern,
                source_description="Manually taught pattern",
                reference_time=datetime.now()
            )
        )
        
        return jsonify({
            "status": "learned",
            "pattern": pattern,
            "stored_in": "Graphiti knowledge graph"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "service": "Bob's Brain",
        "version": "5.0 - Graphiti Unified",
        "architecture": "Graphiti-Centric Knowledge System",
        "description": "Graphiti ties together all data sources into one intelligent knowledge graph"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)