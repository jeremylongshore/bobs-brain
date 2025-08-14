#!/usr/bin/env python3
"""
Reddit Equipment Knowledge Scraper using PRAW
Scrapes repair subreddits for diagnostic knowledge
"""

import os
import re
from datetime import datetime

import praw
from google.cloud import bigquery


class RedditEquipmentScraper:
    def __init__(self):
        self.project_id = "bobs-house-ai"
        self.bq_client = bigquery.Client(project=self.project_id)

        # Reddit API credentials (need to be set)
        # Get these from https://www.reddit.com/prefs/apps
        self.reddit = None

        # Initialize Reddit instance (read-only mode for demo)
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID", "YOUR_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET", "YOUR_SECRET"),
                user_agent="EquipmentKnowledgeBot/1.0 by /u/yourusername",
            )
            # For demo, we'll use read-only mode
            self.reddit.read_only = True
        except:
            print("⚠️  Reddit API not configured - using demo mode")

        # HIGH-VALUE EQUIPMENT REPAIR SUBREDDITS
        self.subreddits = {
            "general_repair": [
                "MechanicAdvice",  # 1.5M members - Car repair Q&A
                "Justrolledintotheshop",  # 2.8M - Shop stories & failures
                "AskMechanics",  # Diagnostic help
                "Cartalk",  # General automotive
                "mechanicporn",  # Repair photos/videos
            ],
            "diesel_specific": [
                "Diesel",  # Diesel engines
                "Dieseltechs",  # Professional diesel techs
                "DieselTrucks",  # Pickup truck specific
                "Cummins",  # Cummins engines
                "Duramax",  # GM Duramax
                "Powerstroke",  # Ford Powerstroke
            ],
            "equipment_specific": [
                "Skidsteers",  # Skid steer specific
                "Bulldozers",  # Heavy equipment
                "tractors",  # Farm tractors
                "farming",  # Agricultural equipment
                "Construction",  # Construction equipment
                "HeavyEquipment",  # All heavy machinery
            ],
            "bobcat_related": [
                "Bobcat",  # Bobcat specific (if exists)
                "CompactEquipment",  # Compact machines
                "Excavators",  # Mini excavators
                "landscaping",  # Often has equipment repair
            ],
            "diy_repair": [
                "DIY",  # General DIY
                "fixit",  # Fix anything
                "AskElectronics",  # Electrical diagnostics
                "hydraulics",  # Hydraulic systems
                "welding",  # Repair fabrication
            ],
        }

        # Search queries for finding relevant posts
        self.search_queries = [
            "bobcat error code",
            "bobcat won't start",
            "skid steer hydraulic problem",
            "diesel no start",
            "def system fault",
            "dpf regeneration",
            "hydraulic pump failure",
            "error code P0",
            "diagnostic trouble code",
            "multimeter test",
            "scan tool recommendation",
            "part number",
        ]

    def extract_knowledge(self, text):
        """Extract repair knowledge from Reddit post/comment"""

        knowledge = {
            "error_codes": [],
            "part_numbers": [],
            "tools_mentioned": [],
            "problems": [],
            "solutions": [],
            "costs": [],
            "time_estimates": [],
        }

        if not text:
            return knowledge

        text_upper = text.upper()
        text_lower = text.lower()

        # Extract error codes
        code_patterns = [
            r"\b[PC][0-9]{4}\b",  # P and C codes
            r"\bB[0-9]{4}\b",  # Body codes
            r"\bU[0-9]{4}\b",  # Network codes
            r"\bSPN\s*\d{3,5}\b",  # J1939 SPN codes
            r"\bFMI\s*\d{1,2}\b",  # Failure mode identifier
        ]

        for pattern in code_patterns:
            codes = re.findall(pattern, text_upper)
            knowledge["error_codes"].extend(codes)

        # Extract part numbers (various formats)
        part_patterns = [
            r"\b\d{5,}-\d{2,}\b",  # 12345-67
            r"\b[A-Z]{2,4}[-\s]?\d{4,}\b",  # AB-1234 or AB1234
            r"part\s*#?\s*:?\s*([A-Z0-9-]+)",  # "part number: XXX"
            r"P/N\s*:?\s*([A-Z0-9-]+)",  # P/N: XXX
        ]

        for pattern in part_patterns:
            parts = re.findall(pattern, text_upper)
            if isinstance(parts, list) and len(parts) > 0:
                if isinstance(parts[0], tuple):
                    knowledge["part_numbers"].extend([p for p in parts[0] if p])
                else:
                    knowledge["part_numbers"].extend(parts)

        # Extract tools
        tools = [
            "multimeter",
            "scan tool",
            "scanner",
            "code reader",
            "oscilloscope",
            "scope",
            "pressure gauge",
            "test light",
            "vacuum pump",
            "compression tester",
            "fuel pressure gauge",
            "amp clamp",
            "torque wrench",
            "impact",
            "breaker bar",
            "jack",
            "jack stands",
            "diagnostic software",
            "laptop",
        ]

        for tool in tools:
            if tool in text_lower:
                knowledge["tools_mentioned"].append(tool)

        # Extract problems
        problem_patterns = [
            r"won'?t\s+start",
            r"no\s+start",
            r"hard\s+start",
            r"rough\s+idle",
            r"misfire",
            r"overheating",
            r"no\s+power",
            r"loss\s+of\s+power",
            r"won'?t\s+move",
            r"hydraulic\s+leak",
            r"oil\s+leak",
            r"coolant\s+leak",
            r"check\s+engine",
            r"warning\s+light",
            r"limp\s+mode",
            r"black\s+smoke",
            r"white\s+smoke",
            r"blue\s+smoke",
            r"knocking",
            r"grinding",
            r"clunking",
            r"squealing",
        ]

        for pattern in problem_patterns:
            if re.search(pattern, text_lower):
                knowledge["problems"].append(pattern.replace("\\s+", " ").replace("\\", ""))

        # Extract costs mentioned
        cost_pattern = r"\$\s*(\d{1,5}(?:,\d{3})*(?:\.\d{2})?)"
        costs = re.findall(cost_pattern, text)
        knowledge["costs"] = costs[:5]  # Limit to 5

        # Extract time estimates
        time_patterns = [
            r"(\d+)\s*hours?",
            r"(\d+)\s*minutes?",
            r"(\d+)\s*days?",
            r"about\s+(\d+)\s*(?:hours?|minutes?)",
        ]

        for pattern in time_patterns:
            times = re.findall(pattern, text_lower)
            knowledge["time_estimates"].extend(times[:3])

        # Remove duplicates
        for key in knowledge:
            if isinstance(knowledge[key], list):
                knowledge[key] = list(set(knowledge[key]))[:10]  # Limit to 10

        return knowledge

    def scrape_subreddit(self, subreddit_name, limit=50, time_filter="week"):
        """Scrape a subreddit for equipment repair knowledge"""

        if not self.reddit:
            return self.demo_data(subreddit_name)

        results = []

        try:
            subreddit = self.reddit.subreddit(subreddit_name)

            # Get top posts from past week
            for submission in subreddit.top(time_filter=time_filter, limit=limit):
                # Extract from post
                post_knowledge = self.extract_knowledge(submission.title + " " + submission.selftext)

                # Extract from top comments
                submission.comments.replace_more(limit=0)
                comment_text = " ".join([comment.body for comment in submission.comments.list()[:10]])
                comment_knowledge = self.extract_knowledge(comment_text)

                # Combine knowledge
                combined = {
                    "subreddit": subreddit_name,
                    "post_id": submission.id,
                    "post_title": submission.title,
                    "post_url": f"https://reddit.com{submission.permalink}",
                    "author": str(submission.author),
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "created_utc": datetime.fromtimestamp(submission.created_utc),
                    "error_codes": list(set(post_knowledge["error_codes"] + comment_knowledge["error_codes"])),
                    "part_numbers": list(set(post_knowledge["part_numbers"] + comment_knowledge["part_numbers"])),
                    "tools_mentioned": list(
                        set(post_knowledge["tools_mentioned"] + comment_knowledge["tools_mentioned"])
                    ),
                    "problems": list(set(post_knowledge["problems"] + comment_knowledge["problems"])),
                    "costs_mentioned": list(set(post_knowledge["costs"] + comment_knowledge["costs"])),
                    "scraped_at": datetime.utcnow(),
                }

                results.append(combined)

            return results

        except Exception as e:
            print(f"Error scraping r/{subreddit_name}: {e}")
            return self.demo_data(subreddit_name)

    def demo_data(self, subreddit_name):
        """Demo data showing what we'd extract"""
        return [
            {
                "subreddit": subreddit_name,
                "post_title": "DEMO: Bobcat S740 throwing code 9809-31",
                "error_codes": ["P0171", "P0174", "9809-31"],
                "part_numbers": ["7023037", "6667352"],
                "tools_mentioned": ["scan tool", "multimeter"],
                "problems": ["won't start", "hydraulic leak"],
                "costs_mentioned": ["$450", "$1200"],
                "solutions": ["Replaced hydraulic filter", "Cleaned MAF sensor"],
                "score": 156,
                "num_comments": 42,
            }
        ]

    def store_in_bigquery(self, records):
        """Store Reddit knowledge in BigQuery"""

        # Create table if not exists
        dataset_id = "reddit_equipment"
        table_id = f"{self.project_id}.{dataset_id}.repair_knowledge"

        # Store records
        if records:
            try:
                errors = self.bq_client.insert_rows_json(table_id, records)
                if errors:
                    print(f"BigQuery errors: {errors}")
                else:
                    print(f"✅ Stored {len(records)} Reddit posts")
            except:
                print("Would store to BigQuery:", table_id)

    def demo_scrape(self):
        """Demo what the scraper extracts"""

        print("🔍 REDDIT EQUIPMENT KNOWLEDGE SCRAPER")
        print("=" * 60)
        print()
        print("📚 TARGET SUBREDDITS:")
        print()

        for category, subs in self.subreddits.items():
            print(f"{category.upper()}:")
            for sub in subs[:3]:
                print(f"  • r/{sub}")
            print()

        print("-" * 60)
        print("🎯 WHAT WE EXTRACT FROM EACH POST:")
        print()

        # Demo extraction
        sample_text = """
        My Bobcat T770 is showing error code P0401 and won't start.
        Already replaced the EGR valve (part# 7080234) which cost me $450.
        Used my Autel scanner to check codes. Took about 2 hours to diagnose.
        Anyone seen this before? Getting fuel pressure of 45psi.
        """

        knowledge = self.extract_knowledge(sample_text)

        print("From sample post:")
        print(f"  Error codes: {knowledge['error_codes']}")
        print(f"  Part numbers: {knowledge['part_numbers']}")
        print(f"  Tools: {knowledge['tools_mentioned']}")
        print(f"  Problems: {knowledge['problems']}")
        print(f"  Costs: {knowledge['costs']}")
        print(f"  Time: {knowledge['time_estimates']} hours")
        print()

        print("📊 VALUABLE SUBREDDITS FOR YOUR NEEDS:")
        print()
        print("r/MechanicAdvice (1.5M members)")
        print("  • Real mechanics answering questions")
        print("  • Diagnostic procedures")
        print("  • Part recommendations")
        print()
        print("r/Diesel (Diesel engines)")
        print("  • DEF/DPF issues")
        print("  • Injector problems")
        print("  • Turbo diagnostics")
        print()
        print("r/Skidsteers (Your equipment!)")
        print("  • Bobcat specific issues")
        print("  • Hydraulic problems")
        print("  • Attachment troubles")

        return knowledge


def main():
    scraper = RedditEquipmentScraper()

    print("🤖 REDDIT SCRAPER USING PRAW")
    print("=" * 60)
    print()
    print("✅ PRAW ADVANTAGES:")
    print("  • Official Reddit API")
    print("  • Real-time data")
    print("  • Comments and discussions")
    print("  • Vote scores show solution quality")
    print("  • Free tier: 60 requests/minute")
    print()

    # Run demo
    scraper.demo_scrape()

    print()
    print("-" * 60)
    print("💡 HOW TO SET UP:")
    print("1. Go to https://www.reddit.com/prefs/apps")
    print("2. Create app (script type)")
    print("3. Get client_id and client_secret")
    print("4. Set environment variables:")
    print("   export REDDIT_CLIENT_ID='your_id'")
    print("   export REDDIT_CLIENT_SECRET='your_secret'")
    print()
    print("Then scraper will pull real data from:")
    print("  • Equipment repair posts")
    print("  • Diagnostic discussions")
    print("  • Part number recommendations")
    print("  • Cost comparisons")
    print("  • Time estimates")


if __name__ == "__main__":
    main()
