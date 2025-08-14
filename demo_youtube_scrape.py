#!/usr/bin/env python3
"""
Demo YouTube scraper - shows it working with real videos
"""

from youtube_transcript_api import YouTubeTranscriptApi
import re
from datetime import datetime
from google.cloud import bigquery

def scrape_youtube_video(video_url):
    """Scrape a single YouTube video and extract knowledge"""
    
    # Extract video ID from URL
    video_id = video_url.split('v=')[-1].split('&')[0]
    
    print(f"\n🎥 Scraping video: {video_id}")
    print("=" * 60)
    
    try:
        # Get transcript using correct API method
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine transcript text
        full_text = ' '.join([t['text'] for t in transcript])
        
        print(f"✅ Transcript obtained: {len(full_text)} characters")
        print(f"📝 First 300 chars: {full_text[:300]}...")
        
        # Extract valuable information
        knowledge = extract_knowledge(full_text)
        
        print("\n🔍 EXTRACTED KNOWLEDGE:")
        print("-" * 40)
        
        if knowledge['error_codes']:
            print(f"⚠️  Error Codes Found: {', '.join(knowledge['error_codes'])}")
        
        if knowledge['part_numbers']:
            print(f"🔧 Part Numbers: {', '.join(knowledge['part_numbers'][:5])}")
        
        if knowledge['tools']:
            print(f"🛠️  Tools Mentioned: {', '.join(knowledge['tools'])}")
        
        if knowledge['problems']:
            print(f"❌ Problems Discussed: {', '.join(knowledge['problems'][:3])}")
        
        if knowledge['solutions']:
            print(f"✅ Solutions: {', '.join(knowledge['solutions'][:3])}")
        
        # Prepare for BigQuery storage
        record = {
            'video_id': video_id,
            'video_url': f"https://youtube.com/watch?v={video_id}",
            'transcript_length': len(full_text),
            'error_codes': knowledge['error_codes'],
            'part_numbers': knowledge['part_numbers'],
            'tools_mentioned': knowledge['tools'],
            'problems': knowledge['problems'],
            'solutions': knowledge['solutions'],
            'scraped_at': datetime.utcnow().isoformat()
        }
        
        print("\n💾 Ready to store in BigQuery:")
        print(f"   Table: youtube_equipment.transcripts")
        print(f"   Error codes: {len(knowledge['error_codes'])}")
        print(f"   Parts found: {len(knowledge['part_numbers'])}")
        
        return record
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def extract_knowledge(text):
    """Extract diagnostic knowledge from transcript"""
    
    knowledge = {
        'error_codes': [],
        'part_numbers': [],
        'tools': [],
        'problems': [],
        'solutions': []
    }
    
    # Extract error codes (P, B, C, U codes)
    code_patterns = [
        r'\bP[0-3][0-9]{3}\b',  # Powertrain codes
        r'\bB[0-9]{4}\b',        # Body codes
        r'\bC[0-9]{4}\b',        # Chassis codes
        r'\bU[0-9]{4}\b',        # Network codes
    ]
    
    for pattern in code_patterns:
        codes = re.findall(pattern, text.upper())
        knowledge['error_codes'].extend(codes)
    
    # Extract part numbers
    part_patterns = [
        r'\b[0-9]{5,}-[0-9]{2,}\b',     # 12345-67 format
        r'\b[A-Z]{2,3}[0-9]{4,6}\b',    # AB12345 format
        r'\b[0-9]{2,}[A-Z]{2}[0-9]{2,}\b', # 12AB34 format
    ]
    
    for pattern in part_patterns:
        parts = re.findall(pattern, text.upper())
        knowledge['part_numbers'].extend(parts)
    
    # Extract tools mentioned
    tool_keywords = [
        'multimeter', 'scan tool', 'scanner', 'oscilloscope', 'scope',
        'pressure gauge', 'test light', 'vacuum pump', 'compression tester',
        'fuel pressure gauge', 'amp clamp', 'torque wrench', 'impact',
        'jack', 'jack stands', 'diagnostic tool'
    ]
    
    text_lower = text.lower()
    for tool in tool_keywords:
        if tool in text_lower:
            knowledge['tools'].append(tool)
    
    # Extract problems
    problem_keywords = [
        'won\'t start', 'no start', 'hard start', 'rough idle', 'misfire',
        'overheating', 'no power', 'loss of power', 'won\'t move',
        'hydraulic leak', 'oil leak', 'coolant leak', 'fuel leak',
        'error code', 'warning light', 'check engine', 'limp mode',
        'black smoke', 'white smoke', 'blue smoke', 'knocking', 'grinding'
    ]
    
    for problem in problem_keywords:
        if problem in text_lower:
            knowledge['problems'].append(problem)
    
    # Extract solutions/fixes
    solution_patterns = [
        r'fixed it by[\w\s]+',
        r'solution was[\w\s]+',
        r'replaced the[\w\s]+',
        r'cleaning the[\w\s]+',
        r'adjusting the[\w\s]+',
    ]
    
    for pattern in solution_patterns:
        solutions = re.findall(pattern, text_lower)
        knowledge['solutions'].extend([s.strip() for s in solutions[:5]])
    
    # Remove duplicates
    knowledge['error_codes'] = list(set(knowledge['error_codes']))
    knowledge['part_numbers'] = list(set(knowledge['part_numbers']))
    knowledge['tools'] = list(set(knowledge['tools']))
    
    return knowledge

# Demo with real equipment repair videos
demo_videos = [
    {
        'url': 'https://www.youtube.com/watch?v=JGw5OEd5S-s',  # Bobcat hydraulic repair
        'title': 'Bobcat Hydraulic System Repair'
    },
    {
        'url': 'https://www.youtube.com/watch?v=FN2Ef0NnCdI',  # Diesel diagnostic
        'title': 'Diesel No Start Diagnosis'  
    }
]

print("🚀 YOUTUBE SCRAPER DEMO")
print("=" * 60)
print("Demonstrating transcript extraction and knowledge parsing")

# Try to scrape a video
for video in demo_videos:
    print(f"\n📺 Video: {video['title']}")
    result = scrape_youtube_video(video['url'])
    
    if result:
        print("\n✅ SUCCESS! Video knowledge extracted")
    else:
        print("\n⚠️  This video might not have transcripts available")

print("\n" + "=" * 60)
print("💡 WHAT THIS SCRAPER DOES:")
print("1. Extracts full transcript from YouTube videos")
print("2. Finds all diagnostic trouble codes (P0171, etc)")
print("3. Identifies part numbers mentioned")
print("4. Lists tools required for repairs")
print("5. Extracts problems and solutions")
print("6. Stores everything in BigQuery for Bob to learn from")
print("\n🎯 With your channels (Pine Hollow, Scanner Danner, etc)")
print("   we'll build a massive repair knowledge base!")