#!/usr/bin/env python3
"""
Trigger Immediate Scraping
Starts scraping forums right now without waiting for schedule
"""

import asyncio
import logging
from datetime import datetime
from src.forum_scraper import ForumIntelligenceScraper
from src.skidsteer_scraper import SkidsteerKnowledgeScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def run_immediate_scraping():
    """Run scraping immediately"""
    print("=" * 60)
    print("🚀 STARTING IMMEDIATE SCRAPING")
    print(f"📅 {datetime.now()}")
    print("=" * 60)
    
    # Initialize scrapers
    forum_scraper = ForumIntelligenceScraper()
    skidsteer_scraper = SkidsteerKnowledgeScraper()
    
    print("\n📊 Phase 1: Discovering Forums...")
    # Search queries focused on Bobcat S740
    search_queries = [
        "Bobcat S740 repair forum",
        "skid steer troubleshooting forum",
        "heavy equipment repair community",
        "compact equipment maintenance forum",
        "Bobcat error codes forum"
    ]
    
    # Discover forums
    forums = await forum_scraper.discover_forums(search_queries)
    print(f"✅ Discovered {len(forums)} forums")
    
    print("\n📊 Phase 2: Scraping Bobcat S740 Knowledge...")
    # Scrape S740 specific knowledge
    s740_results = await skidsteer_scraper.scrape_skidsteer_forums()
    print(f"✅ Collected S740 knowledge: {s740_results}")
    
    print("\n📊 Phase 3: Scraping Forum Threads...")
    # Scrape top forums
    for forum in forums[:5]:  # Limit to first 5 for immediate run
        try:
            print(f"  Scraping: {forum.get('name', 'Unknown')} [{forum.get('auth_level', 'unknown')}]")
            threads = await forum_scraper.scrape_forum_threads(
                forum['url'],
                max_threads=10  # Limit threads per forum
            )
            print(f"    ✅ Scraped {len(threads)} threads")
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    # Clean up
    await forum_scraper.close_browser()
    await skidsteer_scraper.close_browser()
    
    print("\n" + "=" * 60)
    print("✅ IMMEDIATE SCRAPING COMPLETE")
    print("=" * 60)
    print("\n📌 Data stored in BigQuery datasets:")
    print("  - bobs-house-ai.scraped_data.forums")
    print("  - bobs-house-ai.scraped_data.forum_threads")
    print("  - bobs-house-ai.skidsteer_knowledge.bobcat_s740_issues")
    print("\n🔄 Bob's Brain will now have access to this knowledge!")

def main():
    """Main entry point"""
    try:
        # Run async scraping
        asyncio.run(run_immediate_scraping())
    except KeyboardInterrupt:
        print("\n⚠️ Scraping interrupted by user")
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise

if __name__ == "__main__":
    main()