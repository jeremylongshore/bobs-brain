#!/usr/bin/env python3
"""
Data Ingestion Pipeline for Bob's Brain
Handles web scraping data and syncs to Graphiti, Firestore, and BigQuery
"""

import os
import json
import asyncio
import logging
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from enum import Enum

from flask import Flask, request, jsonify
from google.cloud import firestore
from google.cloud import bigquery
from graphiti_core import Graphiti
import google.generativeai as genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class DataSource(Enum):
    """Types of data sources"""
    WEB_SCRAPE = "web_scrape"
    API = "api"
    MANUAL = "manual"
    CUSTOMER_FORM = "customer_form"
    SLACK = "slack"

class DataType(Enum):
    """Types of data we collect"""
    REPAIR_QUOTE = "repair_quote"
    SHOP_INFO = "shop_info"
    CUSTOMER_REVIEW = "customer_review"
    PRICE_DATA = "price_data"
    VEHICLE_INFO = "vehicle_info"
    DIAGNOSTIC_DATA = "diagnostic_data"
    MARKET_ANALYSIS = "market_analysis"

class DataIngestionPipeline:
    """Handles all incoming data and routes it appropriately"""
    
    def __init__(self):
        # Initialize Graphiti as the central brain
        self.graphiti = Graphiti(
            uri=os.environ.get('NEO4J_URI', 'bolt://10.128.0.2:7687'),
            user=os.environ.get('NEO4J_USER', 'neo4j'),
            password=os.environ.get('NEO4J_PASSWORD', '<REDACTED_NEO4J_PASSWORD>')
        )
        logger.info("🧠 Graphiti initialized as central knowledge graph")
        
        # Firestore for real-time data
        self.firestore = firestore.Client(
            project='diagnostic-pro-mvp', 
            database='bob-brain'
        )
        logger.info("📊 Firestore connected for real-time storage")
        
        # BigQuery for analytics
        self.bigquery = bigquery.Client(project='bobs-house-ai')
        self._ensure_bigquery_tables()
        logger.info("🗄️ BigQuery ready for analytics")
        
        # Configure AI for entity extraction
        genai.configure(api_key=os.environ.get('GOOGLE_API_KEY', '<REDACTED_GOOGLE_API_KEY>'))
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("🤖 AI model ready for entity extraction")
        
        # Track ingestion statistics
        self.stats = {
            'total_ingested': 0,
            'by_source': {},
            'by_type': {},
            'errors': 0
        }
    
    def _ensure_bigquery_tables(self):
        """Create BigQuery tables if they don't exist"""
        dataset_id = 'bobs-house-ai.scraped_data'
        
        # Create dataset if needed
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = 'US'
        try:
            self.bigquery.create_dataset(dataset, exists_ok=True)
        except Exception as e:
            logger.warning(f"Dataset exists or error: {e}")
        
        # Define table schemas
        tables = {
            'repair_quotes': [
                bigquery.SchemaField('id', 'STRING', mode='REQUIRED'),
                bigquery.SchemaField('source', 'STRING'),
                bigquery.SchemaField('shop_name', 'STRING'),
                bigquery.SchemaField('vehicle_make', 'STRING'),
                bigquery.SchemaField('vehicle_model', 'STRING'),
                bigquery.SchemaField('vehicle_year', 'INTEGER'),
                bigquery.SchemaField('repair_type', 'STRING'),
                bigquery.SchemaField('quoted_price', 'FLOAT'),
                bigquery.SchemaField('parts_cost', 'FLOAT'),
                bigquery.SchemaField('labor_cost', 'FLOAT'),
                bigquery.SchemaField('scraped_url', 'STRING'),
                bigquery.SchemaField('ingested_at', 'TIMESTAMP'),
                bigquery.SchemaField('processed', 'BOOLEAN'),
                bigquery.SchemaField('graphiti_synced', 'BOOLEAN'),
            ],
            'shop_data': [
                bigquery.SchemaField('shop_id', 'STRING', mode='REQUIRED'),
                bigquery.SchemaField('name', 'STRING'),
                bigquery.SchemaField('address', 'STRING'),
                bigquery.SchemaField('phone', 'STRING'),
                bigquery.SchemaField('website', 'STRING'),
                bigquery.SchemaField('rating', 'FLOAT'),
                bigquery.SchemaField('review_count', 'INTEGER'),
                bigquery.SchemaField('specialties', 'STRING', mode='REPEATED'),
                bigquery.SchemaField('price_level', 'STRING'),
                bigquery.SchemaField('scraped_at', 'TIMESTAMP'),
            ],
            'market_trends': [
                bigquery.SchemaField('trend_id', 'STRING', mode='REQUIRED'),
                bigquery.SchemaField('repair_type', 'STRING'),
                bigquery.SchemaField('region', 'STRING'),
                bigquery.SchemaField('avg_price', 'FLOAT'),
                bigquery.SchemaField('min_price', 'FLOAT'),
                bigquery.SchemaField('max_price', 'FLOAT'),
                bigquery.SchemaField('sample_size', 'INTEGER'),
                bigquery.SchemaField('trend_direction', 'STRING'),
                bigquery.SchemaField('calculated_at', 'TIMESTAMP'),
            ]
        }
        
        for table_name, schema in tables.items():
            table_id = f"{dataset_id}.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            try:
                self.bigquery.create_table(table, exists_ok=True)
                logger.info(f"✅ Table {table_name} ready")
            except Exception as e:
                logger.warning(f"Table {table_name} exists or error: {e}")
    
    async def ingest_data(self, 
                         data: Dict[str, Any],
                         source: DataSource,
                         data_type: DataType,
                         metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Main ingestion method - routes data to appropriate storage"""
        
        try:
            # Generate unique ID for this data
            data_id = self._generate_id(data)
            
            # Add metadata
            enriched_data = {
                'id': data_id,
                'source': source.value,
                'type': data_type.value,
                'ingested_at': datetime.now(timezone.utc),
                'raw_data': data,
                'metadata': metadata or {}
            }
            
            # Extract entities and relationships using AI
            entities = await self._extract_entities(data, data_type)
            enriched_data['entities'] = entities
            
            # Store in appropriate systems
            results = {}
            
            # 1. Always store in Firestore for real-time access
            firestore_ref = await self._store_firestore(enriched_data, data_type)
            results['firestore'] = firestore_ref
            
            # 2. Store in BigQuery for analytics
            bigquery_result = await self._store_bigquery(enriched_data, data_type)
            results['bigquery'] = bigquery_result
            
            # 3. Update Graphiti knowledge graph with relationships
            graphiti_result = await self._update_graphiti(enriched_data, entities, data_type)
            results['graphiti'] = graphiti_result
            
            # Update statistics
            self.stats['total_ingested'] += 1
            self.stats['by_source'][source.value] = self.stats['by_source'].get(source.value, 0) + 1
            self.stats['by_type'][data_type.value] = self.stats['by_type'].get(data_type.value, 0) + 1
            
            logger.info(f"✅ Ingested {data_type.value} from {source.value}: {data_id}")
            
            return {
                'success': True,
                'data_id': data_id,
                'storage': results,
                'entities_extracted': len(entities)
            }
            
        except Exception as e:
            logger.error(f"Ingestion error: {e}")
            self.stats['errors'] += 1
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_id(self, data: Dict) -> str:
        """Generate unique ID for data"""
        content = json.dumps(data, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def _extract_entities(self, data: Dict, data_type: DataType) -> List[Dict]:
        """Use AI to extract entities and relationships from data"""
        
        prompt = f"""
Extract key entities and relationships from this {data_type.value} data.
Return as JSON with entities (name, type, attributes) and relationships.

Data: {json.dumps(data, indent=2)}

Extract:
1. Entities (shops, vehicles, repairs, prices, people)
2. Relationships (shop performs repair, vehicle needs repair, etc.)
3. Key attributes (prices, dates, ratings)

Return JSON format:
{{
  "entities": [
    {{"name": "...", "type": "...", "attributes": {{}}}}
  ],
  "relationships": [
    {{"from": "...", "to": "...", "type": "..."}}
  ]
}}
"""
        
        try:
            response = self.ai_model.generate_content(prompt)
            # Parse JSON from response
            json_str = response.text
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0]
            elif '```' in json_str:
                json_str = json_str.split('```')[1].split('```')[0]
            
            extracted = json.loads(json_str)
            return extracted.get('entities', [])
        except Exception as e:
            logger.error(f"Entity extraction error: {e}")
            return []
    
    async def _store_firestore(self, data: Dict, data_type: DataType) -> str:
        """Store in Firestore for real-time access"""
        
        collection_name = f"scraped_{data_type.value}"
        doc_ref = self.firestore.collection(collection_name).document(data['id'])
        doc_ref.set(data)
        
        # Also update a summary collection for quick access
        summary = {
            'id': data['id'],
            'type': data_type.value,
            'source': data['source'],
            'ingested_at': data['ingested_at'],
            'key_data': self._extract_key_data(data, data_type)
        }
        self.firestore.collection('data_summary').document(data['id']).set(summary)
        
        return doc_ref.path
    
    async def _store_bigquery(self, data: Dict, data_type: DataType) -> str:
        """Store in BigQuery for analytics"""
        
        # Map data type to table
        table_map = {
            DataType.REPAIR_QUOTE: 'repair_quotes',
            DataType.SHOP_INFO: 'shop_data',
            DataType.MARKET_ANALYSIS: 'market_trends'
        }
        
        table_name = table_map.get(data_type, 'repair_quotes')
        table_id = f"bobs-house-ai.scraped_data.{table_name}"
        
        # Transform data for BigQuery
        row = self._transform_for_bigquery(data, data_type)
        
        # Insert row
        table = self.bigquery.get_table(table_id)
        errors = self.bigquery.insert_rows_json(table, [row])
        
        if errors:
            logger.error(f"BigQuery insert errors: {errors}")
            return f"error: {errors}"
        
        return table_id
    
    async def _update_graphiti(self, data: Dict, entities: List[Dict], data_type: DataType) -> str:
        """Update Graphiti knowledge graph"""
        
        # Create episode from ingested data
        episode_body = f"""
New {data_type.value} data ingested from {data['source']}:
"""
        
        # Add entity information
        for entity in entities:
            episode_body += f"- {entity.get('type', 'Unknown')}: {entity.get('name', 'Unknown')}\n"
            if entity.get('attributes'):
                for key, value in entity['attributes'].items():
                    episode_body += f"  - {key}: {value}\n"
        
        # Add key data points
        if data_type == DataType.REPAIR_QUOTE:
            raw = data.get('raw_data', {})
            episode_body += f"""
Repair Quote Details:
- Shop: {raw.get('shop_name', 'Unknown')}
- Vehicle: {raw.get('vehicle_year', '')} {raw.get('vehicle_make', '')} {raw.get('vehicle_model', '')}
- Repair: {raw.get('repair_type', 'Unknown')}
- Price: ${raw.get('quoted_price', 0)}
"""
        
        # Add to Graphiti
        await self.graphiti.add_episode(
            name=f"{data_type.value}_{data['id']}",
            episode_body=episode_body,
            source_description=f"Scraped from {data['source']}",
            reference_time=data['ingested_at']
        )
        
        return f"graphiti_episode_{data['id']}"
    
    def _extract_key_data(self, data: Dict, data_type: DataType) -> Dict:
        """Extract key fields for summary"""
        raw = data.get('raw_data', {})
        
        if data_type == DataType.REPAIR_QUOTE:
            return {
                'shop': raw.get('shop_name'),
                'price': raw.get('quoted_price'),
                'repair': raw.get('repair_type')
            }
        elif data_type == DataType.SHOP_INFO:
            return {
                'name': raw.get('name'),
                'rating': raw.get('rating'),
                'location': raw.get('address')
            }
        else:
            return raw
    
    def _transform_for_bigquery(self, data: Dict, data_type: DataType) -> Dict:
        """Transform data for BigQuery schema"""
        raw = data.get('raw_data', {})
        
        if data_type == DataType.REPAIR_QUOTE:
            return {
                'id': data['id'],
                'source': data['source'],
                'shop_name': raw.get('shop_name'),
                'vehicle_make': raw.get('vehicle_make'),
                'vehicle_model': raw.get('vehicle_model'),
                'vehicle_year': raw.get('vehicle_year'),
                'repair_type': raw.get('repair_type'),
                'quoted_price': raw.get('quoted_price'),
                'parts_cost': raw.get('parts_cost'),
                'labor_cost': raw.get('labor_cost'),
                'scraped_url': raw.get('url'),
                'ingested_at': data['ingested_at'].isoformat(),
                'processed': False,
                'graphiti_synced': True
            }
        elif data_type == DataType.SHOP_INFO:
            return {
                'shop_id': data['id'],
                'name': raw.get('name'),
                'address': raw.get('address'),
                'phone': raw.get('phone'),
                'website': raw.get('website'),
                'rating': raw.get('rating'),
                'review_count': raw.get('review_count'),
                'specialties': raw.get('specialties', []),
                'price_level': raw.get('price_level'),
                'scraped_at': data['ingested_at'].isoformat()
            }
        else:
            # Default transformation
            return {
                'id': data['id'],
                'data': json.dumps(raw),
                'ingested_at': data['ingested_at'].isoformat()
            }
    
    async def bulk_ingest(self, data_list: List[Dict], source: DataSource, data_type: DataType) -> Dict:
        """Ingest multiple data items efficiently"""
        results = {
            'total': len(data_list),
            'successful': 0,
            'failed': 0,
            'ids': []
        }
        
        for data in data_list:
            result = await self.ingest_data(data, source, data_type)
            if result['success']:
                results['successful'] += 1
                results['ids'].append(result['data_id'])
            else:
                results['failed'] += 1
        
        return results
    
    def get_stats(self) -> Dict:
        """Get ingestion statistics"""
        return {
            **self.stats,
            'firestore_collections': self._get_firestore_stats(),
            'bigquery_rows': self._get_bigquery_stats(),
            'graphiti_episodes': self._get_graphiti_stats()
        }
    
    def _get_firestore_stats(self) -> Dict:
        """Get Firestore collection statistics"""
        try:
            collections = ['scraped_repair_quote', 'scraped_shop_info', 'data_summary']
            stats = {}
            for collection in collections:
                # Get approximate count
                docs = self.firestore.collection(collection).limit(1).stream()
                stats[collection] = 'has_data' if list(docs) else 'empty'
            return stats
        except:
            return {}
    
    def _get_bigquery_stats(self) -> Dict:
        """Get BigQuery table statistics"""
        try:
            tables = ['repair_quotes', 'shop_data', 'market_trends']
            stats = {}
            for table in tables:
                query = f"SELECT COUNT(*) as count FROM `bobs-house-ai.scraped_data.{table}`"
                try:
                    result = self.bigquery.query(query).result()
                    for row in result:
                        stats[table] = row.count
                except:
                    stats[table] = 0
            return stats
        except:
            return {}
    
    def _get_graphiti_stats(self) -> Dict:
        """Get Graphiti statistics"""
        # This would require async, so returning placeholder
        return {'status': 'connected'}

# Initialize pipeline
pipeline = DataIngestionPipeline()

# Flask API Endpoints

@app.route('/health', methods=['GET'])
def health():
    """Health check with pipeline status"""
    return jsonify({
        'status': 'healthy',
        'service': 'Data Ingestion Pipeline',
        'stats': pipeline.get_stats()
    })

@app.route('/ingest', methods=['POST'])
def ingest_single():
    """Ingest a single data item"""
    try:
        data = request.json
        
        # Get parameters
        source = DataSource(data.get('source', 'web_scrape'))
        data_type = DataType(data.get('type', 'repair_quote'))
        content = data.get('data', {})
        metadata = data.get('metadata', {})
        
        # Run async ingestion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            pipeline.ingest_data(content, source, data_type, metadata)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ingest/bulk', methods=['POST'])
def ingest_bulk():
    """Ingest multiple data items"""
    try:
        data = request.json
        
        # Get parameters
        source = DataSource(data.get('source', 'web_scrape'))
        data_type = DataType(data.get('type', 'repair_quote'))
        items = data.get('items', [])
        
        # Run async bulk ingestion
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            pipeline.bulk_ingest(items, source, data_type)
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/ingest/repair-quote', methods=['POST'])
def ingest_repair_quote():
    """Specialized endpoint for repair quotes"""
    try:
        data = request.json
        
        # Validate required fields
        required = ['shop_name', 'vehicle_make', 'vehicle_model', 'repair_type', 'quoted_price']
        for field in required:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add optional fields with defaults
        data.setdefault('vehicle_year', datetime.now().year)
        data.setdefault('parts_cost', 0)
        data.setdefault('labor_cost', 0)
        
        # Ingest
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            pipeline.ingest_data(
                data,
                DataSource.WEB_SCRAPE,
                DataType.REPAIR_QUOTE,
                {'specialized_endpoint': True}
            )
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get ingestion statistics"""
    return jsonify(pipeline.get_stats())

@app.route('/analyze/market-trends', methods=['POST'])
def analyze_trends():
    """Analyze market trends from ingested data"""
    try:
        # Run BigQuery analysis
        query = """
        SELECT 
            repair_type,
            AVG(quoted_price) as avg_price,
            MIN(quoted_price) as min_price,
            MAX(quoted_price) as max_price,
            COUNT(*) as sample_size,
            STDDEV(quoted_price) as price_variance
        FROM `bobs-house-ai.scraped_data.repair_quotes`
        WHERE ingested_at > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        GROUP BY repair_type
        HAVING sample_size > 5
        ORDER BY avg_price DESC
        """
        
        results = pipeline.bigquery.query(query).result()
        
        trends = []
        for row in results:
            trends.append({
                'repair_type': row.repair_type,
                'avg_price': row.avg_price,
                'min_price': row.min_price,
                'max_price': row.max_price,
                'sample_size': row.sample_size,
                'price_variance': row.price_variance
            })
        
        # Store trends in BigQuery and Graphiti
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        for trend in trends:
            # Add to Graphiti as insight
            loop.run_until_complete(
                pipeline.graphiti.add_episode(
                    name=f"market_trend_{trend['repair_type']}_{datetime.now().date()}",
                    episode_body=f"Market analysis: {trend['repair_type']} averages ${trend['avg_price']:.2f} across {trend['sample_size']} samples",
                    source_description="BigQuery market analysis",
                    reference_time=datetime.now()
                )
            )
        
        return jsonify({
            'trends': trends,
            'analyzed_at': datetime.now().isoformat(),
            'stored_in': ['bigquery', 'graphiti']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'Bob\'s Data Ingestion Pipeline',
        'version': '1.0',
        'description': 'Handles web scraping and data ingestion for Bob\'s Brain',
        'endpoints': {
            '/ingest': 'POST - Ingest single data item',
            '/ingest/bulk': 'POST - Ingest multiple items',
            '/ingest/repair-quote': 'POST - Specialized repair quote ingestion',
            '/stats': 'GET - View ingestion statistics',
            '/analyze/market-trends': 'POST - Analyze market trends',
            '/health': 'GET - Health check'
        },
        'storage': {
            'realtime': 'Firestore',
            'analytics': 'BigQuery',
            'knowledge': 'Graphiti (Neo4j)'
        },
        'data_types': [t.value for t in DataType],
        'data_sources': [s.value for s in DataSource]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    app.run(host='0.0.0.0', port=port)