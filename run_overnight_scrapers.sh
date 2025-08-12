#!/bin/bash
# Overnight Scraper Runner - Runs all scrapers and dumps to Neo4j

echo "🌙 Starting overnight scraping at $(date)"
echo "================================================"

# Set project directory
cd /home/jeremylongshore/bobs-brain

# Export environment variables
export GOOGLE_CLOUD_PROJECT=bobs-house-ai
export NEO4J_URI=bolt://10.128.0.2:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=BobBrain2025

# Function to trigger scrapers via Cloud Run
trigger_scrapers() {
    echo "🚀 Triggering Neo4j scrapers..."
    
    # Trigger unified scraper (if deployed)
    echo "  Triggering unified scraper..."
    curl -X POST https://unified-scraper-157908567967.us-central1.run.app/scrape \
        -H "Content-Type: application/json" \
        -d '{"type":"overnight"}' || echo "    Unified scraper not responding"
    
    # Trigger Circle of Life scraper
    echo "  Triggering Circle of Life scraper..."
    curl -X POST https://circle-of-life-scraper-157908567967.us-central1.run.app/scrape \
        -H "Content-Type: application/json" \
        -d '{"scrape_type":"overnight"}' || echo "    Circle of Life scraper not responding"
    
    echo "✅ Scraper triggers sent"
}

# Function to run local scrapers
run_local_scrapers() {
    echo "🖥️ Running local scrapers..."
    
    # Run YouTube scraper
    echo "  Running YouTube equipment scraper..."
    python3 -c "
import asyncio
import sys
sys.path.append('src')
from youtube_equipment_scraper import YouTubeEquipmentScraper

async def run():
    scraper = YouTubeEquipmentScraper(use_neo4j=True)
    queries = [
        'Bobcat S740 hydraulic problems',
        'mini skid steer repair',
        'diesel truck DPF regeneration',
        'compact tractor troubleshooting'
    ]
    total = 0
    for q in queries:
        try:
            count = await scraper.search_and_scrape(q, max_results=25)
            total += count
            print(f'    ✅ {q}: {count} videos')
            await asyncio.sleep(10)
        except Exception as e:
            print(f'    ❌ Error: {e}')
    print(f'  Total YouTube videos: {total}')

asyncio.run(run())
" 2>/dev/null || echo "    YouTube scraper failed"
    
    # Run TSB scraper
    echo "  Running TSB scraper..."
    python3 -c "
import asyncio
import sys
sys.path.append('src')
from tsb_scraper import TSBScraper

async def run():
    scraper = TSBScraper(use_neo4j=True)
    try:
        equipment = await scraper.scrape_equipment_tsbs()
        trucks = await scraper.scrape_diesel_truck_tsbs()
        print(f'    ✅ TSBs: {equipment + trucks} bulletins')
    except Exception as e:
        print(f'    ❌ Error: {e}')

asyncio.run(run())
" 2>/dev/null || echo "    TSB scraper failed"
}

# Main loop - run every hour all night
HOURS_TO_RUN=8
CURRENT_HOUR=0

while [ $CURRENT_HOUR -lt $HOURS_TO_RUN ]; do
    echo ""
    echo "🕐 Hour $((CURRENT_HOUR + 1)) of $HOURS_TO_RUN - $(date)"
    echo "----------------------------------------"
    
    # Try cloud scrapers first
    trigger_scrapers
    
    # Also run local scrapers
    run_local_scrapers
    
    # Check Neo4j status
    echo ""
    echo "📊 Checking Neo4j status..."
    python3 -c "
from neo4j import GraphDatabase
try:
    driver = GraphDatabase.driver('bolt://10.128.0.2:7687', auth=('neo4j', 'BobBrain2025'))
    with driver.session() as session:
        result = session.run('MATCH (n) RETURN count(n) as total')
        total = result.single()['total']
        print(f'    ✅ Neo4j nodes: {total}')
    driver.close()
except Exception as e:
    print(f'    ❌ Neo4j error: {e}')
" 2>/dev/null || echo "    Neo4j check failed"
    
    # Increment hour
    CURRENT_HOUR=$((CURRENT_HOUR + 1))
    
    # Sleep for 1 hour if not the last iteration
    if [ $CURRENT_HOUR -lt $HOURS_TO_RUN ]; then
        echo ""
        echo "💤 Sleeping for 1 hour until next run..."
        sleep 3600
    fi
done

echo ""
echo "================================================"
echo "✅ Overnight scraping complete at $(date)"
echo "   Ran for $HOURS_TO_RUN hours"
echo "   Data stored in Neo4j at bolt://10.128.0.2:7687"
echo "================================================"