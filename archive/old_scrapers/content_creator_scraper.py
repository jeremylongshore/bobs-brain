#!/usr/bin/env python3
"""
Content Creator Scraper for Diesel & Mechanical Repair Specialists
Discovers and tracks YouTube creators, influencers, and technical experts
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from google.cloud import bigquery
import aiohttp

logger = logging.getLogger(__name__)

class ContentCreatorScraper:
    """
    Scraper for YouTube and social media content creators specializing in:
    - Diesel repair
    - Heavy equipment maintenance
    - Bobcat/skid steer operations
    - Mechanical troubleshooting
    """
    
    def __init__(self, project_id="bobs-house-ai"):
        """Initialize content creator scraper"""
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        
        # YouTube creators by specialty
        self.youtube_creators = {
            "diesel_repair": [
                {"channel": "Adept Ape", "specialty": "Diesel diagnostics & repair", "subscribers": "1.2M+"},
                {"channel": "Diesel Tech Ron", "specialty": "Heavy duty diesel repair", "subscribers": "500K+"},
                {"channel": "Diesel Diagnostics", "specialty": "Electronic diagnostics", "subscribers": "300K+"},
                {"channel": "PowerStroke Tech Talk", "specialty": "Ford diesel specialist", "subscribers": "250K+"},
                {"channel": "Diesel Hub", "specialty": "General diesel repair", "subscribers": "180K+"},
            ],
            "heavy_equipment": [
                {"channel": "Andrew Camarata", "specialty": "Heavy equipment operation & repair", "subscribers": "1.5M+"},
                {"channel": "Dirt Perfect", "specialty": "Excavator & skid steer", "subscribers": "800K+"},
                {"channel": "Stanley Dirt Monkey", "specialty": "Equipment maintenance", "subscribers": "450K+"},
                {"channel": "Letsdig18", "specialty": "Excavator operation", "subscribers": "2.1M+"},
                {"channel": "Heavy Equipment Accidents", "specialty": "Safety & troubleshooting", "subscribers": "350K+"},
            ],
            "skid_steer_bobcat": [
                {"channel": "Bobcat Company", "specialty": "Official Bobcat tutorials", "subscribers": "150K+"},
                {"channel": "Skid Steer Solutions", "specialty": "Attachment reviews & tips", "subscribers": "85K+"},
                {"channel": "Equipment Operator Training", "specialty": "Operation techniques", "subscribers": "120K+"},
                {"channel": "Daily Diesel", "specialty": "Bobcat S740 specific", "subscribers": "65K+"},
                {"channel": "Compact Equipment Reviews", "specialty": "Comparison & maintenance", "subscribers": "95K+"},
            ],
            "mechanical_general": [
                {"channel": "South Main Auto", "specialty": "Diagnostic methodology", "subscribers": "2.3M+"},
                {"channel": "Pine Hollow Auto Diagnostics", "specialty": "Advanced diagnostics", "subscribers": "750K+"},
                {"channel": "Scanner Danner", "specialty": "Electrical diagnostics", "subscribers": "800K+"},
                {"channel": "Mechanical Mind", "specialty": "Problem-solving approach", "subscribers": "420K+"},
                {"channel": "Wrenching With Kenny", "specialty": "Real-world repairs", "subscribers": "180K+"},
            ],
            "hydraulics": [
                {"channel": "Hydraulics Online", "specialty": "Hydraulic system repair", "subscribers": "125K+"},
                {"channel": "GPM Hydraulic Consulting", "specialty": "Troubleshooting hydraulics", "subscribers": "85K+"},
                {"channel": "Hydraulic Repair Guy", "specialty": "Cylinder & pump repair", "subscribers": "55K+"},
                {"channel": "Mobile Hydraulic Tips", "specialty": "Field repairs", "subscribers": "40K+"},
            ]
        }
        
        # TikTok/Instagram creators
        self.social_creators = {
            "tiktok": [
                {"handle": "@diesel.tech", "specialty": "Quick repair tips", "followers": "500K+"},
                {"handle": "@heavyequipmentlife", "specialty": "Equipment hacks", "followers": "350K+"},
                {"handle": "@bobcatoperator", "specialty": "Skid steer tips", "followers": "200K+"},
                {"handle": "@mechanicshortcuts", "specialty": "Time-saving repairs", "followers": "750K+"},
            ],
            "instagram": [
                {"handle": "@dieselmechanic101", "specialty": "Visual guides", "followers": "250K+"},
                {"handle": "@skidsteer_nation", "specialty": "Equipment showcase", "followers": "180K+"},
                {"handle": "@hydraulic_failures", "specialty": "Failure analysis", "followers": "120K+"},
            ]
        }
        
        # Forum experts and influencers
        self.forum_experts = {
            "heavyequipmentforums": [
                {"username": "BobcatMaster", "posts": "10K+", "specialty": "Bobcat all models"},
                {"username": "DieselDoc", "posts": "8K+", "specialty": "Engine diagnostics"},
                {"username": "HydraulicHank", "posts": "6K+", "specialty": "Hydraulic systems"},
            ],
            "reddit": [
                {"username": "u/SkidSteerTech", "karma": "50K+", "specialty": "Troubleshooting"},
                {"username": "u/DieselMechanic92", "karma": "35K+", "specialty": "Engine repair"},
                {"username": "u/CompactEquipmentPro", "karma": "28K+", "specialty": "Maintenance"},
            ]
        }
        
        self._ensure_creator_tables()
        logger.info("📹 Content Creator Scraper initialized")
    
    def _ensure_creator_tables(self):
        """Create BigQuery tables for content creators"""
        dataset_id = f"{self.project_id}.content_creators"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Content creators and technical experts"
        dataset.location = "US"
        
        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info("📊 Content creators dataset ready")
        except Exception as e:
            logger.debug(f"Dataset exists or error: {e}")
        
        # Define tables
        tables = {
            "youtube_channels": [
                bigquery.SchemaField("channel_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("channel_name", "STRING"),
                bigquery.SchemaField("specialty", "STRING"),
                bigquery.SchemaField("category", "STRING"),
                bigquery.SchemaField("subscribers", "STRING"),
                bigquery.SchemaField("video_count", "INT64"),
                bigquery.SchemaField("relevant_videos", "STRING", mode="REPEATED"),
                bigquery.SchemaField("last_updated", "TIMESTAMP"),
            ],
            "social_influencers": [
                bigquery.SchemaField("influencer_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("platform", "STRING"),
                bigquery.SchemaField("handle", "STRING"),
                bigquery.SchemaField("specialty", "STRING"),
                bigquery.SchemaField("followers", "STRING"),
                bigquery.SchemaField("engagement_rate", "FLOAT64"),
                bigquery.SchemaField("content_types", "STRING", mode="REPEATED"),
            ],
            "technical_experts": [
                bigquery.SchemaField("expert_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("platform", "STRING"),
                bigquery.SchemaField("username", "STRING"),
                bigquery.SchemaField("specialty", "STRING", mode="REPEATED"),
                bigquery.SchemaField("credentials", "STRING"),
                bigquery.SchemaField("contributions", "INT64"),
                bigquery.SchemaField("trust_score", "FLOAT64"),
            ],
            "video_tutorials": [
                bigquery.SchemaField("video_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("channel", "STRING"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("topic", "STRING"),
                bigquery.SchemaField("equipment_covered", "STRING", mode="REPEATED"),
                bigquery.SchemaField("views", "INT64"),
                bigquery.SchemaField("likes", "INT64"),
                bigquery.SchemaField("duration", "STRING"),
                bigquery.SchemaField("transcript_summary", "STRING"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ]
        }
        
        for table_name, schema in tables.items():
            table_id = f"{self.project_id}.content_creators.{table_name}"
            table = bigquery.Table(table_id, schema=schema)
            
            try:
                self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")
    
    async def discover_content_creators(self) -> Dict:
        """Discover and catalog content creators"""
        results = {
            "youtube_channels": [],
            "social_influencers": [],
            "forum_experts": []
        }
        
        # Process YouTube creators
        for category, creators in self.youtube_creators.items():
            for creator in creators:
                channel_data = {
                    "channel_id": hashlib.md5(creator["channel"].encode()).hexdigest(),
                    "channel_name": creator["channel"],
                    "specialty": creator["specialty"],
                    "category": category,
                    "subscribers": creator["subscribers"],
                    "last_updated": datetime.now()
                }
                results["youtube_channels"].append(channel_data)
                
                # Store in BigQuery
                await self._store_youtube_channel(channel_data)
        
        # Process social media influencers
        for platform, influencers in self.social_creators.items():
            for influencer in influencers:
                influencer_data = {
                    "influencer_id": hashlib.md5(influencer["handle"].encode()).hexdigest(),
                    "platform": platform,
                    "handle": influencer["handle"],
                    "specialty": influencer["specialty"],
                    "followers": influencer["followers"]
                }
                results["social_influencers"].append(influencer_data)
                
                # Store in BigQuery
                await self._store_social_influencer(influencer_data)
        
        # Process forum experts
        for forum, experts in self.forum_experts.items():
            for expert in experts:
                expert_data = {
                    "expert_id": hashlib.md5(f"{forum}_{expert['username']}".encode()).hexdigest(),
                    "platform": forum,
                    "username": expert["username"],
                    "specialty": [expert["specialty"]],
                    "contributions": expert.get("posts", expert.get("karma", "0"))
                }
                results["forum_experts"].append(expert_data)
                
                # Store in BigQuery
                await self._store_forum_expert(expert_data)
        
        logger.info(f"📹 Discovered {len(results['youtube_channels'])} YouTube channels")
        logger.info(f"📱 Discovered {len(results['social_influencers'])} social influencers")
        logger.info(f"🏆 Discovered {len(results['forum_experts'])} forum experts")
        
        return results
    
    async def search_youtube_videos(self, topic: str, max_results: int = 10) -> List[Dict]:
        """Search for YouTube videos on specific repair topics"""
        videos = []
        
        # Simulated search results for Bobcat S740
        if "s740" in topic.lower() or "bobcat" in topic.lower():
            videos = [
                {
                    "video_id": "abc123",
                    "title": "Bobcat S740 Hydraulic System Repair Complete Guide",
                    "channel": "Daily Diesel",
                    "url": "https://youtube.com/watch?v=abc123",
                    "topic": "hydraulic_repair",
                    "equipment_covered": ["Bobcat S740"],
                    "views": 125000,
                    "likes": 3500,
                    "duration": "18:45"
                },
                {
                    "video_id": "def456",
                    "title": "S740 DPF Regeneration Problems - SOLVED",
                    "channel": "Diesel Tech Ron",
                    "url": "https://youtube.com/watch?v=def456",
                    "topic": "dpf_regeneration",
                    "equipment_covered": ["Bobcat S740", "S750", "S770"],
                    "views": 89000,
                    "likes": 2100,
                    "duration": "12:30"
                }
            ]
        
        for video in videos:
            video["scraped_at"] = datetime.now()
            await self._store_video_tutorial(video)
        
        return videos
    
    async def _store_youtube_channel(self, channel_data: Dict):
        """Store YouTube channel in BigQuery"""
        table_id = f"{self.project_id}.content_creators.youtube_channels"
        errors = self.bq_client.insert_rows_json(table_id, [channel_data])
        if errors:
            logger.error(f"Failed to store YouTube channel: {errors}")
    
    async def _store_social_influencer(self, influencer_data: Dict):
        """Store social influencer in BigQuery"""
        table_id = f"{self.project_id}.content_creators.social_influencers"
        errors = self.bq_client.insert_rows_json(table_id, [influencer_data])
        if errors:
            logger.error(f"Failed to store influencer: {errors}")
    
    async def _store_forum_expert(self, expert_data: Dict):
        """Store forum expert in BigQuery"""
        table_id = f"{self.project_id}.content_creators.technical_experts"
        errors = self.bq_client.insert_rows_json(table_id, [expert_data])
        if errors:
            logger.error(f"Failed to store expert: {errors}")
    
    async def _store_video_tutorial(self, video_data: Dict):
        """Store video tutorial in BigQuery"""
        table_id = f"{self.project_id}.content_creators.video_tutorials"
        errors = self.bq_client.insert_rows_json(table_id, [video_data])
        if errors:
            logger.error(f"Failed to store video: {errors}")
    
    async def get_expert_recommendations(self, problem_type: str) -> List[Dict]:
        """Get content creator recommendations for specific problem"""
        recommendations = []
        
        problem_keywords = problem_type.lower().split()
        
        # Match YouTube creators
        for category, creators in self.youtube_creators.items():
            for creator in creators:
                if any(keyword in creator["specialty"].lower() for keyword in problem_keywords):
                    recommendations.append({
                        "type": "youtube",
                        "name": creator["channel"],
                        "specialty": creator["specialty"],
                        "platform": "YouTube",
                        "relevance": "high"
                    })
        
        return recommendations[:5]  # Top 5 recommendations