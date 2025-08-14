#!/usr/bin/env python3
"""
Complete Unified Scraper for Circle of Life
Integrates YouTube (yt-dlp), Reddit (PRAW), RSS feeds, and Graphiti
This is the holistic scraper that feeds Bob's Brain ecosystem
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Optional

# Third-party imports
import feedparser
import praw
import requests
import yt_dlp
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from google.cloud import bigquery
from neo4j import GraphDatabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app for Cloud Run
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=4)


# Import the real Graphiti integration
try:
    from graphiti_integration import CircleOfLifeGraphiti
    GRAPHITI_AVAILABLE = True
except ImportError:
    logger.warning("Graphiti integration not available, using fallback")
    GRAPHITI_AVAILABLE = False

class GraphitiIntegration:
    """Graphiti integration for knowledge graph management"""
    
    def __init__(self):
        if GRAPHITI_AVAILABLE:
            try:
                self.graphiti = CircleOfLifeGraphiti()
                self.driver = self.graphiti.memory.driver
                logger.info("✅ Using real Graphiti integration")
            except Exception as e:
                logger.error(f"Graphiti init failed: {e}")
                self._init_fallback()
        else:
            self._init_fallback()
    
    def _init_fallback(self):
        """Fallback to direct Neo4j connection"""
        # Neo4j connection (using Aura)
        self.neo4j_uri = os.getenv("NEO4J_URI", "neo4j+s://d3653283.databases.neo4j.io")
        self.neo4j_user = os.getenv("NEO4J_USER", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "q9eazAmPqXsv0KSnnjiX6Q-UvXXPKIUCZbkC7P5VOAE")
        self.graphiti = None
        
        try:
            self.driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            self.driver.verify_connectivity()
            logger.info(f"✅ Connected to Neo4j at {self.neo4j_uri}")
        except Exception as e:
            logger.error(f"❌ Neo4j connection failed: {e}")
            self.driver = None
    
    def add_knowledge(self, data: Dict):
        """Add scraped knowledge to Neo4j graph"""
        # Use real Graphiti if available
        if self.graphiti:
            try:
                processed = self.graphiti.process_scraped_data([data])
                if processed > 0:
                    logger.info(f"✅ Added via Graphiti: {data.get('title', 'Unknown')[:50]}")
                return
            except Exception as e:
                logger.error(f"Graphiti processing error: {e}")
        
        # Fallback to direct Neo4j
        if not self.driver:
            return
        
        try:
            with self.driver.session() as session:
                # Create content node
                content_id = hashlib.md5(f"{data.get('url', '')}_{datetime.now()}".encode()).hexdigest()
                
                query = """
                MERGE (c:Content {id: $id})
                SET c.title = $title,
                    c.content = $content,
                    c.url = $url,
                    c.source = $source,
                    c.source_type = $source_type,
                    c.scraped_at = $scraped_at
                """
                
                session.run(query, 
                    id=content_id,
                    title=data.get('title', ''),
                    content=data.get('content', '')[:5000],  # Limit content size
                    url=data.get('url', ''),
                    source=data.get('source', ''),
                    source_type=data.get('source_type', ''),
                    scraped_at=datetime.utcnow().isoformat()
                )
                
                # Create entity relationships
                self._create_entities(session, content_id, data)
                
                logger.info(f"✅ Added to Neo4j: {data.get('title', 'Unknown')[:50]}")
                
        except Exception as e:
            logger.error(f"Neo4j insert error: {e}")
    
    def _create_entities(self, session, content_id: str, data: Dict):
        """Extract and create entity nodes with relationships"""
        
        # Equipment entities
        if data.get('equipment_brand'):
            query = """
            MATCH (c:Content {id: $content_id})
            MERGE (e:Equipment {name: $name, brand: $brand})
            MERGE (c)-[:MENTIONS]->(e)
            """
            session.run(query,
                content_id=content_id,
                name=data.get('equipment_model', data['equipment_brand']),
                brand=data['equipment_brand']
            )
        
        # Error code entities
        for code in data.get('error_codes', []):
            query = """
            MATCH (c:Content {id: $content_id})
            MERGE (e:ErrorCode {code: $code})
            MERGE (c)-[:REFERENCES]->(e)
            """
            session.run(query, content_id=content_id, code=code)
        
        # Part number entities
        for part in data.get('part_numbers', []):
            query = """
            MATCH (c:Content {id: $content_id})
            MERGE (p:Part {number: $part})
            MERGE (c)-[:MENTIONS_PART]->(p)
            """
            session.run(query, content_id=content_id, part=part)


class YouTubeScraper:
    """YouTube scraper using yt-dlp for transcript extraction"""
    
    def __init__(self):
        self.ydl_opts = {
            'skip_download': True,  # Don't download video
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        # Priority channels for equipment repair
        self.channels = {
            'Pine Hollow Auto Diagnostics': 'UCn4Ifss-t3wMT6VBzQoKPUA',
            'Scanner Danner': 'UCtAixbt3jqKDfOTWU_qauXQ',
            'South Main Auto': 'UCJnJ5SqDUIJK8OGdeFhDL6g',
            'FarmCraft101': 'UC3mERhm6W3WjEDy0JKZPMmA',
            'Bobcat Company': 'UCZNk7Jjb2t8EuBsdsDRXJnA',
            'Diesel Tech Ron': 'UC7Px2cqDnkMrymoHj4Du7IA',
        }
    
    def scrape_channel(self, channel_name: str, channel_id: str, max_videos: int = 5) -> List[Dict]:
        """Scrape recent videos from a channel"""
        results = []
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Get channel videos
                channel_url = f"https://www.youtube.com/channel/{channel_id}/videos"
                
                logger.info(f"📺 Scraping YouTube channel: {channel_name}")
                
                # Extract channel info
                info = ydl.extract_info(channel_url, download=False)
                
                if 'entries' in info:
                    for entry in info['entries'][:max_videos]:
                        if entry:
                            video_data = self._process_video(entry, channel_name)
                            if video_data:
                                results.append(video_data)
                
                logger.info(f"   ✅ Scraped {len(results)} videos from {channel_name}")
                
        except Exception as e:
            logger.error(f"YouTube scraping error for {channel_name}: {e}")
        
        return results
    
    def _process_video(self, video_info: Dict, channel_name: str) -> Optional[Dict]:
        """Process video info and extract knowledge"""
        try:
            # Extract basic info
            video_data = {
                'video_id': video_info.get('id'),
                'title': video_info.get('title', ''),
                'url': f"https://www.youtube.com/watch?v={video_info.get('id')}",
                'channel': channel_name,
                'description': video_info.get('description', ''),
                'source': f"YouTube - {channel_name}",
                'source_type': 'youtube',
                'duration': video_info.get('duration'),
                'view_count': video_info.get('view_count'),
                'upload_date': video_info.get('upload_date'),
            }
            
            # Combine title and description for analysis
            full_text = f"{video_data['title']} {video_data['description']}"
            
            # Extract knowledge
            video_data.update(self._extract_knowledge(full_text))
            
            return video_data
            
        except Exception as e:
            logger.error(f"Video processing error: {e}")
            return None
    
    def _extract_knowledge(self, text: str) -> Dict:
        """Extract equipment knowledge from text"""
        knowledge = {
            'error_codes': [],
            'part_numbers': [],
            'equipment_brand': None,
            'equipment_model': None,
            'repair_type': None,
        }
        
        # Extract error codes
        error_patterns = [
            r'\b[PC][0-9A-F]{4}\b',  # P0087, C0234
            r'\bU[0-9]{4}\b',         # U codes
            r'\bB[0-9]{4}\b',         # Body codes
        ]
        
        for pattern in error_patterns:
            codes = re.findall(pattern, text.upper())
            knowledge['error_codes'].extend(codes)
        
        # Extract part numbers
        part_patterns = [
            r'\b[A-Z]{2,4}[0-9]{2,}-[0-9A-Z]{4,}\b',  # BC3Z-9A543-B
            r'\b[0-9]{5,}-[0-9]{2,}\b',               # 12345-67
        ]
        
        for pattern in part_patterns:
            parts = re.findall(pattern, text.upper())
            knowledge['part_numbers'].extend(parts)
        
        # Extract equipment brands
        brands = ['Bobcat', 'Caterpillar', 'John Deere', 'Ford', 'Cummins', 'Duramax']
        text_lower = text.lower()
        
        for brand in brands:
            if brand.lower() in text_lower:
                knowledge['equipment_brand'] = brand
                break
        
        # Categorize repair type
        if any(word in text_lower for word in ['hydraulic', 'pump', 'cylinder']):
            knowledge['repair_type'] = 'hydraulic'
        elif any(word in text_lower for word in ['engine', 'motor', 'piston']):
            knowledge['repair_type'] = 'engine'
        elif any(word in text_lower for word in ['electrical', 'wiring', 'battery']):
            knowledge['repair_type'] = 'electrical'
        
        return knowledge


class RedditScraper:
    """Reddit scraper using PRAW"""
    
    def __init__(self):
        # Reddit API credentials
        self.client_id = os.getenv('REDDIT_CLIENT_ID', '')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET', '')
        
        self.reddit = None
        if self.client_id and self.client_secret:
            try:
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    user_agent='BobsBrain/1.0 Equipment Knowledge Bot'
                )
                self.reddit.read_only = True
                logger.info("✅ Reddit API configured")
            except Exception as e:
                logger.error(f"Reddit API error: {e}")
        else:
            logger.warning("⚠️ Reddit API not configured - set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
        
        # Target subreddits
        self.subreddits = [
            'MechanicAdvice',
            'Diesel',
            'Skidsteers',
            'HeavyEquipment',
            'Justrolledintotheshop',
            'tractors',
        ]
    
    def scrape_subreddit(self, subreddit_name: str, limit: int = 10) -> List[Dict]:
        """Scrape posts from a subreddit"""
        if not self.reddit:
            return []
        
        results = []
        
        try:
            logger.info(f"📱 Scraping Reddit: r/{subreddit_name}")
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get hot posts
            for submission in subreddit.hot(limit=limit):
                post_data = self._process_post(submission, subreddit_name)
                if post_data:
                    results.append(post_data)
            
            logger.info(f"   ✅ Scraped {len(results)} posts from r/{subreddit_name}")
            
        except Exception as e:
            logger.error(f"Reddit scraping error for r/{subreddit_name}: {e}")
        
        return results
    
    def _process_post(self, submission, subreddit_name: str) -> Optional[Dict]:
        """Process Reddit post"""
        try:
            # Combine title and selftext
            content = f"{submission.title}\n{submission.selftext}"
            
            post_data = {
                'title': submission.title,
                'content': content[:5000],  # Limit content size
                'url': f"https://reddit.com{submission.permalink}",
                'source': f"Reddit - r/{subreddit_name}",
                'source_type': 'reddit',
                'score': submission.score,
                'num_comments': submission.num_comments,
                'created_utc': datetime.fromtimestamp(submission.created_utc).isoformat(),
            }
            
            # Extract knowledge (reuse YouTube extractor logic)
            yt_scraper = YouTubeScraper()
            post_data.update(yt_scraper._extract_knowledge(content))
            
            return post_data
            
        except Exception as e:
            logger.error(f"Reddit post processing error: {e}")
            return None


class RSSFeedScraper:
    """RSS feed scraper for equipment news and blogs"""
    
    def __init__(self):
        self.feeds = [
            {
                "name": "Equipment World",
                "url": "https://www.equipmentworld.com/feed/",
                "category": "construction"
            },
            {
                "name": "Diesel Progress",
                "url": "https://www.dieselprogress.com/feed/",
                "category": "diesel"
            },
            {
                "name": "Heavy Equipment Guide",
                "url": "https://www.heavyequipmentguide.ca/feed",
                "category": "heavy_equipment"
            },
            {
                "name": "For Construction Pros",
                "url": "https://www.forconstructionpros.com/rss/",
                "category": "construction"
            },
            {
                "name": "Compact Equipment Magazine",
                "url": "https://compactequip.com/feed/",
                "category": "compact"
            },
        ]
    
    def scrape_feed(self, feed_info: Dict, limit: int = 10) -> List[Dict]:
        """Scrape RSS feed"""
        results = []
        
        try:
            logger.info(f"📰 Scraping RSS: {feed_info['name']}")
            feed = feedparser.parse(feed_info['url'])
            
            if not feed.entries:
                logger.warning(f"No entries in {feed_info['name']}")
                return results
            
            for entry in feed.entries[:limit]:
                try:
                    item_data = {
                        'title': entry.get('title', ''),
                        'content': entry.get('summary', '')[:5000],
                        'url': entry.get('link', ''),
                        'source': feed_info['name'],
                        'source_type': 'rss',
                        'category': feed_info['category'],
                        'published': entry.get('published', ''),
                    }
                    
                    # Extract knowledge
                    yt_scraper = YouTubeScraper()
                    item_data.update(yt_scraper._extract_knowledge(
                        f"{item_data['title']} {item_data['content']}"
                    ))
                    
                    results.append(item_data)
                    
                except Exception as e:
                    logger.error(f"RSS entry error: {e}")
                    continue
            
            logger.info(f"   ✅ Scraped {len(results)} items from {feed_info['name']}")
            
        except Exception as e:
            logger.error(f"RSS feed error for {feed_info['name']}: {e}")
        
        return results


class UnifiedScraperComplete:
    """Complete unified scraper integrating all sources"""
    
    def __init__(self):
        self.project_id = "bobs-house-ai"
        
        # Initialize components
        self.graphiti = GraphitiIntegration()
        self.youtube_scraper = YouTubeScraper()
        self.reddit_scraper = RedditScraper()
        self.rss_scraper = RSSFeedScraper()
        
        # BigQuery client
        try:
            self.bq_client = bigquery.Client(project=self.project_id)
            self._init_bigquery_tables()
            logger.info("✅ BigQuery initialized")
        except Exception as e:
            logger.error(f"BigQuery init error: {e}")
            self.bq_client = None
    
    def _init_bigquery_tables(self):
        """Initialize BigQuery dataset and tables"""
        if not self.bq_client:
            return
        
        # Create dataset
        dataset_id = f"{self.project_id}.circle_of_life"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset ready: {dataset_id}")
        except Exception as e:
            logger.error(f"Dataset error: {e}")
        
        # Create unified knowledge table
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("url", "STRING"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),
            bigquery.SchemaField("equipment_brand", "STRING"),
            bigquery.SchemaField("equipment_model", "STRING"),
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("part_numbers", "STRING", mode="REPEATED"),
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            bigquery.SchemaField("metadata", "JSON"),
        ]
        
        table_id = f"{dataset_id}.unified_knowledge"
        table = bigquery.Table(table_id, schema=schema)
        
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table ready: unified_knowledge")
        except Exception as e:
            logger.error(f"Table error: {e}")
    
    def store_to_bigquery(self, items: List[Dict]) -> int:
        """Store items to BigQuery"""
        if not self.bq_client or not items:
            return 0
        
        table_id = f"{self.project_id}.circle_of_life.unified_knowledge"
        stored = 0
        
        for item in items:
            try:
                # Generate ID
                item['id'] = hashlib.md5(f"{item.get('url', '')}_{datetime.now()}".encode()).hexdigest()
                item['scraped_at'] = datetime.utcnow()
                
                # Store to BigQuery
                errors = self.bq_client.insert_rows_json(table_id, [item])
                
                if not errors:
                    stored += 1
                    
                    # Also store to Neo4j via Graphiti
                    self.graphiti.add_knowledge(item)
                else:
                    logger.error(f"BigQuery errors: {errors}")
                    
            except Exception as e:
                logger.error(f"Storage error: {e}")
                continue
        
        logger.info(f"✅ Stored {stored}/{len(items)} items to BigQuery and Neo4j")
        return stored
    
    async def scrape_all_sources(self) -> Dict:
        """Scrape all data sources"""
        logger.info("🚀 Starting Circle of Life unified scraping...")
        
        all_items = []
        results = {
            'youtube': 0,
            'reddit': 0,
            'rss': 0,
            'total': 0,
            'stored': 0
        }
        
        # Use ThreadPoolExecutor for concurrent scraping
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            # YouTube scraping
            for channel_name, channel_id in self.youtube_scraper.channels.items():
                future = executor.submit(self.youtube_scraper.scrape_channel, channel_name, channel_id, 3)
                futures.append(('youtube', future))
            
            # Reddit scraping
            for subreddit in self.reddit_scraper.subreddits:
                future = executor.submit(self.reddit_scraper.scrape_subreddit, subreddit, 5)
                futures.append(('reddit', future))
            
            # RSS scraping
            for feed in self.rss_scraper.feeds:
                future = executor.submit(self.rss_scraper.scrape_feed, feed, 10)
                futures.append(('rss', future))
            
            # Collect results
            for source_type, future in futures:
                try:
                    items = future.result(timeout=30)
                    if items:
                        all_items.extend(items)
                        results[source_type] += len(items)
                except Exception as e:
                    logger.error(f"Scraping error for {source_type}: {e}")
        
        # Store all items
        results['total'] = len(all_items)
        results['stored'] = self.store_to_bigquery(all_items)
        
        logger.info(f"✅ Circle of Life complete: {results['total']} items scraped, {results['stored']} stored")
        logger.info(f"   YouTube: {results['youtube']}, Reddit: {results['reddit']}, RSS: {results['rss']}")
        
        return results


# Flask API Routes
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Circle of Life Unified Scraper',
        'components': {
            'youtube': bool(YouTubeScraper().channels),
            'reddit': bool(os.getenv('REDDIT_CLIENT_ID')),
            'graphiti': bool(GraphitiIntegration().driver),
        },
        'timestamp': datetime.utcnow().isoformat()
    })


@app.route('/scrape', methods=['POST'])
def scrape_all():
    """Scrape all sources endpoint"""
    try:
        def run_scraping():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = UnifiedScraperComplete()
            return loop.run_until_complete(scraper.scrape_all_sources())
        
        future = executor.submit(run_scraping)
        results = future.result(timeout=300)  # 5 minute timeout
        
        return jsonify({
            'success': True,
            'results': results,
            'message': f"Circle of Life: {results['total']} items processed"
        })
        
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/scrape/youtube', methods=['POST'])
def scrape_youtube():
    """Scrape YouTube only"""
    try:
        data = request.get_json() or {}
        channel = data.get('channel', 'Pine Hollow Auto Diagnostics')
        
        scraper = YouTubeScraper()
        channel_id = scraper.channels.get(channel)
        
        if not channel_id:
            return jsonify({'error': f'Unknown channel: {channel}'}), 400
        
        items = scraper.scrape_channel(channel, channel_id, 5)
        
        # Store results
        unified = UnifiedScraperComplete()
        stored = unified.store_to_bigquery(items)
        
        return jsonify({
            'success': True,
            'channel': channel,
            'scraped': len(items),
            'stored': stored
        })
        
    except Exception as e:
        logger.error(f"YouTube scrape error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/scrape/reddit', methods=['POST'])
def scrape_reddit():
    """Scrape Reddit only"""
    try:
        data = request.get_json() or {}
        subreddit = data.get('subreddit', 'MechanicAdvice')
        
        scraper = RedditScraper()
        items = scraper.scrape_subreddit(subreddit, 10)
        
        # Store results
        unified = UnifiedScraperComplete()
        stored = unified.store_to_bigquery(items)
        
        return jsonify({
            'success': True,
            'subreddit': subreddit,
            'scraped': len(items),
            'stored': stored
        })
        
    except Exception as e:
        logger.error(f"Reddit scrape error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get scraping statistics"""
    try:
        scraper = UnifiedScraperComplete()
        
        if not scraper.bq_client:
            return jsonify({'error': 'BigQuery not connected'}), 500
        
        query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT source) as unique_sources,
            COUNT(DISTINCT equipment_brand) as equipment_brands,
            ARRAY_LENGTH(ARRAY_AGG(DISTINCT UNNEST(error_codes) IGNORE NULLS)) as unique_error_codes,
            MAX(scraped_at) as last_scrape
        FROM `bobs-house-ai.circle_of_life.unified_knowledge`
        """
        
        results = scraper.bq_client.query(query).result()
        row = list(results)[0] if results.total_rows > 0 else None
        
        if row:
            return jsonify({
                'total_records': row.total_records,
                'unique_sources': row.unique_sources,
                'equipment_brands': row.equipment_brands,
                'unique_error_codes': row.unique_error_codes or 0,
                'last_scrape': row.last_scrape.isoformat() if row.last_scrape else None
            })
        else:
            return jsonify({
                'total_records': 0,
                'unique_sources': 0,
                'equipment_brands': 0,
                'unique_error_codes': 0,
                'last_scrape': None
            })
            
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    
    if port:
        logger.info(f"🚀 Starting Circle of Life Unified Scraper on port {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Test locally
        async def test():
            scraper = UnifiedScraperComplete()
            results = await scraper.scrape_all_sources()
            print(json.dumps(results, indent=2))
        
        asyncio.run(test())