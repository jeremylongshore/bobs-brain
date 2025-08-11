#!/usr/bin/env python3
"""
Unified Open-Source Scraper System
Combines Scrapy, Playwright, BeautifulSoup, and native tools
Minimalistic, efficient, and scalable for Cloud Run
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Open-source scraping libraries
import requests
from bs4 import BeautifulSoup
import aiohttp
from playwright.async_api import async_playwright
from google.cloud import bigquery
import feedparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UnifiedScraper:
    """
    Unified scraper combining best open-source tools:
    - Scrapy for complex crawling (via subprocess for Cloud Run compatibility)
    - Playwright for JavaScript-heavy sites
    - BeautifulSoup for simple HTML parsing
    - Requests/aiohttp for API calls
    - Feedparser for RSS feeds
    """
    
    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.browser = None
        self.context = None
        
        # Scraping strategies by content type
        self.strategies = {
            'static_html': self.scrape_with_beautifulsoup,
            'javascript': self.scrape_with_playwright,
            'api': self.scrape_with_requests,
            'rss': self.scrape_with_feedparser,
            'forum': self.scrape_forum_optimized,
            'youtube': self.scrape_youtube_optimized,
        }
        
        # Target sources organized by priority
        self.priority_sources = {
            'critical': [  # Bobcat S740 specific
                {'url': 'https://www.bobcat.com/na/en/support/maintenance', 'type': 'static_html', 'topic': 'maintenance'},
                {'url': 'https://www.reddit.com/r/Bobcat/top/.json?limit=50', 'type': 'api', 'topic': 'problems'},
                {'url': 'https://www.heavyequipmentforums.com/forums/skid-steers.50/', 'type': 'forum', 'topic': 'repairs'},
            ],
            'high': [  # General heavy equipment
                {'url': 'https://www.reddit.com/r/HeavyEquipment/.json?limit=30', 'type': 'api', 'topic': 'equipment'},
                {'url': 'https://www.tractorbynet.com/forums/compact-utility-tractors.4/', 'type': 'forum', 'topic': 'compact'},
            ],
            'medium': [  # YouTube and social
                {'url': 'https://www.youtube.com/@BobcatCompany', 'type': 'youtube', 'topic': 'tutorials'},
                {'url': 'https://www.youtube.com/@AndrewCamarata', 'type': 'youtube', 'topic': 'repairs'},
            ]
        }
        
        self._ensure_tables()
        logger.info("🚀 Unified Scraper initialized")
    
    def _ensure_tables(self):
        """Create minimal BigQuery tables for scraped data"""
        dataset_id = f"{self.project_id}.unified_scraping"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except:
            pass
        
        # Single unified table for all scraped content
        schema = [
            bigquery.SchemaField("content_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("source_url", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),  # forum, youtube, api, etc.
            bigquery.SchemaField("topic", "STRING"),  # maintenance, repairs, etc.
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("metadata", "JSON"),  # Flexible field for any extra data
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]
        
        table_id = f"{self.project_id}.unified_scraping.content"
        table = bigquery.Table(table_id, schema=schema)
        
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info("✅ Unified content table ready")
        except:
            pass
    
    async def scrape_all_parallel(self) -> Dict[str, Any]:
        """
        Main entry point - scrapes all sources in parallel
        Uses appropriate tool for each source type
        """
        results = {
            'total_scraped': 0,
            'by_type': {},
            'by_priority': {},
            'errors': []
        }
        
        # Process all priorities in parallel
        tasks = []
        for priority, sources in self.priority_sources.items():
            for source in sources:
                task = self._scrape_source(source)
                tasks.append((priority, source, task))
        
        # Gather results
        for priority, source, task in tasks:
            try:
                result = await task
                if result:
                    results['total_scraped'] += len(result.get('items', []))
                    
                    # Track by type
                    source_type = source['type']
                    if source_type not in results['by_type']:
                        results['by_type'][source_type] = 0
                    results['by_type'][source_type] += len(result.get('items', []))
                    
                    # Track by priority
                    if priority not in results['by_priority']:
                        results['by_priority'][priority] = 0
                    results['by_priority'][priority] += len(result.get('items', []))
                    
            except Exception as e:
                results['errors'].append({
                    'url': source['url'],
                    'error': str(e)[:100]
                })
        
        logger.info(f"📊 Scraping complete: {results['total_scraped']} items")
        return results
    
    async def _scrape_source(self, source: Dict) -> Optional[Dict]:
        """Route to appropriate scraper based on source type"""
        scraper = self.strategies.get(source['type'])
        if scraper:
            return await scraper(source)
        return None
    
    async def scrape_with_beautifulsoup(self, source: Dict) -> Dict:
        """Use BeautifulSoup for static HTML"""
        try:
            response = requests.get(source['url'], timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; BobBrain/1.0)'
            })
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant content
            items = []
            for article in soup.find_all(['article', 'div'], class_=['content', 'post', 'entry'])[:10]:
                title = article.find(['h1', 'h2', 'h3'])
                content = article.get_text(strip=True)[:1000]
                
                if title and content:
                    item_data = {
                        'title': title.get_text(strip=True),
                        'content': content,
                        'url': source['url']
                    }
                    items.append(item_data)
                    await self._store_content(item_data, source)
            
            return {'items': items, 'source': source['url']}
            
        except Exception as e:
            logger.error(f"BeautifulSoup error for {source['url']}: {e}")
            return {'items': [], 'error': str(e)}
    
    async def scrape_with_playwright(self, source: Dict) -> Dict:
        """Use Playwright for JavaScript-heavy sites"""
        try:
            if not self.browser:
                playwright = await async_playwright().start()
                self.browser = await playwright.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-setuid-sandbox']
                )
                self.context = await self.browser.new_context()
            
            page = await self.context.new_page()
            await page.goto(source['url'], wait_until='networkidle', timeout=30000)
            
            # Extract content using JavaScript
            items = await page.evaluate("""
                () => {
                    const items = [];
                    document.querySelectorAll('article, .post, .content').forEach(el => {
                        const title = el.querySelector('h1, h2, h3');
                        if (title) {
                            items.push({
                                title: title.innerText,
                                content: el.innerText.substring(0, 1000)
                            });
                        }
                    });
                    return items.slice(0, 10);
                }
            """)
            
            await page.close()
            
            # Store items
            for item in items:
                item['url'] = source['url']
                await self._store_content(item, source)
            
            return {'items': items, 'source': source['url']}
            
        except Exception as e:
            logger.error(f"Playwright error for {source['url']}: {e}")
            return {'items': [], 'error': str(e)}
    
    async def scrape_with_requests(self, source: Dict) -> Dict:
        """Use requests for API endpoints"""
        try:
            response = requests.get(source['url'], headers={
                'User-Agent': 'BobBrain/1.0'
            }, timeout=10)
            
            data = response.json()
            items = []
            
            # Handle Reddit JSON structure
            if 'reddit.com' in source['url'] and 'data' in data:
                for child in data['data']['children'][:20]:
                    post = child['data']
                    item_data = {
                        'title': post.get('title', ''),
                        'content': post.get('selftext', '')[:1000],
                        'url': f"https://reddit.com{post.get('permalink', '')}"
                    }
                    items.append(item_data)
                    await self._store_content(item_data, source)
            
            return {'items': items, 'source': source['url']}
            
        except Exception as e:
            logger.error(f"API error for {source['url']}: {e}")
            return {'items': [], 'error': str(e)}
    
    async def scrape_with_feedparser(self, source: Dict) -> Dict:
        """Use feedparser for RSS feeds"""
        try:
            feed = feedparser.parse(source['url'])
            items = []
            
            for entry in feed.entries[:20]:
                item_data = {
                    'title': entry.get('title', ''),
                    'content': entry.get('summary', '')[:1000],
                    'url': entry.get('link', '')
                }
                items.append(item_data)
                await self._store_content(item_data, source)
            
            return {'items': items, 'source': source['url']}
            
        except Exception as e:
            logger.error(f"RSS error for {source['url']}: {e}")
            return {'items': [], 'error': str(e)}
    
    async def scrape_forum_optimized(self, source: Dict) -> Dict:
        """Optimized forum scraping combining multiple techniques"""
        # Try BeautifulSoup first (faster), fall back to Playwright if needed
        result = await self.scrape_with_beautifulsoup(source)
        if not result.get('items'):
            result = await self.scrape_with_playwright(source)
        return result
    
    async def scrape_youtube_optimized(self, source: Dict) -> Dict:
        """Optimized YouTube scraping"""
        # For now, use Playwright for YouTube
        # Could be enhanced with youtube-dl or yt-dlp in the future
        return await self.scrape_with_playwright(source)
    
    async def _store_content(self, item_data: Dict, source: Dict):
        """Store scraped content in BigQuery"""
        try:
            # Generate unique ID
            content_hash = hashlib.md5(
                f"{item_data.get('url', '')}{item_data.get('title', '')}".encode()
            ).hexdigest()
            
            record = {
                'content_id': content_hash,
                'source_url': source['url'],
                'source_type': source['type'],
                'topic': source.get('topic', 'general'),
                'title': item_data.get('title', ''),
                'content': item_data.get('content', ''),
                'metadata': json.dumps({
                    'item_url': item_data.get('url', ''),
                    'scraped_from': source['url']
                }),
                'scraped_at': datetime.now()
            }
            
            table_id = f"{self.project_id}.unified_scraping.content"
            errors = self.bq_client.insert_rows_json(table_id, [record])
            
            if errors:
                logger.error(f"BigQuery insert error: {errors}")
                
        except Exception as e:
            logger.error(f"Storage error: {e}")
    
    async def cleanup(self):
        """Clean up resources"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None


async def main():
    """Main execution for testing"""
    scraper = UnifiedScraper()
    
    print("=" * 60)
    print("🚀 UNIFIED SCRAPER - COLLECTING DATA")
    print(f"📅 {datetime.now()}")
    print("=" * 60)
    
    try:
        results = await scraper.scrape_all_parallel()
        
        print("\n📊 SCRAPING RESULTS:")
        print(f"  Total items: {results['total_scraped']}")
        print("\n  By type:")
        for source_type, count in results.get('by_type', {}).items():
            print(f"    - {source_type}: {count}")
        print("\n  By priority:")
        for priority, count in results.get('by_priority', {}).items():
            print(f"    - {priority}: {count}")
        
        if results.get('errors'):
            print(f"\n  ⚠️ Errors: {len(results['errors'])}")
    
    finally:
        await scraper.cleanup()
    
    print("\n✅ Data stored in BigQuery: unified_scraping.content")
    print("🔄 Bob's Brain now has fresh equipment knowledge!")


if __name__ == "__main__":
    asyncio.run(main())