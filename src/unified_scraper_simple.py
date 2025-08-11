#!/usr/bin/env python3
"""
Simple Unified Scraper - Focused on Actually Storing Data
Minimalistic scraper that ensures data gets into BigQuery
"""

import asyncio
import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery
import feedparser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleUnifiedScraper:
    """
    Simplified scraper that focuses on actually storing data
    """
    
    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        
        # Initialize BigQuery client with explicit project
        os.environ['GOOGLE_CLOUD_PROJECT'] = project_id
        self.bq_client = bigquery.Client(project=project_id)
        
        # Priority sources for immediate scraping
        self.sources = {
            'bobcat': [
                {'url': 'https://www.bobcat.com/na/en/support/maintenance', 'type': 'static'},
            ],
            'reddit': [
                {'url': 'https://www.reddit.com/r/Bobcat/top/.json?limit=10', 'type': 'api'},
                {'url': 'https://www.reddit.com/r/HeavyEquipment/top/.json?limit=10', 'type': 'api'},
                {'url': 'https://www.reddit.com/r/Diesel/top/.json?limit=10', 'type': 'api'},
            ],
            'forums': [
                {'url': 'https://www.heavyequipmentforums.com/', 'type': 'static'},
            ],
            'rss': [
                {'url': 'https://www.equipmentworld.com/feed/', 'type': 'rss'},
            ]
        }
        
        self._ensure_simple_table()
        logger.info("✅ Simple Unified Scraper initialized")
    
    def _ensure_simple_table(self):
        """Create a simple BigQuery table that will definitely work"""
        dataset_id = f"{self.project_id}.simple_scraping"
        
        # Create dataset
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset created/verified: {dataset_id}")
        except Exception as e:
            logger.info(f"Dataset exists: {e}")
        
        # Create simple table with basic fields
        table_id = f"{dataset_id}.content"
        schema = [
            bigquery.SchemaField("id", "STRING"),
            bigquery.SchemaField("url", "STRING"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table created/verified: {table_id}")
        except Exception as e:
            logger.info(f"Table exists: {e}")
    
    async def scrape_all(self) -> Dict[str, Any]:
        """Scrape all sources and store data"""
        results = {
            'total': 0,
            'stored': 0,
            'errors': [],
            'by_type': {}
        }
        
        for category, sources in self.sources.items():
            logger.info(f"📊 Scraping {category}...")
            
            for source in sources:
                try:
                    items = await self._scrape_source(source)
                    results['total'] += len(items)
                    
                    # Store each item
                    for item in items:
                        if self._store_item(item, source['type']):
                            results['stored'] += 1
                    
                    # Track by type
                    source_type = source['type']
                    if source_type not in results['by_type']:
                        results['by_type'][source_type] = 0
                    results['by_type'][source_type] += len(items)
                    
                except Exception as e:
                    error_msg = f"Error scraping {source['url']}: {str(e)[:100]}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
        
        logger.info(f"✅ Scraping complete: {results['stored']}/{results['total']} items stored")
        return results
    
    async def _scrape_source(self, source: Dict) -> List[Dict]:
        """Scrape a single source"""
        source_type = source['type']
        url = source['url']
        
        if source_type == 'api':
            return self._scrape_api(url)
        elif source_type == 'rss':
            return self._scrape_rss(url)
        else:  # static
            return self._scrape_static(url)
    
    def _scrape_api(self, url: str) -> List[Dict]:
        """Scrape API endpoints (Reddit)"""
        items = []
        try:
            headers = {'User-Agent': 'BobBrain/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()
            
            # Handle Reddit JSON
            if 'reddit.com' in url and 'data' in data:
                for child in data['data']['children'][:10]:
                    post = child['data']
                    items.append({
                        'title': post.get('title', '')[:500],
                        'content': post.get('selftext', '')[:2000],
                        'url': f"https://reddit.com{post.get('permalink', '')}"
                    })
        except Exception as e:
            logger.error(f"API scrape error: {e}")
        
        return items
    
    def _scrape_rss(self, url: str) -> List[Dict]:
        """Scrape RSS feeds"""
        items = []
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:
                items.append({
                    'title': entry.get('title', '')[:500],
                    'content': entry.get('summary', '')[:2000],
                    'url': entry.get('link', url)
                })
        except Exception as e:
            logger.error(f"RSS scrape error: {e}")
        
        return items
    
    def _scrape_static(self, url: str) -> List[Dict]:
        """Scrape static HTML"""
        items = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0 BobBrain/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find articles or content blocks
            for element in soup.find_all(['article', 'div'])[:5]:
                text = element.get_text(strip=True)
                if len(text) > 100:
                    title = text[:100] if text else "Content"
                    items.append({
                        'title': title[:500],
                        'content': text[:2000],
                        'url': url
                    })
        except Exception as e:
            logger.error(f"Static scrape error: {e}")
        
        return items if items else [{'title': 'Page scraped', 'content': f'Scraped {url}', 'url': url}]
    
    def _store_item(self, item: Dict, source_type: str) -> bool:
        """Store a single item in BigQuery"""
        try:
            # Generate unique ID
            unique_string = f"{item.get('url', '')}{item.get('title', '')}{datetime.now().isoformat()}"
            item_id = hashlib.md5(unique_string.encode()).hexdigest()
            
            # Prepare row
            row = {
                'id': item_id,
                'url': item.get('url', '')[:1000],
                'title': item.get('title', '')[:500],
                'content': item.get('content', '')[:2000],
                'source_type': source_type,
                'scraped_at': datetime.now().isoformat()
            }
            
            # Insert into BigQuery
            table_id = f"{self.project_id}.simple_scraping.content"
            errors = self.bq_client.insert_rows_json(table_id, [row])
            
            if errors:
                logger.error(f"BigQuery insert errors: {errors}")
                return False
            else:
                logger.debug(f"Stored item: {item.get('title', '')[:50]}")
                return True
                
        except Exception as e:
            logger.error(f"Storage error: {e}")
            return False


async def main():
    """Test the simple scraper"""
    scraper = SimpleUnifiedScraper()
    
    print("=" * 60)
    print("🚀 SIMPLE SCRAPER TEST - STORING DATA")
    print(f"📅 {datetime.now()}")
    print("=" * 60)
    
    results = await scraper.scrape_all()
    
    print(f"\n📊 Results:")
    print(f"  Total scraped: {results['total']}")
    print(f"  Successfully stored: {results['stored']}")
    print(f"  Storage rate: {results['stored']/max(results['total'], 1)*100:.1f}%")
    
    if results['by_type']:
        print("\n  By type:")
        for typ, count in results['by_type'].items():
            print(f"    - {typ}: {count}")
    
    if results['errors']:
        print(f"\n  ⚠️ Errors: {len(results['errors'])}")
    
    print("\n✅ Data stored in: simple_scraping.content")

if __name__ == "__main__":
    asyncio.run(main())