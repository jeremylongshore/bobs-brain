#!/usr/bin/env python3
"""
Circle of Life Scraper API
Flask API for Cloud Run deployment
Runs overnight to gather Bobcat S740 and equipment knowledge
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from flask import Flask, jsonify, request

from circle_of_life_scraper import CircleOfLifeScraperIntegration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize scraper integration
scraper_integration = CircleOfLifeScraperIntegration()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        "status": "healthy",
        "service": "circle-of-life-scraper",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/scrape', methods=['POST'])
def trigger_scraping():
    """
    Trigger scraping operation
    Called by Cloud Scheduler at 2 AM daily
    """
    try:
        # Get scrape type from request
        data = request.get_json() or {}
        scrape_type = data.get('scrape_type', 'overnight')
        
        logger.info(f"🚀 Scraping triggered: {scrape_type}")
        
        # Run scraping in async context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        if scrape_type == 'overnight':
            results = loop.run_until_complete(
                scraper_integration.run_overnight_scraping()
            )
        else:
            # Quick scrape for testing
            results = loop.run_until_complete(
                scraper_integration.skidsteer_scraper.scrape_skidsteer_forums()
            )
        
        loop.close()
        
        return jsonify({
            "status": "success",
            "scrape_type": scrape_type,
            "results": results
        }), 200
        
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/scrape/status/<scrape_id>', methods=['GET'])
def get_scrape_status(scrape_id):
    """Get status of a scraping operation"""
    try:
        from google.cloud import bigquery
        
        client = bigquery.Client()
        query = f"""
        SELECT *
        FROM `bobs-house-ai.circle_of_life.scraping_history`
        WHERE scrape_id = '{scrape_id}'
        LIMIT 1
        """
        
        results = list(client.query(query).result())
        
        if results:
            row = results[0]
            return jsonify({
                "scrape_id": row.scrape_id,
                "status": row.status,
                "start_time": row.start_time.isoformat() if row.start_time else None,
                "end_time": row.end_time.isoformat() if row.end_time else None,
                "forums_scraped": row.forums_scraped,
                "threads_scraped": row.threads_scraped,
                "solutions_found": row.solutions_found,
                "s740_issues_found": row.s740_issues_found
            })
        else:
            return jsonify({"error": "Scrape ID not found"}), 404
            
    except Exception as e:
        logger.error(f"Failed to get scrape status: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/insights/today', methods=['GET'])
def get_todays_insights():
    """Get today's scraping insights"""
    try:
        from google.cloud import bigquery
        
        client = bigquery.Client()
        
        # Get today's S740 issues
        query = """
        SELECT 
            COUNT(*) as total_issues,
            COUNT(DISTINCT problem_type) as unique_problems,
            COUNT(DISTINCT solution) as unique_solutions
        FROM `bobs-house-ai.skidsteer_knowledge.bobcat_s740_issues`
        WHERE DATE(scraped_at) = CURRENT_DATE()
        """
        
        result = list(client.query(query).result())[0]
        
        # Get top problems
        query = """
        SELECT 
            problem_type,
            COUNT(*) as count
        FROM `bobs-house-ai.skidsteer_knowledge.bobcat_s740_issues`
        WHERE DATE(scraped_at) = CURRENT_DATE()
        GROUP BY problem_type
        ORDER BY count DESC
        LIMIT 5
        """
        
        top_problems = []
        for row in client.query(query).result():
            top_problems.append({
                "type": row.problem_type,
                "count": row.count
            })
        
        return jsonify({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_issues_found": result.total_issues,
            "unique_problems": result.unique_problems,
            "unique_solutions": result.unique_solutions,
            "top_problems": top_problems,
            "message": f"Found {result.total_issues} Bobcat S740 issues with {result.unique_solutions} solutions"
        })
        
    except Exception as e:
        logger.error(f"Failed to get insights: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/search/s740', methods=['GET'])
def search_s740_knowledge():
    """Search Bobcat S740 knowledge base"""
    try:
        query_text = request.args.get('q', '')
        
        if not query_text:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        from google.cloud import bigquery
        
        client = bigquery.Client()
        query = f"""
        SELECT 
            problem_type,
            problem_description,
            solution,
            ARRAY_TO_STRING(parts_needed, ', ') as parts,
            ARRAY_TO_STRING(error_codes, ', ') as codes,
            difficulty,
            cost_estimate
        FROM `bobs-house-ai.skidsteer_knowledge.bobcat_s740_issues`
        WHERE LOWER(problem_description) LIKE LOWER('%{query_text}%')
           OR LOWER(solution) LIKE LOWER('%{query_text}%')
           OR LOWER(ARRAY_TO_STRING(error_codes, ' ')) LIKE LOWER('%{query_text}%')
        LIMIT 10
        """
        
        results = []
        for row in client.query(query).result():
            results.append({
                "problem_type": row.problem_type,
                "problem": row.problem_description,
                "solution": row.solution,
                "parts_needed": row.parts,
                "error_codes": row.codes,
                "difficulty": row.difficulty,
                "cost": row.cost_estimate
            })
        
        return jsonify({
            "query": query_text,
            "results": results,
            "count": len(results)
        })
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/schedule/setup', methods=['POST'])
def setup_scheduler():
    """Set up Cloud Scheduler for overnight runs"""
    try:
        scraper_integration.setup_cloud_scheduler()
        return jsonify({
            "status": "success",
            "message": "Cloud Scheduler configured for 2 AM daily runs"
        })
    except Exception as e:
        logger.error(f"Failed to set up scheduler: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)