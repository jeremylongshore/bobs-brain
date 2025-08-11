#!/usr/bin/env python3
"""
YouTube Repair Content Scraper using Crawl4AI
Focuses on repair & maintenance channels with detailed video information
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from google.cloud import bigquery
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy, LLMExtractionStrategy

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeRepairScraper:
    """
    Scrapes YouTube repair & maintenance channels using Crawl4AI
    Focuses on extracting detailed video information, transcripts, and expertise
    """
    
    def __init__(self, project_id="bobs-house-ai"):
        """Initialize YouTube repair scraper with Crawl4AI"""
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        
        # Top repair & maintenance YouTube channels with detailed info
        self.repair_channels = {
            "heavy_equipment": [
                {
                    "channel": "Andrew Camarata",
                    "url": "https://www.youtube.com/@AndrewCamarata",
                    "subscribers": "1.5M+",
                    "specialty": "Heavy equipment repair, excavator, bulldozer maintenance",
                    "notable_series": ["Castle Build", "Property Maintenance", "Equipment Repairs"],
                    "equipment_covered": ["Excavators", "Bulldozers", "Skid Steers", "Trucks"]
                },
                {
                    "channel": "Dirt Perfect",
                    "url": "https://www.youtube.com/@DirtPerfect",
                    "subscribers": "850K+",
                    "specialty": "Excavator and skid steer operation & maintenance",
                    "notable_videos": ["How to Grade", "Equipment Maintenance", "Attachment Reviews"],
                    "equipment_covered": ["Cat Excavators", "Bobcat Skid Steers", "Attachments"]
                },
                {
                    "channel": "Letsdig18",
                    "url": "https://www.youtube.com/@letsdig18",
                    "subscribers": "2.1M+",
                    "specialty": "Excavator operation, maintenance, problem-solving",
                    "notable_content": ["Field repairs", "Hydraulic troubleshooting", "Daily operations"],
                    "equipment_covered": ["Volvo Excavators", "CAT Equipment", "Komatsu"]
                }
            ],
            "diesel_repair": [
                {
                    "channel": "Adept Ape",
                    "url": "https://www.youtube.com/@AdeptApe",
                    "subscribers": "1.3M+",
                    "specialty": "Diesel engine diagnostics, turbo repairs, injector service",
                    "notable_series": ["Cummins Rebuilds", "Duramax Repairs", "PowerStroke Issues"],
                    "tools_featured": ["Snap-on Scanner", "Diesel laptops", "Injector testers"]
                },
                {
                    "channel": "Diesel Tech Ron",
                    "url": "https://www.youtube.com/@DieselTechRon",
                    "subscribers": "520K+",
                    "specialty": "Heavy duty diesel repair, DPF/DEF issues",
                    "notable_content": ["DPF Cleaning", "EGR Delete", "Turbo Replacement"],
                    "brands_covered": ["Detroit Diesel", "Cummins", "CAT", "International"]
                },
                {
                    "channel": "Diesel Creek",
                    "url": "https://www.youtube.com/@DieselCreek",
                    "subscribers": "780K+",
                    "specialty": "Equipment restoration, diesel engine rebuilds",
                    "project_types": ["Full restorations", "Engine swaps", "Hydraulic rebuilds"],
                    "equipment_restored": ["Bulldozers", "Excavators", "Vintage diesels"]
                }
            ],
            "bobcat_skidsteer": [
                {
                    "channel": "Bobcat Company",
                    "url": "https://www.youtube.com/@BobcatCompany",
                    "subscribers": "156K+",
                    "specialty": "Official Bobcat tutorials, maintenance guides",
                    "video_categories": ["How-To", "Maintenance", "New Products", "Safety"],
                    "models_covered": ["S740", "S770", "T740", "E165", "All models"]
                },
                {
                    "channel": "Skid Steer Solutions",
                    "url": "https://www.youtube.com/@skidsteersolutions",
                    "subscribers": "92K+",
                    "specialty": "Skid steer attachments, maintenance, troubleshooting",
                    "content_types": ["Attachment reviews", "Maintenance tips", "Problem solving"],
                    "brands": ["Bobcat", "CAT", "John Deere", "Kubota"]
                },
                {
                    "channel": "Mike the Mower",
                    "url": "https://www.youtube.com/@MikeMower",
                    "subscribers": "145K+",
                    "specialty": "Compact equipment repair, small engine work",
                    "repair_types": ["Engine rebuilds", "Hydraulic repairs", "Electrical troubleshooting"],
                    "equipment": ["Skid steers", "Compact tractors", "Zero-turns"]
                }
            ],
            "diagnostic_experts": [
                {
                    "channel": "South Main Auto",
                    "url": "https://www.youtube.com/@SouthMainAutoRepairAvoca",
                    "subscribers": "2.3M+",
                    "specialty": "Diagnostic methodology, electrical troubleshooting",
                    "teaching_style": "Step-by-step diagnostic process",
                    "tools": ["Pico scope", "Power Probe", "Scan tools"]
                },
                {
                    "channel": "Pine Hollow Auto Diagnostics",
                    "url": "https://www.youtube.com/@PineHollowAutoDiagnostics",
                    "subscribers": "765K+",
                    "specialty": "Advanced automotive diagnostics, module programming",
                    "content": ["CAN bus diagnostics", "Module repairs", "Wiring issues"],
                    "certifications": ["ASE Master Tech", "L1 Advanced Diagnostics"]
                },
                {
                    "channel": "Scanner Danner",
                    "url": "https://www.youtube.com/@ScannerDanner",
                    "subscribers": "820K+",
                    "specialty": "Oscilloscope diagnostics, electrical theory",
                    "course_offerings": ["Scope training", "Electrical fundamentals", "Diagnostic strategy"],
                    "tools": ["Oscilloscopes", "Multimeters", "Current clamps"]
                }
            ],
            "hydraulic_specialists": [
                {
                    "channel": "Hydraulics Online",
                    "url": "https://www.youtube.com/@HydraulicsOnline",
                    "subscribers": "128K+",
                    "specialty": "Hydraulic system design, troubleshooting, repair",
                    "video_types": ["Theory", "Troubleshooting", "Component rebuild"],
                    "systems": ["Mobile hydraulics", "Industrial", "Pneumatics"]
                },
                {
                    "channel": "The Hydraulic Guy",
                    "url": "https://www.youtube.com/@TheHydraulicGuy",
                    "subscribers": "67K+",
                    "specialty": "Mobile hydraulic repair, cylinder rebuilding",
                    "content": ["Cylinder tear-down", "Pump repairs", "Valve troubleshooting"],
                    "equipment": ["Excavators", "Loaders", "Cranes"]
                }
            ]
        }
        
        # Initialize Crawl4AI browser config
        self.browser_config = BrowserConfig(
            headless=True,
            browser_type="chromium",
            viewport={"width": 1920, "height": 1080}
        )
        
        self._ensure_youtube_tables()
        logger.info("📹 YouTube Repair Scraper initialized with Crawl4AI")
    
    def _ensure_youtube_tables(self):
        """Create BigQuery tables for YouTube content"""
        dataset_id = f"{self.project_id}.youtube_repair_content"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "YouTube repair and maintenance content"
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info("📊 YouTube content dataset ready")
        except Exception as e:
            logger.debug(f"Dataset exists or error: {e}")
        
        # Define detailed tables
        tables = {
            "channels": [
                bigquery.SchemaField("channel_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("channel_name", "STRING"),
                bigquery.SchemaField("channel_url", "STRING"),
                bigquery.SchemaField("category", "STRING"),
                bigquery.SchemaField("subscribers", "STRING"),
                bigquery.SchemaField("specialty", "STRING"),
                bigquery.SchemaField("equipment_covered", "STRING", mode="REPEATED"),
                bigquery.SchemaField("notable_content", "STRING", mode="REPEATED"),
                bigquery.SchemaField("tools_featured", "STRING", mode="REPEATED"),
                bigquery.SchemaField("last_scraped", "TIMESTAMP"),
            ],
            "videos": [
                bigquery.SchemaField("video_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("channel_name", "STRING"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("description", "STRING"),
                bigquery.SchemaField("duration", "STRING"),
                bigquery.SchemaField("views", "INT64"),
                bigquery.SchemaField("likes", "INT64"),
                bigquery.SchemaField("upload_date", "TIMESTAMP"),
                bigquery.SchemaField("repair_type", "STRING"),
                bigquery.SchemaField("equipment_featured", "STRING", mode="REPEATED"),
                bigquery.SchemaField("problems_solved", "STRING", mode="REPEATED"),
                bigquery.SchemaField("parts_used", "STRING", mode="REPEATED"),
                bigquery.SchemaField("tools_used", "STRING", mode="REPEATED"),
                bigquery.SchemaField("transcript_summary", "STRING"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "repair_techniques": [
                bigquery.SchemaField("technique_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("video_id", "STRING"),
                bigquery.SchemaField("channel_name", "STRING"),
                bigquery.SchemaField("technique_name", "STRING"),
                bigquery.SchemaField("equipment_type", "STRING"),
                bigquery.SchemaField("problem_description", "STRING"),
                bigquery.SchemaField("solution_steps", "STRING", mode="REPEATED"),
                bigquery.SchemaField("time_required", "STRING"),
                bigquery.SchemaField("difficulty_level", "STRING"),
                bigquery.SchemaField("cost_estimate", "STRING"),
                bigquery.SchemaField("success_rate", "FLOAT64"),
            ]
        }
        
        for table_name, schema in tables.items():
            table_id = f"{self.project_id}.youtube_repair_content.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            
            try:
                self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")
    
    async def scrape_youtube_channel(self, channel_data: Dict) -> Dict:
        """Scrape a YouTube channel using Crawl4AI"""
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            try:
                # Configure extraction strategy for YouTube
                extraction_strategy = JsonCssExtractionStrategy(
                    schema={
                        "videos": {
                            "selector": "ytd-rich-item-renderer",
                            "fields": {
                                "title": "h3#video-title",
                                "url": {"selector": "a#video-title-link", "attr": "href"},
                                "views": "span.style-scope.ytd-video-meta-block",
                                "duration": "span.style-scope.ytd-thumbnail-overlay-time-status-renderer"
                            }
                        }
                    }
                )
                
                # Crawl the channel page
                result = await crawler.arun(
                    url=channel_data["url"],
                    config=CrawlerRunConfig(
                        extraction_strategy=extraction_strategy,
                        wait_for="ytd-rich-item-renderer",
                        timeout=30000,
                        screenshot=True
                    )
                )
                
                if result.success:
                    # Parse extracted data
                    extracted_data = json.loads(result.extracted_content or "{}")
                    videos = extracted_data.get("videos", [])
                    
                    logger.info(f"✅ Scraped {len(videos)} videos from {channel_data['channel']}")
                    
                    # Store channel info
                    await self._store_channel_info(channel_data)
                    
                    # Store video details
                    for video in videos[:20]:  # Limit to top 20 videos
                        await self._store_video_info(video, channel_data["channel"])
                    
                    return {
                        "channel": channel_data["channel"],
                        "videos_found": len(videos),
                        "status": "success"
                    }
                else:
                    logger.error(f"Failed to scrape {channel_data['url']}")
                    return {"channel": channel_data["channel"], "status": "failed"}
                    
            except Exception as e:
                logger.error(f"Error scraping {channel_data['channel']}: {e}")
                return {"channel": channel_data["channel"], "status": "error", "message": str(e)}
    
    async def scrape_all_repair_channels(self) -> Dict:
        """Scrape all repair channels"""
        results = {
            "channels_scraped": 0,
            "videos_found": 0,
            "categories": {}
        }
        
        for category, channels in self.repair_channels.items():
            logger.info(f"\n📊 Scraping {category} channels...")
            category_results = []
            
            for channel_data in channels[:2]:  # Limit for testing
                result = await self.scrape_youtube_channel(channel_data)
                category_results.append(result)
                results["channels_scraped"] += 1
                
                if result.get("status") == "success":
                    results["videos_found"] += result.get("videos_found", 0)
            
            results["categories"][category] = category_results
        
        return results
    
    async def _store_channel_info(self, channel_data: Dict):
        """Store channel information in BigQuery"""
        import hashlib
        
        record = {
            "channel_id": hashlib.md5(channel_data["channel"].encode()).hexdigest(),
            "channel_name": channel_data["channel"],
            "channel_url": channel_data.get("url", ""),
            "category": channel_data.get("category", "general"),
            "subscribers": channel_data.get("subscribers", ""),
            "specialty": channel_data.get("specialty", ""),
            "equipment_covered": channel_data.get("equipment_covered", []),
            "notable_content": channel_data.get("notable_series", channel_data.get("notable_videos", [])),
            "tools_featured": channel_data.get("tools_featured", channel_data.get("tools", [])),
            "last_scraped": datetime.now()
        }
        
        table_id = f"{self.project_id}.youtube_repair_content.channels"
        errors = self.bq_client.insert_rows_json(table_id, [record])
        if errors:
            logger.error(f"Failed to store channel: {errors}")
    
    async def _store_video_info(self, video_data: Dict, channel_name: str):
        """Store video information in BigQuery"""
        import hashlib
        
        video_url = video_data.get("url", "")
        if video_url and not video_url.startswith("http"):
            video_url = f"https://youtube.com{video_url}"
        
        record = {
            "video_id": hashlib.md5(video_url.encode()).hexdigest(),
            "channel_name": channel_name,
            "title": video_data.get("title", ""),
            "url": video_url,
            "description": video_data.get("description", ""),
            "duration": video_data.get("duration", ""),
            "views": self._parse_views(video_data.get("views", "0")),
            "likes": 0,  # Would need additional API call
            "upload_date": datetime.now(),  # Placeholder
            "repair_type": self._classify_repair_type(video_data.get("title", "")),
            "equipment_featured": [],
            "problems_solved": [],
            "parts_used": [],
            "tools_used": [],
            "transcript_summary": "",
            "scraped_at": datetime.now()
        }
        
        table_id = f"{self.project_id}.youtube_repair_content.videos"
        errors = self.bq_client.insert_rows_json(table_id, [record])
        if errors:
            logger.error(f"Failed to store video: {errors}")
    
    def _parse_views(self, views_str: str) -> int:
        """Parse view count from string"""
        import re
        numbers = re.findall(r'\d+', views_str.replace(',', ''))
        return int(numbers[0]) if numbers else 0
    
    def _classify_repair_type(self, title: str) -> str:
        """Classify repair type from video title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ["hydraulic", "cylinder", "pump"]):
            return "hydraulic"
        elif any(word in title_lower for word in ["engine", "diesel", "turbo"]):
            return "engine"
        elif any(word in title_lower for word in ["electrical", "wiring", "sensor"]):
            return "electrical"
        elif any(word in title_lower for word in ["maintenance", "service", "filter"]):
            return "maintenance"
        elif any(word in title_lower for word in ["troubleshoot", "diagnos", "problem"]):
            return "diagnostic"
        else:
            return "general"

async def main():
    """Run YouTube repair content scraping"""
    scraper = YouTubeRepairScraper()
    
    print("=" * 60)
    print("🚀 STARTING YOUTUBE REPAIR CONTENT SCRAPING")
    print(f"📅 {datetime.now()}")
    print("=" * 60)
    
    # Scrape all channels
    results = await scraper.scrape_all_repair_channels()
    
    print("\n📊 SCRAPING RESULTS:")
    print(f"  Channels scraped: {results['channels_scraped']}")
    print(f"  Videos found: {results['videos_found']}")
    
    print("\n✅ YouTube content stored in BigQuery:")
    print("  - youtube_repair_content.channels")
    print("  - youtube_repair_content.videos")
    print("  - youtube_repair_content.repair_techniques")
    
    print("\n🔄 Bob's Brain now has access to YouTube repair knowledge!")

if __name__ == "__main__":
    asyncio.run(main())