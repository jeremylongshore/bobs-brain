#!/usr/bin/env python3
"""
Cloud Run API for Unified Scraper
Minimalistic, efficient, and production-ready
"""

import asyncio
import logging
import os
from datetime import datetime

from flask import Flask, jsonify, request

# Import scrapers - use simple scraper for reliable storage
try:
    from unified_scraper_simple import SimpleUnifiedScraper

    scraper_class = SimpleUnifiedScraper
except ImportError:
    try:
        from unified_scraper_enhanced import EnhancedUnifiedScraper

        scraper_class = EnhancedUnifiedScraper
    except ImportError:
        from unified_scraper import UnifiedScraper

        scraper_class = UnifiedScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask
app = Flask(__name__)

# Global scraper instance (reused for efficiency)
scraper = None


def get_scraper():
    """Get or create scraper instance"""
    global scraper
    if scraper is None:
        scraper = scraper_class()
    return scraper


@app.route("/health", methods=["GET"])
def health():
    """Health check for Cloud Run"""
    return jsonify(
        {"status": "healthy", "service": "unified-scraper", "version": "2.0.0", "timestamp": datetime.now().isoformat()}
    )


@app.route("/scrape", methods=["POST"])
def scrape():
    """
    Main scraping endpoint
    Can be triggered by scheduler or manually
    """
    try:
        # Get parameters
        data = request.get_json() or {}
        scrape_type = data.get("type", "all")
        priority = data.get("priority", "all")

        logger.info(f"🚀 Scraping triggered: type={scrape_type}, priority={priority}")

        # Run async scraper in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            scraper = get_scraper()

            # Handle different scraper methods
            if hasattr(scraper, "scrape_all"):
                # Simple scraper
                results = loop.run_until_complete(scraper.scrape_all())
            elif hasattr(scraper, "scrape_all_sources"):
                # Enhanced scraper with categories
                categories = None if priority == "all" else [priority]
                results = loop.run_until_complete(scraper.scrape_all_sources(categories))
            else:
                # Basic scraper fallback
                if priority != "all" and priority in scraper.priority_sources:
                    original_sources = scraper.priority_sources.copy()
                    scraper.priority_sources = {priority: scraper.priority_sources[priority]}
                    results = loop.run_until_complete(scraper.scrape_all_parallel())
                    scraper.priority_sources = original_sources
                else:
                    results = loop.run_until_complete(scraper.scrape_all_parallel())

            return (
                jsonify(
                    {
                        "status": "success",
                        "results": {
                            "total_scraped": results.get("total_scraped", results.get("total_items", 0)),
                            "by_type": results.get("by_type", {}),
                            "by_category": results.get("by_category", results.get("by_priority", {})),
                            "errors": len(results.get("errors", [])),
                        },
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Scraping error: {e}")
        return jsonify({"status": "error", "message": str(e)[:500]}), 500


@app.route("/scrape/quick", methods=["POST"])
def scrape_quick():
    """
    Quick scrape endpoint - only critical sources
    Faster response for immediate needs
    """
    try:
        logger.info("⚡ Quick scrape triggered")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            scraper = get_scraper()

            # Handle different scraper methods for quick scrape
            if hasattr(scraper, "scrape_all"):
                # Simple scraper - just run it (it's already fast)
                results = loop.run_until_complete(scraper.scrape_all())
            elif hasattr(scraper, "scrape_all_sources"):
                # Enhanced scraper - limit to critical sources
                results = loop.run_until_complete(scraper.scrape_all_sources(["reddit_communities"]))
            else:
                # Basic scraper - only critical priority
                original_sources = scraper.priority_sources.copy()
                scraper.priority_sources = {"critical": scraper.priority_sources.get("critical", [])}
                results = loop.run_until_complete(scraper.scrape_all_parallel())
                scraper.priority_sources = original_sources

            return (
                jsonify(
                    {
                        "status": "success",
                        "type": "quick",
                        "items_scraped": results.get("total_scraped", 0),
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                200,
            )

        finally:
            loop.close()

    except Exception as e:
        logger.error(f"Quick scrape error: {e}")
        return jsonify({"status": "error", "message": str(e)[:500]}), 500


@app.route("/stats", methods=["GET"])
def stats():
    """Get scraping statistics from BigQuery"""
    try:
        from google.cloud import bigquery

        client = bigquery.Client()

        # Get today's stats - check both datasets
        results = None
        for dataset_table in ["simple_scraping.content", "comprehensive_scraping.all_content"]:
            try:
                query = f"""
                SELECT
                    COUNT(*) as total_items,
                    COUNT(DISTINCT {'url' if 'simple' in dataset_table else 'source_url'}) as unique_sources,
                    COUNT(DISTINCT source_type) as source_types,
                    MAX(scraped_at) as last_scrape
                FROM `bobs-house-ai.{dataset_table}`
                WHERE DATE(scraped_at) = CURRENT_DATE()
                """

                results = list(client.query(query).result())
                if results and results[0].total_items > 0:
                    break
            except Exception:
                continue

        if results:
            row = results[0]
            return jsonify(
                {
                    "today": {
                        "total_items": row.total_items,
                        "unique_sources": row.unique_sources,
                        "source_types": row.source_types,
                        "last_scrape": row.last_scrape.isoformat() if row.last_scrape else None,
                    },
                    "status": "success",
                }
            )

        return jsonify({"today": {}, "status": "no_data"})

    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({"error": str(e)[:500]}), 500


@app.route("/search", methods=["GET"])
def search():
    """Search scraped content"""
    try:
        query_text = request.args.get("q", "")
        topic = request.args.get("topic", "")
        limit = min(int(request.args.get("limit", 10)), 50)

        if not query_text:
            return jsonify({"error": "Query parameter 'q' required"}), 400

        from google.cloud import bigquery

        client = bigquery.Client()

        # Build query
        sql = """
        SELECT title, content, source_url, topic, scraped_at
        FROM `bobs-house-ai.comprehensive_scraping.all_content`
        WHERE LOWER(content) LIKE LOWER(@query)
        """

        if topic:
            sql += " AND topic = @topic"

        sql += f" ORDER BY scraped_at DESC LIMIT {limit}"

        # Execute query
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("query", "STRING", f"%{query_text}%"),
                bigquery.ScalarQueryParameter("topic", "STRING", topic) if topic else None,
            ]
        )

        results = client.query(sql, job_config=job_config).result()

        items = []
        for row in results:
            items.append(
                {
                    "title": row.title,
                    "content": row.content[:500],
                    "source": row.source_url,
                    "topic": row.topic,
                    "scraped_at": row.scraped_at.isoformat() if row.scraped_at else None,
                }
            )

        return jsonify({"query": query_text, "results": items, "count": len(items)})

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"error": str(e)[:500]}), 500


@app.route("/api/process", methods=["POST"])
def api_process():
    """Process scraped content - stores in BigQuery and/or Neo4j"""
    try:
        data = request.get_json() or {}

        # Validate required fields
        if not data.get("url") or not data.get("content"):
            return jsonify({"error": "Missing required fields: url and content"}), 400

        # Prepare content for storage
        content_item = {
            "url": data.get("url"),
            "title": data.get("title", "Untitled"),
            "content": data.get("content"),
            "type": data.get("type", data.get("source_type", "manual")),
            "topic": data.get("topic", "general"),
            "metadata": data.get("metadata", {}),
            "timestamp": data.get("timestamp", datetime.now().isoformat()),
        }

        # Store in BigQuery
        scraper = get_scraper()
        stored = False

        if hasattr(scraper, "store_to_bigquery"):
            # Use existing storage method
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            stored = loop.run_until_complete(scraper.store_to_bigquery([content_item], "manual_submission"))
        else:
            # Direct BigQuery insert
            from google.cloud import bigquery

            client = bigquery.Client(project="bobs-house-ai")

            table_id = "bobs-house-ai.comprehensive_scraping.all_content"
            table = client.get_table(table_id)

            # Add required fields
            content_item["source"] = "api_process"
            content_item["scraped_at"] = datetime.now().isoformat()

            errors = client.insert_rows_json(table, [content_item])
            stored = len(errors) == 0

            if errors:
                logger.error(f"BigQuery insert errors: {errors}")

        # Also try to store in Neo4j if router is available
        neo4j_stored = False
        try:
            from scraper_neo4j_router import ScraperIntegration

            integration = ScraperIntegration()
            neo4j_stored = integration.process_scraped_data(content_item)
        except Exception as e:
            logger.warning(f"Neo4j storage not available: {e}")

        return jsonify(
            {
                "status": "processed",
                "bigquery_stored": stored,
                "neo4j_stored": neo4j_stored,
                "url": content_item["url"],
                "timestamp": content_item["timestamp"],
            }
        )

    except Exception as e:
        logger.error(f"Process error: {e}")
        return jsonify({"error": "Failed to process content", "details": str(e)[:500]}), 500


@app.route("/topics", methods=["GET"])
def topics():
    """Get available topics and counts"""
    try:
        from google.cloud import bigquery

        client = bigquery.Client()

        query = """
        SELECT topic, COUNT(*) as count
        FROM `bobs-house-ai.comprehensive_scraping.all_content`
        GROUP BY topic
        ORDER BY count DESC
        """

        results = client.query(query).result()

        topics_list = []
        for row in results:
            topics_list.append({"topic": row.topic, "count": row.count})

        return jsonify({"topics": topics_list, "total": len(topics_list)})

    except Exception as e:
        logger.error(f"Topics error: {e}")
        return jsonify({"error": str(e)[:500]}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Unified Scraper API on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)
