#!/usr/bin/env python3
"""
YouTube Equipment Knowledge Scraper
Uses open-source libraries to extract transcripts from equipment repair videos
Focuses on: Mini skid steers, diesel pickup trucks, compact construction equipment
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional

import yt_dlp
from google.cloud import bigquery
from neo4j import GraphDatabase

# Open-source YouTube libraries
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

logger = logging.getLogger(__name__)


class YouTubeEquipmentScraper:
    """
    Scrapes YouTube video transcripts for equipment repair knowledge
    Uses youtube-transcript-api for existing captions
    Falls back to yt-dlp + whisper for videos without captions
    """

    def __init__(self, project_id="bobs-house-ai", use_neo4j=False):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.use_neo4j = use_neo4j
        self.neo4j_driver = None

        if use_neo4j:
            self._init_neo4j()

        # Equipment-focused YouTube channels
        self.channels = {
            "mini_skid_steers": [
                {
                    "channel": "Ditch Witch",
                    "channel_id": "UC3D6IQ8HGJLVBegQSCEQNpA",
                    "focus": "mini skid steer maintenance",
                },
                {"channel": "Toro", "channel_id": "UCNyWeXg1n3NEFKBirNGZfDg", "focus": "compact utility loaders"},
                {"channel": "Vermeer", "channel_id": "UC5N2WYEQxmw8NGW-FNhG8IQ", "focus": "mini skid steer operation"},
                {
                    "channel": "Bobcat Company",
                    "channel_id": "UCZNk7Jjb2t8EuBsdsDRXJnA",
                    "focus": "MT series mini track loaders",
                },
            ],
            "diesel_trucks": [
                {
                    "channel": "PowerStrokeHelp",
                    "channel_id": "UCGgvVW0cqN_rW1-BU3FXvDA",
                    "focus": "Ford PowerStroke repairs",
                },
                {
                    "channel": "Diesel Tech Ron",
                    "channel_id": "UC7Px2cqDnkMrymoHj4Du7IA",
                    "focus": "Cummins diagnostics",
                },
                {"channel": "Deboss Garage", "channel_id": "UCPnvRLOYnmvDl8s1lJW0mBQ", "focus": "Duramax builds"},
                {"channel": "Truck Master", "channel_id": "UC24vYOO0gAGZUSqhaKpqqhw", "focus": "diesel maintenance"},
            ],
            "compact_equipment": [
                {"channel": "Messicks", "channel_id": "UCDLymqv1LAcu8hpWlwvmFEQ", "focus": "compact tractor repair"},
                {
                    "channel": "Good Works Tractors",
                    "channel_id": "UCjfONpK_pp-aJ6HBqJpI7Pw",
                    "focus": "subcompact maintenance",
                },
                {
                    "channel": "Neil Messick",
                    "channel_id": "UC_L4VnJJzEzgdLM9egFyBSQ",
                    "focus": "loader troubleshooting",
                },
                {
                    "channel": "Tractor Time with Tim",
                    "channel_id": "UC_L_qpyTaAGGlqBGf6qDsWQ",
                    "focus": "compact tractor tips",
                },
            ],
        }

        # Search queries for finding repair videos
        self.search_queries = [
            "mini skid steer troubleshooting",
            "Bobcat MT55 MT85 repair",
            "Ditch Witch SK repair manual",
            "diesel pickup truck common problems",
            "6.7 Powerstroke maintenance",
            "5.9 Cummins troubleshooting",
            "Duramax LML issues",
            "compact tractor hydraulic problems",
            "skid steer attachment repair",
            "mini excavator maintenance schedule",
            "DPF regeneration diesel truck",
            "DEF system problems solutions",
        ]

        self._ensure_tables()
        logger.info("🎥 YouTube Equipment Scraper initialized")

    def _init_neo4j(self):
        """Initialize Neo4j connection for graph storage"""
        try:
            uri = "bolt://10.128.0.2:7687"
            self.neo4j_driver = GraphDatabase.driver(uri, auth=("neo4j", "BobBrain2025"))
            logger.info("✅ Connected to Neo4j for graph storage")
        except Exception as e:
            logger.error(f"Neo4j connection failed: {e}")
            self.use_neo4j = False

    def _ensure_tables(self):
        """Create BigQuery tables for YouTube content"""
        dataset_id = f"{self.project_id}.youtube_equipment"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except:
            pass

        # Schema for YouTube transcripts
        schema = [
            bigquery.SchemaField("video_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("channel_name", "STRING"),
            bigquery.SchemaField("channel_id", "STRING"),
            bigquery.SchemaField("video_title", "STRING"),
            bigquery.SchemaField("video_url", "STRING"),
            bigquery.SchemaField("transcript", "STRING"),
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("topics", "STRING", mode="REPEATED"),
            bigquery.SchemaField("duration", "INT64"),
            bigquery.SchemaField("view_count", "INT64"),
            bigquery.SchemaField("published_date", "TIMESTAMP"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{dataset_id}.transcripts"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info("✅ YouTube transcript table ready")
        except:
            pass

    async def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Get transcript using youtube-transcript-api
        Falls back to yt-dlp for downloading if needed
        """
        try:
            # Try to get existing transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
            return transcript_text

        except Exception as e:
            logger.warning(f"No transcript available for {video_id}: {e}")

            # Fallback: Download with yt-dlp and transcribe with whisper
            # This would require whisper installation
            return await self._download_and_transcribe(video_id)

    async def _download_and_transcribe(self, video_id: str) -> Optional[str]:
        """
        Download audio with yt-dlp and transcribe with whisper
        Requires: pip install openai-whisper
        """
        try:
            # yt-dlp options for audio extraction
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"/tmp/{video_id}.%(ext)s",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "quiet": True,
                "no_warnings": True,
            }

            url = f"https://www.youtube.com/watch?v={video_id}"

            # Download audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            # Here you would use whisper to transcribe
            # import whisper
            # model = whisper.load_model("base")
            # result = model.transcribe(f"/tmp/{video_id}.mp3")
            # return result["text"]

            # For now, return None if no transcript available
            logger.info(f"Audio downloaded for {video_id}, whisper transcription needed")
            return None

        except Exception as e:
            logger.error(f"Failed to download/transcribe {video_id}: {e}")
            return None

    async def get_video_metadata(self, video_id: str) -> Dict:
        """Get video metadata using yt-dlp"""
        try:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": False,
            }

            url = f"https://www.youtube.com/watch?v={video_id}"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    "title": info.get("title", ""),
                    "channel": info.get("channel", ""),
                    "channel_id": info.get("channel_id", ""),
                    "duration": info.get("duration", 0),
                    "view_count": info.get("view_count", 0),
                    "upload_date": info.get("upload_date", ""),
                    "description": info.get("description", ""),
                }

        except Exception as e:
            logger.error(f"Failed to get metadata for {video_id}: {e}")
            return {}

    def extract_topics(self, text: str) -> List[str]:
        """Extract equipment repair topics from transcript"""
        topics = []

        # Common repair topics to look for
        topic_patterns = {
            "hydraulic": r"\b(hydraulic|cylinder|pump|valve|pressure)\b",
            "engine": r"\b(engine|diesel|turbo|injector|compression)\b",
            "electrical": r"\b(electrical|battery|alternator|starter|wiring)\b",
            "transmission": r"\b(transmission|gear|clutch|drive|axle)\b",
            "maintenance": r"\b(oil|filter|fluid|grease|service)\b",
            "troubleshooting": r"\b(problem|issue|fault|error|code)\b",
            "dpf_def": r"\b(dpf|def|regeneration|exhaust|emission)\b",
        }

        text_lower = text.lower()
        for topic, pattern in topic_patterns.items():
            if re.search(pattern, text_lower):
                topics.append(topic)

        return topics

    async def scrape_channel_videos(self, channel_id: str, max_videos: int = 10) -> List[Dict]:
        """Scrape recent videos from a channel"""
        videos = []

        try:
            ydl_opts = {
                "quiet": True,
                "extract_flat": True,
                "playlist_items": f"1-{max_videos}",
            }

            url = f"https://www.youtube.com/channel/{channel_id}/videos"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False)

                for entry in playlist_info.get("entries", [])[:max_videos]:
                    video_id = entry.get("id")
                    if video_id:
                        videos.append(video_id)

        except Exception as e:
            logger.error(f"Failed to get channel videos: {e}")

        return videos

    async def scrape_and_store(self, video_id: str, equipment_type: str = "general") -> bool:
        """Scrape a single video and store in BigQuery/Neo4j"""
        try:
            # Get transcript
            transcript = await self.get_video_transcript(video_id)
            if not transcript:
                logger.warning(f"No transcript for {video_id}")
                return False

            # Get metadata
            metadata = await self.get_video_metadata(video_id)

            # Extract topics
            topics = self.extract_topics(transcript)

            # Prepare record
            record = {
                "video_id": video_id,
                "channel_name": metadata.get("channel", ""),
                "channel_id": metadata.get("channel_id", ""),
                "video_title": metadata.get("title", ""),
                "video_url": f"https://www.youtube.com/watch?v={video_id}",
                "transcript": transcript[:10000],  # Limit transcript length
                "equipment_type": equipment_type,
                "topics": topics,
                "duration": metadata.get("duration", 0),
                "view_count": metadata.get("view_count", 0),
                "published_date": datetime.strptime(metadata.get("upload_date", "20230101"), "%Y%m%d")
                if metadata.get("upload_date")
                else None,
                "scraped_at": datetime.now(),
            }

            # Store in BigQuery
            table_id = f"{self.project_id}.youtube_equipment.transcripts"
            errors = self.bq_client.insert_rows_json(table_id, [record])

            if errors:
                logger.error(f"Failed to store in BigQuery: {errors}")
                return False

            # Store in Neo4j if enabled
            if self.use_neo4j and self.neo4j_driver:
                await self._store_in_neo4j(record)

            logger.info(f"✅ Stored transcript for: {metadata.get('title', video_id)}")
            return True

        except Exception as e:
            logger.error(f"Failed to scrape {video_id}: {e}")
            return False

    async def _store_in_neo4j(self, record: Dict):
        """Store video knowledge in Neo4j graph"""
        try:
            with self.neo4j_driver.session() as session:
                query = """
                MERGE (v:Video {video_id: $video_id})
                SET v.title = $title,
                    v.channel = $channel,
                    v.transcript = $transcript,
                    v.equipment_type = $equipment_type,
                    v.url = $url,
                    v.scraped_at = datetime($scraped_at)

                WITH v
                UNWIND $topics as topic
                MERGE (t:Topic {name: topic})
                MERGE (v)-[:COVERS]->(t)
                """

                session.run(
                    query,
                    video_id=record["video_id"],
                    title=record["video_title"],
                    channel=record["channel_name"],
                    transcript=record["transcript"][:1000],  # Store partial in graph
                    equipment_type=record["equipment_type"],
                    url=record["video_url"],
                    topics=record["topics"],
                    scraped_at=record["scraped_at"].isoformat(),
                )

                logger.info(f"✅ Stored in Neo4j graph: {record['video_title']}")

        except Exception as e:
            logger.error(f"Neo4j storage failed: {e}")

    async def scrape_all_channels(self, max_videos_per_channel: int = 5):
        """Scrape videos from all configured channels"""
        total_scraped = 0

        for equipment_type, channels in self.channels.items():
            logger.info(f"📊 Scraping {equipment_type} channels...")

            for channel_info in channels:
                channel_id = channel_info["channel_id"]
                channel_name = channel_info["channel"]

                logger.info(f"  Scraping {channel_name}...")

                # Get recent videos
                video_ids = await self.scrape_channel_videos(channel_id, max_videos_per_channel)

                # Scrape each video
                for video_id in video_ids:
                    success = await self.scrape_and_store(video_id, equipment_type)
                    if success:
                        total_scraped += 1

                    # Rate limiting
                    await asyncio.sleep(2)

        logger.info(f"✅ Total videos scraped: {total_scraped}")
        return total_scraped

    async def search_and_scrape(self, query: str, max_results: int = 10):
        """Search for videos by query and scrape them"""
        try:
            ydl_opts = {
                "quiet": True,
                "extract_flat": True,
                "default_search": "ytsearch",
                "playlist_items": f"1-{max_results}",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)

                scraped_count = 0
                for entry in search_results.get("entries", []):
                    video_id = entry.get("id")
                    if video_id:
                        # Determine equipment type from query
                        equipment_type = "general"
                        if "skid" in query.lower():
                            equipment_type = "mini_skid_steers"
                        elif "diesel" in query.lower() or "truck" in query.lower():
                            equipment_type = "diesel_trucks"
                        elif "tractor" in query.lower() or "compact" in query.lower():
                            equipment_type = "compact_equipment"

                        success = await self.scrape_and_store(video_id, equipment_type)
                        if success:
                            scraped_count += 1

                        await asyncio.sleep(2)  # Rate limiting

                logger.info(f"✅ Scraped {scraped_count} videos for query: {query}")
                return scraped_count

        except Exception as e:
            logger.error(f"Search failed for {query}: {e}")
            return 0


async def main():
    """Test the YouTube equipment scraper"""
    logging.basicConfig(level=logging.INFO)

    scraper = YouTubeEquipmentScraper(use_neo4j=False)  # Set to True if Neo4j is available

    print("=" * 60)
    print("🎥 YOUTUBE EQUIPMENT TRANSCRIPT SCRAPER")
    print(f"📅 {datetime.now()}")
    print("=" * 60)

    # Test with a specific search
    print("\n🔍 Searching for mini skid steer repair videos...")
    count = await scraper.search_and_scrape("mini skid steer hydraulic repair", max_results=3)

    print(f"\n✅ Scraped {count} videos")
    print("📊 Data stored in BigQuery: youtube_equipment.transcripts")

    # Uncomment to scrape all channels
    # total = await scraper.scrape_all_channels(max_videos_per_channel=2)
    # print(f"\n✅ Total videos from channels: {total}")


if __name__ == "__main__":
    asyncio.run(main())
