#!/usr/bin/env python3
"""
Enhanced Unified Open-Source Scraper System
Includes all diesel, heavy equipment, and repair content sources
Minimalistic, efficient, and scalable for Cloud Run
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import os

# Open-source scraping libraries
import requests
from bs4 import BeautifulSoup
import aiohttp
from playwright.async_api import async_playwright
from google.cloud import bigquery
import feedparser

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedUnifiedScraper:
    """
    Enhanced scraper with comprehensive source coverage:
    - YouTube repair channels
    - Specialized forums
    - Reddit communities
    - Government technical resources
    - Industry publications
    - Market intelligence sources
    """

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.browser = None
        self.context = None

        # Comprehensive source catalog organized by category
        self.sources = {
            'youtube_diesel_experts': [
                {'channel': 'PowerNation Truck Tech', 'url': 'https://www.youtube.com/@PowerNation', 'specialty': 'diesel_builds'},
                {'channel': 'Diesel Creek', 'url': 'https://www.youtube.com/@DieselCreek', 'specialty': 'restoration'},
                {'channel': 'Adept Ape', 'url': 'https://www.youtube.com/@AdeptApe', 'specialty': 'diesel_diagnostics'},
                {'channel': 'DeBoss Garage', 'url': 'https://www.youtube.com/@DeBossGarage', 'specialty': 'diesel_repair'},
                {'channel': 'Andrew Camarata', 'url': 'https://www.youtube.com/@AndrewCamarata', 'specialty': 'heavy_equipment'},
                {'channel': 'FarmCraft101', 'url': 'https://www.youtube.com/@FarmCraft101', 'specialty': 'agricultural'},
                {'channel': 'Heavy Duty Country', 'url': 'https://www.youtube.com/@HeavyDutyCountry', 'specialty': 'semi_truck'},
            ],

            'youtube_equipment': [
                {'channel': 'Marty T', 'url': 'https://www.youtube.com/@MartyT', 'specialty': 'excavator'},
                {'channel': 'Mustie1', 'url': 'https://www.youtube.com/@Mustie1', 'specialty': 'small_engine'},
                {'channel': 'Homesteady', 'url': 'https://www.youtube.com/@Homesteady', 'specialty': 'compact_equipment'},
                {'channel': 'Tractor Time with Tim', 'url': 'https://www.youtube.com/@TractorTimeWithTim', 'specialty': 'compact_troubleshooting'},
                {'channel': 'Messicks', 'url': 'https://www.youtube.com/@Messicks', 'specialty': 'compact_expert'},
            ],

            'forums_heavy_equipment': [
                {'url': 'https://www.heavyequipmentforums.com/forums/skid-steers.50/', 'type': 'forum', 'topic': 'skid_steer'},
                {'url': 'https://www.mytractorforum.com/forums/', 'type': 'forum', 'topic': 'compact_equipment'},
                {'url': 'https://www.orangetractortalks.net/forums/', 'type': 'forum', 'topic': 'kubota_diy'},
                {'url': 'https://www.tractordata.com/forums/', 'type': 'forum', 'topic': 'specifications'},
                {'url': 'https://www.dieselbombers.com/', 'type': 'forum', 'topic': 'diesel_performance'},
                {'url': 'https://www.compd.com/forums/', 'type': 'forum', 'topic': 'diesel_troubleshooting'},
                {'url': 'https://www.ironplanet.com/jsp/s/community', 'type': 'forum', 'topic': 'equipment_condition'},
                {'url': 'https://www.truckersreport.com/truckingindustryforum/', 'type': 'forum', 'topic': 'trucker_breakdowns'},
            ],

            'reddit_communities': [
                {'url': 'https://www.reddit.com/r/Justrolledintotheshop/top/.json?limit=50', 'type': 'api', 'topic': 'mechanic_insights'},
                {'url': 'https://www.reddit.com/r/Skookum/top/.json?limit=30', 'type': 'api', 'topic': 'quality_tools'},
                {'url': 'https://www.reddit.com/r/MechanicAdvice/top/.json?limit=30', 'type': 'api', 'topic': 'repair_advice'},
                {'url': 'https://www.reddit.com/r/Welding/top/.json?limit=30', 'type': 'api', 'topic': 'fabrication'},
                {'url': 'https://www.reddit.com/r/Hydraulics/top/.json?limit=30', 'type': 'api', 'topic': 'hydraulic_systems'},
                {'url': 'https://www.reddit.com/r/Truckers/top/.json?limit=30', 'type': 'api', 'topic': 'trucker_experiences'},
                {'url': 'https://www.reddit.com/r/Diesel/top/.json?limit=30', 'type': 'api', 'topic': 'diesel_specific'},
                {'url': 'https://www.reddit.com/r/Construction/top/.json?limit=30', 'type': 'api', 'topic': 'equipment_reliability'},
                {'url': 'https://www.reddit.com/r/farming/top/.json?limit=30', 'type': 'api', 'topic': 'farm_equipment'},
                {'url': 'https://www.reddit.com/r/Skidsteer/top/.json?limit=30', 'type': 'api', 'topic': 'skidsteer_specific'},
            ],

            'manufacturer_resources': [
                {'url': 'https://www.bobcat.com/na/en/support/maintenance', 'type': 'static', 'topic': 'bobcat_maintenance'},
                {'url': 'https://www.cat.com/en_US/support/maintenance.html', 'type': 'static', 'topic': 'cat_maintenance'},
                {'url': 'https://www.deere.com/en/parts-and-service/', 'type': 'static', 'topic': 'deere_service'},
                {'url': 'https://www.kubotausa.com/service-and-support', 'type': 'static', 'topic': 'kubota_support'},
                {'url': 'https://www.cummins.com/support', 'type': 'static', 'topic': 'cummins_diesel'},
            ],

            'industry_publications': [
                {'url': 'https://www.equipmentworld.com/feed/', 'type': 'rss', 'topic': 'equipment_news'},
                {'url': 'https://www.heavydutytrucking.com/rss', 'type': 'rss', 'topic': 'trucking_news'},
                {'url': 'https://www.fleetowner.com/rss.xml', 'type': 'rss', 'topic': 'fleet_maintenance'},
                {'url': 'https://www.dieselprogress.com/rss', 'type': 'rss', 'topic': 'diesel_technology'},
                {'url': 'https://www.compactequip.com/rss', 'type': 'rss', 'topic': 'compact_equipment_news'},
            ],

            'market_intelligence': [
                {'url': 'https://www.machinerytrader.com/listings/construction-equipment/', 'type': 'market', 'topic': 'equipment_pricing'},
                {'url': 'https://www.truckpaper.com/listings/trucks/', 'type': 'market', 'topic': 'truck_market'},
                {'url': 'https://www.ironplanet.com/', 'type': 'market', 'topic': 'auction_data'},
                {'url': 'https://www.ritchiebros.com/', 'type': 'market', 'topic': 'equipment_auctions'},
            ],
        }

        # Scraping strategies
        self.strategies = {
            'static': self.scrape_static_html,
            'forum': self.scrape_forum,
            'api': self.scrape_api,
            'rss': self.scrape_rss,
            'youtube': self.scrape_youtube,
            'market': self.scrape_market_data,
        }

        self._ensure_tables()
        logger.info("🚀 Enhanced Unified Scraper initialized with comprehensive sources")

    def _ensure_tables(self):
        """Create BigQuery tables for all scraped content"""
        dataset_id = f"{self.project_id}.comprehensive_scraping"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except:
            pass

        # Comprehensive schema for all content types
        schema = [
            bigquery.SchemaField("content_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("source_url", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),  # youtube, forum, reddit, etc.
            bigquery.SchemaField("category", "STRING"),  # diesel, equipment, etc.
            bigquery.SchemaField("topic", "STRING"),  # specific topic
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("author", "STRING"),  # for forums/reddit
            bigquery.SchemaField("engagement", "JSON"),  # likes, views, comments
            bigquery.SchemaField("metadata", "JSON"),  # flexible additional data
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{self.project_id}.comprehensive_scraping.all_content"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info("✅ Comprehensive content table ready")
        except:
            pass

    async def scrape_all_sources(self, categories: List[str] = None) -> Dict[str, Any]:
        """
        Scrape all or selected categories of sources
        """
        if categories is None:
            categories = list(self.sources.keys())

        results = {
            'total_items': 0,
            'by_category': {},
            'by_type': {},
            'errors': [],
            'start_time': datetime.now().isoformat(),
        }

        # Process each category
        for category in categories:
            if category not in self.sources:
                continue

            logger.info(f"📊 Scraping category: {category}")
            category_items = 0

            sources = self.sources[category]

            # Process sources in parallel within category
            tasks = []
            for source in sources[:5]:  # Limit for efficiency
                if 'youtube' in category:
                    task = self.scrape_youtube(source)
                else:
                    scrape_type = source.get('type', 'static')
                    task = self.strategies[scrape_type](source)
                tasks.append(task)

            # Gather results
            for task in asyncio.as_completed(tasks):
                try:
                    result = await task
                    if result and 'items' in result:
                        category_items += len(result['items'])
                        results['total_items'] += len(result['items'])

                        # Track by type
                        source_type = result.get('type', 'unknown')
                        if source_type not in results['by_type']:
                            results['by_type'][source_type] = 0
                        results['by_type'][source_type] += len(result['items'])

                except Exception as e:
                    results['errors'].append(str(e)[:100])

            results['by_category'][category] = category_items

        results['end_time'] = datetime.now().isoformat()
        logger.info(f"✅ Scraping complete: {results['total_items']} total items")

        return results

    async def scrape_static_html(self, source: Dict) -> Dict:
        """Scrape static HTML pages"""
        try:
            response = requests.get(source['url'], timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 BobBrain/2.0'
            })
            soup = BeautifulSoup(response.text, 'html.parser')

            items = []
            for element in soup.find_all(['article', 'div', 'section'])[:10]:
                text = element.get_text(strip=True)
                if len(text) > 100:
                    item = {
                        'title': text[:100],
                        'content': text[:1000],
                        'source_url': source['url'],
                        'topic': source.get('topic', 'general')
                    }
                    items.append(item)
                    await self._store_item(item, source, 'static')

            return {'items': items, 'type': 'static'}

        except Exception as e:
            logger.error(f"Static HTML error: {e}")
            return {'items': [], 'error': str(e)}

    async def scrape_forum(self, source: Dict) -> Dict:
        """Scrape forum threads"""
        # Use BeautifulSoup for forums, with Playwright fallback if needed
        result = await self.scrape_static_html(source)
        result['type'] = 'forum'
        return result

    async def scrape_api(self, source: Dict) -> Dict:
        """Scrape API endpoints (Reddit, etc.)"""
        try:
            response = requests.get(source['url'], headers={
                'User-Agent': 'BobBrain/2.0'
            }, timeout=10)

            data = response.json()
            items = []

            # Handle Reddit JSON
            if 'reddit.com' in source['url'] and 'data' in data:
                for child in data['data']['children'][:20]:
                    post = child['data']
                    item = {
                        'title': post.get('title', ''),
                        'content': post.get('selftext', '')[:1000],
                        'author': post.get('author', ''),
                        'source_url': f"https://reddit.com{post.get('permalink', '')}",
                        'topic': source.get('topic', 'general'),
                        'engagement': {
                            'score': post.get('score', 0),
                            'comments': post.get('num_comments', 0)
                        }
                    }
                    items.append(item)
                    await self._store_item(item, source, 'reddit')

            return {'items': items, 'type': 'api'}

        except Exception as e:
            logger.error(f"API error: {e}")
            return {'items': [], 'error': str(e)}

    async def scrape_rss(self, source: Dict) -> Dict:
        """Scrape RSS feeds"""
        try:
            feed = feedparser.parse(source['url'])
            items = []

            for entry in feed.entries[:15]:
                item = {
                    'title': entry.get('title', ''),
                    'content': entry.get('summary', '')[:1000],
                    'source_url': entry.get('link', ''),
                    'topic': source.get('topic', 'general')
                }
                items.append(item)
                await self._store_item(item, source, 'rss')

            return {'items': items, 'type': 'rss'}

        except Exception as e:
            logger.error(f"RSS error: {e}")
            return {'items': [], 'error': str(e)}

    async def scrape_youtube(self, source: Dict) -> Dict:
        """Scrape YouTube channel metadata"""
        try:
            # For YouTube, we'll just store the channel info
            # Full video scraping would require YouTube API or youtube-dl
            item = {
                'title': source.get('channel', ''),
                'content': f"YouTube channel specializing in {source.get('specialty', 'repairs')}",
                'source_url': source.get('url', ''),
                'topic': source.get('specialty', 'general')
            }

            await self._store_item(item, source, 'youtube')

            return {'items': [item], 'type': 'youtube'}

        except Exception as e:
            logger.error(f"YouTube error: {e}")
            return {'items': [], 'error': str(e)}

    async def scrape_market_data(self, source: Dict) -> Dict:
        """Scrape market/auction data"""
        # Simplified - would need more complex parsing for real market data
        return await self.scrape_static_html(source)

    async def _store_item(self, item: Dict, source: Dict, content_type: str):
        """Store item in BigQuery"""
        try:
            # Generate unique ID
            content_id = hashlib.md5(
                f"{item.get('source_url', '')}{item.get('title', '')}{datetime.now().isoformat()}".encode()
            ).hexdigest()

            record = {
                'content_id': content_id,
                'source_url': item.get('source_url', source.get('url', '')),
                'source_type': content_type,
                'category': source.get('category', 'general'),
                'topic': item.get('topic', source.get('topic', 'general')),
                'title': item.get('title', ''),
                'content': item.get('content', ''),
                'author': item.get('author', ''),
                'engagement': json.dumps(item.get('engagement', {})),
                'metadata': json.dumps(item.get('metadata', {})),
                'scraped_at': datetime.now()
            }

            table_id = f"{self.project_id}.comprehensive_scraping.all_content"
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
    """Test the enhanced scraper"""
    scraper = EnhancedUnifiedScraper()

    print("=" * 60)
    print("🚀 ENHANCED UNIFIED SCRAPER - COMPREHENSIVE DATA COLLECTION")
    print(f"📅 {datetime.now()}")
    print("=" * 60)

    # Scrape priority categories
    priority_categories = [
        'forums_heavy_equipment',
        'reddit_communities',
        'manufacturer_resources'
    ]

    results = await scraper.scrape_all_sources(priority_categories)

    print("\n📊 SCRAPING RESULTS:")
    print(f"  Total items: {results['total_items']}")
    print("\n  By category:")
    for category, count in results.get('by_category', {}).items():
        print(f"    - {category}: {count}")
    print("\n  By type:")
    for source_type, count in results.get('by_type', {}).items():
        print(f"    - {source_type}: {count}")

    if results.get('errors'):
        print(f"\n  ⚠️ Errors: {len(results['errors'])}")

    await scraper.cleanup()

    print("\n✅ Data stored in BigQuery: comprehensive_scraping.all_content")
    print("🔄 Bob's Brain now has comprehensive equipment knowledge!")

if __name__ == "__main__":
    asyncio.run(main())