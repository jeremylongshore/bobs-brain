#!/usr/bin/env python3
"""
Real Graphiti Integration for Bob's Brain Circle of Life
Using graphiti-core from Zep for temporal knowledge graphs
"""

import os
import json
import logging
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

# Neo4j driver
from neo4j import GraphDatabase

# Google Cloud
from google.cloud import bigquery
import google.generativeai as genai

logger = logging.getLogger(__name__)


class GraphitiMemory:
    """
    Graphiti-compatible memory system for Bob's Brain
    Since graphiti-core requires specific LLM providers, we'll implement
    a compatible interface that works with our Google Gemini setup
    """
    
    def __init__(self):
        # Neo4j Aura connection
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE")
        
        # Initialize Neo4j driver
        try:
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            self.driver.verify_connectivity()
            logger.info(f"✅ Graphiti connected to Neo4j at {self.neo4j_uri}")
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            self.driver = None
        
        # Initialize Gemini for entity extraction
        try:
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY", ""))
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("✅ Gemini configured for entity extraction")
        except Exception as e:
            logger.warning(f"Gemini not configured: {e}")
            self.model = None
        
        # BigQuery for analytics
        try:
            self.bq_client = bigquery.Client(project="bobs-house-ai")
            logger.info("✅ BigQuery connected")
        except Exception as e:
            logger.warning(f"BigQuery not configured: {e}")
            self.bq_client = None
    
    def add_episode(self, 
                   content: str,
                   source: str = "scraper",
                   metadata: Dict = None,
                   timestamp: datetime = None) -> str:
        """
        Add an episode to the knowledge graph
        Compatible with Graphiti's episode concept
        """
        if not self.driver:
            logger.error("Neo4j not connected")
            return None
        
        # Generate episode ID
        episode_id = hashlib.md5(
            f"{content}_{timestamp or datetime.now()}".encode()
        ).hexdigest()
        
        if timestamp is None:
            timestamp = datetime.now()
        
        # Extract entities and relationships
        entities, relationships = self._extract_knowledge(content)
        
        with self.driver.session() as session:
            # Create Episode node
            episode_query = """
            MERGE (e:Episode {id: $id})
            SET e.content = $content,
                e.source = $source,
                e.timestamp = $timestamp,
                e.metadata = $metadata,
                e.t_valid = $timestamp,
                e.t_invalid = null
            RETURN e
            """
            
            session.run(
                episode_query,
                id=episode_id,
                content=content[:10000],  # Limit content size
                source=source,
                timestamp=timestamp.isoformat(),
                metadata=json.dumps(metadata) if metadata else "{}"
            )
            
            # Create Entity nodes
            for entity in entities:
                entity_query = """
                MERGE (n:Entity {name: $name})
                SET n.type = $type,
                    n.last_seen = $timestamp
                WITH n
                MATCH (e:Episode {id: $episode_id})
                MERGE (e)-[r:MENTIONS {
                    confidence: $confidence,
                    t_valid: $timestamp,
                    t_invalid: null
                }]->(n)
                """
                
                session.run(
                    entity_query,
                    name=entity['name'],
                    type=entity['type'],
                    confidence=entity.get('confidence', 1.0),
                    timestamp=timestamp.isoformat(),
                    episode_id=episode_id
                )
            
            # Create Relationships between entities
            for rel in relationships:
                rel_query = """
                MATCH (e1:Entity {name: $source})
                MATCH (e2:Entity {name: $target})
                MERGE (e1)-[r:RELATES_TO {
                    type: $rel_type,
                    t_valid: $timestamp,
                    t_invalid: null,
                    episode_id: $episode_id
                }]->(e2)
                """
                
                session.run(
                    rel_query,
                    source=rel['source'],
                    target=rel['target'],
                    rel_type=rel['type'],
                    timestamp=timestamp.isoformat(),
                    episode_id=episode_id
                )
            
            logger.info(f"✅ Added episode {episode_id} with {len(entities)} entities")
        
        # Sync to BigQuery for analytics
        self._sync_to_bigquery(episode_id, content, source, entities, relationships, metadata)
        
        return episode_id
    
    def search(self, 
              query: str,
              num_results: int = 10,
              point_in_time: datetime = None) -> List[Dict]:
        """
        Search the knowledge graph
        Supports temporal queries like Graphiti
        """
        if not self.driver:
            return []
        
        results = []
        
        with self.driver.session() as session:
            if point_in_time:
                # Temporal query - get state at specific time
                search_query = """
                MATCH (e:Episode)
                WHERE toLower(e.content) CONTAINS toLower($query)
                  AND datetime(e.timestamp) <= datetime($point_in_time)
                  AND (e.t_invalid IS NULL OR datetime(e.t_invalid) > datetime($point_in_time))
                OPTIONAL MATCH (e)-[:MENTIONS]->(entity:Entity)
                RETURN e.id as id,
                       e.content as content,
                       e.source as source,
                       e.timestamp as timestamp,
                       e.metadata as metadata,
                       collect(DISTINCT entity.name) as entities
                ORDER BY e.timestamp DESC
                LIMIT $limit
                """
                
                result = session.run(
                    search_query,
                    query=query,
                    point_in_time=point_in_time.isoformat(),
                    limit=num_results
                )
            else:
                # Current state query
                search_query = """
                MATCH (e:Episode)
                WHERE toLower(e.content) CONTAINS toLower($query)
                  AND e.t_invalid IS NULL
                OPTIONAL MATCH (e)-[:MENTIONS]->(entity:Entity)
                RETURN e.id as id,
                       e.content as content,
                       e.source as source,
                       e.timestamp as timestamp,
                       e.metadata as metadata,
                       collect(DISTINCT entity.name) as entities
                ORDER BY e.timestamp DESC
                LIMIT $limit
                """
                
                result = session.run(
                    search_query,
                    query=query,
                    limit=num_results
                )
            
            for record in result:
                results.append({
                    'id': record['id'],
                    'content': record['content'],
                    'source': record['source'],
                    'timestamp': record['timestamp'],
                    'metadata': json.loads(record['metadata']) if record['metadata'] else {},
                    'entities': record['entities']
                })
        
        return results
    
    def get_entity_history(self, entity_name: str) -> List[Dict]:
        """
        Get the temporal history of an entity
        Shows how it evolved over time
        """
        if not self.driver:
            return []
        
        history = []
        
        with self.driver.session() as session:
            query = """
            MATCH (e:Entity {name: $name})<-[r:MENTIONS]-(episode:Episode)
            RETURN episode.id as episode_id,
                   episode.content as content,
                   episode.timestamp as timestamp,
                   r.confidence as confidence,
                   r.t_valid as valid_from,
                   r.t_invalid as valid_until
            ORDER BY episode.timestamp DESC
            """
            
            result = session.run(query, name=entity_name)
            
            for record in result:
                history.append({
                    'episode_id': record['episode_id'],
                    'content': record['content'],
                    'timestamp': record['timestamp'],
                    'confidence': record['confidence'],
                    'valid_from': record['valid_from'],
                    'valid_until': record['valid_until']
                })
        
        return history
    
    def build_context(self, query: str, max_context_items: int = 5) -> str:
        """
        Build context for Bob's responses using the knowledge graph
        This is the key Circle of Life integration point
        """
        # Search for relevant episodes
        episodes = self.search(query, num_results=max_context_items)
        
        if not episodes:
            return ""
        
        # Build context string
        context_parts = ["Relevant knowledge from the Circle of Life:\n"]
        
        for episode in episodes:
            context_parts.append(f"- {episode['content'][:200]}...")
            if episode['entities']:
                context_parts.append(f"  Entities: {', '.join(episode['entities'][:5])}")
        
        return "\n".join(context_parts)
    
    def _extract_knowledge(self, content: str) -> tuple:
        """
        Extract entities and relationships from content
        Uses Gemini if available, otherwise pattern matching
        """
        entities = []
        relationships = []
        
        if self.model:
            # Use Gemini for extraction
            try:
                prompt = f"""Extract entities and relationships from this text.
                Return JSON with format:
                {{
                    "entities": [
                        {{"name": "entity_name", "type": "entity_type", "confidence": 0.9}}
                    ],
                    "relationships": [
                        {{"source": "entity1", "target": "entity2", "type": "relationship_type"}}
                    ]
                }}
                
                Text: {content[:2000]}
                """
                
                response = self.model.generate_content(prompt)
                
                # Parse response
                try:
                    data = json.loads(response.text)
                    entities = data.get('entities', [])
                    relationships = data.get('relationships', [])
                except:
                    # Fallback to pattern matching
                    pass
                    
            except Exception as e:
                logger.error(f"Gemini extraction failed: {e}")
        
        # Fallback or enhancement with pattern matching
        if not entities:
            entities = self._extract_entities_pattern(content)
        
        return entities, relationships
    
    def _extract_entities_pattern(self, content: str) -> List[Dict]:
        """
        Extract entities using pattern matching
        """
        import re
        
        entities = []
        
        # Equipment brands
        brands = ['Bobcat', 'Caterpillar', 'John Deere', 'Ford', 'Cummins', 'Duramax']
        for brand in brands:
            if brand.lower() in content.lower():
                entities.append({
                    'name': brand,
                    'type': 'Equipment',
                    'confidence': 0.9
                })
        
        # Error codes
        error_codes = re.findall(r'\b[PC][0-9A-F]{4}\b', content.upper())
        for code in error_codes:
            entities.append({
                'name': code,
                'type': 'ErrorCode',
                'confidence': 0.95
            })
        
        # Part numbers
        part_numbers = re.findall(r'\b[A-Z]{2,4}[0-9]{2,}-[0-9A-Z]{4,}\b', content.upper())
        for part in part_numbers:
            entities.append({
                'name': part,
                'type': 'Part',
                'confidence': 0.85
            })
        
        return entities
    
    def _sync_to_bigquery(self, episode_id: str, content: str, source: str,
                         entities: List, relationships: List, metadata: Dict):
        """
        Sync episode data to BigQuery for analytics
        """
        if not self.bq_client:
            return
        
        try:
            # Create dataset if needed
            dataset_id = "bobs-house-ai.graphiti_memory"
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"
            
            self.bq_client.create_dataset(dataset, exists_ok=True)
            
            # Create table if needed
            table_id = f"{dataset_id}.episodes"
            
            schema = [
                bigquery.SchemaField("episode_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("content", "STRING"),
                bigquery.SchemaField("source", "STRING"),
                bigquery.SchemaField("entity_count", "INTEGER"),
                bigquery.SchemaField("relationship_count", "INTEGER"),
                bigquery.SchemaField("metadata", "JSON"),
                bigquery.SchemaField("created_at", "TIMESTAMP"),
            ]
            
            table = bigquery.Table(table_id, schema=schema)
            self.bq_client.create_table(table, exists_ok=True)
            
            # Insert episode record
            rows_to_insert = [{
                "episode_id": episode_id,
                "content": content[:10000],
                "source": source,
                "entity_count": len(entities),
                "relationship_count": len(relationships),
                "metadata": metadata,
                "created_at": datetime.utcnow()
            }]
            
            errors = self.bq_client.insert_rows_json(table_id, rows_to_insert)
            
            if errors:
                logger.error(f"BigQuery insert errors: {errors}")
            else:
                logger.info(f"✅ Synced episode {episode_id} to BigQuery")
                
        except Exception as e:
            logger.error(f"BigQuery sync error: {e}")
    
    def get_statistics(self) -> Dict:
        """
        Get knowledge graph statistics
        """
        if not self.driver:
            return {}
        
        stats = {}
        
        with self.driver.session() as session:
            # Count nodes
            node_query = """
            MATCH (n)
            RETURN labels(n)[0] as label, count(n) as count
            """
            
            result = session.run(node_query)
            stats['nodes'] = {record['label']: record['count'] for record in result}
            
            # Count relationships
            rel_query = """
            MATCH ()-[r]->()
            RETURN type(r) as type, count(r) as count
            """
            
            result = session.run(rel_query)
            stats['relationships'] = {record['type']: record['count'] for record in result}
            
            # Get recent episodes
            recent_query = """
            MATCH (e:Episode)
            RETURN count(e) as total,
                   max(datetime(e.timestamp)) as latest
            """
            
            result = session.run(recent_query)
            record = result.single()
            if record:
                stats['episodes'] = {
                    'total': record['total'],
                    'latest': record['latest'].isoformat() if record['latest'] else None
                }
        
        return stats


# Integration with Circle of Life
class CircleOfLifeGraphiti:
    """
    Integration layer between scrapers and Graphiti memory
    This completes the Circle of Life
    """
    
    def __init__(self):
        self.memory = GraphitiMemory()
    
    def process_scraped_data(self, items: List[Dict]) -> int:
        """
        Process scraped items and add to knowledge graph
        """
        processed = 0
        
        for item in items:
            try:
                # Combine title and content for episode
                content = f"{item.get('title', '')}\n{item.get('content', '')}"
                
                # Create metadata
                metadata = {
                    'url': item.get('url', ''),
                    'source_type': item.get('source_type', ''),
                    'equipment_brand': item.get('equipment_brand', ''),
                    'error_codes': item.get('error_codes', []),
                    'part_numbers': item.get('part_numbers', [])
                }
                
                # Add episode to Graphiti
                episode_id = self.memory.add_episode(
                    content=content,
                    source=item.get('source', 'unknown'),
                    metadata=metadata,
                    timestamp=datetime.now()
                )
                
                if episode_id:
                    processed += 1
                    logger.info(f"✅ Added to Graphiti: {item.get('title', 'Unknown')[:50]}")
                    
            except Exception as e:
                logger.error(f"Error processing item: {e}")
                continue
        
        logger.info(f"✅ Circle of Life: Processed {processed}/{len(items)} items into Graphiti")
        return processed
    
    def get_context_for_bob(self, user_query: str) -> str:
        """
        Get context from Graphiti for Bob's responses
        """
        return self.memory.build_context(user_query)
    
    def learn_from_conversation(self, user_message: str, bob_response: str):
        """
        Add conversation to the knowledge graph for learning
        """
        content = f"User: {user_message}\nBob: {bob_response}"
        
        metadata = {
            'type': 'conversation',
            'user_message': user_message,
            'bob_response': bob_response
        }
        
        episode_id = self.memory.add_episode(
            content=content,
            source='bob_conversation',
            metadata=metadata
        )
        
        logger.info(f"✅ Learned from conversation: {episode_id}")
        return episode_id


if __name__ == "__main__":
    # Test the Graphiti integration
    import asyncio
    
    async def test():
        # Initialize
        graphiti = CircleOfLifeGraphiti()
        
        # Test adding episode
        test_item = {
            'title': 'How to Fix Bobcat S740 Hydraulic Problems',
            'content': 'When error code 9809-31 appears, check the hydraulic pump pressure...',
            'url': 'https://example.com/repair',
            'source': 'Test',
            'source_type': 'manual',
            'equipment_brand': 'Bobcat',
            'error_codes': ['9809-31'],
            'part_numbers': ['7023037']
        }
        
        processed = graphiti.process_scraped_data([test_item])
        print(f"Processed {processed} items")
        
        # Test search
        context = graphiti.get_context_for_bob("Bobcat hydraulic error")
        print(f"Context: {context}")
        
        # Get statistics
        stats = graphiti.memory.get_statistics()
        print(f"Stats: {json.dumps(stats, indent=2)}")
    
    asyncio.run(test())