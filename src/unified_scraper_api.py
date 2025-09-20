#!/usr/bin/env python3
"""
Unified Scraper API Server for Cloud Run
Provides HTTP endpoints for scraping operations
"""

import asyncio
import logging
import os
from datetime import datetime
from flask import Flask, jsonify, request

# Import scrapers
from unified_scraper_simple import SimpleUnifiedScraper
from youtube_equipment_scraper import YouTubeEquipmentScraper
from tsb_scraper import TSBScraper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize scrapers
simple_scraper = SimpleUnifiedScraper()
youtube_scraper = YouTubeEquipmentScraper(use_neo4j=True)
tsb_scraper = TSBScraper(use_neo4j=True)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "unified-scraper",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "neo4j_enabled": True
    })

@app.route('/scrape', methods=['POST'])
def scrape():
    """Main scraping endpoint"""
    try:
        data = request.get_json() or {}
        scrape_type = data.get('type', 'quick')

        logger.info(f"🚀 Scraping triggered: type={scrape_type}")

        # Run async scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            # Always use scrape_all for now
            results = loop.run_until_complete(simple_scraper.scrape_all())
        finally:
            loop.close()

        return jsonify({
            "status": "success",
            "type": scrape_type,
            "items_scraped": results.get('total_items', 0),
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/scrape/youtube', methods=['POST'])
def scrape_youtube():
    """Scrape YouTube transcripts"""
    try:
        data = request.get_json() or {}
        query = data.get('query', 'equipment repair')
        max_results = data.get('max_results', 5)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            count = loop.run_until_complete(
                youtube_scraper.search_and_scrape(query, max_results)
            )

            return jsonify({
                "status": "success",
                "query": query,
                "transcripts_scraped": count
            }), 200

        finally:
            loop.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape/tsb', methods=['POST'])
def scrape_tsb():
    """Scrape Technical Service Bulletins"""
    try:
        data = request.get_json() or {}
        manufacturer = data.get('manufacturer', 'Bobcat')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            equipment_tsbs = loop.run_until_complete(
                tsb_scraper.scrape_equipment_tsbs()
            )

            truck_tsbs = loop.run_until_complete(
                tsb_scraper.scrape_diesel_truck_tsbs()
            )

            total = equipment_tsbs + truck_tsbs

            return jsonify({
                "status": "success",
                "manufacturer": manufacturer,
                "tsbs_found": total,
                "equipment": equipment_tsbs,
                "trucks": truck_tsbs
            }), 200

        finally:
            loop.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scrape/quick', methods=['POST'])
def scrape_quick():
    """Quick scrape endpoint for scheduler"""
    try:
        logger.info("⚡ Quick scrape triggered")

        # Run async scraping
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            results = loop.run_until_complete(simple_scraper.scrape_all())
        finally:
            loop.close()

        return jsonify({
            "status": "success",
            "type": "quick",
            "items": results.get('total_items', 0),
            "timestamp": datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Quick scrape error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Unified Scraper API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)