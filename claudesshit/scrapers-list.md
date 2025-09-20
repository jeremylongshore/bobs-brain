# Bob's Brain Scrapers - Complete List

## Current Scrapers in src/

### 1. **circle_of_life_scraper.py** (23KB)
- **Purpose**: Core learning system - automatically runs overnight
- **Function**: Feeds repair knowledge into Bob's Brain learning loop
- **Focus**: Bobcat S740 and compact equipment
- **Integration**: Essential for Circle of Life learning

### 2. **forum_scraper.py** (59KB) - LARGEST FILE
- **Purpose**: Forum and community discussion scraping
- **Function**: Extracts Q&A, discussions, user expertise from forums
- **Technology**: Playwright browser automation, complex analysis
- **Integration**: Forum intelligence and authentication detection

### 3. **neo4j_unified_scraper.py** (13KB)
- **Purpose**: Neo4j database integrated scraper
- **Function**: Stores scraped data directly into graph database
- **Integration**: Direct Neo4j connection for data storage

### 4. **scraper_cloud_run.py** (13KB)
- **Purpose**: Cloud Run deployment orchestration
- **Function**: Manages scraper deployment and cloud execution
- **Integration**: Infrastructure for running scrapers in cloud

### 5. **scraper_neo4j_router.py** (12KB)
- **Purpose**: Routes scraping results to Neo4j
- **Function**: Database integration and data flow management
- **Integration**: Neo4j data routing and management

### 6. **skidsteer_scraper.py** (36KB) - SECOND LARGEST
- **Purpose**: Specialized Bobcat S740 skid steer scraper
- **Function**: Equipment hacks, maintenance schedules, problem/solution DB
- **Focus**: Very specific to Bobcat S740 equipment
- **Integration**: Specialized equipment knowledge

### 7. **tsb_scraper.py** (19KB)
- **Purpose**: Technical Service Bulletin scraper
- **Function**: Scrapes TSBs, recalls, service bulletins
- **Technology**: NHTSA API integration
- **Integration**: Official manufacturer data

### 8. **unified_scraper_api.py** (5KB)
- **Purpose**: REST API for scraping operations
- **Function**: Provides API endpoints for scraper control
- **Integration**: Web API interface for scraping management

### 9. **unified_scraper_simple.py** (11KB)
- **Purpose**: Simple unified scraper implementation
- **Function**: Basic multi-source scraping capability
- **Integration**: Simplified scraping interface

### 10. **youtube_equipment_scraper.py** (16KB)
- **Purpose**: YouTube transcript extraction
- **Function**: Extracts repair video transcripts (no video downloads)
- **Focus**: Equipment repair knowledge from video content
- **Integration**: Video-based knowledge extraction

---

## Summary Stats
- **Total Scrapers**: 10
- **Total Code Size**: ~215KB
- **Largest**: forum_scraper.py (59KB)
- **Second Largest**: skidsteer_scraper.py (36KB)
- **Focus Areas**: Forums, Equipment, TSBs, YouTube, Neo4j Integration

---

**Ready for your direction on which ones to move to diagnostic-platform/scraper/**