#!/usr/bin/env python3
"""
Fixed Unified Scraper for Circle of Life
Collects data from multiple sources to feed Bob's Brain
"""

import asyncio
import hashlib
import json
import logging
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional

import feedparser
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from google.cloud import bigquery

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
executor = ThreadPoolExecutor(max_workers=2)

class UnifiedScraper:
    """Unified scraper for all data sources"""
    
    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        try:
            self.bq_client = bigquery.Client(project=project_id)
            logger.info(f"✅ Connected to BigQuery project: {project_id}")
        except Exception as e:
            logger.error(f"❌ BigQuery connection failed: {e}")
            self.bq_client = None
            
        self._init_bigquery()
        
    def _init_bigquery(self):
        """Initialize BigQuery dataset and tables"""
        if not self.bq_client:
            return
            
        # Create dataset
        dataset_id = f"{self.project_id}.scraped_data"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset ready: {dataset_id}")
        except Exception as e:
            logger.error(f"Dataset creation error: {e}")
            
        # Create tables
        self._create_equipment_table()
        self._create_repair_table()
        
    def _create_equipment_table(self):
        """Create equipment knowledge table"""
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
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("cost_estimate", "FLOAT64"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]
        
        table_id = f"{self.project_id}.scraped_data.equipment_knowledge"
        table = bigquery.Table(table_id, schema=schema)
        
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table ready: equipment_knowledge")
        except Exception as e:
            logger.error(f"Table creation error: {e}")
            
    def _create_repair_table(self):
        """Create repair cases table"""
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("vehicle_type", "STRING"),
            bigquery.SchemaField("problem_description", "STRING"),
            bigquery.SchemaField("solution", "STRING"),
            bigquery.SchemaField("parts_used", "STRING", mode="REPEATED"),
            bigquery.SchemaField("cost", "FLOAT64"),
            bigquery.SchemaField("labor_hours", "FLOAT64"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]
        
        table_id = f"{self.project_id}.scraped_data.repair_cases"
        table = bigquery.Table(table_id, schema=schema)
        
        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table ready: repair_cases")
        except Exception as e:
            logger.error(f"Table creation error: {e}")
    
    async def scrape_rss_feeds(self) -> List[Dict]:
        """Scrape RSS feeds for equipment news"""
        feeds = [
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
            }
        ]
        
        all_items = []
        
        for feed_info in feeds:
            try:
                logger.info(f"📰 Scraping RSS: {feed_info['name']}")
                feed = feedparser.parse(feed_info["url"])
                
                if not feed.entries:
                    logger.warning(f"No entries found in {feed_info['name']}")
                    continue
                
                for entry in feed.entries[:20]:  # Get more entries
                    try:
                        title = entry.get("title", "")
                        summary = entry.get("summary", "")
                        link = entry.get("link", "")
                        
                        # Extract equipment mentions
                        equipment_brands = self._extract_equipment_brands(title + " " + summary)
                        
                        item = {
                            "id": hashlib.md5(link.encode()).hexdigest(),
                            "title": title[:500],
                            "content": summary[:5000],
                            "url": link,
                            "source": feed_info["name"],
                            "source_type": "rss",
                            "equipment_brand": equipment_brands[0] if equipment_brands else None,
                            "equipment_model": self._extract_model(title + " " + summary),
                            "error_codes": self._extract_error_codes(summary),
                            "repair_type": self._categorize_repair(title + " " + summary),
                            "cost_estimate": None,
                            "scraped_at": datetime.utcnow().isoformat()
                        }
                        all_items.append(item)
                    except Exception as e:
                        logger.error(f"Error processing entry: {e}")
                        continue
                        
                logger.info(f"   ✅ Scraped {len([i for i in all_items if i['source'] == feed_info['name']])} items from {feed_info['name']}")
                
            except Exception as e:
                logger.error(f"RSS feed error for {feed_info['name']}: {e}")
                continue
                
        return all_items
    
    async def scrape_youtube_transcripts(self) -> List[Dict]:
        """Scrape YouTube video transcripts"""
        channels = [
            {
                "name": "Pine Hollow Auto Diagnostics",
                "channel_id": "UCLpU5qla9_nYUGS85D4s-1Q",
                "search_terms": ["diagnostic", "repair", "troubleshooting"]
            },
            {
                "name": "Scanner Danner",
                "channel_id": "UCtAGzm9e_liY7ko1PBhzTHA",
                "search_terms": ["scan tool", "diagnostic", "waveform"]
            },
            {
                "name": "South Main Auto",
                "channel_id": "UCWng6bxEbxA",
                "search_terms": ["repair", "diagnosis", "fix"]
            }
        ]
        
        all_items = []
        
        # For now, return mock data since YouTube API needs setup
        # In production, this would use youtube-transcript-api
        logger.info("📺 YouTube scraping configured but needs API key")
        
        return all_items
    
    async def scrape_forums(self) -> List[Dict]:
        """Scrape equipment forums"""
        forums = [
            {
                "name": "BobcatForum",
                "url": "https://www.bobcatforum.com/forums/",
                "category": "bobcat"
            },
            {
                "name": "TractorByNet",
                "url": "https://www.tractorbynet.com/forums/",
                "category": "tractors"
            }
        ]
        
        all_items = []
        
        for forum in forums:
            try:
                logger.info(f"💬 Scraping forum: {forum['name']}")
                
                # Forums typically need authentication
                # For now, we'll skip to avoid rate limiting
                logger.info(f"   ⏭️ Skipping {forum['name']} - needs authentication")
                
            except Exception as e:
                logger.error(f"Forum error for {forum['name']}: {e}")
                
        return all_items
    
    def _extract_equipment_brands(self, text: str) -> List[str]:
        """Extract equipment brand mentions"""
        brands = [
            "Bobcat", "Caterpillar", "CAT", "John Deere", "Kubota",
            "Case", "New Holland", "Komatsu", "Volvo", "Hitachi",
            "Ford", "Chevrolet", "GMC", "Ram", "Dodge",
            "Cummins", "Duramax", "Powerstroke"
        ]
        
        text_lower = text.lower()
        found = []
        
        for brand in brands:
            if brand.lower() in text_lower:
                found.append(brand)
                
        return found
    
    def _extract_model(self, text: str) -> Optional[str]:
        """Extract equipment model numbers"""
        import re
        
        # Look for patterns like S740, T770, F-250, etc.
        patterns = [
            r'[A-Z]\d{3,4}',  # S740, T770
            r'[A-Z]{1,2}-\d{3,4}',  # F-250, MT-85
            r'\d{3,4}[A-Z]{1,2}',  # 2500HD
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
                
        return None
    
    def _extract_error_codes(self, text: str) -> List[str]:
        """Extract error codes from text"""
        import re
        
        # Look for patterns like P0087, P0299, etc.
        pattern = r'[PBCUc][0-9A-F]{4}'
        matches = re.findall(pattern, text.upper())
        
        return list(set(matches))  # Remove duplicates
    
    def _categorize_repair(self, text: str) -> Optional[str]:
        """Categorize the type of repair"""
        text_lower = text.lower()
        
        categories = {
            "hydraulic": ["hydraulic", "pump", "cylinder", "valve"],
            "engine": ["engine", "motor", "piston", "crankshaft", "camshaft"],
            "electrical": ["electrical", "wiring", "battery", "alternator", "starter"],
            "transmission": ["transmission", "gear", "clutch", "torque converter"],
            "fuel": ["fuel", "injector", "pump", "filter", "tank"],
            "cooling": ["coolant", "radiator", "thermostat", "water pump"],
            "exhaust": ["exhaust", "dpf", "def", "egr", "turbo"],
            "brakes": ["brake", "caliper", "rotor", "pad"],
            "suspension": ["suspension", "shock", "strut", "spring"]
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
                
        return "general"
    
    def store_to_bigquery(self, items: List[Dict], table_name: str = "equipment_knowledge") -> int:
        """Store scraped items to BigQuery"""
        if not self.bq_client or not items:
            return 0
            
        table_id = f"{self.project_id}.scraped_data.{table_name}"
        
        stored = 0
        errors = []
        
        for item in items:
            try:
                # Ensure timestamp is properly formatted
                if 'scraped_at' in item and isinstance(item['scraped_at'], str):
                    item['scraped_at'] = datetime.fromisoformat(item['scraped_at'].replace('Z', '+00:00'))
                else:
                    item['scraped_at'] = datetime.utcnow()
                    
                # Insert row
                errors = self.bq_client.insert_rows_json(table_id, [item])
                
                if not errors:
                    stored += 1
                else:
                    logger.error(f"BigQuery insert errors: {errors}")
                    
            except Exception as e:
                logger.error(f"Error storing item: {e}")
                continue
                
        logger.info(f"✅ Stored {stored}/{len(items)} items to BigQuery")
        return stored
    
    async def scrape_all(self) -> Dict:
        """Run all scrapers"""
        logger.info("🚀 Starting unified scraping...")
        
        results = {
            "rss": [],
            "youtube": [],
            "forums": [],
            "total": 0,
            "stored": 0
        }
        
        try:
            # Run scrapers
            results["rss"] = await self.scrape_rss_feeds()
            results["youtube"] = await self.scrape_youtube_transcripts()
            results["forums"] = await self.scrape_forums()
            
            # Combine all results
            all_items = results["rss"] + results["youtube"] + results["forums"]
            results["total"] = len(all_items)
            
            # Store to BigQuery
            results["stored"] = self.store_to_bigquery(all_items)
            
            logger.info(f"✅ Scraping complete: {results['total']} items found, {results['stored']} stored")
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            logger.error(traceback.format_exc())
            
        return results

# Flask API Routes
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Unified Scraper",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/scrape", methods=["POST"])
def scrape_endpoint():
    """General scraping endpoint"""
    try:
        def run_scrape():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = UnifiedScraper()
            return loop.run_until_complete(scraper.scrape_all())
        
        future = executor.submit(run_scrape)
        results = future.result(timeout=120)
        
        return jsonify({
            "success": True,
            "results": results,
            "message": f"Scraped {results['total']} items, stored {results['stored']}"
        })
        
    except Exception as e:
        logger.error(f"Scrape endpoint error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/scrape/quick", methods=["POST"])
def scrape_quick():
    """Quick scrape - RSS feeds only"""
    try:
        def run_quick():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            scraper = UnifiedScraper()
            items = loop.run_until_complete(scraper.scrape_rss_feeds())
            stored = scraper.store_to_bigquery(items)
            return {"total": len(items), "stored": stored}
        
        future = executor.submit(run_quick)
        results = future.result(timeout=60)
        
        return jsonify({
            "success": True,
            "results": results,
            "message": f"Quick scrape complete: {results['stored']} items stored"
        })
        
    except Exception as e:
        logger.error(f"Quick scrape error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/stats", methods=["GET"])
def get_stats():
    """Get scraping statistics"""
    try:
        scraper = UnifiedScraper()
        
        if not scraper.bq_client:
            return jsonify({"error": "BigQuery not connected"}), 500
            
        query = """
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT source) as sources,
            MAX(scraped_at) as last_scrape
        FROM `bobs-house-ai.scraped_data.equipment_knowledge`
        """
        
        results = scraper.bq_client.query(query).result()
        row = list(results)[0] if results.total_rows > 0 else None
        
        if row:
            return jsonify({
                "total_records": row.total_records,
                "sources": row.sources,
                "last_scrape": row.last_scrape.isoformat() if row.last_scrape else None
            })
        else:
            return jsonify({
                "total_records": 0,
                "sources": 0,
                "last_scrape": None
            })
            
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    
    if port:
        logger.info(f"🚀 Starting Unified Scraper API on port {port}")
        app.run(host="0.0.0.0", port=port, debug=False)
    else:
        # Run test scrape locally
        async def test():
            scraper = UnifiedScraper()
            results = await scraper.scrape_all()
            print(json.dumps(results, indent=2))
            
        asyncio.run(test())