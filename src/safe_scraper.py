#!/usr/bin/env python3
"""
Safe Scraper - Avoids Rate Limited Sources
Focuses on sources that don't block us
Now with Flask API endpoints for Cloud Run deployment
"""

import asyncio
import hashlib
import logging
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List

import feedparser
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app for API endpoints
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=2)


class SafeScraper:
    """Scraper that avoids rate-limited sources until we have proper API keys"""

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)

        # Check for Reddit credentials
        self.reddit_client_id = os.environ.get("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
        self.has_reddit_api = bool(self.reddit_client_id and self.reddit_client_secret)

        if not self.has_reddit_api:
            logger.warning("⚠️ Reddit API not configured - skipping Reddit to avoid rate limits")

        # SAFE SOURCES (No Rate Limits)
        self.safe_sources = {
            # RSS FEEDS - Always Safe
            "rss_feeds": [
                {
                    "name": "Equipment World",
                    "url": "https://www.equipmentworld.com/feed/",
                    "topics": "Construction equipment news, maintenance tips",
                },
                {
                    "name": "For Construction Pros",
                    "url": "https://www.forconstructionpros.com/rss/",
                    "topics": "Equipment maintenance, industry news",
                },
                {
                    "name": "Diesel Progress",
                    "url": "https://www.dieselprogress.com/rss/",
                    "topics": "Diesel engine technology, maintenance",
                },
                {
                    "name": "Compact Equipment Magazine",
                    "url": "https://compactequip.com/feed/",
                    "topics": "Compact equipment, attachments",
                },
                {
                    "name": "Heavy Equipment Guide",
                    "url": "https://www.heavyequipmentguide.ca/rss",
                    "topics": "Heavy equipment news, tips",
                },
                {
                    "name": "OEM Off-Highway",
                    "url": "https://www.oemoffhighway.com/rss",
                    "topics": "Equipment technology, components",
                },
            ],
            # MANUFACTURER BLOGS - Public Access
            "manufacturer_sites": [
                {
                    "name": "John Deere Blog",
                    "url": "https://blog.machinefinder.com/",
                    "selector": "article",
                    "topics": "John Deere equipment tips",
                },
                {
                    "name": "Bobcat Advantage",
                    "url": "https://www.bobcat.com/resources/blog",
                    "selector": "article",
                    "topics": "Bobcat equipment maintenance",
                },
                {
                    "name": "Kubota Blog",
                    "url": "https://www.kubotausa.com/blog",
                    "selector": "article",
                    "topics": "Tractor maintenance, tips",
                },
                {
                    "name": "Case CE Blog",
                    "url": "https://blog.casece.com/",
                    "selector": "article",
                    "topics": "Construction equipment",
                },
            ],
            # TECHNICAL DOCUMENTATION SITES
            "tech_docs": [
                {
                    "name": "Equipment Specs",
                    "url": "https://www.equipmentworld.com/equipment",
                    "topics": "Equipment specifications, comparisons",
                },
                {
                    "name": "RitchieSpecs",
                    "url": "https://www.ritchiespecs.com/",
                    "topics": "Equipment specifications database",
                },
            ],
            # AUCTION SITES (Market Intelligence)
            "market_data": [
                {
                    "name": "Equipment Trader Blog",
                    "url": "https://www.equipmenttrader.com/",
                    "topics": "Equipment values, market trends",
                },
                {"name": "MachineryPete", "url": "https://www.machinerypete.com/", "topics": "Used equipment values"},
            ],
        }

        self._ensure_tables()

    def _ensure_tables(self):
        """Create BigQuery tables"""
        dataset_id = f"{self.project_id}.safe_scraping"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset ready: {dataset_id}")
        except:
            pass

        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("url", "STRING"),
            bigquery.SchemaField("source_name", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),
            bigquery.SchemaField("equipment_mentions", "STRING", mode="REPEATED"),
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{dataset_id}.equipment_content"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table ready: {table_id}")
        except:
            pass

    async def scrape_rss_feeds(self) -> List[Dict]:
        """Scrape RSS feeds - these never rate limit"""
        all_items = []

        for feed_info in self.safe_sources["rss_feeds"]:
            try:
                logger.info(f"📰 Scraping RSS: {feed_info['name']}")
                feed = feedparser.parse(feed_info["url"])

                for entry in feed.entries[:10]:
                    # Check if it's repair/maintenance related
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    full_text = (title + " " + summary).lower()

                    # Look for relevant content
                    relevant_keywords = [
                        "repair",
                        "maintenance",
                        "fix",
                        "troubleshoot",
                        "service",
                        "problem",
                        "issue",
                        "diagnostic",
                        "hydraulic",
                        "engine",
                        "transmission",
                        "electrical",
                    ]

                    if any(keyword in full_text for keyword in relevant_keywords):
                        item = {
                            "title": title[:500],
                            "content": summary[:3000],
                            "url": entry.get("link", ""),
                            "source_name": feed_info["name"],
                            "source_type": "rss",
                            "published": entry.get("published", ""),
                            "equipment_mentions": self._extract_equipment(full_text),
                        }
                        all_items.append(item)

                logger.info(
                    f"   ✅ Found {len([i for i in all_items if i['source_name'] == feed_info['name']])} relevant articles"
                )

            except Exception as e:
                logger.error(f"RSS error for {feed_info['name']}: {str(e)[:100]}")
                continue

        return all_items

    async def scrape_manufacturer_sites(self) -> List[Dict]:
        """Scrape manufacturer blogs - they want us to read their content"""
        all_items = []

        for site in self.safe_sources["manufacturer_sites"]:
            try:
                logger.info(f"🏭 Scraping: {site['name']}")

                # Use requests with proper headers
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                response = requests.get(site["url"], headers=headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")

                    # Find article links
                    articles = soup.find_all(["article", "div"], class_=lambda x: x and "article" in str(x).lower())[:5]

                    for article in articles:
                        title_elem = article.find(["h1", "h2", "h3", "h4"])
                        content_elem = article.find(
                            ["p", "div"],
                            class_=lambda x: x
                            and any(word in str(x).lower() for word in ["content", "excerpt", "summary"]),
                        )

                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            content = content_elem.get_text(strip=True) if content_elem else ""

                            # Get article URL
                            link_elem = article.find("a", href=True)
                            article_url = link_elem["href"] if link_elem else site["url"]

                            if not article_url.startswith("http"):
                                from urllib.parse import urljoin

                                article_url = urljoin(site["url"], article_url)

                            item = {
                                "title": title[:500],
                                "content": content[:3000],
                                "url": article_url,
                                "source_name": site["name"],
                                "source_type": "manufacturer",
                                "equipment_mentions": self._extract_equipment(title + " " + content),
                            }
                            all_items.append(item)

                    logger.info(
                        f"   ✅ Found {len([i for i in all_items if i['source_name'] == site['name']])} articles"
                    )
                else:
                    logger.warning(f"   ⚠️ {site['name']} returned status {response.status_code}")

            except Exception as e:
                logger.error(f"Site error for {site['name']}: {str(e)[:100]}")
                continue

        return all_items

    def _extract_equipment(self, text: str) -> List[str]:
        """Extract equipment mentions from text"""
        text = text.lower()
        equipment_found = []

        equipment_patterns = {
            "excavator": ["excavator", "backhoe", "digger"],
            "skid_steer": ["skid steer", "bobcat", "skidsteer"],
            "tractor": ["tractor", "john deere", "kubota", "case ih"],
            "dozer": ["dozer", "bulldozer", "crawler"],
            "loader": ["loader", "wheel loader", "front loader"],
            "grader": ["grader", "motor grader"],
            "truck": ["truck", "dump truck", "haul truck"],
            "forklift": ["forklift", "telehandler"],
            "mower": ["mower", "zero turn", "lawn"],
            "generator": ["generator", "genset"],
        }

        for equipment_type, patterns in equipment_patterns.items():
            if any(pattern in text for pattern in patterns):
                equipment_found.append(equipment_type)

        return equipment_found[:5]  # Limit to 5 equipment types

    def _detect_repair_type(self, text: str) -> str:
        """Detect type of repair from content"""
        text = text.lower()

        repair_patterns = {
            "hydraulic": ["hydraulic", "cylinder", "pump", "valve", "pressure"],
            "engine": ["engine", "motor", "diesel", "fuel", "compression"],
            "electrical": ["electrical", "battery", "alternator", "wiring", "sensor"],
            "transmission": ["transmission", "gear", "clutch", "drive", "axle"],
            "maintenance": ["maintenance", "service", "oil", "filter", "grease"],
            "diagnostic": ["diagnostic", "troubleshoot", "error", "code", "fault"],
        }

        for repair_type, patterns in repair_patterns.items():
            if any(pattern in text for pattern in patterns):
                return repair_type

        return "general"

    def _store_item(self, item: Dict) -> bool:
        """Store item in BigQuery"""
        try:
            # Generate unique ID
            content_hash = hashlib.md5(f"{item.get('title', '')}{item.get('url', '')}".encode()).hexdigest()

            # Detect repair type
            full_text = item.get("title", "") + " " + item.get("content", "")
            repair_type = self._detect_repair_type(full_text)

            record = {
                "id": content_hash,
                "title": item.get("title", ""),
                "content": item.get("content", ""),
                "url": item.get("url", ""),
                "source_name": item.get("source_name", ""),
                "source_type": item.get("source_type", ""),
                "equipment_mentions": item.get("equipment_mentions", []),
                "repair_type": repair_type,
                "scraped_at": datetime.now(),
            }

            table_id = f"{self.project_id}.safe_scraping.equipment_content"
            errors = self.bq_client.insert_rows_json(table_id, [record])

            if errors:
                logger.error(f"BigQuery error: {errors}")
                return False

            return True

        except Exception as e:
            logger.error(f"Store error: {str(e)[:100]}")
            return False

    async def scrape_all(self) -> Dict:
        """Scrape all safe sources"""
        results = {"total": 0, "stored": 0, "by_source": {}, "skipped": []}

        logger.info("🚀 Starting SAFE scraping (avoiding rate-limited sources)...")

        if not self.has_reddit_api:
            results["skipped"].append("Reddit (no API credentials)")
            logger.warning("⏭️ Skipping Reddit - no API credentials to avoid rate limits")

        # Scrape RSS feeds
        logger.info("\n📰 Scraping RSS feeds...")
        rss_items = await self.scrape_rss_feeds()
        results["total"] += len(rss_items)
        results["by_source"]["rss"] = len(rss_items)
        for item in rss_items:
            if self._store_item(item):
                results["stored"] += 1

        # Scrape manufacturer sites
        logger.info("\n🏭 Scraping manufacturer sites...")
        manufacturer_items = await self.scrape_manufacturer_sites()
        results["total"] += len(manufacturer_items)
        results["by_source"]["manufacturers"] = len(manufacturer_items)
        for item in manufacturer_items:
            if self._store_item(item):
                results["stored"] += 1

        logger.info(f"\n✅ SAFE scraping complete: {results['stored']}/{results['total']} items stored")
        logger.info(f"📊 By source: {results['by_source']}")
        if results["skipped"]:
            logger.info(f"⏭️ Skipped sources: {', '.join(results['skipped'])}")

        return results


# Make it work with the existing unified scraper API
class SimpleUnifiedScraper(SafeScraper):
    """Alias for compatibility with existing code"""

    pass


# Flask API Routes
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "Safe Scraper API",
            "reddit_configured": bool(os.environ.get("REDDIT_CLIENT_ID")),
        }
    )


@app.route("/scrape", methods=["POST"])
def scrape_endpoint():
    """General scraping endpoint"""
    try:
        # Get scrape type from request
        data = request.get_json() or {}
        scrape_type = data.get("type", "quick")

        # Run scraper in background
        def run_scrape():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = SafeScraper()
            return loop.run_until_complete(scraper.scrape_all())

        future = executor.submit(run_scrape)
        results = future.result(timeout=120)

        return jsonify(
            {"success": True, "results": results, "message": f"Scraped {results['stored']} items successfully"}
        )

    except Exception as e:
        logger.error(f"Scrape error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/scrape/quick", methods=["POST"])
def scrape_quick():
    """Quick scrape endpoint - just RSS feeds"""
    try:

        def run_quick_scrape():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = SafeScraper()
            items = loop.run_until_complete(scraper.scrape_rss_feeds())

            stored = 0
            for item in items:
                if scraper._store_item(item):
                    stored += 1

            return {"total": len(items), "stored": stored, "source": "rss_feeds_only"}

        future = executor.submit(run_quick_scrape)
        results = future.result(timeout=30)

        return jsonify(
            {"success": True, "results": results, "message": f"Quick scrape: {results['stored']} RSS items stored"}
        )

    except Exception as e:
        logger.error(f"Quick scrape error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/scrape/manufacturers", methods=["POST"])
def scrape_manufacturers():
    """Scrape manufacturer sites only"""
    try:

        def run_manufacturer_scrape():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = SafeScraper()
            items = loop.run_until_complete(scraper.scrape_manufacturer_sites())

            stored = 0
            for item in items:
                if scraper._store_item(item):
                    stored += 1

            return {"total": len(items), "stored": stored, "source": "manufacturers"}

        future = executor.submit(run_manufacturer_scrape)
        results = future.result(timeout=60)

        return jsonify(
            {"success": True, "results": results, "message": f"Manufacturer scrape: {results['stored']} items stored"}
        )

    except Exception as e:
        logger.error(f"Manufacturer scrape error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    """Get scraper status and configuration"""
    try:
        scraper = SafeScraper()

        return jsonify(
            {
                "status": "operational",
                "configuration": {
                    "reddit_api": scraper.has_reddit_api,
                    "project_id": scraper.project_id,
                    "sources": {
                        "rss_feeds": len(scraper.safe_sources.get("rss_feeds", [])),
                        "manufacturers": len(scraper.safe_sources.get("manufacturer_sites", [])),
                        "tech_docs": len(scraper.safe_sources.get("tech_docs", [])),
                        "market_data": len(scraper.safe_sources.get("market_data", [])),
                    },
                },
                "bigquery": {"dataset": f"{scraper.project_id}.safe_scraping", "table": "equipment_content"},
            }
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


async def main():
    """Test the safe scraper locally"""
    scraper = SafeScraper()
    results = await scraper.scrape_all()
    print(f"\n✅ Results: {results}")

    if not scraper.has_reddit_api:
        print("\n⚠️ TO ENABLE REDDIT SCRAPING:")
        print("1. Create Reddit app at: https://www.reddit.com/prefs/apps")
        print("2. Set environment variables:")
        print("   REDDIT_CLIENT_ID=your_client_id")
        print("   REDDIT_CLIENT_SECRET=your_secret")


if __name__ == "__main__":
    # If PORT is set, run as Flask server (for Cloud Run)
    port = int(os.environ.get("PORT", 0))
    if port:
        logger.info(f"🚀 Starting Safe Scraper API on port {port}")
        from waitress import serve

        serve(app, host="0.0.0.0", port=port)
    else:
        # Run test scrape locally
        asyncio.run(main())
