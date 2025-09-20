#!/usr/bin/env python3
"""
Neo4j Unified Scraper - All scrapers dumping to Neo4j
Runs overnight to collect YouTube, TSB, and forum data
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any
from flask import Flask, jsonify, request

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import all scrapers
from youtube_equipment_scraper import YouTubeEquipmentScraper
from tsb_scraper import TSBScraper
from unified_scraper_enhanced import EnhancedUnifiedScraper
from circle_of_life_scraper import CircleOfLifeScraperIntegration

# Initialize Flask for Cloud Run
app = Flask(__name__)

class Neo4jUnifiedScraper:
    """
    Unified scraper that runs all scrapers and stores in Neo4j
    """

    def __init__(self):
        # Force Neo4j usage for all scrapers
        self.youtube_scraper = YouTubeEquipmentScraper(use_neo4j=True)
        self.tsb_scraper = TSBScraper(use_neo4j=True)
        self.enhanced_scraper = EnhancedUnifiedScraper()
        self.circle_of_life = CircleOfLifeScraperIntegration()

        logger.info("🚀 Neo4j Unified Scraper initialized - All data goes to graph!")

    async def run_overnight_scraping(self) -> Dict[str, Any]:
        """
        Run all scrapers overnight - dump everything into Neo4j
        """
        start_time = datetime.now()
        logger.info(f"🌙 STARTING OVERNIGHT NEO4J SCRAPING - {start_time}")

        results = {
            "start_time": start_time.isoformat(),
            "scrapers": {},
            "total_items": 0,
            "errors": []
        }

        try:
            # Phase 1: YouTube Equipment Transcripts
            logger.info("📹 Phase 1: Scraping YouTube equipment videos...")
            try:
                # Search for equipment repair videos
                youtube_queries = [
                    "mini skid steer repair troubleshooting",
                    "Bobcat S740 MT55 MT85 maintenance",
                    "diesel truck DPF DEF problems",
                    "6.7 Powerstroke common issues",
                    "5.9 Cummins repair guide",
                    "Duramax LML LBZ problems",
                    "compact tractor hydraulic repair",
                    "skid steer attachment troubleshooting",
                    "Ditch Witch SK repair",
                    "Toro Dingo maintenance"
                ]

                youtube_count = 0
                for query in youtube_queries:
                    count = await self.youtube_scraper.search_and_scrape(query, max_results=10)
                    youtube_count += count
                    await asyncio.sleep(5)  # Rate limiting

                # Also scrape from configured channels
                channel_count = await self.youtube_scraper.scrape_all_channels(max_videos_per_channel=5)
                youtube_count += channel_count

                results["scrapers"]["youtube"] = {
                    "status": "completed",
                    "videos_scraped": youtube_count,
                    "storage": "Neo4j + BigQuery"
                }
                results["total_items"] += youtube_count
                logger.info(f"✅ YouTube: {youtube_count} videos scraped")

            except Exception as e:
                logger.error(f"YouTube scraping failed: {e}")
                results["errors"].append(f"YouTube: {str(e)}")

            # Phase 2: Technical Service Bulletins
            logger.info("📋 Phase 2: Scraping TSBs...")
            try:
                # Scrape equipment TSBs
                equipment_tsbs = await self.tsb_scraper.scrape_equipment_tsbs()

                # Scrape diesel truck TSBs
                truck_tsbs = await self.tsb_scraper.scrape_diesel_truck_tsbs()

                # Search forums for TSB discussions
                forum_tsbs = await self.tsb_scraper.search_forums_for_tsbs("Bobcat service bulletin")

                total_tsbs = equipment_tsbs + truck_tsbs + len(forum_tsbs)

                results["scrapers"]["tsb"] = {
                    "status": "completed",
                    "tsbs_found": total_tsbs,
                    "equipment": equipment_tsbs,
                    "trucks": truck_tsbs,
                    "forums": len(forum_tsbs),
                    "storage": "Neo4j + BigQuery"
                }
                results["total_items"] += total_tsbs
                logger.info(f"✅ TSB: {total_tsbs} bulletins scraped")

            except Exception as e:
                logger.error(f"TSB scraping failed: {e}")
                results["errors"].append(f"TSB: {str(e)}")

            # Phase 3: Enhanced Unified Scraper (40+ sources)
            logger.info("🌐 Phase 3: Scraping forums and equipment sites...")
            try:
                # Scrape priority categories
                categories = [
                    'forums_heavy_equipment',
                    'manufacturer_resources',
                    'industry_publications'
                ]

                enhanced_results = await self.enhanced_scraper.scrape_all_sources(categories)

                results["scrapers"]["enhanced"] = {
                    "status": "completed",
                    "items_scraped": enhanced_results.get('total_items', 0),
                    "by_category": enhanced_results.get('by_category', {}),
                    "storage": "BigQuery"  # This one doesn't have Neo4j yet
                }
                results["total_items"] += enhanced_results.get('total_items', 0)
                logger.info(f"✅ Enhanced: {enhanced_results.get('total_items', 0)} items scraped")

            except Exception as e:
                logger.error(f"Enhanced scraping failed: {e}")
                results["errors"].append(f"Enhanced: {str(e)}")

            # Phase 4: Circle of Life Scraper
            logger.info("🔄 Phase 4: Circle of Life scraping...")
            try:
                circle_results = await self.circle_of_life.run_overnight_scraping()

                results["scrapers"]["circle_of_life"] = {
                    "status": circle_results.get("status", "unknown"),
                    "data_collected": circle_results.get("total_data_collected", 0),
                    "phases": circle_results.get("phases_completed", [])
                }
                results["total_items"] += circle_results.get("total_data_collected", 0)
                logger.info(f"✅ Circle of Life: {circle_results.get('total_data_collected', 0)} items")

            except Exception as e:
                logger.error(f"Circle of Life failed: {e}")
                results["errors"].append(f"Circle of Life: {str(e)}")

            # Calculate runtime
            end_time = datetime.now()
            runtime = (end_time - start_time).total_seconds() / 60

            results["end_time"] = end_time.isoformat()
            results["runtime_minutes"] = round(runtime, 2)
            results["status"] = "completed" if len(results["errors"]) == 0 else "completed_with_errors"

            logger.info(f"""
            🎉 OVERNIGHT SCRAPING COMPLETE!
            ================================
            Total Items: {results['total_items']}
            Runtime: {runtime:.1f} minutes
            YouTube Videos: {results['scrapers'].get('youtube', {}).get('videos_scraped', 0)}
            TSBs Found: {results['scrapers'].get('tsb', {}).get('tsbs_found', 0)}
            Forum Items: {results['scrapers'].get('enhanced', {}).get('items_scraped', 0)}
            Circle of Life: {results['scrapers'].get('circle_of_life', {}).get('data_collected', 0)}

            💾 Data stored in Neo4j graph database!
            """)

        except Exception as e:
            logger.error(f"Critical scraping failure: {e}")
            results["status"] = "failed"
            results["errors"].append(f"Critical: {str(e)}")

        return results

    async def run_quick_scrape(self) -> Dict[str, Any]:
        """
        Quick scrape - just YouTube and TSB for immediate needs
        """
        logger.info("⚡ Running quick Neo4j scrape...")

        results = {
            "type": "quick",
            "items": 0
        }

        try:
            # Quick YouTube search
            count = await self.youtube_scraper.search_and_scrape(
                "Bobcat S740 hydraulic problems",
                max_results=5
            )
            results["youtube"] = count
            results["items"] += count

            # Quick TSB check
            recalls = await self.tsb_scraper.scrape_nhtsa_recalls("Bobcat")
            for recall in recalls[:3]:
                await self.tsb_scraper.store_tsb(recall)
            results["tsb"] = len(recalls[:3])
            results["items"] += len(recalls[:3])

        except Exception as e:
            logger.error(f"Quick scrape error: {e}")
            results["error"] = str(e)

        return results

# Flask endpoints for Cloud Run

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "neo4j-unified-scraper",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/scrape', methods=['POST'])
def scrape():
    """Main scraping endpoint"""
    try:
        data = request.get_json() or {}
        scrape_type = data.get('type', 'overnight')

        logger.info(f"🚀 Scraping triggered: type={scrape_type}")

        # Run async scraper
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            scraper = Neo4jUnifiedScraper()

            if scrape_type == 'quick':
                results = loop.run_until_complete(scraper.run_quick_scrape())
            else:
                results = loop.run_until_complete(scraper.run_overnight_scraping())

            return jsonify(results), 200

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)[:500]
        }), 500

@app.route('/scrape/youtube', methods=['POST'])
def scrape_youtube():
    """Scrape just YouTube"""
    try:
        data = request.get_json() or {}
        query = data.get('query', 'equipment repair')
        max_results = data.get('max_results', 10)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            scraper = YouTubeEquipmentScraper(use_neo4j=True)
            count = loop.run_until_complete(
                scraper.search_and_scrape(query, max_results)
            )

            return jsonify({
                "status": "success",
                "query": query,
                "videos_scraped": count
            }), 200

        finally:
            loop.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape/tsb', methods=['POST'])
def scrape_tsb():
    """Scrape just TSBs"""
    try:
        data = request.get_json() or {}
        manufacturer = data.get('manufacturer', 'Bobcat')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            scraper = TSBScraper(use_neo4j=True)

            # Get recalls
            recalls = loop.run_until_complete(
                scraper.scrape_nhtsa_recalls(manufacturer)
            )

            # Store them
            stored = 0
            for recall in recalls:
                success = loop.run_until_complete(
                    scraper.store_tsb(recall)
                )
                if success:
                    stored += 1

            return jsonify({
                "status": "success",
                "manufacturer": manufacturer,
                "tsbs_found": len(recalls),
                "tsbs_stored": stored
            }), 200

        finally:
            loop.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats', methods=['GET'])
def stats():
    """Get scraping statistics"""
    try:
        from neo4j import GraphDatabase

        # Connect to Neo4j
        uri = "bolt://10.128.0.2:7687"
        driver = GraphDatabase.driver(uri, auth=("neo4j", "BobBrain2025"))

        with driver.session() as session:
            # Count nodes
            result = session.run("""
                MATCH (n)
                RETURN
                    labels(n)[0] as type,
                    count(n) as count
                ORDER BY count DESC
            """)

            stats = {}
            for record in result:
                stats[record["type"]] = record["count"]

            # Get recent activity
            result = session.run("""
                MATCH (n)
                WHERE n.scraped_at IS NOT NULL
                RETURN count(n) as today_count
            """)

            today = result.single()["today_count"]

        driver.close()

        return jsonify({
            "neo4j_stats": stats,
            "today_items": today,
            "status": "connected"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "disconnected"
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Neo4j Unified Scraper on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)