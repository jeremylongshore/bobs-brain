# Bob's Brain Scrapers Inventory

**Total Scrapers**: 10
**Combined Size**: ~200KB of code
**Data Sources**: 40+ sources across all scrapers

## Core Infrastructure Scrapers

### 1. **circle_of_life_scraper.py** (23KB)
- **Purpose**: Automatically runs overnight to gather repair knowledge
- **Features**:
  - Feeds directly into Bob's Brain learning system
  - Focus on Bobcat S740 and compact equipment
  - Core learning loop component
- **Status**: ✅ **KEEP** - Essential for learning system

### 2. **unified_scraper_simple.py** (11KB)
- **Purpose**: Simple unified scraper for multiple data sources
- **Features**: Basic implementation for scraping various sources
- **Status**: ⚠️ **EVALUATE** - May be redundant with API version

### 3. **unified_scraper_api.py** (5KB)
- **Purpose**: REST API server for unified scraping operations
- **Features**: API endpoints for scraping control
- **Status**: ✅ **KEEP** - Provides API interface

## Specialized Content Scrapers

### 4. **forum_scraper.py** (59KB) - LARGEST
- **Purpose**: Forum and community scraping with intelligence
- **Features**:
  - Extracts discussions, Q&A, user expertise
  - Playwright-based browser automation
  - Forum analysis and authentication detection
- **Status**: ⚠️ **EVALUATE** - Very large, may be over-engineered

### 5. **skidsteer_scraper.py** (36KB) - SECOND LARGEST
- **Purpose**: Specialized scraper for skid steer equipment
- **Features**:
  - Bobcat S740 specific knowledge
  - Equipment hacks and maintenance schedules
  - Problem/solution database
- **Status**: ⚠️ **EVALUATE** - Very specific, may be redundant

### 6. **tsb_scraper.py** (19KB)
- **Purpose**: Technical Service Bulletin (TSB) scraper
- **Features**:
  - Scrapes TSBs, recalls, service bulletins
  - NHTSA API integration
  - Vehicle/equipment specific
- **Status**: ✅ **KEEP** - Valuable official data source

### 7. **youtube_equipment_scraper.py** (16KB)
- **Purpose**: YouTube transcript extraction for equipment repair
- **Features**:
  - Extracts transcripts from repair videos
  - No video downloads (transcript only)
  - Equipment repair focused
- **Status**: ✅ **KEEP** - Good knowledge source

## Database Integration Scrapers

### 8. **neo4j_unified_scraper.py** (13KB)
- **Purpose**: Neo4j integrated scraper
- **Features**: Stores scraped data directly into graph database
- **Status**: ⚠️ **EVALUATE** - May be redundant with other integrations

### 9. **scraper_cloud_run.py** (13KB)
- **Purpose**: Cloud Run deployment wrapper for scrapers
- **Features**: Manages scraper deployment and orchestration
- **Status**: ✅ **KEEP** - Deployment infrastructure

### 10. **scraper_neo4j_router.py** (12KB)
- **Purpose**: Routes scraping results to Neo4j database
- **Features**: Database integration and data flow management
- **Status**: ⚠️ **EVALUATE** - May overlap with other Neo4j integrations

---

## Potential Redundancies & Cleanup Candidates

### 🔴 **High Priority for Review/Removal**

1. **skidsteer_scraper.py** (36KB)
   - Very specific to Bobcat S740
   - Large codebase for narrow use case
   - Functionality may be covered by other scrapers

2. **forum_scraper.py** (59KB)
   - Extremely large and complex
   - May be over-engineered for current needs
   - Playwright dependency adds complexity

### 🟡 **Medium Priority for Review**

3. **unified_scraper_simple.py** vs **unified_scraper_api.py**
   - Potential duplication of functionality
   - Keep API version, evaluate if simple version is needed

4. **neo4j_unified_scraper.py** vs **scraper_neo4j_router.py**
   - Both handle Neo4j integration
   - May be consolidatable

### ✅ **Definitely Keep**

- **circle_of_life_scraper.py** - Core learning system
- **tsb_scraper.py** - Official data source
- **youtube_equipment_scraper.py** - Good knowledge source
- **unified_scraper_api.py** - API interface
- **scraper_cloud_run.py** - Deployment infrastructure

---

## Recommendations

1. **Remove or significantly simplify** the two largest scrapers (forum + skidsteer)
2. **Consolidate** Neo4j integration into single component
3. **Choose one** unified scraper approach (API vs simple)
4. **Focus on** the core learning loop and essential data sources

**Potential Code Reduction**: ~100KB (50% reduction) by removing redundant/over-engineered components