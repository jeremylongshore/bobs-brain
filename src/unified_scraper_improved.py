#!/usr/bin/env python3
"""
Top Equipment Repair & Maintenance Sites Scraper
Targets the most popular public sites across all equipment types
"""

import asyncio
import hashlib
import logging
import os
from datetime import datetime
from typing import Dict, List

import feedparser
import requests
from bs4 import BeautifulSoup
from google.cloud import bigquery

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TopRepairSitesScraper:
    """Scraper for most popular repair/maintenance sites - all equipment types"""

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)

        # Reddit API (optional but recommended)
        self.reddit_client_id = os.environ.get("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
        self.reddit_token = None

        # TOP REPAIR & MAINTENANCE SITES (All Public, No Login Required)
        self.top_sites = {
            # REDDIT - Most Active Repair Communities
            "reddit_repair": [
                "https://www.reddit.com/r/MechanicAdvice/hot.json",  # 500k+ members
                "https://www.reddit.com/r/Justrolledintotheshop/hot.json",  # 2M+ members
                "https://www.reddit.com/r/diesel/hot.json",  # Diesel repairs
                "https://www.reddit.com/r/tractors/hot.json",  # Tractor maintenance
                "https://www.reddit.com/r/heavyequipment/hot.json",  # Heavy equipment
                "https://www.reddit.com/r/Bulldozers/hot.json",  # Bulldozer specific
                "https://www.reddit.com/r/Construction/hot.json",  # Construction equipment
                "https://www.reddit.com/r/farming/hot.json",  # Farm equipment
                "https://www.reddit.com/r/lawncare/hot.json",  # Small equipment
                "https://www.reddit.com/r/smallengines/hot.json",  # Small engine repair
            ],
            # YOUTUBE CHANNELS - Video Repair Guides (Channel IDs for reference)
            "youtube_repair": [
                {"name": "Messick's Equipment", "topics": "Tractor repair, maintenance"},
                {"name": "Diesel Creek", "topics": "Heavy equipment restoration"},
                {"name": "Andrew Camarata", "topics": "Equipment repair, excavators"},
                {"name": "Deboss Garage", "topics": "Diesel truck repairs"},
                {"name": "Vice Grip Garage", "topics": "Equipment revival"},
                {"name": "Mustie1", "topics": "Small engine, equipment repair"},
                {"name": "Taryl Fixes All", "topics": "Lawn equipment repair"},
                {"name": "Steve's Small Engine Saloon", "topics": "Small engine diagnostics"},
            ],
            # TOP MANUFACTURER RESOURCES (Public Pages)
            "manufacturer_resources": [
                {
                    "name": "John Deere MachineFinder Blog",
                    "url": "https://blog.machinefinder.com/",
                    "topics": "Maintenance tips, troubleshooting",
                },
                {
                    "name": "CAT Equipment Maintenance",
                    "url": "https://www.cat.com/en_US/support/maintenance.html",
                    "topics": "Maintenance schedules, tips",
                },
                {
                    "name": "Bobcat Advantage Blog",
                    "url": "https://www.bobcat.com/resources/blog",
                    "topics": "Equipment care, operation tips",
                },
                {
                    "name": "Kubota USA Blog",
                    "url": "https://www.kubotausa.com/blog",
                    "topics": "Tractor maintenance, tips",
                },
                {
                    "name": "Case Construction Blog",
                    "url": "https://blog.casece.com/",
                    "topics": "Construction equipment maintenance",
                },
            ],
            # INDUSTRY PUBLICATIONS (RSS Feeds)
            "industry_publications": [
                {
                    "name": "Equipment World",
                    "url": "https://www.equipmentworld.com/feed/",
                    "topics": "Equipment news, maintenance",
                },
                {
                    "name": "For Construction Pros",
                    "url": "https://www.forconstructionpros.com/rss/",
                    "topics": "Equipment maintenance, repairs",
                },
                {
                    "name": "Diesel Progress",
                    "url": "https://www.dieselprogress.com/rss/",
                    "topics": "Diesel engine maintenance",
                },
                {
                    "name": "Compact Equipment Magazine",
                    "url": "https://compactequip.com/feed/",
                    "topics": "Compact equipment maintenance",
                },
                {
                    "name": "Heavy Equipment Guide",
                    "url": "https://www.heavyequipmentguide.ca/rss",
                    "topics": "Heavy equipment repairs",
                },
            ],
            # REPAIR MANUALS & GUIDES (Public Access)
            "repair_guides": [
                {
                    "name": "iFixit Heavy Equipment",
                    "url": "https://www.ifixit.com/Device/Heavy_Equipment",
                    "topics": "Repair guides, troubleshooting",
                },
                {
                    "name": "WikiHow Equipment Repair",
                    "url": "https://www.wikihow.com/Category:Cars-%26-Other-Vehicles",
                    "topics": "DIY repair guides",
                },
            ],
            # FORUMS (Public Sections - No Login)
            "public_forums": [
                {
                    "name": "The Diesel Stop",
                    "url": "https://www.thedieselstop.com/forums/",
                    "topics": "Diesel engine troubleshooting",
                },
                {"name": "SmokStak", "url": "http://www.smokstak.com/forum/", "topics": "Antique equipment repair"},
            ],
        }

        self._ensure_tables()

    def _ensure_tables(self):
        """Create BigQuery tables for top sites data"""
        dataset_id = f"{self.project_id}.top_repair_sites"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info(f"✅ Dataset {dataset_id} ready")
        except:
            pass

        # Schema for repair content
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("url", "STRING"),
            bigquery.SchemaField("source_site", "STRING"),
            bigquery.SchemaField("equipment_type", "STRING"),
            bigquery.SchemaField("repair_type", "STRING"),
            bigquery.SchemaField("upvotes", "INT64"),
            bigquery.SchemaField("comments", "INT64"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{dataset_id}.repair_content"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
            logger.info(f"✅ Table {table_id} ready")
        except:
            pass

    def _get_reddit_token(self):
        """Get Reddit OAuth token if credentials available"""
        if not self.reddit_client_id:
            return None

        if not self.reddit_token:
            try:
                auth = (self.reddit_client_id, self.reddit_client_secret)
                data = {"grant_type": "client_credentials"}
                headers = {"User-Agent": "BobsBrain/1.0 Equipment Repair Knowledge"}

                response = requests.post(
                    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers, timeout=10
                )

                if response.status_code == 200:
                    self.reddit_token = response.json()["access_token"]
                    logger.info("✅ Reddit OAuth token obtained")
            except Exception as e:
                logger.warning(f"Reddit OAuth failed, using public API: {e}")

        return self.reddit_token

    async def scrape_reddit(self) -> List[Dict]:
        """Scrape Reddit repair communities"""
        all_items = []
        token = self._get_reddit_token()

        for url in self.top_sites["reddit_repair"]:
            try:
                # Extract subreddit name
                subreddit = url.split("/r/")[1].split("/")[0]

                if token:
                    # Use OAuth API (higher rate limits)
                    api_url = url.replace("www.reddit.com", "oauth.reddit.com")
                    headers = {"User-Agent": "BobsBrain/1.0", "Authorization": f"bearer {token}"}
                else:
                    # Use public API
                    api_url = url
                    headers = {"User-Agent": "BobsBrain/1.0"}

                response = requests.get(api_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    for child in data.get("data", {}).get("children", [])[:5]:
                        post = child["data"]

                        # Skip stickied/promoted posts
                        if post.get("stickied") or post.get("promoted"):
                            continue

                        # Look for repair/maintenance keywords
                        title = post.get("title", "").lower()
                        if any(
                            word in title
                            for word in [
                                "repair",
                                "fix",
                                "broke",
                                "maintenance",
                                "troubleshoot",
                                "problem",
                                "issue",
                                "help",
                                "diagnose",
                                "replace",
                                "rebuild",
                            ]
                        ):
                            item = {
                                "title": post.get("title", ""),
                                "content": post.get("selftext", "")[:3000],
                                "url": f"https://reddit.com{post.get('permalink', '')}",
                                "source": f"r/{subreddit}",
                                "upvotes": post.get("ups", 0),
                                "comments": post.get("num_comments", 0),
                                "equipment_type": self._detect_equipment_type(
                                    post.get("title", "") + " " + post.get("selftext", "")
                                ),
                            }
                            all_items.append(item)

                    logger.info(
                        f"✅ Scraped r/{subreddit}: {len([i for i in all_items if i['source'] == f'r/{subreddit}'])} repair posts"
                    )

            except Exception as e:
                logger.error(f"Reddit scrape error for {url}: {str(e)[:100]}")

        return all_items

    async def scrape_manufacturer_sites(self) -> List[Dict]:
        """Scrape manufacturer maintenance resources"""
        all_items = []

        for site in self.top_sites["manufacturer_resources"]:
            try:
                response = requests.get(site["url"], timeout=10)
                soup = BeautifulSoup(response.content, "html.parser")

                # Find article links
                article_links = []
                for link in soup.find_all("a", href=True):
                    href = link["href"]

                    # Look for maintenance/repair articles
                    if any(
                        word in href.lower()
                        for word in ["maintenance", "repair", "service", "troubleshoot", "tips", "guide"]
                    ):
                        if not href.startswith("http"):
                            from urllib.parse import urljoin

                            href = urljoin(site["url"], href)
                        article_links.append(href)

                # Scrape first 3 articles
                for article_url in article_links[:3]:
                    try:
                        article_resp = requests.get(article_url, timeout=5)
                        article_soup = BeautifulSoup(article_resp.content, "html.parser")

                        # Extract title
                        title = ""
                        if article_soup.find("h1"):
                            title = article_soup.find("h1").get_text(strip=True)

                        # Extract content
                        content = ""
                        article_body = article_soup.find("article") or article_soup.find("main")
                        if article_body:
                            content = article_body.get_text(strip=True)[:3000]

                        if title and content:
                            item = {
                                "title": title,
                                "content": content,
                                "url": article_url,
                                "source": site["name"],
                                "equipment_type": self._detect_equipment_type(title + " " + content),
                            }
                            all_items.append(item)

                    except Exception as e:
                        logger.error(f"Article scrape error: {str(e)[:50]}")

                logger.info(
                    f"✅ Scraped {site['name']}: {len([i for i in all_items if i['source'] == site['name']])} articles"
                )

            except Exception as e:
                logger.error(f"Site scrape error for {site['name']}: {str(e)[:100]}")

        return all_items

    async def scrape_rss_feeds(self) -> List[Dict]:
        """Scrape industry publication RSS feeds"""
        all_items = []

        for pub in self.top_sites["industry_publications"]:
            try:
                feed = feedparser.parse(pub["url"])

                for entry in feed.entries[:5]:
                    # Look for repair/maintenance content
                    title = entry.get("title", "").lower()
                    summary = entry.get("summary", "").lower()

                    if any(
                        word in title + summary
                        for word in ["maintenance", "repair", "service", "troubleshoot", "fix", "diagnos"]
                    ):
                        item = {
                            "title": entry.get("title", ""),
                            "content": entry.get("summary", "")[:3000],
                            "url": entry.get("link", ""),
                            "source": pub["name"],
                            "equipment_type": self._detect_equipment_type(
                                entry.get("title", "") + " " + entry.get("summary", "")
                            ),
                        }
                        all_items.append(item)

                logger.info(
                    f"✅ Scraped {pub['name']}: {len([i for i in all_items if i['source'] == pub['name']])} articles"
                )

            except Exception as e:
                logger.error(f"RSS error for {pub['name']}: {str(e)[:100]}")

        return all_items

    def _detect_equipment_type(self, text: str) -> str:
        """Detect equipment type from text"""
        text = text.lower()

        equipment_keywords = {
            "tractor": ["tractor", "john deere", "kubota", "massey"],
            "excavator": ["excavator", "digger", "cat ", "caterpillar"],
            "skid_steer": ["skid steer", "bobcat", "loader"],
            "truck": ["truck", "pickup", "diesel", "ford", "chevy", "ram"],
            "mower": ["mower", "lawn", "zero turn", "grass"],
            "dozer": ["dozer", "bulldozer", "crawler"],
            "backhoe": ["backhoe", "hoe", "case"],
            "forklift": ["forklift", "lift truck"],
            "generator": ["generator", "genset"],
            "compressor": ["compressor", "air compressor"],
        }

        for equipment, keywords in equipment_keywords.items():
            if any(keyword in text for keyword in keywords):
                return equipment

        return "general_equipment"

    def _store_item(self, item: Dict) -> bool:
        """Store item in BigQuery"""
        try:
            # Generate unique ID
            content_hash = hashlib.md5(f"{item.get('title', '')}{item.get('url', '')}".encode()).hexdigest()

            # Detect repair type
            repair_type = "general"
            content = (item.get("title", "") + " " + item.get("content", "")).lower()
            if "hydraulic" in content:
                repair_type = "hydraulic"
            elif "engine" in content or "motor" in content:
                repair_type = "engine"
            elif "electric" in content or "wiring" in content:
                repair_type = "electrical"
            elif "transmission" in content or "gear" in content:
                repair_type = "transmission"

            record = {
                "id": content_hash,
                "title": item.get("title", "")[:500],
                "content": item.get("content", "")[:5000],
                "url": item.get("url", "")[:500],
                "source_site": item.get("source", ""),
                "equipment_type": item.get("equipment_type", "general"),
                "repair_type": repair_type,
                "upvotes": item.get("upvotes", 0),
                "comments": item.get("comments", 0),
                "scraped_at": datetime.now(),
            }

            table_id = f"{self.project_id}.top_repair_sites.repair_content"
            errors = self.bq_client.insert_rows_json(table_id, [record])

            if errors:
                logger.error(f"BigQuery error: {errors}")
                return False

            return True

        except Exception as e:
            logger.error(f"Store error: {str(e)[:100]}")
            return False

    async def scrape_all(self) -> Dict:
        """Scrape all top repair sites"""
        results = {"total": 0, "stored": 0, "by_source": {}}

        logger.info("🚀 Starting top repair sites scraping...")

        # Scrape Reddit
        logger.info("📊 Scraping Reddit repair communities...")
        reddit_items = await self.scrape_reddit()
        results["total"] += len(reddit_items)
        results["by_source"]["reddit"] = len(reddit_items)
        for item in reddit_items:
            if self._store_item(item):
                results["stored"] += 1

        # Scrape manufacturer sites
        logger.info("📊 Scraping manufacturer resources...")
        manufacturer_items = await self.scrape_manufacturer_sites()
        results["total"] += len(manufacturer_items)
        results["by_source"]["manufacturers"] = len(manufacturer_items)
        for item in manufacturer_items:
            if self._store_item(item):
                results["stored"] += 1

        # Scrape RSS feeds
        logger.info("📊 Scraping industry publications...")
        rss_items = await self.scrape_rss_feeds()
        results["total"] += len(rss_items)
        results["by_source"]["publications"] = len(rss_items)
        for item in rss_items:
            if self._store_item(item):
                results["stored"] += 1

        logger.info(f"✅ Scraping complete: {results['stored']}/{results['total']} items stored")
        logger.info(f"📊 By source: {results['by_source']}")

        return results


async def main():
    """Test the scraper"""
    scraper = TopRepairSitesScraper()
    results = await scraper.scrape_all()
    print(f"\n✅ Final results: {results}")


if __name__ == "__main__":
    asyncio.run(main())
