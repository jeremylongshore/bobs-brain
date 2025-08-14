#!/usr/bin/env python3
"""
Scrape YouTube channels for Jeremy's specific interests
Focuses on: Bobcat, Pine Hollow Auto Diagnostics, How I Did It
"""

import asyncio
import logging
from datetime import datetime
import requests
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomYouTubeScraper:
    def __init__(self):
        self.project_id = "bobs-house-ai"
        self.bq_client = bigquery.Client(project=self.project_id)
        
        # Jeremy's recommended channels
        self.priority_channels = {
            "diagnostic_experts": [
                {
                    "channel": "Pine Hollow Auto Diagnostics",
                    "channel_id": "UCn4Ifss-t3wMT6VBzQoKPUA",
                    "focus": "Scientific diagnostic approach, live troubleshooting",
                    "why_valuable": "244K subs, real-world diagnostics, methodical approach"
                },
                {
                    "channel": "South Main Auto Repair LLC", 
                    "channel_id": "UCJnJ5SqDUIJK8OGdeFhDL6g",
                    "focus": "Diagnostic case studies, electrical issues",
                    "why_valuable": "Eric O. is a diagnostic legend"
                },
                {
                    "channel": "Scanner Danner",
                    "channel_id": "UCtAixbt3jqKDfOTWU_qauXQ",  # Corrected channel ID
                    "focus": "Oscilloscope diagnostics, waveform analysis, case studies",
                    "why_valuable": "THE authority on scope diagnostics - must watch!"
                }
            ],
            "equipment_specific": [
                {
                    "channel": "Bobcat Company",
                    "channel_id": "UCZNk7Jjb2t8EuBsdsDRXJnA",
                    "focus": "Official Bobcat maintenance and troubleshooting",
                    "why_valuable": "Direct from manufacturer"
                },
                {
                    "channel": "FarmCraft101",
                    "channel_id": "UC3mERhm6W3WjEDy0JKZPMmA",
                    "focus": "Compact tractor repair, implements, maintenance",
                    "why_valuable": "Real farmer fixing real equipment - practical solutions"
                },
                {
                    "channel": "How I Did It",
                    "channel_id": "NEED_TO_FIND",  # We'll need to search for this
                    "focus": "DIY repairs and modifications",
                    "why_valuable": "Practical hands-on solutions"
                }
            ],
            "diesel_specialists": [
                {
                    "channel": "Diesel Tech Ron",
                    "channel_id": "UC7Px2cqDnkMrymoHj4Du7IA",
                    "focus": "Cummins and diesel diagnostics",
                    "why_valuable": "Deep diesel expertise"
                },
                {
                    "channel": "Adept Ape",
                    "channel_id": "UCW9omsDmmPYZR1yUcO0jC5Q",
                    "focus": "Heavy equipment and diesel repair",
                    "why_valuable": "No-nonsense repair approach"
                }
            ]
        }
        
        # High-value search queries based on your needs
        self.targeted_searches = [
            # Bobcat specific
            "Bobcat S740 hydraulic problems",
            "Bobcat T770 error codes",
            "Bobcat MT85 no start",
            "Bobcat warning lights meaning",
            "Bobcat def problems",
            "Bobcat hydraulic oil change",
            
            # Diagnostic procedures
            "no communication scan tool",
            "parasitic draw testing",
            "fuel pressure diagnostics",
            "oscilloscope automotive basics",
            "bidirectional control testing",
            
            # Common equipment issues
            "skid steer hydraulic troubleshooting",
            "diesel no start diagnosis",
            "dpf regeneration problems",
            "def quality issues",
            "hydraulic pump failure symptoms"
        ]
    
    def create_bigquery_table(self):
        """Create enhanced YouTube knowledge table"""
        dataset_id = "youtube_equipment"
        table_id = f"{self.project_id}.{dataset_id}.channel_knowledge"
        
        schema = [
            bigquery.SchemaField("video_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("channel_name", "STRING"),
            bigquery.SchemaField("channel_id", "STRING"),
            bigquery.SchemaField("video_title", "STRING"),
            bigquery.SchemaField("video_url", "STRING"),
            bigquery.SchemaField("transcript", "STRING"),
            bigquery.SchemaField("description", "STRING"),
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("problem_category", "STRING"),
            bigquery.SchemaField("diagnostic_steps", "STRING", mode="REPEATED"),
            bigquery.SchemaField("parts_mentioned", "STRING", mode="REPEATED"),
            bigquery.SchemaField("tools_required", "STRING", mode="REPEATED"),
            bigquery.SchemaField("error_codes", "STRING", mode="REPEATED"),
            bigquery.SchemaField("solution_found", "BOOLEAN"),
            bigquery.SchemaField("repair_time_minutes", "INTEGER"),
            bigquery.SchemaField("difficulty_level", "STRING"),
            bigquery.SchemaField("view_count", "INTEGER"),
            bigquery.SchemaField("like_count", "INTEGER"),
            bigquery.SchemaField("comment_count", "INTEGER"),
            bigquery.SchemaField("published_date", "TIMESTAMP"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            bigquery.SchemaField("ai_summary", "STRING"),
            bigquery.SchemaField("key_timestamps", "JSON"),
        ]
        
        table = bigquery.Table(table_id, schema=schema)
        table = self.bq_client.create_table(table, exists_ok=True)
        logger.info(f"Created/verified table {table_id}")
        return table
    
    async def scrape_channel_videos(self, channel_id: str, channel_name: str, max_videos: int = 20):
        """Scrape recent videos from a channel"""
        logger.info(f"Scraping {channel_name} - Channel ID: {channel_id}")
        
        # This would use YouTube API or scraping to get video IDs
        # For now, we'll use the search endpoint
        
        results = []
        # Simulate getting video IDs (in production, use YouTube API)
        video_ids = await self.get_channel_video_ids(channel_id, max_videos)
        
        for video_id in video_ids:
            try:
                # Get transcript using youtube-transcript-api
                transcript = await self.get_transcript(video_id)
                if transcript:
                    # Extract valuable information
                    knowledge = self.extract_knowledge(transcript)
                    
                    record = {
                        'video_id': video_id,
                        'channel_name': channel_name,
                        'channel_id': channel_id,
                        'video_url': f"https://youtube.com/watch?v={video_id}",
                        'transcript': transcript[:10000],  # Limit size
                        'diagnostic_steps': knowledge.get('steps', []),
                        'parts_mentioned': knowledge.get('parts', []),
                        'error_codes': knowledge.get('codes', []),
                        'scraped_at': datetime.utcnow().isoformat()
                    }
                    results.append(record)
                    
            except Exception as e:
                logger.error(f"Error scraping {video_id}: {e}")
                continue
        
        return results
    
    def extract_knowledge(self, transcript: str):
        """Extract diagnostic knowledge from transcript"""
        import re
        
        knowledge = {
            'steps': [],
            'parts': [],
            'codes': [],
            'tools': []
        }
        
        # Extract error codes (P0, P1, B, C, U codes)
        code_pattern = r'\b[PBCU]\d{4}\b'
        knowledge['codes'] = list(set(re.findall(code_pattern, transcript.upper())))
        
        # Extract part numbers (various formats)
        part_patterns = [
            r'\b\d{5,}-\d{2,}\b',  # 12345-67 format
            r'\b[A-Z]{2,4}\d{4,}\b',  # AB1234 format
            r'\b\d{2,}[A-Z]{2,}\d{2,}\b'  # 12AB34 format
        ]
        for pattern in part_patterns:
            knowledge['parts'].extend(re.findall(pattern, transcript.upper()))
        
        # Extract diagnostic steps (look for numbered steps or sequence words)
        step_indicators = ['first', 'second', 'next', 'then', 'after that', 'finally']
        lines = transcript.split('.')
        for line in lines:
            if any(indicator in line.lower() for indicator in step_indicators):
                knowledge['steps'].append(line.strip())
        
        # Extract tools mentioned
        tool_patterns = [
            'multimeter', 'scan tool', 'scanner', 'oscilloscope', 'pressure gauge',
            'test light', 'vacuum pump', 'compression tester', 'fuel pressure gauge'
        ]
        for tool in tool_patterns:
            if tool in transcript.lower():
                knowledge['tools'].append(tool)
        
        return knowledge
    
    async def get_channel_video_ids(self, channel_id: str, max_videos: int):
        """Get video IDs from channel (placeholder - needs YouTube API)"""
        # In production, this would use YouTube Data API
        # For now, return empty list
        logger.info(f"Would fetch {max_videos} videos from channel {channel_id}")
        return []
    
    async def get_transcript(self, video_id: str):
        """Get transcript for a video"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = ' '.join([t['text'] for t in transcript_list])
            return transcript
        except Exception as e:
            logger.error(f"Could not get transcript for {video_id}: {e}")
            return None
    
    async def scrape_priority_channels(self):
        """Scrape all priority channels"""
        self.create_bigquery_table()
        
        all_results = []
        
        # Scrape each channel category
        for category, channels in self.priority_channels.items():
            logger.info(f"\n📁 Scraping {category} channels...")
            
            for channel_info in channels:
                if channel_info['channel_id'] != "NEED_TO_FIND":
                    results = await self.scrape_channel_videos(
                        channel_info['channel_id'],
                        channel_info['channel'],
                        max_videos=10
                    )
                    all_results.extend(results)
                    logger.info(f"  ✅ {channel_info['channel']}: {len(results)} videos processed")
        
        # Store results in BigQuery
        if all_results:
            table_id = f"{self.project_id}.youtube_equipment.channel_knowledge"
            errors = self.bq_client.insert_rows_json(table_id, all_results)
            if errors:
                logger.error(f"BigQuery errors: {errors}")
            else:
                logger.info(f"\n🎉 Successfully stored {len(all_results)} videos in BigQuery")
        
        return all_results

async def main():
    """Run the scraper"""
    scraper = CustomYouTubeScraper()
    
    print("\n🎥 YOUTUBE CHANNEL SCRAPER FOR JEREMY")
    print("=" * 50)
    print("\nChannels to scrape:")
    print("✅ Pine Hollow Auto Diagnostics (244K subs)")
    print("✅ Bobcat Company (Official)")
    print("✅ South Main Auto (Eric O.)")
    print("✅ Scanner Danner (Advanced diagnostics)")
    print("✅ Diesel Tech Ron")
    print("\n⚠️  Note: 'How I Did It' needs channel ID")
    print("=" * 50)
    
    # Run the scraper
    results = await scraper.scrape_priority_channels()
    
    print(f"\n📊 Scraping complete!")
    print(f"Videos processed: {len(results)}")
    print(f"Location: bobs-house-ai.youtube_equipment.channel_knowledge")
    
    # Show sample queries
    print("\n🔍 Sample BigQuery queries to explore your data:")
    print("1. Find all Bobcat error codes:")
    print("   SELECT DISTINCT code FROM `bobs-house-ai.youtube_equipment.channel_knowledge`, UNNEST(error_codes) as code WHERE code LIKE 'P%'")
    print("\n2. Get Pine Hollow's most viewed videos:")
    print("   SELECT video_title, view_count FROM `bobs-house-ai.youtube_equipment.channel_knowledge` WHERE channel_name = 'Pine Hollow Auto Diagnostics' ORDER BY view_count DESC")

if __name__ == "__main__":
    asyncio.run(main())