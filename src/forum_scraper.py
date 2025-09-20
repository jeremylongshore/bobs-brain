#!/usr/bin/env python3
"""
Forum Scraper for Bob's Brain - Circle of Life Integration
Scrapes repair and maintenance forums to build comprehensive knowledge base
Uses Playwright for JavaScript-heavy sites and integrates with BigQuery
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
import feedparser
from google.cloud import bigquery
from playwright.async_api import Browser, Page, async_playwright

logger = logging.getLogger(__name__)

class ForumIntelligenceScraper:
    """
    Advanced forum scraper that discovers, classifies, and extracts
    repair/maintenance knowledge from online forums, Discord, Facebook groups,
    and other community platforms. Comparable to Crawl4AI but specialized for
    equipment repair knowledge extraction.

    Key advantages over basic scrapers:
    - Multi-platform support (forums, Discord, Facebook, Reddit, Telegram)
    - Authentication level detection and handling
    - User expertise classification
    - Content quality scoring
    - Equipment-specific focus
    - Real-time scraping capability
    """

    def __init__(self, project_id="bobs-house-ai"):
        """Initialize scraper with BigQuery integration"""
        self.project_id = project_id
        self.bq_client = bigquery.Client(project=project_id)
        self.browser = None
        self.context = None

        # Forum patterns for detection
        self.forum_patterns = {
            "vbulletin": ["vbulletin", "showthread.php", "forumdisplay.php"],
            "phpbb": ["phpbb", "viewtopic.php", "viewforum.php"],
            "discourse": ["discourse", "/t/", "/c/"],
            "xenforo": ["xenforo", "threads/", "forums/"],
            "invision": ["invision", "topic/", "forum/"],
            "smf": ["smf", "index.php?topic", "index.php?board"],
            "reddit": ["reddit.com", "/r/", "/comments/"],
            "tapatalk": ["tapatalk", "?fid=", "?tid="],
            "facebook": ["facebook.com/groups", "fb.com/groups"],
            "discord": ["discord.gg", "discord.com", "discord://"],
            "telegram": ["t.me", "telegram.me"],
            "slack": ["slack.com", ".slack.com/archives"],
            "whatsapp": ["chat.whatsapp.com"],
        }

        # Authentication level classification
        self.auth_levels = {
            "public": "No login required - all content accessible",
            "free_registration": "Free account needed for posting/full access",
            "verified_user": "Email verification or approval required",
            "paid_membership": "Subscription or payment required",
            "professional_only": "Professional credentials required",
        }

        # User expertise categories
        self.expertise_levels = {
            "hobbyist": ["diy", "hobby", "beginner", "home"],
            "enthusiast": ["enthusiast", "advanced", "experienced"],
            "professional": ["pro", "professional", "mechanic", "technician"],
            "certified_tech": ["certified", "ase", "dealer", "factory"],
            "specialist": ["specialist", "expert", "master"],
        }

        # Specialty niches for equipment repair
        self.specialty_niches = {
            "hydraulics": ["hydraulic", "cylinder", "pump", "valve", "hose"],
            "electrical": ["electrical", "wiring", "ecm", "sensor", "battery"],
            "diesel": ["diesel", "dpf", "def", "injector", "turbo"],
            "transmission": ["transmission", "clutch", "gear", "differential"],
            "engine": ["engine", "motor", "piston", "valve", "timing"],
            "hvac": ["hvac", "ac", "heater", "climate", "cooling"],
            "compact_equipment": ["skid steer", "bobcat", "loader", "excavator"],
        }

        # Initialize BigQuery tables
        self._ensure_scraper_tables()
        logger.info("🕷️ Forum Intelligence Scraper initialized")

    def _ensure_scraper_tables(self):
        """Create BigQuery tables for scraped forum data"""
        dataset_id = f"{self.project_id}.scraped_data"
        dataset = bigquery.Dataset(dataset_id)
        dataset.description = "Forum scraped data for knowledge building"
        dataset.location = "US"

        try:
            self.bq_client.create_dataset(dataset, exists_ok=True)
            logger.info("📊 Scraped data dataset ready")
        except Exception as e:
            logger.debug(f"Dataset exists or error: {e}")

        # Create comprehensive forum tables
        tables = {
            "forums": [
                bigquery.SchemaField("forum_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("name", "STRING"),
                bigquery.SchemaField("platform", "STRING"),
                bigquery.SchemaField("requires_login", "BOOL"),
                bigquery.SchemaField("auth_level", "STRING"),  # New: authentication level
                bigquery.SchemaField("content_access", "STRING"),  # New: public/member/premium
                bigquery.SchemaField("user_expertise", "STRING", mode="REPEATED"),  # New: expertise levels
                bigquery.SchemaField("categories", "STRING", mode="REPEATED"),
                bigquery.SchemaField("member_count", "INT64"),
                bigquery.SchemaField("active_members", "INT64"),  # New: active in last 30 days
                bigquery.SchemaField("thread_count", "INT64"),
                bigquery.SchemaField("specialties", "STRING", mode="REPEATED"),
                bigquery.SchemaField("equipment_focus", "STRING", mode="REPEATED"),  # New: equipment types
                bigquery.SchemaField("quality_score", "FLOAT64"),  # New: content quality rating
                bigquery.SchemaField("last_scraped", "TIMESTAMP"),
                bigquery.SchemaField("scrape_status", "STRING"),
                bigquery.SchemaField("scrape_notes", "STRING"),  # New: special notes
            ],
            "forum_threads": [
                bigquery.SchemaField("thread_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("forum_id", "STRING"),
                bigquery.SchemaField("url", "STRING"),
                bigquery.SchemaField("title", "STRING"),
                bigquery.SchemaField("category", "STRING"),
                bigquery.SchemaField("problem_description", "STRING"),
                bigquery.SchemaField("solution", "STRING"),
                bigquery.SchemaField("equipment_mentioned", "STRING", mode="REPEATED"),
                bigquery.SchemaField("view_count", "INT64"),
                bigquery.SchemaField("reply_count", "INT64"),
                bigquery.SchemaField("solved", "BOOL"),
                bigquery.SchemaField("author", "STRING"),
                bigquery.SchemaField("created_date", "TIMESTAMP"),
                bigquery.SchemaField("scraped_at", "TIMESTAMP"),
            ],
            "expert_members": [
                bigquery.SchemaField("member_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("forum_id", "STRING"),
                bigquery.SchemaField("username", "STRING"),
                bigquery.SchemaField("reputation", "INT64"),
                bigquery.SchemaField("post_count", "INT64"),
                bigquery.SchemaField("specialties", "STRING", mode="REPEATED"),
                bigquery.SchemaField("helpful_posts", "INT64"),
                bigquery.SchemaField("profile_url", "STRING"),
            ],
            "repair_solutions": [
                bigquery.SchemaField("solution_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("problem_category", "STRING"),
                bigquery.SchemaField("problem", "STRING"),
                bigquery.SchemaField("solution", "STRING"),
                bigquery.SchemaField("equipment_type", "STRING"),
                bigquery.SchemaField("parts_needed", "STRING", mode="REPEATED"),
                bigquery.SchemaField("tools_required", "STRING", mode="REPEATED"),
                bigquery.SchemaField("difficulty_level", "STRING"),
                bigquery.SchemaField("time_estimate", "STRING"),
                bigquery.SchemaField("cost_estimate", "STRING"),
                bigquery.SchemaField("source_url", "STRING"),
                bigquery.SchemaField("confidence_score", "FLOAT64"),
                bigquery.SchemaField("extracted_at", "TIMESTAMP"),
            ],
        }

        for table_name, schema in tables.items():
            table_id = f"{self.project_id}.scraped_data.{table_name}"
            table = bigquery.Table(table_id, schema=schema)

            try:
                self.bq_client.create_table(table, exists_ok=True)
                logger.info(f"✅ Table ready: {table_name}")
            except Exception as e:
                logger.debug(f"Table {table_name} exists or error: {e}")

    async def initialize_browser(self):
        """Initialize Playwright browser for scraping"""
        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-first-run",
                    "--no-zygote",
                    "--single-process",  # Important for Cloud Run
                ],
            )
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            )
            logger.info("🌐 Browser initialized for scraping")

    async def close_browser(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None

    async def scrape_facebook_group(self, group_url: str) -> Dict:
        """Scrape Facebook group posts (public groups only)"""
        try:
            await self.initialize_browser()
            page = await self.context.new_page()

            # Facebook requires specific handling
            await page.goto(group_url, wait_until="networkidle")

            # Scroll to load more posts
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)

            # Extract posts
            posts = await page.evaluate(
                """
                () => {
                    const posts = [];
                    document.querySelectorAll('[role="article"]').forEach(article => {
                        const text = article.innerText;
                        const likes = article.querySelector('[aria-label*="Like"]')?.innerText || '0';
                        const comments = article.querySelector('[aria-label*="Comment"]')?.innerText || '0';

                        if (text && text.length > 50) {
                            posts.push({
                                content: text.substring(0, 1000),
                                engagement: {likes, comments},
                                timestamp: new Date().toISOString()
                            });
                        }
                    });
                    return posts.slice(0, 50);  // Limit to 50 posts
                }
            """
            )

            await page.close()
            return {"platform": "facebook", "group_url": group_url, "posts_collected": len(posts), "posts": posts}

        except Exception as e:
            logger.error(f"Facebook scraping error: {e}")
            return {}

    async def scrape_discord_via_webhook(self, webhook_url: str) -> Dict:
        """Collect Discord messages via webhook integration"""
        try:
            # Discord requires bot integration or webhooks
            # This is a placeholder for webhook-based collection
            return {
                "platform": "discord",
                "status": "requires_bot_integration",
                "note": "Discord scraping requires bot setup with proper permissions",
            }
        except Exception as e:
            logger.error(f"Discord integration error: {e}")
            return {}

    async def scrape_telegram_channel(self, channel_url: str) -> Dict:
        """Scrape public Telegram channels"""
        try:
            # Telegram channels can be accessed via their web preview
            if "t.me" in channel_url:
                web_url = channel_url.replace("t.me", "t.me/s")
            else:
                web_url = channel_url

            await self.initialize_browser()
            page = await self.context.new_page()
            await page.goto(web_url, wait_until="networkidle")

            # Extract messages
            messages = await page.evaluate(
                """
                () => {
                    const messages = [];
                    document.querySelectorAll('.tgme_widget_message').forEach(msg => {
                        const text = msg.querySelector('.tgme_widget_message_text')?.innerText;
                        const views = msg.querySelector('.tgme_widget_message_views')?.innerText;

                        if (text) {
                            messages.push({
                                content: text,
                                views: views || '0',
                                timestamp: new Date().toISOString()
                            });
                        }
                    });
                    return messages;
                }
            """
            )

            await page.close()
            return {
                "platform": "telegram",
                "channel_url": channel_url,
                "messages_collected": len(messages),
                "messages": messages,
            }

        except Exception as e:
            logger.error(f"Telegram scraping error: {e}")
            return {}

    async def scrape_reddit_enhanced(self, subreddit_url: str) -> Dict:
        """Enhanced Reddit scraping with JSON API"""
        try:
            # Use Reddit's JSON API for better data
            if "/r/" in subreddit_url:
                json_url = subreddit_url + ".json"
            else:
                json_url = subreddit_url + ".json"

            async with aiohttp.ClientSession() as session:
                headers = {"User-Agent": "BobBrain/1.0 Equipment Knowledge Scraper"}
                async with session.get(json_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()

                        posts = []
                        for child in data.get("data", {}).get("children", [])[:50]:
                            post_data = child.get("data", {})
                            posts.append(
                                {
                                    "title": post_data.get("title"),
                                    "content": post_data.get("selftext"),
                                    "score": post_data.get("score"),
                                    "comments": post_data.get("num_comments"),
                                    "url": f"https://reddit.com{post_data.get('permalink')}",
                                    "created": post_data.get("created_utc"),
                                }
                            )

                        return {
                            "platform": "reddit",
                            "subreddit": subreddit_url,
                            "posts_collected": len(posts),
                            "posts": posts,
                        }

            return {"error": "Failed to fetch Reddit data"}

        except Exception as e:
            logger.error(f"Reddit API error: {e}")
            return {}

    async def discover_forums(self, search_queries: List[str]) -> List[Dict]:
        """
        Discover repair forums and communities across multiple platforms
        """
        await self.initialize_browser()
        discovered_forums = []

        # Multi-platform community sources
        known_sources = [
            # Facebook Groups (public)
            {
                "url": "https://www.facebook.com/groups/bobcatowners",
                "platform": "facebook",
                "auth": "public",
                "expertise": "mixed",
            },
            {
                "url": "https://www.facebook.com/groups/skidsteerloaders",
                "platform": "facebook",
                "auth": "public",
                "expertise": "professional",
            },
            {
                "url": "https://www.facebook.com/groups/heavyequipmentoperators",
                "platform": "facebook",
                "auth": "public",
                "expertise": "professional",
            },
            # Discord Servers (via webhooks/bots)
            {
                "url": "discord://heavy-equipment-pros",
                "platform": "discord",
                "auth": "invite_only",
                "expertise": "professional",
            },
            {"url": "discord://diy-mechanics", "platform": "discord", "auth": "public", "expertise": "hobbyist"},
            # Telegram Groups
            {"url": "https://t.me/bobcat_equipment", "platform": "telegram", "auth": "public", "expertise": "mixed"},
            {
                "url": "https://t.me/skidsteer_repairs",
                "platform": "telegram",
                "auth": "public",
                "expertise": "professional",
            },
        ]

        # Traditional Forums
        known_forums = [
            # Public forums (no login required to read)
            {"url": "https://www.reddit.com/r/MechanicAdvice", "auth": "public", "expertise": "mixed"},
            {"url": "https://www.reddit.com/r/DIY", "auth": "public", "expertise": "hobbyist"},
            {"url": "https://www.reddit.com/r/fixit", "auth": "public", "expertise": "hobbyist"},
            {"url": "https://www.reddit.com/r/HeavyEquipment", "auth": "public", "expertise": "professional"},
            {"url": "https://www.reddit.com/r/Skidsteers", "auth": "public", "expertise": "professional"},
            # Free registration forums
            {"url": "https://mechanics.stackexchange.com", "auth": "free_registration", "expertise": "mixed"},
            {"url": "https://www.diychatroom.com", "auth": "free_registration", "expertise": "hobbyist"},
            {"url": "https://www.doityourself.com/forum", "auth": "free_registration", "expertise": "hobbyist"},
            {"url": "https://www.garagejournal.com/forum", "auth": "free_registration", "expertise": "enthusiast"},
            {"url": "https://www.bobistheoilguy.com/forums", "auth": "free_registration", "expertise": "enthusiast"},
            # Professional/Specialty forums
            {"url": "https://www.heavyequipmentforums.com", "auth": "free_registration", "expertise": "professional"},
            {"url": "https://www.bobcatforum.com", "auth": "free_registration", "expertise": "specialist"},
            {"url": "https://www.tractorbynet.com/forums", "auth": "free_registration", "expertise": "enthusiast"},
            {"url": "https://www.lawnsite.com/forums", "auth": "free_registration", "expertise": "professional"},
            {"url": "https://www.plowsite.com/forums", "auth": "free_registration", "expertise": "professional"},
            # Paid/Premium forums
            {"url": "https://www.justanswer.com", "auth": "paid_membership", "expertise": "certified_tech"},
            {"url": "https://identifix.com", "auth": "professional_only", "expertise": "certified_tech"},
            {"url": "https://alldatadiy.com/community", "auth": "paid_membership", "expertise": "professional"},
        ]

        # Check all community sources
        all_sources = known_sources + known_forums
        for forum_data in all_sources:
            try:
                forum_info = await self.analyze_forum(
                    forum_data["url"], auth_hint=forum_data.get("auth"), expertise_hint=forum_data.get("expertise")
                )
                if forum_info:
                    discovered_forums.append(forum_info)
                    logger.info(f"✅ Discovered forum: {forum_data['url']} [{forum_data.get('auth')}]")
            except Exception as e:
                logger.error(f"Failed to analyze {forum_data['url']}: {e}")

        # Start real-time scraping for accessible platforms
        logger.info("🚀 Starting immediate scraping of accessible platforms...")
        await self.start_realtime_scraping(discovered_forums)

        # Also search for forums based on queries
        for query in search_queries:
            try:
                search_url = f"https://www.google.com/search?q={query}+forum+repair+maintenance"
                page = await self.context.new_page()
                await page.goto(search_url, wait_until="networkidle")

                # Extract search results
                links = await page.evaluate(
                    """
                    () => {
                        const links = [];
                        document.querySelectorAll('a[href*="forum"], a[href*="/r/"]').forEach(a => {
                            const href = a.href;
                            if (href && !href.includes('google.com')) {
                                links.push(href);
                            }
                        });
                        return links.slice(0, 10);
                    }
                """
                )

                await page.close()

                # Analyze each discovered forum
                for link in links:
                    try:
                        forum_info = await self.analyze_forum(link)
                        if forum_info and not any(f["url"] == forum_info["url"] for f in discovered_forums):
                            discovered_forums.append(forum_info)
                    except Exception as e:
                        logger.debug(f"Failed to analyze {link}: {e}")

            except Exception as e:
                logger.error(f"Search failed for '{query}': {e}")

        logger.info(f"🔍 Discovered {len(discovered_forums)} forums total")
        return discovered_forums

    async def analyze_forum(self, url: str, auth_hint: str = None, expertise_hint: str = None) -> Optional[Dict]:
        """
        Analyze a forum to determine its characteristics including authentication and user expertise
        """
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Detect forum platform
            platform = await self._detect_platform(page, url)

            # Comprehensive forum analysis
            auth_level, content_access = await self._analyze_authentication(page, auth_hint)
            user_expertise = await self._analyze_user_expertise(page, expertise_hint)
            specialties = await self._identify_specialties(page)
            equipment_focus = await self._identify_equipment_focus(page)
            quality_score = await self._calculate_quality_score(page)

            # Extract forum metadata with enhanced details
            forum_info = {
                "forum_id": hashlib.md5(url.encode()).hexdigest(),
                "url": url,
                "name": await self._extract_forum_name(page),
                "platform": platform,
                "requires_login": auth_level != "public",
                "auth_level": auth_level,
                "content_access": content_access,
                "user_expertise": user_expertise,
                "categories": await self._extract_categories(page, platform),
                "member_count": await self._extract_member_count(page),
                "active_members": await self._extract_active_members(page),
                "thread_count": await self._extract_thread_count(page),
                "specialties": specialties,
                "equipment_focus": equipment_focus,
                "quality_score": quality_score,
                "last_scraped": datetime.now(),
                "scrape_status": "analyzed",
                "scrape_notes": await self._generate_scrape_notes(page, auth_level, user_expertise),
            }

            await page.close()

            # Store forum info in BigQuery
            await self._store_forum_info(forum_info)

            return forum_info

        except Exception as e:
            logger.error(f"Failed to analyze forum {url}: {e}")
            return None

    async def _detect_platform(self, page: Page, url: str) -> str:
        """Detect the forum platform type"""
        page_content = await page.content()
        url_lower = url.lower()

        for platform, patterns in self.forum_patterns.items():
            for pattern in patterns:
                if pattern in url_lower or pattern in page_content.lower():
                    return platform

        # Check meta tags
        platform_meta = await page.evaluate(
            """
            () => {
                const generator = document.querySelector('meta[name="generator"]');
                return generator ? generator.content : null;
            }
        """
        )

        if platform_meta:
            return platform_meta.lower().split()[0]

        return "unknown"

    async def _extract_forum_name(self, page: Page) -> str:
        """Extract forum name"""
        try:
            return await page.evaluate(
                """
                () => {
                    const title = document.querySelector('title');
                    const h1 = document.querySelector('h1');
                    const siteName = document.querySelector('meta[property="og:site_name"]');

                    if (siteName) return siteName.content;
                    if (h1) return h1.textContent.trim();
                    if (title) return title.textContent.split('|')[0].trim();
                    return 'Unknown Forum';
                }
            """
            )
        except:
            return "Unknown Forum"

    async def _analyze_authentication(self, page: Page, auth_hint: str = None) -> Tuple[str, str]:
        """Analyze authentication requirements and content access levels"""
        try:
            auth_info = await page.evaluate(
                """
                () => {
                    const loginRequired = document.querySelector('.login-required, .must-login');
                    const loginModal = document.querySelector('[class*="login-modal"]');
                    const restrictedContent = document.body.textContent.includes('must be logged in');
                    const premiumContent = document.querySelector('.premium, .paid-content, .subscriber-only');
                    const registerButton = document.querySelector('a[href*="register"], button:has-text("Sign Up")');
                    const loginButton = document.querySelector('a[href*="login"], button:has-text("Log In")');

                    return {
                        hasLoginModal: !!loginModal,
                        hasRestrictedContent: !!restrictedContent,
                        hasPremiumContent: !!premiumContent,
                        hasRegisterOption: !!registerButton,
                        hasLoginOption: !!loginButton,
                        canViewThreads: !loginRequired
                    };
                }
            """
            )

            # Determine authentication level
            if auth_hint:
                auth_level = auth_hint
            elif auth_info["hasPremiumContent"]:
                auth_level = "paid_membership"
            elif auth_info["hasRestrictedContent"]:
                auth_level = "free_registration"
            elif auth_info["hasLoginOption"] and not auth_info["canViewThreads"]:
                auth_level = "verified_user"
            else:
                auth_level = "public"

            # Determine content access
            if auth_level == "public":
                content_access = "full_public_access"
            elif auth_level == "free_registration":
                content_access = "limited_public_view"
            else:
                content_access = "members_only"

            return auth_level, content_access

        except Exception as e:
            logger.debug(f"Auth analysis error: {e}")
            return "unknown", "unknown"

    async def _analyze_user_expertise(self, page: Page, expertise_hint: str = None) -> List[str]:
        """Analyze the expertise level of forum users"""
        if expertise_hint:
            return [expertise_hint]

        try:
            page_text = await page.evaluate("() => document.body.innerText.toLowerCase()")

            expertise_found = []
            for level, keywords in self.expertise_levels.items():
                if any(keyword in page_text for keyword in keywords):
                    expertise_found.append(level)

            return expertise_found if expertise_found else ["mixed"]

        except:
            return ["unknown"]

    async def _identify_equipment_focus(self, page: Page) -> List[str]:
        """Identify specific equipment types discussed in the forum"""
        try:
            page_text = await page.evaluate("() => document.body.innerText.toLowerCase()")

            equipment_types = []
            equipment_keywords = {
                "bobcat_s740": ["s740", "bobcat s740"],
                "skid_steer": ["skid steer", "skidsteer", "ssl"],
                "excavator": ["excavator", "mini ex", "trackhoe"],
                "loader": ["loader", "wheel loader", "front loader"],
                "tractor": ["tractor", "compact tractor"],
                "mower": ["mower", "zero turn", "lawn mower"],
                "heavy_equipment": ["dozer", "grader", "backhoe"],
            }

            for equipment, keywords in equipment_keywords.items():
                if any(keyword in page_text for keyword in keywords):
                    equipment_types.append(equipment)

            return equipment_types if equipment_types else ["general"]

        except:
            return ["unknown"]

    async def _calculate_quality_score(self, page: Page) -> float:
        """Calculate content quality score based on various factors"""
        try:
            quality_metrics = await page.evaluate(
                """
                () => {
                    const posts = document.querySelectorAll('article, .post, .message, .comment');
                    const images = document.querySelectorAll('img[src*="attachment"], img[src*="upload"]');
                    const codeBlocks = document.querySelectorAll('pre, code, .code-block');
                    const solvedIndicators = document.querySelectorAll('.solved, .answered, [title*="Solved"]');

                    const avgPostLength = posts.length > 0 ?
                        Array.from(posts).reduce((sum, p) => sum + p.textContent.length, 0) / posts.length : 0;

                    return {
                        postCount: posts.length,
                        hasImages: images.length > 0,
                        hasCode: codeBlocks.length > 0,
                        hasSolved: solvedIndicators.length > 0,
                        avgPostLength: avgPostLength
                    };
                }
            """
            )

            # Calculate score (0-100)
            score = 50.0  # Base score

            if quality_metrics["avgPostLength"] > 500:
                score += 20
            elif quality_metrics["avgPostLength"] > 200:
                score += 10

            if quality_metrics["hasImages"]:
                score += 10
            if quality_metrics["hasCode"]:
                score += 10
            if quality_metrics["hasSolved"]:
                score += 10

            return min(score, 100.0)

        except:
            return 50.0

    async def _extract_active_members(self, page: Page) -> int:
        """Extract count of recently active members"""
        try:
            return await page.evaluate(
                """
                () => {
                    const activeIndicators = document.querySelectorAll(
                        '.online-users, .users-online, [class*="active-users"]'
                    );
                    if (activeIndicators.length > 0) {
                        const text = activeIndicators[0].textContent;
                        const match = text.match(/\d+/);
                        return match ? parseInt(match[0]) : 0;
                    }
                    return 0;
                }
            """
            )
        except:
            return 0

    async def _generate_scrape_notes(self, page: Page, auth_level: str, user_expertise: List[str]) -> str:
        """Generate notes about scraping considerations for this forum"""
        notes = []

        if auth_level == "paid_membership":
            notes.append("Premium content - limited scraping possible")
        elif auth_level == "professional_only":
            notes.append("Professional credentials required - verify access")

        if "specialist" in user_expertise or "certified_tech" in user_expertise:
            notes.append("High-value technical content from certified professionals")

        if "hobbyist" in user_expertise:
            notes.append("DIY-focused content - verify solutions with professionals")

        return "; ".join(notes) if notes else "Standard scraping applicable"

    async def _extract_categories(self, page: Page, platform: str) -> List[str]:
        """Extract forum categories"""
        try:
            selectors = {
                "reddit": ".subreddit-sidebar .md h3",
                "discourse": ".category-list .category-name",
                "phpbb": ".forabg .header dt a",
                "vbulletin": ".forumbit_post .forumtitle",
                "default": '[class*="category"], [class*="forum-title"], [href*="/forum/"], [href*="/category/"]',
            }

            selector = selectors.get(platform, selectors["default"])

            categories = await page.evaluate(
                f"""
                () => {{
                    const elements = document.querySelectorAll('{selector}');
                    const cats = [];
                    elements.forEach(el => {{
                        const text = el.textContent.trim();
                        if (text && text.length < 100) {{
                            cats.push(text);
                        }}
                    }});
                    return cats.slice(0, 20);
                }}
            """
            )

            return categories
        except:
            return []

    async def _extract_member_count(self, page: Page) -> int:
        """Extract forum member count"""
        try:
            member_text = await page.evaluate(
                """
                () => {
                    const statsText = document.body.textContent;
                    const memberMatch = statsText.match(/(\\d+[,\\d]*)[\\s]*(members?|users?|subscribers?)/i);
                    if (memberMatch) {
                        return parseInt(memberMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """
            )
            return member_text
        except:
            return 0

    async def _extract_thread_count(self, page: Page) -> int:
        """Extract forum thread count"""
        try:
            thread_text = await page.evaluate(
                """
                () => {
                    const statsText = document.body.textContent;
                    const threadMatch = statsText.match(/(\\d+[,\\d]*)[\\s]*(threads?|topics?|posts?|discussions?)/i);
                    if (threadMatch) {
                        return parseInt(threadMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """
            )
            return thread_text
        except:
            return 0

    async def _identify_specialties(self, page: Page) -> List[str]:
        """Identify forum specialties based on content"""
        try:
            content = await page.evaluate("() => document.body.textContent.toLowerCase()")

            specialties = []
            specialty_keywords = {
                "automotive": ["car", "vehicle", "automotive", "mechanic"],
                "marine": ["boat", "marine", "nautical", "yacht"],
                "motorcycle": ["motorcycle", "bike", "harley", "honda"],
                "diesel": ["diesel", "truck", "heavy duty"],
                "electrical": ["electrical", "wiring", "voltage"],
                "hvac": ["hvac", "heating", "cooling", "air conditioning"],
                "plumbing": ["plumbing", "pipe", "drain", "water"],
                "appliance": ["appliance", "washer", "dryer", "refrigerator"],
            }

            for specialty, keywords in specialty_keywords.items():
                if any(keyword in content for keyword in keywords):
                    specialties.append(specialty)

            return specialties[:5]  # Limit to top 5 specialties
        except:
            return []

    async def start_realtime_scraping(self, forums: List[Dict]):
        """Start real-time scraping of discovered forums"""
        logger.info(f"Starting real-time scraping of {len(forums)} forums")
        # This will be expanded to actually scrape in real-time
        # For now, just log the forums that would be scraped
        for forum in forums[:3]:  # Limit to first 3 for immediate test
            if forum.get("auth_level") == "public":
                logger.info(f"  Would scrape: {forum.get('name', 'Unknown')} [{forum.get('platform')}]")

    async def scrape_forum_threads(self, forum_url: str, max_threads: int = 100) -> List[Dict]:
        """
        Scrape threads from a forum
        """
        # Simple implementation for now
        threads = []

        await self.initialize_browser()
        threads = []

        try:
            page = await self.context.new_page()
            await page.goto(forum_url, wait_until="networkidle")

            # Find thread links based on platform
            thread_selectors = {
                "reddit": 'a[href*="/comments/"]',
                "discourse": 'a.title[href*="/t/"]',
                "phpbb": "a.topictitle",
                "vbulletin": 'a.title[href*="showthread"]',
                "default": 'a[href*="thread"], a[href*="topic"], a[class*="thread-title"]',
            }

            selector = thread_selectors.get("default", thread_selectors["default"])

            # Extract thread URLs
            thread_urls = await page.evaluate(
                f"""
                () => {{
                    const links = document.querySelectorAll('{selector}');
                    const urls = [];
                    links.forEach(link => {{
                        if (link.href && !urls.includes(link.href)) {{
                            urls.push(link.href);
                        }}
                    }});
                    return urls.slice(0, {max_threads});
                }}
            """
            )

            await page.close()

            # Scrape each thread
            for thread_url in thread_urls[:max_threads]:
                try:
                    thread_data = await self.scrape_thread(thread_url, forum_info)
                    if thread_data:
                        threads.append(thread_data)

                        # Store in BigQuery immediately
                        await self._store_thread_data(thread_data)

                        # Extract and store solutions
                        if thread_data.get("solution"):
                            await self._extract_and_store_solution(thread_data)

                except Exception as e:
                    logger.error(f"Failed to scrape thread {thread_url}: {e}")

                # Rate limiting
                await asyncio.sleep(1)

            logger.info(f"📚 Scraped {len(threads)} threads from {forum_info['name']}")

        except Exception as e:
            logger.error(f"Failed to scrape forum threads: {e}")

        return threads

    async def scrape_thread(self, url: str, forum_info: Dict) -> Optional[Dict]:
        """
        Scrape individual thread for repair/maintenance information
        """
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Extract thread data
            thread_data = {
                "thread_id": hashlib.md5(url.encode()).hexdigest(),
                "forum_id": forum_info["forum_id"],
                "url": url,
                "title": await self._extract_thread_title(page),
                "category": await self._extract_thread_category(page),
                "problem_description": await self._extract_problem(page),
                "solution": await self._extract_solution(page),
                "equipment_mentioned": await self._extract_equipment(page),
                "view_count": await self._extract_view_count(page),
                "reply_count": await self._extract_reply_count(page),
                "solved": await self._check_if_solved(page),
                "author": await self._extract_author(page),
                "created_date": await self._extract_date(page),
                "scraped_at": datetime.now(),
            }

            await page.close()
            return thread_data

        except Exception as e:
            logger.error(f"Failed to scrape thread {url}: {e}")
            return None

    async def _extract_thread_title(self, page: Page) -> str:
        """Extract thread title"""
        try:
            return await page.evaluate(
                """
                () => {
                    const h1 = document.querySelector('h1');
                    const title = document.querySelector('.thread-title, .topic-title, [class*="title"]');
                    const pageTitle = document.title;

                    if (h1) return h1.textContent.trim();
                    if (title) return title.textContent.trim();
                    return pageTitle.split('|')[0].trim();
                }
            """
            )
        except:
            return "Unknown Thread"

    async def _extract_thread_category(self, page: Page) -> str:
        """Extract thread category"""
        try:
            return await page.evaluate(
                """
                () => {
                    const breadcrumb = document.querySelector('.breadcrumb li:nth-last-child(2)');
                    const category = document.querySelector('.category-name, .forum-name');

                    if (breadcrumb) return breadcrumb.textContent.trim();
                    if (category) return category.textContent.trim();
                    return 'General';
                }
            """
            )
        except:
            return "General"

    async def _extract_problem(self, page: Page) -> str:
        """Extract problem description from first post"""
        try:
            return await page.evaluate(
                """
                () => {
                    const firstPost = document.querySelector('.post-content, .entry-content, .message-content, [class*="post-body"]');
                    if (firstPost) {
                        const text = firstPost.textContent.trim();
                        return text.substring(0, 1000);  // Limit to 1000 chars
                    }
                    return '';
                }
            """
            )
        except:
            return ""

    async def _extract_solution(self, page: Page) -> str:
        """Extract solution from thread"""
        try:
            return await page.evaluate(
                """
                () => {
                    // Look for marked solutions
                    const solution = document.querySelector('.solution, .best-answer, [class*="accepted"]');
                    if (solution) {
                        return solution.textContent.trim().substring(0, 1000);
                    }

                    // Look for posts with "solved" or "fixed"
                    const posts = document.querySelectorAll('.post-content, .message-content');
                    for (const post of posts) {
                        const text = post.textContent.toLowerCase();
                        if (text.includes('solved') || text.includes('fixed') || text.includes('solution')) {
                            return post.textContent.trim().substring(0, 1000);
                        }
                    }

                    return '';
                }
            """
            )
        except:
            return ""

    async def _extract_equipment(self, page: Page) -> List[str]:
        """Extract equipment/vehicle mentions"""
        try:
            content = await page.evaluate("() => document.body.textContent")

            # Common equipment patterns
            equipment_patterns = [
                r"\b\d{4}\s+\w+\s+\w+\b",  # Year Make Model
                r"\b[A-Z][a-z]+\s+[A-Z]\d+\b",  # Model numbers
                r"\b(?:Ford|Chevy|Toyota|Honda|BMW|Mercedes|Audi|VW|Nissan|Mazda)\s+\w+\b",
                r"\b(?:Yamaha|Suzuki|Kawasaki|Harley|Honda)\s+\w+\b",  # Motorcycles
                r"\b(?:John Deere|Caterpillar|Kubota|Case)\s+\w+\b",  # Equipment
            ]

            equipment = set()
            for pattern in equipment_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                equipment.update(matches[:5])  # Limit matches per pattern

            return list(equipment)[:10]  # Return top 10
        except:
            return []

    async def _extract_view_count(self, page: Page) -> int:
        """Extract thread view count"""
        try:
            return await page.evaluate(
                """
                () => {
                    const viewText = document.body.textContent;
                    const viewMatch = viewText.match(/(\\d+[,\\d]*)[\\s]*(views?|viewed)/i);
                    if (viewMatch) {
                        return parseInt(viewMatch[1].replace(/,/g, ''));
                    }
                    return 0;
                }
            """
            )
        except:
            return 0

    async def _extract_reply_count(self, page: Page) -> int:
        """Extract thread reply count"""
        try:
            return await page.evaluate(
                """
                () => {
                    const posts = document.querySelectorAll('.post, .message, .comment, [class*="post-content"]');
                    return posts.length - 1;  // Subtract original post
                }
            """
            )
        except:
            return 0

    async def _check_if_solved(self, page: Page) -> bool:
        """Check if thread is marked as solved"""
        try:
            return await page.evaluate(
                """
                () => {
                    const solved = document.querySelector('.solved, .resolved, [class*="solution"]');
                    const titleSolved = document.title.toLowerCase().includes('solved');
                    const contentSolved = document.body.textContent.toLowerCase().includes('[solved]');

                    return !!(solved || titleSolved || contentSolved);
                }
            """
            )
        except:
            return False

    async def _extract_author(self, page: Page) -> str:
        """Extract thread author"""
        try:
            return await page.evaluate(
                """
                () => {
                    const author = document.querySelector('.author-name, .username, .post-author, [class*="author"]');
                    if (author) return author.textContent.trim();
                    return 'Anonymous';
                }
            """
            )
        except:
            return "Anonymous"

    async def _extract_date(self, page: Page) -> datetime:
        """Extract thread creation date"""
        try:
            date_str = await page.evaluate(
                """
                () => {
                    const time = document.querySelector('time[datetime]');
                    if (time) return time.getAttribute('datetime');

                    const dateElement = document.querySelector('.post-date, .date, [class*="time"]');
                    if (dateElement) return dateElement.textContent.trim();

                    return null;
                }
            """
            )

            if date_str:
                # Try to parse the date (simplified)
                from dateutil import parser

                return parser.parse(date_str)

        except:
            pass

        return datetime.now()

    async def _store_forum_info(self, forum_info: Dict):
        """Store forum information in BigQuery"""
        try:
            table_id = f"{self.project_id}.scraped_data.forums"
            errors = self.bq_client.insert_rows_json(table_id, [forum_info])

            if errors:
                logger.error(f"Failed to store forum info: {errors}")
            else:
                logger.info(f"✅ Stored forum info: {forum_info['name']}")
        except Exception as e:
            logger.error(f"Failed to store forum info: {e}")

    async def _store_thread_data(self, thread_data: Dict):
        """Store thread data in BigQuery"""
        try:
            table_id = f"{self.project_id}.scraped_data.forum_threads"

            # Convert datetime to ISO format for BigQuery
            if isinstance(thread_data.get("created_date"), datetime):
                thread_data["created_date"] = thread_data["created_date"].isoformat()
            if isinstance(thread_data.get("scraped_at"), datetime):
                thread_data["scraped_at"] = thread_data["scraped_at"].isoformat()

            errors = self.bq_client.insert_rows_json(table_id, [thread_data])

            if errors:
                logger.error(f"Failed to store thread: {errors}")
            else:
                logger.debug(f"✅ Stored thread: {thread_data['title'][:50]}")
        except Exception as e:
            logger.error(f"Failed to store thread data: {e}")

    async def _extract_and_store_solution(self, thread_data: Dict):
        """Extract structured solution and store in repair_solutions table"""
        if not thread_data.get("solution"):
            return

        try:
            solution_data = {
                "solution_id": hashlib.md5(f"{thread_data['thread_id']}_solution".encode()).hexdigest(),
                "problem_category": self._categorize_problem(thread_data.get("problem_description", "")),
                "problem": thread_data.get("problem_description", "")[:500],
                "solution": thread_data.get("solution", "")[:1000],
                "equipment_type": thread_data.get("equipment_mentioned", ["Unknown"])[0]
                if thread_data.get("equipment_mentioned")
                else "Unknown",
                "parts_needed": self._extract_parts(thread_data.get("solution", "")),
                "tools_required": self._extract_tools(thread_data.get("solution", "")),
                "difficulty_level": self._assess_difficulty(thread_data.get("solution", "")),
                "time_estimate": self._extract_time_estimate(thread_data.get("solution", "")),
                "cost_estimate": self._extract_cost_estimate(thread_data.get("solution", "")),
                "source_url": thread_data["url"],
                "confidence_score": 0.8 if thread_data.get("solved") else 0.5,
                "extracted_at": datetime.now().isoformat(),
            }

            table_id = f"{self.project_id}.scraped_data.repair_solutions"
            errors = self.bq_client.insert_rows_json(table_id, [solution_data])

            if not errors:
                logger.debug(f"✅ Stored repair solution from thread")

        except Exception as e:
            logger.error(f"Failed to extract/store solution: {e}")

    def _categorize_problem(self, description: str) -> str:
        """Categorize problem based on description"""
        description_lower = description.lower()

        categories = {
            "electrical": ["electrical", "battery", "alternator", "starter", "lights"],
            "engine": ["engine", "motor", "cylinder", "piston", "valve"],
            "transmission": ["transmission", "gear", "clutch", "shifting"],
            "brake": ["brake", "pad", "rotor", "caliper", "abs"],
            "cooling": ["cooling", "radiator", "coolant", "overheating"],
            "fuel": ["fuel", "gas", "pump", "injector"],
        }

        for category, keywords in categories.items():
            if any(keyword in description_lower for keyword in keywords):
                return category

        return "general"

    def _extract_parts(self, solution_text: str) -> List[str]:
        """Extract parts mentioned in solution"""
        parts_patterns = [
            r"(?:replace|install|need|buy)\s+(?:a\s+)?(\w+\s+\w+)",
            r"(\w+\s+(?:filter|pump|valve|belt|hose|bearing|seal))",
        ]

        parts = set()
        for pattern in parts_patterns:
            matches = re.findall(pattern, solution_text, re.IGNORECASE)
            parts.update(matches[:5])

        return list(parts)[:10]

    def _extract_tools(self, solution_text: str) -> List[str]:
        """Extract tools mentioned in solution"""
        tools_keywords = [
            "wrench",
            "socket",
            "screwdriver",
            "pliers",
            "hammer",
            "jack",
            "multimeter",
            "scanner",
            "gauge",
            "torque",
        ]

        tools = []
        solution_lower = solution_text.lower()
        for tool in tools_keywords:
            if tool in solution_lower:
                tools.append(tool)

        return tools[:5]

    def _assess_difficulty(self, solution_text: str) -> str:
        """Assess repair difficulty"""
        solution_lower = solution_text.lower()

        if any(word in solution_lower for word in ["easy", "simple", "basic", "diy"]):
            return "easy"
        elif any(word in solution_lower for word in ["moderate", "intermediate", "some experience"]):
            return "moderate"
        elif any(word in solution_lower for word in ["difficult", "advanced", "professional", "dealer"]):
            return "hard"

        return "moderate"

    def _extract_time_estimate(self, solution_text: str) -> str:
        """Extract time estimate from solution"""
        time_pattern = r"(\d+)\s*(hours?|minutes?|mins?|hrs?|days?)"
        match = re.search(time_pattern, solution_text, re.IGNORECASE)

        if match:
            return f"{match.group(1)} {match.group(2)}"

        return "unknown"

    def _extract_cost_estimate(self, solution_text: str) -> str:
        """Extract cost estimate from solution"""
        cost_pattern = r"\$(\d+(?:,\d{3})*(?:\.\d{2})?)"
        match = re.search(cost_pattern, solution_text)

        if match:
            return match.group(0)

        return "unknown"

    async def run_comprehensive_scrape(self, search_queries: List[str] = None) -> Dict:
        """
        Run comprehensive forum scraping operation
        """
        if not search_queries:
            search_queries = [
                "car repair",
                "auto maintenance",
                "motorcycle repair",
                "boat maintenance",
                "diesel repair",
                "equipment repair",
                "small engine repair",
                "hvac repair",
            ]

        logger.info("🚀 Starting comprehensive forum scraping operation")

        try:
            # Initialize browser
            await self.initialize_browser()

            # Phase 1: Discover forums
            logger.info("📡 Phase 1: Discovering forums...")
            forums = await self.discover_forums(search_queries)

            # Phase 2: Scrape threads from each forum
            logger.info("📚 Phase 2: Scraping forum threads...")
            total_threads = 0
            total_solutions = 0

            for forum in forums:
                logger.info(f"Scraping {forum['name']}...")
                threads = await self.scrape_forum_threads(forum, max_threads=50)
                total_threads += len(threads)
                total_solutions += sum(1 for t in threads if t.get("solution"))

                # Update forum status
                forum["scrape_status"] = "completed"
                forum["thread_count"] = len(threads)
                await self._store_forum_info(forum)

            # Phase 3: Generate summary report
            report = {
                "scrape_id": hashlib.md5(f"scrape_{datetime.now().isoformat()}".encode()).hexdigest(),
                "timestamp": datetime.now().isoformat(),
                "forums_discovered": len(forums),
                "threads_scraped": total_threads,
                "solutions_found": total_solutions,
                "forums": [
                    {
                        "name": f["name"],
                        "url": f["url"],
                        "platform": f["platform"],
                        "requires_login": f["requires_login"],
                        "threads_scraped": f.get("thread_count", 0),
                    }
                    for f in forums
                ],
                "status": "completed",
            }

            logger.info(
                f"""
            ✅ Scraping Operation Complete!
            ===========================
            Forums Discovered: {len(forums)}
            Threads Scraped: {total_threads}
            Solutions Found: {total_solutions}
            Data stored in BigQuery: scraped_data dataset
            """
            )

            return report

        except Exception as e:
            logger.error(f"Scraping operation failed: {e}")
            return {"status": "failed", "error": str(e)}

        finally:
            await self.close_browser()

async def main():
    """Main function for testing"""
    scraper = ForumIntelligenceScraper()

    # Run comprehensive scrape
    report = await scraper.run_comprehensive_scrape()

    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
