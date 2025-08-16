#!/usr/bin/env python3
"""
Unified Public Scraper - No Login Required
Focuses on publicly accessible sources and can navigate beyond landing pages
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


class PublicUnifiedScraper:
    """Scraper for public sources only - no login required"""

    def __init__(self, project_id="bobs-house-ai"):
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)

        # Reddit API credentials from environment
        self.reddit_client_id = os.environ.get("REDDIT_CLIENT_ID", "")
        self.reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
        self.reddit_access_token = None

        # Public sources that don't require login
        self.public_sources = {
            "reddit": [
                {"url": "https://www.reddit.com/r/MechanicAdvice/hot.json", "type": "api"},
                {"url": "https://www.reddit.com/r/Diesel/hot.json", "type": "api"},
                {"url": "https://www.reddit.com/r/Justrolledintotheshop/hot.json", "type": "api"},
                {"url": "https://www.reddit.com/r/tractors/hot.json", "type": "api"},
                {"url": "https://www.reddit.com/r/heavyequipment/hot.json", "type": "api"},
            ],
            "rss": [
                {"url": "https://www.equipmentworld.com/feed/", "type": "rss"},
                {"url": "https://www.dieselprogress.com/rss/", "type": "rss"},
                {"url": "https://www.forconstructionpros.com/rss/", "type": "rss"},
            ],
            "manufacturer_blogs": [
                # These are public pages we can scrape
                {"url": "https://blog.machinefinder.com/", "type": "multi_page"},
                {"url": "https://www.deere.com/en/news/", "type": "multi_page"},
                {"url": "https://www.cat.com/en_US/news.html", "type": "multi_page"},
            ],
            "youtube_channels": [
                # Just channel IDs for reference - use YouTube API
                {"channel": "Messick's Equipment", "id": "UCDLymqv1LAcu8hpWlwvmFEQ"},
                {"channel": "Diesel Creek", "id": "UC2IEGI3uDNHjzT8GVfYDwfQ"},
            ],
        }

        self._ensure_tables()

    def _ensure_tables(self):
        """Create BigQuery tables if they don't exist"""
        dataset_id = f"{self.project_id}.public_scraping"
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
        except:
            pass

        # Schema for public content
        schema = [
            bigquery.SchemaField("id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("title", "STRING"),
            bigquery.SchemaField("content", "STRING"),
            bigquery.SchemaField("url", "STRING"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("source_type", "STRING"),
            bigquery.SchemaField("scraped_at", "TIMESTAMP"),
        ]

        table_id = f"{dataset_id}.public_content"
        table = bigquery.Table(table_id, schema=schema)

        try:
            self.bq_client.create_table(table, exists_ok=True)
        except:
            pass

    def _get_reddit_token(self):
        """Get Reddit OAuth token"""
        if not self.reddit_client_id or not self.reddit_client_secret:
            logger.warning("Reddit API credentials not configured")
            return None

        if not self.reddit_access_token:
            try:
                auth = (self.reddit_client_id, self.reddit_client_secret)
                data = {"grant_type": "client_credentials"}
                headers = {"User-Agent": "BobsBrain/1.0"}

                response = requests.post(
                    "https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers, timeout=10
                )

                if response.status_code == 200:
                    self.reddit_access_token = response.json()["access_token"]
                    logger.info("✅ Reddit OAuth token obtained")
                else:
                    logger.error(f"Reddit auth failed: {response.status_code}")
            except Exception as e:
                logger.error(f"Failed to get Reddit token: {e}")

        return self.reddit_access_token

    async def scrape_reddit(self) -> List[Dict]:
        """Scrape Reddit using API (no login required with API key)"""
        all_items = []

        for source in self.public_sources["reddit"]:
            try:
                # Try with OAuth first
                token = self._get_reddit_token()

                if token:
                    # Use OAuth API
                    oauth_url = source["url"].replace("www.reddit.com", "oauth.reddit.com")
                    headers = {"User-Agent": "BobsBrain/1.0", "Authorization": f"bearer {token}"}
                else:
                    # Use public API (rate limited but works)
                    headers = {"User-Agent": "BobsBrain/1.0"}
                    oauth_url = source["url"]

                response = requests.get(oauth_url, headers=headers, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    if "data" in data and "children" in data["data"]:
                        for child in data["data"]["children"][:10]:
                            post = child["data"]

                            # Skip stickied posts and ads
                            if post.get("stickied") or post.get("promoted"):
                                continue

                            item = {
                                "title": post.get("title", ""),
                                "content": post.get("selftext", "")[:2000],
                                "url": f"https://reddit.com{post.get('permalink', '')}",
                                "source": "reddit",
                                "upvotes": post.get("ups", 0),
                                "comments": post.get("num_comments", 0),
                            }
                            all_items.append(item)

                    logger.info(f"✅ Scraped {len(all_items)} items from Reddit")
                else:
                    logger.error(f"Reddit returned {response.status_code}")

            except Exception as e:
                logger.error(f"Reddit scrape error: {e}")

        return all_items

    async def scrape_multi_page(self, base_url: str) -> List[Dict]:
        """Scrape sites that require navigating beyond landing page"""
        items = []

        try:
            # Get the landing page
            response = requests.get(base_url, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")

            # Look for article/blog links
            article_links = []

            # Common patterns for article links
            for link in soup.find_all("a", href=True):
                href = link["href"]

                # Skip navigation/footer links
                if any(skip in href.lower() for skip in ["#", "javascript:", "mailto:", ".pdf"]):
                    continue

                # Look for article patterns
                if any(pattern in href for pattern in ["/news/", "/blog/", "/article/", "/posts/"]):
                    # Make absolute URL
                    if not href.startswith("http"):
                        from urllib.parse import urljoin

                        href = urljoin(base_url, href)
                    article_links.append(href)

            # Scrape first 5 articles
            for article_url in article_links[:5]:
                try:
                    article_response = requests.get(article_url, timeout=5)
                    article_soup = BeautifulSoup(article_response.content, "html.parser")

                    # Extract title
                    title = ""
                    if article_soup.find("h1"):
                        title = article_soup.find("h1").get_text(strip=True)
                    elif article_soup.find("title"):
                        title = article_soup.find("title").get_text(strip=True)

                    # Extract content (look for article body)
                    content = ""
                    for tag in ["article", "main", "div"]:
                        article_body = article_soup.find(
                            tag,
                            class_=lambda x: x
                            and any(word in str(x).lower() for word in ["content", "article", "body", "post"]),
                        )
                        if article_body:
                            content = article_body.get_text(strip=True)[:2000]
                            break

                    if title and content:
                        items.append({"title": title, "content": content, "url": article_url, "source": base_url})

                except Exception as e:
                    logger.error(f"Error scraping article {article_url}: {e}")

            logger.info(f"✅ Scraped {len(items)} articles from {base_url}")

        except Exception as e:
            logger.error(f"Multi-page scrape error for {base_url}: {e}")

        return items

    async def scrape_rss(self) -> List[Dict]:
        """Scrape RSS feeds (always public)"""
        all_items = []

        for source in self.public_sources["rss"]:
            try:
                feed = feedparser.parse(source["url"])

                for entry in feed.entries[:10]:
                    item = {
                        "title": entry.get("title", ""),
                        "content": entry.get("summary", "")[:2000],
                        "url": entry.get("link", ""),
                        "source": "rss",
                        "published": entry.get("published", ""),
                    }
                    all_items.append(item)

                logger.info(f"✅ Scraped {len(feed.entries[:10])} items from RSS")

            except Exception as e:
                logger.error(f"RSS scrape error: {e}")

        return all_items

    async def scrape_all(self) -> Dict:
        """Scrape all public sources"""
        results = {"total": 0, "stored": 0, "sources": []}

        logger.info("🚀 Starting public scraping...")

        # Scrape Reddit
        reddit_items = await self.scrape_reddit()
        results["total"] += len(reddit_items)
        for item in reddit_items:
            if self._store_item(item, "reddit"):
                results["stored"] += 1

        # Scrape RSS
        rss_items = await self.scrape_rss()
        results["total"] += len(rss_items)
        for item in rss_items:
            if self._store_item(item, "rss"):
                results["stored"] += 1

        # Scrape manufacturer blogs
        for source in self.public_sources["manufacturer_blogs"]:
            items = await self.scrape_multi_page(source["url"])
            results["total"] += len(items)
            for item in items:
                if self._store_item(item, "blog"):
                    results["stored"] += 1

        logger.info(f"✅ Public scraping complete: {results['stored']}/{results['total']} items stored")
        return results

    def _store_item(self, item: Dict, source_type: str) -> bool:
        """Store item in BigQuery"""
        try:
            # Generate unique ID
            content_hash = hashlib.md5(f"{item.get('title', '')}{item.get('url', '')}".encode()).hexdigest()

            record = {
                "id": content_hash,
                "title": item.get("title", "")[:500],
                "content": item.get("content", "")[:5000],
                "url": item.get("url", "")[:500],
                "source": item.get("source", "unknown"),
                "source_type": source_type,
                "scraped_at": datetime.now(),
            }

            table_id = f"{self.project_id}.public_scraping.public_content"
            errors = self.bq_client.insert_rows_json(table_id, [record])

            if errors:
                logger.error(f"BigQuery insert error: {errors}")
                return False

            return True

        except Exception as e:
            logger.error(f"Failed to store item: {e}")
            return False


async def main():
    """Test the public scraper"""
    scraper = PublicUnifiedScraper()
    results = await scraper.scrape_all()
    print(f"Scraped {results['total']} items, stored {results['stored']}")


if __name__ == "__main__":
    asyncio.run(main())
